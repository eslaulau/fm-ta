#!/usr/bin/env python3
"""Idempotently rebuild the R5.1 machine manifest and pin current source hashes."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
AUDIT = PROJECT_DIR / "R5.1_DESIGN_AND_AUDIT.md"
RECIPE = PROJECT_DIR / "R5.1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_single_line(source: str, label: str, value: str) -> str:
    pattern = rf"(?m)^{re.escape(label)}：.*$"
    updated, count = re.subn(pattern, f"{label}：{value}", source)
    if count != 1:
        raise ValueError(f"Expected exactly one audit hash line for {label}; found {count}")
    return updated


def main() -> None:
    audit_text = AUDIT.read_text(encoding="utf-8")
    recipe = json.loads(RECIPE.read_text(encoding="utf-8"))

    manifest = {
        "schema_version": 1,
        "selected_configurations": [],
        "retired_configurations": [],
    }
    for slot in recipe.get("p", []):
        for phase, key in (("IP", "in"), ("OOP", "out")):
            item = slot[key]
            pos = item["pos"]
            role = item["role"]
            duty = item["duty"]
            rationale = (
                f"{phase}/{pos} 本轮全新组合，无本队D5槽位级准入证据；"
                "仅作为可证伪的新假设。"
            )
            manifest["selected_configurations"].append({
                "phase": phase,
                "pos": pos,
                "role": role,
                "duty": duty,
                "pi": item["pi"],
                "decision": "新增待验证",
                "evidence_grade": "U",
                "rationale": rationale,
                "hypothesis": (
                    f"{phase}/{pos} {role} {duty} 的行为将与相邻槽位形成新的阶段分工；"
                    "当前仅为假设。"
                ),
                "d5_metric": "完整38场报告中该槽位可归因的职责过程指标；同时全队xG和PPG。",
                "failure_condition": (
                    "无法归因或职责过程无改善则不准入；"
                    "全队xG<100或积分<109则整套战术D5失败。"
                ),
            })

    if len(manifest["selected_configurations"]) != 22:
        raise ValueError(
            f"R5.1 recipe must contain 22 phase configurations; "
            f"found {len(manifest['selected_configurations'])}"
        )

    start_marker = "MACHINE_DECISION_MANIFEST_JSON_START"
    end_marker = "MACHINE_DECISION_MANIFEST_JSON_END"
    start = audit_text.find(start_marker)
    end = audit_text.find(end_marker)
    if start < 0 or end < start:
        raise ValueError("Audit is missing its machine decision manifest markers.")
    body_start = start + len(start_marker)
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2)
    audit_text = (
        audit_text[:body_start]
        + "\n"
        + manifest_text
        + "\n"
        + audit_text[end:]
    )

    hash_inputs = {
        "本轮配方 SHA-256": RECIPE,
        "项目规则 SHA-256": PROJECT_DIR / "PROJECT_RULES.md",
        "决策总账 SHA-256": PROJECT_DIR / "TACTIC_INSTRUCTION_DECISION_LEDGER.md",
        "PPG 策略 SHA-256": PROJECT_DIR / "PPG_TARGET_POLICY.json",
        "位置绩效标准 SHA-256": PROJECT_DIR / "POSITION_PERFORMANCE_ELIMINATION_STANDARD.md",
    }
    for label, path in hash_inputs.items():
        audit_text = replace_single_line(audit_text, label, sha256(path))

    AUDIT.write_text(audit_text, encoding="utf-8")
    print("R5.1 audit repinned; manifest entries:", len(manifest["selected_configurations"]))
    for label, path in hash_inputs.items():
        print(f"{label} {sha256(path)}")


if __name__ == "__main__":
    main()
