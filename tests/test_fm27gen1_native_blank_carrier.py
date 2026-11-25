#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the V0.8 parent snapshot is a format carrier, not a blank tactic."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen
from scripts.preflight_fm27_tactic import preflight

RECIPE_PATH = ROOT / "tactic_development/FM27_EngineDividend_4Back/V0.9.json"
PARENT_SHA256 = "c7480f2c32c55c1b8e8ce3f8724c9ea2c7b2f02fa4e9759b9c6aff8c31d7bb2e"
CANONICAL_CARRIER = "FM27 Native Parent Snapshot (V0.8)"
LEGACY_ALIAS = "FM27 Native Blank (V0.8 Carrier)"


class NativeParentSnapshotCarrierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((GEN_DIR / "style_template_registry.json").read_text(encoding="utf-8"))
        cls.recipe = json.loads(RECIPE_PATH.read_text(encoding="utf-8"))
        cls.carrier = next(x for x in cls.registry["native_carriers"] if x["name"] == CANONICAL_CARRIER)

    def test_native_parent_snapshot_is_not_an_official_style_or_blank_tactic(self):
        self.assertEqual(len(self.registry["styles"]), 10)
        self.assertNotIn(self.carrier, self.registry["styles"])
        self.assertTrue(self.carrier["carrier_only"])
        self.assertEqual(self.carrier["status"], "native_snapshot_verified")
        self.assertIn(LEGACY_ALIAS, self.carrier["aliases"])
        resolved = gen.resolve_style_definition(CANONICAL_CARRIER, self.registry)
        self.assertEqual(resolved["tac_style_string"], "")
        self.assertEqual(resolved["style_code"].hex(), "4c4c554e")
        self.assertEqual(gen.resolve_style_definition(LEGACY_ALIAS, self.registry)["template"], resolved["template"])
        self.assertEqual(gen.resolve_template_path(LEGACY_ALIAS, self.registry), (GEN_DIR / self.carrier["template"]).resolve())

    def test_parent_hash_and_native_identity(self):
        template = gen.resolve_template_path(CANONICAL_CARRIER, self.registry)
        raw = template.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), PARENT_SHA256)
        fmf = gen.parse_fmf(raw)
        tac = gen.parse_tac(fmf.data_by_ext[".tac"])
        self.assertEqual(tac.style, "")
        self.assertEqual(bytes(tac.quad).hex(), "4c4c554e")
        self.assertEqual(int(tac.hdr[2]), 4)

    def test_v09_official_snapshot_is_registered_as_a_parent_carrier(self):
        carrier = next(
            x for x in self.registry["native_carriers"]
            if x["name"] == "FM27 Native Parent Snapshot (V0.9)"
        )
        self.assertTrue(carrier["carrier_only"])
        self.assertEqual(carrier["status"], "native_snapshot_verified")
        template = gen.resolve_template_path(carrier["name"], self.registry)
        raw = template.read_bytes()
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            "5dc33a05f032345ca9c674b02d48e7619b32303e3e0eb54930598941df3456a1",
        )
        parsed = gen.parse_fmf(raw)
        tac = gen.parse_tac(parsed.data_by_ext[".tac"])
        self.assertEqual(tac.style, "")
        self.assertEqual(bytes(tac.quad).hex(), "4c4c554e")
        self.assertEqual(len(tac.pairs), 11)

    def test_v10_recipe_reuses_v09_parent_and_resets_only_two_team_instruction_groups(self):
        recipe_path = ROOT / "tactic_development/FM27_EngineDividend_4Back/V1.0.json"
        recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        self.assertEqual(recipe["base"]["g"], "FM27 Native Parent Snapshot (V0.9)")
        self.assertEqual(recipe["ti"]["ATTACKING_WIDTH"], "DEFAULT")
        self.assertEqual(recipe["ti"]["DEFENSIVE_LINE"], "DEFAULT")
        self.assertEqual(recipe["ti"]["TEMPO"], "HIGHER")
        self.assertEqual(recipe["ti"]["TRIGGER_PRESS"], "MORE_OFTEN")
        self.assertEqual(len(recipe["p"]), 11)
        for old_slot, new_slot in zip(self.recipe["p"], recipe["p"]):
            self.assertEqual(old_slot, new_slot)
        preflight_result = preflight(recipe, self.catalog, self.registry)
        self.assertEqual(preflight_result["checked_phases"], 22)
        fmf_bytes, report = gen.build_fmf_from_recipe(recipe, self.catalog, style_registry=self.registry)
        self.assertEqual(
            report["template_sha256"],
            "5dc33a05f032345ca9c674b02d48e7619b32303e3e0eb54930598941df3456a1",
        )
        self.assertEqual(len(report["player_phase_map"]), 22)
        self.assertEqual(len(report["readback_player_phase_map"]), 22)
        parsed = gen.parse_fmf(fmf_bytes)
        tac = gen.parse_tac(parsed.data_by_ext[".tac"])
        for bit in (52, 58):  # V0.9 narrower width / lower defensive line
            self.assertEqual(tac.packed[bit // 8] & (1 << (bit % 8)), 0)
        self.assertEqual(tac.style, "")
        self.assertEqual(bytes(tac.quad).hex(), "4c4c554e")

    def test_full_v09_recipe_preflight_and_roundtrip(self):
        gen.validate_recipe_structure(self.recipe)
        phases = [x for slot in self.recipe["p"] for x in (slot["in"], slot["out"])]
        self.assertEqual(len(self.recipe["p"]), 11)
        self.assertEqual(len(phases), 22)
        self.assertTrue(all(x["pi"] for x in phases))
        preflight_result = preflight(self.recipe, self.catalog, self.registry)
        self.assertEqual(preflight_result["checked_phases"], 22)
        self.assertEqual(preflight_result["configured_pi_phases"], 22)
        fmf_bytes, report = gen.build_fmf_from_recipe(self.recipe, self.catalog, style_registry=self.registry)
        self.assertEqual(report["status"], "offline_binary_roundtrip_verified_not_game_import_verified")
        self.assertEqual(report["template_sha256"], PARENT_SHA256)
        self.assertEqual(report["tac_style_string"], "")
        self.assertEqual(report["style_code_hex"], "4c4c554e")
        self.assertEqual(len(report["player_phase_map"]), 22)
        self.assertEqual(len(report["readback_player_phase_map"]), 22)
        self.assertEqual(sorted(x["position"] for x in report["readback_player_phase_map"] if x["phase"] == "in" and x["position"] in {"DL", "DCL", "DCR", "DR"}), ["DCL", "DCR", "DL", "DR"])
        parsed = gen.parse_fmf(fmf_bytes)
        tac = gen.parse_tac(parsed.data_by_ext[".tac"])
        self.assertEqual(tac.style, "")
        self.assertEqual(bytes(tac.quad).hex(), "4c4c554e")

    def test_all_empty_pi_arrays_pass_permission_preflight_and_build(self):
        recipe = json.loads(json.dumps(self.recipe))
        for slot in recipe["p"]:
            slot["in"]["pi"] = []
            slot["out"]["pi"] = []
        result = preflight(recipe, self.catalog, self.registry)
        self.assertEqual(result["checked_phases"], 22)
        self.assertEqual(result["configured_pi_phases"], 0)
        self.assertEqual(result["configured_pi_items"], 0)
        self.assertEqual(result["serialized_pi_override_bits"], 0)
        fmf_bytes, report = gen.build_fmf_from_recipe(recipe, self.catalog, style_registry=self.registry)
        self.assertEqual(len(report["player_phase_map"]), 22)
        self.assertEqual(len(report["readback_player_phase_map"]), 22)
        self.assertTrue(fmf_bytes)

    def test_invalid_selected_pi_is_rejected(self):
        recipe = json.loads(json.dumps(self.recipe))
        recipe["p"][0]["in"]["pi"] = [["PASSING_STRATEGY", "NOT_A_NATIVE_OPTION"]]
        with self.assertRaises(ValueError):
            preflight(recipe, self.catalog, self.registry)


if __name__ == "__main__":
    unittest.main(verbosity=2)
