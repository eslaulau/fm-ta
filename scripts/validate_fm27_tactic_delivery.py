#!/usr/bin/env python3
"""Validate FM27 tactic recipe structure before catalog-backed native preflight."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

GEN_DIR = Path(__file__).resolve().parents[1] / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


def validate_deliverable_recipe(recipe: dict) -> dict:
    """Check 11-slot / 22-phase structure; an empty PI list is valid."""
    gen.validate_recipe_structure(recipe)
    counts = [
        len(spec[phase_key]["pi"])
        for spec in recipe["p"]
        for phase_key in ("in", "out")
    ]
    return {
        "status": "recipe_structure_passed",
        "phase_count": len(counts),
        "configured_pi_phases": sum(1 for count in counts if count > 0),
        "configured_pi_items": sum(counts),
        "empty_pi_phases_allowed": True,
        "pi_counts": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe", type=Path, nargs="?")
    args = parser.parse_args()
    inline_json = os.environ.get("RECIPE_JSON", "").strip()
    if inline_json and args.recipe:
        raise ValueError("Provide RECIPE_JSON or recipe path, not both")
    if inline_json:
        recipe = json.loads(inline_json)
        if not isinstance(recipe, dict):
            raise ValueError("RECIPE_JSON root value must be a JSON object")
        input_format = "python_dict"
        recipe_label = os.environ.get("RECIPE_LABEL", "<inline-json>")
    elif args.recipe:
        recipe, input_format = gen.load_recipe_input(args.recipe)
        recipe_label = str(args.recipe)
    else:
        raise ValueError("Provide RECIPE_JSON or a recipe path")
    report = validate_deliverable_recipe(recipe)
    report["recipe_input_format"] = input_format
    report["recipe"] = recipe_label
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(f"Recipe structure validation failed: {type(exc).__name__}: {exc}") from exc
