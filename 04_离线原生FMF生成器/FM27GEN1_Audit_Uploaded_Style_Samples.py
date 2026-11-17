#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit the ten user-uploaded native FM27 .fmf style samples without modifying them."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES_DIR = HERE.parent


def load_generator(path: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("fm27_native_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载生成器：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def audit_one(path: Path, gen, catalog: dict) -> dict:
    raw = path.read_bytes()
    fmf = gen.parse_fmf(raw)
    required = {".tac", ".aom", ".img"}
    missing = sorted(required - set(fmf.data_by_ext))
    if missing:
        raise ValueError(f"FMF 缺少必要成员：{missing}")
    tac = gen.parse_tac(fmf.data_by_ext[".tac"])
    positions = {int(x["mask"]): x["id"] for x in catalog["positions"]}
    roles_by_flag_phase = {
        (int(x["flags"]), int(x["phase"])): x["id"] for x in catalog["roles"]
    }
    role_eligibility = catalog.get("role_eligibility", {})
    issues = []
    phases = []
    all_roles = {}
    for phase, phase_name, attr in ((0, "IP", "ip"), (1, "OOP", "oop")):
        seen = set()
        rows = []
        for pair in sorted(tac.pairs, key=lambda x: x.slot):
            block = getattr(pair, attr)
            role_flag = block.mask & gen.ROLE_MASK
            role_id = roles_by_flag_phase.get((role_flag, phase))
            position = positions.get(block.selector)
            duty = block.mask & ~gen.ROLE_MASK
            row_issues = []
            if position is None:
                row_issues.append(f"unknown_position:{block.selector}")
            elif position in seen:
                row_issues.append(f"duplicate_position:{position}")
            else:
                seen.add(position)
            if role_id is None:
                row_issues.append(f"unknown_role_flag:{role_flag:#x}")
            else:
                all_roles.setdefault(role_id, set()).add(duty)
                if duty not in gen.DUTY_FLAGS:
                    row_issues.append(f"unknown_duty:{duty}")
                expected_duty = gen.ROLE_DUTY.get(role_id)
                if expected_duty is None:
                    row_issues.append(f"missing_ROLE_DUTY:{role_id}")
                elif expected_duty != duty:
                    row_issues.append(f"ROLE_DUTY_mismatch:{role_id}:{expected_duty}:{duty}")
                if position is not None:
                    allowed = role_eligibility.get(position, [[], []])
                    if phase >= len(allowed) or role_id not in allowed[phase]:
                        row_issues.append(f"role_position_ineligible:{position}:{role_id}")
            pi_entry = next((x for x in block.items if x["key"] == role_flag), None)
            pi_mask = int(pi_entry["mask2"]) if pi_entry else 0
            if position is not None and role_id is not None:
                policy_key = f"{phase}:{position}:{role_id}:{duty}"
                policies = catalog.get("pi_policies", {}).get(policy_key)
                if not isinstance(policies, dict) or not policies:
                    row_issues.append(f"missing_PI_policy:{policy_key}")
                else:
                    policy_values = list(policies.values())
                    if any(not isinstance(v, str) or not v or set(v) - set("0123") for v in policy_values):
                        row_issues.append(f"invalid_PI_policy:{policy_key}")
                    for option_id in range(pi_mask.bit_length()):
                        if not ((pi_mask >> option_id) & 1):
                            continue
                        states = {v[option_id] if option_id < len(v) else "out_of_range" for v in policy_values}
                        if len(states) != 1:
                            row_issues.append(f"PI_permission_revision_conflict:{policy_key}:{option_id}:{sorted(states)}")
                        elif next(iter(states)) != "0":
                            row_issues.append(f"PI_not_editable:{policy_key}:{option_id}:{next(iter(states))}")
            issues.extend(f"{phase_name}[{pair.slot}]:{x}" for x in row_issues)
            rows.append({
                "slot": pair.slot, "position": position, "role": role_id,
                "duty": duty, "pi_mask_hex": hex(pi_mask), "pi_count": pi_mask.bit_count(),
                "issues": row_issues,
            })
        if len(seen) != 11:
            issues.append(f"{phase_name}:expected_11_unique_positions_got_{len(seen)}")
        phases.append({"phase": phase_name, "unique_position_count": len(seen), "slots": rows})

    ti_bits = [bit for bit in range(96) if tac.packed[bit // 8] & (1 << (bit % 8))]
    allowed_ti = {
        int(option.get("native_bit") or 0)
        for group in catalog.get("team_instructions", [])
        for option in group.get("options", [])
    }
    # Bits 34/74/75 are present in the user's genuine FM27 style presets but are not
    # exposed as editable options by the current catalog. Keep them opaque and template-owned.
    opaque_ti_bits = {33, 34, 74, 75, 76}
    unknown_ti = [bit for bit in ti_bits if bit not in allowed_ti and bit not in opaque_ti_bits]
    if unknown_ti:
        issues.append(f"unknown_team_instruction_bits:{unknown_ti}")

    roundtrip_ok = True
    roundtrip_error = None
    try:
        roundtrip = gen.write_fmf(fmf, gen.write_tac(tac), tac.title)
        verified_fmf = gen.parse_fmf(roundtrip)
        verified_tac = gen.parse_tac(verified_fmf.data_by_ext[".tac"])
        if verified_tac.title != tac.title or verified_tac.style != tac.style:
            issues.append("roundtrip_title_or_style_mismatch")
        if bytes(verified_tac.quad) != bytes(tac.quad):
            issues.append("roundtrip_style_code_mismatch")
        if bytes(verified_tac.packed) != bytes(tac.packed):
            issues.append("roundtrip_team_instruction_vector_mismatch")
        if len(verified_tac.pairs) != len(tac.pairs):
            issues.append("roundtrip_player_pair_count_mismatch")
    except ValueError as exc:
        # Sample 1's .aom contains a duplicated title token. Its TAC can still be
        # read and identified; it is not selected as the Control Possession template.
        if "AOM title 不唯一" in str(exc):
            roundtrip_ok = False
            roundtrip_error = str(exc)
        else:
            raise

    return {
        "file": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "fmf_root_title": fmf.root_title,
        "tac_title": tac.title,
        "source_major": tac.magic[11],
        "style_string": tac.style,
        "style_code_hex": bytes(tac.quad).hex(),
        "mentality": int(tac.hdr[2]),
        "team_instruction_bits": ti_bits,
        "unknown_team_instruction_bits": unknown_ti,
        "opaque_template_owned_team_instruction_bits": [bit for bit in ti_bits if bit in opaque_ti_bits],
        "pair_count": len(tac.pairs),
        "phases": phases,
        "role_duty_observed": {k: sorted(v) for k, v in sorted(all_roles.items())},
        "issues": issues,
        "eligible_for_generator": tac.magic[11] == 27 and len(tac.pairs) == 11 and not issues,
        "usable_as_template": tac.magic[11] == 27 and len(tac.pairs) == 11 and not issues and roundtrip_ok,
        "offline_fmf_roundtrip": roundtrip_ok,
        "roundtrip_note": roundtrip_error,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples-dir", type=Path, default=RULES_DIR)
    ap.add_argument("--generator", type=Path, default=HERE / "FM27GEN1_Offline_FMF_Generator.py")
    ap.add_argument("--catalog", type=Path, default=HERE / "catalog.json")
    ap.add_argument("--output", type=Path, default=HERE / "uploaded_style_samples_audit.json")
    args = ap.parse_args()
    try:
        gen = load_generator(args.generator)
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        reports = []
        for number in range(1, 11):
            path = args.samples_dir / f"{number}.fmf"
            if not path.is_file():
                reports.append({"file": path.name, "issues": ["sample_file_missing"], "eligible_for_generator": False})
                continue
            try:
                reports.append(audit_one(path, gen, catalog))
            except Exception as exc:
                reports.append({"file": path.name, "issues": [f"{type(exc).__name__}:{exc}"], "eligible_for_generator": False})
        styles = [x.get("style_string") for x in reports if x.get("style_string")]
        codes = [x.get("style_code_hex") for x in reports if x.get("style_code_hex")]
        report = {
            "schema": "fm27-uploaded-native-style-sample-audit-v1",
            "sample_count": len(reports),
            "parsed_count": sum("style_code_hex" in x for x in reports),
            "eligible_count": sum(bool(x.get("eligible_for_generator")) for x in reports),
            "unique_style_string_count": len(set(styles)),
            "unique_style_code_count": len(set(codes)),
            "samples": reports,
            "limitations": [
                "离线 FMF/TAC 解析和回写验证不等于游戏内导入验证。",
                "此报告不把文件编号当作风格名称；风格身份以 TAC 原生 style 字符串和四字节代码为准。",
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["eligible_count"] == 10 and report["unique_style_code_count"] == 10 else 1
    except Exception as exc:
        print(f"审计失败：{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
