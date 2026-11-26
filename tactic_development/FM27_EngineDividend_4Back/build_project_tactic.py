#!/usr/bin/env python3
"""The only supported build entrypoint for FM27 EngineDividend 4Back iterations."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
ROOT = PROJECT_DIR.parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
VALIDATOR = PROJECT_DIR / "validate_project_iteration.py"
PREFLIGHT = ROOT / "scripts" / "preflight_fm27_tactic.py"
GENERATOR = ROOT / "scripts" / "build_fm27_tactic.py"
BUILD_DIR = PROJECT_DIR / "builds"


def project_path(path: Path, label: str) -> Path:
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(PROJECT_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must be inside {PROJECT_DIR}: {resolved}") from exc
    return resolved


def run(command: list[str]) -> None:
    print("+", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mandatory project gate -> unchanged FM-TA preflight -> unchanged FM-TA generator."
    )
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--parent-fmf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    recipe = project_path(args.recipe, "Recipe")
    audit = project_path(args.audit, "Design audit")
    parent_fmf = args.parent_fmf.resolve()
    output = project_path(args.output, "FMF output")
    report = project_path(args.report, "Build report")

    if output == report or output.exists() or report.exists():
        raise FileExistsError("Refusing to overwrite an existing FMF/report or use the same path.")
    if not parent_fmf.is_file():
        raise FileNotFoundError(f"Parent FMF not found: {parent_fmf}")
    if not recipe.is_file() or not audit.is_file():
        raise FileNotFoundError("Recipe or design audit is missing.")

    # Fail closed: if this exits non-zero, neither generic tool is called.
    run([
        sys.executable, str(VALIDATOR),
        "--recipe", str(recipe),
        "--audit", str(audit),
        "--parent-fmf", str(parent_fmf),
    ])

    # Generic FM-TA tools remain unchanged and are invoked only after project approval.
    run([
        sys.executable, str(PREFLIGHT),
        "--recipe", str(recipe),
        "--catalog", str(GEN_DIR / "catalog.json"),
        "--style-registry", str(GEN_DIR / "style_template_registry.json"),
    ])
    run([
        sys.executable, str(GENERATOR),
        "--recipe-path", str(recipe),
        "--catalog", str(GEN_DIR / "catalog.json"),
        "--style-registry", str(GEN_DIR / "style_template_registry.json"),
        "--output", str(output),
        "--report", str(report),
    ])
    print("D3 offline build complete. In-game import (D4) and season performance (D5) remain unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
