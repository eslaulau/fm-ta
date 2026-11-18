from __future__ import annotations

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


class TacticDeliveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipe = gen.load_recipe_input(ROOT / "build_requests" / "Unmapped_Mapping_Import_Test_v1.json")[0]

    def test_established_full_recipe_passes_22_of_22_pi_delivery_gate(self):
        result = validator.validate_deliverable_recipe(self.recipe)
        self.assertEqual(result["status"], "deliverable_structure_passed")
        self.assertEqual(result["phase_count"], 22)
        self.assertEqual(result["non_empty_pi_phases"], 22)
        self.assertTrue(all(count >= 1 for count in result["pi_counts"]))

    def test_any_empty_pi_phase_is_rejected_with_slot_and_phase(self):
        recipe = json.loads(json.dumps(self.recipe))
        recipe["p"][4]["out"]["pi"] = []
        with self.assertRaisesRegex(ValueError, r"slot 4 out"):
            validator.validate_deliverable_recipe(recipe)

    def test_all_empty_pi_phases_are_rejected(self):
        recipe = json.loads(json.dumps(self.recipe))
        for spec in recipe["p"]:
            spec["in"]["pi"] = []
            spec["out"]["pi"] = []
        with self.assertRaisesRegex(ValueError, "22/22"):
            validator.validate_deliverable_recipe(recipe)


if __name__ == "__main__":
    unittest.main(verbosity=2)
