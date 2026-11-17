#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit all 90 Netlify-listed FM27 presets against the native role catalog.

This verifies position aliases, phase-specific role IDs, role/position eligibility,
the D/S/A duty values recorded in the source index, and the existence of matching
catalog PI-policy rows. It does not infer native TAC style FourCCs or claim that
website-index records are raw FM27 .fmf exports.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES_DIR = HERE.parent
INDEX_DIR = RULES_DIR / "01_网站生成规则"
INDEX_PATH = INDEX_DIR / "Netlify_90官方预设索引.csv"
ROLE_INDEX_PATH = INDEX_DIR / "Netlify_角色显示名称索引.csv"
GENERATOR_PATH = HERE / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG_PATH = HERE / "catalog.json"

EXPECTED_STYLES = (
    "Catenaccio",
    "Control Possession",
    "Direct Counter Attack",
    "Fluid Counter Attack",
    "Gegenpress",
    "Park The Bus",
    "Route One",
    "Tiki-Taka",
    "Vertical Tiki-Taka",
    "Wingplay",
)
DUTY_BITS = {"D": 2097152, "S": 4194304, "A": 8388608}


def load_generator(path: Path):
    spec = importlib.util.spec_from_file_location("fm27_native_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载生成器模块：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_role_names(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = {}
    for row in rows:
        ident = int(row["index"])
        name = row["role_display_name"].strip()
        if ident in result or not name:
            raise ValueError(f"角色显示名称索引重复或为空：{ident}")
        result[ident] = name
    return result


def audit_official_index(
    index_path: Path = INDEX_PATH,
    role_index_path: Path = ROLE_INDEX_PATH,
    generator_path: Path = GENERATOR_PATH,
    catalog_path: Path = CATALOG_PATH,
) -> dict:
    gen = load_generator(generator_path)
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    role_names = read_role_names(role_index_path)
    roles = {item["id"]: item for item in catalog["roles"]}
    positions = {item["id"] for item in catalog["positions"]}
    eligibility = catalog.get("role_eligibility", {})
    pi_policies = catalog.get("pi_policies", {})

    errors: list[dict] = []
    rows: list[dict] = []
    style_counts: Counter[str] = Counter()
    position_aliases: Counter[str] = Counter()
    role_coverage: dict[str, set[str]] = defaultdict(set)
    duty_coverage: dict[str, set[str]] = defaultdict(set)
    total_phase_slots = 0

    with index_path.open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))

    seen_ids = set()
    for row in source_rows:
        preset_id = str(row.get("preset_id", "")).strip()
        style = str(row.get("style_group", "")).strip()
        if not preset_id or preset_id in seen_ids:
            errors.append({"preset": preset_id, "error": "missing_or_duplicate_preset_id"})
            continue
        seen_ids.add(preset_id)
        style_counts[style] += 1

        compact = str(row.get("player_assignments_compact", "")).strip()
        assignments = compact.split()
        if len(assignments) != 11:
            errors.append({
                "preset": preset_id,
                "style": style,
                "error": f"expected_11_slots_got_{len(assignments)}",
            })
            continue

        used_positions = {0: set(), 1: set()}
        slot_rows = []
        for slot, packed in enumerate(assignments):
            parts = packed.split(",")
            if len(parts) != 6:
                errors.append({
                    "preset": preset_id,
                    "style": style,
                    "slot": slot,
                    "error": f"expected_6_compact_fields_got_{len(parts)}",
                })
                continue

            for phase, pos_index, role_index, duty_index in (
                (0, 0, 1, 2),
                (1, 3, 4, 5),
            ):
                phase_name = "IP" if phase == 0 else "OOP"
                source_pos = parts[pos_index].strip()
                native_pos = gen.native_position_id(source_pos, phase)
                duty_label = parts[duty_index].strip()
                role_index_text = parts[role_index].strip()
                try:
                    display = role_names[int(role_index_text)]
                    role_id = gen.role_id_from_display(display, phase, set(roles))
                except (ValueError, KeyError) as exc:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"role_mapping_failed:{exc}",
                    })
                    continue

                if source_pos != native_pos:
                    position_aliases[f"{source_pos}->{native_pos}"] += 1
                if native_pos not in positions:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"unknown_position:{source_pos}->{native_pos}",
                    })
                    continue

                role = roles[role_id]
                if int(role["phase"]) != phase:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"role_phase_mismatch:{role_id}",
                    })

                allowed_phases = eligibility.get(native_pos)
                if (
                    not isinstance(allowed_phases, list)
                    or len(allowed_phases) <= phase
                    or role_id not in allowed_phases[phase]
                ):
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"role_position_ineligible:{native_pos}:{role_id}",
                    })

                if duty_label not in DUTY_BITS:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"unknown_duty_label:{duty_label}",
                    })
                    continue
                duty = DUTY_BITS[duty_label]
                mapped_duty = gen.ROLE_DUTY.get(role_id)
                if mapped_duty is None:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"missing_role_duty:{role_id}",
                    })
                elif mapped_duty != duty:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"role_duty_conflict:{role_id}:{mapped_duty}:{duty}",
                    })

                policy_key = f"{phase}:{native_pos}:{role_id}:{duty}"
                policy = pi_policies.get(policy_key)
                if not isinstance(policy, dict) or not policy:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"missing_pi_policy:{policy_key}",
                    })
                else:
                    policy_versions = list(policy.values())
                    invalid_versions = [
                        value for value in policy_versions
                        if not isinstance(value, str) or not value or set(value) - set("0123")
                    ]
                    if invalid_versions:
                        errors.append({
                            "preset": preset_id,
                            "style": style,
                            "slot": slot,
                            "phase": phase_name,
                            "error": f"invalid_pi_policy_versions:{policy_key}",
                        })

                if native_pos in used_positions[phase]:
                    errors.append({
                        "preset": preset_id,
                        "style": style,
                        "slot": slot,
                        "phase": phase_name,
                        "error": f"duplicate_position:{native_pos}",
                    })
                used_positions[phase].add(native_pos)
                role_coverage[phase_name].add(role_id)
                duty_coverage[f"{phase_name}:{role_id}"].add(duty_label)
                slot_rows.append({
                    "slot": slot,
                    "phase": phase_name,
                    "source_position": source_pos,
                    "native_position": native_pos,
                    "role_display": display,
                    "role_id": role_id,
                    "duty": duty_label,
                    "pi_policy_key": policy_key,
                })
                total_phase_slots += 1

        for phase, phase_name in ((0, "IP"), (1, "OOP")):
            if len(used_positions[phase]) != 11:
                errors.append({
                    "preset": preset_id,
                    "style": style,
                    "phase": phase_name,
                    "error": f"expected_11_unique_positions_got_{len(used_positions[phase])}",
                })

        rows.append({
            "preset_id": preset_id,
            "style": style,
            "ip_formation": row.get("ip_formation", ""),
            "oop_formation": row.get("oop_formation", ""),
            "mentality": row.get("mentality", ""),
            "slots": slot_rows,
        })

    missing_styles = sorted(set(EXPECTED_STYLES) - set(style_counts))
    unexpected_styles = sorted(set(style_counts) - set(EXPECTED_STYLES))
    if len(source_rows) != 90:
        errors.append({"error": f"expected_90_presets_got_{len(source_rows)}"})
    if missing_styles:
        errors.append({"error": "missing_styles", "styles": missing_styles})
    if unexpected_styles:
        errors.append({"error": "unexpected_styles", "styles": unexpected_styles})
    for style in EXPECTED_STYLES:
        if style_counts[style] != 9:
            errors.append({
                "style": style,
                "error": f"expected_9_presets_got_{style_counts[style]}",
            })

    return {
        "schema": "fm27-netlify-90-official-index-audit-v1",
        "status": (
            "website_index_role_position_duty_and_pi_policy_audit_passed"
            if not errors else "audit_failed"
        ),
        "source": str(index_path),
        "source_boundary": (
            "The index records website-exposed official-preset data. This audit "
            "does not prove raw native TAC style FourCCs, native template bytes, "
            "or successful in-game FMF import."
        ),
        "preset_count": len(source_rows),
        "style_count": len(style_counts),
        "style_counts": dict(sorted(style_counts.items())),
        "phase_slot_count": total_phase_slots,
        "role_coverage": {
            phase: sorted(values) for phase, values in sorted(role_coverage.items())
        },
        "role_phase_pair_count": len(duty_coverage),
        "website_position_aliases": dict(sorted(position_aliases.items())),
        "errors": errors,
        "presets": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=INDEX_PATH)
    parser.add_argument("--role-index", type=Path, default=ROLE_INDEX_PATH)
    parser.add_argument("--generator", type=Path, default=GENERATOR_PATH)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        report = audit_official_index(
            args.index, args.role_index, args.generator, args.catalog
        )
        if args.output:
            target = args.output.expanduser().resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        print(json.dumps({
            "status": report["status"],
            "preset_count": report["preset_count"],
            "style_count": report["style_count"],
            "style_counts": report["style_counts"],
            "phase_slot_count": report["phase_slot_count"],
            "role_phase_pair_count": report["role_phase_pair_count"],
            "position_aliases": report["website_position_aliases"],
            "error_count": len(report["errors"]),
            "errors_preview": report["errors"][:20],
            "output": str(args.output.resolve()) if args.output else None,
        }, ensure_ascii=False, indent=2))
        return 0 if not report["errors"] else 1
    except Exception as exc:
        print(f"失败：{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
