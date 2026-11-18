from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))

import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


class ExperimentalMappingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))

    def test_experimental_pi_ids_exist_in_native_catalog_groups(self):
        group_ids = {
            "CROSSING_TARGET": 9,
            "ROAMING": 4,
            "CROSSING_FREQUENCY": 10,
            "ATTACK_BOX_DEPTH": 16,
            "TRIGGER_PRESS": 11,
            "TACKLING": 13,
        }
        groups = {int(g["id"]): g for g in self.catalog["player_instructions"]}
        for (group, option), native_id in gen.EXPERIMENTAL_PI_MAP.items():
            native_group = groups[group_ids[group]]
            self.assertIn(
                native_id,
                {int(x["id"]) for x in native_group["options"]},
                f"{group}={option} -> native option ID {native_id}",
            )

    def test_experimental_ti_bits_exist_in_native_catalog_groups(self):
        groups = {int(g["id"]): g for g in self.catalog["team_instructions"]}
        for (key, option), native_bit in gen.EXPERIMENTAL_TI_MAP.items():
            group_ids = gen.TI_GROUPS[key]
            available_bits = {
                int(x.get("native_bit") or 0)
                for group_id in group_ids
                for x in groups[group_id]["options"]
            }
            self.assertIn(
                native_bit,
                available_bits,
                f"{key}={option} -> native bit {native_bit}",
            )

    def test_experimental_test_recipe_has_22_permission_checked_pi_phases(self):
        raw_recipe_path = os.environ.get("RECIPE_PATH", "build_requests/Unmapped_Mapping_Import_Test_v1.txt")
        recipe_path = Path(raw_recipe_path)
        if not recipe_path.is_absolute():
            recipe_path = ROOT / recipe_path
        if not recipe_path.is_file():
            self.skipTest(f"Import-test GEN1 recipe is not present in this commit: {recipe_path}")
        recipe = gen.parse_gen1(recipe_path)
        self.assertEqual(len(recipe["p"]), 11)
        phase_count = 0
        experimental_pi_count = 0
        for slot, spec in enumerate(recipe["p"]):
            for phase, key in ((0, "in"), (1, "out")):
                item = spec[key]
                position = gen.native_position_id(item["pos"], phase)
                role_id = gen.role_id_from_display(item["role"], phase, {x["id"] for x in self.catalog["roles"]})
                duty = gen.ROLE_DUTY[role_id]
                self.assertIn(role_id, self.catalog["role_eligibility"][position][phase])
                bits = gen.encode_pi(item["pi"], self.catalog, phase, position, role_id, duty)
                self.assertGreater(bits, 0, f"slot={slot}, phase={key}: PI mask is empty")
                phase_count += 1
                experimental_pi_count += sum(
                    (str(pair[0]), str(pair[1])) in gen.EXPERIMENTAL_PI_MAP
                    for pair in item["pi"]
                )
        self.assertEqual(phase_count, 22)
        self.assertGreaterEqual(experimental_pi_count, 6)

        ti_vector = gen.encode_ti(recipe, self.catalog, bytearray(12))
        self.assertEqual(len(ti_vector), 12)
        self.assertGreaterEqual(len(recipe.get("ti", {})), 6)
        self.assertTrue(
            any((key, value) in gen.EXPERIMENTAL_TI_MAP.items()
                for key, value in recipe["ti"].items())
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
