# FM27 引擎红利四后卫｜版本与产物总目录

## 当前版本：N2

- 战术：N2｜双内锋纵深增量 4-1-2-3。
- 父版本：N1；父FMF SHA-256：`ee945b19e4134e16f722eef624f9cfa1e1f7584d2157ee1414c5a8c78b595deb`。
- 状态：D1-D3通过；D4游戏内导入、D5赛季效果待验证。
- 配方：[N2.json](N2.json)
- 设计记录：[N2_DESIGN_AND_AUDIT.md](N2_DESIGN_AND_AUDIT.md)
- FMF：[builds/N2.fmf](builds/N2.fmf)
- 同次回读报告：[builds/N2.report.json](builds/N2.report.json)
- 构建运行：[GitHub Actions 45957641658](https://github.com/eslaulau/fm-ta/actions/runs/45957641658)
- FMF SHA-256：`dd15cb0fed579eccd6fc479c33d3d205388ae3b44990f08f2a5942bedc94f9ed`（4,576 bytes）。
- 目标：完整38场联赛至少100分且至少100个进球；未经D5实测不得宣称达标。

## N1赛季结果（用户确认）

- 报告：[Exporter Run 45955914738](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45955914738)
- 38场：20胜10平8负，70分，77进球、45失球；xG 70.23、xGA 42.72。
- 传中1,046次，成功160次（15.3%）；主场41分、客场29分。
- N1为已完成D5赛季的历史版本；结果未达到当前100分/100球目标。

## 现行规则入口

1. [PROJECT_RULES.md](PROJECT_RULES.md)
2. [TACTIC_FIXED_CONSTRAINTS.md](TACTIC_FIXED_CONSTRAINTS.md)
3. [UPGRADE_GATE.md](UPGRADE_GATE.md)
4. [GENERATION_EXECUTION_POLICY.md](GENERATION_EXECUTION_POLICY.md)
5. [AGENTS.md](AGENTS.md)

## 历史证据入口

- [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)：完整历史配置、逐代差异、赛季结果和证据状态。
- [ITERATION_LOG.md](ITERATION_LOG.md)：历史研发事件、构建与复盘过程。
- [V0.5_BASELINE.md](V0.5_BASELINE.md) 与 [V0.5_NATIVE_SNAPSHOT.json](V0.5_NATIVE_SNAPSHOT.json)：历史原生快照和格式载体。
- 各版本recipe、设计审计、D5报告、FMF及build report均保留。

## 历史版本索引

| 版本系列 | 当前定位 |
|---|---|
| V0.5–V1.9 | 历史战术与赛季证据 |
| 2.0–2.6 | 历史实验与技术构建 |
| R3–R6 | 历史候选/构建，须按现行固定边界重新核验 |
| N1 | 已完成D5；本次Run 45955914738：70分、77球 |
| N2 | 当前最新D3候选；D4/D5待验证 |

## 归档原则

- 历史事实不改写；旧版本中的旧规则只代表当时情况。
- 新版本所有配方、审计、报告和FMF均保留，不覆盖历史产物。
- 每个新版本记录实际父版本、父FMF SHA-256、recipe SHA-256、构建run、FMF SHA-256及同次回读报告。
- 赛季成绩只按用户确认的版本和报告记录；不同存档/随机状态不作单项因果证明。
