from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "04_离线原生FMF生成器"
GENERATOR = GEN_DIR / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG = GEN_DIR / "catalog.json"
LEGACY_FIXTURE = ROOT / "build_requests" / "Unmapped_Mapping_Import_Test_v1.txt"

sys.path.insert(0, str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen  # noqa: E402


class DirectJSONInputTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not LEGACY_FIXTURE.is_file():
            raise RuntimeError(f"Missing established FM27 input fixture: {LEGACY_FIXTURE}")
        cls.recipe = gen.parse_gen1(LEGACY_FIXTURE)

    def test_native_json_is_loaded_without_gen1_transport(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "direct_recipe.json"
            path.write_text(
                json.dumps(self.recipe, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            loaded, input_format = gen.load_recipe_input(path)

            self.assertEqual(input_format, "json")
            self.assertEqual(loaded, self.recipe)
            self.assertTrue(path.read_text(encoding="utf-8").lstrip().startswith("{"))
            self.assertFalse(path.read_text(encoding="utf-8").lstrip().startswith("FM27GEN1:"))

    def test_python_dict_api_builds_without_any_recipe_transport_file(self):
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        registry_path = GEN_DIR / "style_template_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))

        # Pass the already parsed Python object directly: no JSON recipe file,
        # no Base64 wrapper, and no CLI parser are involved in this path.
        fmf_bytes, report = gen.build_fmf_from_recipe(
            self.recipe,
            catalog,
            style_registry=registry,
        )

        self.assertIsInstance(fmf_bytes, bytes)
        self.assertGreater(len(fmf_bytes), 0)
        self.assertEqual(report.get("recipe_input_format"), "python_dict")
        self.assertEqual(
            report.get("status"),
            "offline_binary_roundtrip_verified_not_game_import_verified",
        )
        self.assertEqual(report.get("bytes"), len(fmf_bytes))
        self.assertEqual(report.get("sha256"), hashlib.sha256(fmf_bytes).hexdigest())

        parsed = gen.parse_fmf(fmf_bytes)
        tac = gen.parse_tac(parsed.data_by_ext[".tac"])
        self.assertEqual(tac.title, report.get("name"))
        self.assertEqual(len(tac.pairs), 11)
        self.assertEqual(len(report.get("player_phase_map", [])), 22)
        self.assertEqual(len(report.get("readback_player_phase_map", [])), 22)
        for check in (
            "fmf_outer_roundtrip",
            "all_member_decrypt_and_zstd_checksums",
            "tac_full_parse",
            "11_ip_oop_pairs",
            "22_positions_roles_pi_readback_exact",
            "pi_permissions_checked_against_catalog",
            "team_instruction_vector_readback",
            "native_style_string_and_code_readback",
        ):
            self.assertIs(report.get("checks", {}).get(check), True, check)

    def test_direct_api_rejects_unknown_and_incomplete_recipe_fields(self):
        with self.subTest(case="unknown root field"):
            malformed = dict(self.recipe)
            malformed["unmapped_override"] = True
            with self.assertRaisesRegex(ValueError, "未知根字段"):
                gen.validate_recipe_structure(malformed)

        with self.subTest(case="missing phase PI array"):
            malformed = json.loads(json.dumps(self.recipe))
            del malformed["p"][0]["in"]["pi"]
            with self.assertRaisesRegex(ValueError, "缺少必需字段"):
                gen.validate_recipe_structure(malformed)

        with self.subTest(case="boolean is not a valid mentality integer"):
            malformed = dict(self.recipe)
            malformed["ment"] = True
            with self.assertRaisesRegex(ValueError, "ment 必须是 1–7 的整数"):
                gen.validate_recipe_structure(malformed)
    def test_schema_accepts_ip_oop_base_metadata_without_using_it_as_phase_data(self):
        recipe = json.loads(json.dumps(self.recipe))
        recipe["base"]["ip"] = "native"
        recipe["base"]["oop"] = "native"
        self.assertIsNone(gen.validate_recipe_structure(recipe))
    def test_cli_generates_and_reads_back_native_fmf_from_direct_json(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_dir = Path(temp)
            recipe_path = temp_dir / "direct_recipe.json"
            output_path = temp_dir / "direct_recipe.fmf"
            report_path = temp_dir / "direct_recipe.report.json"
            recipe_path.write_text(
                json.dumps(self.recipe, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    str(recipe_path),
                    "--catalog",
                    str(CATALOG),
                    "--output",
                    str(output_path),
                    "--report",
                    str(report_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"Direct JSON generation failed.\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}",
            )
            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report.get("recipe_input_format"), "json")
            self.assertEqual(
                report.get("status"),
                "offline_binary_roundtrip_verified_not_game_import_verified",
            )
            required = [
                "fmf_outer_roundtrip",
                "all_member_decrypt_and_zstd_checksums",
                "tac_full_parse",
                "11_ip_oop_pairs",
                "22_positions_roles_pi_readback_exact",
                "pi_permissions_checked_against_catalog",
                "team_instruction_vector_readback",
                "native_style_string_and_code_readback",
            ]
            for key in required:
                self.assertIs(report.get("checks", {}).get(key), True, key)
            self.assertEqual(len(report.get("player_phase_map", [])), 22)
            self.assertEqual(len(report.get("readback_player_phase_map", [])), 22)


if __name__ == "__main__":
    unittest.main(verbosity=2)
