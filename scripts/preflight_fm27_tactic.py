#!/usr/bin/env python3
"""Fast, catalog-backed preflight for a deliverable FM27 tactic recipe."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


def preflight(recipe: dict, catalog: dict, style_registry: dict) -> dict:
    gen.validate_recipe_structure(recipe)
    gen.resolve_style_definition(str(recipe["base"]["g"]), style_registry)
    gen.encode_ti(recipe, catalog, bytearray(12))

    positions = {item["id"]: int(item["mask"]) for item in catalog["positions"]}
    roles = {item["id"]: item for item in catalog["roles"]}
    eligibility = catalog.get("role_eligibility", {})
    empty_pi = []
    checked = []

    for slot, spec in enumerate(recipe["p"]):
        for phase, phase_key in ((0, "in"), (1, "out")):
            item = spec[phase_key]
            pos_name = str(item["pos"])
            pos_id = gen.native_position_id(pos_name, phase)
            if pos_id not in positions:
                raise ValueError(f"slot {slot} {phase_key}: unknown native position {pos_name!r}")

            role_id = gen.role_id_from_display(str(item["role"]), phase, set(roles))
            role = roles[role_id]
            if int(role["phase"]) != phase:
                raise ValueError(f"slot {slot} {phase_key}: role phase mismatch: {role_id}")
            if role_id not in eligibility.get(pos_id, [[], []])[phase]:
                raise ValueError(f"slot {slot} {phase_key}: incompatible position/role {pos_name}/{role_id}")

            duty = gen.resolve_role_duty(role_id, item)
            gen.encode_pi(item["pi"], catalog, phase, pos_id, role_id, duty)
            if not item["pi"]:
                empty_pi.append(f"slot {slot} {phase_key}")
            checked.append({"slot": slot, "phase": phase_key, "position": pos_name, "role": role_id})

    if empty_pi:
        raise ValueError("22/22 PI completeness failed; empty: " + ", ".join(empty_pi))

    return {
        "status": "preflight_passed",
        "catalog_schema_version": catalog.get("schema_version"),
        "catalog_source_bundle_sha256": catalog.get("source_bundle_sha256"),
        "checked_phases": len(checked),
        "non_empty_pi_phases": len(checked),
        "roles": checked,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe", type=Path)
    parser.add_argument("--catalog", type=Path, default=GEN_DIR / "catalog.json")
    parser.add_argument("--style-registry", type=Path, default=GEN_DIR / "style_template_registry.json")
    args = parser.parse_args()
    recipe = json.loads(args.recipe.read_text(encoding="utf-8")) if args.recipe else json.loads(__import__("os").environ["RECIPE_JSON"])
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    registry = json.loads(args.style_registry.read_text(encoding="utf-8"))
    report = preflight(recipe, catalog, registry)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(f"FM27 tactic preflight failed: {type(exc).__name__}: {exc}") from exc
