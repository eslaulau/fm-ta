from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectAiInstructionTests(unittest.TestCase):
    def test_mandatory_root_agent_guide_exists_and_defines_delivery_contract(self):
        guide = ROOT / "AGENTS.md"
        self.assertTrue(guide.is_file(), "Root AGENTS.md is the mandatory AI execution guide")
        text = guide.read_text(encoding="utf-8")
        for phrase in (
            "The user must not be asked to:",
            "build_requests/",
            "Do not use any tactic, preset, recipe, FMF, old report",
            "22/22 phases",
            "Download the artifact",
            "D3 is the final acceptance point",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_no_later_game_or_match_acceptance_stages_in_core_guides(self):
        phase_labels = {"D" + str(number) for number in (4, 5)}
        paths = (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "00_资料总索引与检索规范.md",
            ROOT / "build_requests" / "README.md",
            ROOT / "04_离线原生FMF生成器" / "README.md",
            ROOT / "04_离线原生FMF生成器" / "FM27GEN1_离线原生FMF_生成流程.md",
            ROOT / "04_离线原生FMF生成器" / "FM27GEN1_离线原生FMF_字段契约.md",
            ROOT / "03_GEN1编码与导入规则" / "README.md",
            ROOT / "03_GEN1编码与导入规则" / "GEN1_导入验收清单.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for label in phase_labels:
                with self.subTest(path=path.name, label=label):
                    self.assertNotIn(label, text)
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("D3 is the final acceptance point", guide)
        self.assertIn("does not include game-client import", guide)
        self.assertIn("match-performance testing", guide)

    def test_copilot_and_readmes_point_to_the_same_mandatory_guide(self):
        copilot = (ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        index = (ROOT / "00_资料总索引与检索规范.md").read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", copilot)
        self.assertIn("AGENTS.md", readme)
        self.assertIn("AGENTS.md", index)

    def test_new_tactic_does_not_require_unsolicited_squad_or_match_analysis(self):
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Do not require squad analysis", guide)
        self.assertIn("unless the user explicitly asks", guide)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("不是新战术设计的前置条件", readme)

    def test_official_delivery_is_repository_push_not_manual_desktop_steps(self):
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("GitHub Actions builds", guide)
        self.assertIn("build_requests/", guide)
        requests = (ROOT / "build_requests" / "README.md").read_text(encoding="utf-8")
        self.assertIn("正式对话交付", requests)
        self.assertIn("无需用户操作 GitHub 页面或本地电脑", requests)


if __name__ == "__main__":
    unittest.main(verbosity=2)
