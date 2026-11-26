# FM27 引擎红利四后卫｜版本总目录

> **每轮研发统一入口：** [UPGRADE_GATE.md](UPGRADE_GATE.md)。用户提交赛季报告默认启动完整分析、历史总账联动、引擎红利研究、整体升级与FMF交付；不得把分析与升级拆开。

**项目原始战术：V0.5（V21 原生快照）。本目录仅收录 V0.5 及之后的正式项目资料；V0.5 之前不属于本项目历史。**

本文件是本项目唯一版本总表。每个版本的配方、构建请求（如仓库曾保存）、设计审计、构建报告、赛季分析均以本目录为归档根目录；不得再把本项目的 build request 放回仓库根目录的通用 `build_requests/`。

## 当前状态

> 2026-11-26：研发规则已修订：IP仅要求DL/DCL/DCR/DR四个后场位置，不固定任何IP阵型；OOP完全开放；每轮只设计和构建一个完整方案。每轮战术迭代/赛季复盘必须同步更新 `TACTIC_INSTRUCTION_DECISION_LEDGER.md`、`ITERATION_LOG.md`、本目录与 `SOURCE_REGISTER.md`，并逐个GitHub read-back。详细门禁见 `ANALYSIS_AND_ITERATION_RULES.md` 第七节。

- **最近完成D5的研发基准：V1.8（Exporter Run45753659141）**
- **当前研发候选：V1.9重新执行版R2**，父版本V1.8；IP 4-1-2-1-2 Diamond、OOP 5-2-3；D0历史总账审计未验收；D1-D3技术构建通过（Run169，8/8独立回读、22/22阶段）；D4/D5暂缓。
- **历史V1.9 Run165：** 完整复用V1.7配方的OOP回退实验，保留原构建身份，不认定为正式性能升级。
- **历史V1.9重新设计版R1（Run167）：** IP 4-3-3 DM、OOP 4-1-4-1；D3通过但D4/D5未验证。当前27.1.1外部证据复核后由R2替代为当前研发候选；不将R1标记为比赛失败。
- **最高完整英超胜率：73.7%（V1.6，28胜5平5负、89分）**；V1.3仍是失球最少（30球）和4负的防守基准。
- 版本比较必须使用英超联赛口径。非完整 38 场样本单独标记，不与完整赛季胜率排名混用。

## 完整战术历史总账

**逐代配置与差异的唯一主表：** [TACTIC_INSTRUCTION_DECISION_LEDGER.md（历史配置档案章节）](TACTIC_INSTRUCTION_DECISION_LEDGER.md（历史配置档案章节）)。它包含V0.5–V1.8每版的赛季表现、IP/OOP 11槽角色/职责/PI、TI/心态和父子版本逐项变化。本目录只保留成绩索引；不能代替完整配置历史总账。

## 历代联赛结果总表

胜率 = 胜场 ÷ 实际已赛英超场次。仅 38 场完整赛季可进入“完整赛季排名”。

| 版本 | 英超场次 | 胜-平-负 | 胜率 | 进失球 | 积分 | 数据级别 |
|---|---:|---:|---:|---:|---:|---|
| V0.5 | 38 | 20-9-9 | 52.6% | 75:43 | 69 | 完整赛季 |
| V0.6 | 38 | 20-8-10 | 52.6% | 83:49 | 68 | 完整赛季 |
| V0.7 | 38 | 15-8-15 | 39.5% | 70:58 | 53 | 完整赛季 |
| V0.8 | 38 | 19-9-10 | 50.0% | 79:46 | 66 | 完整赛季 |
| V0.9 | 38 | 25-5-8 | 65.8% | 86:48 | 80 | 完整赛季 |
| V1.0 | 38 | 27-6-5 | **71.1%** | 107:35 | 87 | 完整赛季 |
| V1.1 | 38 | 19-10-9 | 50.0% | 84:48 | 67 | 完整赛季 |
| V1.2 | 38 | 26-8-4 | 68.4% | 72:29 | 86 | 完整赛季 |
| V1.3 | 38 | 27-7-4 | **71.1%** | 83:30 | **88** | 完整赛季 |
| V1.4 | 38 | 27-2-9 | **71.1%** | 101:53 | 83 | 完整赛季 |
| V1.5 | 38 | 25-3-10 | 65.8% | 95:48 | 78 | 完整赛季 |
| V1.6 | 38 | 28-5-5 | **73.7%** | 87:37 | **89** | 完整赛季 |
| V1.7 | 38 | 25-7-6 | 65.8% | 79:36 | 82 | 完整赛季；Exporter Run45748944770；数据partial/unverified |
| V1.8 | 38 | 21-9-8 | 55.3% | 98:55 | 72 | 完整38场；Run45753659141；partial/unverified |
| V1.9（Run165旧实验） | V1.8载体 / V1.7配方 | OOP回退至V1.7的4-2-1-2-1；整套配置复用 | — | — | — | 构建回读完成；非正式性能升级；D4/D5待验证 |
| V1.9重新设计版R1（Run167） | V1.8 | IP 4-3-3 DM / OOP 4-1-4-1 | — | [Run167摘要](V1.9_REDESIGN_BUILD_REPORT_SUMMARY.json) | [R1设计审计](V1.9_REDESIGN_DESIGN_AND_AUDIT.md) | D1-D3技术构建通过；8/8回读、22/22阶段；历史总账审计未验收；已由R2替代为当前候选 |
| **V1.9重新执行版R2（Run169）** | **V1.8** | **IP 4-1-2-1-2 Diamond / OOP 5-2-3；DMC→DC、双MC→双DM、双ST→AMR/AML** | **待实测** | [R2构建摘要](V1.9_REDESIGN_R2_BUILD_REPORT_SUMMARY.json) · [Run169](https://github.com/eslaulau/fm-ta/actions/runs/45760556137) | [R2设计审计](V1.9_REDESIGN_R2_DESIGN_AND_AUDIT.md) · [赛季追踪矩阵](V1.9_REDESIGN_R2_SEASON_TO_TACTIC_TRACEABILITY_45753659141.md) | D0未验收；D1-D3技术通过；8/8回读、22/22阶段；FMF 4,688 bytes；SHA-256 `b199063dec9f8745d692ba2abcb78664bdbaa41184d8ea03455afaf6fefea4a5`；D4/D5待验证 |

**口径提醒**
- V0.5 起各正式基准赛季按各自报告的英超赛季口径记录；杯赛/欧战场次不混入该表。
- V0.6 的 20-8-10、83:49、68分；V0.7 的 15-8-15、70:58、53分，来自跨版本决策台账及相应版本审计。
- 版本来自不同存档/阵容/赛季状态，结果是描述性历史比较，不是同随机种子受控 A/B。
- V1.5已完成38场英超D5：25-3-10、78分、65.8%；V1.6已完成38场英超D5：28-5-5、89分、73.7%；V1.7由V1.6 D5触发，Build Run163已成功；D5已由Run45748944770完成，D4未单独逐项验收。V1.8由V1.7 D5触发；D3 Run164通过，D4由用户提供截图解析的位置/角色表确认IP四后卫及OOP无锋5-2-3，D5由Run45753659141完成（21-9-8、72分）。V1.9 Run165为旧回退实验；V1.9 R1 Run167保留为历史D3候选；V1.9 R2 Run169以V1.8为唯一战术父版本，D0历史审计未验收、D1-D3技术通过，D4/D5暂缓。

## 版本文件清单

所有相对链接均以本目录为基准。

| 版本 | 配方 | 构建请求 | 设计/审计 | 构建报告 | 赛季分析/复核 | FMF |
|---|---|---|---|---|---|---|
| V0.5 | 基准见 [BASELINE](V0.5_BASELINE.md) | 未单独归档 | [角色/PI审计](V0.5_ROLE_PI_AUDIT_45540803100.md) | 未单独归档 | [赛季分析](V0.5_SEASON_REPORT_ANALYSIS_45540803100.md) | 基准 FMF 哈希见 BASELINE |
| V0.6 | [JSON](V0.6.json) | 未单独归档 | [设计审计](V0.6_DESIGN_AND_AUDIT.md) | [报告](V0.6_BUILD_REPORT.json) | [复核](V0.6_REANALYSIS_45554864463.md) | [FMF](V0.6.fmf) |
| V0.7 | [JSON](V0.7.json) | 未单独归档 | [设计审计](V0.7_DESIGN_AND_AUDIT.md) | [报告](V0.7_BUILD_REPORT.json) | [复核](V0.7_REANALYSIS_45564413834.md) | [FMF](V0.7.fmf) |
| V0.8 | [JSON](V0.8.json) | 未单独归档 | [设计审计](V0.8_DESIGN_AND_AUDIT.md) | [报告](V0.8_BUILD_REPORT.json) | [赛季分析](V0.8_SEASON_REPORT_ANALYSIS_45570292427.md) | [FMF](V0.8.fmf) |
| V0.9 | [JSON](V0.9.json) | [JSON](V0.9_BUILD_REQUEST.json) | [设计审计](V0.9_DESIGN_AND_AUDIT.md) | [报告](V0.9_BUILD_REPORT.json) | [赛季分析](V0.9_SEASON_REPORT_ANALYSIS_45584292488.md) | [FMF](V0.9.fmf) |
| V1.0 | [JSON](V1.0.json) | [JSON](V1.0_BUILD_REQUEST.json) | [设计审计](V1.0_DESIGN_AND_AUDIT.md) | [报告](V1.0_BUILD_REPORT.json) | [赛季分析](V1.0_SEASON_REPORT_ANALYSIS_45602694823.md) | Actions 历史 |
| V1.1 | [JSON](V1.1.json) | [JSON](V1.1_BUILD_REQUEST.json) | [设计审计](V1.1_DESIGN_AND_AUDIT.md) | [报告](V1.1_BUILD_REPORT.json) | [赛季分析](V1.1_SEASON_REPORT_ANALYSIS_45617475212.md) | Actions 历史 |
| V1.2 | [JSON](V1.2.json) | [JSON](V1.2_BUILD_REQUEST.json) | [设计审计](V1.2_DESIGN_AND_AUDIT.md) | [报告](V1.2_BUILD_REPORT.json) | [赛季分析](V1.2_SEASON_REPORT_ANALYSIS_45635282210.md) | Actions 历史 |
| V1.3 | [JSON](V1.3.json) | [JSON](V1.3_BUILD_REQUEST.json) | [设计审计](V1.3_DESIGN_AND_AUDIT.md) | [报告](V1.3_BUILD_REPORT.json) | [赛季分析](V1.3_SEASON_REPORT_ANALYSIS_45644106773.md) | Actions 历史 |
| V1.4 | [JSON](V1.4.json) | [JSON](V1.4_BUILD_REQUEST.json) | [设计审计](V1.4_DESIGN_AND_AUDIT.md) | [报告](V1.4_BUILD_REPORT.json) | [赛季分析](V1.4_SEASON_REPORT_ANALYSIS_45727738275.md) | Actions 历史 |
| V1.5 | [JSON](V1.5.json) | [JSON](V1.5_BUILD_REQUEST.json) | [设计审计](V1.5_DESIGN_AND_AUDIT.md) | [报告](V1.5_BUILD_REPORT.json) | [赛季分析](V1.5_SEASON_REPORT_ANALYSIS_45734426186.md) | Actions Run149 artifact |
| V1.6 | [JSON](V1.6.json) | [JSON](V1.6_BUILD_REQUEST.json) | [设计审计](V1.6_DESIGN_AND_AUDIT.md) | [构建报告](V1.6_BUILD_REPORT.json) | [赛季分析](V1.6_SEASON_REPORT_ANALYSIS_45744550318.md) | Run162 FMF 4,480 bytes |
| V1.7 | [JSON](V1.7.json) | [JSON](V1.7_BUILD_REQUEST.json) | [设计审计](V1.7_DESIGN_AND_AUDIT.md) | [构建报告](V1.7_BUILD_REPORT.json) | [D5赛季分析](V1.7_SEASON_REPORT_ANALYSIS_45748944770.md) · Run45748944770 | [正式FMF](V1.7.fmf) · 4,504 bytes · SHA-256 `42a7038c4fe89667d0f1f7c7ff1ff74f31633f52f570d0f8b4d4d9c774ee46ab` |
| V1.8 | [JSON](V1.8.json) | [JSON](V1.8_BUILD_REQUEST.json) | [设计审计](V1.8_DESIGN_AND_AUDIT.md) | [D3构建摘要](V1.8_BUILD_REPORT_SUMMARY.json) · [Run164](https://github.com/eslaulau/fm-ta/actions/runs/45750563671) | [D5分析](V1.8_SEASON_REPORT_ANALYSIS_45753659141.md) · Run45753659141 | [Run164 artifact](https://github.com/eslaulau/fm-ta/actions/runs/45750563671) · 4,616 bytes · SHA-256 `51e94c684c66ce016950d93f2619a40086820e7a9dcf792b7251d4ac67fa4e72` |
| V1.9旧实验（Run165） | [JSON](V1.9.json) | [JSON](V1.9_BUILD_REQUEST.json) | [旧审计](V1.9_DESIGN_AND_AUDIT.md) | [旧摘要](V1.9_BUILD_REPORT_SUMMARY.json) · [Run165](https://github.com/eslaulau/fm-ta/actions/runs/45754396168) | D4/D5待验证；非正式性能升级 | [Run165 artifact](https://github.com/eslaulau/fm-ta/actions/runs/45754396168) · 4,552 bytes · SHA-256 `57446c3d4e4cb3cd957840a436843f8b87fcb2d119bc223e2136d9512f1af8e7` |
| V1.9重新设计版（Run167） | [配方](V1.9_REDESIGN.json) | [构建请求](V1.9_REDESIGN_BUILD_REQUEST.json) | [整体审计](V1.9_REDESIGN_DESIGN_AND_AUDIT.md) | [Run167摘要](V1.9_REDESIGN_BUILD_REPORT_SUMMARY.json) · [Run167](https://github.com/eslaulau/fm-ta/actions/runs/45756670647) | D4/D5待验证 | [Run167 artifact](https://github.com/eslaulau/fm-ta/actions/runs/45756670647) · 4,688 bytes · SHA-256 `4b948f9dfeccddc8ae93e225a085a6d1f5b74e9ecd723670a68a7a1b032c4f85` |
| V1.9重新执行版R2（Run169） | [配方](V1.9_REDESIGN_R2.json) | [构建请求](V1.9_REDESIGN_R2_BUILD_REQUEST.json) | [整体审计](V1.9_REDESIGN_R2_DESIGN_AND_AUDIT.md) · [赛季追踪](V1.9_REDESIGN_R2_SEASON_TO_TACTIC_TRACEABILITY_45753659141.md) | [Run169摘要](V1.9_REDESIGN_R2_BUILD_REPORT_SUMMARY.json) · [Run169](https://github.com/eslaulau/fm-ta/actions/runs/45760556137) | 基于V1.8 D5；D0历史复核待补；D4/D5暂缓 | [Run169 artifact](https://github.com/eslaulau/fm-ta/actions/runs/45760556137) · 4,688 bytes · SHA-256 `b199063dec9f8745d692ba2abcb78664bdbaa41184d8ea03455afaf6fefea4a5` |

## 唯一研发入口与规则

- [项目说明与历史记录](README.md)
- [唯一版本迭代日志](ITERATION_LOG.md)
- [跨版本指令决策台账](TACTIC_INSTRUCTION_DECISION_LEDGER.md)
- [分析与迭代规则](ANALYSIS_AND_ITERATION_RULES.md)
- 当前战术升级按四层执行：结构搜索与空间协同 → 角色/职责引擎协同 → PI/TI/OI服务结构；详见正式规则第3.1–3.6节。
- [外部引擎基准](EXTERNAL_ENGINE_BENCHMARK.md)
- [角色/PI审计模板](ROLE_PI_AUDIT_TEMPLATE.md)
- [原始报告来源登记](SOURCE_REGISTER.md)

## 归档规则（强制）

1. 新版本所有文件统一放在本目录，不得散落到仓库根目录通用 `build_requests/`。
2. 文件名统一为 `Vx.y_<TYPE>.<ext>`，例如 `V1.6.json`、`V1.6_BUILD_REQUEST.json`、`V1.6_DESIGN_AND_AUDIT.md`、`V1.6_BUILD_REPORT.json`、`V1.6_SEASON_REPORT_ANALYSIS_<run>.md`。
3. 同一版本的 recipe、build request、build report、FMF、D4 验收、D5 分析必须互相引用同一父版本、Actions run/artifact、SHA-256 和数据源。
4. 原始 Exporter 数据仍以 FM27-Exporter 仓库为原始来源；本项目保存完整分析和永久来源 URL/Run ID，不伪造“原始数据已镜像”。如果用户要求离线完整归档，再把原始报告快照导入本目录的 `source_snapshots/`。
5. 不覆盖历史版本、不把草案混为正式版本；撤销/取代的内容保留并明确标注。
6. 每次提交后回读目录、校验链接与 SHA；总目录必须同步更新。

 
## 赛季诊断与升级决策追踪（强制）

每个版本条目必须链接本轮赛季分析和 `Vx.y_SEASON_TO_TACTIC_TRACEABILITY_<run>.md`。版本摘要需列出主要ISS/EXP编号、四类决策、收益—代价目标、下一轮D5验证清单及D0–D5状态。新报告到来后，先回看父版本条目中的全部D5目标，再建立本轮问题编号；不得只比较上一版本的总积分。追踪表模板：[SEASON_TO_TACTIC_TRACEABILITY_TEMPLATE.md](SEASON_TO_TACTIC_TRACEABILITY_TEMPLATE.md)。
