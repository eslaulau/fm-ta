#!/usr/bin/env python3
"""Build FM27 FMF from an in-memory JSON object or an existing recipe file."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

GEN_DIR = Path(__file__).resolve().parents[1] / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


def load_recipe_from_environment_or_path(recipe_path: str | None) -> tuple[dict, str, str]:
    inline_json = os.environ.get("RECIPE_JSON", "").strip()
    if inline_json:
        try:
            recipe = json.loads(inline_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"RECIPE_JSON is invalid JSON: {exc}") from exc
        if not isinstance(recipe, dict):
            raise ValueError("RECIPE_JSON root value must be a JSON object")
        return recipe, "python_dict", os.environ.get("RECIPE_LABEL", "<inline-json>")
    if recipe_path:
        recipe, input_format = gen.load_recipe_input(Path(recipe_path))
        return recipe, input_format, recipe_path
    raise ValueError("Provide RECIPE_JSON or a recipe path")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe-path", default=os.environ.get("RECIPE_PATH") or None)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--style-registry", type=Path, default=GEN_DIR / "style_template_registry.json")
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite existing FMF: {args.output}")
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    style_registry = json.loads(args.style_registry.read_text(encoding="utf-8"))
    recipe, input_format, recipe_source = load_recipe_from_environment_or_path(args.recipe_path)
    fmf_bytes, report = gen.build_fmf_from_recipe(
        recipe,
        catalog,
        style_registry=style_registry,
        template_path=args.template,
        recipe_input_format=input_format,
        recipe_source=recipe_source,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(fmf_bytes)
    report["output"] = str(args.output.resolve())
    report["style_registry"] = str(args.style_registry.resolve())
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(f"Native FMF build failed: {type(exc).__name__}: {exc}") from exc
