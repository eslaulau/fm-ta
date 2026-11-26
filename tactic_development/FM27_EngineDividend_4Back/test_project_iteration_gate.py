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
        self.recipe = self.root / "candidate.json"
        self.audit = self.root / "design_audit.md"
        self.parent = self.root / "parent.fmf"
        self.parent.write_bytes(b"exact parent FMF bytes")
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

    def write_recipe_and_audit(self):
        raw = json.dumps(self.valid_recipe, ensure_ascii=False, indent=2).encode()
        self.recipe.write_bytes(raw)
        parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        recipe_sha = hashlib.sha256(raw).hexdigest()
        self.audit.write_text(
            "项目最高目标：PPG ≥ 2.85\n"
            "父版本：V1.8\n"
            f"父 FMF SHA-256：{parent_sha}\n"
            f"本轮配方 SHA-256：{recipe_sha}\n"
            "### 继承保留\n### 替换淘汰\n### 新增待验证\n### 证据不足\n"
            "D5 验证指标：PPG、胜平负、xG、xGA\n"
            "风险：样本量不足\n审计结论： PASS\n",
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

    def test_missing_decision_class_is_rejected(self):
        self.audit.write_text(
            self.audit.read_text(encoding="utf-8").replace("### 证据不足\n", ""),
            encoding="utf-8",
        )
        self.assertTrue(any("证据不足" in e for e in self.validate()))


if __name__ == "__main__":
    unittest.main()
