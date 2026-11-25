#!/usr/bin/env python3
"""Catalog-backed preflight for an FM27 tactic recipe; empty PI arrays are valid."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


# These roles are position-compatible in the native catalogue, but only valid
# when the phase shape contains a three-centre-back line. Catalogue eligibility
# does not encode this formation-level condition.
THREE_BACK_OUTER_CENTRE_BACK_ROLES = {
    0: {"WideCentreBack", "OverlappingCentreBack"},
    1: {"OPWideCentreBack", "OPCoveringWideCentreBack", "OPStoppingWideCentreBack"},
}
CENTRE_BACK_POSITIONS = {"DC", "DCL", "DCR"}
OUTER_CENTRE_BACK_POSITIONS = {"DCL", "DCR"}


def validate_formation_role_compatibility(phase_items: list[dict], phase: int) -> dict:
    """Reject roles that require an outer centre-back in a back-three shape."""
    phase_name = "in-possession" if phase == 0 else "out-of-possession"
    centre_back_positions = [
        str(item["pos"]) for item in phase_items
        if str(item["pos"]) in CENTRE_BACK_POSITIONS
    ]
    special_roles = THREE_BACK_OUTER_CENTRE_BACK_ROLES.get(phase, set())

    checked = []
    for item in phase_items:
        pos = str(item["pos"])
        role_id = str(item["role"])
        if role_id not in special_roles:
            continue
        if pos not in OUTER_CENTRE_BACK_POSITIONS:
            raise ValueError(
                f"{phase_name}: {role_id} requires an outer centre-back slot (DCL/DCR); "
                f"found {pos}"
            )
        if len(centre_back_positions) != 3:
            raise ValueError(
                f"{phase_name}: {role_id} is only available to an outer centre-back "
                "in a back-three shape; "
                f"found {len(centre_back_positions)} centre-back slots "
                f"({', '.join(centre_back_positions) or 'none'})"
            )
        checked.append({"position": pos, "role": role_id})

    return {
        "phase": phase_name,
        "centre_back_positions": centre_back_positions,
        "centre_back_count": len(centre_back_positions),
        "formation_dependent_roles": checked,
    }


def preflight(recipe: dict, catalog: dict, style_registry: dict) -> dict:
    gen.validate_recipe_structure(recipe)
    gen.resolve_style_definition(str(recipe["base"]["g"]), style_registry)
    gen.encode_ti(recipe, catalog, bytearray(12))

    positions = {item["id"]: int(item["mask"]) for item in catalog["positions"]}
    roles = {item["id"]: item for item in catalog["roles"]}
    eligibility = catalog.get("role_eligibility", {})
    checked = []
    phase_role_items = {0: [], 1: []}
    seen_positions = {0: set(), 1: set()}
    configured_pi_phases = 0
    configured_pi_items = 0
    serialized_override_bits = 0
    selected_fixed_on_options = 0

    for slot, spec in enumerate(recipe["p"]):
        for phase, phase_key in ((0, "in"), (1, "out")):
            item = spec[phase_key]
            pos_name = str(item["pos"])
            pos_id = gen.native_position_id(pos_name, phase)
            if pos_id not in positions:
                raise ValueError(f"slot {slot} {phase_key}: unknown native position {pos_name!r}")
            if pos_id in seen_positions[phase]:
                raise ValueError(f"slot {slot} {phase_key}: duplicate native position {pos_name!r}")
            seen_positions[phase].add(pos_id)

            role_id = gen.role_id_from_display(str(item["role"]), phase, set(roles))
            role = roles[role_id]
            if int(role["phase"]) != phase:
                raise ValueError(f"slot {slot} {phase_key}: role phase mismatch: {role_id}")
            if role_id not in eligibility.get(pos_id, [[], []])[phase]:
                raise ValueError(f"slot {slot} {phase_key}: incompatible position/role {pos_name}/{role_id}")
            phase_role_items[phase].append({"pos": pos_name, "role": role_id})

            duty = gen.resolve_role_duty(role_id, item)
            selected_count = len(item["pi"])
            pi_mask, fixed_on_count = gen.encode_pi_details(item["pi"], catalog, phase, pos_id, role_id, duty)
            override_bits = pi_mask.bit_count()
            if fixed_on_count + override_bits != selected_count:
                raise ValueError(f"slot {slot} {phase_key}: PI selection summary does not reconcile")

            configured_pi_phases += int(selected_count > 0)
            configured_pi_items += selected_count
            serialized_override_bits += override_bits
            selected_fixed_on_options += fixed_on_count
            checked.append({
                "slot": slot,
                "phase": phase_key,
                "position": pos_name,
                "role": role_id,
                "configured_pi_count": selected_count,
                "serialized_override_bit_count": override_bits,
                "selected_fixed_on_count": fixed_on_count,
            })

    formation_checks = [
        validate_formation_role_compatibility(phase_role_items[phase], phase)
        for phase in (0, 1)
    ]

    return {
        "status": "preflight_passed",
        "catalog_schema_version": catalog.get("schema_version"),
        "catalog_source_bundle_sha256": catalog.get("source_bundle_sha256"),
        "checked_phases": len(checked),
        "configured_pi_phases": configured_pi_phases,
        "configured_pi_items": configured_pi_items,
        "serialized_pi_override_bits": serialized_override_bits,
        "selected_fixed_on_options": selected_fixed_on_options,
        "empty_pi_phases_allowed": True,
        "formation_role_checks": formation_checks,
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
