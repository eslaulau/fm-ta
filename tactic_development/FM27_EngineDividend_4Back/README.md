> **2026-11-26｜项目最高目标与规则执行入口更新**
>
> - 唯一最高目标：联赛 PPG ≥ 2.85（38 场至少 109 分）。项目规则只在本目录生效。
> - 正式规则：[PROJECT_RULES.md](PROJECT_RULES.md)；机器策略：[PPG_TARGET_POLICY.json](PPG_TARGET_POLICY.json)。
> - 项目审计是强制门禁，构建执行通道不设单一限制：[build_project_tactic.py](build_project_tactic.py) 是标准入口；若当前执行环境不能调用它，可先运行同一 [validate_project_iteration.py](validate_project_iteration.py)，再用本仓库离线原生生成器完成权限校验、FMF生成与独立回读。不得因 GitHub/聊天接口不能远程执行 Python 而停止迭代。具体执行政策见 [GENERATION_EXECUTION_POLICY.md](GENERATION_EXECUTION_POLICY.md)。审计失败绝不生成。
> - 配方、审计文件和生成输出均限定在项目目录；项目自动化测试见 [test_project_iteration_gate.py](test_project_iteration_gate.py)。FMF生成可由本地工作区/附件工作区/合规runner执行，执行通道不能代替或绕过项目审计。
> - 每轮设计审计使用 [ITERATION_DESIGN_AUDIT_TEMPLATE.md](ITERATION_DESIGN_AUDIT_TEMPLATE.md)；项目规则与执行命令见 [PROJECT_RULES.md](PROJECT_RULES.md)。
> - FM-TA 仅作为 FMF 工具。本次及后续不得修改其通用导出器、生成器规则或通用工作流来承载本项目规则。
> - 历史版本成绩保持原样；不追溯改写旧赛季为 PPG 2.85 目标下的成绩。

---

# FM27 引擎红利四后卫

- **连续研发闭环（最高执行入口）：** [UPGRADE_GATE.md](UPGRADE_GATE.md)。用户提交赛季报告即默认启动完整分析、历史总账联动、引擎红利研究、唯一整体战术升级和FMF交付，不再把分析与升级拆开。

## 项目统一入口（原始战术 V0.5｜当前候选 V1.9 R2）

- **研发规则（最高优先级）：** IP唯一硬约束为后场DL/DCL/DCR/DR四个位置槽，不固定4-2-3-1或任何IP数字阵型；其余IP位置与全部OOP结构完全开放。每轮只设计、输出、构建一个完整方案，不提供多套候选战术，不把局部单变量调整当作默认升级。详见 [正式研发规则](ANALYSIS_AND_ITERATION_RULES.md)。
- **唯一版本总目录：** [VERSION_CATALOG.md](VERSION_CATALOG.md)（所有版本成绩、配方、构建请求、设计审计、构建报告、FMF 与赛季分析索引）。
- **唯一权威研发总账（决策 + 完整历史配置）：** [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)。该文件现已合并V0.5–V1.8完整配置、赛季表现、11槽×IP/OOP角色/职责/PI、TI/心态和逐代差异；以后所有赛季反馈与迭代决策只更新这一份总账。

- **赛季分析到战术升级追踪模板：** [SEASON_TO_TACTIC_TRACEABILITY_TEMPLATE.md](SEASON_TO_TACTIC_TRACEABILITY_TEMPLATE.md)。每个问题必须贯通赛季数据、历史版本、引擎机制、配置决策、收益代价和下一轮D5验证。

- **原始数据来源：** [SOURCE_REGISTER.md](SOURCE_REGISTER.md)（Exporter Run ID、原始报告 URL、版本映射及缺失来源登记）。
- **原始战术：** [V0.5 原生基准](V0.5_BASELINE.md)，来源为 V21 原生快照；本项目全部历史追踪从 V0.5 开始。
- **当前候选：** [V1.9 R2 配方](V1.9_REDESIGN_R2.json) · [设计审计](V1.9_REDESIGN_R2_DESIGN_AND_AUDIT.md) · [历史总账复核纠正记录](V1.9_REDESIGN_R2_HISTORICAL_REAUDIT_REQUIRED.md) · [Run169构建](https://github.com/eslaulau/fm-ta/actions/runs/45760556137)。D0历史总账复核现已完成，D1-D3技术构建通过；R2可进入D4游戏内核验，D5仍待完整赛季。R2仍是高风险待验证候选，不是已验证升级。V1.8仍是最近完成D5的研发基准。V1.8 D5分析见 [赛季报告](V1.8_SEASON_REPORT_ANALYSIS_45753659141.md)；V1.8联赛21-9-8、72分，防守机会指标未达标。
- **历代最佳：** V1.6以28胜5平5负、89分、73.7%胜率刷新完整英超赛季纪录；V1.3仍是失球最少（30）且仅4负的防守基准。
- **辅助版本执行记录：** [ITERATION_LOG.md](ITERATION_LOG.md)；**唯一权威决策与完整历史配置总账：** [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)。
- **归档约束：** 此后本项目的版本文件全部放在当前目录；不再放进仓库根目录的通用 `build_requests/`。


本目录维护一个持续进行的数据驱动战术研发项目，而非只负责输出一个 FMF 文件。正式循环是：先读取跨版本指令决策台账和唯一父版本 → 读取用户确认的赛季报告 → 数据质量审计与整体诊断 → 对每项角色/职责/PI/TI 判定继承、暂留、替换或待验证 → 外部引擎机制交叉研究 → IP/OOP 协同设计 → D3 原生 FMF 构建 → D4 游戏内导入/显示确认 → D5 比赛/赛季效果复盘 → 回写决策台账并进入下一轮。

## 当前项目文件

- ANALYSIS_AND_ITERATION_RULES.md：正式研发、数据口径与 D0–D5 规则。
- ROLE_PI_AUDIT_TEMPLATE.md：审查单轮完整角色/PI/TI 协同、数据归因边界与验收阶段。
- TACTIC_INSTRUCTION_DECISION_LEDGER.md：跨版本指令决策台账，逐项追踪 IP/OOP 角色、职责、PI、TI、结构组合的版本沿革、证据、保留/替换状态与下一轮验证指标。
- 阵型级角色约束：边中卫系列与套上中卫只适用于三中卫外侧槽位；生成器 preflight 已增加阵型检查，历史 V0.9/V1.0 的非法角色条目见迭代日志。
- EXTERNAL_ENGINE_BENCHMARK.md：外部引擎研究与榜单基准，按 IP 结构和 build 区分。
- ITERATION_LOG.md：唯一版本主线、唯一父版本和构建/复盘记录。
- V0.8_SEASON_REPORT_ANALYSIS_45570292427.md：V0.8 正式赛季报告复核与 V0.9 草案/正式版差异记录。
- V0.9.json / V0.9_DESIGN_AND_AUDIT.md：正式 V0.9 综合版 recipe 与审查。
- V0.9_SEASON_REPORT_ANALYSIS_45584292488.md：V0.9 正式使用赛季的完整数据复核和下一轮诊断。
- V1.0.json / V1.0_DESIGN_AND_AUDIT.md：基于 V0.9 赛季复盘的下一版完整配方与设计审计。
- V1.0_SEASON_REPORT_ANALYSIS_45602694823.md：V1.0 正式赛季复盘，记录英超 87 分、进攻/防守机会质量改善、客场推进差距及 DCL 角色一致性警报。
- V1.0 正式 FMF：Run 144 artifact `15009749134`，FMF 4,400 bytes，SHA-256 `31abf4454e3d4c5e816a2221b669a2e5b31507bdcfa280c059007359f7eab666`；原始文件保留，配方结构含四后卫不可用的 DCL 边中卫，已由 V1.1 修正。
- V1.1 正式 FMF：Run 145 artifact `15018939550`，FMF 4,544 bytes，SHA-256 `b4d757cca5a849b771fc18683775234e2c3d445cfb581d961a5524afdfaf40dc`；同次 report SHA-256 `8636e20931373d2915578970e9adcbe8dce5de31a1bf8abf3e8df9b2e7223101`；本对话提供 FMF、同次报告与完整 artifact ZIP。
- V0.9.fmf：Run 142 正式 V0.9 原生 FMF；同次原始 report 保存在 Actions artifact `15005190567`，SHA-256 记录于 `V0.9_BUILD_REPORT.json`。
- V0.9_BUILD_REPORT.json：Run 142 的版本与哈希摘要。
- V0.9_ST_ONLY_DRAFT_SUPERSEDED_run3.fmf：首轮单改 ST 草案历史 FMF；Run 3 同次 report 保存在 Actions artifact `15002228385`；已取代，不是正式 V0.9。
- V0.8.fmf：4,352 bytes；SHA-256 c7480f2c32c55c1b8e8ce3f8724c9ea2c7b2f02fa4e9759b9c6aff8c31d7bb2e；Run 142 唯一父快照。

- V1.9_REDESIGN.json / V1.9_REDESIGN_DESIGN_AND_AUDIT.md / V1.9_REDESIGN_BUILD_REPORT_SUMMARY.json：IP 4-3-3 DM + OOP 4-1-4-1 的历史R1重设计配方、审计和Run167构建摘要；D1-D3技术构建通过；R1为历史候选，未完成D4/D5；R2已完成历史D0复核并作为当前高风险待验证候选。

## 项目硬约束与开放项

- 唯一战术结构硬约束：IP后场四个位置槽为DL、DCL、DCR、DR；不固定IP为4-2-3-1或任何其他数字阵型，阵型其余部分完全开放；阵型级角色适用条件必须同时通过。
- 四后卫角色、职责、PI 完全开放；OOP 阵型、位置、角色、职责、PI 也完全开放。
- 每轮只设计、输出和构建一个完整方案；允许该方案内多个位置、角色、职责、PI、TI及心态协同调整，不强制单变量实验。OOP结构完全开放。
- 每个阶段对象必须有 PI 数组，但可为空；只对实际选择的 PI 核验原生权限，禁止填充无意义 PI。
- V0.9 使用 V0.8 原生父快照作为格式载体；不是空白 FMF。所有 22 个 IP/OOP 阶段配置由 recipe 重建，而共享 TI 向量仅显式覆盖四项，其余继承父快照。
- 空 style string 与 FourCC 4c4c554e 是当前父快照的格式兼容身份，不是引擎效果或战术性能规则。
- 纪律数据（犯规、黄牌、红牌）不进入战术评价。
- 每个版本唯一对应父版本 SHA、recipe SHA、Actions run/artifact、FMF SHA 和同次 report SHA；标签复用必须增加唯一草案/修订/run 标识。
- 每代战术必须先读取跨版本指令决策台账；赛季复盘后回写每条指令的沿革、观察证据、去留状态和下次验证目标。

D3 原生构建通过只说明文件能生成并独立回读；D4 游戏内显示验证、D5 比赛/赛季表现验证必须分别有证据，不得混淆。

---

## 项目原始战术｜V0.5

V0.5 是本项目唯一原始战术基准，来源为 V21 原生快照，不继承任何更早版本。后续所有赛季分析、配置筛选、战术升级和版本比较均从 V0.5 开始；V0.5 之前的资料不属于本项目研发谱系。

- [V0.5 原生基准与完整配置](V0.5_BASELINE.md)
- [V0.5 赛季报告分析](V0.5_SEASON_REPORT_ANALYSIS_45540803100.md)
- [V0.5 角色/PI 审查](V0.5_ROLE_PI_AUDIT_45540803100.md)

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


## V0.8 赛季复盘（Exporter run 45570292427）

- 用户确认本报告使用 V0.8；正式比赛 65 场，球队与球员逐场详细报告均为 65/65。
- 英超 38 场：19胜9平10负、79:46、66分；xG82.07、xGA44.01。相较 V0.7 的 53 分明显反弹，33 场共同联赛对阵中 V0.8 为 17胜7平9负，V0.7 为 11胜8平14负。
- 进攻推进恢复，但平局与败场 19 场累计 xG35.23 仅进21球；ST 位置 12球/19.63 xG，是本轮优先审查点。
- 角色码已按原生 79 角色目录解码出 10 种实际角色码；位置语义 10/10 通过原生目录核验。仍有 10/1,022 出场身份未解析，693 条历史 role_code 缺失；build 27.1.1+2511875 未被 fmsave 0.14.3 上游登记，schema-6 使用借用布局。
- 完整复盘见 [V0.8_SEASON_REPORT_ANALYSIS_45570292427.md](V0.8_SEASON_REPORT_ANALYSIS_45570292427.md)。

## 正式 V0.9｜整套有球四后卫协同升级（Run 142）

- 父版本 V0.8 SHA-256：`c7480f2c32c55c1b8e8ce3f8724c9ea2c7b2f02fa4e9759b9c6aff8c31d7bb2e`。
- IP 四后场：DL 内收型边后卫（防守）；DCL 宽中卫（防守）；DCR 出球中卫（防守）；DR 翼卫（进攻）。
- 中前场：MCR 中前卫（策应）、MCL 肋部中场（进攻）、AMR/AML 组织型边锋（策应）、AMC 前场组织核心（进攻）、ST 抢点前锋（进攻）。
- OOP 的 11 个位置/角色/职责/PI 本轮暂时保持 V0.8；这只是本轮策略，不是规则锁定。
- TI：比赛节奏极高→较高、进攻宽度极窄→较窄、防线极低→较低、团队逼抢极多→较多；其他 TI 与心态沿用 V0.8。
- V0.8 二次诊断：[赛季分析](V0.8_SEASON_REPORT_ANALYSIS_45570292427.md)；[V0.9 设计审计](V0.9_DESIGN_AND_AUDIT.md)。
- 构建： [FM27 Tactic Build run 142](https://github.com/eslaulau/fm-ta/actions/runs/45576936835)，artifact `15005190567`。FMF 4,400 bytes，SHA-256 `5dc33a05f032345ca9c674b02d48e7619b32303e3e0eb54930598941df3456a1`。
- D3 原生读回通过；游戏内导入和比赛引擎表现尚未验证。


---

## 当前版本｜V1.5（Run 149）

- 最新版本：[V1.5 配方](V1.5.json)、[V1.5 设计与完整差异审计](V1.5_DESIGN_AND_AUDIT.md)、[V1.5 构建摘要](V1.5_BUILD_REPORT.json)。
- 父版本：V1.4 / Run148；父 FMF SHA-256 `5bce6f33f70ec9aa8627e18cc866b51f5cd79b99e2e52ba667087b4e142e92bc`。
- V1.4 正式赛季报告：[Exporter Run 45727738275](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45727738275)。英超38场：27胜2平9负、101:53、83分；xG92.62/xGA43.46；我方/对手绝佳机会100/39。进攻产量上升，但失球、xGA和客场表现风险明显增加。
- V1.5 战术迭代：心态 `4→3`；防线高度 `DEFAULT→LOWER`；保留较高比赛节奏、较宽进攻宽度、高位防守介入线和较多团队逼抢。IP 四后场 DL/DCL/DCR/DR 不变；22个阶段位置/角色/职责/PI均继承 V1.4。
- Build Run149：[Actions](https://github.com/eslaulau/fm-ta/actions/runs/45729221041)，成功；artifact ID `15076425618`。FMF 4,504 bytes，SHA-256 `c4d68446a7da3e4857bc12dc1a2a9fa2b0c34341ec9653c77b08ce2ccb951711`；same-run report SHA-256 `b8a9c32e82c84eee2847c3328c25e4d569aedad4c64191cd4debe34be587a07f`。
- D3 独立回读 8/8 通过，22/22阶段一致；状态为 `offline_binary_roundtrip_verified_not_game_import_verified`。**D4 游戏内导入和 D5 比赛效果仍待验证**，不得将构建成功表述为实战验证成功。
- V1.4 完整数据复盘：[V1.4_SEASON_REPORT_ANALYSIS_45727738275.md](V1.4_SEASON_REPORT_ANALYSIS_45727738275.md)；V1.5 四类决策与 D0–D5 状态见 [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)。



---

## V1.6 正式赛季复盘｜Exporter Run 45744550318
- 用户确认本报告使用V1.6；源存档SHA-256 `c91d8caa2e9a9030c784efb6b627a06d1098ac71ff48887843a68cd5386a8c75`；FM27 build 27.1.1+2511875。
- 英超38场：**28胜5平5负、87:37、89分、73.7%胜率**，刷新本项目完整赛季胜率/积分纪录。
- xG75.54/xGA46.33；我方/对手绝佳机会63/40；主场17-1-1、客场11-4-4；客场xGA26.55，对手绝佳机会22。
- 实际失球低于xGA 9.33、进球高于xG 11.46；结果优秀，但机会质量提示防守风险，不能只看实际失球。
- 完整分析：[V1.6_SEASON_REPORT_ANALYSIS_45744550318.md](V1.6_SEASON_REPORT_ANALYSIS_45744550318.md)。

## V1.7 设计迭代｜父版 V1.6
- 目标：保留V1.6进攻骨架和心态/TI，回调OOP双后腰同时积极逼抢的结构风险。
- OOP DML：逼抢后腰→屏障后腰；OOP DMR Trigger Press MORE_OFTEN→LESS_OFTEN，Tackle Harder保留。
- 其余20阶段完全继承；IP四后场DL/DCL/DCR/DR保持。
- 四类决策和完整22阶段矩阵见[V1.7_DESIGN_AND_AUDIT.md](V1.7_DESIGN_AND_AUDIT.md)。
- V1.7 D3构建：[Run163](https://github.com/eslaulau/fm-ta/actions/runs/45745327285)成功；Artifact ID `15082962594`；正式 FMF 已归档：[V1.7.fmf](V1.7.fmf)，4,504 bytes，SHA-256 `42a7038c4fe89667d0f1f7c7ff1ff74f31633f52f570d0f8b4d4d9c774ee46ab`；8/8回读通过、22/22阶段一致。D5已由Exporter Run45748944770完成，英超25胜7平6负、82分；分析见 [V1.7赛季报告](V1.7_SEASON_REPORT_ANALYSIS_45748944770.md)。D4未单独逐项截图验收；构建报告：[V1.7_BUILD_REPORT.json](V1.7_BUILD_REPORT.json)。


## V1.8 设计迭代｜父版 V1.7

- 核心约束：IP四后场DL/DCL/DCR/DR完全保留；IP 11槽角色、职责、PI均继承V1.7。
- OOP由4-2-1-2-1改为无锋5-2-3：WBL/DCL/DC/DCR/WBR五后卫、DML/DMR双后腰、AML/AMC/AMR前场三人组。
- 结构依据：FM27 27.1.1 metaFM高排名样本反复出现OOP 5-2-3；本队V1.7数据也显示客场防守仍有优化空间。外部测试只作候选方向，不等于本队效果保证。
- D1–D3： [Run164](https://github.com/eslaulau/fm-ta/actions/runs/45750563671)成功；8/8检查通过，22/22阶段精确回读。
- FMF：4,616 bytes；SHA-256 `51e94c684c66ce016950d93f2619a40086820e7a9dcf792b7251d4ac67fa4e72`；构建摘要见 [V1.8_BUILD_REPORT_SUMMARY.json](V1.8_BUILD_REPORT_SUMMARY.json)。
- D3不代表游戏内导入或比赛验证；D4/D5待完成。

 
## 当前研发版本｜V1.9重新执行版R2（Run169）

- 唯一父版本：V1.8 / Run45753659141。
- IP：4-1-2-1-2 Diamond；OOP：5-2-3；IP后场四槽DL/DCL/DCR/DR。
- [配方](V1.9_REDESIGN_R2.json) · [构建请求](V1.9_REDESIGN_R2_BUILD_REQUEST.json) · [设计审计](V1.9_REDESIGN_R2_DESIGN_AND_AUDIT.md) · [赛季追踪矩阵](V1.9_REDESIGN_R2_SEASON_TO_TACTIC_TRACEABILITY_45753659141.md) · [D3构建摘要](V1.9_REDESIGN_R2_BUILD_REPORT_SUMMARY.json)。
- [GitHub Actions Run169](https://github.com/eslaulau/fm-ta/actions/runs/45760556137)：D1-D3技术检查通过，8/8检查、22/22阶段精确回读；D0历史复核现已完成；R2可进入D4游戏内核验，但尚非已验证升级。详见[历史复核记录](V1.9_REDESIGN_R2_HISTORICAL_REAUDIT_REQUIRED.md)及唯一权威总账。FMF SHA-256 `b199063dec9f8745d692ba2abcb78664bdbaa41184d8ea03455afaf6fefea4a5`。
- D4游戏内导入和D5赛季表现尚未验证。Run167保留为历史R1，不覆盖、不宣称比赛失败。


## 构建执行原则（2026-11-26 修订）

项目门禁严格，但不把某一种工具调用方式当作唯一生成通道。助手不得再以“GitHub 工具只能读取/写入、不能执行项目脚本”作为停止迭代的理由。必须继续使用当前可用的工作区或离线原生生成器完成构建；离线路径仍先运行项目审计，再进行原生权限检查、FMF生成和独立回读。只有真实输入缺失或所有执行路径均出现可复现错误时，才报告具体阻断。详见 [GENERATION_EXECUTION_POLICY.md](GENERATION_EXECUTION_POLICY.md)。


## 最高优先级迭代规则：每轮从 V0.5 重生

- V0.5 原始 FMF SHA-256：`e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。
- 每一轮都以该 V0.5 文件作为唯一重生基准；V0.6 及之后版本只作为历史实验、赛季结果和机制经验来源，不自动成为父版本。
- 历史有效经验经过证据审查后可以迁移；每轮必须重新设计完整战术，不是简单复制 V0.5，也不是从最近版本接着改。
- 生成门禁已强制要求父版本 V0.5 及其固定 SHA-256；任何 V1.x 父版均应拒绝。详细规则见 [PROJECT_RULES.md](PROJECT_RULES.md) 第 11 节和 [UPGRADE_GATE.md](UPGRADE_GATE.md) 第 13 节。
