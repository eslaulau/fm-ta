# FM27 引擎红利四后卫｜原始数据来源登记

本文件记录每一代战术使用的原始赛季报告来源。分析文档保存在本目录；Exporter 原始报告仍由 `eslaulau/FM27-Exporter` 仓库托管，本项目不复制或篡改原始来源。

| 战术版本 | Exporter Run | 本地分析文件 | 原始来源 |
|---|---:|---|---|
| V0.5 | 45540803100 | [分析](V0.5_SEASON_REPORT_ANALYSIS_45540803100.md) | [Exporter Run 45540803100](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/V0.5/45540803100) |
| V0.6 | 45554864463 | [复核](V0.6_REANALYSIS_45554864463.md) | [Exporter Run 45554864463](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/V0.6/45554864463) |
| V0.7 | 45564413834 | [复核](V0.7_REANALYSIS_45564413834.md) | [Exporter Run 45564413834](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/V0.7/45564413834) |
| V0.8 | 45570292427 | [分析](V0.8_SEASON_REPORT_ANALYSIS_45570292427.md) | [Exporter Run 45570292427](https://github.com/eslaulau/FM27-Exporter) |
| V0.9 | 45584292488 | [分析](V0.9_SEASON_REPORT_ANALYSIS_45584292488.md) | [Exporter Run 45584292488](https://github.com/eslaulau/FM27-Exporter) |
| V1.0 | 45602694823 | [分析](V1.0_SEASON_REPORT_ANALYSIS_45602694823.md) | [Exporter Run 45602694823](https://github.com/eslaulau/FM27-Exporter) |
| V1.1 | 45617475212 | [分析](V1.1_SEASON_REPORT_ANALYSIS_45617475212.md) | [Exporter Run 45617475212](https://github.com/eslaulau/FM27-Exporter) |
| V1.2 | 45635282210 | [分析](V1.2_SEASON_REPORT_ANALYSIS_45635282210.md) | [Exporter Run 45635282210](https://github.com/eslaulau/FM27-Exporter) |
| V1.3 | 45644106773 | [分析](V1.3_SEASON_REPORT_ANALYSIS_45644106773.md) | [Exporter Run 45644106773](https://github.com/eslaulau/FM27-Exporter) |
| V1.4 | 45727738275 | [分析](V1.4_SEASON_REPORT_ANALYSIS_45727738275.md) | [Exporter Run 45727738275](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45727738275) |
| V1.5 | 45734426186 | [分析](V1.5_SEASON_REPORT_ANALYSIS_45734426186.md) | [Exporter Run 45734426186](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45734426186) |
| V1.6 | 45744550318 | [分析](V1.6_SEASON_REPORT_ANALYSIS_45744550318.md) | [Exporter Run 45744550318](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45744550318) |
| V1.7 | 45748944770 | [赛季分析](V1.7_SEASON_REPORT_ANALYSIS_45748944770.md)；[设计审计](V1.7_DESIGN_AND_AUDIT.md) | [Exporter Run 45748944770](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45748944770) |
| V1.8 | 45753659141 | [赛季分析](V1.8_SEASON_REPORT_ANALYSIS_45753659141.md)；[设计审计](V1.8_DESIGN_AND_AUDIT.md) | [Exporter Run 45753659141](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45753659141) |

## 来源完整性规则

- 用户确认的战术版本映射必须记录在本表。
- Run ID、原始 URL、游戏 build、存档 SHA、导出时间应从原始报告读取后登记；缺失项标注“未定位/待补录”，不得推断。
- 每个赛季分析文件必须注明其原始 Run ID，并链接回本登记表。
- 原始数据与分析结论分层保存：Exporter 原始 JSON/CSV 是源数据；本项目 Markdown 是分析层；recipe/build report 是战术版本层。


## 版本映射与来源状态补充（2026-11-26）
- V1.6 / Run162：用户确认对应Exporter Run 45744550318；该Run为V1.6赛季报告来源。
- V1.7 / Run163：用户确认 [Exporter Run 45748944770](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45748944770) 使用V1.7；D5已完成，分析文件为 `V1.7_SEASON_REPORT_ANALYSIS_45748944770.md`。源存档SHA-256 `3af3b8a4d5a51903e2d2a2b6a1ae4e1ee40c8a0caed8fc787b054245ce5bc6a1`；FM27 build `27.1.1+2511875`；数据整体 `partial_or_unverified`，限制见分析文件。
- V1.8：D5报告已由用户确认，来源为Run45753659141；英超38场21-9-8、98:55、72分。不得把V1.7 Run45748944770误登记为V1.8成绩。
- 对每个后续版本，先登记用户确认的版本映射；未确认时写“未确认”，不得从文件名或最近一次导出推断。

- V1.8 / Run45753659141：用户确认使用V1.8；英超38场21-9-8、98:55、72分；build 27.1.1+2511875；源存档SHA-256 `6c07ec389a2894a3d2a8829f2618b8dec337c06bb1a2e7af334d4acb798713e0`；数据partial/unverified，详情见V1.8赛季分析。
- V1.9重新设计版：唯一父版本V1.8；recipe `V1.9_REDESIGN.json`；IP 4-3-3 DM / OOP 4-1-4-1；D0-D3由Run167完成；FMF SHA-256 `4b948f9dfeccddc8ae93e225a085a6d1f5b74e9ecd723670a68a7a1b032c4f85`；D4/D5待验证。V1.9 Run165单独保留为旧回退实验，不登记为本版。


## V1.9重新设计版｜外部引擎来源（2026-11-26）
- metaFM 27.1.1总榜：https://metafm.net/leaderboard（72套、164,080场；同一AI game plans/相同球员，四种强弱条件综合PPG）。
- metaFM 4-3-3 DM分类：https://metafm.net/formations/4-3-3-dm（6套、13,440场；领先样本1.882 PPG，IP 4-3-3 DM / OOP 5-2-3）。仅作为IP结构参考，不迁移其OOP或成绩。
- metaFM 4-1-2-1-2 Diamond分类：https://metafm.net/formations/4-1-2-1-2-diamond（5套、11,200场；领先样本1.949 PPG；协议同上）。记录为未选择的结构参考，不代表无效。
- metaFM 4-1-4-1分类：https://metafm.net/formations/4-1-4-1（27.1.1尚无样本，页面展示的是27.1.0单个560场样本）；OOP 4-1-4-1因此标记为本队待验证假设，不作为外部已证实META。
- FM-Arena 27.1.1测试页：https://fm-arena.com/tactic-testing/（62套、83,700场；与metaFM协议不同，不合并样本）。

 
## 赛季报告分析质量与追踪字段（新增）

每个新Run在对应登记项或分析文件中，必须保留可用于复核的：用户确认战术版本映射、赛事/比赛数、球队与球员统计覆盖、身份匹配率、统计对账、位置/角色映射状态、FM27 build、Exporter版本、存档SHA、schema/兼容性状态和未解析字段。分析使用的分组、指标定义、样本数及限制必须能回溯到原始Run。每轮追踪矩阵链接：[SEASON_TO_TACTIC_TRACEABILITY_TEMPLATE.md](SEASON_TO_TACTIC_TRACEABILITY_TEMPLATE.md)。

来源登记只负责记录来源与数据质量，不把Exporter字段自动解释为战术因果；缺少逐场槽位映射时必须明确限制角色/PI归因。

 
## 2026-11-26｜V1.9 R2 外部机制与赛季输入登记

- 本轮赛季输入：Exporter Run45753659141，用户确认V1.8；源存档SHA-256 `6c07ec389a2894a3d2a8829f2618b8dec337c06bb1a2e7af334d4acb798713e0`；FM27 build `27.1.1+2511875`；Exporter 1.5.0；数据质量partial/unverified，详见V1.8分析和R2追踪矩阵。
- metaFM 27.1.1“442菱形中场”：https://metafm.net/zh/tactics/442-0c7c98；阵型分类：https://metafm.net/formations/4-1-2-1-2-diamond；总榜：https://metafm.net/zh/leaderboard。公开样本2,240场、综合1.949 PPG、xG2.28、xGA1.43；公开IP/OOP角色结构；页面部分PI/TI隐藏；外部测试球员所有非门将位置熟练度20。证据等级：当前build结构候选，非本队因果证据。
- FM-Arena 27.1.1聚合榜：https://fm-arena.com/tactic-testing/aggregators/13/；timmerl 4-1-2-1-2 v3有1,350场，73/114分、xGF74、xGA50。独立协议，不与metaFM合并。
- FMAX 27.1.1：https://getfmax.com/en/lab/；出现4-1-2-1-2/菱形变体，作为阵型家族交叉参考，不能与其他平台分数混排。
- PlayGM社区：https://playgm.cc/forum.php?mod=viewthread&tid=986807；2026-11-18“442边翼卫 菱形中场v2.fmf”社区分享，证据等级为用户案例/定性线索。
- 旧V1.9 Run167采用4-3-3 DM / 4-1-4-1；当前27.1.1 4-3-3 DM分类样本较弱，4-1-4-1无当前build足量样本。R2将其标记为历史D3候选，不删除、不宣称D5失败。


## 2026-11-26｜V1.9 R2 历史审计纠正

- [V1.9_REDESIGN_R2_HISTORICAL_REAUDIT_REQUIRED.md](V1.9_REDESIGN_R2_HISTORICAL_REAUDIT_REQUIRED.md)：记录V0.5–V1.8历史总账复核缺口、已发现的版本转折和待补工作。该文件是本轮D0质量纠正依据。


## 2026-11-26｜V0.5–V1.8 全历史D0复核完成
- 已逐一核对14份赛季分析/重分析及其用户确认版本映射；详细数据质量、指标、配置变化和R2历史映射见唯一权威总账 `TACTIC_INSTRUCTION_DECISION_LEDGER.md` 的“D0全历史重生式复核”章节。
- 本次确认：V1.3为综合攻守参照；V1.6为最高积分参照；V1.2/V1.3/V1.7的OOP四后卫+双后腰分层保护有重复正向机会质量观察；V1.1/V1.8的两套具体OOP 5-2-3均需作为高风险历史样本。
- 报告质量边界仍按各版分析文件执行；多数build/schema并非上游完整认证，且无同seed受控A/B，不得据此声称单项因果。
