# FM27 战术研发固定边界｜2026-11-27 生效

> 本文件是当前战术研发的唯一可执行配置边界。它取代此前“除IP四后卫外，阵型、OOP、TI、心态完全开放”等旧规则。历史 recipe、FMF、报告和日志仍保留，但不得用作违反本文件约束的当前候选。

## 1. 允许的有球阵型

IP 有球阶段只允许以下三种阵型，名称必须精确登记：

| 允许阵型 | 位置槽（按项目 11 槽顺序） |
|---|---|
| 4-2-3-1 | GK、DR、DCR、DCL、DL、MCR、MCL、AMR、AML、AMC、ST |
| 4-3-3 | GK、DR、DCR、DCL、DL、MCR、MCL、AMR、AML、MC、ST |
| 4-1-2-3 | GK、DR、DCR、DCL、DL、DMC、MCL、AMR、AML、MCR、ST |

三种阵型的 IP 后场都必须且只能有 DL、DCL、DCR、DR，各一次。不得创造第四种有球阵型或临时自定义其他位置结构。

## 2. 无球阶段位置固定

OOP 位置槽与 V0.5 的 11 槽配对关系固定，不得改动：

| 槽位 | OOP 位置 |
|---:|---|
| 0 | GK |
| 1 | DR |
| 2 | DCR |
| 3 | DCL |
| 4 | DL |
| 5 | DMR |
| 6 | DML |
| 7 | MR |
| 8 | ML |
| 9 | MC |
| 10 | AMC |

允许修改这些 OOP 位置上的**球员角色、职责和个人指令**；不允许改动 OOP 的位置映射、增加/减少 OOP 位置或另行设计 OOP 阵型位置。

## 3. 红框团队指令：固定，不得修改

以下 15 组团队指令以用户 2026-11-27 提供的两张游戏截图为准。配方必须显式写入相同原生选项；不得省略、不得设为其他值，也不得用其他 PI/TI 间接覆盖其固定意图。

### 有球阶段 IP

| 截图显示的指令 | 固定游戏值 | 原生配方值 |
|---|---|---|
| 传球偏好 | 尽量直传 | `PASSING_DIRECTNESS: MORE_DIRECT` |
| 比赛节奏 | 极快 | `TEMPO: MUCH_HIGHER` |
| 进攻宽度 | 大幅收缩 | `ATTACKING_WIDTH: MUCH_NARROWER` |
| 接球 | 多传空当 | `PASS_RECEPTION: PASS_INTO_SPACE` |
| 进攻启动 | 穿透压迫 | `BUILD_UP_STRATEGY: BYPASS_PRESS` |
| 球门球 | 短传 | `GOAL_KICKS: SHORT` |
| 门将出球（速度） | 平衡 | `GK_DISTRIBUTION_(SPEED): DEFAULT` |
| 门将出球 | 中后卫 | `GOALKEEPER_DISTRIBUTION: CENTRE_BACKS` |

### 无球阶段 OOP

| 截图显示的指令 | 固定游戏值 | 原生配方值 |
|---|---|---|
| 遭遇线 | 高位逼抢 | `LINE_OF_ENGAGEMENT: HIGH_PRESS` |
| 后防线 | 大幅后撤 | `DEFENSIVE_LINE: MUCH_LOWER` |
| 防守转换 | 重组队形 | `DEFENSIVE_TRANSITION: REGROUP` |
| 抢断 | 凶狠拼抢 | `TACKLING: GET_STUCK_IN` |
| 压迫陷阱 | 平衡 | `PRESSING_TRAP: DEFAULT` |
| 干扰门将短传 | 是 | `SHORT_GOALKEEPER_DISTRIBUTION: YES` |
| 传中防御 | 放任传中 | `CROSS_ENGAGEMENT: INVITE_CROSSES` |

“平衡”对应原生选项的中性/默认值，recipe 中必须显式使用 `DEFAULT` 清除 V0.5 载体中可能存在的该组可见选项位。

## 4. 唯一允许调整的内容

以后每轮只允许调整以下三类：

1. **球员角色与职责**：IP/OOP 各位置的角色和职责可以重新组合，但必须通过当前 FM27 原生位置/阶段/角色/职责权限预检。
2. **球员个人指令 PI**：可按位置、阶段、角色、职责和原生 PI 权限调整；不能越权修改红框团队指令。
3. **非红框球队指令 TI**：以下14组可根据数据与测试结果调整：

| 原生TI键 | 游戏内指令类别 |
|---|---|
| `ATTACKING_TRANSITION` | 得球后 |
| `CREATIVE_FREEDOM` | 创造力 |
| `TIME_WASTING` | 拖延时间 |
| `PLAY_FOR_SET_PIECES` | 定位球策略 |
| `PROGRESS_THROUGH` | 推进方向 |
| `SUPPORTING_RUNS` | 支援跑动 |
| `SUPPORTING_RUNS_SECONDARY` | 次级支援跑动 |
| `GOALKEEPER_ATTACKING_SET_PIECES` | 门将参与进攻定位球 |
| `PATIENCE` | 耐心 |
| `DRIBBLING` | 盘带 |
| `SHOTS_FROM_DISTANCE` | 远程射门 |
| `CROSSING_STYLE` | 传中类型 |
| `DEFENSIVE_LINE_BEHAVIOR` | 后防线行为 |
| `TRIGGER_PRESS` | 触发压迫 |

为避免“未声明设置意外沿用”的问题，每份正式 recipe 仍须显式覆盖当前原生目录中的全部29组团队指令；其中15组固定值必须精确匹配，其余14组只在本表内可调整。

## 5. 不在允许调整范围内的字段

- IP 只能从第 1 节的三种阵型中选择；除选择对应阵型所需的位置槽变化外，不得自定义 IP 位置。
- OOP 位置映射按第 2 节锁定。
- 心态固定为 V0.5 原生值 **4**（来自 `V0.5_NATIVE_SNAPSHOT.json` 的 `tactical_metadata.mentality.native_value`），用户未授权改变。
- 原生风格字符串、FourCC 及其他未授权原生字段保持 V0.5 格式身份，不得擅自修改。

## 6. 新的研发顺序

1. 从 V0.5 原生快照重生。
2. 先在三种允许阵型中选择本轮唯一 IP 阵型。
3. 保持 OOP 11 个位置映射和心态 4 不变。
4. 设计 IP/OOP 角色、职责和 PI。
5. 只调整未被红框框住的 TI；15 项红框指令保持固定。
6. 原生预检和项目 D0 门禁必须自动验证以上规则，任一不符即禁止生成。
7. 通过后再生成 FMF、独立回读；D4 游戏导入与 D5 赛季实测仍分别验收。

## 7. 旧规则处理与历史版本状态

此前规则文件中“IP 阵型完全开放”“OOP 阵型/位置转换完全开放”“心态可自由调整”“全部 TI 可自由调整”等表述已被本文件取代。它们若出现在旧审计、旧日志或历史版本说明中，只代表当时规则，不再是当前开发指令。

R6 在旧规则下生成，IP 为 4-2-2-2，OOP 位置映射、心态及多项红框 TI 也不符合本规则。因此 R6 保留为 D0-D3 技术历史，但撤销当前候选资格，不进入 D4/D5。下一次符合本规则的版本必须重新按本文件生成。

