# FM27 引擎红利四后卫｜原始数据来源登记

本文件首先记录每一代战术使用的原始赛季报告来源。分析文档保存在本目录；Exporter原始报告仍由 `eslaulau/FM27-Exporter` 仓库托管。本项目外部机制研究由 [EXTERNAL_ENGINE_BENCHMARK.md](EXTERNAL_ENGINE_BENCHMARK.md) 管理；外部战术只能贡献角色/职责、PI和非红框TI机制参考，必须映射到当前允许的4-2-3-1、4-3-3或4-1-2-3 IP布局，并保持V0.5 OOP位置、心态4及红框15项TI不变。

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
| 2.2 | 45794923641 | [D5复盘](2.2_D5_SEASON_REVIEW_20261126.md) | [Exporter Run 45794923641](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45794923641)（用户确认本赛季使用2.2；Exporter不含战术配置，身份映射来自用户声明） |
| 2.5 | 未进行 | D5尚未执行；D3构建报告：[builds/2.5.report.json](builds/2.5.report.json) | 无Exporter赛季来源；D4导入与D5完整38场验证待执行 |

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


## V2.1｜历史成功改动综合重构与D1-D3构建（2026-11-26）

- 历史证据主索引：本项目唯一总账 TACTIC_INSTRUCTION_DECISION_LEDGER.md 中“历史配置档案｜V0.5–V1.8”及“V2.1 D0”章节；关键原始配方为V1.3.json、V1.6.json、V1.7.json，关键赛季结果及限制按对应D5分析记录。
- 当前build外部快照：metaFM 27.1.1 leaderboard https://metafm.net/leaderboard（72套/164,080场；榜首2.07 PPG；测试覆盖相同AI game plans与球员的四种强弱条件）；metaFM meta https://metafm.net/meta（4-2-3-1分类最佳约1.70 PPG）；FM-Arena 27.1.1 https://fm-arena.com/tactic-testing/（页面快照62套/83,700场；独立协议，不与metaFM合并）。
- 外部样本只作结构假设来源；不能与本队英超38场赛季PPG直接比较，也不能覆盖IP四后场硬约束。
- 构建来源：V0.5原生FMF SHA-256 e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257；Run 45784291686；Artifact 15099985865。
- FMF SHA-256 497afc117defebde99b3cb8433f3e21fee159eeea5f97e5a5aa98130103cc22d；same-run report SHA-256 9d22ef9120bad01c2f65fd9a08235dc8072411af0f283ad0b640405bde8975d2。
- D0–D3完成；D4待游戏内导入；D5待完整赛季报告。


- 2.2 / Run45794923641：用户确认38场英超使用2.2；38/38场、26胜6平6负、84分、87:40；D5性能FAIL。FM27 build 27.1.1+2511875；Exporter v1.5.0；源存档SHA-256 `ed659d74cdfefa0136d6559697797051f430e0684a2f9c7ef8aa4f6541131963`；导出时间2026-11-26T09:46:58Z。战术配置未由Exporter导出，2.2映射来自用户声明。详细复盘见 `2.2_D5_SEASON_REVIEW_20261126.md`。

## 2.3构建来源与验证｜2026-11-26
- [GitHub Actions Run 45801670338](https://github.com/eslaulau/fm-ta/actions/runs/45801670338)，Artifact ID `15107846123`，名称 `FM27_EngineDividend_4Back_2.3`。
- 从V0.5重生，父SHA `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`；FMF 4,528 bytes，SHA-256 `ebceb7d4da76b386007f124dfb1ca0b917fdcbb68b549debd274c4b74d45b5aa`。
- 配方SHA-256 `eb6523f2b55f7e2ee6175ecb59f2366e76103d4e44e8a25bcb754b5a97f9fb8c`；D3八项二进制检查全部通过。D4/D5尚未完成。
- 2.3为Whipped Crosses × Back Post单变量实验；D5结果不得从2.2历史报告推断。


## 2.5 构建身份（非赛季数据来源）
- D3构建：GitHub Actions [Run 45809444848](https://github.com/eslaulau/fm-ta/actions/runs/45809444848)，Artifact ID `15112455227`。
- 父版本：V0.5；父FMF SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。
- FMF SHA-256 `ead1701ff6de352494521730ac5bcf51ac3a3b37d5d93919b3fb40dc45b31d25`；4,552 bytes；D3 8/8独立回读通过。
- 目前没有2.5赛季报告或Exporter Run；不得将构建Run误登记为D5数据来源。


## 2.6构建身份（非赛季数据来源）
- GitHub Actions [Run 45824386052](https://github.com/eslaulau/fm-ta/actions/runs/45824386052)，Artifact ID 15119676222，Artifact ZIP SHA-256 a84d03a5491f5728f646f91b1c69ffe877ddcd623c68e1f6860624d610907dba。

- 最终哈希同步复核：[Run 45824948252](https://github.com/eslaulau/fm-ta/actions/runs/45824948252)，Artifact ID 15118729342，Artifact ZIP SHA-256 9337d4aa33302dd209bf0bc28df3b54fda13c44a35e0fda393a78819ccddd06b；FMF与same-run报告字节级一致。
- 父版本V0.5；父FMF SHA-256 e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257；配方SHA-256 675a6e5122d741c77183ad4f1d92081244600587663e12e8252b7fa7f4404b9c。
- FMF SHA-256 1cbdd6142fd40a60b1073915e78a3a9956f29c2a324383c8dd73213bb2457039；4,616 bytes；报告SHA-256 51eaa1a30dc0d6c60f5e5292ed5e421cf0465b6ba7c94a2a35a0e3f848255955。
- D3 8/8离线回读通过；D4游戏内导入未验证；D5无Exporter赛季来源。不得将构建Run登记为赛季结果。


---

## R3｜设计与构建来源登记（2026-11-26）

| 来源类别 | 资料 | 用途 / 证据边界 |
|---|---|---|
| 用户指定的引擎机制假设 | [ENGINE_DIVIDEND_PRIORITY_INDICATORS_27.1.1.md](ENGINE_DIVIDEND_PRIORITY_INDICATORS_27.1.1.md) | 五组高优先级研究方向；用户提供，尚未附可独立复核的外部原始样本；均标记为待验证假设 |
| 项目配方 | [R3.json](R3.json) | 唯一R3配置源；从V0.5原生FMF重生 |
| 设计审计 | [R3_DESIGN_AND_AUDIT.md](R3_DESIGN_AND_AUDIT.md) | 11槽/22阶段、四类决策、22槽位置矩阵、引擎错位与D5标准 |
| D3构建报告 | [R3.report.json](builds/R3.report.json) | 原生FMF独立回读报告；不是比赛报告，不证明D4/D5 |
| GitHub Actions D3 | [Run 45845663863](https://github.com/eslaulau/fm-ta/actions/runs/45845663863) | D0项目门禁、D1原生预检、D2结构检查、D3构建与独立回读均成功 |
| D3构建Artifact | Artifact ID `15131511605` | FMF 4,676 bytes；SHA-256 `449fb1a76ca8967ccfd674e59c8dd007d40def9da8aafaf8f23edf10c8d3fa4e` |

**R3当前没有Exporter赛季报告。** D4游戏内导入和D5完整38场英超报告待用户测试后登记；在此之前不得登记R3为实战有效版本。


| R3 | 45850910254 | [D5复盘](R3_D5_SEASON_REVIEW_45850910254.md) | [Exporter Run 45850910254](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45850910254) |
| R4 | D3 workflow 45854019401 | [设计审计](R4_DESIGN_AND_AUDIT.md)；[构建报告](builds/R4.report.json) | [R4 D3 Workflow](https://github.com/eslaulau/fm-ta/actions/runs/45854019401)；D5待补Exporter赛季报告 |


| R4 | D3 workflow 45854019401 | [设计审计](R4_DESIGN_AND_AUDIT.md)；[构建报告](builds/R4.report.json) | [R4 D3 Workflow](https://github.com/eslaulau/fm-ta/actions/runs/45854019401)；D5待补Exporter赛季报告 |


## R4 D5 赛季来源登记｜2026-11-27

- 原始报告：[Exporter Run 45914272197](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45914272197)；本队分析：[R4_D5_SEASON_REVIEW_45914272197.md](R4_D5_SEASON_REVIEW_45914272197.md)。用户确认该赛季使用R4，Exporter本身不导出战术配置。
- 源存档SHA-256：`0afc7213468d5da2af8f3137158565432271f42a0eeeeb27d155a5f70831866c`；FM27 build `27.1.1+2511875`；Exporter 1.5.0；fmsave 0.14.3；known_build=false，schema-6借用布局。
- 正式比赛60/60详细报告；英超38/38。球队/球员总量核对1,140/1,140；球员原始进球124/124；识别913/932（97.96%），未识别19；英超识别589、未识别3；位置209/209、评分190/190零差异。
- 角色码解码10类IP角色、309条记录，604条缺失；没有OOP角色/职责/PI/TI逐场映射。角色码只支持有限的IP角色观察。
- 联赛结果12胜10平16负、46分、52:57、xG58.86、xGA61.02；D5 FAIL。不得把局部交叉核对通过写成上游known_build注册或完整字段语义验证。

## R5设计与输入来源登记｜2026-11-27

- 本轮父文件：V0.5原生FMF，SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`；不以R4 FMF作为父文件。
- R5配方：[R5.json](R5.json)，SHA-256 `1990f40739388ed9370431532b3d898a8d414956427f7b0aebe8e434313f8b5c`。
- D0审计：[R5_DESIGN_AND_AUDIT.md](R5_DESIGN_AND_AUDIT.md)；赛季到配置追踪：[R5_SEASON_TO_TACTIC_TRACEABILITY.md](R5_SEASON_TO_TACTIC_TRACEABILITY.md)。
- 主要本队数据输入：R4 Exporter Run [45914272197](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45914272197)，用户声明该赛季使用R4；Exporter不自动识别战术版本。原始存档SHA-256 `0afc7213468d5da2af8f3137158565432271f42a0eeeeb27d155a5f70831866c`；build 27.1.1+2511875，known_build=false，整体partial/unverified。
- 外部结构参考：FM-Arena https://fm-arena.com/；MetaFM https://metafm.net/leaderboard；SI论坛 https://community.sigames.com/forums/forum/19-tactics-training-strategies-discussion/；Sortitoutsi https://sortitoutsi.net/；Reddit https://www.reddit.com/r/footballmanagergames/；FM Scout https://www.fmscout.com/；Ludens Media https://www.ludens.com.tw/；PlayGM https://www.playgm.cc/。完整跨阵型研究字段与迁移判定见EXTERNAL_ENGINE_BENCHMARK.md。
- 当前本机原生权限输入：04_离线原生FMF生成器/catalog.json、FM27GEN1_Offline_FMF_Generator.py、style_template_registry.json；项目门禁与构建脚本：validate_project_iteration.py、build_project_tactic.py、materialize_v05_baseline.py。
- 当前状态：仅完成设计/静态核对；D0 Python门禁与D1-D3未执行；无R5 FMF/report；D4/D5未验证。



## R5.1 D0-D3构建身份登记｜2026-11-27
- 用户要求依据MASTER_UPGRADE_GUIDE重新研发R5；旧R5已INVALIDATED并继续封锁。R5.1为全新实验身份，父源为V0.5原生FMF SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。
- 配方：[R5.1.json](R5.1.json)，SHA-256 `873110d5a885fe105ad28bf0ab61a376b977c4a9cdf1068dd4323255e0984852`；审计：[R5.1_DESIGN_AND_AUDIT.md](R5.1_DESIGN_AND_AUDIT.md)；原生回读报告：[builds/R5.1.report.json](builds/R5.1.report.json)。
- GitHub Actions [Run 45929011714](https://github.com/eslaulau/fm-ta/actions/runs/45929011714)；Artifact ID `15167568553`；Artifact ZIP SHA-256 `3a584523e54d11a155306d72425506e5f35017f30346c470e17e07de0ac1556a`。
- FMF大小4,572 bytes；SHA-256 `292e027e5f9b5664bf224e577e176be27f414c3c655fe5a17b292c88e5fbf51a`；同次构建报告SHA-256 `98d0077a64f5ee2bb89eb74286403894ca7b89d019b5a34030c02e2f17c39c5a`。
- D0项目决策门禁、D1 catalog权限预检、D2 11槽/22阶段/IP四后场、D3 8/8独立二进制回读均通过。
- FM27 build目标：27.1.1+2511875（以本轮项目catalog/配置快照为准）。本轮没有Exporter/D5来源；D4游戏内导入、D5完整38场赛季尚未确认，不得登记为有效战术或达成109分/xG100。

## R5.2 设计和构建来源登记｜2026-11-27
- 用户拒绝R5.1菱形整体设计；R5.1仅保留D3技术档案，不进入D4/D5。
- R5.2固定从V0.5原始FMF重生：SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。
- 配方：[R5.2.json](R5.2.json)；设计/审计：[R5.2_DESIGN_AND_AUDIT.md](R5.2_DESIGN_AND_AUDIT.md)；审计脚本：[prepare_R5_2_audit.py](prepare_R5_2_audit.py)。
- 当前原生研究输入：`04_离线原生FMF生成器/catalog.json` 与 `FM27GEN1_Offline_FMF_Generator.py`；外部机制来源见本轮审计及 [EXTERNAL_ENGINE_BENCHMARK.md](EXTERNAL_ENGINE_BENCHMARK.md)。
- 设计依据：MetaFM 27.1.1公开同协议测试；Trinity 3133（3-4-3 DM→5-2-3）及2-3-2-3宽度/纵深样本。外部结果只作机制线索，不作为本队效果证据。
- 当前状态：R5.2已完成项目D0-D3，D4/D5未验证。Actions Run [45935606662](https://github.com/eslaulau/fm-ta/actions/runs/45935606662)，Artifact ID `15170830371`；Artifact ZIP SHA-256 `f345b3c6557ea097fad8a4b036ca43d11066b36cbf571b419a22982ed0300d23`。FMF 4,564 bytes，SHA-256 `c47adc36a04d3274a1368c1800bec0c9ac9f8ccaf490b1483a423a106e3c0db5`；报告 SHA-256 `a7bb3d1d0f51ba94e485d10adaf64a3b29d20ab96f132356b8c2a889e0924404`；recipe SHA-256 `6f5d29978d6fb0721a9f0b9f7a456d7cde0341ba225044f91c4b331519ae1edd`。D0/D1/D2/D3均PASS；D4/D5不作推断。



## R5.3外部战术结构来源（2026-11-27）
- MetaFM 27.1.1 Vanco Hellcat v21：https://metafm.net/tactics/vanco-hellcat-v21 。公开页面所示样本2,240场，PPG1.93、场均xG2.29；IP 4-1-2-3 / OOP 5-2-3，使用双出球中卫、单DMC、双攻击中场及STL/ST/STR三前锋。R5.3仅迁移阶段结构与角色通道作为待验证假设，不复制成绩，不作为本队战术有效证据。
- MetaFM 27.1.1总榜：https://metafm.net/leaderboard 。用于观察当前patch的IP/OOP双阵型切换和高样本排名；三后卫IP不复制到本项目，IP四后场硬约束不变。
