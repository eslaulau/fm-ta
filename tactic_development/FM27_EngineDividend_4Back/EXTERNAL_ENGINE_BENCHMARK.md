# FM27 引擎红利四后卫｜外部研究与战术榜单基准库

本文件记录外部引擎机制研究、战术排行榜、社区测试库和候选战术。它是动态研究档案，不是把不同网站数据拼成的统一总榜。每次更新必须追加日期快照，保留历史数值。

## 使用原则

- 先核对 FM27 版本/build 和测试协议，再比较指标。
- 区分四后卫、三中卫、五后卫与动态转换体系；以 IP/OOP 实际站位为准。
- 外部榜单用于寻找高收益候选和测试基准；本项目原版四后卫实测决定最终配置。
- 未取得原始 FMF 并解析前，网页显示的阵型和战术名只算初筛信息。
- 不把外部成绩直接推断成某条 PI/TI 的因果效果。
- 犯规、黄牌、红牌不属于本项目分析或验证指标。

## 来源登记

| 来源 | 类型 | 适用价值 | 主要限制 |
|---|---|---|---|
| [metaFM Leaderboard](https://metafm.net/leaderboard) | 受控大样本排行榜 | 相同对手计划/球员、不同强弱对手测试、PPG与xG等 | 需核对具体测试是否完成；当前头部战术多为OOP五后卫，不能直接作为四后卫基准 |
| [metaFM How we test](https://metafm.net/how-we-test) | 测试协议说明 | 了解筛选节点、样本量、误差范围、跨版本重测原则 | 不代表所有网站使用相同协议 |
| [FMDelicious Official Rankings](https://www.fmdelicious.com/matchlab/rankings) | 独立测试榜单 | 独立协议、每套样本量、95%误差范围、对手强度分组 | 与metaFM协议不同，Pts/38不可直接与PPG换算混排 |
| [Sortitoutsi FM27 Testing Table](https://sortitoutsi.net/football-manager-2027-tactics) | 社区测试库 | 不同球队/人工或假期模拟的实测记录 | 测试条件异质，样本量差异大，需逐项检查 |
| [FM Scout Tactics Analyser](https://www.fmscout.com/tac) | 战术结构分析工具 | 解析IP/OOP结构、指令作用与潜在冲突 | 本次打开页面返回403，尚未提取具体战术数据；后续可重试 |

## 2026-11-24 首次检索快照

### 1. metaFM — FM27 27.1.0

- 页面：[Leaderboard](https://metafm.net/leaderboard)
- 检索时间：2026-11-24（页面显示更新 10:04 UTC）
- 游戏版本：FM27 27.1.0
- 页面显示：441 套战术、684,691 场测试；测试使用相同的 3,977 份 AI 对手战术计划和相同球员，单套战术最高可进行 8,008 场测试。
- 当前榜首：Vanco Corsair v70，PPG 2.09，页面显示 ±0.02；16,016 场，Pts/38 79.6，胜率 64.5%，进球/38 111.8，失球/38 60.9，xG 2.48，对手 xG 1.60。
- 该战术网页显示有球 2-4-1-3 DM、无球 5-2-3，**属于无球五后卫候选，不纳入本项目四后卫成绩基准**。
- 当前榜单第二名 ARGUS 27.1 3322 P85 EC：有球 3-3-2-2、无球 5-2-3，同样排除出四后卫成绩榜，但可供角色/PI/TI机制候选研究。
- 测试方法说明：弱势战术会在 560、1,120、4,004 场节点分阶段淘汰；完整测试最多 8,008 场。榜单对头部战术另有强队/弱队等条件测试。不同阶段样本数不可忽略。

### 2. FMDelicious — FM27 27.1.0

- 页面：[Official Rankings](https://www.fmdelicious.com/matchlab/rankings)
- 检索时间：2026-11-24；页面显示更新时间 2026-11-23 13:43 UTC。
- 协议：`fmd-twin-mid@2`；游戏版本 FM27 27.1.0。
- 页面显示：266 套战术、1,608,768 场模拟，每套 6,048 场，按每 38 场积分 Pts/38 排名并给出 95% 误差范围。
- 榜首：3421 Purity v4，75.8 ± 1.1，n=6,048。
- 第二：ARGUS 27 FR 3421 N P97 AC，71.8 ± 1.2，n=6,048。
- 第三：FM26 3421N Gasperini META，71.0 ± 1.2，n=6,048。
- 榜首名称/阵型提示 3-4-2-1 类三中卫结构，不能直接作为四后卫成绩基准；需要下载战术并核对 IP/OOP 后才可确定具体结构。
- 此榜单与 metaFM 测试协议不同，不得把 Pts/38 与 metaFM PPG 直接放入同一排名。

### 3. Sortitoutsi — FM27 社区测试表

- 页面：[FM27 Tactics Testing Table](https://sortitoutsi.net/football-manager-2027-tactics)
- 检索时间：2026-11-24。
- 页面说明每条战术可包含一个或多个用户测试，记录球队、胜负、进失球，并区分手动比赛或假期模拟；页面提醒比赛引擎更新会影响战术表现。
- 页面示例包括 XPOS META 4-2-3-1 DM：52 场、PPG 2.27；Bakerball v1：326 场、PPG 2.27（页面显示 9 项测试）。这些只作社区线索，不与受控榜单混排，因为球队与测试条件可能不同。
- 后续必须逐条确认战术实际无球结构和测试球队，不以标题中的 4-2-3-1 自动认定其无球仍为四后卫。

### 4. FM Scout — 战术分析器

- 页面：[FM Scout Tactics Analyser](https://www.fmscout.com/tac)
- 搜索结果说明其目标是显示战术有球/无球形态、指令效果及指令之间的冲突。
- 本次页面打开返回 403，未读取具体分析结果；登记为待重试工具，不作为本轮配置结论来源。

## 首轮对本项目的含义

1. 当前公开大样本榜单的头部样本明显存在 OOP 5-2-3 等五后卫结构。它们可以提示“无球五后卫结构可能在该测试协议下强势”，但这不能推翻本项目的四后卫约束。
2. 需要在各榜单内专门筛选 OOP 最后防线为四人的战术，建立独立四后卫候选表；不能以网页标题阵型代替 OOP 站位核对。
3. 外部高排名战术可用于提出角色、职责、PI、TI 的候选假设；只有拿到原始 FMF 并解析具体配置后，才能与 V0.1/V0.2 做字段级对照。
4. 不同测试站点必须保留自己的排名和协议。优先比较各站内部相同 build、相同测试协议下的结果，再观察跨站是否出现一致趋势。
5. 本次仅完成首轮来源登记和排行榜快照，**尚未完成 4 后卫候选战术的完整筛选、FMF 下载解析或引擎机制复现**；不得把本文件误读为已完成外部战术逆向分析。

## 后续快照模板

每次追加：
- 日期/时区：
- 游戏版本与 build：
- 网站/榜单 URL：
- 测试协议：
- 战术总数/单套样本量：
- 指标及误差：
- 四后卫候选（IP/OOP）：
- 原始 FMF 是否取得、SHA-256：
- 解析到的角色/职责/PI/TI：
- 可迁移到本项目的候选机制：
- 反例/副作用/证据等级：
- 下一步本地复现实验：


## 外部研究快照｜2026-11-24（V0.3 设计输入）

### 当前受控榜单（FM27 27.1.0）
- **metaFM**（抓取：2026-11-24 10:04 UTC）：441 套战术、684,691 场总测试；榜首 Vanco Corsair v70 为 2.09 PPG，示例结构 IP 2-4-1-3 DM / OOP 5-2-3，16,016 场、79.6 Pts/38、xG 2.48、xGA 1.60。头部示例为无球五后卫，排除出本项目四后卫成绩基准。协议：同一批 3,977 个 AI game plans、相同球员、主客场对半，分阶段筛选至最多 8,008 场。证据等级 A（平台统一控制测试；单套战术完成场次需单独核对）。来源：[排行榜](https://metafm.net/leaderboard)。
- **FMDelicious**（抓取：2026-11-24）：协议 `fmd-twin-mid v2`、FM27 27.1.0，266 套、总计 1,608,768 场，每套 6,048 场，95% 误差范围。可明确筛出 IP/OOP 均为 4-2-3-1 的 **FM27 Meta**：#9，66.7±1.2 Pts/38，51% 胜率，78.9 GF/38、53.8 GA/38，xG 2.00、xGA 1.28。属于四后卫比较样本；未取得并解析其 FMF 前，不将 PI/TI 视为已核对配置。证据等级 A。来源：[排行榜](https://fmdelicious.com/tactics?fm_version=FM27&view_mode=all)。

### 四后卫机制候选（FM-Arena 社区测试）
- **ZaZ - Ace of Diamonds 1.0**：作者标注 base 4-3-3；战术信息截图显示无球后防线为 FB-CB-CB-FB，即真实四后卫，另有 DM、双 CM、双边锋和 CFD。FM27 27.1.0：1,350 场，68/114 分，+24 GD，77 GF、53 GA，xGF 74、xGA 54；FM27 27.0.1：1,350 场，69/114 分，+26 GD，85 GF、59 GA，xGF 76、xGA 56。两 build 分开记录，不合并。来源：[测试主题及原始战术信息图](https://fm-arena.com/threads/zaz-ace-of-diamonds-1-0.84/)。证据等级 B（单一独立测试站、公开 build/样本/主客场拆分；非本项目相同球队条件）。
- 其 PI 公布：DM `Press More Often`；两名 BCB `Press Less Often`；WB `Press More Often`；CB 短传；WB 内收、少射门、底线传中。TI 包含 More Direct、Much Higher、Much Narrower、Counter、High Press、Much Lower Defensive Line、Counter-Press。仅将“后腰主动触发压迫”登记为可移植的单变量候选，不复制整套战术。图像核对了四后卫 OOP 结构。该作者战术在 metaFM 另一套协议下，27.0.1 为 5,432 场、1.73 PPG；27.1.0 测试在 560 场检查点停止、1.63 PPG。不同协议结果不可直接换算，提示不能把单一榜单当成绝对排名。来源：[metaFM 该战术版本记录](https://metafm.net/zh/tactics/zaz-ace-of-diamonds-1-0-3b0c82)。

### 引擎版本变化
- 27.1.0 的公开更新整理提及 OOP 压迫决策/强度调整、边路压迫改善、最后一名防守者不再像此前那样大幅前顶，以及 AMC 有球站位变化。此信息来自社区对更新说明的整理，证据等级 C；V0.2 报告来自 27.0.1，不能直接等同于 27.1.0 表现。来源：[27.1.0 变化汇总](https://fm27.vi.ki/tactics-after-update-27-1)。

### 对 V0.3 的实际影响
- V0.2 新增 4 场联赛样本显示对手 xG 9.52、绝佳机会 17，防守机会质量是首要风险；但只有 4 场，不能归因到单个 PI。
- V0.2 的 DML OOP `TRIGGER_PRESS=LESS_OFTEN`，而独立四后卫候选将 DM 设为 `Press More Often`。这是角色级候选，不是机制已证实。
- V0.3 仅把 DML 的 `TRIGGER_PRESS` 从 `LESS_OFTEN` 改为 `MORE_OFTEN`；其余结构与配置全部保持不变，作为单变量本地实验。V0.2 的 `DEFENSIVE_LINE=HIGHER` 保留，因为共同 19 场比较中净胜球改善 +9，当前数据不足以证明防线高度应回退。
- 27.1.0 排行榜与项目报告的 27.0.1 build 不混排；新版本赛季测试必须记录实际 build。


## 外部基准快照｜2026-11-24（配合 V0.3 报告，锁定 FM27 27.0.1）

### 1. FM-Arena：27.0.1 受测战术
- 页面记录：81 套、109,350 场；每套候选条目通常 1,350 场，需按各自页面确认具体测试重复次数。来源：[27.0.1 排行榜](https://www.fm-arena.com/tactic-testing/aggregators/1/)。
- **HIGHWAY STAR 27 BBMIW 4231 P96 FA**：1,350 场，68/114 分、+27 GD、79 GF、52 GA、xGF 72、xGA 52；主题页注明 3 次测试结果。其战术信息图可直接确认无球后场为 FB-CB-CB-FB 四人线，故符合本项目 OOP 四后卫筛选。图中还显示高位逼抢、较低防线、Step Up More、Trigger Press More Often、Counter-Press。来源：[测试主题](https://www.fm-arena.com/threads/highway-star-27-bbmiw-4231-p96-fa.110/)；[原始战术信息图](https://www.fm-arena.com/data/fmt_tactic_info/0/508-e41f9d790a6091b3c15fdc531aa7b8bc.webp)。
- 证据等级 B：公开 build、样本量、结果与实际 OOP 结构截图；尚未取得并解析该战术 FMF 的完整 PI/TI。它支持“高位压迫可与真实四后卫 OOP 共存”作为候选机制，但其低防线与本项目高防线不同，不直接复制。
- 榜单其他 4-2-3-1/4-3-3 标题不能仅凭标题认定 OOP 四后卫；没有截图或 FMF 的条目不计入严格四后卫样本。

### 2. metaFM：27.0.1 独立受控榜单
- 27.0.1 存档页：150 套战术、453,062 场；页面说明使用同一批 2,689 个 AI 对手计划（417 家俱乐部、14 种阵型）、相同球员、主客场均衡，逐步筛选至每套最多 5,432 场。来源：[metaFM 27.0.1](https://metafm.net/versions/27.0.1)；[测试方法](https://metafm.net/how-we-test)。
- 榜首大量样本是 OOP 5-2-3/5-4-1，均排除出四后卫成绩排名。页面可见的四后卫候选之一 **STORMBRINGER 27 BBMIW 424 P102 FA**：IP 4-2-4 / OOP 4-4-2 DM，5,432 场，69.3/114 分，85.3 GF/38、56.6 GA/38，xG 2.14、xGA 1.45。其 OOP 标示为四后卫，但尚未下载原始 FMF 独立解析，故结构证据低于 FM-Arena 上述截图。
- 证据等级 A（榜单测试协议和大样本控制）；该具体条目的战术细节仍待原始 FMF 复核。不得把 27.0.1 与 metaFM 27.1.0 成绩混排。

### 3. Sortitoutsi：异质社区赛果表
- 当前页面列出 **XPOS META 4-2-3-1 DM**：52 场、2.27 PPG、2.33 GF/场、1.21 GA/场。该站明确混有手动比赛与假期模拟、不同球队与测试数量；没有统一控制协议和明确 build 时，证据等级 C，只作社区信号，不用于与 FM-Arena/metaFM 的受控排名直接换算。来源：[FM27 Tactics Testing Table](https://sortitoutsi.net/football-manager-2027-tactics)。

### 4. 引擎版本隔离
- SI 官方 27.1.0 更新说明明确提及 OOP 压迫决策/强度调整、边路压迫改善，以及进攻转换、传球与 AMC 行为变化。来源：[官方 27.1.0 changelist](https://footballmanager.sega.com/asia-en/info/details/000290.html)。
- 本轮 V0.3 存档实际 build 为 **27.0.1+2494687**，所以本轮本地表现必须与 27.0.1 外部结果对照；27.1.0 只能登记为后续版本机制变化，不可用来解释本轮赛果。

### 5. 对本项目的决策
- V0.3 DML OOP `TRIGGER_PRESS=MORE_OFTEN` 与 FM-Arena 四后卫样本的主动压迫方向一致，但一个使用 DML 个体 PI、另一个显示团队 Trigger Press TI，不能视为同一配置。
- V0.3 的 20 场共同赛程成绩明显优于 V0.2；当前保留该 PI，不回退、不叠加第二项更改。
- 下一轮优先完成同存档/同阵容/同 build 的 V0.2 对 V0.3 原生引擎 A/B；在本地详细统计覆盖不足时，不强制创建 V0.4。


## 外部研究快照｜2026-11-24（V0.4 设计输入，重新核验）
- **FM-Arena 27.0.1**：当前测试页仍列出 81 套战术、109,350 场；本项目使用的报告 build 为 27.0.1+2494687，版本对应。来源：[FM-Arena 27.0.1](https://fm-arena.com/tactic-testing/aggregators/1/)。
- **metaFM 27.0.1**：当前归档 150 套战术、453,062 场；STORMBRINGER 27 BBMIW 424 P102 FA 明确为 IP 4-2-4 / OOP 4-4-2 DM，5,432 场、1.82 PPG、69.3 Pts/38、85.3 GF/38、56.6 GA/38、xG 2.14、xGA 1.45。协议固定相同球员与 2,689 个 AI 对手计划，主客场平衡。证据等级 A（受控协议）；仅用于四后卫结构成绩参照，不将其配置因果移植到 V0.4。来源：[榜单](https://metafm.net/versions/27.0.1)；[方法](https://metafm.net/how-we-test)。
- **FM-Arena 与 metaFM 当前样本差异**：FM-Arena 27.0.1 的 81 套/109,350 场与 metaFM 的 150 套/453,062 场采用不同协议，分别存档，不换算混排。
- **设计应用**：V0.4 将 DEFENSIVE_LINE 从 HIGHER 调至 LOWER，参考 FM-Arena 四后卫候选的高位逼抢+较低防线组合；将 PASS_RECEPTION 调为 PASS_TO_FEET、删除 CROSSING_STYLE=LOW_CROSSES 显式覆盖，使用 catalog 原生默认混合传中（native bit 0），是针对本地 V0.3 90 次越位与低传中成功率的本地数据驱动修正，不是外部榜单已验证的固定配方。


## 外部基准快照｜2026-11-24（重做 V0.4，锁定 FM27 27.0.1）

- FM-Arena 27.0.1：81 套战术、109,350 场；本地报告 build 27.0.1+2494687 与其版本一致。来源：[FM-Arena 27.0.1](https://fm-arena.com/tactic-testing/aggregators/1/)。证据 A（榜单整体测试数据）。
- HIGHWAY STAR 27 BBMIW 4231 P96 FA：1,350 场、68/114 分、+27 GD、79 GF、52 GA、xGF 72、xGA 52；原始战术信息图显示 OOP 为 FB-CB-CB-FB。来源：[测试主题](https://fm-arena.com/threads/highway-star-27-bbmiw-4231-p96-fa.110/)；[战术信息图](https://www.fm-arena.com/data/fmt_tactic_info/0/508-e41f9d790a6091b3c15fdc531aa7b8bc.webp)。证据 B；支持高位压迫与四后卫、较低防线共存，不证明单一指令因果。
- metaFM 27.0.1：150 套、453,062 场；STORMBRINGER 27 BBMIW 424 P102 FA 为 IP 4-2-4/OOP 4-4-2 DM，5,432 场、1.82 PPG、85.3 GF/38、56.6 GA/38、xG 2.14、xGA 1.45。来源：[27.0.1 榜单](https://metafm.net/versions/27.0.1)；[测试协议](https://metafm.net/how-we-test)。证据 A（平台控制协议）；只作四后卫参照，不跨站混排。
- metaFM 27.1.0 已采用新引擎；版本更新后重新测试。来源：[27.1.0 更新影响](https://metafm.net/patch/27.1.0)。不用于解释本地 27.0.1 赛果。
- 设计应用：保留 PASS_TO_FEET、原生默认混合传中、LOWER 防线；补左侧宽度、右中卫留守、AMC 减少重复盘带。所有本地效果仍待实测。


## 外部研究快照｜2026-11-24（V0.4 run139 报告复核，build 27.0.1）

- FM-Arena 27.0.1：81 套战术、109,350 场。HIGHWAY STAR 27 BBMIW 4231 P96 FA：1,350 场、68/114 分、+27 GD、79:52、xGF72、xGA52；原始战术信息图确认 OOP 四后卫 FB-CB-CB-FB。证据 B。来源：[榜单](https://www.fm-arena.com/tactic-testing/aggregators/1/)；[测试条目](https://fm-arena.com/threads/highway-star-27-bbmiw-4231-p96-fa.110/)。
- metaFM 27.0.1：150 套、453,062 场；STORMBRINGER 27 BBMIW 424 P102 FA：IP 4-2-4/OOP 4-4-2 DM，5,432 场、1.82 PPG、69.3 Pts/38、85.3 GF/38、56.6 GA/38、xG2.14、xGA1.45。证据 A（固定球员与同一批 2,689 个 AI 对手计划，主客场均衡）。来源：[版本榜单](https://metafm.net/versions/27.0.1)；[测试方法](https://metafm.net/how-we-test)；[STORMBRINGER](https://metafm.net/tactics/stormbringer-27-bbmiw-424-p102-fa-d5a3d4)。
- 两个测试体系分别存档，PPG、Pts/38、FM-Arena PTS 不换算混排。仅筛选 OOP 真正四后卫的候选，不纳入 3/5 后卫结构成绩。
- SI 27.1.0 更新包括越位跑动、短传、OOP 压迫和边路压迫等变化；与本项目 27.0.1 build 隔离。来源：[官方更新公告](https://steamcommunity.com/app/4530370/allnews)。
- 官方引擎说明强调球员智能、Anticipation、Off The Ball 对禁区跑动决策的影响，以及 Marking/Anticipation 对防守表现的影响。来源：[FM27 Match Engine 深度说明](https://www.footballmanager.com/fm27/features/fm27-tactical-tweaks-and-match-engine-upgrades)。
- 本轮本地数据结论：V0.4 联赛 30 场 13-10-7、50:39、49 分；球队详细联赛统计仅 5 场；94 条逐场出场均未识别身份。V0.5 暂不建配方，避免从不同存档的共同赛程差异推断单一 PI/TI 因果。


---

## 2026-11-25｜FM27 build 27.1.1 外部榜单与测试协议快照

### 1. metaFM：27.1.1 受控排行榜（证据 A）

- 页面：[FM27.1.1 Leaderboard](https://metafm.net/leaderboard)；检索日期 2026-11-25，页面更新时间 01:02 UTC。
- 页面当前显示 **12 套战术、28,560 场测试**。协议使用同一批 3,977 个真实 AI 对手计划、相同球员阵容，改变被测战术；分四种强弱条件测试，并综合四类条件的 PPG 排名。
- 当前榜首 ARGUS 27.1 3322 P85 EC：有球 3-3-2-2、无球 **5-2-3**；综合 2.074 PPG、2,240 场总测试、79.0 Pts/38、xG 2.40、xGA 1.47。
- 第二名 2-1-4-3 TOP NEW：有球 2-5-3 DM、无球 **5-2-3**；2.062 PPG、2,240 场、83.1 Pts/38、xG 2.36、xGA 1.44。
- 当前榜单前 12 名的无球结构均显示为 **5-2-3 或 5-3-2**。因此本快照没有可直接纳入“真实无球四后卫”成绩对比的候选。它们只能用于发现引擎机制/指令候选，不可作为四后卫基准或照搬结构。
- metaFM 报告使用相同战术、AI 计划、球员和比赛 seed 的 1,664 场 27.1.0→27.1.1 重放中，有 974 场（58.5%）结果不同；页面明确提醒不要跨 27.1.0 与 27.1.1 直接比较排名数值。该站测试口径自身属于 A 级，但该结论不等于独立第二来源复现。
- 页面链接：[排行榜与当前测试统计](https://metafm.net/leaderboard)；[完整方法说明](https://metafm.net/how-we-test)。

### 2. FM-Arena：27.1.1 测试进度（证据 C，未完成）

- 来源：[FM Tactic Testing Log](https://fm-arena.com/tactic-testing-log/)，检索日期 2026-11-25。
- 日志显示 27.1.1 的不同战术仍有 Test #2 / Test #3 陆续新增，例如 Roman Empire、STORMBRINGER 424 P94、ZaZ - Ace of Hearts 2.1、ARGUS 27.1 3421 等。
- 本次读取的是测试活动日志，不是完整的 27.1.1 已完成成绩汇总；因此不引用其战术最终排名/PPG，也不根据战术名称推断 OOP 站位。后续取得战术页/信息图/FMF 并核对 OOP 结构后再分类。

### 3. 官方引擎更新事实（机制候选，不等于性能因果）

- 官方 [FM27 Update 27.1.0 Changelist](https://footballmanager.sega.com/asia-en/info/details/000290.html)（2026-11-17）明确列出：反击阶段传球与盘带决策调整；越位跑动与相关传球决策调整；短传精度及接球逻辑调整；AMC 有球时更宽移动；OOP 压迫决策/强度和边路压迫调整；Wide Midfielder 无球内收频率调整；次级盯防者覆盖位置/压迫重做；双后腰情况下 AI 更少选择 Dropping DM。
- 这些变化与 V0.5 的“传入空当/立即反击”、AMC Channel Midfielder、ML/MR Tracking Wide Midfielder 及双后腰结构直接相关。故 V0.5 数据必须以存档 build 27.1.1 为独立版本解释，不与 V0.4 的 27.0.1 数值作因果比较。
- 官方 [27.1.1 发布说明](https://steamcommunity.com/app/4530370/allnews/)描述了较小的后续更新；metaFM 自身相同输入重放仍观察到跨版本结果变化。两者的表述层面不同，本项目遵循实测隔离原则，不推断 27.1.1 变化由某个单独战术机制造成。

### 4. 对 V0.5 / V0.6 的影响

- 当前外部 27.1.1 metaFM 前列战术没有真实 OOP 四后卫对照；FM-Arena 同 build 结果仍在测试中。
- 不把 OOP 五后卫榜首的 2.07 PPG、xG 等指标与 V0.5 38 场联赛的 2.03 PPG 或 xG 直接比较；测试协议、阵容、赛程强度和比赛环境均不同。
- 对 V0.5 有价值的机制监测候选：高压迫边路行为、Wide Midfielder 无球内收、反击传球决策、短传/接球质量、AMC 有球宽度。现有 V0.5 报告中，团队机会质量已经强，尚无证据要求仅凭这些 patch notes 改角色或 PI。
- 本轮不把任何榜单冠军的五后卫配置移植到真实四后卫体系；等待可核对的 27.1.1 OOP 四后卫 FMF/信息图再做字段级比较。
