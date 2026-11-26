# FM27 战术历史总账｜V0.5–V1.8 完整配置与逐代差异

> **项目唯一历史配置总账。原始战术固定为 V0.5（V21 原生快照）。** 本表记录 V0.5–V1.8 每一代的赛季表现、11个槽位的IP/OOP位置、角色、职责、个人指令（PI）、球队指令（TI）、心态，以及相对上一代的明确变化。

## 1. 读表规则与证据边界

- IP=有球阶段；OOP=无球阶段；每行对应同一球员槽位在两种比赛阶段的位置转换。D=防守，S=策应，A=进攻。
- 角色名称同时保留中文释义和原始枚举；PI同时保留中文释义和原始枚举，便于逐项核验。
- V0.5来自原生快照；V0.6–V0.8由V0.5原生配置和各版正式变更清单逐项重建；V0.9–V1.8来自各版完整配方中的11组IP/OOP配置。
- V0.9–V1.8配方仅列显式TI字段；未列字段不擅自推断为沿用、关闭或默认，需以对应FMF/build report回读为准。
- V0.6/V0.7的xG/xGA为报告场均值乘38的估算值（*）。V0.7/V0.8共同赛程仅作描述性对照，不是同seed因果实验。
- V0.9的IP DCL使用边中卫角色，存在四后卫槽位资格问题；此处忠实记录历史配置，不代表认可其合规性。
- V1.7/V1.8报告部分字段为partial/unverified；球队级结果可描述，角色归因受报告覆盖限制。
- 犯规、黄牌、红牌不作为战术优劣指标。

## 2. 各代赛季表现总表

| 版本 | 战绩（胜-平-负） | 进失球 | 积分 | xG | xGA | 说明 |
|---|---:|---:|---:|---:|---:|---|
| V0.5 | 20-9-9 | 75:43 | 69 | 72.92 | 44.12 | 完整38场；V21原生快照 |
| V0.6 | 20-8-10 | 83:49 | 68 | 80.10* | 44.92* | *xG/xGA由报告场均值乘38估算 |
| V0.7 | 15-8-15 | 70:58 | 53 | 68.78* | 56.43* | *由报告场均值乘38估算；与V0.6有36场共同联赛对阵 |
| V0.8 | 19-9-10 | 79:46 | 66 | 82.07 | 44.01 | 完整38场；与V0.7有33场共同对阵 |
| V0.9 | 25-5-8 | 86:48 | 80 | 73.83 | 43.24 | 完整38场；DCL有球边中卫存在四后卫槽位合规问题 |
| V1.0 | 27-6-5 | 107:35 | 87 | 85.40 | 40.07 | 完整38场；实际进球高于xG、失球低于xGA |
| V1.1 | 19-10-9 | 84:48 | 67 | 81.73 | 52.53 | 完整38场；OOP 5-2-3 |
| V1.2 | 26-8-4 | 72:29 | 86 | 70.31 | 39.97 | 完整38场；OOP回四后卫+双后腰屏障 |
| V1.3 | 27-7-4 | 83:30 | 88 | 80.54 | 34.27 | 完整38场；历史防守机会质量最佳 |
| V1.4 | 27-2-9 | 101:53 | 83 | 92.62 | 43.46 | 完整38场；进攻产量高、防守机会质量回落 |
| V1.5 | 25-3-10 | 95:48 | 78 | 77.29 | 40.51 | 完整38场；心态原生值3、防线较低 |
| V1.6 | 28-5-5 | 87:37 | 89 | 75.54 | 46.33 | 完整38场；历史最高积分 |
| V1.7 | 25-7-6 | 79:36 | 82 | 74.29 | 44.13 | 完整38场；报告partial/unverified |
| V1.8 | 21-9-8 | 98:55 | 72 | 88.87 | 59.67 | 完整38场；报告partial/unverified；OOP无锋5-2-3 |

## 3. 每一代相对上一代的明确改动

### V0.5 → V0.6

**本版赛季表现：** 20-8-10，83:49，68分；xG 80.10* / xGA 44.92*。

**逐项差异：**

- **IP DR：** PI「进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）」→「进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST）」
- **IP DL：** PI「进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）」→「进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST）」
- **IP ST：** PI「射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=前点（ATTACK_BOX_SIDE:NEAR_POST）」→「射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST）」
- **补充：** 球队指令20项全部沿用V0.5；PI变化：DR、DL增加后点传中；ST禁区攻击方向由前点改后点。

### V0.6 → V0.7

**本版赛季表现：** 15-8-15，70:58，53分；xG 68.78* / xGA 56.43*。

**逐项差异：**

- **IP MCR：** 角色 肋部中场→中前卫；职责 进攻→策应；PI「传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）」→「传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION）」
- **IP AMC：** 角色 肋部中场→前场组织核心；职责 进攻→策应；PI「传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）」→「跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）」
- **补充：** 球队指令：比赛节奏 极高→较高；进攻宽度 极窄→较窄；逼抢频率 极多→较多。

### V0.7 → V0.8

**本版赛季表现：** 19-9-10，79:46，66分；xG 82.07 / xGA 44.01。

**逐项差异：**

- **IP AMC：** 职责 策应→进攻；PI「跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）」→「跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）」
- **补充：** 球队指令：比赛节奏 较高→极高；进攻宽度 较窄→极窄；逼抢频率 较多→极多。

### V0.8 → V0.9

**本版赛季表现：** 25-5-8，86:48，80分；xG 73.83 / xGA 43.24。

**逐项差异：**

- **IP DR：** 职责 策应→进攻
- **IP DCL：** 角色 中后卫→边中卫
- **IP DL：** 角色 边后卫→内收型边后卫；职责 策应→防守；PI「进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST）」→「传球距离=短传（PASSING_STRATEGY:SHORTER）」
- **OOP MCR：** PI「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；指定盯防位置=ST（MARKING_TARGET:ST）」→「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **IP AMR：** PI「—」→「传球距离=短传（PASSING_STRATEGY:SHORTER）」
- **IP AML：** PI「—」→「传球距离=短传（PASSING_STRATEGY:SHORTER）」
- **IP ST：** 角色 拉边前锋→抢点前锋；PI「射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST）」→「射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST）」
- **补充：** 球队指令：比赛节奏 极高→较高；进攻宽度 极窄→较窄；防线高度 极低→较低；逼抢频率 极多→较多。其余TI以原生FMF/build回读核实，不从配方缺省推断。

### V0.9 → V1.0

**本版赛季表现：** 27-6-5，107:35，87分；xG 85.40 / xGA 40.07。

**逐项差异：**

- **补充：** 球队指令：进攻宽度 较窄→默认；防线高度 较低→默认。

### V1.0 → V1.1

**本版赛季表现：** 19-10-9，84:48，67分；xG 81.73 / xGA 52.53。

**逐项差异：**

- **OOP位置 DR：** DR→WBR
- **OOP位置 DL：** DL→WBL
- **OOP位置 MCR：** DMR→DC
- **OOP位置 MCL：** DML→DMR
- **OOP位置 AMR：** MR→AMR
- **OOP位置 AML：** ML→AML
- **OOP位置 AMC：** MC→DML
- **OOP DR：** 角色 逼抢边后卫→逼抢翼卫；职责 策应→防守
- **OOP DCR：** 角色 补位中卫→补位边中卫；PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **IP DCL：** 角色 边中卫→中后卫
- **OOP DCL：** 角色 中后卫→补位边中卫
- **OOP DL：** 角色 逼抢边后卫→逼抢翼卫；职责 策应→防守
- **OOP MCR：** 角色 回撤后腰→中后卫；PI「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP MCL：** 角色 防守中场→逼抢型防守中场；PI「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP AMR：** 角色 回防边前卫→边锋；职责 防守→策应
- **OOP AML：** 角色 回防边前卫→边锋；职责 防守→策应
- **OOP AMC：** 角色 中前卫→屏障型防守中场；职责 策应→防守；PI「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **补充：** 结构变化：OOP从四后卫+双后腰/双边前卫/MC/AMC整体改为5-2-3；IP DCL边中卫改为中后卫。

### V1.1 → V1.2

**本版赛季表现：** 26-8-4，72:29，86分；xG 70.31 / xGA 39.97。

**逐项差异：**

- **OOP位置 DR：** WBR→DR
- **OOP位置 DL：** WBL→DL
- **OOP位置 MCR：** DC→DMR
- **OOP位置 MCL：** DMR→DML
- **OOP位置 AMR：** AMR→MR
- **OOP位置 AML：** AML→ML
- **OOP位置 AMC：** DML→MC
- **OOP DR：** 角色 逼抢翼卫→防守型边后卫；PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「—」
- **OOP DCR：** 角色 补位边中卫→中后卫；PI「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」
- **OOP DCL：** 角色 补位边中卫→补位中卫；PI「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」
- **OOP DL：** 角色 逼抢翼卫→逼抢边后卫；职责 防守→策应；PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP MCR：** 角色 中后卫→宽幅覆盖型防守中场
- **OOP MCL：** 角色 逼抢型防守中场→屏障型防守中场；PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「—」
- **OOP AMR：** 角色 边锋→回防边前卫；职责 策应→防守
- **OOP AML：** 角色 边锋→回防边前卫；职责 策应→防守
- **OOP AMC：** 角色 屏障型防守中场→屏障型中前卫；PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「—」
- **OOP ST：** 角色 进攻型中场→分离出球点进攻中场；职责 策应→进攻；PI「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）」
- **补充：** 结构变化：OOP从V1.1的5-2-3回到四后卫+双后腰/边前卫/屏障中场/前腰。

### V1.2 → V1.3

**本版赛季表现：** 27-7-4，83:30，88分；xG 80.54 / xGA 34.27。

**逐项差异：**

- **IP MCR：** PI「传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION）」→「传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）」
- **补充：** 球队指令：进攻宽度 默认→较宽。

### V1.3 → V1.4

**本版赛季表现：** 27-2-9，101:53，83分；xG 92.62 / xGA 43.46。

**逐项差异：**

- **IP AML：** 角色 组织型边锋→内锋；职责 策应→进攻；PI「传球距离=短传（PASSING_STRATEGY:SHORTER）」→「传球距离=短传（PASSING_STRATEGY:SHORTER）；盘带方向=持球内切（DRIBBLING_DIRECTION:CUT_INSIDE_WITH_BALL）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）」
- **补充：** IP AML：组织型边锋（策应）→内锋（进攻），同时更换角色允许的个人指令。

### V1.4 → V1.5

**本版赛季表现：** 25-3-10，95:48，78分；xG 77.29 / xGA 40.51。

**逐项差异：**

- **心态：** 原生值 4→3
- **补充：** 球队指令：防线高度 默认→较低。心态原生值4→3。

### V1.5 → V1.6

**本版赛季表现：** 28-5-5，87:37，89分；xG 75.54 / xGA 46.33。

**逐项差异：**

- **OOP MCR：** PI「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）」
- **OOP MCL：** 角色 屏障型防守中场→逼抢型防守中场
- **心态：** 原生值 3→4
- **补充：** OOP DML：屏障型防守中场→逼抢型防守中场，职责仍为防守。

### V1.6 → V1.7

**本版赛季表现：** 25-7-6，79:36，82分；xG 74.29 / xGA 44.13。

**逐项差异：**

- **OOP MCR：** PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」
- **OOP MCL：** 角色 逼抢型防守中场→屏障型防守中场
- **补充：** OOP DML：逼抢型防守中场→屏障型防守中场，职责仍为防守。

### V1.7 → V1.8

**本版赛季表现：** 21-9-8，98:55，72分；xG 88.87 / xGA 59.67。

**逐项差异：**

- **OOP位置 DR：** DR→WBR
- **OOP位置 DL：** DL→WBL
- **OOP位置 MCR：** DMR→DC
- **OOP位置 MCL：** DML→DMR
- **OOP位置 AMR：** MR→AMR
- **OOP位置 AML：** ML→AML
- **OOP位置 AMC：** MC→DML
- **OOP DR：** 角色 防守型边后卫→逼抢翼卫；PI「—」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP DCR：** 角色 中后卫→补位边中卫；PI「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP DCL：** 角色 补位中卫→补位边中卫；PI「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP DL：** 角色 逼抢边后卫→逼抢翼卫；职责 策应→防守；PI「逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP MCR：** 角色 宽幅覆盖型防守中场→中后卫；PI「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」→「逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **OOP MCL：** 角色 屏障型防守中场→宽幅覆盖型防守中场；PI「—」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）」
- **OOP AMR：** 角色 回防边前卫→边锋；职责 防守→策应
- **OOP AML：** 角色 回防边前卫→边锋；职责 防守→策应
- **OOP AMC：** 角色 屏障型中前卫→屏障型防守中场；PI「—」→「铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）」
- **补充：** 结构变化：OOP从四后卫+双后腰屏障改为无锋5-2-3：DR/DL转WBR/WBL；DCR/DCL转补位边中卫；MCR转DC；MCL转DMR；AMR/AML变双边锋；AMC转DML；ST转AMC分离出球点进攻中场。

## 4. 每一代完整战术配置快照

下表每个版本均列出全部11个槽位的IP/OOP位置、角色、职责和显式PI。PI为“—”表示该阶段没有显式PI，不表示角色默认行为为空。

### V0.5｜20-9-9｜69分｜心态原生值 4

**赛季表现：** 75:43；xG 72.92；xGA 44.12。完整38场；V21原生快照

**球队指令：**

| 指令 | 值 |
|---|---|
| 传球方式 | 直传 |
| 接球方式 | 传入空当 |
| 后场组织 | 通过传递破解逼抢 |
| 传中方式 | 弧线传中 |
| 盘带 | 更多盘带突破 |
| 远射 | 减少远射 |
| 肋部套上 | 两翼内套 |
| 门将出球目标 | 中后卫 |
| 球门球 | 短传 |
| 比赛节奏 | 极高 |
| 进攻宽度 | 极窄 |
| 得球后 | 立刻反击 |
| 防线高度 | 极低 |
| 防守介入线 | 高位逼抢 |
| 逼抢频率 | 极多 |
| 阻止门将短传 | 是 |
| 丢球后 | 重新组织防守 |
| 铲抢 | 凶狠铲抢 |
| 拖延时间 | 有时 |
| 防守传中 | 允许传中 |

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER） | DR 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位中卫（CoveringCentreBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 边后卫（FullBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER） | DL 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 回撤后腰（DroppingDefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；指定盯防位置=ST（MARKING_TARGET:ST） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 防守中场（DefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | — | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | — | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | MC 中前卫（CentralMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 拉边前锋（ChannelForward）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=前点（ATTACK_BOX_SIDE:NEAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V0.5.json) · [赛季分析](./V0.5_SEASON_REPORT_ANALYSIS_45540803100.md)

### V0.6｜20-8-10｜68分｜心态原生值 4

**赛季表现：** 83:49；xG 80.10*；xGA 44.92*。*xG/xGA由报告场均值乘38估算

**球队指令：**

| 指令 | 值 |
|---|---|
| 传球方式 | 直传 |
| 接球方式 | 传入空当 |
| 后场组织 | 通过传递破解逼抢 |
| 传中方式 | 弧线传中 |
| 盘带 | 更多盘带突破 |
| 远射 | 减少远射 |
| 肋部套上 | 两翼内套 |
| 门将出球目标 | 中后卫 |
| 球门球 | 短传 |
| 比赛节奏 | 极高 |
| 进攻宽度 | 极窄 |
| 得球后 | 立刻反击 |
| 防线高度 | 极低 |
| 防守介入线 | 高位逼抢 |
| 逼抢频率 | 极多 |
| 阻止门将短传 | 是 |
| 丢球后 | 重新组织防守 |
| 铲抢 | 凶狠铲抢 |
| 拖延时间 | 有时 |
| 防守传中 | 允许传中 |

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位中卫（CoveringCentreBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 边后卫（FullBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DL 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 回撤后腰（DroppingDefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；指定盯防位置=ST（MARKING_TARGET:ST） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 防守中场（DefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | — | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | — | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | MC 中前卫（CentralMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 拉边前锋（ChannelForward）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V0.6.json) · [赛季分析](./V0.6_REANALYSIS_45554864463.md)

### V0.7｜15-8-15｜53分｜心态原生值 4

**赛季表现：** 70:58；xG 68.78*；xGA 56.43*。*由报告场均值乘38估算；与V0.6有36场共同联赛对阵

**球队指令：**

| 指令 | 值 |
|---|---|
| 传球方式 | 直传 |
| 接球方式 | 传入空当 |
| 后场组织 | 通过传递破解逼抢 |
| 传中方式 | 弧线传中 |
| 盘带 | 更多盘带突破 |
| 远射 | 减少远射 |
| 肋部套上 | 两翼内套 |
| 门将出球目标 | 中后卫 |
| 球门球 | 短传 |
| 比赛节奏 | 较高 |
| 进攻宽度 | 较窄 |
| 得球后 | 立刻反击 |
| 防线高度 | 极低 |
| 防守介入线 | 高位逼抢 |
| 逼抢频率 | 较多 |
| 阻止门将短传 | 是 |
| 丢球后 | 重新组织防守 |
| 铲抢 | 凶狠铲抢 |
| 拖延时间 | 有时 |
| 防守传中 | 允许传中 |

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位中卫（CoveringCentreBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 边后卫（FullBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DL 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION） | DMR 回撤后腰（DroppingDefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；指定盯防位置=ST（MARKING_TARGET:ST） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 防守中场（DefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | — | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | — | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/策应 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | MC 中前卫（CentralMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 拉边前锋（ChannelForward）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V0.7.json) · [赛季分析](./V0.7_REANALYSIS_45564413834.md)

### V0.8｜19-9-10｜66分｜心态原生值 4

**赛季表现：** 79:46；xG 82.07；xGA 44.01。完整38场；与V0.7有33场共同对阵

**球队指令：**

| 指令 | 值 |
|---|---|
| 传球方式 | 直传 |
| 接球方式 | 传入空当 |
| 后场组织 | 通过传递破解逼抢 |
| 传中方式 | 弧线传中 |
| 盘带 | 更多盘带突破 |
| 远射 | 减少远射 |
| 肋部套上 | 两翼内套 |
| 门将出球目标 | 中后卫 |
| 球门球 | 短传 |
| 比赛节奏 | 极高 |
| 进攻宽度 | 极窄 |
| 得球后 | 立刻反击 |
| 防线高度 | 极低 |
| 防守介入线 | 高位逼抢 |
| 逼抢频率 | 极多 |
| 阻止门将短传 | 是 |
| 丢球后 | 重新组织防守 |
| 铲抢 | 凶狠铲抢 |
| 拖延时间 | 有时 |
| 防守传中 | 允许传中 |

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位中卫（CoveringCentreBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 边后卫（FullBack）/策应 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DL 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION） | DMR 回撤后腰（DroppingDefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；指定盯防位置=ST（MARKING_TARGET:ST） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 防守中场（DefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | — | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | — | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 中前卫（CentralMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 拉边前锋（ChannelForward）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V0.8.json) · [赛季分析](./V0.8_SEASON_REPORT_ANALYSIS_45570292427.md)

### V0.9｜25-5-8｜80分｜心态原生值 4

**赛季表现：** 86:48；xG 73.83；xGA 43.24。完整38场；DCL有球边中卫存在四后卫槽位合规问题

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较窄 |
| DEFENSIVE_LINE | 防线高度 | 较低 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位中卫（CoveringCentreBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 边中卫（WideCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION） | DMR 回撤后腰（DroppingDefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 防守中场（DefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 中前卫（CentralMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V0.9.json) · [赛季分析](./V0.9_SEASON_REPORT_ANALYSIS_45584292488.md)

### V1.0｜27-6-5｜87分｜心态原生值 4

**赛季表现：** 107:35；xG 85.40；xGA 40.07。完整38场；实际进球高于xG、失球低于xGA

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 默认 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位中卫（CoveringCentreBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 边中卫（WideCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION） | DMR 回撤后腰（DroppingDefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 防守中场（DefensiveMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 中前卫（CentralMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V1.0.json) · [赛季分析](./V1.0_SEASON_REPORT_ANALYSIS_45602694823.md)

### V1.1｜19-10-9｜67分｜心态原生值 4

**赛季表现：** 84:48；xG 81.73；xGA 52.53。完整38场；OOP 5-2-3

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 默认 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | WBR 逼抢翼卫（PressingWingBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位边中卫（CoveringWideCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位边中卫（CoveringWideCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | WBL 逼抢翼卫（PressingWingBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION） | DC 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DMR 逼抢型防守中场（PressingDefensiveMidfielder）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | AMR 边锋（Winger）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | AML 边锋（Winger）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 进攻型中场（AttackingMidfielder）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |

**来源：** [配方](./V1.1.json) · [赛季分析](./V1.1_SEASON_REPORT_ANALYSIS_45617475212.md)

### V1.2｜26-8-4｜86分｜心态原生值 4

**赛季表现：** 72:29；xG 70.31；xGA 39.97。完整38场；OOP回四后卫+双后腰屏障

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 默认 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 防守型边后卫（HoldingFullBack）/防守 | — |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位中卫（CoveringCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=保持位置（FORWARD_RUNS:KEEP_POSITION） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | — |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 屏障型中前卫（ScreeningCentralMidfielder）/防守 | — |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.2.json) · [赛季分析](./V1.2_SEASON_REPORT_ANALYSIS_45635282210.md)

### V1.3｜27-7-4｜88分｜心态原生值 4

**赛季表现：** 83:30；xG 80.54；xGA 34.27。完整38场；历史防守机会质量最佳

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较宽 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 防守型边后卫（HoldingFullBack）/防守 | — |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位中卫（CoveringCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | — |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 屏障型中前卫（ScreeningCentralMidfielder）/防守 | — |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.3.json) · [赛季分析](./V1.3_SEASON_REPORT_ANALYSIS_45644106773.md)

### V1.4｜27-2-9｜83分｜心态原生值 4

**赛季表现：** 101:53；xG 92.62；xGA 43.46。完整38场；进攻产量高、防守机会质量回落

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较宽 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 防守型边后卫（HoldingFullBack）/防守 | — |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位中卫（CoveringCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | — |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 内锋（InsideForward）/进攻 | 传球距离=短传（PASSING_STRATEGY:SHORTER）；盘带方向=持球内切（DRIBBLING_DIRECTION:CUT_INSIDE_WITH_BALL）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 屏障型中前卫（ScreeningCentralMidfielder）/防守 | — |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.4.json) · [赛季分析](./V1.4_SEASON_REPORT_ANALYSIS_45727738275.md)

### V1.5｜25-3-10｜78分｜心态原生值 3

**赛季表现：** 95:48；xG 77.29；xGA 40.51。完整38场；心态原生值3、防线较低

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较宽 |
| DEFENSIVE_LINE | 防线高度 | 较低 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 防守型边后卫（HoldingFullBack）/防守 | — |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位中卫（CoveringCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | — |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 内锋（InsideForward）/进攻 | 传球距离=短传（PASSING_STRATEGY:SHORTER）；盘带方向=持球内切（DRIBBLING_DIRECTION:CUT_INSIDE_WITH_BALL）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 屏障型中前卫（ScreeningCentralMidfielder）/防守 | — |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.5.json) · [赛季分析](./V1.5_SEASON_REPORT_ANALYSIS_45734426186.md)

### V1.6｜28-5-5｜89分｜心态原生值 4

**赛季表现：** 87:37；xG 75.54；xGA 46.33。完整38场；历史最高积分

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较宽 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 防守型边后卫（HoldingFullBack）/防守 | — |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位中卫（CoveringCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 逼抢型防守中场（PressingDefensiveMidfielder）/防守 | — |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 内锋（InsideForward）/进攻 | 传球距离=短传（PASSING_STRATEGY:SHORTER）；盘带方向=持球内切（DRIBBLING_DIRECTION:CUT_INSIDE_WITH_BALL）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 屏障型中前卫（ScreeningCentralMidfielder）/防守 | — |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.6.json) · [赛季分析](./V1.6_SEASON_REPORT_ANALYSIS_45744550318.md)

### V1.7｜25-7-6｜82分｜心态原生值 4

**赛季表现：** 79:36；xG 74.29；xGA 44.13。完整38场；报告partial/unverified

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较宽 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | DR 防守型边后卫（HoldingFullBack）/防守 | — |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位中卫（CoveringCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DL 逼抢边后卫（PressingFullBack）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | — |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | MR 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 内锋（InsideForward）/进攻 | 传球距离=短传（PASSING_STRATEGY:SHORTER）；盘带方向=持球内切（DRIBBLING_DIRECTION:CUT_INSIDE_WITH_BALL）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | ML 回防边前卫（TrackingWideMidfielder）/防守 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | MC 屏障型中前卫（ScreeningCentralMidfielder）/防守 | — |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.7.json) · [赛季分析](./V1.7_SEASON_REPORT_ANALYSIS_45748944770.md)

### V1.8｜21-9-8｜72分｜心态原生值 4

**赛季表现：** 98:55；xG 88.87；xGA 59.67。完整38场；报告partial/unverified；OOP无锋5-2-3

**球队指令：**

| 原始字段 | 中文字段 | 配方显式值 |
|---|---|---|
| TEMPO | 比赛节奏 | 较高 |
| ATTACKING_WIDTH | 进攻宽度 | 较宽 |
| DEFENSIVE_LINE | 防线高度 | 默认 |
| TRIGGER_PRESS | 逼抢频率 | 较多 |

> 本版配方显式列出 4 个TI字段；其余字段不从缺省状态推断。

| 槽位 | IP位置/角色/职责 | IP显式PI | OOP位置/角色/职责 | OOP显式PI |
|---|---|---|---|---|
| GK | GK 出球门将（BallPlayingGoalkeeper）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | GK 清道夫门将（SweeperKeeper）/进攻 | 铲抢=谨慎铲抢（TACKLING:EASE_OFF_TACKLES） |
| DR | DR 翼卫（WingBack）/进攻 | 进攻站位=拉开宽度（ATTACKING_WIDTH:STAY_WIDER）；传中目标=后点（CROSSING_TARGET:BACK_POST） | WBR 逼抢翼卫（PressingWingBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCR | DCR 出球中卫（BallPlayingCentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCR 补位边中卫（CoveringWideCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DCL | DCL 中后卫（CentreBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | DCL 补位边中卫（CoveringWideCentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| DL | DL 内收型边后卫（InsideFullBack）/防守 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | WBL 逼抢翼卫（PressingWingBack）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCR | MCR 中前卫（CentralMidfielder）/策应 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DC 中后卫（CentreBack）/防守 | 逼抢=更少（TRIGGER_PRESS:LESS_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| MCL | MCL 肋部中场（ChannelMidfielder）/进攻 | 传球风险=减少冒险传球（PASSING_RISKS:TAKE_FEWER_RISKS）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | DMR 宽幅覆盖型防守中场（WideCoverDefensiveMidfielder）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN）；逼抢=更少（TRIGGER_PRESS:LESS_OFTEN） |
| AMR | AMR 组织型边锋（PlaymakingWinger）/策应 | 传球距离=短传（PASSING_STRATEGY:SHORTER） | AMR 边锋（Winger）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AML | AML 内锋（InsideForward）/进攻 | 传球距离=短传（PASSING_STRATEGY:SHORTER）；盘带方向=持球内切（DRIBBLING_DIRECTION:CUT_INSIDE_WITH_BALL）；跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION） | AML 边锋（Winger）/策应 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN）；铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| AMC | AMC 前场组织核心（AdvancedPlaymaker）/进攻 | 跑位自由度=自由跑位（ROAMING:ROAM_FROM_POSITION）；前插=更多前插（FORWARD_RUNS:MAKE_MORE_RUNS） | DML 屏障型防守中场（ScreeningDefensiveMidfielder）/防守 | 铲抢=凶狠铲抢（TACKLING:GET_STUCK_IN） |
| ST | ST 抢点前锋（Poacher）/进攻 | 射门倾向=更多射门（SHOOTING:SHOOT_MORE_OFTEN）；禁区进攻方向=后点（ATTACK_BOX_SIDE:FAR_POST） | AMC 分离出球点进攻中场（SplittingOutletAttackingMidfielder）/进攻 | 逼抢=更多（TRIGGER_PRESS:MORE_OFTEN） |

**来源：** [配方](./V1.8.json) · [赛季分析](./V1.8_SEASON_REPORT_ANALYSIS_45753659141.md)

## 5. V0.5 原始战术身份

- 原始文件：`V21_Leaderboard_TeamInstructions(1).fmf`
- SHA-256：`e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`
- 心态原生值：4；style string为空；FourCC `4c4c554e`。
- [V0.5原生基准与20项TI/35项PI清单](./V0.5_BASELINE.md) · [角色/PI审计](./V0.5_ROLE_PI_AUDIT_45540803100.md)

## 6. 后续版本录入规则

每新增一版，必须追加完整11槽×IP/OOP配置、相对父版本的逐字段差异、TI/心态原生值、对应赛季结果与报告质量限制。新增/删除PI必须单独列明；不能只写“阵型变化”“加强进攻”“调整防守”等概括语。

