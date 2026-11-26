#!/usr/bin/env python3
"""Fail-closed, project-local pre-generation gate for FM27 EngineDividend 4Back."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
ROOT = PROJECT_DIR.parents[1]
POLICY = PROJECT_DIR / "PPG_TARGET_POLICY.json"
RULES = PROJECT_DIR / "PROJECT_RULES.md"
LEDGER = PROJECT_DIR / "TACTIC_INSTRUCTION_DECISION_LEDGER.md"
DECISIONS = ("继承保留", "替换淘汰", "新增待验证", "证据不足")
IP_BACK_FOUR = ("DL", "DCL", "DCR", "DR")
DUTIES = {"D", "S", "A"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inside_project(path: Path) -> bool:
    try:
        path.resolve().relative_to(PROJECT_DIR.resolve())
        return True
    except ValueError:
        return False


def one_line_value(text: str, label: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(label)}\s*：\s*(.*?)\s*$", text)
    return match.group(1).strip() if match else None


def validate(recipe_path: Path, audit_path: Path, parent_fmf: Path) -> list[str]:
    errors: list[str] = []
    for label, path in (
        ("recipe", recipe_path),
        ("design audit", audit_path),
    ):
        if not inside_project(path):
            errors.append(f"{label} must be inside the project directory: {path}")
        if not path.is_file():
            errors.append(f"{label} file is missing: {path}")
    for required in (POLICY, RULES, LEDGER, parent_fmf):
        if not required.is_file():
            errors.append(f"Required project/parent file is missing: {required}")
    if errors:
        return errors

    try:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        recipe_bytes = recipe_path.read_bytes()
        recipe = json.loads(recipe_bytes.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"Unable to read project policy or recipe: {exc}"]

    if not isinstance(recipe, dict):
        return ["Recipe root must be a JSON object."]

    rules = RULES.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = audit_path.read_text(encoding="utf-8")

    if policy.get("target_ppg") != 2.85 or policy.get("primary_objective") != "PPG >= 2.85":
        errors.append("Project policy must define PPG >= 2.85 as the primary objective.")
    if "PPG ≥ 2.85" not in rules:
        errors.append("PROJECT_RULES.md does not state the PPG 2.85 objective.")
    if "PPG" not in ledger or "2.85" not in ledger:
        errors.append("Authoritative decision ledger has not recorded the PPG 2.85 objective.")

    if "PPG ≥ 2.85" not in audit and "PPG >= 2.85" not in audit:
        errors.append("Design audit must explicitly state the PPG 2.85 objective.")
    for decision in DECISIONS:
        section = re.search(
            rf"(?ms)^###\s*{re.escape(decision)}\s*$\n(.*?)(?=^###\s|^##\s|\Z)",
            audit,
        )
        if not section:
            errors.append(f"Design audit must contain a dedicated '{decision}' section.")
        else:
            payload_lines = [
                line.strip() for line in section.group(1).splitlines()
                if line.strip()
                and not line.strip().startswith("- [")
                and not (line.strip().startswith("- ") and line.strip().endswith(("：", ":")))
            ]
            if not payload_lines:
                errors.append(f"Design audit section '{decision}' is empty; add evidence-backed decisions.")

    if not any("PPG" in line and any(word in line for word in ("提高", "收益", "积分")) for line in audit.splitlines()):
        errors.append("Design audit must state an explicit PPG/points improvement path.")

    parent_version = one_line_value(audit, "父版本")
    if not parent_version or not re.fullmatch(r"V\d+(?:\.\d+)?(?:[-_A-Za-z0-9.]*)?", parent_version):
        errors.append("Design audit must identify one exact parent version, e.g. 父版本：V1.8.")

    declared_parent_sha = one_line_value(audit, "父 FMF SHA-256")
    actual_parent_sha = sha256_file(parent_fmf)
    if not declared_parent_sha or not re.fullmatch(r"[0-9a-fA-F]{64}", declared_parent_sha):
        errors.append("Design audit must include a 64-character 父 FMF SHA-256.")
    elif declared_parent_sha.lower() != actual_parent_sha:
        errors.append(
            f"Parent FMF SHA-256 mismatch: audit={declared_parent_sha.lower()}, file={actual_parent_sha}."
        )

    for audit_label, source_path, description in (
        ("项目规则 SHA-256", RULES, "PROJECT_RULES.md"),
        ("决策总账 SHA-256", LEDGER, "TACTIC_INSTRUCTION_DECISION_LEDGER.md"),
        ("PPG 策略 SHA-256", POLICY, "PPG_TARGET_POLICY.json"),
    ):
        declared = one_line_value(audit, audit_label)
        actual = sha256_file(source_path)
        if not declared or not re.fullmatch(r"[0-9a-fA-F]{64}", declared):
            errors.append(f"Design audit must include a 64-character {audit_label}.")
        elif declared.lower() != actual:
            errors.append(f"Stale design audit: {description} has changed since this audit was prepared.")

    declared_recipe_sha = one_line_value(audit, "本轮配方 SHA-256")
    actual_recipe_sha = hashlib.sha256(recipe_bytes).hexdigest()
    if not declared_recipe_sha or not re.fullmatch(r"[0-9a-fA-F]{64}", declared_recipe_sha):
        errors.append("Design audit must include a 64-character 本轮配方 SHA-256.")
    elif declared_recipe_sha.lower() != actual_recipe_sha:
        errors.append(
            f"Recipe SHA-256 mismatch: audit={declared_recipe_sha.lower()}, file={actual_recipe_sha}."
        )

    if not re.search(r"(?m)^审计结论：\s*PASS\s*$", audit):
        errors.append("Design audit must explicitly conclude '审计结论： PASS'.")
    if not any(token in audit for token in ("D5", "下一轮验证", "验证指标")):
        errors.append("Design audit must define measurable D5 validation criteria.")
    if not any(token in audit for token in ("风险", "副作用", "失败条件")):
        errors.append("Design audit must record risks, side effects or failure conditions.")

    if policy.get("hard_constraints", {}).get("ip_back_four_positions") != list(IP_BACK_FOUR):
        errors.append("Policy IP hard constraint must be exactly DL/DCL/DCR/DR.")

    if not isinstance(recipe.get("base"), dict) or not isinstance(recipe["base"].get("g"), str):
        errors.append("Recipe must identify its native base/template in base.g.")
    if not isinstance(recipe.get("ti"), dict):
        errors.append("Recipe must include a team-instructions object 'ti'.")

    slots = recipe.get("p")
    if not isinstance(slots, list) or len(slots) != 11:
        errors.append("Recipe must contain exactly 11 paired player slots.")
        return errors

    phase_positions: dict[str, list[str]] = {"in": [], "out": []}
    for index, slot in enumerate(slots, start=1):
        if not isinstance(slot, dict):
            errors.append(f"Recipe slot {index} must be an object.")
            continue
        for phase in ("in", "out"):
            item = slot.get(phase)
            if not isinstance(item, dict):
                errors.append(f"Recipe slot {index} is missing its '{phase}' phase object.")
                continue
            for key in ("pos", "role", "duty", "pi"):
                if key not in item:
                    errors.append(f"Recipe slot {index} {phase}: missing required field '{key}'.")
            position = item.get("pos")
            if not isinstance(position, str) or not position:
                errors.append(f"Recipe slot {index} {phase}: invalid position.")
            else:
                phase_positions[phase].append(position)
            if not isinstance(item.get("role"), str) or not item.get("role"):
                errors.append(f"Recipe slot {index} {phase}: invalid role.")
            if item.get("duty") not in DUTIES:
                errors.append(f"Recipe slot {index} {phase}: duty must be one of D/S/A.")
            pi = item.get("pi")
            if not isinstance(pi, list):
                errors.append(f"Recipe slot {index} {phase}: PI must be a list.")
            elif any(
                not isinstance(entry, list) or len(entry) != 2
                or not all(isinstance(value, str) for value in entry)
                for entry in pi
            ):
                errors.append(f"Recipe slot {index} {phase}: each PI must be a [key, value] string pair.")

    for phase, positions in phase_positions.items():
        if len(positions) != 11:
            errors.append(f"{phase.upper()} phase must contain 11 valid positions; found {len(positions)}.")
        if len(set(positions)) != len(positions):
            errors.append(f"{phase.upper()} phase contains duplicate positions: {positions}.")

    ip_positions = phase_positions["in"]
    for position in IP_BACK_FOUR:
        count = ip_positions.count(position)
        if count != 1:
            errors.append(f"IP hard constraint failed: {position} must appear exactly once; found {count}.")
    if len(ip_positions) == 11 and sum(ip_positions.count(p) for p in IP_BACK_FOUR) != 4:
        errors.append(f"IP must contain exactly four back-four slots {IP_BACK_FOUR}; got {ip_positions}.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed project gate before FMF generation.")
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--parent-fmf", type=Path, required=True)
    args = parser.parse_args()

    def resolve(path: Path) -> Path:
        return path.resolve() if path.is_absolute() else (ROOT / path).resolve()

    errors = validate(resolve(args.recipe), resolve(args.audit), resolve(args.parent_fmf))
    if errors:
        print("BLOCKED: FM27 EngineDividend project gate failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: project rules, exact parent FMF, recipe hash, 11/22 slots, IP back-four and D5 audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
