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
        self.runner_temp = self.root / "runner_temp"
        self.recipe = {"v": 1, "name": "原创战术 A", "ment": 5, "base": {"g": "Gegenpress"}, "ti": {}, "p": []}

    def test_workflow_dispatch_inline_json_creates_temp_json_not_repo_file(self):
        result = resolver.resolve_recipe_input(
            event_name="workflow_dispatch",
            event_data={},
            recipe_json_input=json.dumps(self.recipe, ensure_ascii=False),
            repo_root=self.root,
            runner_temp=self.runner_temp,
            run_number="12",
        )
        path = Path(result["recipe_path"])
        self.assertTrue(path.is_file())
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), self.recipe)
        self.assertEqual(path.parent, self.runner_temp)
        self.assertEqual(result["output_stem"], "A_run12")

    def test_repository_dispatch_accepts_recipe_object(self):
        result = resolver.resolve_recipe_input(
            event_name="repository_dispatch",
            event_data={"client_payload": {"recipe": self.recipe}},
            repo_root=self.root,
            runner_temp=self.runner_temp,
            run_number="13",
        )
        self.assertTrue(Path(result["recipe_path"]).is_file())
        self.assertEqual(json.loads(Path(result["recipe_path"]).read_text(encoding="utf-8")), self.recipe)
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
        # The CLI obtains changed_files through git diff-tree --diff-filter=AM,
        # so a deletion-only push reaches this resolver as an empty list.
        skipped = resolver.resolve_recipe_input(
            event_name="push",
            event_data={},
            changed_files=[],
            **common
        )
        self.assertTrue(skipped["skip_build"])
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolver.resolve_recipe_input(
                event_name="push",
                event_data={},
                changed_files=["build_requests/one.json", "build_requests/two.txt"],
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
