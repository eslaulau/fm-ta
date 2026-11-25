#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the V0.8 blank-style native snapshot is a carrier, not an official style."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen

RECIPE_PATH = ROOT / "tactic_development/FM27_EngineDividend_4Back/V0.9.json"
PARENT_SHA256 = "c7480f2c32c55c1b8e8ce3f8724c9ea2c7b2f02fa4e9759b9c6aff8c31d7bb2e"


class NativeBlankCarrierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((GEN_DIR / "style_template_registry.json").read_text(encoding="utf-8"))
        cls.recipe = json.loads(RECIPE_PATH.read_text(encoding="utf-8"))
        cls.carrier = next(x for x in cls.registry["native_carriers"]
                           if x["name"] == cls.recipe["base"]["g"])

    def test_native_carrier_is_not_an_official_style(self):
        self.assertEqual(len(self.registry["styles"]), 10)
        self.assertNotIn(self.carrier, self.registry["styles"])
        self.assertTrue(self.carrier["carrier_only"])
        self.assertEqual(self.carrier["status"], "native_snapshot_verified")
        resolved = gen.resolve_style_definition(self.carrier["name"], self.registry)
        self.assertEqual(resolved["tac_style_string"], "")
        self.assertEqual(resolved["style_code"].hex(), "4c4c554e")
        self.assertEqual(gen.resolve_template_path(self.carrier["name"], self.registry),
                         (GEN_DIR / self.carrier["template"]).resolve())

    def test_parent_hash_and_native_identity(self):
        template = gen.resolve_template_path(self.carrier["name"], self.registry)
        raw = template.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), PARENT_SHA256)
        fmf = gen.parse_fmf(raw)
        tac = gen.parse_tac(fmf.data_by_ext[".tac"])
        self.assertEqual(tac.style, "")
        self.assertEqual(bytes(tac.quad).hex(), "4c4c554e")
        self.assertEqual(int(tac.hdr[2]), 4)

    def test_full_v09_recipe_preflight_and_roundtrip(self):
        gen.validate_recipe_structure(self.recipe)
        phases = [x for slot in self.recipe["p"] for x in (slot["in"], slot["out"])]
        self.assertEqual(len(self.recipe["p"]), 11)
        self.assertEqual(len(phases), 22)
        self.assertTrue(all(x["pi"] for x in phases))
        fmf_bytes, report = gen.build_fmf_from_recipe(
            self.recipe, self.catalog, style_registry=self.registry
        )
        self.assertEqual(report["status"], "offline_binary_roundtrip_verified_not_game_import_verified")
        self.assertEqual(report["template_sha256"], PARENT_SHA256)
        self.assertEqual(report["tac_style_string"], "")
        self.assertEqual(report["style_code_hex"], "4c4c554e")
        self.assertEqual(len(report["player_phase_map"]), 22)
        self.assertEqual(len(report["readback_player_phase_map"]), 22)
        self.assertEqual(
            sorted(x["position"] for x in report["readback_player_phase_map"]
                   if x["phase"] == "IP" and x["position"] in {"DL", "DCL", "DCR", "DR"}),
            ["DCL", "DCR", "DL", "DR"],
        )
        parsed = gen.parse_fmf(fmf_bytes)
        tac = gen.parse_tac(parsed.data_by_ext[".tac"])
        self.assertEqual(tac.style, "")
        self.assertEqual(bytes(tac.quad).hex(), "4c4c554e")


if __name__ == "__main__":
    unittest.main(verbosity=2)
