> 当前迭代候选：V0.8，父版本 V0.7。核心目标为 FM27 有球阶段四后卫 DL–DCL–DCR–DR。V0.7 正常赛季报告显示联赛 15胜8平15负、53分，较 V0.6 少15分；共同36场联赛样本中，场均 xG 下降、对手 xG 上升。V0.8 保留 MCR 中前卫（策应）稳定接应，将 AMC 前场组织核心改为进攻职责并启用更多前插，同时恢复极高节奏、极窄进攻宽度和极多团队逼抢。V0.8 原生 FMF 构建状态以 GitHub Actions 结果为准。

本项目研发利用 FM27 引擎红利机制的高效有球四后卫战术，不以现实足球理论作为限制。每轮按五步执行：读取赛季报告、诊断整体优势与弱点、重构整套配置、生成下一正式 FMF、正常赛季复盘。允许多个相关位置、角色、职责、PI 和 TI 协同升级；逐字段实验和 OOP 四后卫不再是强制门槛。

## 当前项目文件

- ANALYSIS_AND_ITERATION_RULES.md：正式五步研发规则，有球四后卫为核心目标。
- ROLE_PI_AUDIT_TEMPLATE.md：审查完整角色/PI/TI 协同，不是逐字段效能准入表。
- EXTERNAL_ENGINE_BENCHMARK.md：外部引擎研究与榜单基准，按 IP 结构分类。
- ITERATION_LOG.md：唯一版本主线及构建/复盘记录。
- V0.6_REANALYSIS_45554864463.md：V0.6 赛季报告重新分析。
- V0.7.fmf / V0.7_BUILD_REPORT.json：V0.8 唯一父版本及原生构建报告。
- V0.7_REANALYSIS_45564413834.md：V0.7 完整赛季复盘，含共同赛程比较和位置字段质量审计。
- V0.8.fmf：4,352 bytes；SHA-256 `c7480f2c32c55c1b8e8ce3f8724c9ea2c7b2f02fa4e9759b9c6aff8c31d7bb2e`；原生回读通过，游戏内导入待验证。
- V0.8.json / V0.8_DESIGN_AND_AUDIT.md / V0.8_BUILD_REPORT.json：正式配方、设计审查和原生构建报告。
- V0.7_REANALYSIS_45564413834.md：V0.7 正常赛季完整复盘，含共同赛程比较和数据质量审计。
- V0.8.json / V0.8_DESIGN_AND_AUDIT.md：V0.8 升级配方与协同设计审查。
- V0.8_BUILD_REPORT.json：V0.8 原生构建回读结果（构建完成后归档）。
- ../../scripts/build_fm27_snapshot_tactic.py：从指定父版原生快照定点改写的构建器。
- ../../.github/workflows/fm27-v0.8-native-build.yml：V0.8 原生 FMF 构建和 artifact 工作流。

## 版本原则

- V0.1 至 V0.7 全部保留，V0.8 唯一父版本为 V0.7。
- 有球四后卫位置为 DL、DCL、DCR、DR；无球结构可以独立设计。
- 原生 style string 保持空白，FourCC 保持 4c4c554e。
- 原生二进制回读不等于游戏内导入或赛季表现验证。

---

## 历史版本文档（旧规则与结论仅作为历史记录，不作为新流程约束）

## V0.1 基准与问题定位

V0.1：有球 4-2-3-1；无球由 AML/AMC/AMR 转换为 MCL/MC/MCR，前场三人组参与中场压迫。进攻核心角色与结构保留。

已有赛季报告摘要（仅作为 V0.1 的实测基线）：

- 总计 34 场：20 胜、2 平、12 负，65 进球、36 失球；其中混合多个赛事，不能用总战绩代替联赛表现。
- 联赛 19 场：8 胜、1 平、10 负，21 进球、26 失球，25 分。
- 详细球队比赛统计只覆盖 9 场，其中 7 场联赛：联赛样本我方 xG 8.91、对方 xG 12.81；我方绝佳机会 5 次、对方 15 次。
- 9 场详细样本共 24 张黄牌、81 次犯规；传中 309 次、成功 44 次（约 14.2%）；越位 27 次。
- 详细球员比赛报告只恢复 7/21 场，部分球员身份无法识别；压力数据不可用，不能量化逼抢成功率。

**数据解释边界：** 这些数据足以确定 V0.1 的防守机会质量和纪律成本是优先排查方向，但样本不完整，且没有对照组。它们不能单独证明某一条 PI/TI 的因果贡献。V0.2 因此采用少量、可追踪的改动，不宣称已经证明改动必然有效。

## V0.2 本轮改动

### 1. 防线高度与纵深

- `DEFENSIVE_LINE`: `LOWER` → `HIGHER`
- 删除 `DEFENSIVE_LINE_BEHAVIOR=DROP_OFF_MORE`，回到该组的标准/均衡状态。
- 保留 `LINE_OF_ENGAGEMENT=HIGH_PRESS`、`TRIGGER_PRESS=MORE_OFTEN` 与 `DEFENSIVE_TRANSITION=COUNTER_PRESS`。

目的：减少高位逼抢线与较低防线之间的纵向空当，改善中场与后防之间的连接。此为基于 V0.1 xGA/绝佳机会数据提出的战术假设。

### 2. 左后腰的无球职责

- DML 的 `OPDroppingDefensiveMidfielder (D)` 保留。
- `TRIGGER_PRESS`: `MORE_OFTEN` → `LESS_OFTEN`。
- 该位置的 `TACKLING`: `GET_STUCK_IN` → `EASE_OFF_TACKLES`。

目的：让左后腰更稳定地留在保护区域，减少主动上抢造成的中路空当；右后腰仍保留原有 Pressing Defensive Midfielder 职责。

### 3. 后场六人的对抗控制

DL、DCL、DCR、DR、DML、DMR 的 OOP `TACKLING` 由 `GET_STUCK_IN` 改为 `EASE_OFF_TACKLES`。前场 AML/AMC/AMR/ST 的无球积极对抗 PI 保留，GK 原有谨慎铲抢保留。

目的：针对 9 场样本 24 张黄牌和 81 次犯规，降低后场不必要的对抗成本，同时保留前场压迫侵略性。当前目录已确认上述六个 OOP 角色/位置/duty 对 `EASE_OFF_TACKLES` 的 PI 权限为可编辑。

## 明确保留的核心

- 有球 4-2-3-1 的 11 个位置、角色和职责全部保留。
- 无球 4-2-3-0/中场三人组回撤压迫的角色转换全部保留。
- 前场 False Nine、Second Striker、Inside Forward、Wide Forward 组合保留。
- 进攻 TI（节奏、传球、传入空当、宽度、推进、反击等）不在本轮调整。
- Gegenpress 是当前原生风格标识/序列化选择；战术具体配置由配方显式写入。

## V0.2 后续评估指标

拿到 V0.2 的赛季/比赛报告后，与 V0.1 使用相同口径对比：

1. 对手 xGA、绝佳机会、射正：检查防守机会质量是否下降。
2. 抢断成功率及防守机会质量：检查后场防守行为是否改善；犯规、黄牌、红牌不纳入后续评估。
3. 我方 xG、绝佳机会、禁区触球/射门：检查进攻产量是否保持。
4. 越位、传中成功率：作为保留进攻结构的监测项，本轮不主动针对它们改配置。
5. 若样本覆盖不一致，必须按共同比赛范围或每场均值比较，不得直接比较不等量总数。

## 后续迭代规则

**分析范围更正：** 后续赛季分析不统计、不分析、不验证犯规、黄牌或红牌；不将其作为版本对照或战术调整依据。历史记录中的相关数据仅保留为当时报告原貌，不再作为后续验证指标。

- V0.1 永久保留为基准，不覆盖。
- 每轮只维护一条 V0.x 迭代主线，不另开无关战术。
- 每次版本必须记录：父版本、完整配方、变更字段、对应数据问题、预期效果、构建报告及之后的实测结果。
- D3 报告只证明 FMF 生成与独立回读；不能冒充游戏内比赛表现验证。


## V0.2 原生构建记录

- GitHub Actions： [FM27 Tactic Build #135](https://github.com/eslaulau/fm-ta/actions/runs/45377758101)
- 构建请求 commit：`696b4db67f65c14cc765855e9cea36c44301046a`
- 结果：成功；catalog-backed preflight、原生 FMF 生成、D3 独立回读和 artifact 上传全部通过。
- Artifact：`FM27_FM27_EngineDividend_4Back_V0.2_20261124_run135`
- FMF：`FM27_EngineDividend_4Back_V0.2_20261124_run135.fmf`
- 大小：3,806 bytes
- SHA-256：`396a46969c6d694d0fd166a880c27cdbff482862728c9a5a196d1b9ef44738e6`
- 回读：22/22 阶段完整；22/22 PI 非空；设计表与回读表逐项一致；FMF 容器、成员校验、TAC、TI 向量、原生风格字段均通过。
- 报告状态：`offline_binary_roundtrip_verified_not_game_import_verified`。这代表 D3 原生文件生成与独立回读成功，不代表游戏内导入或比赛表现已经验证。


## V0.2 赛季报告（2026-11-24）
- 已读取 [Exporter run 45381925241](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/FM27_EngineDividend_4Back_V0.2/45381925241)，用户确认报告使用 V0.2。
- 联赛 23 场：7胜3平13负，29-34，24 分；球队详细比赛统计仅覆盖 4 场联赛。
- 4 场详细联赛样本全部失利，对手 xG 9.52、绝佳机会 17；球员联赛赛季汇总为 29 球、32.35 xG、27 助攻、31.05 xA。
- 球员详细比赛报告 94 条均未识别身份，评分缺失；FM27 27.0.1 build 使用借用 schema，球队比赛统计覆盖不足。完整限制和 V0.3 待研究方向见 [ITERATION_LOG.md](ITERATION_LOG.md)。
- **当前决定：不仓促构建 V0.3。** 先补充球队逐场统计与可识别球员数据，再针对防线纵深做小变量实验。


### 共同赛程对照补充
按 19 场完全相同的联赛赛程逐场匹配：V0.1 为 8-1-10、21:26、25 分；V0.2 为 7-3-9、25:21、24 分。V0.2 净胜球改善 9，但积分少 1。V0.2 随后新增 4 场联赛全部失利（4:13）；这 4 场对手 xG 9.52、绝佳机会 17。详细分析及限制见 [ITERATION_LOG.md](ITERATION_LOG.md)。


## 外部研究与排行榜交叉基准

后续每轮战术分析必须联网检索当前 FM27 build 的引擎机制研究、受控战术榜单、社区实测库和战术结构分析工具。必须区分测试协议与版本，单独筛选无球阶段真实四后卫；三中卫/五后卫高排名仅用于寻找候选机制，不得混入四后卫成绩基准。来源分级、筛选和归档规范见 [ANALYSIS_AND_ITERATION_RULES.md](ANALYSIS_AND_ITERATION_RULES.md)，动态快照见 [EXTERNAL_ENGINE_BENCHMARK.md](EXTERNAL_ENGINE_BENCHMARK.md)。


## V0.3 单变量实验（2026-11-24）
- [V0.3 配方](V0.3.json)：以 V0.2 为父版本，仅将 DML 无球 `TRIGGER_PRESS` 从 `LESS_OFTEN` 改为 `MORE_OFTEN`。
- [V0.3 构建请求](../../build_requests/FM27_EngineDividend_4Back_V0.3_20261124.json)。
- 本轮不是宣称已验证的性能升级，而是依据 V0.2 防守机会质量风险及外部四后卫 DM 压迫候选，设计的单变量实验。其余配置全部保持不变。
- 实测要求：至少 8–10 场同口径球队详细统计，记录实际 FM27 build；以对手 xG/绝佳机会/射门和我方 xG/绝佳机会为主，不分析犯规、黄牌、红牌。
- 当前外部研究快照与证据分级见 [EXTERNAL_ENGINE_BENCHMARK.md](EXTERNAL_ENGINE_BENCHMARK.md)；完整决策见 [ITERATION_LOG.md](ITERATION_LOG.md)。


### V0.3 构建记录
- GitHub Actions：[FM27 Tactic Build #136](https://github.com/eslaulau/fm-ta/actions/runs/45388048044) 成功。
- Artifact：`FM27_FM27_EngineDividend_4Back_V0.3_20261124_run136`。
- FMF：`FM27_EngineDividend_4Back_V0.3_20261124_run136.fmf`（3,806 bytes）。
- SHA-256：`fe17432d0f2fa5bdc803c179ff7a861effc41c58f4fcc52a30f09ff8188a5aff`。
- D3 独立回读全部通过；尚未验证游戏内导入和比赛表现。


## V0.3 赛季报告（Exporter run 45391011796）
- 用户确认报告使用 V0.3；存档 build `27.0.1+2494687`，日期 2027-01-08。
- 联赛 20 场：**13胜3平4负，35:24，42分**。
- 与 V0.2 相同的 20 场联赛逐场匹配：V0.2 为 7胜3平10负、25:22、24分；V0.3 为 13胜3平4负、35:24、42分。V0.3 是明显正向信号，但不是相同随机条件的受控 A/B。
- 详细球队统计覆盖 6/20 场联赛；球员逐场报告 93 条全部未识别。27.0.1 parser build 未上游注册，schema 6 借用 27.0.0 布局，114/114 总量核对通过但覆盖不完整。
- 决策：保留 V0.3 DML OOP `TRIGGER_PRESS=MORE_OFTEN`、高防线及其余配置；本轮不强行生成 V0.4。补足 8–10 场详细统计或做同存档原生引擎 A/B 后再确定下一变量。完整分析见 [ITERATION_LOG.md](ITERATION_LOG.md)。



## V0.4 重做版（2026-11-24）
- [V0.4 配方](V0.4.json)：父版本 V0.3；旧版迭代报告已撤下，本次重新审查后复用版本号。
- [V0.4 角色与 PI 完整审查](V0.4_ROLE_PI_AUDIT.md)：11 个位置 IP/OOP 矩阵、全部 PI、组合冲突和变更决策均已完成。
- TI：PASS_RECEPTION 改为 PASS_TO_FEET；删除显式 LOW_CROSSES（原生默认混合传中）；DEFENSIVE_LINE 改为 LOWER。
- 角色/PI：DL InsideFullBack/D 改 FullBack/S 并取消 SIT_NARROWER；DCR OverlappingCentreBack/S 改 CentreBack/D 并移除 SHORTER；AMC 移除 DRIBBLE_MORE，保留游弋。
- [FM27 Tactic Build #139](https://github.com/eslaulau/fm-ta/actions/runs/45396091251) 成功；[构建 Artifact](https://github.com/eslaulau/fm-ta/actions/runs/45396091251/artifacts/14920777363)。FMF 3,758 bytes，SHA-256：`92aaa02c46a8aec76107274a2735548a343c2d8aa72f092cf179e15f9915791d`。
- D3 独立回读 8/8 检查、22/22 阶段角色/PI 回读通过；游戏内导入和比赛效果待验证。


## V0.4 run139 赛季报告分析（Exporter 45399643857）
- [完整报告分析](V0.4_SEASON_REPORT_ANALYSIS_45399643857.md)。用户确认使用 V0.4 run139。
- 联赛 30 场：13胜10平7负，50:39，49分；与 V0.3 的 20 场共同赛程比较，V0.4 为 8胜7平5负、31分（不同存档，不是受控 A/B）。
- 球队详细统计覆盖 5/30 场联赛；球员逐场 94 条全部未识别身份；球员赛季汇总可用但不能归因到角色。
- 传中成功率 15.76%（赛季汇总），越位 130 次/30 场；较 V0.3 的每场传中成功和越位仅呈小幅改善，不能作因果判断。
- 决策：本轮完成分析与角色/PI审查，但不创建 V0.5，现有数据不足以定位单一负收益配置。优先候选实验为仅将防线 LOWER→HIGHER，其余 V0.4 锁定；尚不落配方。


## V0.5 基准切换（用户确认，2026-11-25）
- [V0.5 原生基准](V0.5_BASELINE.md)：当前有效战术基准为 `V21_Leaderboard_TeamInstructions(1).fmf`，SHA-256：`e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`；赛季报告已完成分析归档。
- **V0.5 以 V21 原生快照为底稿，不继承 V0.4。** 用户已持有该战术并将自行完成赛季测试；收到其报告入库通知后，从 V0.5 基准分析并决定下一次迭代，后续版本沿用 V0.6、V0.7……顺序。
- 可修改项包括球队指令、个人指令、位置/位置转换、角色、职责和心态；**唯一锁定项是原生风格字段：style string 持续为空，原始 FourCC `4c4c554e` 原样保留**。不得为了迁就现有命名风格模板而更改。
- 位置、角色、职责和心态不是永久锁定项；每轮按数据与完整配置审查决定保留或调整。位置改动必须重新核对无球真实四后卫结构。
- 此前 V0.4 赛季分析提出的 “V0.5 只把防线 LOWER→HIGHER” 是旧计划，已由本次版本谱系切换取代，不再作为 V0.5 的构建指令。


## V0.5 赛季报告（Exporter run 45540803100）

- [完整赛季分析](V0.5_SEASON_REPORT_ANALYSIS_45540803100.md)：用户确认使用 V0.5；FM27 build 27.1.1+2511875；联赛38场完整球队统计覆盖。
- [角色/职责/PI专项审查](V0.5_ROLE_PI_AUDIT_45540803100.md)：22/22 IP/OOP 角色/职责/位置组合通过 catalog 资格检查；35/35 显式 PI 均可编辑；组合审查完成。
- 联赛：20胜9平9负，75:43，69分（2.03分/场）；xG72.92、xGA44.12；75次绝佳机会，对手29次；控球率41.42%。
- 球员逐场报告：876次有效出场中786次识别（89.7%），但位置语义除GK外仅为候选、role_code 未解码，不把球员表现归因到具体战术角色。
- build 27.1.1 未被 fmsave 0.14.3 upstream 注册；使用借用 schema-6 布局，数据交叉核验良好但整体仍标记 partial/unverified；3个正式比赛进球差异未归属。
- **版本决策：不创建 V0.6。** 当前没有一条 TI/PI/角色/职责/位置可被数据明确指认成负收益；传中完成率与非胜场转化偏差暂列待研究。V0.5 全部配置保留。
- 最新 27.1.1 外部基准见 [EXTERNAL_ENGINE_BENCHMARK.md](EXTERNAL_ENGINE_BENCHMARK.md)：当前 metaFM 前12名均为 OOP 五后卫，不能作为真实四后卫成绩基准。
- 状态：COMPLETE（报告分析和配置审查完成；不代表 fmsave 目标 build 已 upstream 注册，也不代表外部不同测试协议可以直接比较）。



## V0.6 迭代（2026-11-25，V0.5 数据驱动修订）

- 父版本：V0.5 原始 FMF，SHA-256 e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257。
- 依据：Exporter run 45540803100 的 38 场联赛统计。全季 1,139 次传中、156 次成功（13.7%）；胜场/平局/失利传中成功率分别为 15.9%/13.0%/9.9%。主/客场 xG 为 2.11/1.72，对手 xG 为 1.02/1.31。
- 仅改三个 PI：DR WingBack Support 增加传中目标后点；DL FullBack Support 增加传中目标后点；ST ChannelForward Attack 的禁区进攻方向由前点改为后点。
- 保留全部位置、角色、职责、其他 PI、20 条 TI、心态 4、空白 style string、FourCC 4c4c554e；无球最后防线仍为 DL–DCL–DCR–DR。
- 新 FMF 4,236 bytes，SHA-256 97e8ac91ce369024745905d5e22c9a29167c85faad9b3454a30920e23f67cf0c。原生回读通过，游戏内导入和比赛表现未验证。
- 撤回说明：此前以外部 META 套件为模板的大幅 V0.6 改写版（SHA-256 58aa50060888233b1592b291a53b947d9ea9fb9b592dea8482d916ba8349f568）已撤回，不再是有效候选。
- 验收：同 build、尽可能相近阵容进行至少 10–15 场详细比赛，观察传中成功率、尝试量、xG、射门、射正、绝佳机会及对手 xG/绝佳机会。若传中完成率上升但 xG/绝佳机会不升，不视为成功。纪律数据排除。
