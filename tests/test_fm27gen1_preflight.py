from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
from scripts.preflight_fm27_tactic import preflight, validate_formation_role_compatibility
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


class NativePiPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((GEN_DIR / "style_template_registry.json").read_text(encoding="utf-8"))
        cls.recipe = gen.load_recipe_input(ROOT / "tactic_development/FM27_EngineDividend_4Back/V0.9.json")[0]
        # These PI-focused tests need a valid four-back fixture; preserve V0.9 history and correct only the copied test data.
        for slot in cls.recipe["p"]:
            if slot["in"]["pos"] == "DCL" and slot["in"]["role"] == "WideCentreBack":
                slot["in"]["role"] = "CentreBack"

    def test_four_back_wide_centre_back_is_rejected(self):
        recipe = gen.load_recipe_input(ROOT / "tactic_development/FM27_EngineDividend_4Back/V1.0.json")[0]
        with self.assertRaisesRegex(ValueError, "only available to an outer centre-back in a back-three shape"):
            preflight(recipe, self.catalog, self.registry)

    def test_wide_centre_back_is_allowed_on_outer_slot_of_back_three(self):
        result = validate_formation_role_compatibility([
            {"pos": "DCL", "role": "WideCentreBack"},
            {"pos": "DC", "role": "CentreBack"},
            {"pos": "DCR", "role": "BallPlayingCentreBack"},
        ], 0)
        self.assertEqual(result["centre_back_count"], 3)
        self.assertEqual(result["formation_dependent_roles"], [
            {"position": "DCL", "role": "WideCentreBack"}
        ])

    def test_overlapping_centre_back_is_rejected_in_four_back_shape(self):
        with self.assertRaisesRegex(ValueError, "only available to an outer centre-back in a back-three shape"):
            validate_formation_role_compatibility([
                {"pos": "DL", "role": "FullBack"},
                {"pos": "DCL", "role": "CentreBack"},
                {"pos": "DCR", "role": "OverlappingCentreBack"},
                {"pos": "DR", "role": "FullBack"},
            ], 0)

    def test_oop_wide_centre_back_is_rejected_in_four_back_shape(self):
        with self.assertRaisesRegex(ValueError, "only available to an outer centre-back in a back-three shape"):
            validate_formation_role_compatibility([
                {"pos": "DL", "role": "OPFullBack"},
                {"pos": "DCL", "role": "OPWideCentreBack"},
                {"pos": "DCR", "role": "OPCoveringCentreBack"},
                {"pos": "DR", "role": "OPFullBack"},
            ], 1)

    def test_oop_wide_centre_back_is_allowed_in_three_back_shape(self):
        result = validate_formation_role_compatibility([
            {"pos": "DCL", "role": "OPWideCentreBack"},
            {"pos": "DC", "role": "OPCentreBack"},
            {"pos": "DCR", "role": "OPCoveringCentreBack"},
        ], 1)
        self.assertEqual(result["centre_back_count"], 3)

    def test_v11_four_back_with_strikerless_oop_five_back_preflights(self):
        recipe = gen.load_recipe_input(ROOT / "tactic_development/FM27_EngineDividend_4Back/V1.1.json")[0]
        result = preflight(recipe, self.catalog, self.registry)
        self.assertEqual(result["checked_phases"], 22)
        self.assertEqual(result["formation_role_checks"][0]["centre_back_positions"], ["DCR", "DCL"])
        self.assertEqual(result["formation_role_checks"][0]["centre_back_count"], 2)
        self.assertEqual(set(result["formation_role_checks"][1]["centre_back_positions"]), {"DCR", "DCL", "DC"})
        self.assertEqual(result["formation_role_checks"][1]["centre_back_count"], 3)
        self.assertEqual(set(result["formation_role_checks"][1]["formation_dependent_roles"]), {
            ("DCR", "OPCoveringWideCentreBack"),
            ("DCL", "OPCoveringWideCentreBack"),
        })
        oop_positions = {slot["out"]["pos"] for slot in recipe["p"]}
        self.assertEqual(oop_positions, {"GK", "WBR", "DCR", "DCL", "WBL", "DC", "DMR", "AMR", "AML", "DML", "AMC"})
        oop_by_pos = {slot["out"]["pos"]: slot["out"] for slot in recipe["p"]}
        self.assertEqual(oop_by_pos["WBR"]["role"], "PressingWingBack")
        self.assertEqual(oop_by_pos["WBL"]["role"], "PressingWingBack")
        self.assertEqual(oop_by_pos["WBR"]["pi"], [["TACKLING", "GET_STUCK_IN"]])
        self.assertEqual(oop_by_pos["WBL"]["pi"], [["TACKLING", "GET_STUCK_IN"]])
        # The two pivot roles supply their own press-frequency defaults; do not serialize duplicate overrides.
        self.assertNotIn(["TRIGGER_PRESS", "MORE_OFTEN"], oop_by_pos["DMR"]["pi"])
        self.assertNotIn(["TRIGGER_PRESS", "LESS_OFTEN"], oop_by_pos["DML"]["pi"])
        self.assertNotIn("ST", oop_positions)
        self.assertEqual(result["configured_pi_items"], result["serialized_pi_override_bits"] + result["selected_fixed_on_options"])

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
        self.assertEqual(result["selected_fixed_on_options"], 0)

    def test_empty_pi_does_not_require_a_policy_table(self):
        recipe = copy.deepcopy(self.recipe)
        item = recipe["p"][0]["in"]
        role_id = gen.role_id_from_display(item["role"], 0, {x["id"] for x in self.catalog["roles"]})
        duty = gen.resolve_role_duty(role_id, item)
        pos_id = gen.native_position_id(item["pos"], 0)
        catalog = copy.deepcopy(self.catalog)
        catalog["pi_policies"].pop(f"0:{pos_id}:{role_id}:{duty}", None)
        recipe["p"][0]["in"]["pi"] = []
        result = preflight(recipe, catalog, self.registry)
        self.assertEqual(result["checked_phases"], 22)
        self.assertEqual(result["roles"][0]["serialized_override_bit_count"], 0)

    def test_fixed_on_selections_are_counted_separately_from_override_bits(self):
        result = preflight(self.recipe, self.catalog, self.registry)
        self.assertEqual(
            result["configured_pi_items"],
            result["serialized_pi_override_bits"] + result["selected_fixed_on_options"],
        )

    def test_selected_pi_is_still_checked(self):
        recipe = copy.deepcopy(self.recipe)
        recipe["p"][0]["in"]["pi"] = [["PASSING_STRATEGY", "NOT_A_NATIVE_OPTION"]]
        with self.assertRaises(ValueError):
            preflight(recipe, self.catalog, self.registry)


if __name__ == "__main__":
    unittest.main(verbosity=2)
