#!/usr/bin/env python3
"""Project-local fail-closed gate. Does not alter or replace FM-TA tooling."""
from __future__ import annotations

import argparse
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


def validate(recipe_path: Path, audit_path: Path) -> list[str]:
    errors: list[str] = []
    for required in (POLICY, RULES, LEDGER, recipe_path, audit_path):
        if not required.is_file():
            errors.append(f"Required project file is missing: {required}")
    if errors:
        return errors

    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    rules = RULES.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = audit_path.read_text(encoding="utf-8")
    recipe = json.loads(recipe_path.read_text(encoding="utf-8"))

    if policy.get("target_ppg") != 2.85 or policy.get("primary_objective") != "PPG >= 2.85":
        errors.append("Project policy must define PPG >= 2.85 as the primary objective.")
    if "PPG ≥ 2.85" not in rules:
        errors.append("PROJECT_RULES.md does not state the PPG 2.85 objective.")
    if "PPG" not in ledger or "2.85" not in ledger:
        errors.append("Authoritative decision ledger has not recorded the PPG 2.85 objective.")

    if "PPG" not in audit or "2.85" not in audit:
        errors.append("Design audit must explicitly connect this iteration to PPG 2.85.")
    for decision in DECISIONS:
        if decision not in audit:
            errors.append(f"Design audit is missing the decision class: {decision}.")
    if not re.search(r"父版本.{0,120}(?:V\d|V0)", audit, re.S):
        errors.append("Design audit must identify the exact parent version.")
    if not re.search(r"(?i)(?:sha-?256).{0,120}[0-9a-f]{64}|[0-9a-f]{64}.{0,120}(?:sha-?256)", audit, re.S):
        errors.append("Design audit must identify the exact 64-character parent FMF SHA-256.")
    if not any(token in audit for token in ("D5", "下一轮验证", "验证指标")):
        errors.append("Design audit must define next-season/D5 validation.")
    if not any(token in audit for token in ("风险", "副作用", "失败条件")):
        errors.append("Design audit must record material risks or failure conditions.")

    if policy.get("hard_constraints", {}).get("ip_back_four_positions") != list(IP_BACK_FOUR):
        errors.append("Policy IP hard constraint must be DL/DCL/DCR/DR.")

    slots = recipe.get("p")
    if not isinstance(slots, list) or len(slots) != 11:
        errors.append("Recipe must contain exactly 11 paired player slots.")
        return errors

    ip_positions: list[str] = []
    for index, slot in enumerate(slots, start=1):
        if not isinstance(slot, dict) or not isinstance(slot.get("in"), dict) or not isinstance(slot.get("out"), dict):
            errors.append(f"Recipe slot {index} must contain both 'in' and 'out' phase objects.")
            continue
        position = slot["in"].get("pos")
        if not isinstance(position, str):
            errors.append(f"Recipe slot {index} has no valid IP position.")
        else:
            ip_positions.append(position)

    for position in IP_BACK_FOUR:
        count = ip_positions.count(position)
        if count != 1:
            errors.append(f"IP hard constraint failed: {position} must appear exactly once; found {count}.")
    if len(ip_positions) == 11 and sum(ip_positions.count(p) for p in IP_BACK_FOUR) != 4:
        errors.append(f"IP must contain exactly four back-four slots {IP_BACK_FOUR}; got {ip_positions}.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FM27 EngineDividend project rules before FMF generation.")
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    recipe = args.recipe if args.recipe.is_absolute() else (ROOT / args.recipe).resolve()
    audit = args.audit if args.audit.is_absolute() else (ROOT / args.audit).resolve()
    errors = validate(recipe, audit)
    if errors:
        print("BLOCKED: FM27 EngineDividend project gate failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: PPG 2.85 objective, four decision classes, parent identity, D5 criteria and IP back-four.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
