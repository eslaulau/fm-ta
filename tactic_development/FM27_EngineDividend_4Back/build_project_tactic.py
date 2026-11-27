#!/usr/bin/env python3
"""Project-gated builder using a selected historical tactic parent and the native V0.5 serialization carrier."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
ROOT = PROJECT_DIR.parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
VALIDATOR = PROJECT_DIR / "validate_project_iteration.py"
PREFLIGHT = ROOT / "scripts" / "preflight_fm27_tactic.py"
GENERATOR = GEN_DIR / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG = GEN_DIR / "catalog.json"
STYLE_REGISTRY = GEN_DIR / "style_template_registry.json"
EXPECTED_V05_SHA = "e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257"
CARRIER_NAME = "FM27 Native Parent Snapshot (V0.5)"

def run(command: list[str]) -> None:
    print("+", " ".join(str(x) for x in command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)

def project_path(path: Path, label: str) -> Path:
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(PROJECT_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must be inside {PROJECT_DIR}: {resolved}") from exc
    return resolved

def main() -> int:
    ap = argparse.ArgumentParser(description="Historical tactic parent -> project gate -> native preflight -> FMF build/readback")
    ap.add_argument("--recipe", type=Path, required=True)
    ap.add_argument("--audit", type=Path, required=True)
    ap.add_argument("--parent-fmf", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()

    recipe_path = project_path(args.recipe, "Recipe")
    audit_path = project_path(args.audit, "Design audit")
    output_path = project_path(args.output, "FMF output")
    report_path = project_path(args.report, "Build report")
    parent_fmf = args.parent_fmf.resolve()

    if output_path == report_path or output_path.exists() or report_path.exists():
        raise FileExistsError("Refusing to overwrite an existing FMF/report.")
    if not all(p.is_file() for p in (recipe_path, audit_path, parent_fmf, CATALOG, STYLE_REGISTRY, GENERATOR)):
        raise FileNotFoundError("Recipe, audit, selected historical parent FMF, catalog, registry or generator is missing.")
    parent_sha = hashlib.sha256(parent_fmf.read_bytes()).hexdigest()

    # Fail closed before any generic preflight or generator call.
    run([sys.executable, str(VALIDATOR), "--recipe", str(recipe_path), "--audit", str(audit_path), "--parent-fmf", str(parent_fmf)])

    registry = json.loads(STYLE_REGISTRY.read_text(encoding="utf-8"))
    carriers = registry.setdefault("native_carriers", [])
    if any(x.get("name") == CARRIER_NAME for x in carriers):
        raise ValueError("V0.5 carrier overlay unexpectedly collides with an existing registry entry.")
    carriers.append({
        "name": CARRIER_NAME,
        "status": "native_snapshot_verified",
        "style_code_hex": "4c4c554e",
        "tac_style_string": "",
        "template": "../tactic_development/FM27_EngineDividend_4Back/builds/V0.5.fmf",
        "carrier_only": True,
        "evidence": {
            "repository_path": "tactic_development/FM27_EngineDividend_4Back/builds/V0.5.fmf",
            "sha256": EXPECTED_V05_SHA,
            "source_major": 27,
            "source": "Exact original V0.5 FMF bytes restored from the project's embedded native snapshot and independently SHA-256 verified.",
            "offline_fmf_roundtrip": "source identity verified; output will be independently read back",
            "game_import": "not_verified",
            "note": "This V0.5 carrier is the actual reset baseline for this project iteration, not a V0.8/V0.9 tactical parent."
        },
        "inheritance_policy": {
            "phase_configuration": "Complete recipe replacement for all 22 IP/OOP phase configurations",
            "team_instruction_vector": "V0.5 original native TI vector with explicit mapped recipe overlays",
            "opaque_bits": "V0.5 template-owned opaque bits remain preserved unless a mapped native bit is explicitly changed"
        }
    })

    with tempfile.TemporaryDirectory(prefix="fm27_v05_registry_") as temp:
        overlay_path = Path(temp) / "style_template_registry.json"
        overlay_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
        run([sys.executable, str(PREFLIGHT), "--recipe", str(recipe_path), "--catalog", str(CATALOG), "--style-registry", str(overlay_path)])

        spec = importlib.util.spec_from_file_location("fm27gen1_offline_project", GENERATOR)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load the native FMF generator module.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        output, report = module.build_fmf_from_recipe(
            recipe, catalog, registry, None,
            recipe_input_format="json",
            recipe_source=str(recipe_path),
        )

    if report.get("template_sha256") != EXPECTED_V05_SHA:
        raise ValueError(f"Generator did not use exact V0.5 carrier: {report.get('template_sha256')}")
    required = (
        "fmf_outer_roundtrip", "all_member_decrypt_and_zstd_checksums", "tac_full_parse",
        "11_ip_oop_pairs", "22_positions_roles_pi_readback_exact",
        "pi_permissions_checked_against_catalog", "team_instruction_vector_readback",
        "native_style_string_and_code_readback",
    )
    checks = report.get("checks", {})
    failed = [key for key in required if checks.get(key) is not True]
    if failed:
        raise RuntimeError(f"D3 independent readback failed: {failed}")
    if len(report.get("player_phase_map", [])) != 22 or len(report.get("readback_player_phase_map", [])) != 22:
        raise RuntimeError("D3 must contain 22 designed and 22 read-back phases.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(output)
    report["output"] = str(output_path)
    report["project_version"] = recipe.get("name", "unknown").rsplit("_", 1)[-1]
    report["project_recipe_sha256"] = hashlib.sha256(recipe_path.read_bytes()).hexdigest()
    report["project_parent_version"] = next((line.split("：", 1)[1].strip() for line in audit_path.read_text(encoding="utf-8").splitlines() if line.startswith("父版本：")), "UNSPECIFIED")
    report["project_parent_sha256"] = parent_sha
    report["project_style_registry_overlay"] = "temporary V0.5 native-format serialization carrier only; tactical configuration comes from the selected historical parent recipe and current complete recipe"
    report["sha256"] = hashlib.sha256(output).hexdigest()
    report["bytes"] = len(output)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PASS: D3 native FMF build and independent readback")
    print(f"FMF: {output_path} ({len(output)} bytes)")
    print(f"SHA256: {report['sha256']}")
    print(f"Template SHA256: {report['template_sha256']}")
    print("D4 game import and D5 season performance remain unverified.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
