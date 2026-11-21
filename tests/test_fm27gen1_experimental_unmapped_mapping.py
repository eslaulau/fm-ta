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

    def test_all_non_default_native_pi_options_have_exact_generator_mappings(self):
        native_groups = {
            0: "ATTACKING_WIDTH",
            1: "DRIBBLING_DIRECTION",
            2: "DRIBBLING_FREQUENCY",
            3: "FORWARD_RUNS",
            4: "ROAMING",
            5: "HOLD_UP_BALL",
            6: "SHOOTING",
            7: "PASSING_STRATEGY",
            8: "PASSING_RISKS",
            9: "CROSSING_TARGET",
            10: "CROSSING_FREQUENCY",
            11: "TRIGGER_PRESS",
            12: "MARKING",
            13: "TACKLING",
            14: "MARKING_TARGET",
            15: "ATTACK_BOX_SIDE",
            16: "ATTACK_BOX_DEPTH",
        }
        expected = {}
        for group in self.catalog["player_instructions"]:
            token = native_groups[int(group["id"])]
            for option in group["options"]:
                native_id = int(option["id"])
                if native_id:
                    self.assertNotIn(native_id, expected)
                    expected[native_id] = token
        self.assertEqual(len(expected), 37)
        actual = {native_id: key[0] for key, native_id in gen.PI_MAP.items()}
        self.assertEqual(len(actual), len(gen.PI_MAP), "PI native IDs must be unique")
        self.assertEqual(set(actual), set(expected))
        for native_id, expected_group in expected.items():
            self.assertEqual(actual[native_id], expected_group, f"native PI option {native_id}")

    def test_every_pi_option_id_has_a_valid_editable_context_and_encodes(self):
        native_ids = {int(value) for value in gen.PI_MAP.values()}
        self.assertEqual(len(native_ids), 37)
        self.assertEqual(len(self.catalog["pi_policies"]), 1547)
        for (group, option), native_id in gen.PI_MAP.items():
            found_editable_context = False
            for policy_key, revisions in self.catalog["pi_policies"].items():
                values = list(revisions.values())
                self.assertTrue(values, f"empty PI policy: {policy_key}")
                states = set()
                for value in values:
                    self.assertIsInstance(value, str)
                    self.assertLess(native_id, len(value), f"{policy_key}: option {native_id}")
                    states.add(value[native_id])
                # A few historical policy keys differ across catalog versions.
                # encode_pi() rejects those specific contexts; only a fully
                # consistent editable context can be used for this encode test.
                if states == {"0"}:
                    phase, position, role_id, duty = policy_key.split(":", 3)
                    bits = gen.encode_pi(
                        [[group, option]], self.catalog, int(phase), position,
                        role_id, int(duty),
                    )
                    self.assertEqual(bits, 1 << native_id, f"{group}={option}")
                    found_editable_context = True
                    break
            self.assertTrue(found_editable_context, f"PI option {native_id} has no editable role context")


    def test_legacy_cross_from_byline_alias_encodes_native_option_8(self):
        # catalog.json group 10 is the native "Crossing From" menu;
        # option ID 8 is "Crossing From Byline". The source A4.11 GEN1
        # uses the older CROSS_FROM token for this same native option.
        group = next(g for g in self.catalog["player_instructions"] if int(g["id"]) == 10)
        self.assertIn(8, {int(option["id"]) for option in group["options"]})
        policy_key = "0:DR:WingBack:4194304"
        self.assertEqual(
            {value[8] for value in self.catalog["pi_policies"][policy_key].values()},
            {"0"},
        )
        legacy_bits = gen.encode_pi(
            [["CROSS_FROM", "BYLINE"]], self.catalog, 0, "DR", "WingBack", 4194304
        )
        canonical_bits = gen.encode_pi(
            [["CROSSING_FREQUENCY", "BYLINE"]], self.catalog, 0, "DR", "WingBack", 4194304
        )
        self.assertEqual(legacy_bits, 1 << 8)
        self.assertEqual(legacy_bits, canonical_bits)


    def test_legacy_crossing_strategy_far_post_alias_encodes_native_option_10(self):
        # The original A4.11 GEN1 uses CROSSING_STRATEGY=FAR_POST.
        # In the native catalog this is group 9, option 10 ("后点").
        group = next(g for g in self.catalog["player_instructions"] if int(g["id"]) == 9)
        self.assertIn(10, {int(option["id"]) for option in group["options"]})
        policy_key = "0:DR:WingBack:4194304"
        self.assertEqual(
            {value[10] for value in self.catalog["pi_policies"][policy_key].values()},
            {"0"},
        )
        legacy_bits = gen.encode_pi(
            [["CROSSING_STRATEGY", "FAR_POST"]], self.catalog, 0, "DR", "WingBack", 4194304
        )
        canonical_bits = gen.encode_pi(
            [["CROSSING_TARGET", "BACK_POST"]], self.catalog, 0, "DR", "WingBack", 4194304
        )
        self.assertEqual(legacy_bits, 1 << 10)
        self.assertEqual(legacy_bits, canonical_bits)

    def test_conflicting_pi_catalog_revisions_are_rejected_for_that_context(self):
        with self.assertRaisesRegex(ValueError, "权限冲突"):
            gen.encode_pi(
                [["ROAMING", "ROAM_FROM_POSITION"]], self.catalog,
                0, "AMC", "FreeRole", 0,
            )

    def test_unmapped_native_role_duties_are_explicit_and_complete(self):
        native_roles = {item["id"] for item in self.catalog["roles"]}
        unmapped = native_roles - set(gen.ROLE_DUTY)
        self.assertEqual(len(native_roles), 79)
        self.assertEqual(len(gen.ROLE_DUTY), 73)
        self.assertEqual(unmapped, set(gen.ROLE_DUTY_UNMAPPED))
        self.assertEqual(
            unmapped,
            {
                "PlaymakingWinger",
                "OPCoveringWideCentreBack",
                "OverlappingCentreBack",
                "FalseNine",
                "HalfBack",
                "AdvancedCentreBack",
            },
        )
        self.assertTrue(set(gen.ROLE_DUTY.values()).issubset(gen.DUTY_FLAGS))

    def test_every_native_ti_group_and_active_bit_has_a_mapping(self):
        native_groups = {
            int(group["id"]): group for group in self.catalog["team_instructions"]
        }
        mapped_group_ids = {
            group_id for group_ids in gen.TI_GROUPS.values() for group_id in group_ids
        }
        self.assertEqual(mapped_group_ids, set(native_groups))
        flattened_groups = [
            group_id for group_ids in gen.TI_GROUPS.values() for group_id in group_ids
        ]
        self.assertEqual(len(flattened_groups), len(native_groups))
        self.assertEqual(len(mapped_group_ids), len(native_groups))

        native_bits = {
            int(option.get("native_bit") or 0)
            for group in native_groups.values()
            for option in group["options"]
            if int(option.get("native_bit") or 0) > 0
        }
        mapped_bits = {
            int(bit) for bit in gen.TI_MAP.values() if int(bit) > 0
        }
        self.assertEqual(len(native_bits), 75)
        self.assertEqual(len(mapped_bits), len(gen.TI_MAP) - sum(
            1 for bit in gen.TI_MAP.values() if int(bit) == 0
        ))
        self.assertEqual(mapped_bits, native_bits)

        for (key, option), native_bit in gen.TI_MAP.items():
            if int(native_bit) == 0:
                continue
            target_groups = set(gen.TI_GROUPS[key])
            owners = {
                int(group["id"])
                for group in self.catalog["team_instructions"]
                if any(
                    int(item.get("native_bit") or 0) == int(native_bit)
                    for item in group["options"]
                )
            }
            self.assertTrue(
                target_groups & owners,
                f"{key}={option} -> bit {native_bit} is not in mapped native group",
            )

    def test_native_ti_options_encode_exact_bits(self):
        for (key, option), native_bit in gen.TI_MAP.items():
            with self.subTest(key=key, option=option, native_bit=native_bit):
                vector = gen.encode_ti({"ti": {key: option}}, self.catalog, bytearray(12))
                self.assertEqual(len(vector), 12)
                actual_bits = {
                    bit for bit in range(96)
                    if vector[bit // 8] & (1 << (bit % 8))
                }
                expected_bits = {int(native_bit)} if int(native_bit) else set()
                self.assertEqual(actual_bits, expected_bits, f"{key}={option}")

    def test_six_roles_accept_explicit_native_duty_for_all_catalog_duty_states(self):
        cases = [
            (0, "MR", "PlaymakingWinger"),
            (1, "DCR", "OPCoveringWideCentreBack"),
            (0, "DC", "OverlappingCentreBack"),
            (0, "ST", "FalseNine"),
            (0, "DMC", "HalfBack"),
            (0, "DC", "AdvancedCentreBack"),
        ]
        native_duties = {int(value) for value in self.catalog["duties"]}
        for phase, position, role_id in cases:
            with self.subTest(role=role_id):
                self.assertIn(role_id, self.catalog["role_eligibility"][position][phase])
                self.assertNotIn(role_id, gen.ROLE_DUTY)
                for duty in native_duties:
                    self.assertIn(f"{phase}:{position}:{role_id}:{duty}", self.catalog["pi_policies"])
                    self.assertEqual(gen.resolve_role_duty(role_id, {"duty": duty}), duty)
                    self.assertEqual(gen.encode_pi([], self.catalog, phase, position, role_id, duty), 0)
                with self.assertRaisesRegex(ValueError, "显式填写 duty"):
                    gen.resolve_role_duty(role_id, {})
        self.assertEqual(gen.resolve_role_duty("CentreBack", {}), 2097152)
        self.assertEqual(gen.resolve_role_duty("CentreBack", {"duty": "SUPPORT"}), 4194304)
        self.assertEqual(gen.resolve_role_duty("CentreBack", {"duty": "A"}), 8388608)
        self.assertEqual(gen.resolve_role_duty("FalseNine", {"duty": "NONE"}), 0)
        with self.assertRaises(ValueError):
            gen.resolve_role_duty("FalseNine", {"duty": True})

    def test_hold_shape_uses_real_native_bit_and_supporting_run_groups_are_separate(self):
        self.assertEqual(gen.TI_MAP[("ATTACKING_TRANSITION", "HOLD_SHAPE")], 55)
        self.assertEqual(gen.TI_GROUPS["SUPPORTING_RUNS"], [28])
        self.assertEqual(gen.TI_GROUPS["SUPPORTING_RUNS_SECONDARY"], [31])
        self.assertEqual(gen.TI_GROUPS["GOALKEEPER_ATTACKING_SET_PIECES"], [32])

    def test_experimental_test_recipe_has_22_permission_checked_pi_phases(self):
        raw_recipe_path = os.environ.get("RECIPE_PATH", "build_requests/Unmapped_Mapping_Import_Test_v1.txt")
        recipe_path = Path(raw_recipe_path)
        if not recipe_path.is_absolute():
            recipe_path = ROOT / recipe_path
        if not recipe_path.is_file():
            self.skipTest(f"Import-test GEN1 recipe is not present in this commit: {recipe_path}")
        recipe, input_format = gen.load_recipe_input(recipe_path)
        self.assertIn(input_format, {"json", "legacy_gen1_base64"})
        self.assertEqual(len(recipe["p"]), 11)
        phase_count = 0
        experimental_pi_count = 0
        for slot, spec in enumerate(recipe["p"]):
            for phase, key in ((0, "in"), (1, "out")):
                item = spec[key]
                position = gen.native_position_id(item["pos"], phase)
                role_id = gen.role_id_from_display(item["role"], phase, {x["id"] for x in self.catalog["roles"]})
                duty = gen.resolve_role_duty(role_id, item)
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
            any((key, value) in gen.EXPERIMENTAL_TI_MAP
                for key, value in recipe["ti"].items())
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
