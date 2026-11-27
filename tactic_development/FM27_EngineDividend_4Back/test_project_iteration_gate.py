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
        self.old_paths = (gate.PROJECT_DIR, gate.POLICY, gate.RULES, gate.LEDGER, gate.PERFORMANCE_STANDARD, gate.V05_BASELINE_SHA256)
        gate.PROJECT_DIR = self.root
        gate.POLICY = self.root / "PPG_TARGET_POLICY.json"
        gate.RULES = self.root / "PROJECT_RULES.md"
        gate.LEDGER = self.root / "TACTIC_INSTRUCTION_DECISION_LEDGER.md"
        gate.PERFORMANCE_STANDARD = self.root / "POSITION_PERFORMANCE_ELIMINATION_STANDARD.md"
        gate.PERFORMANCE_STANDARD.write_text("D0强制门禁\n低效配置清除规则", encoding="utf-8")
        gate.POLICY.write_text(json.dumps({
            "target_ppg": 2.85,
            "primary_objective": "PPG >= 2.85",
            "minimum_attack_process_gate": {"metric": "team_xG", "minimum_38_match_total": 100},
            "hard_constraints": {"ip_back_four_positions": ["DL", "DCL", "DCR", "DR"]},
        }), encoding="utf-8")
        gate.RULES.write_text("PPG ≥ 2.85\nxG≥100\n不以现实足球理论作为否决依据；强制引擎行为错位设计。\n每轮从 V0.5 重生；最高优先级。", encoding="utf-8")
        gate.LEDGER.write_text("PPG 2.85 xG≥100", encoding="utf-8")
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
        gate.PROJECT_DIR, gate.POLICY, gate.RULES, gate.LEDGER, gate.PERFORMANCE_STANDARD, gate.V05_BASELINE_SHA256 = self.old_paths

    def write_recipe_and_audit(self):
        raw = json.dumps(self.valid_recipe, ensure_ascii=False, indent=2).encode()
        self.recipe.write_bytes(raw)
        parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        recipe_sha = hashlib.sha256(raw).hexdigest()
        rules_sha = hashlib.sha256(gate.RULES.read_bytes()).hexdigest()
        ledger_sha = hashlib.sha256(gate.LEDGER.read_bytes()).hexdigest()
        policy_sha = hashlib.sha256(gate.POLICY.read_bytes()).hexdigest()
        standard_sha = hashlib.sha256(gate.PERFORMANCE_STANDARD.read_bytes()).hexdigest()
        manifest = self.make_machine_manifest()
        manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2)
        rows = "\n".join(f"| {phase}-{i:02d} | GK | Role / S | U | 未提供 | 未提供 | 未提供 | 未知 | U | 新增待验证 | D5验证 |" for phase in ("IP", "OOP") for i in range(1, 12))
        position_section = (
            "## 位置绩效高强度审查与低效淘汰\n"
            "| 槽位 | 角色 | 分钟 | 评分 | 进球 | xG | 过程 | 风险 | 证据等级 | 判决 | 下一步 |\n"
            + rows + "\n低效淘汰清单：暂无；证据等级完整记录。准入保留、条件保留、替换淘汰均按D5审查。\n"
        )
        self.audit.write_text(
            "版本：gate-test\n项目最高目标：PPG ≥ 2.85；38场xG≥100\n"
            "父版本：V0.5\n重生基准：V0.5\n"
            f"重生基准 FMF SHA-256：{gate.V05_BASELINE_SHA256}\n"
            f"父 FMF SHA-256：{parent_sha}\n本轮配方 SHA-256：{recipe_sha}\n"
            f"项目规则 SHA-256：{rules_sha}\n决策总账 SHA-256：{ledger_sha}\n"
            f"PPG 策略 SHA-256：{policy_sha}\n位置绩效标准 SHA-256：{standard_sha}\n"
            "### 继承保留\n- 暂无；本测试全部作为新假设。\n"
            "### 替换淘汰\n- 旧配置不进入本轮。\n"
            "### 新增待验证\n- 本轮所有配置均为待验证假设。\n"
            "### 证据不足\n- 不足证据不作为继承项。\n"
            "本轮 PPG 收益路径：改善进攻产量以提高积分。\nD5 验证指标：PPG、xG、胜平负。\n风险：新假设可能失败。\n"
            "现实足球理论不是战术筛选/否决标准。\n"
            "## 7. 强制审计：引擎行为错位设计\n"
            "- 错位类型：角色与PI行为错位\n- 错位配置：IP四后场及前场跑动\n"
            "- 角色/指令默认行为：与显式指令可能冲突\n"
            "- FM27引擎预期执行行为：待验证行为\n- 对手AI可能：改变盯人与压迫\n"
            "- 预期创造的空间：形成接球空间\n- 对PPG：增加机会以提高积分\n"
            "- 可能副作用：转换暴露\n- D5量化验证指标：PPG与xG\n"
            + position_section
            + "\n## 机器决策清单（强制）\nMACHINE_DECISION_MANIFEST_JSON_START\n"
            + manifest_text + "\nMACHINE_DECISION_MANIFEST_JSON_END\n"
            + "\n审计结论： PASS\n",
            encoding="utf-8",
        )

    def validate(self):
        return gate.validate(self.recipe, self.audit, self.parent)

    def test_valid_project_iteration_passes(self):
        self.assertEqual(self.validate(), [])

    def test_latest_version_cannot_become_parent(self):
        self.audit.write_text(
            self.audit.read_text(encoding="utf-8").replace("父版本：V0.5", "父版本：V1.8"),
            encoding="utf-8",
        )
        self.assertTrue(any("父版本：V0.5" in e for e in self.validate()))

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


    def make_machine_manifest(self):
        selected = []
        for slot in self.valid_recipe["p"]:
            for phase, key in (("IP", "in"), ("OOP", "out")):
                item = slot[key]
                selected.append({
                    "phase": phase, "pos": item["pos"], "role": item["role"],
                    "duty": item["duty"], "pi": item["pi"],
                    "decision": "新增待验证", "evidence_grade": "U",
                    "rationale": "当前没有足够证据支持继承，因此作为新假设审查。",
                    "hypothesis": "本轮提出一个可由比赛行为数据证伪的新机制假设。",
                    "d5_metric": "完整38场记录PPG、xG和该槽位可归因过程指标。",
                    "failure_condition": "未达到PPG与xG双门槛或机制指标没有改善即判失败。"
                })
        return {"schema_version": 1, "selected_configurations": selected, "retired_configurations": []}

    def test_machine_manifest_matches_all_22_recipe_phases(self):
        manifest = self.make_machine_manifest()
        audit = "MACHINE_DECISION_MANIFEST_JSON_START\n" + json.dumps(manifest, ensure_ascii=False) + "\nMACHINE_DECISION_MANIFEST_JSON_END"
        self.assertEqual(gate.validate_decision_manifest(self.valid_recipe, audit, {}), [])

    def test_machine_manifest_rejects_role_mismatch(self):
        manifest = self.make_machine_manifest()
        manifest["selected_configurations"][7]["role"] = "DifferentRole"
        audit = "MACHINE_DECISION_MANIFEST_JSON_START\n" + json.dumps(manifest, ensure_ascii=False) + "\nMACHINE_DECISION_MANIFEST_JSON_END"
        self.assertTrue(any("do not exactly match" in e for e in gate.validate_decision_manifest(self.valid_recipe, audit, {})))

    def test_unadmitted_historical_role_cannot_be_silently_inherited(self):
        manifest = self.make_machine_manifest()
        entry = manifest["selected_configurations"][14]
        entry["decision"] = "继承保留"
        entry["evidence_grade"] = "B"
        policy = {"historical_non_admitted_configurations": [{
            "phase": entry["phase"], "position": entry["pos"],
            "role": entry["role"], "duty": entry["duty"]
        }]}
        audit = "MACHINE_DECISION_MANIFEST_JSON_START\n" + json.dumps(manifest, ensure_ascii=False) + "\nMACHINE_DECISION_MANIFEST_JSON_END"
        errors = gate.validate_decision_manifest(self.valid_recipe, audit, policy)
        self.assertTrue(any("only return as 新增待验证" in e for e in errors))

    def test_evidence_insufficient_cannot_remain_in_selected_recipe(self):
        manifest = self.make_machine_manifest()
        manifest["selected_configurations"][0]["decision"] = "证据不足"
        audit = "MACHINE_DECISION_MANIFEST_JSON_START\n" + json.dumps(manifest, ensure_ascii=False) + "\nMACHINE_DECISION_MANIFEST_JSON_END"
        self.assertTrue(any("still exists in the selected recipe" in e for e in gate.validate_decision_manifest(self.valid_recipe, audit, {})))

if __name__ == "__main__":
    unittest.main()
