import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT
GEN_DIR = RULES / "04_离线原生FMF生成器"
GEN_PATH = GEN_DIR / "FM27GEN1_Offline_FMF_Generator.py"
spec = importlib.util.spec_from_file_location("fm27gen1_native_style_samples", GEN_PATH)
gen = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gen
spec.loader.exec_module(gen)


class NativeStyleSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((GEN_DIR / "style_template_registry.json").read_text(encoding="utf-8"))

    def test_all_ten_styles_have_unique_native_codes_and_templates(self):
        styles = self.registry["styles"]
        self.assertEqual(len(styles), 10)
        self.assertEqual(len({x["name"] for x in styles}), 10)
        self.assertEqual(len({x["style_code_hex"] for x in styles}), 10)
        for item in styles:
            with self.subTest(style=item["name"]):
                self.assertEqual(item["status"], "implemented_sample_verified")
                resolved = gen.resolve_style_definition(item["name"], self.registry)
                self.assertEqual(resolved["style_code"].hex(), item["style_code_hex"])
                template = (GEN_DIR / item["template"]).resolve()
                self.assertEqual(gen.resolve_template_path(item["name"], self.registry), template)
                self.assertTrue(template.is_file(), str(template))
                fmf = gen.parse_fmf(template.read_bytes())
                self.assertTrue({".tac", ".aom", ".img"}.issubset(fmf.data_by_ext))
                tac = gen.parse_tac(fmf.data_by_ext[".tac"])
                self.assertEqual(tac.magic[11], 27)
                self.assertEqual(bytes(tac.quad).hex(), item["style_code_hex"])
                self.assertEqual(tac.style, item["tac_style_string"])



    def test_explicit_cross_style_template_is_rejected(self):
        gegenpress = gen.resolve_template_path("Gegenpress", self.registry)
        with self.assertRaisesRegex(ValueError, "拒绝跨风格模板"):
            gen.resolve_template_path("Tiki-Taka", self.registry, gegenpress)

    def test_generate_and_roundtrip_a_recipe_for_each_of_the_ten_styles(self):
        profiles = json.loads((GEN_DIR / "official_style_team_instruction_profiles.json").read_text(encoding="utf-8"))
        profile_by_name = {x["name"]: x for x in profiles["styles"]}
        mentality_ids = {"Defensive": 2, "Cautious": 3, "Balanced": 4, "Positive": 5}
        positions = {int(x["mask"]): x["id"] for x in self.catalog["positions"]}
        role_by_flag_phase = {
            (int(x["flags"]), int(x["phase"])): x["id"] for x in self.catalog["roles"]
        }

        for style in self.registry["styles"]:
            with self.subTest(style=style["name"]):
                profile = profile_by_name[style["name"]]
                template_path = (GEN_DIR / style["template"]).resolve()
                fmf = gen.parse_fmf(template_path.read_bytes())
                tac = gen.parse_tac(fmf.data_by_ext[".tac"])
                player_slots = []
                for pair in sorted(tac.pairs, key=lambda x: x.slot):
                    slot = {}
                    for phase, key, block in ((0, "in", pair.ip), (1, "out", pair.oop)):
                        role_id = role_by_flag_phase[(block.mask & gen.ROLE_MASK, phase)]
                        display_role = role_id[2:] if phase == 1 and role_id.startswith("OP") else role_id
                        slot[key] = {
                            "pos": positions[block.selector],
                            "role": display_role,
                            "pi": [],
                        }
                    player_slots.append(slot)

                recipe = {
                    "v": 1,
                    "name": f"CI Native Roundtrip - {style['name']}",
                    "ment": mentality_ids[profile["mentality"]],
                    "base": {"g": style["name"], "ip": "native", "oop": "native"},
                    "ti": profile["ti"],
                    "p": player_slots,
                }
                summary = gen.apply_recipe(tac, recipe, self.catalog, self.registry)
                self.assertEqual(summary["style_code_hex"], style["style_code_hex"])
                output = gen.write_fmf(fmf, gen.write_tac(tac), summary["name"])
                verify_fmf = gen.parse_fmf(output)
                verify_tac = gen.parse_tac(verify_fmf.data_by_ext[".tac"])
                self.assertEqual(verify_tac.style, style["tac_style_string"])
                self.assertEqual(bytes(verify_tac.quad).hex(), style["style_code_hex"])
                self.assertEqual(verify_fmf.root_title, summary["name"])
                self.assertEqual(bytes(verify_tac.packed), bytes(tac.packed))
                readback = gen.verify_recipe_roundtrip(verify_tac, recipe, self.catalog)
                self.assertEqual(len(readback["verified_slots"]), 22)

    def test_template_owned_opaque_native_ti_bits_are_preserved(self):
        base = bytearray(12)
        for bit in gen.PRESERVED_OPAQUE_TI_BITS:
            base[bit // 8] |= 1 << (bit % 8)
        encoded = gen.encode_ti({"ti": {}}, self.catalog, base)
        for bit in gen.PRESERVED_OPAQUE_TI_BITS:
            self.assertTrue(encoded[bit // 8] & (1 << (bit % 8)), bit)

    def test_all_official_style_profile_ti_values_are_encodable(self):
        profiles = json.loads((GEN_DIR / "official_style_team_instruction_profiles.json").read_text(encoding="utf-8"))
        self.assertEqual(len(profiles["styles"]), 10)
        for style in profiles["styles"]:
            with self.subTest(style=style["name"]):
                for key, value in style["ti"].items():
                    self.assertIn(key, gen.TI_GROUPS)
                    self.assertIn((key, value), gen.TI_MAP)
                gen.encode_ti({"ti": style["ti"]}, self.catalog, bytearray(12))


if __name__ == "__main__":
    unittest.main()
