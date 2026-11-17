#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercise real FM27GEN1 generation against every registered native style template."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
RULES_DIR = GEN_DIR.parent
GEN_PATH = GEN_DIR / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG_PATH = GEN_DIR / "catalog.json"
REGISTRY_PATH = GEN_DIR / "style_template_registry.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("fm27gen1_all_styles", GEN_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载 FM27GEN1 生成器")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AllTenNativeStylesGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gen = load_generator()
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.styles = cls.registry["styles"]
        cls.roles_by_flag_phase = {
            (int(role["flags"]), int(role["phase"])): role["id"]
            for role in cls.catalog["roles"]
        }
        cls.positions_by_mask = {
            int(position["mask"]): position["id"]
            for position in cls.catalog["positions"]
        }

    def recipe_from_native_sample(self, style):
        evidence = style["evidence"]
        sample_path = ROOT / evidence["sample_path"]
        sample_fmf = self.gen.parse_fmf(sample_path.read_bytes())
        sample_tac = self.gen.parse_tac(sample_fmf.data_by_ext[".tac"])
        self.assertEqual(sample_tac.magic[11], 27, style["name"])
        self.assertEqual(len(sample_tac.pairs), 11, style["name"])

        players = []
        for pair in sorted(sample_tac.pairs, key=lambda item: item.slot):
            slot = {}
            for phase, key, block in (
                (0, "in", pair.ip),
                (1, "out", pair.oop),
            ):
                position = self.positions_by_mask[block.selector]
                role_flag = block.mask & self.gen.ROLE_MASK
                role_id = self.roles_by_flag_phase[(role_flag, phase)]
                # role_id_from_display adds the native OOP prefix itself.
                role_name = role_id[2:] if phase == 1 and role_id.startswith("OP") else role_id
                slot[key] = {
                    "pos": position,
                    "role": role_name,
                    # This is a structural generation smoke test. PI override
                    # selection is separately checked against the full catalog.
                    "pi": [],
                }
            players.append(slot)

        return {
            "v": 1,
            "name": f"CI {style['name']} native roundtrip",
            "base": {"g": style["name"]},
            "ment": int(sample_tac.hdr[2]),
            "ti": {},
            "p": players,
        }

    def test_all_ten_styles_generate_from_their_registered_native_template(self):
        self.assertEqual(len(self.styles), 10)
        self.assertEqual(
            {style["name"] for style in self.styles},
            {
                "Catenaccio", "Control Possession", "Direct Counter Attack",
                "Fluid Counter Attack", "Gegenpress", "Park The Bus",
                "Route One", "Tiki-Taka", "Vertical Tiki-Taka", "Wingplay",
            },
        )
        codes = set()
        results = []
        for style in self.styles:
            with self.subTest(style=style["name"]):
                self.assertEqual(style["status"], "implemented_sample_verified")
                code = bytes.fromhex(style["style_code_hex"])
                self.assertEqual(len(code), 4)
                self.assertNotIn(code, codes)
                codes.add(code)

                recipe = self.recipe_from_native_sample(style)
                template_path = (GEN_DIR / style["template"]).resolve()
                self.assertTrue(template_path.is_file(), str(template_path))
                template_fmf = self.gen.parse_fmf(template_path.read_bytes())
                template_tac = self.gen.parse_tac(template_fmf.data_by_ext[".tac"])
                summary = self.gen.apply_recipe(
                    template_tac, recipe, self.catalog, self.registry
                )
                self.assertEqual(summary["style"], style["name"])
                self.assertEqual(summary["style_code_hex"], style["style_code_hex"])

                output = self.gen.write_fmf(
                    template_fmf, self.gen.write_tac(template_tac), summary["name"]
                )
                output_fmf = self.gen.parse_fmf(output)
                output_tac = self.gen.parse_tac(output_fmf.data_by_ext[".tac"])
                readback = self.gen.verify_recipe_roundtrip(
                    output_tac, recipe, self.catalog
                )
                self.assertEqual(output_tac.style, style["tac_style_string"])
                self.assertEqual(bytes(output_tac.quad).hex(), style["style_code_hex"])
                self.assertEqual(len(readback["verified_slots"]), 22)
                self.assertEqual(len(output_tac.pairs), 11)
                self.assertEqual(bytes(output_tac.packed), bytes(template_tac.packed))
                results.append(style["name"])

        self.assertEqual(len(results), 10)
        self.assertEqual(len(codes), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
