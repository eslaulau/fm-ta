#!/usr/bin/env python3
"""Project-owned build entrypoint: project gate first, FM-TA generic tools second."""
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


def run(command: list[str]) -> None:
    print("+", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build one EngineDividend tactic only after its project-specific PPG gate passes."
    )
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    def root_path(path: Path) -> Path:
        return path.resolve() if path.is_absolute() else (ROOT / path).resolve()

    recipe = root_path(args.recipe)
    audit = root_path(args.audit)
    output = root_path(args.output)
    report = root_path(args.report)

    if output.exists() or report.exists():
        raise FileExistsError("Refusing to overwrite an existing FMF or report.")

    # Project policy gate is mandatory and fail-closed.
    run([sys.executable, str(VALIDATOR), "--recipe", str(recipe), "--audit", str(audit)])

    # Only after project approval, call the unchanged generic FM-TA preflight and generator.
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
    print("D3 build files generated. Game import and season performance remain unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
