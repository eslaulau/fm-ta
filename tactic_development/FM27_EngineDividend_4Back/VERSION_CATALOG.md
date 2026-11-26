# FM27 引擎红利四后卫｜版本总目录

## 当前权威状态｜R3（2026-11-26）

- 用户已明确淘汰R2；不再继续测试，不作为R3父版或配置模板。历史文件和构建报告保留。
- **当前主线：R3（D0-D3已通过）**；固定从V0.5原始FMF重生，SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。D3 Run [45845663863](https://github.com/eslaulau/fm-ta/actions/runs/45845663863)，Artifact `15131511605`；FMF 4,676 bytes，SHA-256 `449fb1a76ca8967ccfd674e59c8dd007d40def9da8aafaf8f23edf10c8d3fa4e`；报告：[R3.report.json](builds/R3.report.json)。
- IP：4-2-3-1；OOP：无锋5-2-3。IP后场仅锁定DL/DCL/DCR/DR四个位置槽。
- D5验收：38场至少109分（PPG≥2.85）且全队xG≥100。
- R3已通过D0项目门禁、D1原生权限预检、D2结构检查、D3原生FMF构建与独立回读；D4游戏内导入、D5完整38场赛季验证尚未完成。
- 此条覆盖本文下方旧版“当前候选/当前主线”状态描述；旧版本成绩与配置历史保持原样。


> **2026-11-26｜PPG 2.85整改状态更新**
>
> - 唯一目标：IP有球阶段DL/DCL/DCR/DR各一次，完整英超38场至少109分（PPG≥2.85）。
> - 最近完成D5：2.2（84分，FAIL）；历史最高：V1.6（89分）。
> - 历史最新D3候选曾为2.5；现由R3作为当前唯一主线，R3已通过D0-D3，D4/D5待验。
> - 2.2从V0.5原生FMF重生，IP 4-1-2-1-2 Diamond，OOP 5-2-3；11槽位置/角色/职责与metaFM公开菱形样本逐项对应。它是待验证候选，不是实战升级，也没有证明达到PPG 2.85。
> - V1.9 R2、V2.1保留为历史结构/技术参考；不得自动继承。2.3仍是抽击传中单变量历史候选；2.4是V1.8 IP × V1.3 OOP历史融合候选；2.5保留为历史候选；当前唯一主线为从V0.5重生的R3 IP 4-2-3-1 / OOP无锋5-2-3。
> - 2.2首次构建Run：[45789108253](https://github.com/eslaulau/fm-ta/actions/runs/45789108253)；审计哈希更新后复核Run：[45789543029](https://github.com/eslaulau/fm-ta/actions/runs/45789543029)，Artifact ID `15101682456`；FMF 4,528 bytes；SHA-256 `7feba49ad389125b64690ce00feaf01717f70ae80cb5854eec614e41fc058a34`。

---


> **每轮研发统一入口：** [UPGRADE_GATE.md](UPGRADE_GATE.md)。用户提交赛季报告默认启动完整分析、历史总账联动、引擎红利研究、整体升级与FMF交付；不得把分析与升级拆开。

**项目原始战术：V0.5（V21 原生快照）。本目录仅收录 V0.5 及之后的正式项目资料；V0.5 之前不属于本项目历史。**

本文件是本项目唯一版本总表。每个版本的配方、构建请求（如仓库曾保存）、设计审计、构建报告、赛季分析均以本目录为归档根目录；不得再把本项目的 build request 放回仓库根目录的通用 `build_requests/`。

## 当前状态

> 2026-11-26：研发规则已修订：IP仅要求DL/DCL/DCR/DR四个后场位置，不固定任何IP阵型；OOP完全开放；每轮只设计和构建一个完整方案。每轮战术迭代/赛季复盘必须同步更新 `TACTIC_INSTRUCTION_DECISION_LEDGER.md`、`ITERATION_LOG.md`、本目录与 `SOURCE_REGISTER.md`，并逐个GitHub read-back。详细门禁见 `ANALYSIS_AND_ITERATION_RULES.md` 第七节。

- **最近完成D5：2.2（84分，未达标）；历史最高积分仍为V1.6（89分）。**
- **当前研发状态：R3已完成D0-D3，等待D4游戏内导入及D5完整38场赛季验证；2.2已完成D5并判定FAIL。** V0.5是每轮固定重生参照，所有后续版本均不因版本号较新自动成为父版。

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
| V1.9重新设计版R1（Run167） | V1.8 | IP 4-3-3 DM / OOP 4-1-4-1 | — | [Run167摘要](V1.9_REDESIGN_BUILD_REPORT_SUMMARY.json) | [R1设计审计](V1.9_REDESIGN_DESIGN_AND_AUDIT.md) | D1-D3技术构建通过；8/8回读、22/22阶段；历史复核现已完成；已由R2替代为当前候选 |
| **V1.9重新执行版R2（Run169）** | **V1.8** | **IP 4-1-2-1-2 Diamond / OOP 5-2-3；DMC→DC、双MC→双DM、双ST→AMR/AML** | **待实测** | [R2构建摘要](V1.9_REDESIGN_R2_BUILD_REPORT_SUMMARY.json) · [Run169](https://github.com/eslaulau/fm-ta/actions/runs/45760556137) | [R2设计审计](V1.9_REDESIGN_R2_DESIGN_AND_AUDIT.md) · [赛季追踪矩阵](V1.9_REDESIGN_R2_SEASON_TO_TACTIC_TRACEABILITY_45753659141.md) | D0历史复核完成；D1-D3技术通过；8/8回读、22/22阶段；D4待游戏内核验、D5待完整赛季；FMF 4,688 bytes；SHA-256 `b199063dec9f8745d692ba2abcb78664bdbaa41184d8ea03455afaf6fefea4a5`；D4/D5待验证 |

**口径提醒**
- V0.5 起各正式基准赛季按各自报告的英超赛季口径记录；杯赛/欧战场次不混入该表。
- V0.6 的 20-8-10、83:49、68分；V0.7 的 15-8-15、70:58、53分，来自跨版本决策台账及相应版本审计。
- 版本来自不同存档/阵容/赛季状态，结果是描述性历史比较，不是同随机种子受控 A/B。
- V1.5已完成38场英超D5：25-3-10、78分、65.8%；V1.6已完成38场英超D5：28-5-5、89分、73.7%；V1.7由V1.6 D5触发，Build Run163已成功；D5已由Run45748944770完成，D4未单独逐项验收。V1.8由V1.7 D5触发；D3 Run164通过，D4由用户提供截图解析的位置/角色表确认IP四后卫及OOP无锋5-2-3，D5由Run45753659141完成（21-9-8、72分）。V1.9 Run165为旧回退实验；V1.9 R1 Run167保留为历史D3候选；V1.9 R2 Run169以V1.8为唯一战术父版本，D0历史复核完成、D1-D3技术通过；D4待游戏内核验、D5待完整赛季。

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
| V1.9重新执行版R2（Run169） | [配方](V1.9_REDESIGN_R2.json) | [构建请求](V1.9_REDESIGN_R2_BUILD_REQUEST.json) | [整体审计](V1.9_REDESIGN_R2_DESIGN_AND_AUDIT.md) · [赛季追踪](V1.9_REDESIGN_R2_SEASON_TO_TACTIC_TRACEABILITY_45753659141.md) | [Run169摘要](V1.9_REDESIGN_R2_BUILD_REPORT_SUMMARY.json) · [Run169](https://github.com/eslaulau/fm-ta/actions/runs/45760556137) | 基于V1.8 D5；D0历史复核完成；可进入D4；D5待至少38场英超 | [Run169 artifact](https://github.com/eslaulau/fm-ta/actions/runs/45760556137) · 4,688 bytes · SHA-256 `b199063dec9f8745d692ba2abcb78664bdbaa41184d8ea03455afaf6fefea4a5` |

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


---

## V2.0｜D1-D3 原生构建完成（2026-11-26）

- 父版本/重生基准：V0.5；原始FMF SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。
- 配方：[2.0.json](2.0.json)；设计审计：[2.0_DESIGN_AND_AUDIT.md](2.0_DESIGN_AND_AUDIT.md)；构建报告摘要：[2.0_BUILD_REPORT_SUMMARY.json](2.0_BUILD_REPORT_SUMMARY.json)。
- GitHub Actions：[Run 45781102266](https://github.com/eslaulau/fm-ta/actions/runs/45781102266)；artifact ID `15097803849`；artifact ZIP SHA-256 `1e744bf20a3ee2ca86c834a3795bc1ed915c55acb9251d922b6c4c7cd13edc3a`。
- FMF：4,360 bytes；SHA-256 `80d3a98349eca59affb3d28057cc54550022b1e1e55942d2ce5f1f0920c54bb0`；same-run报告SHA-256 `d7a64ac249f12eec596839dc6ccb4b8ab2f2dc5f26b91d7e1f4a6be0eadd18d2`。
- D1 catalog-backed角色/职责/PI权限预检通过；D2 11槽/22阶段及IP四后场约束通过；D3原生FMF构建与8/8独立回读通过。
- D4游戏内导入/显示待用户确认；D5完整赛季效果待验证。**本版不宣称已达到PPG≥2.85。**


---

## V2.1｜历史成功改动综合重构｜D1-D3完成（2026-11-26）

- 父版本/重生基准：V0.5；FMF SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。
- 配方：[2.1.json](2.1.json)；设计审计：[2.1_DESIGN_AND_AUDIT.md](2.1_DESIGN_AND_AUDIT.md)；构建摘要：[2.1_BUILD_REPORT_SUMMARY.json](2.1_BUILD_REPORT_SUMMARY.json)。
- GitHub Actions：[Run 45784291686](https://github.com/eslaulau/fm-ta/actions/runs/45784291686)；artifact ID `15099985865`；artifact ZIP SHA-256 `d9b974634d291685fd9f831386e7b45790bd264d51b2765b03cef6b0dd4abe0`。
- FMF：4,432 bytes；SHA-256 `497afc117defebde99b3cb8433f3e21fee159eeea5f97e5a5aa98130103cc22d`；same-run report SHA-256 `9d22ef9120bad01c2f65fd9a08235dc8072411af0f283ad0b640405bde8975d2`。
- 方案来源：V1.6进攻骨架 + V1.7 OOP单屏障/宽幅覆盖保护 + V0.5深防线/高位遭遇线错位实验。不是从V1.7或V2.0继承FMF。
- D1 catalog角色/职责/PI预检通过；D2 11槽/22阶段及IP四后场通过；D3 8/8独立二进制回读通过。
- D4游戏内导入/显示待用户确认；D5完整赛季效果待验证。**本版不宣称已达到PPG≥2.85。**


## V2.2｜菱形IP四后卫 + OOP 5-2-3｜D1-D3完成（2026-11-26）

- 父版本/重生基准：V0.5；FMF SHA-256 e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257。
- 配方：[2.2.json](2.2.json)；设计审计：[2.2_DESIGN_AND_AUDIT.md](2.2_DESIGN_AND_AUDIT.md)；触发：[2.2_TRIGGER.json](2.2_TRIGGER.json)。
- GitHub Actions：首次构建[Run 45789108253](https://github.com/eslaulau/fm-ta/actions/runs/45789108253)；审计哈希复核[Run 45789543029](https://github.com/eslaulau/fm-ta/actions/runs/45789543029)；最新Artifact ID 15101682456。
- FMF：4,528 bytes；SHA-256 7feba49ad389125b64690ce00feaf01717f70ae80cb5854eec614e41fc058a34；same-run report SHA-256 ab436693df94409860b0ca4d6eb57ec79ca3b3ba6d643fdea72c5112ab6ed7e8。
- 方案：IP 4-1-2-1-2 Diamond，OOP 5-2-3；11槽位置/角色/职责与metaFM公开菱形样本逐项对应；五名球员跨位。
- D1-D3：原生权限预检通过；11槽/22阶段通过；8/8独立二进制回读通过。
- D4：用户声明本赛季使用2.2；Exporter不导出战术配置，不能独立核验战术身份。
- D5：[完整38场复盘](2.2_D5_SEASON_REVIEW_20261126.md)；26胜6平6负，84分，87:40，xG81.83，98次绝佳机会；**性能FAIL，未达到109分**。原始报告：[Exporter Run45794923641](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45794923641)。
- 决策：2.2保留为失败基准；2.3暂停，先完成进攻机制专项审计。
- 第一轮进攻机制审计：[2.2_ATTACKING_MECHANISM_AUDIT_20261126.md](2.2_ATTACKING_MECHANISM_AUDIT_20261126.md)；已定位传中效率和进入前场后的机会质量为优先核查方向，仍属待验证假设。


## 2.3｜抽击传中单变量候选（2026-11-26）
- 从V0.5原生FMF重生；2.2仅作为假设来源，不是父版。
- 唯一变量：团队传中方式 LOW_CROSSES → WHIPPED_CROSSES；两侧翼卫后点目标及其余配方配置保持不变。
- D1-D3：GitHub Actions [Run 45801670338](https://github.com/eslaulau/fm-ta/actions/runs/45801670338) 成功；原生预检、11槽/22阶段、PI权限和8/8二进制回读通过。
- FMF 4,528 bytes；SHA-256 `ebceb7d4da76b386007f124dfb1ca0b917fdcbb68b549debd274c4b74d45b5aa`；Artifact `15107846123`。
- D4待游戏内导入；D5未测试。2.3不是达标版本，不宣称PPG改善。配方与审计见[2.3.json](2.3.json)及[2.3_DESIGN_AND_AUDIT.md](2.3_DESIGN_AND_AUDIT.md)。


## 2.3状态纠正｜不得称为迭代升级（2026-11-26）

2.3只把 LOW_CROSSES 改为 WHIPPED_CROSSES，属于单变量诊断候选，不是综合战术升级。保留FMF和D1-D3构建记录，仅用于验证传中轨迹假设；不得宣传为“新一代升级版”，也不要求用户将其视为主力战术。

**主研发方向改为历史强项整合式重构**：从V0.5原始FMF重生，完整读取V0.5–V1.8所有可用配方、PI/TI、IP/OOP结构、赛季报告和构建证据；逐项比较V1.6积分最高（89分）、V1.8进球最多（98球）、V1.3失球最少（30球）背后的配置差异，识别可兼容的机制、冲突与样本限制。重新设计完整11槽/22阶段，不以只改一项TI作为主版本升级。必须保留有球四后卫硬约束。

验收仍以38场至少109分为唯一最终门槛；进球产出是优先优化方向，但不得牺牲积分。没有完整历史配方对照和机制说明，不发布新的主版本FMF。


## 2.4｜历史强项融合重构（2026-11-26）
- 定位：完整战术结构融合，不是单一指令微调。IP采用V1.8进攻11槽；OOP采用V1.3防守11槽；从V0.5原生FMF重新构建。
- 设计依据：V1.8 98球/88.87 xG但55失球/59.67 xGA/72分；V1.3 83球/80.54 xG、30失球/34.27 xGA、88分。融合假设为保留V1.8进攻结构并恢复V1.3 OOP 4-2-1-2-1分层保护。
- 构建：Run 45803243163成功；Artifact 15108511626；FMF 4,536 bytes；SHA-256 50bbec5beb21f528c0504abde8f37575b21dbb4b85b506f4ae125cfe8fa9ce77。
- D1-D3通过，8/8二进制回读检查通过；D4游戏导入、D5比赛效果待验证。2.4不宣称已达到109分。
- 完整设计见[2.4_DESIGN_AND_AUDIT.md](2.4_DESIGN_AND_AUDIT.md)，机器配方见[2.4.json](2.4.json)。


---

## 2.4 配方形状标注纠正｜2026-11-26

复核 `2.4.json` 的实际11个IP位置槽：GK、DR、DCR、DCL、DL、MCR、MCL、AMR、AML、AMC、ST，实际构成是 **4-2-3-1**，不是其旧审计文字中误标的4-1-2-1-2 Diamond。保留2.4历史文件与构建产物，不改写历史；后续引用以实际配方位置槽为准。

## 2.5｜IP菱形四后卫 + OOP 4-2-1-2-1｜D1-D3完成（2026-11-26）

- 父版本/重生基准：V0.5；父FMF SHA-256 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。2.2、2.4仅作为历史证据，不是父版。
- 配方：[2.5.json](2.5.json)；设计审计：[2.5_DESIGN_AND_AUDIT.md](2.5_DESIGN_AND_AUDIT.md)；[FMF文件](builds/2.5.fmf)；机器回读报告：[builds/2.5.report.json](builds/2.5.report.json)。
- GitHub Actions项目专用门禁：[Run 45809444848](https://github.com/eslaulau/fm-ta/actions/runs/45809444848)；Artifact ID `15112455227`；Artifact ZIP SHA-256 `0dcf4f6393d89a22abf830f6408295db810ca0885f363fc1f7df338cccd1047f`。
- FMF：4,552 bytes；SHA-256 `ead1701ff6de352494521730ac5bcf51ac3a3b37d5d93919b3fb40dc45b31d25`；构建报告SHA-256 `18060a62b01d2465570d6a02d6ac2b3835c4a0345c4f4d938e3b513da59318f7`；recipe SHA-256 `132e463277680319532bc668530d6277300509f5fde33ca86a05aa8541508ccd`。
- IP：4-1-2-1-2 Diamond，严格DL/DCL/DCR/DR四后场；OOP：4-2-1-2-1。单侧DR翼卫进攻、DL内收边后卫防守；一攻一策应中场；前场组织核心策应；抢点前锋进攻+拖后前锋策应。
- OOP采用V1.3分层保护的角色/职责结构重新映射；当前27.1.1 catalog不允许相关OOP角色写入个人Trigger Press/凶狠铲抢PI，因此没有伪造这些指令。抢点前锋不允许后点PI，也已移除。
- D1原生角色/职责/PI权限预检通过；D2 11槽/22阶段及IP四后场约束通过；D3外层roundtrip、全部成员解密/Zstandard校验、TAC完整解析、22阶段精确回读、PI权限、TI向量和原生style身份检查8/8通过。
- D4游戏内导入/中文显示/球员位置熟悉度待用户确认；D5完整38场英超报告待验证。**本版不宣称已经达到109分或PPG≥2.85。**


## 2.6｜IP 4-1-3-2 / OOP 4-4-2 DM｜D1-D3完成（2026-11-26）

- 定位：重启V1.6高要求升级计划；V1.6仅作历史证据，父版本固定V0.5。2.3用户实测数回合全败后正式放弃；2.5仅D3、无D4/D5，保留历史。
- 配方：[2.6.json](2.6.json)；D0审计：[2.6_DESIGN_AND_AUDIT.md](2.6_DESIGN_AND_AUDIT.md)；FMF：[builds/2.6.fmf](builds/2.6.fmf)；回读报告：[builds/2.6.report.json](builds/2.6.report.json)。
- IP严格4-1-3-2，DL/DCL/DCR/DR各一次；OOP 4-4-2 DM；心态5（积极）。
- GitHub Actions [Run 45824386052](https://github.com/eslaulau/fm-ta/actions/runs/45824386052)；Artifact ID 15119676222；Artifact ZIP SHA-256 a84d03a5491f5728f646f91b1c69ffe877ddcd623c68e1f6860624d610907dba。
- 最终哈希同步复核：[Run 45824948252](https://github.com/eslaulau/fm-ta/actions/runs/45824948252)；Artifact ID 15118729342；ZIP SHA-256 9337d4aa33302dd209bf0bc28df3b54fda13c44a35e0fda393a78819ccddd06b；FMF与报告均与首次最终构建字节一致。
- FMF 4,616 bytes；SHA-256 1cbdd6142fd40a60b1073915e78a3a9956f29c2a324383c8dd73213bb2457039；同次构建报告SHA-256 51eaa1a30dc0d6c60f5e5292ed5e421cf0465b6ba7c94a2a35a0e3f848255955；recipe SHA-256 675a6e5122d741c77183ad4f1d92081244600587663e12e8252b7fa7f4404b9c。
- D1 catalog角色/职责/PI权限预检通过；D2 11槽/22阶段及IP四后场通过；D3 8/8独立二进制回读通过。game_interactive_import=false、match_engine=false。
- D4：待用户在FM27导入并核对中文显示、IP/OOP阵型、位置熟悉度；D5：待完整38场赛季报告。未宣称109分或xG100达标。


## R3 D5 与 R4 当前状态（2026-11-26）

- **R3：D5 FAIL。** Exporter Run 45850910254 的38场英超结果为66分、PPG1.737、xG65.00、xGA46.18；未达到109分与xG100双门槛。详细分析见 [R3 D5复盘](R3_D5_SEASON_REVIEW_45850910254.md)。R3保留为历史实验，不再标记为达标候选。
- **R4：唯一下一轮设计候选。** IP 4-2-3-1 / OOP strikerless 5-2-3，四后场约束不变；根据R3位置/球队数据调整右翼卫职责、DMR跨阶段角色、OOP前场三出口和两项球队进攻指令。严格以V0.5原生FMF重生；D0-D3待构建，D4/D5未验证。


- **R4：D0-D3 PASS，当前唯一待验证候选。** Workflow Run 45854019401；FMF SHA-256 `8fbe0bddac5e7645a42715e378a8d5dd67400dc9e0f1b7be3ea7c2427febf899`；11组IP/OOP与22阶段精确回读通过。D4游戏内导入、D5完整赛季仍待验证。R3维持历史D5 FAIL状态。
