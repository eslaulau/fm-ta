from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectAiInstructionTests(unittest.TestCase):
    def test_root_agent_guide_defines_build_contract_and_rnd_scope(self):
        guide = ROOT / "AGENTS.md"
        self.assertTrue(guide.is_file(), "Root AGENTS.md is the mandatory AI execution guide")
        text = guide.read_text(encoding="utf-8")
        for phrase in (
            "The user must not be asked to:",
            "build_requests/",
            "GitHub Actions builds the native FMF",
            "22 phase objects",
            "same-run",
            "D3 is not the final acceptance of the continuing EngineDividend R&D line",
            "D4",
            "D5",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_continuing_engine_dividend_project_has_d0_to_d5_lifecycle(self):
        paths = (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "00_资料总索引与检索规范.md",
            ROOT / "tactic_development" / "FM27_EngineDividend_4Back" / "README.md",
            ROOT / "tactic_development" / "FM27_EngineDividend_4Back" / "ANALYSIS_AND_ITERATION_RULES.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("D4", text)
                self.assertIn("D5", text)
        rules = (ROOT / "tactic_development" / "FM27_EngineDividend_4Back" / "ANALYSIS_AND_ITERATION_RULES.md").read_text(encoding="utf-8")
        self.assertIn("正常赛季复盘与下一轮迭代", rules)
        self.assertIn("赛季报告", rules)
        self.assertIn("D3 是单次原生 FMF 构建的技术交付门槛", rules)

    def test_generator_d3_is_separate_from_game_import_and_performance(self):
        request_readme = (ROOT / "build_requests" / "README.md").read_text(encoding="utf-8")
        generator_readme = (ROOT / "04_离线原生FMF生成器" / "README.md").read_text(encoding="utf-8")
        self.assertIn("D3 是生成器的技术输出门槛", request_readme)
        self.assertIn("D4/D5 继续验证", request_readme)
        self.assertIn("D3 是本生成器的技术交付验收", generator_readme)
        self.assertIn("不表示游戏内导入或比赛表现已验证", generator_readme)

    def test_one_off_tactic_does_not_force_unsolicited_squad_analysis_but_ongoing_project_does_review_reports(self):
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("For a one-off tactic, do not require squad analysis", guide)
        self.assertIn("unless requested", guide)
        self.assertIn("when its report is available, analyze it and continue the iteration", guide)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("单次新战术默认", readme)
        self.assertIn("用户确认的父版本、赛季报告、版本映射", readme)

    def test_pi_arrays_may_be_empty_but_selected_options_remain_permission_checked(self):
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("the array may be empty", guide)
        self.assertIn("every PI that is actually selected", guide)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("空数组合法", readme)
        self.assertIn("不存在 22/22 非空 PI 门槛", readme)
        preflight = (ROOT / "scripts" / "preflight_fm27_tactic.py").read_text(encoding="utf-8")
        self.assertIn("encode_pi_details", preflight)
        self.assertIn("empty_pi_phases_allowed", preflight)

    def test_copilot_and_readmes_point_to_the_same_mandatory_guide(self):
        copilot = (ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        index = (ROOT / "00_资料总索引与检索规范.md").read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", copilot)
        self.assertIn("AGENTS.md", readme)
        self.assertIn("AGENTS.md", index)

    def test_official_delivery_is_repository_managed_not_manual_desktop_steps(self):
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("GitHub Actions builds the native FMF", guide)
        self.assertIn("build_requests/", guide)
        requests = (ROOT / "build_requests" / "README.md").read_text(encoding="utf-8")
        self.assertIn("正式对话交付", requests)
        self.assertIn("用户不需要", requests)

    def test_legacy_snapshot_workflow_does_not_automatically_build_structured_v09_recipe(self):
        workflow = (ROOT / ".github" / "workflows" / "fm27-native-snapshot-build.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertIn("legacy", workflow.lower())
        self.assertIn("request_file", workflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
