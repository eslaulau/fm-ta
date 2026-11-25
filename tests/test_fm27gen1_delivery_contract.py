from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_fm27_tactic_delivery.py"
spec = importlib.util.spec_from_file_location("fm27_tactic_delivery_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

GEN = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


class TacticDeliveryStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipe = gen.load_recipe_input(ROOT / "build_requests" / "Unmapped_Mapping_Import_Test_v1.json")[0]

    def test_established_full_recipe_passes_22_phase_structure(self):
        result = validator.validate_deliverable_recipe(self.recipe)
        self.assertEqual(result["status"], "recipe_structure_passed")
        self.assertEqual(result["phase_count"], 22)
        self.assertTrue(result["empty_pi_phases_allowed"])

    def test_one_empty_pi_phase_is_valid(self):
        recipe = copy.deepcopy(self.recipe)
        recipe["p"][4]["out"]["pi"] = []
        result = validator.validate_deliverable_recipe(recipe)
        self.assertEqual(result["phase_count"], 22)
        self.assertEqual(result["pi_counts"][9], 0)

    def test_all_empty_pi_phases_are_valid(self):
        recipe = copy.deepcopy(self.recipe)
        for spec in recipe["p"]:
            spec["in"]["pi"] = []
            spec["out"]["pi"] = []
        result = validator.validate_deliverable_recipe(recipe)
        self.assertEqual(result["phase_count"], 22)
        self.assertEqual(result["configured_pi_phases"], 0)
        self.assertEqual(result["configured_pi_items"], 0)
        self.assertEqual(result["pi_counts"], [0] * 22)

    def test_pi_field_is_still_required(self):
        recipe = copy.deepcopy(self.recipe)
        del recipe["p"][0]["in"]["pi"]
        with self.assertRaisesRegex(ValueError, "缺少必需字段"):
            validator.validate_deliverable_recipe(recipe)


if __name__ == "__main__":
    unittest.main(verbosity=2)
