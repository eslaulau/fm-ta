#!/usr/bin/env python3
"""Fail-closed project gate; historical tactic parents are allowed within the fixed scope."""
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
FIXED_CONSTRAINTS = PROJECT_DIR / "TACTIC_FIXED_CONSTRAINTS.md"
DECISIONS = ("继承保留", "替换淘汰", "新增待验证", "证据不足")
IP_BACK_FOUR = ("DL", "DCL", "DCR", "DR")
V05_BASELINE_SHA256 = "e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257"
DUTIES = {"D", "S", "A"}

# Hard-coded mirrors of the user-approved rule. Policy-file edits alone cannot
# widen these constraints; the policy and canonical Markdown must match them.
IP_FORMATION_POSITIONS = {
    "4-2-3-1": ["GK", "DR", "DCR", "DCL", "DL", "MCR", "MCL", "AMR", "AML", "AMC", "ST"],
    "4-3-3": ["GK", "DR", "DCR", "DCL", "DL", "MCR", "MCL", "AMR", "AML", "MC", "ST"],
    "4-1-2-3": ["GK", "DR", "DCR", "DCL", "DL", "DMC", "MCL", "AMR", "AML", "MCR", "ST"],
}
V05_OOP_POSITIONS_BY_SLOT = ["GK", "DR", "DCR", "DCL", "DL", "DMR", "DML", "MR", "ML", "MC", "AMC"]
V05_MENTALITY_NATIVE_VALUE = 4
V05_NATIVE_CARRIER_NAME = "FM27 Native Parent Snapshot (V0.5)"
V05_OOP_METADATA_LABEL = "V0.5 locked OOP map"
REQUIRED_RECIPE_ROOT_KEYS = {"v", "name", "ment", "base", "ti", "p"}
REQUIRED_BASE_KEYS = {"g", "ip", "oop"}
REQUIRED_SLOT_KEYS = {"in", "out"}
REQUIRED_PHASE_ITEM_KEYS = {"pos", "role", "duty", "pi"}
FIXED_TEAM_INSTRUCTIONS = {
    "PASSING_DIRECTNESS": "MORE_DIRECT",
    "TEMPO": "MUCH_HIGHER",
    "ATTACKING_WIDTH": "MUCH_NARROWER",
    "PASS_RECEPTION": "PASS_INTO_SPACE",
    "BUILD_UP_STRATEGY": "BYPASS_PRESS",
    "GOAL_KICKS": "SHORT",
    "GK_DISTRIBUTION_(SPEED)": "DEFAULT",
    "GOALKEEPER_DISTRIBUTION": "CENTRE_BACKS",
    "LINE_OF_ENGAGEMENT": "HIGH_PRESS",
    "DEFENSIVE_LINE": "MUCH_LOWER",
    "DEFENSIVE_TRANSITION": "REGROUP",
    "TACKLING": "GET_STUCK_IN",
    "PRESSING_TRAP": "DEFAULT",
    "SHORT_GOALKEEPER_DISTRIBUTION": "YES",
    "CROSS_ENGAGEMENT": "INVITE_CROSSES",
}
REQUIRED_TEAM_INSTRUCTION_KEYS = (
    "PASSING_DIRECTNESS", "TEMPO", "ATTACKING_WIDTH", "ATTACKING_TRANSITION",
    "CREATIVE_FREEDOM", "TIME_WASTING", "PLAY_FOR_SET_PIECES", "BUILD_UP_STRATEGY",
    "GOAL_KICKS", "GOALKEEPER_DISTRIBUTION", "GK_DISTRIBUTION_(SPEED)", "PROGRESS_THROUGH",
    "PASS_RECEPTION", "SUPPORTING_RUNS", "SUPPORTING_RUNS_SECONDARY",
    "GOALKEEPER_ATTACKING_SET_PIECES", "PATIENCE", "DRIBBLING", "SHOTS_FROM_DISTANCE",
    "CROSSING_STYLE", "LINE_OF_ENGAGEMENT", "DEFENSIVE_LINE", "DEFENSIVE_LINE_BEHAVIOR",
    "TRIGGER_PRESS", "DEFENSIVE_TRANSITION", "TACKLING", "PRESSING_TRAP",
    "SHORT_GOALKEEPER_DISTRIBUTION", "CROSS_ENGAGEMENT",
)
ADJUSTABLE_NON_BOX_TEAM_INSTRUCTION_KEYS = (
    "ATTACKING_TRANSITION", "CREATIVE_FREEDOM", "TIME_WASTING", "PLAY_FOR_SET_PIECES",
    "PROGRESS_THROUGH", "SUPPORTING_RUNS", "SUPPORTING_RUNS_SECONDARY",
    "GOALKEEPER_ATTACKING_SET_PIECES", "PATIENCE", "DRIBBLING", "SHOTS_FROM_DISTANCE",
    "CROSSING_STYLE", "DEFENSIVE_LINE_BEHAVIOR", "TRIGGER_PRESS",
)
ALLOWED_MODIFICATIONS = [
    "ip_formation_choice_within_allowed_set",
    "player_roles_and_duties_in_IP_and_OOP",
    "player_personal_instructions_in_IP_and_OOP",
    "team_instructions_not_in_the_red_box",
]


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


def validate_decision_manifest(recipe: dict, audit: str, policy: dict) -> list[str]:
    """Require an exact, evidence-classified decision for every IP/OOP recipe slot."""
    errors = []
    start = audit.find("MACHINE_DECISION_MANIFEST_JSON_START")
    end = audit.find("MACHINE_DECISION_MANIFEST_JSON_END")
    if start < 0 or end < start:
        return ["Missing machine decision manifest; prose-only decisions cannot authorize a build."]
    raw_manifest = audit[start + len("MACHINE_DECISION_MANIFEST_JSON_START"):end].strip()
    try:
        manifest = json.loads(raw_manifest)
    except json.JSONDecodeError as exc:
        return [f"Machine decision manifest is invalid JSON: {exc}"]
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return ["Machine decision manifest must be an object with schema_version=1."]
    slots = recipe.get("p")
    if not isinstance(slots, list) or len(slots) != 11:
        return ["Cannot verify manifest unless recipe has exactly 11 slots."]
    actual = []
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        for phase, key in (("IP", "in"), ("OOP", "out")):
            item = slot.get(key)
            if isinstance(item, dict):
                pi = item.get("pi", [])
                actual.append((phase, item.get("pos"), item.get("role"), item.get("duty"),
                               tuple(sorted(tuple(x) for x in pi if isinstance(x, list) and len(x) == 2))))
    selected = manifest.get("selected_configurations")
    if not isinstance(selected, list) or len(selected) != 22:
        return errors + ["Machine decision manifest must contain exactly 22 selected_configurations."]
    declared = []
    by_slot = {}
    for index, item in enumerate(selected, 1):
        if not isinstance(item, dict) or item.get("phase") not in ("IP", "OOP"):
            errors.append(f"Manifest entry {index} must identify IP or OOP.")
            continue
        pi = item.get("pi", [])
        config = (item["phase"], item.get("pos"), item.get("role"), item.get("duty"),
                  tuple(sorted(tuple(x) for x in pi if isinstance(x, list) and len(x) == 2)))
        declared.append(config)
        if config in by_slot:
            errors.append(f"Duplicate manifest entry: {config[0]}/{config[1]}/{config[2]}.")
        by_slot[config] = item
        decision = item.get("decision")
        if decision not in DECISIONS:
            errors.append(f"{config[0]}/{config[1]} has invalid four-class decision.")
        if not isinstance(item.get("rationale"), str) or len(item.get("rationale", "").strip()) < 12:
            errors.append(f"{config[0]}/{config[1]} needs a substantive rationale.")
        if item.get("evidence_grade") not in ("A", "B", "C", "U"):
            errors.append(f"{config[0]}/{config[1]} evidence_grade must be A/B/C/U.")
        if decision == "继承保留":
            if item.get("evidence_grade") not in ("A", "B"):
                errors.append(f"{config[0]}/{config[1]} cannot be inherited without A/B admission evidence.")
            refs = item.get("evidence_refs")
            if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or len(ref.strip()) < 8 for ref in refs):
                errors.append(f"{config[0]}/{config[1]} inherited retention requires at least one concrete evidence_refs entry.")
        if decision in ("证据不足", "替换淘汰"):
            errors.append(f"{config[0]}/{config[1]} is marked {decision} but still exists in the selected recipe.")
        if decision == "新增待验证":
            for field in ("hypothesis", "d5_metric", "failure_condition"):
                if not isinstance(item.get(field), str) or len(item.get(field, "").strip()) < 12:
                    errors.append(f"{config[0]}/{config[1]} needs falsifiable {field}.")
    if sorted(actual, key=repr) != sorted(declared, key=repr):
        errors.append("Decision manifest does not exactly match all 22 recipe phase/position/role/duty/PI configurations.")
    for prior in policy.get("historical_non_admitted_configurations", []):
        for config, item in by_slot.items():
            if (config[0] == prior.get("phase") and config[1] == prior.get("position")
                    and config[2] == prior.get("role") and config[3] == prior.get("duty")
                    and item.get("decision") != "新增待验证"):
                errors.append(f"Previously unadmitted {config[0]}/{config[1]}/{config[2]} can only return as 新增待验证 with a new hypothesis.")
    retired = manifest.get("retired_configurations", [])
    if not isinstance(retired, list):
        errors.append("retired_configurations must be a list.")
        retired = []
    retired_keys = set()
    for item in retired:
        if not isinstance(item, dict) or item.get("phase") not in ("IP", "OOP"):
            errors.append("Each retired configuration needs phase, pos, role, duty and pi.")
            continue
        pi = item.get("pi", [])
        retired_keys.add((item["phase"], item.get("pos"), item.get("role"), item.get("duty"),
                          tuple(sorted(tuple(x) for x in pi if isinstance(x, list) and len(x) == 2))))
    for config in actual:
        if config in retired_keys:
            errors.append(f"Recipe reintroduces retired configuration {config[0]}/{config[1]}/{config[2]}.")
    return errors


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
    for required in (POLICY, PERFORMANCE_STANDARD, RULES, LEDGER, FIXED_CONSTRAINTS, parent_fmf):
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
    unexpected_root_keys = sorted(set(recipe) - REQUIRED_RECIPE_ROOT_KEYS)
    missing_root_keys = sorted(REQUIRED_RECIPE_ROOT_KEYS - set(recipe))
    if unexpected_root_keys or missing_root_keys:
        errors.append(
            f"Recipe root may contain only {sorted(REQUIRED_RECIPE_ROOT_KEYS)}; "
            f"unexpected={unexpected_root_keys}, missing={missing_root_keys}."
        )

    rules = RULES.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    fixed_constraints_text = FIXED_CONSTRAINTS.read_text(encoding="utf-8")
    audit = audit_path.read_text(encoding="utf-8")
    performance_standard = PERFORMANCE_STANDARD.read_text(encoding="utf-8")

    version = one_line_value(audit, "版本")
    if version in policy.get("blocked_versions", []):
        errors.append(f"Version {version} is explicitly blocked/invalidated by project policy; historical D3 success cannot restore candidate status.")


    if "D0强制门禁" not in performance_standard or "低效配置清除规则" not in performance_standard:
        errors.append("Position performance standard is incomplete or missing its mandatory elimination gate.")
    performance_section = re.search(
        r"(?ms)^##\s*位置绩效高强度审查与低效淘汰\s*\n(.*?)(?=^##\s|\Z)",
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

    hard_constraints = policy.get("hard_constraints", {})
    if hard_constraints.get("allowed_ip_formations") != list(IP_FORMATION_POSITIONS):
        errors.append("Policy allowed_ip_formations conflicts with the three user-approved formations.")
    if hard_constraints.get("ip_position_map_by_formation") != IP_FORMATION_POSITIONS:
        errors.append("Policy IP position maps do not match the approved 4-2-3-1 / 4-3-3 / 4-1-2-3 layouts.")
    if hard_constraints.get("oop_position_map_by_slot") != V05_OOP_POSITIONS_BY_SLOT:
        errors.append("Policy OOP position map must remain locked to the V0.5 11-slot mapping.")
    if hard_constraints.get("fixed_mentality_native_value") != V05_MENTALITY_NATIVE_VALUE:
        errors.append("Policy mentality must remain at V0.5 native value 4.")
    if hard_constraints.get("fixed_team_instruction_values") != FIXED_TEAM_INSTRUCTIONS:
        errors.append("Policy red-box team instruction values differ from the canonical fixed values.")
    if set(hard_constraints.get("required_explicit_team_instruction_keys", [])) != set(REQUIRED_TEAM_INSTRUCTION_KEYS):
        errors.append("Policy must require explicit coverage of all 29 native team-instruction groups.")
    if set(ADJUSTABLE_NON_BOX_TEAM_INSTRUCTION_KEYS) & set(FIXED_TEAM_INSTRUCTIONS):
        errors.append("Internal TI policy error: fixed and adjustable TI groups overlap.")
    if set(ADJUSTABLE_NON_BOX_TEAM_INSTRUCTION_KEYS) | set(FIXED_TEAM_INSTRUCTIONS) != set(REQUIRED_TEAM_INSTRUCTION_KEYS):
        errors.append("Internal TI policy error: fixed and adjustable TI groups must partition all 29 groups.")
    if hard_constraints.get("adjustable_non_box_team_instruction_keys") != list(ADJUSTABLE_NON_BOX_TEAM_INSTRUCTION_KEYS):
        errors.append("Policy adjustable_non_box_team_instruction_keys conflicts with canonical 14-group list.")
    if hard_constraints.get("allowed_modifications") != ALLOWED_MODIFICATIONS:
        errors.append("Policy allowed_modifications conflicts with the user-authorized scope.")
    if "只允许以下三种阵型" not in fixed_constraints_text or "红框团队指令：固定，不得修改" not in fixed_constraints_text:
        errors.append("TACTIC_FIXED_CONSTRAINTS.md is missing the current fixed-scope contract.")
    if "IP阵型只允许三种" not in rules or "红框" not in rules:
        errors.append("PROJECT_RULES.md does not incorporate the fixed formation and red-box instruction policy.")

    if policy.get("target_ppg") != 2.85 or policy.get("primary_objective") != "PPG >= 2.85":
        errors.append("Project policy must define PPG >= 2.85 as the primary objective.")
    if "PPG ≥ 2.85" not in rules:
        errors.append("PROJECT_RULES.md does not state the PPG 2.85 objective.")
    if "PPG" not in ledger or "2.85" not in ledger:
        errors.append("Authoritative decision ledger has not recorded the PPG 2.85 objective.")

    attack_gate = policy.get("minimum_attack_process_gate", {})
    if attack_gate.get("metric") != "team_xG" or attack_gate.get("minimum_38_match_total") != 100:
        errors.append("Project policy must enforce the 38-match team xG >= 100 minimum process gate.")
    if "xG≥100" not in rules and "xG >= 100" not in rules:
        errors.append("PROJECT_RULES.md does not state the 100 xG minimum process gate.")
    if "xG≥100" not in ledger and "xG >= 100" not in ledger:
        errors.append("Authoritative decision ledger has not recorded the 100 xG minimum process gate.")
    if not any("xG" in line and "100" in line for line in audit.splitlines()):
        errors.append("Design audit must explicitly state the 38-match xG >= 100 minimum gate.")

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
    if not parent_version or parent_version in {"无", "未知", "None"}:
        errors.append("Design audit must identify the actual historical tactic parent version.")
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
        ("固定战术边界 SHA-256", FIXED_CONSTRAINTS, "TACTIC_FIXED_CONSTRAINTS.md"),
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
    else:
        base_keys = set(recipe["base"])
        if base_keys != REQUIRED_BASE_KEYS:
            errors.append(
                f"Recipe base may contain only {sorted(REQUIRED_BASE_KEYS)}; got {sorted(base_keys)}."
            )
        if recipe["base"].get("g") != V05_NATIVE_CARRIER_NAME:
            errors.append("Recipe native carrier is locked to FM27 Native Parent Snapshot (V0.5).")
        if recipe["base"].get("oop") != V05_OOP_METADATA_LABEL:
            errors.append("Recipe base.oop metadata must identify the locked V0.5 OOP position map.")
    if not isinstance(recipe.get("ti"), dict):
        errors.append("Recipe must include a team-instructions object 'ti'.")
    else:
        ti = recipe["ti"]
        missing_ti = sorted(set(REQUIRED_TEAM_INSTRUCTION_KEYS) - set(ti))
        extra_ti = sorted(set(ti) - set(REQUIRED_TEAM_INSTRUCTION_KEYS))
        if missing_ti:
            errors.append(f"Recipe must explicitly configure all 29 native TI groups; missing: {missing_ti}.")
        if extra_ti:
            errors.append(f"Recipe contains unrecognized TI keys: {extra_ti}.")
        for key, expected in FIXED_TEAM_INSTRUCTIONS.items():
            if ti.get(key) != expected:
                errors.append(f"Red-box TI is locked: {key} must be {expected}, found {ti.get(key)!r}.")

    if recipe.get("ment") != V05_MENTALITY_NATIVE_VALUE:
        errors.append("Team mentality is locked to V0.5 native value 4; mentality changes are not authorized.")

    formation = (recipe.get("base") or {}).get("ip") if isinstance(recipe.get("base"), dict) else None
    if formation not in IP_FORMATION_POSITIONS:
        errors.append(f"IP formation must be exactly one of: {', '.join(IP_FORMATION_POSITIONS)}; found {formation!r}.")

    slots = recipe.get("p")
    if not isinstance(slots, list) or len(slots) != 11:
        errors.append("Recipe must contain exactly 11 paired player slots.")
        return errors

    phase_positions: dict[str, list[str]] = {"in": [], "out": []}
    for index, slot in enumerate(slots, start=1):
        if not isinstance(slot, dict):
            errors.append(f"Recipe slot {index} must be an object.")
            continue
        if set(slot) != REQUIRED_SLOT_KEYS:
            errors.append(
                f"Recipe slot {index} may contain only IP/OOP phase objects; got {sorted(slot)}."
            )
        for phase in ("in", "out"):
            item = slot.get(phase)
            if not isinstance(item, dict):
                errors.append(f"Recipe slot {index} is missing its '{phase}' phase object.")
                continue
            if set(item) != REQUIRED_PHASE_ITEM_KEYS:
                errors.append(
                    f"Recipe slot {index} {phase}: only position, role, duty and PI are authorized fields; "
                    f"got {sorted(item)}."
                )
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
    oop_positions = phase_positions["out"]
    if formation in IP_FORMATION_POSITIONS and len(ip_positions) == 11:
        expected_ip = IP_FORMATION_POSITIONS[formation]
        if set(ip_positions) != set(expected_ip):
            errors.append(
                f"IP positions do not match declared {formation}: expected={expected_ip}, actual={ip_positions}."
            )
    if len(oop_positions) == 11 and oop_positions != V05_OOP_POSITIONS_BY_SLOT:
        errors.append(
            f"OOP position map is locked to V0.5 by slot: expected={V05_OOP_POSITIONS_BY_SLOT}, actual={oop_positions}."
        )
    for position in IP_BACK_FOUR:
        count = ip_positions.count(position)
        if count != 1:
            errors.append(f"IP hard constraint failed: {position} must appear exactly once; found {count}.")
    if len(ip_positions) == 11 and sum(ip_positions.count(p) for p in IP_BACK_FOUR) != 4:
        errors.append(f"IP must contain exactly four back-four slots {IP_BACK_FOUR}; got {ip_positions}.")

    errors.extend(validate_decision_manifest(recipe, audit, policy))
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
