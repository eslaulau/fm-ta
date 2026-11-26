from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
RESOLVER_PATH = ROOT / "scripts" / "resolve_fm27_tactic_recipe.py"
spec = importlib.util.spec_from_file_location("fm27_tactic_recipe_resolver", RESOLVER_PATH)
resolver = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = resolver
spec.loader.exec_module(resolver)


class TacticRecipeInputResolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "build_requests").mkdir()
        (self.root / "tactic_development" / "FM27_EngineDividend_4Back").mkdir(parents=True)
        self.runner_temp = self.root / "runner_temp"
        self.recipe = {"v": 1, "name": "原创战术 A", "ment": 5, "base": {"g": "Gegenpress"}, "ti": {}, "p": []}

    def test_safe_stem_preserves_unicode_but_blocks_path_separators(self):
        self.assertEqual(resolver.safe_stem("战术 A"), "战术_A")
        self.assertEqual(resolver.safe_stem("../../unsafe/name"), "unsafe_name")

    def test_workflow_dispatch_inline_json_stays_in_memory_without_creating_temp_file(self):
        result = resolver.resolve_recipe_input(
            event_name="workflow_dispatch",
            event_data={},
            recipe_json_input=json.dumps(self.recipe, ensure_ascii=False),
            repo_root=self.root,
            runner_temp=self.runner_temp,
            run_number="12",
        )
        self.assertNotIn("recipe_path", result)
        self.assertEqual(json.loads(result["recipe_json"]), self.recipe)
        self.assertFalse(self.runner_temp.exists())
        self.assertEqual(result["output_stem"], "原创战术_A_run12")

    def test_repository_dispatch_accepts_recipe_object(self):
        result = resolver.resolve_recipe_input(
            event_name="repository_dispatch",
            event_data={"client_payload": {"recipe": self.recipe}},
            repo_root=self.root,
            runner_temp=self.runner_temp,
            run_number="13",
        )
        self.assertNotIn("recipe_path", result)
        self.assertEqual(json.loads(result["recipe_json"]), self.recipe)
        self.assertFalse(self.runner_temp.exists())
        self.assertIn("repository_dispatch", result["recipe_label"])

    def test_dispatch_requires_exactly_one_input_and_object_payload(self):
        common = {"repo_root": self.root, "runner_temp": self.runner_temp}
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolver.resolve_recipe_input(
                event_name="workflow_dispatch",
                event_data={},
                recipe_path_input="build_requests/a.json",
                recipe_json_input=json.dumps(self.recipe),
                **common
            )
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolver.resolve_recipe_input(
                event_name="workflow_dispatch", event_data={}, **common
            )
        with self.assertRaisesRegex(ValueError, "JSON object"):
            resolver.resolve_recipe_input(
                event_name="repository_dispatch",
                event_data={"client_payload": {"recipe": [1, 2, 3]}},
                **common
            )

    def test_workflow_dispatch_rejects_invalid_json_and_path_traversal(self):
        common = {"repo_root": self.root, "runner_temp": self.runner_temp}
        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            resolver.resolve_recipe_input(
                event_name="workflow_dispatch",
                event_data={},
                recipe_json_input="{not-json",
                **common
            )
        secret = self.root / "secret.json"
        secret.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "directly inside build_requests"):
            resolver.resolve_recipe_input(
                event_name="workflow_dispatch",
                event_data={},
                recipe_path_input="build_requests/../secret.json",
                **common
            )

    def test_push_mode_resolves_one_file_and_skips_deletion_only_push(self):
        target = self.root / "build_requests" / "one.json"
        target.write_text(json.dumps(self.recipe), encoding="utf-8")
        common = {"repo_root": self.root, "runner_temp": self.runner_temp}
        selected = resolver.resolve_recipe_input(
            event_name="push",
            event_data={},
            changed_files=["build_requests/one.json"],
            **common
        )
        self.assertEqual(selected["recipe_path"], "build_requests/one.json")
        canonical = self.root / "tactic_development" / "FM27_EngineDividend_4Back" / "V1.6_BUILD_REQUEST.json"
        canonical.write_text(json.dumps(self.recipe), encoding="utf-8")
        selected_canonical = resolver.resolve_recipe_input(
            event_name="push",
            event_data={},
            changed_files=["tactic_development/FM27_EngineDividend_4Back/V1.6_BUILD_REQUEST.json"],
            **common
        )
        self.assertEqual(
            selected_canonical["recipe_path"],
            "tactic_development/FM27_EngineDividend_4Back/V1.6_BUILD_REQUEST.json",
        )
        # The CLI obtains changed_files through git diff-tree --diff-filter=AM,
        # so a deletion-only push reaches this resolver as an empty list.
        skipped = resolver.resolve_recipe_input(
            event_name="push",
            event_data={},
            changed_files=[],
            **common
        )
        self.assertTrue(skipped["skip_build"])
        self.assertNotIn("recipe_path", skipped)
        self.assertIn("no added/modified", skipped["recipe_label"])
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolver.resolve_recipe_input(
                event_name="push",
                event_data={},
                changed_files=["build_requests/one.json", "tactic_development/FM27_EngineDividend_4Back/V1.6_BUILD_REQUEST.json"],
                **common
            )

    def test_workflow_dispatch_accepts_existing_legacy_recipe_path(self):
        legacy = self.root / "build_requests" / "legacy.txt"
        legacy.write_text("FM27GEN1:e30=", encoding="utf-8")
        result = resolver.resolve_recipe_input(
            event_name="workflow_dispatch",
            event_data={},
            recipe_path_input="build_requests/legacy.txt",
            repo_root=self.root,
            runner_temp=self.runner_temp,
        )
        self.assertEqual(result["recipe_path"], "build_requests/legacy.txt")


if __name__ == "__main__":
    unittest.main(verbosity=2)
