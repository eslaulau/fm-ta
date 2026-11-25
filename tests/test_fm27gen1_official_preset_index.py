import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = (
    ROOT
    / "04_离线原生FMF生成器"
)
AUDIT = GEN_DIR / "FM27GEN1_Netlify90_OfficialPreset_Audit.py"
spec = importlib.util.spec_from_file_location("fm27_netlify90_audit", AUDIT)
audit = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)

GENERATOR_PATH = GEN_DIR / "FM27GEN1_Offline_FMF_Generator.py"
gen_spec = importlib.util.spec_from_file_location("fm27gen1_generator", GENERATOR_PATH)
gen = importlib.util.module_from_spec(gen_spec)
sys.modules[gen_spec.name] = gen
gen_spec.loader.exec_module(gen)


class OfficialPresetIndexTests(unittest.TestCase):
    def test_all_90_rows_match_native_role_position_and_policy_catalog(self):
        report = audit.audit_official_index()
        self.assertEqual(report["status"], "website_index_role_position_duty_and_pi_policy_audit_passed")
        self.assertEqual(report["preset_count"], 90)
        self.assertEqual(report["style_count"], 10)
        self.assertEqual(report["phase_slot_count"], 1980)
        self.assertEqual(report["errors"], [])
        self.assertEqual(set(report["style_counts"].values()), {9})

    def test_website_position_aliases_normalize_for_both_phases(self):
        for phase in (0, 1):
            self.assertEqual(gen.native_position_id("DM", phase), "DMC")
            self.assertEqual(gen.native_position_id("STC", phase), "ST")
            self.assertEqual(gen.native_position_id("STCR", phase), "STR")
            self.assertEqual(gen.native_position_id("STCL", phase), "STL")

    def test_website_role_display_aliases_resolve_to_catalog_ids(self):
        role_ids = {
            "OPWideCoverCentralMidfielder",
            "OPWideCoverDefensiveMidfielder",
            "OPLineKeeper",
        }
        self.assertEqual(
            gen.role_id_from_display("Wide Covering Central Midfielder", 1, role_ids),
            "OPWideCoverCentralMidfielder",
        )
        self.assertEqual(
            gen.role_id_from_display("Wide Covering Defensive Midfielder", 1, role_ids),
            "OPWideCoverDefensiveMidfielder",
        )
        self.assertEqual(
            gen.role_id_from_display("Line-Holding Keeper", 1, role_ids),
            "OPLineKeeper",
        )

    def test_empty_pi_list_tolerates_unrelated_policy_version_differences(self):
        duty = gen.ROLE_DUTY["FreeRole"]
        policy_key = f"0:AMC:FreeRole:{duty}"
        catalog = {
            "pi_policies": {
                policy_key: {
                    "v1": "0" * 30,
                    "v2": "0" * 25 + "1" + "0" * 4,
                }
            }
        }
        self.assertEqual(gen.encode_pi([], catalog, 0, "AMC", "FreeRole", duty), 0)

    def test_pi_option_conflict_between_catalog_versions_is_rejected(self):
        duty = gen.ROLE_DUTY["FreeRole"]
        policy_key = f"0:AMC:FreeRole:{duty}"
        catalog = {
            "pi_policies": {
                policy_key: {
                    "v1": "0" * 30,
                    "v2": "0" * 25 + "1" + "0" * 4,
                }
            }
        }
        pis = [["SHOOTING", "SHOOT_MORE_OFTEN"]]
        # Native option 18 is consistent/editable in both catalog revisions.
        self.assertEqual(gen.encode_pi(pis, catalog, 0, "AMC", "FreeRole", duty), 1 << 18)

        conflict = [["ATTACKING_WIDTH", "STAY_WIDER"]]
        with self.assertRaisesRegex(ValueError, "权限冲突"):
            gen.encode_pi(conflict, catalog, 0, "AMC", "FreeRole", duty)

    def test_empty_pi_list_does_not_require_a_policy_row_but_selected_pi_does(self):
        duty = gen.ROLE_DUTY["CentreBack"]
        empty_catalog = {"pi_policies": {}}
        self.assertEqual(gen.encode_pi([], empty_catalog, 0, "DC", "CentreBack", duty), 0)
        selected = [["SHOOTING", "SHOOT_MORE_OFTEN"]]
        with self.assertRaisesRegex(ValueError, "缺少原生 PI 权限策略"):
            gen.encode_pi(selected, empty_catalog, 0, "DC", "CentreBack", duty)

    def test_all_mapped_ti_options_match_exactly_one_native_catalog_option(self):
        catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        groups = {int(group["id"]): group for group in catalog["team_instructions"]}
        for (key, value), bit in gen.TI_MAP.items():
            self.assertIn(key, gen.TI_GROUPS, (key, value))
            if bit == 0:  # Default/no explicit native bit is intentionally not serialized.
                continue
            matches = [
                option
                for group_id in gen.TI_GROUPS[key]
                for option in groups[group_id]["options"]
                if int(option.get("native_bit") or 0) == bit
            ]
            self.assertEqual(
                len(matches), 1,
                f"{key}={value} -> native bit {bit} does not map to exactly one option",
            )

    def test_all_ten_official_style_profiles_encode_without_unknown_ti_options(self):
        catalog = json.loads((GEN_DIR / "catalog.json").read_text(encoding="utf-8"))
        profiles = json.loads(
            (GEN_DIR / "official_style_team_instruction_profiles.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(profiles["styles"]), 10)
        self.assertEqual(len({item["name"] for item in profiles["styles"]}), 10)
        for style in profiles["styles"]:
            for key, value in style["ti"].items():
                self.assertIn((key, value), gen.TI_MAP, f"{style['name']}: {key}={value}")
            encoded = gen.encode_ti({"ti": style["ti"]}, catalog, bytearray(12))
            for key, value in style["ti"].items():
                bit = gen.TI_MAP[(key, value)]
                if bit:
                    self.assertTrue(
                        encoded[bit // 8] & (1 << (bit % 8)),
                        f"{style['name']}: {key}={value} bit {bit} not set",
                    )



if __name__ == "__main__":
    unittest.main()
