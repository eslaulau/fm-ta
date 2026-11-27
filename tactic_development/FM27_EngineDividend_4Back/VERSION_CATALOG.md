# FM27 引擎红利四后卫｜版本与产物总目录

## 当前构建候选：N7（D3已通过；D4/D5待验证）

- N7：以N3为父版本，每轮同步调整前场、中场、后场三个区域；ST抢点前锋进攻、MCR前场组织核心支援、DL边后卫支援；保留N3的OOP AMC高位接应出口，29项TI全部沿用N3。
- 实际父版本：N3；父FMF SHA-256：`a28c32350f5923b98a37a428debacc12e1d4d83838248fca9cc919e9d5671dcf`。
- D1-D3：通过；22个阶段位配置精确独立回读，8项离线构建检查全部为true。
- D4游戏内导入：未验证；D5比赛/完整赛季：未验证。
- 配方：[N7.json](N7.json)
- 设计与审计：[N7_DESIGN_AND_AUDIT.md](N7_DESIGN_AND_AUDIT.md)
- FMF：[builds/N7.fmf](builds/N7.fmf)
- 同次回读报告：[builds/N7.report.json](builds/N7.report.json)
- 构建运行：[GitHub Actions 46024743519](https://github.com/eslaulau/fm-ta/actions/runs/46024743519)
- Artifact：[FM27-EngineDividend-4Back-N7-D3](https://github.com/eslaulau/fm-ta/actions/runs/46024743519/artifacts/15210238569)
- FMF SHA-256：`7031a546730a86ee09e8d7ca0a85893bc9c3686da9146d94fb7b6d2505fdb8e7`（4,524 bytes）。
- Recipe SHA-256：`cfcc48d9f457d33a6dcd6a505ccb4618d67314b94fb5e9d5e350fc8e82db1791`。
- 目标：完整38场联赛至少100分且至少100个进球；未经D5实测不得宣称达标。

## N6 实战结果（用户确认失败）

- N6未完成赛季；用户报告累计23场失利后被俱乐部解雇，未保留Exporter报告或下课存档。
- D1-D3技术构建仍然通过，但D5实战判定FAIL；不得继续作为候选或父版本。
- N6配方与FMF作为历史证据保留，不删除、不覆盖。

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
| N2 | 历史版本；已被N3继承和升级 |
| N3 | 已完成D5；77分、90球、34失球；目前N系列较佳基准，未达标 |
| N4 | 已完成D5：68分、73球、46失球；未达标 |
| N5 | 已完成D5：52分、67球、63失球；FAIL | 
| N6 | D1-D3通过；D5实战FAIL：未完成赛季，用户报告23场失利后下课 |

## 归档原则

- 历史事实不改写；旧版本中的旧规则只代表当时情况。
- 新版本所有配方、审计、报告和FMF均保留，不覆盖历史产物。
- 每个新版本记录实际父版本、父FMF SHA-256、recipe SHA-256、构建run、FMF SHA-256及同次回读报告。
- 赛季成绩只按用户确认的版本和报告记录；不同存档/随机状态不作单项因果证明。


## N3赛季复盘（用户确认）

- 报告：[Exporter Run 45970581438](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45970581438)
- 38场：24胜5平9负，77分，90进球、34失球；xG 75.62、xGA 42.86。
- 射门486、射正250、绝佳机会81；传中1,176次，成功175次（14.88%）。
- N3相比N2：+2分、+21进球、-4失球；进攻显著提升，但积分没有同步提升。

## N4｜中路过载 4-3-3

- 父版本：N3；父FMF SHA-256：`a28c32350f5923b98a37a428debacc12e1d4d83838248fca9cc919e9d5671dcf`。
- 状态：D1-D3通过；D4游戏内导入、D5赛季效果待验证。
- 配方：[N4.json](N4.json)
- 设计记录：[N4_DESIGN_AND_AUDIT.md](N4_DESIGN_AND_AUDIT.md)
- FMF：[builds/N4.fmf](builds/N4.fmf)
- 同次回读报告：[builds/N4.report.json](builds/N4.report.json)
- 构建运行：[GitHub Actions 45972134368](https://github.com/eslaulau/fm-ta/actions/runs/45972134368)
- FMF SHA-256：`96215ba3b6c655814ed9b9d8bbf43c1984a4b4a7d6d0164d0b0ba75ae4aa29a9`（4,588 bytes）。
- 目标：完整38场联赛至少100分且至少100个进球；未经D5实测不得宣称达标。

## N5赛季复盘（用户确认，D5 FAIL）

- 报告：[Exporter Run 46017072181](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/46017072181)
- 38场：15胜7平16负，52分，67进球、63失球；xG59.41、xGA50.81；射门437、绝佳机会53。
- 主场35分、42:29；客场17分、25:34，客场12负。
- 对照N3：少25分、少23球、多29个失球；xG少16.21，xGA多7.95，绝佳机会少28。
- 详细诊断：[N5_D5_SEASON_REVIEW_46017072181.md](N5_D5_SEASON_REVIEW_46017072181.md)。

## N6 D3构建记录

- 构建run：46019121563；artifact ID：15207681331。
- 父版本N3；父FMF SHA-256：`a28c32350f5923b98a37a428debacc12e1d4d83838248fca9cc919e9d5671dcf`。
- FMF SHA-256：`c2a156552ab790d06f0f439d4cef8a8e537711444f1994648640966946db2bac`（4,564 bytes）。
- D1-D3通过；D4/D5待验证。
