#!/usr/bin/env python3
"""Enforce project-level completeness rules for a deliverable FM27 tactic."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GEN_DIR = Path(__file__).resolve().parents[1] / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


def validate_deliverable_recipe(recipe: dict) -> dict:
    """Check the stricter 22/22 non-empty PI delivery contract."""
    gen.validate_recipe_structure(recipe)
    empty = []
    counts = []
    for slot, spec in enumerate(recipe["p"]):
        for phase_key in ("in", "out"):
            pis = spec[phase_key]["pi"]
            counts.append(len(pis))
            if not pis:
                empty.append({"slot": slot, "phase": phase_key})
    if empty:
        locations = ", ".join(f"slot {item['slot']} {item['phase']}" for item in empty)
        raise ValueError(
            f"正式战术交付要求 22/22 阶段至少包含一条有效 PI；空 PI 阶段：{locations}"
        )
    return {
        "status": "deliverable_structure_passed",
        "phase_count": len(counts),
        "non_empty_pi_phases": sum(1 for count in counts if count > 0),
        "pi_counts": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe", type=Path)
    args = parser.parse_args()
    recipe, input_format = gen.load_recipe_input(args.recipe)
    report = validate_deliverable_recipe(recipe)
    report["recipe_input_format"] = input_format
    report["recipe"] = str(args.recipe)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(f"Deliverable validation failed: {type(exc).__name__}: {exc}") from exc
