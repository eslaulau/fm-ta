# FM27 引擎红利四后卫｜版本与产物总目录

## 当前版本：N1

- 战术：N1｜窄幅纵向分层 4-1-2-3。
- 状态：D1原生权限预检、D2结构核验、D3 FMF生成与独立回读通过；D4游戏内导入、D5完整赛季效果待验证。
- 配方：[N1.json](N1.json)
- 设计记录：[N1_DESIGN_AND_AUDIT.md](N1_DESIGN_AND_AUDIT.md)
- FMF：[builds/N1.fmf](builds/N1.fmf)
- 同次回读报告：[builds/N1.report.json](builds/N1.report.json)
- 构建运行：[GitHub Actions 45952680145](https://github.com/eslaulau/fm-ta/actions/runs/45952680145)
- N1不是已验证赛季成功战术；最终目标仍为完整38场至少109分且全队xG至少100。

## 现行规则入口

现行规则只以以下文件为准，不再维护平行的总规则、整改计划或重复模板：
1. [PROJECT_RULES.md](PROJECT_RULES.md)
2. [TACTIC_FIXED_CONSTRAINTS.md](TACTIC_FIXED_CONSTRAINTS.md)
3. [UPGRADE_GATE.md](UPGRADE_GATE.md)
4. [GENERATION_EXECUTION_POLICY.md](GENERATION_EXECUTION_POLICY.md)
5. [AGENTS.md](AGENTS.md)

## 历史证据入口

- [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)：完整历史战术配置、逐代差异、赛季结果、证据状态和四类配置决策。
- [ITERATION_LOG.md](ITERATION_LOG.md)：历史研发事件、构建与复盘过程。
- [V0.5_BASELINE.md](V0.5_BASELINE.md) 与 [V0.5_NATIVE_SNAPSHOT.json](V0.5_NATIVE_SNAPSHOT.json)：历史原生快照和格式载体说明。
- 各版本recipe、设计审计、D5赛季报告、FMF及build report均保留原文件，不因规则文档清理而删除。

## 历史版本文件索引

| 版本系列 | 文件范围 | 当前定位 |
|---|---|---|
| V0.5–V1.9 | 各版本JSON、FMF、构建报告、设计审计、赛季报告 | 历史版本和赛季证据 |
| 2.0–2.6 | 各版本JSON、触发文件、设计/机制审计、D5报告 | 历史实验与技术构建 |
| R3–R6 | 各版本JSON、设计审计、D5复盘及builds产物 | 历史候选/历史构建；须按当前固定边界重新核验 |
| N1 | N1.json、N1_DESIGN_AND_AUDIT.md、builds/N1.fmf、builds/N1.report.json | 当前最新D3候选 |

## 归档原则

- 历史事实不改写；旧版本中的旧规则、D0审批、外部研究计划、V0.5强制重生等仅保留为当时的历史记录，不再产生当前约束。
- 新版本所有配方、审计、报告和FMF均保存在本目录；不覆盖历史版本。
- 每个新版本记录实际战术父版本、父FMF SHA-256、recipe SHA-256、构建run/artifact、FMF SHA-256及同次报告SHA-256。
- 赛季成绩只按用户确认的版本和报告记录；不同存档/阵容/随机状态的历史成绩是描述性对照，不作单项因果证明。
