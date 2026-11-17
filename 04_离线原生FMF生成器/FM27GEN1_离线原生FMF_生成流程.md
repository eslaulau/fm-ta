# FM27GEN1 离线原生 FMF 生成流程

**执行源码：** `FM27GEN1_Offline_FMF_Generator.py`  
**目标格式：** FM27 source-major 27 原生 FMF  
**运行平台：** Windows / Python 3.12 x64

本流程按当前仓库 Python 源码实际实现编写。**本流程的正式产物是新生成的原生 .fmf 和同次生成的 .report.json；GEN1 TXT 仅为输入配方。** 离线结构回读、FM27 游戏内导入和比赛效果是三个不同验收阶段。

## 1. 本目录运行文件

以下文件必须保持同目录：

| 文件 | 用途 |
|---|---|
| `FM27GEN1_Offline_FMF_Generator.py` | 生成器源码 |
| `requirements.txt` | 依赖 |
| `安装依赖.bat` | 依赖安装入口 |
| `运行离线生成器.bat` | 默认样本/拖入 GEN1 的运行入口 |
| `catalog.json` | 原生位置、角色、兼容关系和 TI 目录 |
| `FM27_4231_Gegenpress_Template.fmf` | BAT 默认原生模板 |
| `123_Game_Export_Reference.fmf` | 原生导出参考样本 |
| `FM27_A9.0.2_GEN1.txt` | A9.0.2 GEN1 输入 |
| `FM27_A9.0.2_Offline_Rebuild.fmf` | A9.0.2 输出样本 |
| `FM27_A9.0.2_Offline_Rebuild.report.json` | 离线回读报告 |

当前 catalog 有 24 个位置、79 个角色、29 组球队指令目录及 role/position/phase eligibility。源码实际使用 `positions`、`roles`、`role_eligibility`、`team_instructions`。其他 catalog 字段不代表生成器已经实现对应逻辑。

## 2. 安装环境

安装 Python 3.12 x64。在本目录运行：

```powershell
py -3.12 -m pip install -r requirements.txt
```

依赖为 `cryptography>=42` 与 `zstandard>=0.25`。也可双击 `安装依赖.bat`。运行生成器不需要连接网站或游戏平台。

## 3. GEN1 输入契约

输入 TXT 必须以 `FM27GEN1:` 开头，后接严格 Base64 编码的 UTF-8 JSON。源码要求：
- 根版本 `v=1`；
- `p` 为 11 个槽位，每个槽位具有 `in`、`out`；
- `ment` 为 1–7；
- `base.g` 能匹配已实现的 style；
- `ti` 是一个统一的球队指令对象；
- 阶段对象提供 `pos`、`role` 和可选 `pi`。

当前 `STYLE_CODE` 只实现 `Gegenpress`。其他风格直接失败，不会自动转换。

## 4. 位置、角色和 duty

- 位置必须存在于 catalog 的 `positions`。
- 角色名称按源码规则转换为角色 ID，并在 `roles` 中存在；OOP 角色使用 `OP` 前缀。
- 角色 phase 必须与 in/out 阶段一致。
- `role_eligibility[position][phase]` 必须允许当前角色。
- IP 与 OOP 分别要求 11 个唯一位置。
- **OOP STC 特例：** 源码在写入和回读时均把 OOP 输入的 `STC` 规范化为 `ST`，最终写入的是原生 ST selector。这不只是查权限时使用的别名。

GEN1 v1 没有 duty 独立字段。源码通过固定 `ROLE_DUTY` 按角色写入 duty bit。无映射角色会失败；Box-to-Box Midfielder 的 Support duty 在源码注释中明确标记为推断。回读仅检查 duty 是否属于代码允许集合，不构成完整 duty 权限来源证明。

## 5. PI 白名单

PI 格式为 `[[group, option], ...]`。当前源码仅接受以下 pair：

| group | option |
|---|---|
| PASSING_STRATEGY | SHORTER、MORE_DIRECT |
| PASSING_RISKS | TAKE_MORE_RISKS、TAKE_FEWER_RISKS |
| DRIBBLING_FREQUENCY | DRIBBLE_MORE、DRIBBLE_LESS |
| DRIBBLING_DIRECTION | CUT_INSIDE_WITH_BALL |
| SHOOTING | SHOOT_MORE_OFTEN、SHOOT_LESS_OFTEN |
| FORWARD_RUNS | MAKE_MORE_RUNS |
| ATTACKING_WIDTH | STAY_WIDER、SIT_NARROWER |
| MARKING | MARK_TIGHTER |
| TACKLING | EASE_OFF_TACKLES |
| TRIGGER_PRESS | MORE_OFTEN |
| ATTACK_BOX_SIDE | CENTRE、NEAR_POST、FAR_POST |

未知 pair 会报错，不会静默忽略。

**权限边界：** 当前 Python 未调用 catalog 的 `pi_policies`，也未读取第 02 层完整 PI 权限 CSV，逐项判断特定 phase/position/role/duty 下 PI 是可编辑、固定开启还是固定关闭。PI mask 回读一致只证明写入/读取一致，不等于原生 PI 权限通过。必须另行使用第 02 层资料核对。

## 6. TI 向量规则

源码使用一个 `ti` 对象写入单一 12 字节球队指令向量，**没有将 IP 与 OOP TI 分别写为两套独立向量**。

当前非默认映射如下：

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

`TI_GROUPS` 登记的 key 还可使用 `DEFAULT` 清除对应原生选项位。未知 key 或未映射的非默认值会失败。

向量从模板现有值开始；**仅 GEN1 明确提供的 TI key 会被清理或改写**。未出现的 key 保留模板中的 bits。因此应明确填入所有需要设定/重置的指令组，并审计模板原有 TI，不能把未出现理解成自动 DEFAULT。

## 7. 模板要求与二进制写入

模板必须是 FM27 游戏导出的原生 FMF，包含 `.tac`、`.aom`、`.img`，且 TAC source-major byte 为 27。源码实际执行：
1. 检查 FMF outer magic/封装字段并解压 TOC；
2. 对成员执行 AES-CTR 解密、Zstandard 解压及长度检查；
3. 解析 TAC 的 11 组 IP/OOP pairs；
4. 更新战术名、心态、Gegenpress style、单一 TI 向量；
5. 更新 22 个阶段位置、角色/duty mask 和当前角色 PI mask；
6. 重写 TAC，并更新 AOM 中唯一匹配的战术标题；
7. 对变更后的 TAC/AOM 重新压缩和加密，IMG 成员保持原字节；
8. 保留 TAC 原有 ID entries、footer lists、footer records，重建 FMF 偏移和目录表；
9. 从输出文件重新解析并独立回读。

模板缺失成员、结构不符或 source-major 不是 27 时停止。

## 8. 运行命令

以下命令中的 NEW_TACTIC_GEN1.txt 必须是本次新生成并完成预检的 GEN1 配方；输出文件名必须是本次独立名称，不能复用 A9.0.2 历史样本。

从本目录运行：

```powershell
py -3.12 FM27GEN1_Offline_FMF_Generator.py "NEW_TACTIC_GEN1.txt" --template "FM27_4231_Gegenpress_Template.fmf" --catalog "catalog.json" --output "NEW_TACTIC.fmf" --report "NEW_TACTIC.report.json"
```

| 参数 | 规则 |
|---|---|
| `recipe` | 必填位置参数，GEN1 TXT |
| `--template` | 必填，原生 FMF 模板 |
| `--catalog` | 必填，catalog.json |
| `--output` | 必填，新 FMF 路径 |
| `--report` | 可选；省略时使用输出路径对应的 .report.json |

输出路径已存在时拒绝覆盖。成功返回 0，失败返回 2。只有退出码为 0、FMF 实际存在且非空、JSON 报告存在并且独立回读通过，才算完成 D3；若任何条件未满足，任务保持未完成，不得以 GEN1 TXT 代替 FMF。

BAT：
- 双击 `运行离线生成器.bat`：使用内置 A9.0.2 回归输入，只用于生成器测试；
- 将本次 GEN1 TXT 拖到 BAT：在该输入文件同目录生成 `_Offline.fmf`。拖入配方才会针对新战术执行生成。

## 9. 回读报告与游戏验收

每次正式交付必须把本次 FMF 与对应报告一起提供；GEN1 可以附带但不是最终战术文件。报告状态为离线回读通过时仍须等待用户在 FM27 中完成 D4。

源码会独立检查 FMF 外层、全部成员解密/解压长度、TAC 完整解析、11 组 IP/OOP、22 个阶段位置/角色/PI mask、唯一位置、duty 允许集合、标题/AOM、单一 TI 向量和 footer records。

报告状态为 `offline_binary_roundtrip_verified_not_game_import_verified`，并固定记录 `game_interactive_import=false`、`match_engine=false`。这是程序本身不启动游戏的机器验证边界。

用户此前已确认 A9.0.2 样本在 FM27 内成功载入阵型。该后续人工确认不修改原始报告字段，也不代表所有 PI/TI、其他战术或比赛效果已验收。

## 10. 现阶段明确限制

1. 只支持 GEN1 v1、11 槽、Gegenpress。
2. PI/TI 仅限源码白名单；未知值会停止。
3. duty 为硬编码角色映射，含一项源码标记的推断值。
4. 生成器未调用完整 PI 权限矩阵。
5. TI 仅有一个向量，并会继承未在 GEN1 中出现的模板选项位。
6. OOP STC 会写成 ST。
7. 二进制回读不代表游戏内全部字段通过，更不代表比赛效果通过。

后续开发直接基于本目录源码：先接入 PI 权限预检，再增加 TI/PI 映射与样本、完善 duty 来源、扩充原生模板回归测试，最后完成游戏内保存/重开与比赛验证。不得另建重复生成器，也不得重新引入网站/API/游戏平台依赖。
