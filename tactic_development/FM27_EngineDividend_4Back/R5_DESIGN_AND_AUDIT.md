# R5 设计审计｜IP 4-2-3-1 / OOP 5-2-3 无锋三出口

日期：2026-11-27  
状态：D0 设计审计；D1-D3 待项目构建通道执行；D4/D5 未验证。

## 0. 版本身份与固定基准

版本：R5  
父版本：V0.5  
重生基准：V0.5  
重生基准 FMF SHA-256：e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257  
父 FMF SHA-256：e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257  
本轮配方 SHA-256：1990f40739388ed9370431532b3d898a8d414956427f7b0aebe8e434313f8b5c  
项目规则 SHA-256：3f5b03ed932aab6dd3dd7fb119946af6401cb964c7df127e9762c5b615b8aec3  
决策总账 SHA-256：cbfb24e7bb0faa2e96fe052a637ebeec4b392d98916ee9b1a7566806c2c25f46  
PPG 策略 SHA-256：e3904a61aaf71e508fdd33d15705fd9613b0d8b6b8bdb5f97fe497743aac2605  
位置绩效标准 SHA-256：d79a62508aa31490a62c4c63524aa91146b953fd2eb82252e8501312e07838f1

审计结论： PASS

本 PASS 仅表示 D0 设计审计材料满足项目门禁要求；不代表 D1 原生预检、D2 结构检查、D3 FMF 回读、D4 游戏导入或 D5 比赛表现已通过。R5 的唯一性能成功标准仍是完整38场英超同时达到至少109分（PPG ≥ 2.85）及全队 xG≥100。

## 1. 本轮目标、报告身份与数据质量

- 被审计版本：R4；用户确认该赛季38场英超使用R4。Exporter不导出战术配置，战术映射是用户声明，不是Exporter自动识别。
- 原始报告：FM27-Exporter Run 45914272197；源存档 `1.fm`；源SHA-256 `0afc7213468d5da2af8f3137158565432271f42a0eeeeb27d155a5f70831866c`；游戏日期2027-06-03。
- 环境：FM27 build 27.1.1+2511875；Exporter 1.5.0；fmsave 0.14.3；known_build=false。球队/球员解析使用借用schema-6布局；局部字段交叉核对通过，整体仍为partial/unverified。
- 覆盖：英超38/38场；球队/球员统计1,140/1,140对账；活跃出场932、身份识别913（97.96%），19条未识别；英超识别589/592。
- 位置字段209/209交叉核对；角色码只解码309/913条识别出场，604条缺失；无逐场OOP角色、职责、PI/TI执行映射。
- 位置码不能拆分DCL/DCR或DML/DMR；下文位置数据仅是报告位置汇总，不等同11个战术槽的直接贡献。任何缺失字段均标记U/未观测，不补猜。

## 2. R4 D5结果与主要问题

| 指标 | R4 | 项目门槛/基准 | 判断 |
|---|---:|---:|---|
| 联赛场次 | 38 | 38 | 完整 |
| 胜/平/负 | 12/10/16 | — | 未胜26场 |
| 积分 / PPG | 46 / 1.211 | ≥109 / ≥2.85 | FAIL |
| 进球 / 失球 | 52 / 57 | 结果诊断 | 进攻产出低 |
| xG / xGA | 58.86 / 61.02 | xG≥100 | xG硬门槛FAIL |
| 场均xG | 1.549 | ≥2.632 | 明显不足 |
| 射门 / 射正 | 408 / 213 | 过程诊断 | 低于R3 |
| 绝佳机会 | 60 | 过程诊断 | 不能抵消射门量不足 |

R4相对R3：积分-20、进球-13、失球+20、xG-6.14、xGA+14.84、射门-44、射正-22、绝佳机会+4。xG/射门约0.144，与R3约0.144接近，团队xG下降主要伴随射门总量下降。传中尝试约1,181次，成功150次、完成率12.7%；R3约1,190次、成功约192次、完成率16.1%。越位93→77，减少越位没有换来更多射门或xG。

胜/平/负场均xG为2.01/1.33/1.34，场均xGA为1.30/1.77/1.73。败场平均8.94次射门；主场21分、客场25分。防守机会控制是积分损失诊断项，但本项目不以漂亮xGA替代PPG，也不因单独xGA高而自动淘汰能显著提高进球的结构。

### 2.1 低产与高产未胜案例

报告复盘识别的低产样本：
- 2026-12-05 诺丁汉森林 1-1：我方4次射门、xG0.28。
- 2027-01-23 曼城 0-1：我方4次射门、xG0.45。
- 2026-09-19 阿森纳 0-2：我方2次射门、xG0.15。
- 2027-05-02 诺丁汉森林 1-2：我方5次射门、xG0.73。

高产但未胜样本：
- 2026-08-30 切尔西 0-2：我方xG2.14，未进球。
- 2026-10-25 利物浦 1-3：我方xG2.82。
- 2027-05-23 利物浦 2-5：我方xG1.88，对手xG2.17。

因此R4同时存在持续进攻产量不足与部分比赛机会未兑现；不能把问题简化成“前锋浪费机会”。R5优先恢复射门/机会生成通道，同时保留终结与主客场分组诊断。

## 3. 历史多维基准与配置沿革

| 版本 | 积分/PPG | 进球-失球 | xG / xGA | 维度结论 |
|---|---:|---:|---:|---|
| V0.5 | 69 / 1.816 | 75-43 | 72.92 / 44.12 | 原始基准，非达标 |
| V1.3 | 88 / 2.316 | 83-30 | 80.54 / 34.27 | 历史防守机会控制基准 |
| V1.4 | 83 / 2.184 | 101-53 | 92.62 / 43.46 | 进攻增产但积分下降、防守代价增加 |
| V1.6 | 89 / 2.342 | 87-37 | 75.54 / 46.33 | 历史最高积分，但xG未达100、终结超额明显 |
| V1.7 | 82 / 2.158 | 79-36 | 74.29 / 44.13 | OOP分层保护改善机会控制，进球/积分下降 |
| V1.8 | 72 / 1.895 | 98-55 | 88.87 / 59.67 | 进攻机会增多但OOP五后卫组合风险高 |
| 2.2 | 84 / 2.211 | 87-40 | 81.83 / 43.58 | IP菱形双前锋/OOP 5-2-3，仍未达双门槛 |
| R3 | 66 / 1.737 | 65-37 | 65.00 / 46.18 | 非胜场进攻产量不足 |
| R4 | 46 / 1.211 | 52-57 | 58.86 / 61.02 | 当前最差D5，射门与xG继续下降 |

跨版本均非同seed受控A/B，不能把差值归因于单个角色或指令。V1.3是防守机会质量基准，V1.6是积分基准，V1.4是进攻产量/绝佳机会参考，V1.8是高进攻伴随高防守代价的失败样本；任何版本均未达到109分与100 xG双门槛。

### 3.1 相关配置结论

- V1.2/V1.3/V1.7的OOP四后场底线与双后腰分层保护反复伴随较好的xGA/对手绝佳机会；V1.6双后腰更积极后积分最高，但防守机会质量较差。保留“分工而非双后腰同时盲目上抢”作为待验证原则。
- V1.7→V1.8：OOP改无锋5-2-3后xG+14.58、进球+19，但xGA+15.54、对手绝佳机会+20、积分-10。OOP 5-2-3不能只看进攻增益。
- R4采用OOP 5-2-3三出口，但整季46分、xG58.86。R5保留三出口是PPG策略明确指定的下一轮实验方向，不代表R4三出口已被证明有效；本轮通过更改前场压迫层级、边后卫角色和IP供给指令重新验证。
- R3→R4的传球接应由Pass Into Space改Pass To Feet，进攻耐心由Hit Early Crosses改Work Ball Into Box；同时射门减少44次、xG下降6.14、传中成功率下降3.4个百分点。它们共同构成需要回退的配置簇，不能单项归因。
- R4 DR WingBack Attack改为Support、DMR BoxToBox Support改为DefensiveMidfielder Defend，是PPG_TARGET_POLICY明确提出的下一轮方向；位置级统计不能证明单项因果，但DR位置只有1.18 xG/3助攻，DMC合并位置7.70 xG，未提供支持继续加大DR攻击或DMR前插的正向证据。

**为何本轮没有采用菱形IP：** ARCHITECTURE_REVIEW_20261126.md将4-1-2-1-2菱形列为外部样本优先结构；但R4 D5复盘及当前PPG_TARGET_POLICY给出的最近、最具体整改项是保留R4 OOP三出口、恢复Pass Into Space/Hit Early Crosses、DR WingBack Attack回Support、DMR BoxToBox Support回DefensiveMidfielder Defend。R5按这组最新本队D5问题建立单一验证主线，因此保留4-2-3-1槽位映射；这不代表4-2-3-1在外部优于菱形。菱形仍是后续结构研究候选，不在本轮同时混入，避免改变多个结构变量后无法解释结果。\n\n## 4. 外部引擎研究与跨阵型迁移

本轮外部来源以27.1.1当前可见资料为主；不同平台测试协议不合并，外部PPG不换算成本队38场赛季预期。

| 来源 | 可核实信息 | 迁移判定 | 局限 |
|---|---|---|---|
| FM-Arena | 27.1.1 match-engine讨论及大样本测试；社区对27.1.1与27.1.0是否改变存在不同解读 | 仅作当前build风险背景 | 与metaFM对patch差异的观察不完全一致；不能据此断言机制 |
| metaFM | 27.1.1榜首3-4-3 IP / 5-2-3 OOP样本3,447场，约2.09 PPG、xG2.44、xGA1.34；第二名同样OOP 5-2-3，样本6,972场、约2.06 PPG、xG2.51、xGA1.41 | OOP 5-2-3三出口结构可重构迁移；其IP三后卫结构依赖，不可照搬 | 远低于本项目2.85 PPG与2.63场均xG目标；外部协议与本队存档不同 |
| SI官方论坛 | 本轮检索未取得可复核的当前build、完整角色/PI/TI组合与大样本结果 | 证据不足 | 不以讨论帖标题推断配置 |
| Sortitoutsi | XPOS META 4-2-3-1 DM：27.1.0，52场、37胜7平8负、2.27 PPG；IP 4-2-3-1 DM AM Wide，OOP 4-4-1-1双后腰；Pass Into Space、Hit Early Crosses、High Press、Trigger Press More Often、Pressing Full-Back；Tackle Harder主要给后腰，评论提醒前场过度Tackle Harder有黄牌/停赛代价 | IP角色/PI/TI可重构迁移；OOP 4-4-1-1结构依赖，不照搬 | 版本早于27.1.1，样本仅52场，社区赛季结果非受控大样本 |
| Reddit r/footballmanagergames | 27.1.1周讨论有玩家报告高位压迫+高触发可能让防守失序、CPU传中威胁较高、极高防线需顶级中卫 | 风险提示C级；支持本轮不重复Invite Crosses，不能证明普遍机制 | 个案/主观体验，无控制样本 |
| FM Scout | 27.1.1 Asymmetric Block 4-2-3-1：IP阶段转3-2-5、OOP 4-4-1-1；另有4-2-3-1战术索引与榜单 | 该3-2-5 IP结构不符合本项目IP四后场硬约束，整体不可迁移；只作反例 | 搜索摘要可见，详情页403，未取得完整PI/TI原件 |
| Ludens Media | 本轮未找到可复核的FM27.1.1同类引擎样本 | 证据不足 | 未取得可核验的build/样本 |
| PlayGM/爆棚 | 27.1.1 Juventus 3-4-2-1：同一存档432场，289胜90平53负，2.22 PPG；左翼卫更靠前、Channel Forward向中路两侧空当跑、右前腰回撤、中锋留中路接反击 | 角色/阶段转换可重构迁移；3-4-2-1整体结构依赖 | 单一存档社区测试，主客场差异明显（主2.55、客1.88） |

本轮补充的可读战术配置：Sortitoutsi的XPOS META 4-2-3-1提供IP四后场、早传空当和压迫PI参考；其OOP 4-4-1-1不迁移。FM Scout的Asymmetric Block虽以4-2-3-1起始，但IP转为3-2-5，违反四后场硬约束，整体排除。PlayGM 3421仅迁移Channel Forward与前腰回撤/出口机制。Reddit的跨用户观察只作风险提示。\n\n主要来源URL：
- FM-Arena：https://fm-arena.com/
- MetaFM leaderboard：https://metafm.net/leaderboard
- SI官方战术讨论：https://community.sigames.com/forums/forum/19-tactics-training-strategies-discussion/
- Sortitoutsi：https://sortitoutsi.net/
- Reddit：https://www.reddit.com/r/footballmanagergames/
- FM Scout：https://www.fmscout.com/
- Ludens Media：https://www.ludens.com.tw/
- PlayGM：https://www.playgm.cc/

### 4.1 跨阵型机制迁移审查

metaFM高排名样本的IP三后卫是结构依赖，不能进入R5；可迁移的仅是OOP 5-2-3的换位/出口机制。Sortitoutsi 27.0.1/27.1.0的4-2-3-1样本可提供Pass Into Space、Hit Early Crosses、High Press、Trigger Press More Often和Pressing Full-Back等IP/PI/TI机制，但其OOP 4-4-1-1不迁移。FM Scout Asymmetric Block的IP实际转3-2-5，整体排除。R5在IP 4-2-3-1中保留DL/DCL/DCR/DR四后场槽，通过DML→DC、DMR→DML、AMC→DMR、ST→AMC等跨阶段映射形成OOP五人后线、双后腰和前场三出口。此为“可重构迁移”，不是直接复制三后卫战术。

本队V1.1/V1.8/R4的OOP五后卫失败证据仍然有效，不能被外部排名覆盖。R5必须重点检查：五人后线由什么角色组成、哪名中卫主动上抢、双后腰是否离位、前场出口是否回防、客场和非胜场的对手机会质量。

## 5. 四类决策

### 继承保留

- **固定结构：** IP四后场位置槽DL/DCL/DCR/DR各一次；R5从V0.5原生FMF重生，V0.5仅作为原生格式/父文件载体，不继承R4 FMF。
- **结构性候选：** 保留R4 OOP三出口角色：AML InsideOutletWinger、AMR WideOutletWinger、AMC CentralOutletAttackingMidfielder；保留为待验证候选，不是已准入。
- **攻击候选：** IP InsideForward A、FreeRole A、Winger S、TargetForward A、InsideFullBack D作为R5试验角色；由于R4全队xG58.86低于100，任何IP进攻槽均不得标记准入保留。
- **机制候选：** 高位遭遇线、后撤防线、Pass Into Space、Hit Early Crosses、高球/后点目标、Tackle Harder及分层Trigger Press，均按用户指定优先指标和当前原生权限作为待验证组合。

### 替换淘汰

- R4完整配方作为达标候选淘汰；只保留历史数据。
- Pass To Feet → Pass Into Space。
- Work Ball Into Box → Hit Early Crosses。
- DR WingBack Attack → WingBack Support。
- DMR BoxToBoxMidfielder Support → DefensiveMidfielder Defend。
- R4原样的OOP角色/职责/PI组合不得自动继承；R5重新设计PressingFullBack/HoldingFullBack、CoveringCentreBack/StoppingCentreBack及双后腰压迫分工。
- 移除R4式Byline限制，避免与团队Hit Early Crosses形成方向冲突。

### 新增待验证

- IP DR WingBack Support → OOP PressingFullBack Defend；IP DL InsideFullBack Defend → OOP HoldingFullBack Defend，形成非对称边路压迫与留守。
- IP DML DefensiveMidfielder Defend → OOP DC StoppingCentreBack Defend；DCR/DCL均转CoveringCentreBack Defend，形成中央主动、两侧保护的三中卫压迫层级。
- IP DMR DefensiveMidfielder Defend → OOP DML WideCoverDefensiveMidfielder Defend；IP AMC FreeRole Attack → OOP DMR DroppingDefensiveMidfielder Defend。
- OOP团队Trigger Press More Often；DR PressingFullBack与DC StoppingCentreBack角色默认固定较多逼抢；DCL/DCR CoveringCentreBack角色默认固定较少逼抢；双后腰与前场三出口显式More Often。
- OOP后线五人+双后腰共七人Tackle Harder，前场三出口不设Tackle Harder；Trigger Press More Often按角色权限分层。PI已由当前源码PI_MAP与角色权限表逐项检查，最终仍以D1预检和D3回读为准。
- 恢复Pass Into Space + Hit Early Crosses + High Crosses + Back Post；以TargetForward为长传/传中接应点，监控传中完成率、射门量、越位与xG/射门。
- 保留High Press + Much Lower Defensive Line + Drop Off More作为P0假设，但R3/R4表现不支持将其视为已验证；重点监控中场线与后防线之间的空间、禁区前沿射门和直塞身后球。

### 证据不足

- 角色默认行为GameID引用已提取，但缺少本地化文本字典，不能声称已解码每个角色的完整默认移动/指令。
- Exporter无逐场IP/OOP槽位、角色职责、PI/TI执行映射；位置级统计不能冒充槽位级贡献。
- 604/913条识别出场缺少角色码；19条身份未识别。
- 外部metaFM高排名样本的完整PI/TI并非全部公开；榜单成绩不是本队D5。
- R5跨阶段球员熟悉度、属性匹配和真实执行行为必须在D4由游戏内核验。

## 6. 唯一R5整体方案

- **IP：4-2-3-1。** 后场严格为DL InsideFullBack Defend、DCL CentreBack Defend、DCR CentreBack Defend、DR WingBack Support；DML/DMR均为DefensiveMidfielder Defend；AML InsideForward Attack、AMC FreeRole Attack、AMR Winger Support、ST TargetForward Attack。
- **OOP：5-2-3无锋三出口。** DR PressingFullBack Defend、DCR/DCL CoveringCentreBack Defend、DL HoldingFullBack Defend、DC StoppingCentreBack Defend；DML WideCoverDefensiveMidfielder Defend、DMR DroppingDefensiveMidfielder Defend；AML InsideOutletWinger Attack、AMR WideOutletWinger Attack、AMC CentralOutletAttackingMidfielder Attack。
- **心态：Positive（recipe ment=5）**，沿用R4心态值；本轮不把心态变化与进攻指令变化混在一起。
- **进攻TI：** More Direct、Much Higher Tempo、Wider、Counter Attack、Bypass Press、Long Goal Kicks、Target Forward distribution、Pass Into Space、Hit Early Crosses、High Crosses、Encourage Dribbling、Discourage Long Shots。
- **防守TI：** High Press、Much Lower Defensive Line、Drop Off More、Trigger Press More Often、Counter Press、Trap Outside、Invite Crosses。
- **个人PI：** IP后场短传/少冒险；DR与AMR拉开宽度、后点目标、少射门；ST远门柱；OOP后线五人+双后腰七人Tackle Harder；Trigger Press按角色原生权限与分层配置。角色默认GameID文本未知，不对其内容作推断。
- **与R4的关键差异：** 恢复Pass Into Space与Hit Early Crosses；DR职责回到Support；DMR由BoxToBox Support回到DefensiveMidfielder Defend；OOP右侧PressingFullBack与左侧HoldingFullBack非对称；两侧中卫Covering、额外DC Stopping；R5仍从V0.5重建，不复制R4二进制。

## 7. 强制审计：引擎行为错位设计

- 错位类型：IP/OOP跨阶段角色反向分工、团队压迫与中卫保护分层、前场无锋出口与有球攻击角色错位。
- 错位配置：IP四后场DL/DCL/DCR/DR；DR WingBack Support→OOP PressingFullBack；DL InsideFullBack→OOP HoldingFullBack；DML→DC StoppingCentreBack；DCR/DCL→CoveringCentreBack；DMR→DML WideCover DM；AMC FreeRole→DMR Dropping DM；AML/AMR/ST→AML/AMR/AMC三出口。
- 角色/指令默认行为：当前原生catalog显示PressingFullBack的Trigger Press More Often为角色固定项，HoldingFullBack与CoveringCentreBack的Trigger Press Less Often为角色固定项，StoppingCentreBack的Trigger Press More Often为角色固定项；WideCover DM、Dropping DM和三种Outlet角色允许显式More Often。角色默认GameID的可读文本尚缺，故不把这些固定项扩写成未经核实的跑动/盯人规则。
- FM27引擎预期执行行为：团队高位遭遇线与团队More Often触发主动逼抢；角色固定项让右后卫/额外DC更主动、左右保护中卫与左侧HoldingFullBack更少离位；双后腰和前场出口承担更积极的压迫；这些是由原生权限结构提出的行为假设，必须通过游戏内与D5验证。
- 对手AI可能：被迫向边路或更早长传，尝试绕过高位第一线；若压迫被一脚传球破解，可能攻击高位遭遇线与Much Lower后防线之间的区域；面对Invite Crosses可能增加传中，或转向禁区前沿二次球。
- 预期创造的空间：右侧PressingFullBack前顶时，右侧外线由前场出口与中场覆盖接管；左侧HoldingFullBack留守形成不对称rest-defence；三中卫中两侧Covering保护肋部，中央Stopping角色承担主动接触；前场三出口在夺回球权后拉开对手后场。
- 对PPG的收益路径：恢复R4丢失的射门量与传中完成数，争取把R4非胜场1.33-1.34场均xG提升到更接近胜场2.01；更多早传/空当传球和三出口反击提高低产比赛破门概率，减少平局并转化为胜场；最终以109分验收，不以进球/xG单项替代积分。
- 可能副作用：Much Lower防线可能让对手在禁区前沿控球；High Press与深防线间距可能被利用；Invite Crosses可能增加传中与二点球；PressingFullBack前顶会留下右侧身后；两名Covering中卫过度保护可能让中央DC承担过多上抢；高节奏+直传+早传可能增加失误/越位；三出口若未回防可能造成中场人数不足。
- D5量化验证指标：完整38场积分≥109且全队xG≥100；同时记录射门、射正、xG/射门、绝佳机会、传中尝试/完成率、越位、非胜场xG/射门、主客场PPG/xGA、对手禁区内xG与绝佳机会。任何一项硬门槛未达到即FAIL；过程指标用于定位失败原因，不替代硬门槛。另记录对手传中尝试/完成与由传中产生的xG；纪律数据仅作为副作用观察，不作为战术质量门槛。

## 8. 收益—代价、风险与失败条件

| 维度 | 预期收益 | 代价/风险 | 量化观察 |
|---|---|---|---|
| 进攻产量 | 恢复Pass Into Space与Hit Early Crosses，提高射门/传中完成数 | 早传质量不足、越位/失误增加 | xG、射门、xG/shot、传中完成率、越位 |
| 前场纵深 | TargetForward与三出口反击增加禁区接应点 | 过度依赖高球、二点球无人接应 | 绝佳机会、禁区内射门、前场触球 |
| OOP转换 | 5-2-3、双后腰和三中卫形成保护层 | 角色换位熟悉度不足，右侧前顶后身后空间 | 对手xG、绝佳机会、转换后首脚推进 |
| 压迫 | 右侧/中央主动压迫，左右Covering保护 | 对手一脚转移或中路第三人破解 | 对手前场进入、直塞、禁区前沿射门 |
| 主客场 | 争取抬高低产比赛下限 | 高位压迫在客场可能更易被破解 | 主客场PPG、xG/xGA、未胜场分组 |

失败条件：
1. D1角色/职责/PI权限检查失败，禁止生成。
2. D2任一阶段位置重复/缺失，或IP四后场不满足DL/DCL/DCR/DR各一次，禁止生成。
3. D3 FMF与recipe不一致、PI/TI/风格字段未回读或独立二进制检查失败，D3=FAIL。
4. D4游戏内任何位置/角色/职责/PI/TI/心态显示与配方不符，或跨位球员熟悉度不满足用户可接受条件，暂停正式D5。
5. D5未达到38场109分或xG100任一门槛，R5整体FAIL；不得以某个位置相对领先、实际进球高于xG或D3通过豁免。

## 9. D4与D5验收清单

D4由用户在游戏内确认：
- IP显示4-2-3-1，DL/DCL/DCR/DR四后场槽正确。
- OOP显示5-2-3，三中卫、双后腰与AML/AMR/AMC三出口映射正确。
- 核对11槽22阶段的角色、职责、PI、TI和Positive心态。
- 特别核验DML→DC、DMR→DML、AMC→DMR、ST→AMC的球员位置熟悉度和实际游戏显示。
- Exporter不会推断战术身份；未来赛季映射必须由用户明确确认。

D5硬门槛：
- 38场英超至少109分，PPG≥2.85。
- 同一38场英超全队xG≥100（场均≥2.63）。
- 两项必须同时达标。

D5诊断目标：
- 射门量至少恢复到R3的452次作为过程参照；若xG/射门约0.154，则约650次射门才可能达到100 xG。650不是独立硬门槛，实际xG质量更高时可用更少射门。
- 绝佳机会、禁区内射门、传中完成率、xG/射门、非胜场xG与射门、主客场PPG、对手绝佳机会均需报告。
- 对每场平局/失利分为低创造、高质量机会未兑现、领先后丢分、转换/防守机会质量失控或数据不足；不把单场异常推广为普遍规律。

## 10. 本轮已读取的项目资料

- MASTER_UPGRADE_GUIDE.md
- AGENTS.md、UPGRADE_GATE.md、ANALYSIS_AND_ITERATION_RULES.md、GENERATION_EXECUTION_POLICY.md
- PROJECT_RULES.md、PPG_TARGET_POLICY.json、POSITION_PERFORMANCE_ELIMINATION_STANDARD.md
- TACTIC_INSTRUCTION_DECISION_LEDGER.md（含V0.5–V1.8历史配置档案、近邻差异、2.2/R3/R4记录）、VERSION_CATALOG.md、ITERATION_LOG.md、SOURCE_REGISTER.md
- HISTORICAL_REAUDIT_20261126.md、TACTICAL_RESEARCH_DECISIONS_20261126.md、INSTRUCTION_EFFECTIVENESS_AUDIT_20261126.md、ROLE_DEFAULT_BEHAVIOR_AND_MAPPING_RECHECK_20261126.md、ARCHITECTURE_REVIEW_20261126.md、ENGINE_DIVIDEND_PRIORITY_INDICATORS_27.1.1.md
- V0.5_BASELINE.md、R3.json、R4.json、2.6.json、R3_D5_SEASON_REVIEW_45850910254.md、R4_D5_SEASON_REVIEW_45914272197.md、2.2_D5_SEASON_REVIEW_20261126.md、2.6_DESIGN_AND_AUDIT.md
- 当前原生catalog.json、FM27GEN1_Offline_FMF_Generator.py、validate_project_iteration.py、build_project_tactic.py、materialize_v05_baseline.py

## 11. 状态边界

- D0：设计审计材料已形成，待项目验证器实际返回PASS。
- D1：待原生预检。
- D2：待构建入口11槽/22阶段检查。
- D3：待正式FMF、same-run report、SHA-256和8/8独立回读。
- D4：待用户游戏内导入与显示确认。
- D5：待用户确认R5赛季映射后的完整38场英超报告。




## 位置绩效高强度审查与低效淘汰

**数据边界：** R4位置表只按比赛报告位置汇总，不能等同IP/OOP战术槽位。角色码仅309/913，OOP无逐场映射；因此位置数据可写数值，其余明确U。R4团队xG58.86低于100，所有IP进攻槽均不得准入保留。

| 阶段/槽位 | 角色职责 | 分钟/覆盖 | 评分分布 | 进球/助攻 | xG/xA | 过程指标 | 证据等级 | 判决 | 下一步 |
|---|---|---:|---|---|---|---|---|---|---|
| IP-01 | GK 出球门将/策应 | 3420 | 未提供 | 0/0 | 0.00/NA | 守门数据 | C | 条件保留/未准入 | D5观察失球与扑救 |
| IP-02 | DR 翼卫/支援 | 3399 | 未提供 | 1/3 | 1.18/NA | 132传中、20.5%完成 | C | 条件保留/未准入 | WingBack A回调S，测推进/传中/回防 |
| IP-03 | DCR 中后卫/防守 | DC合并6558 | 未提供 | DC合计1/0 | DC合计2.05/NA | 左右不可拆分 | U | 条件保留/未准入 | 不归因右中卫；测失位与对手机会 |
| IP-04 | DCL 中后卫/防守 | DC合并6558 | 未提供 | DC合计1/0 | DC合计2.05/NA | 左右不可拆分 | U | 条件保留/未准入 | 不归因左中卫；测覆盖与上抢 |
| IP-05 | DL 内收边后卫/防守 | 3724 | 未提供 | 0/2 | 0.69/NA | 181传中、7.7%完成 | C | 条件保留/未准入 | 测内收接应与OOP HoldingFullBack |
| IP-06 | DML 防守中场/防守 | DMC合并6782 | 未提供 | DMC合计6/4 | DMC合计7.70/NA | 左右后腰不可拆分 | U | 条件保留/未准入 | 映射DC需D4熟悉度核验 |
| IP-07 | DMR 防守中场/防守 | DMC合并6782 | 未提供 | DMC合计6/4 | DMC合计7.70/NA | 左右后腰不可拆分 | U | 条件保留/未准入 | BoxToBox S淘汰，回到DM D |
| IP-08 | AML 内锋/进攻 | 3382 | 未提供 | 11/14 | 12.02/NA | 位置产出非角色因果 | C | 未准入 | 团队xG未达100；测xG/90与禁区触球 |
| IP-09 | AMC 自由人/进攻 | 3369 | 未提供 | 7/7 | 10.93/NA | 位置产出非角色因果 | C | 未准入 | 团队xG未达100；测创造与射门 |
| IP-10 | AMR 边锋/支援 | 3471 | 未提供 | 6/13 | 6.14/NA | 位置产出非角色因果 | C | 未准入 | 团队xG未达100；测xA/90与传中 |
| IP-11 | ST 支点前锋/进攻 | 3422 | 未提供 | 19/2 | 17.99/NA | 争顶/二点事件未提供 | C | 未准入 | 团队xG未达100；测禁区机会 |
| OOP-01 | GK 门将/策应 | 3420 | 未提供 | 0/0 | NA | OOP守门角色未导出 | U | 条件保留/未准入 | D4核对角色，D5看失球 |
| OOP-02 | DR 逼抢边后卫/防守 | 位置DR参考3399 | 未提供 | 位置DR 1/3 | 位置DR 1.18/NA | 无OOP槽归因 | U | 条件保留/未准入 | 新PressingFullBack待验证 |
| OOP-03 | DCR 补位中卫/防守 | DC合并6558 | 未提供 | DC合计1/0 | DC合计2.05/NA | 无OOP角色映射 | U | 条件保留/未准入 | 测身后球与横向覆盖 |
| OOP-04 | DCL 补位中卫/防守 | DC合并6558 | 未提供 | DC合计1/0 | DC合计2.05/NA | 无OOP角色映射 | U | 条件保留/未准入 | 测左侧覆盖与上抢 |
| OOP-05 | DL 留守边后卫/防守 | 位置DL参考3724 | 未提供 | 位置DL 0/2 | 位置DL 0.69/NA | 无OOP槽归因 | U | 条件保留/未准入 | 测HoldingFullBack落位与传中防守 |
| OOP-06 | DC 上抢中卫/防守 | DML跨阶段映射 | 未提供 | 不可拆分 | NA | OOP事件未导出 | U | 条件保留/未准入 | StoppingCentreBack新增假设 |
| OOP-07 | DML 边路补位后腰/防守 | DMC合并6782 | 未提供 | DMC合计6/4 | NA | 左右DM不可拆分 | U | 条件保留/未准入 | 测半空间补位与逼抢 |
| OOP-08 | DMR 回撤后腰/防守 | AMC跨阶段映射 | 未提供 | 不可拆分 | NA | OOP角色/PI未导出 | U | 条件保留/未准入 | Dropping DM新增假设 |
| OOP-09 | AML 内侧出口边锋/进攻 | 位置AML参考3382 | 未提供 | 位置AML 11/14 | 位置AML 12.02/NA | 不代表OOP角色贡献 | U | 条件保留/未准入 | 测夺回后接球、推进与回防 |
| OOP-10 | AMR 外侧出口边锋/进攻 | 位置AMR参考3471 | 未提供 | 位置AMR 6/13 | 位置AMR 6.14/NA | 不代表OOP角色贡献 | U | 条件保留/未准入 | 测反击宽度与推进 |
| OOP-11 | AMC 中路出口前腰/进攻 | IP ST位置参考3422 | 未提供 | IP ST 19/2 | IP ST 17.99/NA | 不代表OOP AMC贡献 | U | 条件保留/未准入 | 测反击接球与前场压迫 |

### 低效淘汰清单

1. R4整套配方：46分、PPG1.211、xG58.86，双硬门槛失败，不作为R5父版或整体模板。
2. Pass To Feet + Work Ball Into Box：R4射门408、xG58.86，低于R3的452射门/65.00xG；替换为Pass Into Space + Hit Early Crosses。此为组合级撤回，不声称单项因果。
3. DR WingBack Attack：按PPG策略回调Support；现有位置级数据不足以支持继续加大攻击职责。
4. DMR BoxToBoxMidfielder Support：按PPG策略回调DefensiveMidfielder Defend；DMC合并位置数据不能单独归因。
5. R4式Byline限制：从R5移除，避免与Hit Early Crosses方向冲突；不宣称其在所有情境无效。

### 证据等级

- A：本轮无A等级单项因果证据。
- B：R4球队级38场统计完整、关键字段对账通过，但build整体partial/unverified，且无逐场战术执行映射。
- C：位置码汇总、跨赛季描述性对照、社区观察。
- U：OOP槽位执行、角色/职责/PI/TI事件归因、左右DC/DMC拆分。

### 四类位置决策

- **准入保留：无。** R4团队xG58.86低于100，所有IP进攻槽位均不得获得准入保留；所有OOP槽位也没有足够直接数据授予“已验证有效”。
- **条件保留：** 以上22个槽位均作为R5待验证配置，不等于有效或通过绩效门禁。
- **替换淘汰：** 见低效淘汰清单；被淘汰配置不得在R5 recipe中静默复活。
- **D5：** 38场至少109分且全队xG≥100；防守槽位不使用xG评价，使用对手机会质量、禁区进入、转换防守、主客场和失分比赛。
