from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "Invoke-FM27TacticBuild.ps1"


class PowerShellDispatchHelperContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = HELPER.read_text(encoding="utf-8")

    def test_uses_clipboard_and_dispatches_recipe_as_workflow_input(self):
        self.assertIn("Get-Clipboard -Raw", self.source)
        self.assertIn("actions/workflows/$WorkflowFile/dispatches", self.source)
        self.assertIn("recipe_json = $RecipeJson", self.source)
        self.assertIn("$RecipeJson", self.source)
        self.assertNotIn("build_requests/", self.source)

    def test_token_is_encrypted_for_current_windows_user(self):
        self.assertIn("ConvertFrom-SecureString -SecureString $secureToken", self.source)
        self.assertIn("ConvertTo-SecureString -String $encrypted", self.source)
        self.assertIn("github-token.dpapi", self.source)

    def test_downloaded_fmf_is_verified_against_report(self):
        self.assertIn("actions/runs/$runId/artifacts", self.source)
        self.assertIn("Get-FileHash", self.source)
        self.assertIn("$report.sha256", self.source)
        self.assertIn("$report.bytes", self.source)
        self.assertIn("readback_player_phase_map", self.source)
        self.assertIn("native_style_string_and_code_readback", self.source)

    def test_cloud_artifact_is_removed_by_default_after_local_verification(self):
        self.assertIn("[switch]$KeepCloudArtifact", self.source)
        self.assertIn("if (-not $KeepCloudArtifact)", self.source)
        self.assertIn("actions/artifacts/$($artifact[0].id)", self.source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
