#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读扫描 FM27 原生 .fmf 样本，提取可复核的风格标识与模板指纹。

本工具不修改战术、不生成 FMF，也不会根据战术指令猜测风格 ID。
只有真实 FM27 原生文件中读出的 TAC style 字符串和四字节 style code
才可作为新风格映射证据。
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG = HERE / "catalog.json"
REGISTRY = HERE / "style_template_registry.json"


def load_generator(path: Path):
    spec = importlib.util.spec_from_file_location("fm27_native_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载生成器模块：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def normalize_style(value: str) -> str:
    value = re.sub(r"^Custom\s+", "", value.strip(), flags=re.I)
    return "".join(ch for ch in value.casefold() if ch.isalnum())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True,
                    help="包含 FM27 原生 .fmf 样本的目录；递归扫描")
    ap.add_argument("--generator", type=Path, default=GENERATOR)
    ap.add_argument("--catalog", type=Path, default=CATALOG)
    ap.add_argument("--registry", type=Path, default=REGISTRY)
    ap.add_argument("--output", type=Path, default=Path("style_template_audit.json"))
    args = ap.parse_args()

    gen = load_generator(args.generator)
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    positions = {int(x["mask"]): x["id"] for x in catalog["positions"]}
    role_by_flag_phase = {
        (int(x["flags"]), int(x["phase"])): x["id"]
        for x in catalog["roles"]
    }

    known_styles = {}
    for item in registry["styles"]:
        candidates = [item.get("name", ""), item.get("tac_style_string") or ""]
        candidates.extend(item.get("tac_style_aliases", []))
        for candidate in candidates:
            key = normalize_style(candidate)
            if key:
                known_styles[key] = item
    samples = []
    errors = []
    for path in sorted(args.root.rglob("*.fmf")):
        try:
            raw = path.read_bytes()
            archive = gen.parse_fmf(raw)
            tac_raw = archive.data_by_ext[".tac"]
            tac = gen.parse_tac(tac_raw)
            phases = []
            for phase, phase_name in ((0, "IP"), (1, "OOP")):
                rows = []
                for pair in sorted(tac.pairs, key=lambda p: p.slot):
                    block = pair.ip if phase == 0 else pair.oop
                    role_flag = block.mask & gen.ROLE_MASK
                    rows.append({
                        "slot": pair.slot,
                        "position": positions.get(block.selector, f"UNKNOWN:{block.selector}"),
                        "role": role_by_flag_phase.get((role_flag, phase), f"UNKNOWN:{role_flag}"),
                        "role_flag_hex": hex(role_flag),
                        "duty_bits": block.mask & ~gen.ROLE_MASK,
                        "pi_cache_entries": [
                            {
                                "role_flag_hex": hex(item["key"]),
                                "pi_mask_hex": hex(item["mask2"]),
                                "value": item["value"],
                            }
                            for item in block.items
                        ],
                    })
                phases.append({"phase": phase_name, "slots": rows})

            style_key = normalize_style(tac.style)
            matched = known_styles.get(style_key)
            samples.append({
                "file": str(path.resolve()),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "source_major": tac_raw[11],
                "tac_title": tac.title,
                "tac_style_string": tac.style,
                "style_code_hex": bytes(tac.quad).hex(),
                "style_code_ascii": bytes(tac.quad).decode("ascii", "replace"),
                "recognized_registry_style": matched["name"] if matched else None,
                "team_instruction_bits": [
                    bit for bit in range(96)
                    if tac.packed[bit // 8] & (1 << (bit % 8))
                ],
                "phases": phases,
                "template_eligible_candidate": tac_raw[11] == 27,
                "note": "候选模板；仍须单独验证 TI/PI 权限、模板成员与实际导入。",
            })
        except Exception as exc:
            errors.append({"file": str(path), "error": f"{type(exc).__name__}: {exc}"})

    coverage = []
    for item in registry["styles"]:
        keys = {
            normalize_style(item.get("name", "")),
            normalize_style(item.get("tac_style_string") or ""),
            *(normalize_style(x) for x in item.get("tac_style_aliases", [])),
        }
        keys.discard("")
        matched = [x["file"] for x in samples if normalize_style(x["tac_style_string"]) in keys]
        coverage.append({
            "style": item["name"],
            "status": "sample_found" if matched else item["status"],
            "sample_count": len(matched),
            "samples": matched,
            "style_code_hex": item.get("style_code_hex"),
        })

    report = {
        "schema": "fm27-style-template-audit-v1",
        "read_only": True,
        "root": str(args.root.resolve()),
        "sample_count": len(samples),
        "error_count": len(errors),
        "style_coverage": coverage,
        "samples": samples,
        "errors": errors,
        "limitations": [
            "仅从原生文件读取风格字符串与四字节 style code，不推测未知映射。",
            "发现某风格样本不等于该风格已获生成器支持。",
            "候选模板还需验证 FM27 build、TI/PI 权限、职责映射及游戏内导入。",
        ],
    }
    out = args.output.expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "sample_count": len(samples),
        "error_count": len(errors),
        "style_coverage": coverage,
    }, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
