#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从本机 FM27 simatch.fmf 一次性提取十种官方原生战术预设。

只读游戏安装资源；把游戏内原始 .tac 预设包入已有合法 FM27 .fmf 外壳，
逐份执行 TAC/FM F 回读和角色/职责/PI 权限检查。不会修改游戏文件。
只有完整通过检查的风格才可选择性写入 style_template_registry.json。
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATOR_PATH = HERE / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG_PATH = HERE / "catalog.json"
REGISTRY_PATH = HERE / "style_template_registry.json"
WRAPPER_TEMPLATE = HERE / "123_Game_Export_Reference.fmf"
ZSTD_MAGIC = bytes.fromhex("28b52ffd")


def load_generator(path: Path):
    spec = importlib.util.spec_from_file_location("fm27_native_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 FMF 生成器：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_lp(data: bytes, pos: int) -> tuple[str, int]:
    if pos + 4 > len(data):
        raise ValueError("simatch.fmf TOC 长度前缀越界")
    size = struct.unpack_from("<I", data, pos)[0]
    pos += 4
    if size > 1_000_000 or pos + size > len(data):
        raise ValueError("simatch.fmf TOC 字符串越界")
    return data[pos:pos + size].decode("utf-8"), pos + size


def read_u32(data: bytes, pos: int) -> tuple[int, int]:
    if pos + 4 > len(data):
        raise ValueError("simatch.fmf TOC uint32 越界")
    return struct.unpack_from("<I", data, pos)[0], pos + 4


def parse_simatch_container(data: bytes, gen) -> dict[str, bytes]:
    """读取 FM27 安装资源容器，返回 path -> 解压后的成员字节。"""
    if len(data) < 26 + 9 or not data.startswith(gen.OUTER_MAGIC):
        raise ValueError("不是受支持的 FM27 simatch.fmf 容器")
    size, second, revision = struct.unpack_from("<QQB", data, 9)
    if second != 17 or revision != 3:
        raise ValueError("simatch.fmf 外层版本字段不匹配")
    data_end = 9 + size
    if data_end < 26 or data_end + 9 >= len(data):
        raise ValueError("simatch.fmf 数据区/TOC 偏移越界")
    if data[data_end + 2:data_end + 6] != b"fmf.":
        raise ValueError("simatch.fmf TOC 标记不匹配")
    toc = gen.zstd_decompress(data[data_end + 9:])
    files: dict[str, bytes] = {}
    pos = 0
    visited = 0

    def walk(prefix: str, depth: int) -> None:
        nonlocal pos, visited
        if depth > 64:
            raise ValueError("simatch.fmf 目录嵌套超过安全上限")
        folder, pos = read_lp(toc, pos)
        if not folder or "/" in folder or "\\" in folder or folder in (".", ".."):
            raise ValueError(f"simatch.fmf 非法目录名：{folder!r}")
        current = prefix + folder + "/"
        file_count, pos = read_u32(toc, pos)
        if file_count > 100_000:
            raise ValueError("simatch.fmf 单目录文件数量超过安全上限")
        for _ in range(file_count):
            name, pos = read_lp(toc, pos)
            ext, pos = read_lp(toc, pos)
            if pos + 40 > len(toc):
                raise ValueError("simatch.fmf 文件 TOC 记录越界")
            offset, stored, _meta1, _meta2, _meta3 = struct.unpack_from("<QQQQQ", toc, pos)
            pos += 40
            if not name or "/" in name or "\\" in name or name in (".", ".."):
                raise ValueError(f"simatch.fmf 非法文件名：{name!r}")
            start = 26 + offset
            end = start + stored
            if stored > len(data) or start < 26 or end > data_end:
                raise ValueError(f"simatch.fmf 成员数据越界：{current + name + ext}")
            member = data[start:end]
            plain = gen.zstd_decompress(member) if member.startswith(ZSTD_MAGIC) else member
            files[current + name + ext] = plain
            visited += 1
            if visited > 250_000:
                raise ValueError("simatch.fmf 成员总数超过安全上限")
        directory_count, pos = read_u32(toc, pos)
        if directory_count > 100_000:
            raise ValueError("simatch.fmf 子目录数量超过安全上限")
        for _ in range(directory_count):
            walk(current, depth + 1)

    walk("", 0)
    if pos != len(toc):
        raise ValueError(f"simatch.fmf TOC 尾部有 {len(toc) - pos} 个未解析字节")
    return files


def read_style_folders(styles_xml: bytes) -> dict[str, str]:
    """从 styles.xml 的 folder 属性和 text translation 读取官方风格名称。"""
    try:
        root = ET.fromstring(styles_xml)
    except ET.ParseError as exc:
        raise ValueError(f"simatch/tactics/styles.xml 解析失败：{exc}") from exc
    result = {}
    for record in root.iter("record"):
        folder = record.attrib.get("folder", "").strip()
        if not folder:
            continue
        label = ""
        for translation in record.findall("translation"):
            if translation.attrib.get("id") == "text":
                label = translation.attrib.get("value", "").split("[COMMENT", 1)[0].strip()
                break
        result[folder] = label or folder
    return result


def normalize_style(value: str) -> str:
    value = re.sub(r"^Custom\s+", "", value.strip(), flags=re.I)
    return "".join(ch for ch in value.casefold() if ch.isalnum())


def canonical_style(folder_id: str, display: str, registry: dict) -> str | None:
    aliases = {
        "controlpossession": "Control Possession",
        "gegenpress": "Gegenpress",
        "tikitaka": "Tiki-Taka",
        "verticaltikitaka": "Vertical Tiki-Taka",
        "wingplay": "Wingplay",
        "wingplaystyle": "Wingplay",
        "routeone": "Route One",
        "fluidcounterattack": "Fluid Counter Attack",
        "directcounterattack": "Direct Counter Attack",
        "catenaccio": "Catenaccio",
        "parkthebus": "Park The Bus",
    }
    known = {normalize_style(x["name"]): x["name"] for x in registry.get("styles", [])}
    for candidate in (display, folder_id):
        key = normalize_style(candidate)
        if key in known:
            return known[key]
        if key in aliases:
            return aliases[key]
    return None


def audit_tac(tac, catalog: dict, gen) -> dict:
    positions = {int(x["mask"]): x["id"] for x in catalog["positions"]}
    role_by_flag_phase = {
        (int(x["flags"]), int(x["phase"])): x["id"] for x in catalog["roles"]
    }
    role_eligibility = catalog.get("role_eligibility", {})
    role_duties: dict[str, set[int]] = {}
    issues = []
    phase_rows = []
    for phase, phase_name, attr in ((0, "IP", "ip"), (1, "OOP", "oop")):
        rows = []
        for pair in sorted(tac.pairs, key=lambda x: x.slot):
            block = getattr(pair, attr)
            role_flag = block.mask & gen.ROLE_MASK
            role_id = role_by_flag_phase.get((role_flag, phase))
            position = positions.get(block.selector)
            duty = block.mask & ~gen.ROLE_MASK
            row_issues = []
            if position is None:
                row_issues.append(f"unknown_position:{block.selector}")
            if role_id is None:
                row_issues.append(f"unknown_role_flag:{role_flag:#x}")
            else:
                role_duties.setdefault(role_id, set()).add(duty)
                if duty not in gen.DUTY_FLAGS:
                    row_issues.append(f"unknown_duty:{duty}")
                mapped_duty = gen.ROLE_DUTY.get(role_id)
                if mapped_duty is None:
                    row_issues.append(f"missing_ROLE_DUTY:{role_id}:{duty}")
                elif mapped_duty != duty:
                    row_issues.append(f"ROLE_DUTY_mismatch:{role_id}:{mapped_duty}:{duty}")
                if position is not None:
                    allowed = role_eligibility.get(position, [[], []])
                    if phase >= len(allowed) or role_id not in allowed[phase]:
                        row_issues.append(f"role_position_ineligible:{position}:{role_id}")
            pi_entry = next((x for x in block.items if x["key"] == role_flag), None)
            pi_mask = int(pi_entry["mask2"]) if pi_entry else 0
            policy_key = f"{phase}:{position}:{role_id}:{duty}"
            policies = catalog.get("pi_policies", {}).get(policy_key) if position and role_id else None
            statuses = None
            if not isinstance(policies, dict) or not policies:
                row_issues.append(f"missing_PI_policy:{policy_key}")
            else:
                values = list(policies.values())
                if len(set(values)) != 1:
                    row_issues.append(f"conflicting_PI_policy_versions:{policy_key}")
                else:
                    statuses = values[0]
                    if not isinstance(statuses, str) or not statuses:
                        row_issues.append(f"invalid_PI_policy:{policy_key}")
                    else:
                        for option_id in range(pi_mask.bit_length()):
                            if not (pi_mask >> option_id) & 1:
                                continue
                            if option_id >= len(statuses) or statuses[option_id] != "0":
                                state = statuses[option_id] if option_id < len(statuses) else "out_of_range"
                                row_issues.append(f"PI_not_editable:{policy_key}:{option_id}:{state}")
            issues.extend(f"{phase_name}[{pair.slot}]:{x}" for x in row_issues)
            rows.append({
                "slot": pair.slot,
                "position": position,
                "role": role_id,
                "role_flag_hex": hex(role_flag),
                "duty": duty,
                "pi_mask_hex": hex(pi_mask),
                "pi_count": pi_mask.bit_count(),
                "policy_key": policy_key,
                "issues": row_issues,
            })
        phase_rows.append({"phase": phase_name, "slots": rows})
    return {
        "source_major": tac.magic[11],
        "tac_title": tac.title,
        "tac_style_string": tac.style,
        "style_code_hex": bytes(tac.quad).hex(),
        "team_instruction_bits": [
            bit for bit in range(96)
            if tac.packed[bit // 8] & (1 << (bit % 8))
        ],
        "phases": phase_rows,
        "role_duty_observed": {
            key: sorted(values) for key, values in sorted(role_duties.items())
        },
        "issues": issues,
        "eligible_for_generator": tac.magic[11] == 27 and not issues,
    }


def find_simatch(args) -> Path:
    if args.simatch:
        path = args.simatch.expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"找不到 simatch.fmf：{path}")
        return path
    if not args.game_root:
        raise ValueError("必须提供 --simatch 或 --game-root")
    root = args.game_root.expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"游戏目录不存在：{root}")
    hits = sorted(p for p in root.rglob("simatch.fmf") if p.is_file())
    if not hits:
        raise FileNotFoundError(f"在游戏目录内没有找到 simatch.fmf：{root}")
    preferred = [p for p in hits if "shared" in [x.casefold() for x in p.parts] and "data" in [x.casefold() for x in p.parts]]
    if len(preferred) == 1:
        return preferred[0]
    if len(hits) == 1:
        return hits[0]
    raise ValueError("找到多个 simatch.fmf，请使用 --simatch 指定游戏实际使用的那个：" +
                     "；".join(str(x) for x in hits))


def run_extraction(args) -> dict:
    gen = load_generator(args.generator)
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    simatch_path = find_simatch(args)
    source_bytes = simatch_path.read_bytes()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    members = parse_simatch_container(source_bytes, gen)
    styles_path = next((p for p in ("simatch/tactics/styles.xml", "tactics/styles.xml") if p in members), None)
    if not styles_path:
        raise ValueError("simatch.fmf 中找不到 tactics/styles.xml")
    style_folders = read_style_folders(members[styles_path])
    template_path = args.wrapper_template.expanduser().resolve()
    wrapper = gen.parse_fmf(template_path.read_bytes())
    if not all(x in wrapper.data_by_ext for x in (".tac", ".aom", ".img")):
        raise ValueError("包装模板必须包含 .tac/.aom/.img")
    template_tac = gen.parse_tac(wrapper.data_by_ext[".tac"])
    if template_tac.magic[11] != 27:
        raise ValueError("包装模板不是 FM27 source-major 27")
    output = args.output.expanduser().resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"拒绝覆盖非空输出目录：{output}")
    output.mkdir(parents=True, exist_ok=True)

    candidates = []
    skipped = []
    for archive_path, raw_tac in sorted(members.items()):
        if not archive_path.startswith("simatch/tactics/") or not archive_path.lower().endswith(".tac"):
            continue
        parts = archive_path.split("/")
        if len(parts) < 4:
            continue
        folder_id = parts[2]
        display = style_folders.get(folder_id, folder_id)
        style_name = canonical_style(folder_id, display, registry)
        if style_name is None:
            skipped.append({"path": archive_path, "reason": "unrecognized_style_folder", "display": display})
            continue
        try:
            tac = gen.parse_tac(raw_tac)
            audit = audit_tac(tac, catalog, gen)
            if audit["source_major"] != 27:
                skipped.append({"path": archive_path, "reason": "source_major_not_27", "source_major": audit["source_major"]})
                continue
            title = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "-", f"{style_name} - {tac.title}").strip(" .")
            tac.title = title
            tac_bytes = gen.write_tac(tac)
            output_bytes = gen.write_fmf(wrapper, tac_bytes, title)
            verify_fmf = gen.parse_fmf(output_bytes)
            verify_tac = gen.parse_tac(verify_fmf.data_by_ext[".tac"])
            if verify_tac.title != title or verify_tac.style != audit["tac_style_string"]:
                raise ValueError("生成 FMF 后 TAC 标题/风格字符串回读不一致")
            if bytes(verify_tac.quad).hex() != audit["style_code_hex"]:
                raise ValueError("生成 FMF 后四字节 style code 回读不一致")
            if len(verify_tac.pairs) != 11:
                raise ValueError("生成 FMF 后 11 组双阶段球员槽位回读失败")
            slug = re.sub(r"[^A-Za-z0-9]+", "_", style_name).strip("_")
            stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(parts[-1]).stem).strip("._-")[:72] or "preset"
            filename = f"{slug}__{len([x for x in candidates if x['style'] == style_name]) + 1:03d}__{stem}.fmf"
            candidate_path = output / "candidates" / slug / filename
            candidate_path.parent.mkdir(parents=True, exist_ok=True)
            candidate_path.write_bytes(output_bytes)
            candidates.append({
                "style": style_name,
                "folder_id": folder_id,
                "archive_path": archive_path,
                "source_tac_sha256": hashlib.sha256(raw_tac).hexdigest(),
                "output_file": str(candidate_path),
                "output_file_name": filename,
                "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
                "output_bytes": len(output_bytes),
                **audit,
            })
        except Exception as exc:
            skipped.append({"path": archive_path, "reason": f"{type(exc).__name__}: {exc}"})

    coverage = []
    selected = {}
    for style in registry.get("styles", []):
        name = style["name"]
        rows = [x for x in candidates if x["style"] == name]
        eligible = [x for x in rows if x["eligible_for_generator"]]
        best = sorted(rows, key=lambda x: (not x["eligible_for_generator"], len(x["issues"]), x["archive_path"]))[0] if rows else None
        if eligible:
            selected[name] = sorted(eligible, key=lambda x: (len(x["issues"]), x["archive_path"]))[0]
        coverage.append({
            "style": name,
            "existing_status": style.get("status"),
            "candidate_count": len(rows),
            "eligible_candidate_count": len(eligible),
            "selected_archive_path": selected.get(name, {}).get("archive_path"),
            "selected_style_code_hex": selected.get(name, {}).get("style_code_hex"),
            "selected_tac_style_string": selected.get(name, {}).get("tac_style_string"),
            "status_after_optional_update": "implemented_sample_verified" if name in selected else style.get("status"),
        })

    registry_written = False
    if args.update_registry:
        for style in registry.get("styles", []):
            name = style["name"]
            if style.get("status") == "implemented_sample_verified":
                continue
            candidate = selected.get(name)
            if not candidate:
                continue
            template_name = f"FM27_{re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_')}_Native_Template.fmf"
            target = HERE / template_name
            if target.exists():
                raise FileExistsError(f"拒绝覆盖已存在模板：{target}")
            shutil.copyfile(candidate["output_file"], target)
            style["status"] = "implemented_sample_verified"
            style["style_code_hex"] = candidate["style_code_hex"]
            style["tac_style_string"] = candidate["tac_style_string"]
            style["template"] = template_name
            evidence = style.setdefault("evidence", {})
            evidence.update({
                "source": "Extracted from the user's local FM27 installation simatch.fmf; original native TAC preset, source-major 27.",
                "simatch_path_at_extraction": str(simatch_path),
                "simatch_sha256": source_sha,
                "source_tac_path": candidate["archive_path"],
                "source_tac_sha256": candidate["source_tac_sha256"],
                "extracted_fmf_sha256": candidate["output_sha256"],
                "role_position_pairs": "All 22 IP/OOP position-role pairs matched the current catalog and role_eligibility table.",
                "pi_permission_validation": "All active serialized PI bits passed catalog.pi_policies for phase/position/role/duty.",
                "offline_status": "offline_binary_roundtrip_verified_not_game_import_verified",
                "game_import": "not_verified",
            })
        args.registry.expanduser().resolve().write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        registry_written = True

    manifest = {
        "schema": "fm27-installed-preset-extraction-v1",
        "source": str(simatch_path),
        "source_sha256": source_sha,
        "source_bytes": len(source_bytes),
        "wrapper_template": str(template_path),
        "wrapper_template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
        "member_count": len(members),
        "style_folder_count": len(style_folders),
        "candidate_count": len(candidates),
        "skipped_count": len(skipped),
        "registry_updated": registry_written,
        "style_coverage": coverage,
        "candidates": candidates,
        "skipped": skipped,
        "limitations": [
            "只读取本机 FM27 安装资源 simatch.fmf，不修改游戏文件。",
            "提取的 TAC 来自原生游戏预设；FMF 外层使用仓库内已验证的 FM27 原生包装模板。",
            "eligible_for_generator 只表示离线结构、角色/职责映射和当前 PI 权限策略通过，不代表已在游戏内导入。",
            "游戏内导入和比赛引擎效果仍需独立验证。",
        ],
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    proposal = {
        "schema": "fm27-role-duty-proposals-v1",
        "observed": {
            role: sorted({d for c in candidates for role2, ds in c["role_duty_observed"].items() if role2 == role for d in ds})
            for role in sorted({role for c in candidates for role in c["role_duty_observed"]})
        },
        "missing_or_conflicting": sorted({
            issue for c in candidates for issue in c["issues"]
            if "ROLE_DUTY" in issue or "missing_PI_policy" in issue or "unknown_role_flag" in issue
        }),
    }
    (output / "role_duty_and_policy_gaps.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    zip_path = output / "FM27_Installed_Native_Preset_Bundle.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(output.rglob("*")):
            if file.is_file() and file != zip_path:
                archive.write(file, file.relative_to(output))
    return manifest


def self_test(gen) -> None:
    """无游戏文件的最小容器回归，验证 TOC 递归、偏移和 Zstandard 成员解包。"""
    payload = b"<styles><record folder='tiki_taka'><translation id='text' value='Tiki-Taka'/></record></styles>"
    compressed = gen.zstd_raw_frame(payload)
    toc = bytearray(gen.lp_write("simatch"))
    toc += struct.pack("<I", 0) + struct.pack("<I", 1)
    toc += gen.lp_write("tactics") + struct.pack("<I", 1)
    toc += gen.lp_write("styles") + gen.lp_write(".xml")
    toc += struct.pack("<QQQQQ", 0, len(compressed), len(payload), 0, 0)
    toc += struct.pack("<I", 0)
    body = compressed
    outer = gen.OUTER_MAGIC + struct.pack("<QQB", 17 + len(body), 17, 3) + body
    archive = outer + gen.INNER_MAGIC + gen.zstd_raw_frame(bytes(toc))
    parsed = parse_simatch_container(archive, gen)
    assert parsed["simatch/tactics/styles.xml"] == payload
    styles = read_style_folders(parsed["simatch/tactics/styles.xml"])
    assert styles["tiki_taka"] == "Tiki-Taka"
    print("PASS: simatch.fmf TOC recursion, Zstandard member decode, and styles.xml mapping")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simatch", type=Path, help="FM27 安装目录中的 simatch.fmf")
    ap.add_argument("--game-root", type=Path, help="FM27 游戏根目录；自动递归查找 simatch.fmf")
    ap.add_argument("--generator", type=Path, default=GENERATOR_PATH)
    ap.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    ap.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    ap.add_argument("--wrapper-template", type=Path, default=WRAPPER_TEMPLATE)
    ap.add_argument("--output", type=Path, default=HERE / "native_preset_extraction")
    ap.add_argument("--update-registry", action="store_true",
                    help="仅将通过 22 组角色/职责和 PI 权限检查的风格写入本地 registry")
    ap.add_argument("--self-test", action="store_true", help="运行不需要游戏文件的容器解析自测")
    args = ap.parse_args()
    try:
        gen = load_generator(args.generator)
        if args.self_test:
            self_test(gen)
            return 0
        manifest = run_extraction(args)
        print(json.dumps({
            "output": str(args.output.expanduser().resolve()),
            "source_sha256": manifest["source_sha256"],
            "candidate_count": manifest["candidate_count"],
            "skipped_count": manifest["skipped_count"],
            "registry_updated": manifest["registry_updated"],
            "style_coverage": manifest["style_coverage"],
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"失败：{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
