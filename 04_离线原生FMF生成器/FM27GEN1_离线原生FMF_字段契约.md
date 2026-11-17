# FM27GEN1 与离线原生 FMF 生成器字段契约

本契约依据仓库内 Python 源码的实际实现，不代表未来规划功能已经完成。

**交付规则：** GEN1 仅为中间配方。普通新战术生成必须继续执行离线生成，实际提供原生 .fmf 文件和同次生成的 .report.json。只做 A/B/C 阶段而未完成 D3，不得称为战术生成完成。

## 1. 四阶段职责

| 阶段 | 输入 | 输出 | 当前验收 |
|---|---|---|---|
| A 战术设计 | 用户目标、比赛数据、战术样本 | IP/OOP 阵型、角色、TI/PI 意图 | 设计依据可追溯 |
| B 原生兼容核对 | 位置、角色、phase、duty、PI 候选 | 可用配置与未解决项 | 完整 PI 权限须单独预检 |
| C GEN1 | 设计结果 | FM27GEN1 v1 TXT | Base64/JSON、11 槽、双阶段正确 |
| D 离线生成 | GEN1、原生 FMF 模板、catalog | FMF 与 JSON 报告 | 当前源码覆盖字段独立回读一致 |

## 2. GEN1 输入

- TXT 以 `FM27GEN1:` 开头，后接 Base64 编码 UTF-8 JSON。
- `v=1`；`ment` 为 1–7。
- `base.g` 当前仅支持 `Gegenpress`。
- `ti` 是一个统一对象；输出到单一 12 字节团队指令向量，不区分 IP/OOP 两套向量。
- `p` 为 11 个槽位；每槽含 `in` 和 `out`，阶段对象含 `pos`、`role`、可选 `pi`。

## 3. catalog 实际用途

catalog 含 24 个位置、79 个角色、29 组 TI 目录以及更多策略字段。当前生成器实际使用：
- `positions`
- `roles`
- `role_eligibility`
- `team_instructions`

虽然 catalog 还包含 `pi_policies`、`player_instructions`、`duties` 等字段，但当前 Python 没有使用这些字段对 PI 做完整权限裁定。

## 4. 位置和角色

- 位置须存在于 catalog positions。
- 角色名称由源码转换为内部 ID；OOP 角色 ID 使用 `OP` 前缀。
- 角色 phase 必须匹配当前 in/out 阶段。
- `role_eligibility[position][phase]` 必须包含该角色。
- IP/OOP 各自要求 11 个唯一位置。
- **OOP STC 输入会规范化为 ST 并写入 ST native selector。** 这是真正的输出行为，不是仅用于静态权限查询的 alias。

## 5. Duty

GEN1 v1 没有 duty 独立字段。源码按 role ID 使用 `ROLE_DUTY` 固定映射：
- 无映射 role 直接失败；
- Box-to-Box Midfielder 的 Support duty 在源码注释中标记为推断；
- 回读只检查 duty bit 属于 `DUTY_FLAGS`，不代表已完成每种位置/角色/phase 的 duty 权限审计。

## 6. PI 白名单

输入为 `[group, option]` 二元数组。当前接受值：

| group | options |
|---|---|
| PASSING_STRATEGY | SHORTER, MORE_DIRECT |
| PASSING_RISKS | TAKE_MORE_RISKS, TAKE_FEWER_RISKS |
| DRIBBLING_FREQUENCY | DRIBBLE_MORE, DRIBBLE_LESS |
| DRIBBLING_DIRECTION | CUT_INSIDE_WITH_BALL |
| SHOOTING | SHOOT_MORE_OFTEN, SHOOT_LESS_OFTEN |
| FORWARD_RUNS | MAKE_MORE_RUNS |
| ATTACKING_WIDTH | STAY_WIDER, SIT_NARROWER |
| MARKING | MARK_TIGHTER |
| TACKLING | EASE_OFF_TACKLES |
| TRIGGER_PRESS | MORE_OFTEN |
| ATTACK_BOX_SIDE | CENTRE, NEAR_POST, FAR_POST |

其他 pair 报错停止。脚本把白名单选项转换成 mask 并写入 TAC 的当前角色 PI cache，再独立回读比较。

**权限边界：** 当前 Python 未调用 `pi_policies` 或第 02 层完整 PI 权限 CSV，未按 phase/position/role/duty 判断 PI 是可编辑、固定开启或固定关闭。mask 回读一致不等于原生 PI 权限验证。

## 7. TI 白名单和继承

当前非默认 TI 映射：

| group | option |
|---|---|
| PASSING_DIRECTNESS | MORE_DIRECT |
| TEMPO | HIGHER |
| ATTACKING_WIDTH | WIDER |
| ATTACKING_TRANSITION | COUNTER_ATTACK |
| PLAY_FOR_SET_PIECES | KEEP_BALL_IN_PLAY |
| BUILD_UP_STRATEGY | PLAY_THROUGH_PRESS |
| GOAL_KICKS | SHORT |
| GOALKEEPER_DISTRIBUTION | CENTRE_BACKS |
| PASS_RECEPTION | PASS_INTO_SPACE |
| PATIENCE | WORK_BALL_INTO_BOX |
| SHOTS_FROM_DISTANCE | DISCOURAGE |
| LINE_OF_ENGAGEMENT | HIGH_PRESS |
| DEFENSIVE_LINE | HIGHER |
| TRIGGER_PRESS | MORE_OFTEN |
| DEFENSIVE_TRANSITION | COUNTER_PRESS |
| SHORT_GOALKEEPER_DISTRIBUTION | YES |

`TI_GROUPS` 登记的 key 可用 `DEFAULT` 清空对应选项组；其他未映射的非默认值失败。

球队向量以模板为基线。仅 GEN1 明确出现的 key 会清理或改写，未出现的 key 保留模板 bits。当前没有 IP/OOP 独立 TI 向量。

## 8. FMF 写入

模板必须包含 `.tac`、`.aom`、`.img`，TAC source-major byte 为 27。源码会：
1. 解压 TOC；
2. 对成员执行 AES-CTR 解密、Zstandard 解压及长度核对；
3. 更新 TAC 和 AOM title；
4. 重新压缩/加密变更成员；
5. 保持 IMG 成员封装字节不变；
6. 保留 TAC ID entries、footer lists、footer records；
7. 重建成员偏移和外层目录。

## 9. 独立回读

当前脚本检查：FMF 外层、成员解密与解压长度、TAC 结构、11 组 pair、22 个阶段位置/角色/PI mask、各阶段 11 个唯一位置、duty 允许集合、标题/AOM root title、TI 向量和 footer records 数量。该检查范围不包括完整 PI 权限或游戏界面字段逐项验收。

## 10. 运行参数

```powershell
py -3.12 -m pip install -r requirements.txt

py -3.12 FM27GEN1_Offline_FMF_Generator.py "FM27_A9.0.2_GEN1.txt" --template "FM27_4231_Gegenpress_Template.fmf" --catalog "catalog.json" --output "FM27_A9.0.2_Offline.fmf" --report "FM27_A9.0.2_Offline.report.json"
```

`recipe`、`--template`、`--catalog`、`--output` 必填；`--report` 可选。输出存在时拒绝覆盖。

## 11. 后续工作

1. 接入完整原生 PI 权限预检，精确到 phase/position/role/duty。
2. 扩展 TI/PI 映射并提供原生样本证据。
3. 核实 duty 来源和推断项。
4. 增加更多 FM27 build 模板、回归和失败用例。
5. 完成 FM27 导入、保存、关闭重开验收后，才进入比赛测试。

唯一迭代基线是本目录源码，不另建重复生成器，也不引入网站/API/游戏平台依赖。
