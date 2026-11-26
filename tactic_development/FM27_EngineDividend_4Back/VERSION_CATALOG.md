# FM27 引擎红利四后卫｜版本总目录

本文件是本项目唯一版本总表。每个版本的配方、构建请求（如仓库曾保存）、设计审计、构建报告、赛季分析均以本目录为归档根目录；不得再把本项目的 build request 放回仓库根目录的通用 `build_requests/`。

## 当前状态

> 2026-11-26：跨版本总账已进行结构修复。每轮战术迭代/赛季复盘必须同步更新 `TACTIC_INSTRUCTION_DECISION_LEDGER.md`、`ITERATION_LOG.md`、本目录与 `SOURCE_REGISTER.md`，并逐个GitHub read-back。详细门禁见 `ANALYSIS_AND_ITERATION_RULES.md` 第七节。

- **当前开发版本：V1.8（D0完成；D1–D3构建中；D4/D5待验证）**
- **最近完成阶段：V1.7 D5赛季复盘（Run45748944770）；V1.8已完成D0结构设计**
- **仍待验证：V1.8 D1–D3构建、D4游戏内导入、D5比赛/赛季表现**
- **最高完整英超胜率：73.7%（V1.6，28胜5平5负、89分）**；V1.3仍是失球最少（30球）和4负的防守基准。
- 版本比较必须使用英超联赛口径。非完整 38 场样本单独标记，不与完整赛季胜率排名混用。

## 历代联赛结果总表

胜率 = 胜场 ÷ 实际已赛英超场次。仅 38 场完整赛季可进入“完整赛季排名”。

| 版本 | 英超场次 | 胜-平-负 | 胜率 | 进失球 | 积分 | 数据级别 |
|---|---:|---:|---:|---:|---:|---|
| V0.1 | 19 | 8-1-10 | 42.1% | 21:26 | 25 | 部分赛季 |
| V0.2 | 23 | 7-3-13 | 30.4% | 29:34 | 24 | 部分赛季 |
| V0.3 | 20 | 13-3-4 | 65.0% | 35:24 | 42 | 部分赛季 |
| V0.4 | 30 | 13-10-7 | 43.3% | 50:39 | 49 | 部分赛季 |
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
| V1.7 | 38 | 25-7-6 | 65.8% | 79:36 | 82 | 完整赛季；Exporter Run45748944770；数据partial/unverified |\n| V1.8 | — | — | — | — | — | D0完成；D1–D3构建中，D4/D5待验证 |

**口径提醒**
- V0.1–V0.4 为未完成赛季样本，只能描述当前已赛成绩，不可与完整 38 场赛季作最终排名。
- V0.5–V1.6 均为 38 场英超赛季；杯赛/欧战场次不混入该表。
- V0.6 的 20-8-10、83:49、68分；V0.7 的 15-8-15、70:58、53分，来自跨版本决策台账及相应版本审计。
- 版本来自不同存档/阵容/赛季状态，结果是描述性历史比较，不是同随机种子受控 A/B。
- V1.5已完成38场英超D5：25-3-10、78分、65.8%；V1.6已完成38场英超D5：28-5-5、89分、73.7%；V1.7由V1.6 D5触发，Build Run163已成功；D5已由Run45748944770完成，D4未单独逐项验收。V1.8由V1.7 D5触发，D0已完成。

## 版本文件清单

所有相对链接均以本目录为基准。

| 版本 | 配方 | 构建请求 | 设计/审计 | 构建报告 | 赛季分析/复核 | FMF |
|---|---|---|---|---|---|---|
| V0.1 | [JSON](V0.1.json) | [JSON](V0.1_BUILD_REQUEST.json) | 见 [README 历史记录](README.md) | 未单独归档 | README/迭代日志历史记录 | 未归档 |
| V0.2 | [JSON](V0.2.json) | [JSON](V0.2_BUILD_REQUEST.json) | 见 [README 历史记录](README.md) | 未单独归档 | [迭代日志](ITERATION_LOG.md) | Actions 历史 |
| V0.3 | [JSON](V0.3.json) | [JSON](V0.3_BUILD_REQUEST.json) | 见 [README 历史记录](README.md) | 未单独归档 | [迭代日志](ITERATION_LOG.md) | Actions 历史 |
| V0.4 | [JSON](V0.4.json) | [JSON](V0.4_BUILD_REQUEST.json) | [角色/PI审计](V0.4_ROLE_PI_AUDIT.md) | 未单独归档 | [赛季分析](V0.4_SEASON_REPORT_ANALYSIS_45399643857.md) | Actions 历史 |
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
| V1.7 | [JSON](V1.7.json) | [JSON](V1.7_BUILD_REQUEST.json) | [设计审计](V1.7_DESIGN_AND_AUDIT.md) | [构建报告](V1.7_BUILD_REPORT.json) | [D5赛季分析](V1.7_SEASON_REPORT_ANALYSIS_45748944770.md) · Run45748944770 | [正式FMF](V1.7.fmf) · 4,504 bytes · SHA-256 `42a7038c4fe89667d0f1f7c7ff1ff74f31633f52f570d0f8b4d4d9c774ee46ab` |\n| V1.8 | [JSON](V1.8.json) | [JSON](V1.8_BUILD_REQUEST.json) | [设计审计](V1.8_DESIGN_AND_AUDIT.md) | 构建中 | D5待验证 | 构建中 |

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
