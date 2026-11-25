from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
from scripts.preflight_fm27_tactic import preflight
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


class NativePiPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((GEN_DIR / "style_template_registry.json").read_text(encoding="utf-8"))
        cls.recipe = gen.load_recipe_input(ROOT / "tactic_development/FM27_EngineDividend_4Back/V0.9.json")[0]

    def test_empty_pi_arrays_are_valid_for_all_22_phases(self):
        recipe = copy.deepcopy(self.recipe)
        for slot in recipe["p"]:
            slot["in"]["pi"] = []
            slot["out"]["pi"] = []
        result = preflight(recipe, self.catalog, self.registry)
        self.assertEqual(result["status"], "preflight_passed")
        self.assertEqual(result["checked_phases"], 22)
        self.assertEqual(result["configured_pi_phases"], 0)
        self.assertEqual(result["configured_pi_items"], 0)
        self.assertEqual(result["serialized_pi_override_bits"], 0)

    def test_selected_pi_is_still_checked(self):
        recipe = copy.deepcopy(self.recipe)
        recipe["p"][0]["in"]["pi"] = [["PASSING_STRATEGY", "NOT_A_NATIVE_OPTION"]]
        with self.assertRaises(ValueError):
            preflight(recipe, self.catalog, self.registry)


if __name__ == "__main__":
    unittest.main(verbosity=2)
