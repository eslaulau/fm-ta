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
PERFORMANCE_STANDARD = PROJECT_DIR / "POSITION_PERFORMANCE_ELIMINATION_STANDARD.md"
RULES = PROJECT_DIR / "PROJECT_RULES.md"
LEDGER = PROJECT_DIR / "TACTIC_INSTRUCTION_DECISION_LEDGER.md"
DECISIONS = ("继承保留", "替换淘汰", "新增待验证", "证据不足")
IP_BACK_FOUR = ("DL", "DCL", "DCR", "DR")
V05_BASELINE_SHA256 = "e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257"
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
    for required in (POLICY, PERFORMANCE_STANDARD, RULES, LEDGER, parent_fmf):
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
    performance_standard = PERFORMANCE_STANDARD.read_text(encoding="utf-8")

    if "D0强制门禁" not in performance_standard or "低效配置清除规则" not in performance_standard:
        errors.append("Position performance standard is incomplete or missing its mandatory elimination gate.")
    performance_section = re.search(
        r"(?ms)^##\\s*位置绩效高强度审查与低效淘汰\\s*\\n(.*?)(?=^##\\s|\\Z)",
        audit,
    )
    if not performance_section:
        errors.append("Design audit must include a dedicated 位置绩效高强度审查与低效淘汰 section.")
    else:
        section_text = performance_section.group(1)
        for slot_id in [*(f"IP-{i:02d}" for i in range(1, 12)), *(f"OOP-{i:02d}" for i in range(1, 12))]:
            row = next((line for line in section_text.splitlines() if slot_id in line and line.lstrip().startswith("|")), None)
            if row is None or row.count("|") < 10:
                errors.append(f"Position audit must contain a populated table row for {slot_id}.")
            elif sum(bool(cell.strip()) for cell in row.strip().strip("|").split("|")) < 8:
                errors.append(f"Position audit row {slot_id} is incomplete; mark unavailable fields explicitly.")
        for required_term in ("低效淘汰清单", "证据等级", "准入保留", "条件保留", "替换淘汰", "D5"):
            if required_term not in section_text:
                errors.append(f"Position audit section must explicitly include: {required_term}.")

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
    if parent_version != "V0.5":
        errors.append("重生模式强制要求父版本：V0.5；不得继承最近版本或任何 V1.x 版本。")
    baseline_version = one_line_value(audit, "重生基准")
    if baseline_version != "V0.5":
        errors.append("Design audit must explicitly state 重生基准：V0.5.")
    baseline_sha = one_line_value(audit, "重生基准 FMF SHA-256")
    if baseline_sha != V05_BASELINE_SHA256:
        errors.append("Design audit must pin the exact V0.5 baseline FMF SHA-256.")
    declared_parent_sha = one_line_value(audit, "父 FMF SHA-256")
    actual_parent_sha = sha256_file(parent_fmf)
    if not declared_parent_sha or not re.fullmatch(r"[0-9a-fA-F]{64}", declared_parent_sha):
        errors.append("Design audit must include a 64-character 父 FMF SHA-256.")
    elif declared_parent_sha.lower() != actual_parent_sha:
        errors.append(
            f"Parent FMF SHA-256 mismatch: audit={declared_parent_sha.lower()}, file={actual_parent_sha}."
        )
    if actual_parent_sha != V05_BASELINE_SHA256:
        errors.append(
            f"重生模式拒绝非 V0.5 父文件：expected={V05_BASELINE_SHA256}, actual={actual_parent_sha}."
        )
    if declared_parent_sha and declared_parent_sha.lower() != V05_BASELINE_SHA256:
        errors.append("父 FMF SHA-256 必须固定为 V0.5 原始基准 SHA-256。")

    for audit_label, source_path, description in (
        ("项目规则 SHA-256", RULES, "PROJECT_RULES.md"),
        ("决策总账 SHA-256", LEDGER, "TACTIC_INSTRUCTION_DECISION_LEDGER.md"),
        ("PPG 策略 SHA-256", POLICY, "PPG_TARGET_POLICY.json"),
        ("位置绩效标准 SHA-256", PERFORMANCE_STANDARD, "POSITION_PERFORMANCE_ELIMINATION_STANDARD.md"),
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

    # The project must deliberately explore non-traditional engine behaviour.
    # A template heading alone is insufficient: require populated mismatch fields.
    if "现实足球理论不是战术筛选/否决标准" not in audit:
        errors.append("Design audit must explicitly state that real-football theory is not a veto criterion.")
    mismatch_heading = re.search(
        r"(?ms)^##\s*7\.\s*强制审计：引擎行为错位设计.*?\n(.*?)(?=^##\s|\Z)",
        audit,
    )
    if not mismatch_heading:
        errors.append("Design audit must include section 7: 强制审计：引擎行为错位设计.")
    else:
        mismatch_text = mismatch_heading.group(1)
        mismatch_fields = (
            "错位类型", "错位配置", "角色/指令默认行为",
            "FM27引擎预期执行行为", "对手AI可能",
            "预期创造的空间", "对PPG", "可能副作用", "D5量化验证指标",
        )
        for field in mismatch_fields:
            line = next(
                (row for row in mismatch_text.splitlines()
                 if row.strip().startswith("- ") and field in row),
                None,
            )
            if line is None or not re.search(r"：\s*[^：\s].*", line):
                errors.append(f"Engine-mismatch audit field must be completed: {field}.")
    if "不以现实足球" not in rules or "引擎行为错位" not in rules:
        errors.append("PROJECT_RULES.md must retain the mandatory engine-mismatch design rule.")
    if "每轮从 V0.5 重生" not in rules or "最高优先级" not in rules:
        errors.append("PROJECT_RULES.md must enforce V0.5 reset-based iteration as the highest-priority rule.")

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
    print("PASS: V0.5 reset baseline, exact V0.5 parent FMF SHA, project rules, recipe hash, 11/22 slots, IP back-four and D5 audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
