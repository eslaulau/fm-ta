import importlib.util
import unittest
from pathlib import Path

GENERATOR = (
    Path(__file__).resolve().parents[1]
    / "04_离线原生FMF生成器"
    / "FM27GEN1_Offline_FMF_Generator.py"
)
spec = importlib.util.spec_from_file_location("fm27gen1_generator", GENERATOR)
gen = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = gen
spec.loader.exec_module(gen)


def build_roundtrip_fixture():
    positions = [f"P{i}" for i in range(11)]
    role_defs = [
        {"id": "CentreBack", "phase": 0, "flags": 1 << 8},
        {"id": "OPCentreBack", "phase": 1, "flags": 1 << 9},
    ]
    catalog = {
        "positions": [{"id": name, "mask": i + 1} for i, name in enumerate(positions)],
        "roles": role_defs,
        "role_eligibility": {
            name: {0: ["CentreBack"], 1: ["OPCentreBack"]} for name in positions
        },
        "pi_policies": {},
    }
    recipe_players = []
    pairs = []
    for slot, position in enumerate(positions):
        recipe_players.append({
            "in": {"pos": position, "role": "CentreBack", "pi": [["SHOOTING", "SHOOT_MORE_OFTEN"]]},
            "out": {"pos": position, "role": "CentreBack", "pi": [["SHOOTING", "SHOOT_MORE_OFTEN"]]},
        })
        ip_key = f"0:{position}:CentreBack:{gen.ROLE_DUTY['CentreBack']}"
        oop_key = f"1:{position}:OPCentreBack:{gen.ROLE_DUTY['OPCentreBack']}"
        catalog["pi_policies"][ip_key] = {"fixture": "0" * 64}
        catalog["pi_policies"][oop_key] = {"fixture": "0" * 64}
        ip = gen.Block(
            selector=slot + 1,
            flag=0,
            items=[{"key": 1 << 8, "mask2": 1 << 18, "value": 0}],
            mask=(1 << 8) | gen.ROLE_DUTY["CentreBack"],
        )
        oop = gen.Block(
            selector=slot + 1,
            flag=0,
            items=[{"key": 1 << 9, "mask2": 1 << 18, "value": 0}],
            mask=(1 << 9) | gen.ROLE_DUTY["OPCentreBack"],
        )
        pairs.append(gen.Pair(slot=slot, ip=ip, oop=oop))
    tac = gen.Tac(
        magic=b"", title="fixture", hdr=bytearray(6), packed=bytearray(12),
        style="", quad=bytearray(4), pairs=pairs, ids=[], lists=[],
        records=[], end=0,
    )
    return tac, {"p": recipe_players}, catalog


class NativeReadbackTests(unittest.TestCase):
    def test_exact_role_duty_roundtrip_passes(self):
        tac, recipe, catalog = build_roundtrip_fixture()
        result = gen.verify_recipe_roundtrip(tac, recipe, catalog)
        self.assertEqual(result["ip_unique_positions"], 11)
        self.assertEqual(result["oop_unique_positions"], 11)

    def test_wrong_but_known_duty_is_rejected(self):
        tac, recipe, catalog = build_roundtrip_fixture()
        tac.pairs[0].ip.mask = (1 << 8) | 4194304
        with self.assertRaisesRegex(ValueError, "职责回读不一致"):
            gen.verify_recipe_roundtrip(tac, recipe, catalog)

    def test_missing_active_role_pi_cache_is_rejected(self):
        tac, recipe, catalog = build_roundtrip_fixture()
        tac.pairs[0].ip.items.clear()
        with self.assertRaisesRegex(ValueError, "活跃角色 PI cache 数量错误"):
            gen.verify_recipe_roundtrip(tac, recipe, catalog)

    def test_duplicate_active_role_pi_cache_is_rejected(self):
        tac, recipe, catalog = build_roundtrip_fixture()
        tac.pairs[0].ip.items.append(dict(tac.pairs[0].ip.items[0]))
        with self.assertRaisesRegex(ValueError, "活跃角色 PI cache 数量错误"):
            gen.verify_recipe_roundtrip(tac, recipe, catalog)

    def test_recipe_writer_rejects_duplicate_active_role_cache(self):
        block = gen.Block(
            selector=1, flag=0,
            items=[{"key": 1 << 8, "mask2": 0, "value": 0},
                   {"key": 1 << 8, "mask2": 0, "value": 0}],
            mask=(1 << 8) | gen.ROLE_DUTY["CentreBack"],
        )
        with self.assertRaisesRegex(ValueError, "重复 PI cache 项"):
            gen.update_role_entry(block, 1 << 8, 1 << 18)


if __name__ == "__main__":
    unittest.main()
