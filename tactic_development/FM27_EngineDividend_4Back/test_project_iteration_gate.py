#!/usr/bin/env python3
"""Regression tests for the project-local pre-build gate."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import validate_project_iteration as gate


class ProjectGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.old_paths = (gate.PROJECT_DIR, gate.POLICY, gate.RULES, gate.LEDGER, gate.V05_BASELINE_SHA256)
        gate.PROJECT_DIR = self.root
        gate.POLICY = self.root / "PPG_TARGET_POLICY.json"
        gate.RULES = self.root / "PROJECT_RULES.md"
        gate.LEDGER = self.root / "TACTIC_INSTRUCTION_DECISION_LEDGER.md"
        gate.POLICY.write_text(json.dumps({
            "target_ppg": 2.85,
            "primary_objective": "PPG >= 2.85",
            "hard_constraints": {"ip_back_four_positions": ["DL", "DCL", "DCR", "DR"]},
        }), encoding="utf-8")
        gate.RULES.write_text("PPG ≥ 2.85\n不以现实足球理论作为否决依据；强制引擎行为错位设计。\n每轮从 V0.5 重生；最高优先级。", encoding="utf-8")
        gate.LEDGER.write_text("PPG 2.85", encoding="utf-8")
        self.addCleanup(self.restore_gate_paths)
        self.recipe = self.root / "candidate.json"
        self.audit = self.root / "design_audit.md"
        self.parent = self.root / "parent.fmf"
        self.parent.write_bytes(b"exact parent FMF bytes")
        gate.V05_BASELINE_SHA256 = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        self.valid_recipe = {
            "v": 1,
            "name": "gate-test",
            "ment": 4,
            "base": {"g": "native-template"},
            "ti": {"TEMPO": "HIGHER"},
            "p": [],
        }
        positions = [
            ("GK", "GK"), ("DR", "DR"), ("DCR", "DCR"), ("DCL", "DCL"),
            ("DL", "DL"), ("DMC", "DMC"), ("MCR", "MCR"), ("MCL", "MCL"),
            ("AMC", "AMC"), ("AMR", "AMR"), ("STC", "STC"),
        ]
        for ip, oop in positions:
            self.valid_recipe["p"].append({
                "in": {"pos": ip, "role": "Role", "duty": "S", "pi": []},
                "out": {"pos": oop, "role": "Role", "duty": "D", "pi": []},
            })
        self.write_recipe_and_audit()

    def restore_gate_paths(self):
        gate.PROJECT_DIR, gate.POLICY, gate.RULES, gate.LEDGER, gate.V05_BASELINE_SHA256 = self.old_paths

    def write_recipe_and_audit(self):
        raw = json.dumps(self.valid_recipe, ensure_ascii=False, indent=2).encode()
        self.recipe.write_bytes(raw)
        parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        recipe_sha = hashlib.sha256(raw).hexdigest()
        rules_sha = hashlib.sha256(gate.RULES.read_bytes()).hexdigest()
        ledger_sha = hashlib.sha256(gate.LEDGER.read_bytes()).hexdigest()
        policy_sha = hashlib.sha256(gate.POLICY.read_bytes()).hexdigest()
        self.audit.write_text(
            "项目最高目标：PPG ≥ 2.85\n"
            "父版本：V0.5\n"
            "重生基准：V0.5\n"
            f"重生基准 FMF SHA-256：{gate.V05_BASELINE_SHA256}\n"
            f"父 FMF SHA-256：{parent_sha}\n"
            f"本轮配方 SHA-256：{recipe_sha}\n"
            f"项目规则 SHA-256：{rules_sha}\n"
            f"决策总账 SHA-256：{ledger_sha}\n"
            f"PPG 策略 SHA-256：{policy_sha}\n"
            "### 继承保留\n- 防线结构：保留父版本四后卫基础\n"
            "### 替换淘汰\n- 逼抢设置：调整以改善积分\n"
            "### 新增待验证\n- 新跑位：预期提高PPG收益\n"
            "### 证据不足\n- 主客场差异：样本不足暂不定论\n"
            "本轮 PPG 收益路径：改善终结机会以提高积分\n"
            "D5 验证指标：PPG、胜平负、xG、xGA\n"
            "风险：样本量不足\n"
            "现实足球理论不是战术筛选/否决标准。\n"
            "## 7. 强制审计：引擎行为错位设计\n"
            "- 错位类型：角色与PI冲突\n"
            "- 错位配置：IP DL 内收边后卫 + 拉开宽度\n"
            "- 角色/指令默认行为与显式行为：内收与拉宽冲突\n"
            "- FM27引擎预期执行行为：待验证的宽度/内收双重行为\n"
            "- 对手AI可能：可能出现盯防错配（假设）\n"
            "- 预期创造的空间：边肋空间\n"
            "- 对PPG：提升进攻出口和胜率\n"
            "- 可能副作用：转换防守暴露\n"
            "- D5量化验证指标：PPG、xGA、对手大机会\n"
            "审计结论： PASS\n",
            encoding="utf-8",
        )

    def validate(self):
        return gate.validate(self.recipe, self.audit, self.parent)

    def test_valid_project_iteration_passes(self):
        self.assertEqual(self.validate(), [])

    def test_ip_back_four_is_mandatory(self):
        self.valid_recipe["p"][4]["in"]["pos"] = "DMC"
        self.write_recipe_and_audit()
        self.assertTrue(any("IP hard constraint failed" in e for e in self.validate()))

    def test_duplicate_oop_position_is_rejected(self):
        self.valid_recipe["p"][5]["out"]["pos"] = "DCR"
        self.write_recipe_and_audit()
        self.assertTrue(any("OOP phase contains duplicate" in e for e in self.validate()))

    def test_recipe_tampering_after_audit_is_rejected(self):
        self.recipe.write_text(self.recipe.read_text(encoding="utf-8") + "\n ", encoding="utf-8")
        self.assertTrue(any("Recipe SHA-256 mismatch" in e for e in self.validate()))

    def test_wrong_parent_fmf_is_rejected(self):
        self.parent.write_bytes(b"different parent FMF")
        self.assertTrue(any("Parent FMF SHA-256 mismatch" in e for e in self.validate()))

    def test_stale_project_ledger_is_rejected(self):
        gate.LEDGER.write_text("changed ledger", encoding="utf-8")
        self.assertTrue(any("Stale design audit" in e for e in self.validate()))

    def test_missing_decision_class_is_rejected(self):
        self.audit.write_text(
            self.audit.read_text(encoding="utf-8").replace("### 证据不足\n", ""),
            encoding="utf-8",
        )
        self.assertTrue(any("证据不足" in e for e in self.validate()))


if __name__ == "__main__":
    unittest.main()
