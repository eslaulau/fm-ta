# FM27 引擎红利四后卫战术迭代档案

本目录只记录同一条战术开发线：**FM27 引擎红利四后卫 V0.1 → V0.2 → 后续版本**。V0.1 是本项目唯一基准；本次 V0.2 是用户明确授权的定向升级，不引用仓库内其他战术作为设计样板。

## 版本文件

- [版本迭代记录](ITERATION_LOG.md)：逐版本记录父子关系、实际变更字段、设计依据、构建产物与实测状态。以后每次战术版本更新都必须追加记录。

- [V0.1 原始配方](V0.1.json)：从原始构建请求逐字保留。
- [V0.2 升级配方](V0.2.json)：本次唯一候选版本。
- [V0.2 构建请求](../../build_requests/FM27_EngineDividend_4Back_V0.2_20261124.json)：正式云端 FMF 构建入口。

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
2. 黄牌、犯规、抢断成功率：检查后场对抗控制是否降低纪律成本且未损害防守。
3. 我方 xG、绝佳机会、禁区触球/射门：检查进攻产量是否保持。
4. 越位、传中成功率：作为保留进攻结构的监测项，本轮不主动针对它们改配置。
5. 若样本覆盖不一致，必须按共同比赛范围或每场均值比较，不得直接比较不等量总数。

## 后续迭代规则

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
