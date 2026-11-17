> **当前执行规则（2026-11-17）：本文件定义 GEN1 的数据格式及历史样本，不是最终交付说明。GEN1 仅为中间配方。所有新战术必须继续执行第 04 层当前离线生成流程，实际产出原生 .fmf 和同次生成的 .report.json。若本文件中的历史示例、旧工具步骤或 TI 项目数量与第 04 层当前源码字段契约不一致，以当前 Python 源码、字段契约和第 04 层生成流程为准。不得在 GEN1 预检结束后停止并宣称战术已生成。**

# FM27GEN1 v1 生成与导出规范

**版本：** 1.1（增加 A4.3 与 A4.11 完整 GEN1 附录）  
**基准配方：** ENGINE HARVESTER A4.2 - COMPLETE POSITIONAL UPGRADE  
**交叉样本：** A4.2 升级版、A4.12 重建版、A4.13 AWAY CONTROL  
**目的：** 以后只需按本规范，就能把战术设计整理成 GEN1 payload、生成单行 GEN1 代码、检查结构，并交给战术生成器完成后续战术导出。

---

## 0. 最重要的边界：GEN1 代码不等于游戏原生战术文件

`FM27GEN1:` 是本项目使用的**自定义战术配方封装**。从已验证样本可以确认，它的结构是：

1. `FM27GEN1:` 固定前缀；
2. 前缀后面是标准 Base64；
3. Base64 解码后是 UTF-8 JSON；
4. JSON 保存战术基础信息、球队指令，以及 11 个位置槽位各自的有球/无球角色和个人指令。

它不是 Football Manager 原生 `.fm` 文件，也不是可以直接被游戏本体当作战术文件读取的二进制内容。GEN1 负责**表达配方**；要生成可在游戏内使用、保存或分享的战术文件，还需要一个下游转换器/生成器，把配方字段映射为游戏可识别的阵型位置、角色、指令设置，再保存为游戏战术文件。

因此，工作必须分成五个独立验收层级：

| 层级 | 验收内容 | 能证明什么 |
|---|---|---|
| 1. 配方设计 | 阵型、角色、团队/个人指令设计完成 | 战术设计已经确定 |
| 2. GEN1 结构 | JSON schema、字段、槽位、指令对正确 | 代码结构无误 |
| 3. 生成器导入 | 生成器成功读取，且没有未预期的 Skipped changes | 该生成器接受了配方 |
| 4. 游戏战术保存 | 游戏内能看到正确的阵型、角色和指令，并保存/导出 | 已得到可用的原生战术 |
| 5. 比赛验证 | 正式比赛运行并按同口径统计 | 才能评价战术效果 |

**不要把第 2 层的 Base64/JSON 往返通过，说成第 3、4 或第 5 层已经通过。** 当前 A4.2 文件通过了第 2 层；尚无当前生成器导入成功回执，也未完成游戏内比赛验证。

## 1. GEN1 v1 的完整 JSON 结构

当前样本的根对象固定为以下六个字段：

```json
{
  "v": 1,
  "name": "战术名称",
  "ment": 5,
  "base": {
    "g": "Gegenpress",
    "ip": "4-2-3-1 DM AM Wide",
    "oop": "4-3-3 DM Wide"
  },
  "ti": {
    "PASSING_DIRECTNESS": "DEFAULT"
  },
  "p": [
    {
      "in": {
        "pos": "GK",
        "role": "Ball-Playing Goalkeeper",
        "pi": [["PASSING_STRATEGY", "SHORTER"]]
      },
      "out": {
        "pos": "GK",
        "role": "Sweeper Keeper",
        "pi": []
      }
    }
  ]
}
```

上面仅展示一个槽位和一个球队指令，真实的 A4.2 配方有 27 个球队指令和 11 个槽位。

### 1.1 根字段规则

| 字段 | 类型 | 规则 |
|---|---|---|
| `v` | 整数 | 当前格式版本，已见样本为 `1`；不要把它当作游戏版本号。 |
| `name` | 字符串 | 战术名称。建议唯一、清楚地标记版本和用途。 |
| `ment` | 整数 | 心态数字编码。A4.2/A4.12/A4.13 样本均为 `5`；A4.2 说明文本将其标为 Positive。其他数字与心态的对应表尚未由现有材料完整证明。 |
| `base` | 对象 | 战术基础结构，只含 `g`、`ip`、`oop`。 |
| `ti` | 对象 | 球队指令字典，格式为 `指令键: 选项值`。 |
| `p` | 数组 | 位置槽位数组；当前 A4.2 架构按固定 11 槽顺序写入。 |

### 1.2 `base` 字段

- `g`：战术风格/体系标签。已确认样本使用 `Gegenpress`。
- `ip`：有球阵型名称，必须使用生成器能够识别的准确字符串。
- `oop`：无球阵型名称，必须使用生成器能够识别的准确字符串。

本手册的 A4.2 基准是：

- `g = Gegenpress`
- `ip = 4-2-3-1 DM AM Wide`
- `oop = 4-3-3 DM Wide`
- `ment = 5`（对应当前配方所标注的 Positive）

不要仅凭名称相似就改写阵型字符串；阵型名称、槽位位置和角色必须由同一个阵型版本的槽位映射表核对。

### 1.3 `p` 的每个槽位

每个槽位必须有且只有两个阶段对象：`in` 与 `out`。

每个阶段对象必须有且只有三个字段：

- `pos`：该阶段的位置代码；
- `role`：游戏角色的英文显示名称；
- `pi`：个人指令数组。

`in` 代表有球阶段（In Possession，IP）；`out` 代表无球阶段（Out of Possession，OOP）。同一个槽位的 IP 与 OOP 位置可以不同，例如 MCR 有球时在 `MCR`，无球时变为 `DMR`。

**GEN1 的 `role` 使用英文显示名称，不使用内部 CamelCase ID。** 例如 GEN1 写 `Ball-Playing Goalkeeper`；供导出器内部查表使用的 ID 才是 `BallPlayingGoalkeeper`。不要把内部 ID 误写进 `role`。

### 1.4 `pi` 的数据格式

个人指令不是对象，而是二元数组列表：

```json
"pi": [
  ["PASSING_STRATEGY", "SHORTER"],
  ["SHOOTING", "SHOOT_LESS_OFTEN"]
]
```

每一对的第一个字符串是指令键，第二个字符串是该指令的选项值。没有额外个人指令时必须写空数组 `[]`，不要写 `null`，也不要省略 `pi` 字段。

规则：

1. 同一阶段、同一位置中，一个个人指令键最多出现一次。
2. 指令键和选项值必须使用生成器/游戏菜单接受的准确英文 token，大小写也要一致。
3. 个人指令必须在该角色、该阶段的菜单权限内。某指令存在于全局菜单，不代表每个角色都能使用。
4. 不要把球队指令误放进个人指令，也不要把个人指令放进 `ti`。
5. 只写需要明确覆盖角色默认行为的个人指令；不额外覆盖的项目保持空缺。
6. 指令排列顺序不应承担战术语义，但建议按同一套固定顺序输出，方便审计差异。

## 2. A4.2 架构的 11 个固定槽位

对于 A4.2 的 4-2-3-1 DM AM Wide / 4-3-3 DM Wide，`p` 数组必须遵循下表顺序。不要按字母顺序重排，也不要把左右槽位合并。

| 序号 | IP 位置 | IP 角色显示名 | OOP 位置 | OOP 角色显示名 | 导出器角色 ID（供查表） |
|---:|---|---|---|---|---|
| 0 | GK | Ball-Playing Goalkeeper | GK | Sweeper Keeper | `BallPlayingGoalkeeper` / `OPSweeperKeeper` |
| 1 | DR | Wing-Back | DR | Holding Full-Back | `WingBack` / `OPHoldingFullBack` |
| 2 | DCR | Centre-Back | DCR | Covering Centre-Back | `CentreBack` / `OPCoveringCentreBack` |
| 3 | DCL | Centre-Back | DCL | Centre-Back | `CentreBack` / `OPCentreBack` |
| 4 | DL | Full-Back | DL | Holding Full-Back | `FullBack` / `OPHoldingFullBack` |
| 5 | MCR | Midfield Playmaker | DMR | Screening Defensive Midfielder | `MidfieldPlaymaker` / `OPScreeningDefensiveMidfielder` |
| 6 | MCL | Channel Midfielder | DML | Defensive Midfielder | `ChannelMidfielder` / `OPDefensiveMidfielder` |
| 7 | AMR | Playmaking Winger | MR | Tracking Wide Midfielder | `PlaymakingWinger` / `OPTrackingWideMidfielder` |
| 8 | AML | Inside Forward | ML | Tracking Wide Midfielder | `InsideForward` / `OPTrackingWideMidfielder` |
| 9 | AMC | Advanced Playmaker | MCL | Central Midfielder | `AdvancedPlaymaker` / `OPCentralMidfielder` |
| 10 | STC | Channel Forward | STC | Tracking Centre Forward | `ChannelForward` / `OPTrackingCentreForward` |

位置代码的含义必须按阶段理解：`MCR/MCL` 是有球中前卫槽位，而无球分别落在 `DMR/DML`；有球前腰 `AMC` 无球对应 `MCL`；边锋 `AMR/AML` 无球分别对应 `MR/ML`。

这张表是 A4.2 配方的**槽位映射**，不是对所有阵型的通用 11 槽表。换阵型时必须重新核对：位置集合、顺序、角色可用性及导出器内部 ID/mask 映射。

## 3. 27 个球队指令键：A4.2 基准值

`ti` 是一个对象，不是数组。A4.2 升级版保留了完整 27 项球队指令；下表列出当前基准配方的准确键名和值。

| # | GEN1 指令键 | A4.2 值 | 中文含义/当前用途 |
|---:|---|---|---|
| 1 | `PASSING_DIRECTNESS` | `DEFAULT` | 全队传球直接度：标准；不对所有位置统一强制直传。 |
| 2 | `TEMPO` | `HIGHER` | 比赛节奏：更高。 |
| 3 | `ATTACKING_WIDTH` | `WIDER` | 进攻宽度：更宽。 |
| 4 | `ATTACKING_TRANSITION` | `COUNTER_ATTACK` | 进攻转换：反击。 |
| 5 | `CREATIVE_FREEDOM` | `DEFAULT` | 创造自由度：标准。 |
| 6 | `TIME_WASTING` | `DEFAULT` | 拖延时间：标准。 |
| 7 | `PLAY_FOR_SET_PIECES` | `KEEP_BALL_IN_PLAY` | 保持比赛流畅，不主动为定位球放慢/改变比赛。 |
| 8 | `BUILD_UP_STRATEGY` | `PLAY_THROUGH_PRESS` | 组织方式：通过压迫。 |
| 9 | `GOAL_KICKS` | `SHORT` | 球门球：短传。 |
| 10 | `GOALKEEPER_DISTRIBUTION` | `CENTRE_BACKS` | 门将分球对象：中后卫。 |
| 11 | `GK_DISTRIBUTION_(SPEED)` | `DEFAULT` | 门将分球速度：标准。注意键名中的括号是字面字符。 |
| 12 | `PROGRESS_THROUGH` | `DEFAULT` | 推进方向：标准。 |
| 13 | `PASS_RECEPTION` | `PASS_INTO_SPACE` | 接球方式：传入空当。 |
| 14 | `SUPPORTING_RUNS` | `DEFAULT` | 支援跑位：标准。 |
| 15 | `PATIENCE` | `DEFAULT` | 进攻耐心：标准。 |
| 16 | `DRIBBLING` | `DEFAULT` | 团队盘带：标准。 |
| 17 | `SHOTS_FROM_DISTANCE` | `DISCOURAGE` | 远射：减少/不鼓励。 |
| 18 | `CROSSING_STYLE` | `DEFAULT` | 传中方式：标准。 |
| 19 | `LINE_OF_ENGAGEMENT` | `HIGH_PRESS` | 逼抢线：高位压迫。 |
| 20 | `DEFENSIVE_LINE` | `HIGHER` | 防线：较高。 |
| 21 | `DEFENSIVE_LINE_BEHAVIOR` | `DEFAULT` | 防线行为：标准。 |
| 22 | `TRIGGER_PRESS` | `MORE_OFTEN` | 全队逼抢触发：更多。 |
| 23 | `DEFENSIVE_TRANSITION` | `COUNTER_PRESS` | 丢球后：立即反抢。A4.13 客场实验把此项单独改为 `REGROUP`。 |
| 24 | `TACKLING` | `DEFAULT` | 全队铲抢：标准。 |
| 25 | `PRESSING_TRAP` | `DEFAULT` | 压迫陷阱：标准。 |
| 26 | `SHORT_GOALKEEPER_DISTRIBUTION` | `YES` | 门将短传分球：开启。 |
| 27 | `CROSS_ENGAGEMENT` | `DEFAULT` | 防守传中应对：标准。 |

### 3.1 球队指令的生成规则

- 在 A4.2 这套阵型/版本模板中，输出完整的 27 个指令键；不要因当前值是 `DEFAULT` 就删掉键。
- 值必须是一个字符串 token，例如 `HIGHER`，不是中文标签，也不是 `true/false`。
- `GK_DISTRIBUTION_(SPEED)` 的括号、下划线和大小写必须原样保留。
- 任何全队指令改动，都应记录 `旧值 → 新值`，并在版本差异表中只列真实变化。
- 目前样本只充分展示了上表的大多数当前值；`DEFENSIVE_TRANSITION` 另有 `REGROUP` 样本。不能据此宣称列出的值就是游戏所有可能选项。

## 4. 个人指令键与已见选项

以下列出 A4.2/A4.12/A4.13 这些配方中实际出现过的个人指令键和取值。**这是样本中已确认的 token，不是官方全部 PI 选项的穷尽目录。** 如果下一版需要新选项，必须先从相应位置、角色、IP/OOP 阶段的实际菜单或导出器权限目录核对，再加入配方。

| 个人指令键 | 已见取值 | 中文含义 |
|---|---|---|
| `PASSING_STRATEGY` | `SHORTER`, `MORE_DIRECT` | 传球策略：更短 / 更直接。 |
| `PASSING_RISKS` | `TAKE_FEWER_RISKS`, `TAKE_MORE_RISKS` | 传球风险：减少 / 增加冒险。 |
| `DRIBBLING_DIRECTION` | `RUN_WIDE_WITH_BALL`, `CUT_INSIDE_WITH_BALL` | 带球方向：沿边路 / 内切。 |
| `DRIBBLING_FREQUENCY` | `DRIBBLE_LESS`, `DRIBBLE_MORE` | 盘带频率：减少 / 增加。 |
| `SHOOTING` | `SHOOT_LESS_OFTEN`, `SHOOT_MORE_OFTEN` | 射门倾向：减少 / 增加。 |
| `ATTACKING_WIDTH` | `STAY_WIDER`, `SIT_NARROWER`, `MOVE_INTO_CHANNELS` | 进攻位置/宽度：拉开、内收、游弋肋部。 |
| `ATTACK_BOX_SIDE` | `NEAR_POST`, `CENTRE`, `FAR_POST` | 禁区攻击落点：前点、中路、后点。 |
| `FORWARD_RUNS` | `MAKE_MORE_RUNS` | 前插：更多前插。 |
| `CROSS_FROM` | `BYLINE` | 传中位置：下底线附近。 |
| `CROSSING_STRATEGY` | `FAR_POST` | 传中目标：后点。 |
| `MARKING` | `MARK_TIGHTER` | 盯人：更紧密。 |
| `TACKLING` | `EASE_OFF_TACKLES` | 铲抢：谨慎/减少激进铲抢。 |
| `TRIGGER_PRESS` | `MORE_OFTEN` | 个体逼抢触发：更多。 |

球队指令和个人指令可以出现同名键，但属于不同作用层级。例如 `ATTACKING_WIDTH` 在 `ti` 中代表全队宽度，在 `pi` 中代表某个角色/位置的个人宽度指令；不可因此合并或互相覆盖。

## 5. A4.2 升级版完整个人任务表

以下清单就是当前 `FM27_A4.2_GEN1_ONLY.txt` 的 58 条个人指令定义。计数同时包含 IP 和 OOP 两个阶段。

**0 — GK**  
IP `Ball-Playing Goalkeeper`：`PASSING_STRATEGY=SHORTER`。  
OOP `Sweeper Keeper`：无额外个人指令（`[]`）。

**1 — DR**  
IP `Wing-Back`：`DRIBBLING_DIRECTION=RUN_WIDE_WITH_BALL`；`DRIBBLING_FREQUENCY=DRIBBLE_LESS`；`PASSING_STRATEGY=MORE_DIRECT`；`SHOOTING=SHOOT_LESS_OFTEN`；`CROSS_FROM=BYLINE`；`CROSSING_STRATEGY=FAR_POST`。  
OOP `Holding Full-Back`：`MARKING=MARK_TIGHTER`。

**2 — DCR**  
IP `Centre-Back`：`PASSING_STRATEGY=SHORTER`；`PASSING_RISKS=TAKE_FEWER_RISKS`；`DRIBBLING_FREQUENCY=DRIBBLE_LESS`。  
OOP `Covering Centre-Back`：`MARKING=MARK_TIGHTER`；`TACKLING=EASE_OFF_TACKLES`。

**3 — DCL**  
IP `Centre-Back`：`PASSING_STRATEGY=MORE_DIRECT`；`PASSING_RISKS=TAKE_MORE_RISKS`。  
OOP `Centre-Back`：`MARKING=MARK_TIGHTER`；`TACKLING=EASE_OFF_TACKLES`。

**4 — DL**  
IP `Full-Back`：`ATTACKING_WIDTH=STAY_WIDER`；`DRIBBLING_DIRECTION=RUN_WIDE_WITH_BALL`；`DRIBBLING_FREQUENCY=DRIBBLE_MORE`；`FORWARD_RUNS=MAKE_MORE_RUNS`；`SHOOTING=SHOOT_LESS_OFTEN`；`PASSING_RISKS=TAKE_MORE_RISKS`；`PASSING_STRATEGY=SHORTER`。  
OOP `Holding Full-Back`：`MARKING=MARK_TIGHTER`。

**5 — MCR**  
IP `Midfield Playmaker`：`SHOOTING=SHOOT_LESS_OFTEN`；`PASSING_STRATEGY=SHORTER`。  
OOP `Screening Defensive Midfielder`：无额外个人指令（`[]`）。

**6 — MCL**  
IP `Channel Midfielder`：`FORWARD_RUNS=MAKE_MORE_RUNS`；`SHOOTING=SHOOT_LESS_OFTEN`；`PASSING_STRATEGY=SHORTER`。  
OOP `Defensive Midfielder`：无额外个人指令（`[]`）。

**7 — AMR**  
IP `Playmaking Winger`：`DRIBBLING_DIRECTION=CUT_INSIDE_WITH_BALL`；`DRIBBLING_FREQUENCY=DRIBBLE_LESS`；`PASSING_STRATEGY=MORE_DIRECT`；`PASSING_RISKS=TAKE_MORE_RISKS`。  
OOP `Tracking Wide Midfielder`：`TRIGGER_PRESS=MORE_OFTEN`；`TACKLING=EASE_OFF_TACKLES`。

**8 — AML**  
IP `Inside Forward`：`DRIBBLING_DIRECTION=CUT_INSIDE_WITH_BALL`；`ATTACK_BOX_SIDE=CENTRE`；`ATTACKING_WIDTH=SIT_NARROWER`；`DRIBBLING_FREQUENCY=DRIBBLE_MORE`；`PASSING_RISKS=TAKE_MORE_RISKS`；`PASSING_STRATEGY=MORE_DIRECT`；`SHOOTING=SHOOT_MORE_OFTEN`。  
OOP `Tracking Wide Midfielder`：`TRIGGER_PRESS=MORE_OFTEN`；`TACKLING=EASE_OFF_TACKLES`。

**9 — AMC**  
IP `Advanced Playmaker`：`ATTACK_BOX_SIDE=FAR_POST`；`ATTACKING_WIDTH=MOVE_INTO_CHANNELS`；`DRIBBLING_FREQUENCY=DRIBBLE_LESS`；`PASSING_STRATEGY=MORE_DIRECT`；`SHOOTING=SHOOT_MORE_OFTEN`。  
OOP `Central Midfielder`：`TRIGGER_PRESS=MORE_OFTEN`；`TACKLING=EASE_OFF_TACKLES`。

**10 — STC**  
IP `Channel Forward`：`ATTACK_BOX_SIDE=NEAR_POST`；`FORWARD_RUNS=MAKE_MORE_RUNS`；`SHOOTING=SHOOT_MORE_OFTEN`；`PASSING_STRATEGY=MORE_DIRECT`。  
OOP `Tracking Centre Forward`：`TRIGGER_PRESS=MORE_OFTEN`；`TACKLING=EASE_OFF_TACKLES`。

### 5.1 这份任务表背后的分工

- **右侧供给：** DR 负责下底、后点传中；AMR 内收并承担高风险、更直接的创造传球。
- **左侧推进：** DL 负责拉开宽度、带球推进和前插；AML 内收攻击中路，不继续承担指定下底传中任务。
- **中场分工：** MCR 是短传组织点；MCL 是通道跑动和连接点，限制额外射门。
- **前场三通道：** STC 攻击前点；AML 攻击中路；AMC 后点进入并承担第二终结职责。
- **无球结构：** 两边中场回到 MR/ML；双中场落入 DMR/DML；前腰回到 MCL；全队压迫仍由球队指令维持。

以上是战术设计意图，不表示每场比赛都必然按预期触发，也不等于已用阶段事件数据证明了每个 OOP 个人指令的效果。

## 6. 从战术设计到生成 GEN1 的标准流程

### 第一步：锁定基准结构

先确定战术名称、战术风格、心态、有球阵型、无球阵型。确认对应的槽位列表，尤其确认 IP 与 OOP 是否发生位置转换。不要先写 PI 再临时改阵型。

### 第二步：建立槽位表

每个球员位置槽位只登记一次，并为它配对一个 IP 位置/角色和一个 OOP 位置/角色。角色名称必须从当前游戏版本的角色菜单或已验证配方复制，不要自行翻译成中文后写入 GEN1。

### 第三步：填写球队指令

把球队指令逐项填入 `ti`。A4.2 模板使用本手册第 3 节的 27 个键。若改用其他战术体系，先确认该体系生成器需要的球队指令集合；不要直接假定其他战术也与 A4.2 完全相同。

### 第四步：逐槽填个人指令

从第 0 槽到第 10 槽逐一处理：先 IP，再 OOP。每条 PI 都必须确认三个条件：

1. 指令键正确；
2. 选项值正确；
3. 该角色在该阶段确实允许此选项。

无额外指令写 `[]`。不要把整个位置的指令复制到另一侧，除非数据和战术分工确实支持左右对称。

### 第五步：结构校验

至少检查：

- 根字段为 `v/name/ment/base/ti/p`；
- `v=1`；
- `base` 含 `g/ip/oop`；
- 每槽均含 `in/out`；
- 每阶段均含 `pos/role/pi`；
- `pi` 中每项都是 `[键, 值]` 两个字符串；
- 同一阶段没有重复 PI 键；
- IP 位置没有重复，OOP 位置没有重复；
- A4.2 模板的槽位顺序准确，球队指令键齐全。

### 第六步：编码成单行

标准算法：

```python
import base64, json

payload = { ... }  # 已通过结构检查的 GEN1 JSON 对象
raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
code = "FM27GEN1:" + base64.b64encode(raw).decode("ascii")
print(code)  # 一行输出，不要换行拆段或手工编辑 Base64
```

要点：UTF-8、标准 Base64、固定 `FM27GEN1:` 前缀、整段单行、不插入空格、不使用 URL-safe Base64、不额外 gzip。不要手工修改 Base64 字符；有任何指令变化都应该回到 JSON payload 修改，再重新编码。

### 第七步：往返验证

必须执行：

1. 去掉 `FM27GEN1:` 前缀；
2. Base64 解码为字节；
3. UTF-8 解码并解析 JSON；
4. 检查字段/指令/槽位；
5. 对解码得到的原始字节重新 Base64 编码；
6. 与原代码行逐字符比较。

若逐字符相同，代表 Base64/JSON 封装没有被损坏；这仍然不代表生成器或游戏已经接受每一项。

### 第八步：交给生成器并导出游戏战术

在生成器中导入完整的 `FM27GEN1:` 行之后，必须逐项核对生成器的结果：

1. 是否成功识别战术名、风格、心态、IP/OOP 阵型；
2. 11 个槽位是否按预期排列；
3. 每个槽位的 IP 和 OOP 角色是否正确；
4. 27 个球队指令是否全部保留；
5. 每个 PI 是否都显示在正确的位置和正确阶段；
6. `Skipped changes` 是否为空；若不为空，逐条判断是权限不支持、token 不匹配、角色映射错误，还是生成器版本不兼容；
7. 在游戏内保存/导出战术后，重新打开该战术复查，不要只凭生成器提示判断成功。

**下游转换器的职责：** GEN1 的角色显示名需要映射到游戏内部角色 ID；位置代码需要映射到对应阵型位置/位置 mask；指令键和值需要映射到游戏实际的 setting ID/菜单选项。仅做 Base64 解码并不会自动完成这些映射。

当前资料没有包含一个可审计的、从 GEN1 到原生 `.fm` 文件的完整转换器源代码或二进制映射规范。因此本手册能完整定义已观察到的 GEN1 输入格式、A4.2 配方结构和编码校验；具体如何调用某一版生成器、其 `.fm` 写入/保存接口，则必须以该生成器实际版本为准，不能在没有源码/接口证据时虚构步骤。

## 7. 导出后必须核对的项目

| 检查范围 | A4.2 重点 |
|---|---|
| 战术结构 | Gegenpress；Positive；IP `4-2-3-1 DM AM Wide`；OOP `4-3-3 DM Wide` |
| 全队传球 | `PASSING_DIRECTNESS=DEFAULT`，不是旧版 `MORE_DIRECT` |
| DR | Wing-Back；下底传中；后点；减少盘带；更直接传球 |
| DL | Full-Back；拉宽；带球推进；更多前插；不能误带回 DR 的下底传中任务 |
| DCR/DCL | 右侧更稳、左侧更直接；两侧 OOP 盯人和谨慎铲抢 |
| MCR/MCL | MCR 短传组织；MCL 通道跑动、减少射门；MCL OOP 不额外强制个人逼抢 |
| AMR/AML | AMR 创造为主；AML 内切、中路落点并更多射门 |
| AMC/STC | AMC 后点；STC 前点、更多前插和射门 |
| OOP 边路 | AMR/AML 对应 MR/ML 追踪边路中场 |
| OOP 中路 | MCR/MCL 对应 DMR/DML；AMC 对应 MCL |

若发现 PI 没有应用，先检查该角色阶段的菜单权限，再检查 token 与内部映射；不要先假定 Base64 有问题。

## 8. 复杂度与实测要求

A4.2 升级版当前共有 27 条球队指令和 58 条个人指令。指令数量并不等于质量。FM27 的 Tactical Complexity 与球队/球员/对手指令的数量有关，必须同时观察 Tactical Understanding、Player Ability、Player Buy-In 和战术熟悉度。新战术训练不足时，短期表现不佳不能直接证明结构错误。

建议正式测试时保持战术版本一致，至少按主客场拆分记录：积分/场、进球、失球、xG/xGA、禁区内射门、绝佳机会、被反击、关键位置 G+A、DR 传中成功率、DL 推进传球。不要在同一测试组中混入不同战术版本，也不要把一个存档反复回档产生的同场比赛视作独立样本。

## 9. A4.2 配方的验证状态与已知限制

| 项目 | 当前状态 |
|---|---|
| Base64 解码 | 通过 |
| UTF-8 JSON 解析 | 通过 |
| Base64 原文重编码一致 | 通过 |
| 27 个球队指令计数 | 通过 |
| 11 个槽位顺序 | 通过 |
| 58 条个人指令计数 | 通过 |
| 生成器实际导入 | 尚未验证 |
| `Skipped changes` 为零 | 尚未验证 |
| 游戏内保存/导出原生战术 | 尚未验证 |
| 比赛实测 | 尚未验证 |

数据解释限制：

- DCR/DCL 的历史比赛位置数据不能稳定拆分左右侧，不能把合并 DC 数据当作左右中卫独立表现。
- MCR/MCL 的角色确认样本较小，二者的任务分配置信度低于样本更充足的位置。
- 球员整场报告不是 IP/OOP 分阶段事件数据，不能用整场总统计宣称某条 OOP 指令已经被独立证明。
- 角色菜单权限通过，不等于某次生成器导入成功；GEN1 结构通过，也不等于原生战术保存成功。

## 10. 使用附带的命令行工具

随文档提供 `fm27gen1_tool.py`，无需安装第三方 Python 套件。

假设命令提示符当前目录含有该脚本和 JSON/GEN1 文件：

**从 JSON 生成单行 GEN1：**

```powershell
python .\fm27gen1_tool.py encode .\FM27_A4.2_GEN1_decoded_payload.json --a42-template -o .\FM27_A4.2_NEW_GEN1.txt
```

**验证 GEN1：**

```powershell
python .\fm27gen1_tool.py validate .\FM27_A4.2_NEW_GEN1.txt --a42-template
```

**把 GEN1 解码回 JSON：**

```powershell
python .\fm27gen1_tool.py decode .\FM27_A4.2_NEW_GEN1.txt --a42-template -o .\FM27_A4.2_check.json
```

`--a42-template` 会额外检查 A4.2 专用的 11 槽顺序和 27 个球队指令键；其他阵型/模板不要盲目使用此选项。工具只做 GEN1 封装与结构校验，不会启动 FM27，不会代替下游战术生成器，也不会写入原生 `.fm` 文件。

# 附录 A：A4.3 / A4.11 完整 GEN1 实例

本附录把两份可直接导入生成器的完整 GEN1 原文保留在规范内。为了避免长字符串被 Word/PDF 复制过程插入空格或换行，工具包同时附带同名 `*_GEN1_ONLY.txt` 文件；**实际复制导入时优先使用 TXT 文件中的唯一一行**。附录中的代码正文也以单行字符串保存，视觉换行不代表代码中存在换行字符。

## A.1 A4.3 — ENGINE HARVESTER A4.3 - BOX LANE ENGINE

- 来源：A4.3 原始配方文件中的完整 `FM27GEN1:` 行，直接提取，没有重写指令。
- 结构：Gegenpress；Positive；IP `4-2-3-1 DM AM Wide`；OOP `4-3-3 DM Wide`。
- 指令计数：27 项球队指令、11 个 IP/OOP 槽位、5 条个人指令。
- 独有战术特点：STC 前点、AML 中路、AMC 后点三通道。其他 A4.2 骨架与球队指令沿用。
- 校验：Base64 解码、UTF-8 JSON 解析、再编码逐字符往返一致。结构校验通过；生成器导入/游戏内导出仍需单独验收。

```text
FM27GEN1:eyJ2IjoxLCJuYW1lIjoiRU5HSU5FIEhBUlZFU1RFUiBBNC4zIC0gQk9YIExBTkUgRU5HSU5FIiwibWVudCI6NSwiYmFzZSI6eyJnIjoiR2VnZW5wcmVzcyIsImlwIjoiNC0yLTMtMSBETSBBTSBXaWRlIiwib29wIjoiNC0zLTMgRE0gV2lkZSJ9LCJ0aSI6eyJQQVNTSU5HX0RJUkVDVE5FU1MiOiJNT1JFX0RJUkVDVCIsIlRFTVBPIjoiSElHSEVSIiwiQVRUQUNLSU5HX1dJRFRIIjoiV0lERVIiLCJBVFRBQ0tJTkdfVFJBTlNJVElPTiI6IkNPVU5URVJfQVRUQUNLIiwiQ1JFQVRJVkVfRlJFRURPTSI6IkRFRkFVTFQiLCJUSU1FX1dBU1RJTkciOiJERUZBVUxUIiwiUExBWV9GT1JfU0VUX1BJRUNFUyI6IktFRVBfQkFMTF9JTl9QTEFZIiwiQlVJTERfVVBfU1RSQVRFR1kiOiJQTEFZX1RIUk9VR0hfUFJFU1MiLCJHT0FMX0tJQ0tTIjoiU0hPUlQiLCJHT0FMS0VFUEVSX0RJU1RSSUJVVElPTiI6IkNFTlRSRV9CQUNLUyIsIkdLX0RJU1RSSUJVVElPTl8oU1BFRUQpIjoiREVGQVVMVCIsIlBST0dSRVNTX1RIUk9VR0giOiJERUZBVUxUIiwiUEFTU19SRUNFUFRJT04iOiJQQVNTX0lOVE9fU1BBQ0UiLCJTVVBQT1JUSU5HX1JVTlMiOiJERUZBVUxUIiwiUEFUSUVOQ0UiOiJERUZBVUxUIiwiRFJJQkJMSU5HIjoiREVGQVVMVCIsIlNIT1RTX0ZST01fRElTVEFOQ0UiOiJESVNDT1VSQUdFIiwiQ1JPU1NJTkdfU1RZTEUiOiJERUZBVUxUIiwiTElORV9PRl9FTkdBR0VNRU5UIjoiSElHSF9QUkVTUyIsIkRFRkVOU0lWRV9MSU5FIjoiSElHSEVSIiwiREVGRU5TSVZFX0xJTkVfQkVIQVZJT1IiOiJERUZBVUxUIiwiVFJJR0dFUl9QUkVTUyI6Ik1PUkVfT0ZURU4iLCJERUZFTlNJVkVfVFJBTlNJVElPTiI6IkNPVU5URVJfUFJFU1MiLCJUQUNLTElORyI6IkRFRkFVTFQiLCJQUkVTU0lOR19UUkFQIjoiREVGQVVMVCIsIlNIT1JUX0dPQUxLRUVQRVJfRElTVFJJQlVUSU9OIjoiWUVTIiwiQ1JPU1NfRU5HQUdFTUVOVCI6IkRFRkFVTFQifSwicCI6W3siaW4iOnsicG9zIjoiR0siLCJyb2xlIjoiQmFsbC1QbGF5aW5nIEdvYWxrZWVwZXIiLCJwaSI6W1siUEFTU0lOR19TVFJBVEVHWSIsIlNIT1JURVIiXV19LCJvdXQiOnsicG9zIjoiR0siLCJyb2xlIjoiU3dlZXBlciBLZWVwZXIiLCJwaSI6W119fSx7ImluIjp7InBvcyI6IkRSIiwicm9sZSI6IldpbmctQmFjayIsInBpIjpbXX0sIm91dCI6eyJwb3MiOiJEUiIsInJvbGUiOiJIb2xkaW5nIEZ1bGwtQmFjayIsInBpIjpbXX19LHsiaW4iOnsicG9zIjoiRENSIiwicm9sZSI6IkNlbnRyZS1CYWNrIiwicGkiOltdfSwib3V0Ijp7InBvcyI6IkRDUiIsInJvbGUiOiJDb3ZlcmluZyBDZW50cmUtQmFjayIsInBpIjpbXX19LHsiaW4iOnsicG9zIjoiRENMIiwicm9sZSI6IkNlbnRyZS1CYWNrIiwicGkiOltdfSwib3V0Ijp7InBvcyI6IkRDTCIsInJvbGUiOiJDZW50cmUtQmFjayIsInBpIjpbXX19LHsiaW4iOnsicG9zIjoiREwiLCJyb2xlIjoiRnVsbC1CYWNrIiwicGkiOltdfSwib3V0Ijp7InBvcyI6IkRMIiwicm9sZSI6IkhvbGRpbmcgRnVsbC1CYWNrIiwicGkiOltdfX0seyJpbiI6eyJwb3MiOiJNQ1IiLCJyb2xlIjoiTWlkZmllbGQgUGxheW1ha2VyIiwicGkiOltdfSwib3V0Ijp7InBvcyI6IkRNUiIsInJvbGUiOiJTY3JlZW5pbmcgRGVmZW5zaXZlIE1pZGZpZWxkZXIiLCJwaSI6W119fSx7ImluIjp7InBvcyI6Ik1DTCIsInJvbGUiOiJDaGFubmVsIE1pZGZpZWxkZXIiLCJwaSI6W119LCJvdXQiOnsicG9zIjoiRE1MIiwicm9sZSI6IkRlZmVuc2l2ZSBNaWRmaWVsZGVyIiwicGkiOltdfX0seyJpbiI6eyJwb3MiOiJBTVIiLCJyb2xlIjoiUGxheW1ha2luZyBXaW5nZXIiLCJwaSI6W119LCJvdXQiOnsicG9zIjoiTVIiLCJyb2xlIjoiVHJhY2tpbmcgV2lkZSBNaWRmaWVsZGVyIiwicGkiOltdfX0seyJpbiI6eyJwb3MiOiJBTUwiLCJyb2xlIjoiSW5zaWRlIEZvcndhcmQiLCJwaSI6W1siRFJJQkJMSU5HX0RJUkVDVElPTiIsIkNVVF9JTlNJREVfV0lUSF9CQUxMIl0sWyJBVFRBQ0tfQk9YX1NJREUiLCJDRU5UUkUiXV19LCJvdXQiOnsicG9zIjoiTUwiLCJyb2xlIjoiVHJhY2tpbmcgV2lkZSBNaWRmaWVsZGVyIiwicGkiOltdfX0seyJpbiI6eyJwb3MiOiJBTUMiLCJyb2xlIjoiQWR2YW5jZWQgUGxheW1ha2VyIiwicGkiOltbIkFUVEFDS19CT1hfU0lERSIsIkZBUl9QT1NUIl1dfSwib3V0Ijp7InBvcyI6Ik1DTCIsInJvbGUiOiJDZW50cmFsIE1pZGZpZWxkZXIiLCJwaSI6W119fSx7ImluIjp7InBvcyI6IlNUQyIsInJvbGUiOiJDaGFubmVsIEZvcndhcmQiLCJwaSI6W1siQVRUQUNLX0JPWF9TSURFIiwiTkVBUl9QT1NUIl1dfSwib3V0Ijp7InBvcyI6IlNUQyIsInJvbGUiOiJUcmFja2luZyBDZW50cmUgRm9yd2FyZCIsInBpIjpbXX19XX0=
```

## A.2 A4.11 — ENGINE HARVESTER A4.11 - COMPLETE TASK SPECIALISATION

- 版本辨识：本附录收录 A4.11 COMPLETE TASK SPECIALISATION。它不同于早期的 A4.11 UNIVERSAL PI REBALANCE，两者不是同一份配方，不能混用。
- 结构：Gegenpress；Positive；IP `4-2-3-1 DM AM Wide`；OOP `4-3-3 DM Wide`。
- 指令计数：27 项球队指令、11 个 IP/OOP 槽位、58 条个人指令。
- 角色：11 个位置的有球/无球角色全部沿用 A4.9；没有角色或位置槽位改动。
- A4.11 相对 A4.9 的核对结果：球队传球直接度改为 `DEFAULT`；DR 增加下底/后点传中；DL 移除下底/后点传中；MCL 有球射门改为减少、无球移除额外逼抢；AMR 移除更多射门、改更直接传球并增加更多冒险传球；AML 移除下底/前点传中并增加更多射门；AMC 增加更多射门。其余角色、位置和未列出的设置保持不变。
- 还原依据：A4.12 `ST LINK-UP BALANCE` 配方及其验证报告明确记载，A4.12 相比 A4.11 的唯一战术差异，是移除 STC/IP/Channel Forward 的 `PASSING_STRATEGY=MORE_DIRECT`。因此本文件从该 A4.12 配方恢复这一条 ST 个人指令，并将战术名恢复为 `A4.11 - COMPLETE TASK SPECIALISATION`。随后与 A4.9 原始 GEN1 做结构差异比较，确认所有差异与 A4.11 任务再分配报告逐项一致。
- A4.11 的 ST 保留 `PASSING_STRATEGY=MORE_DIRECT`；A4.12 才移除它。这是区分两版最直接的检查点。
- 校验：Base64 解码、UTF-8 JSON 解析、再编码逐字符往返一致；A4.11/A4.12 除战术名及 ST 上述一条 PI 外无其他差异。结构校验通过；生成器导入/游戏内导出仍需单独验收。

```text
FM27GEN1:eyJ2IjoxLCJuYW1lIjoiRU5HSU5FIEhBUlZFU1RFUiBBNC4xMSAtIENPTVBMRVRFIFRBU0sgU1BFQ0lBTElTQVRJT04iLCJtZW50Ijo1LCJiYXNlIjp7ImciOiJHZWdlbnByZXNzIiwiaXAiOiI0LTItMy0xIERNIEFNIFdpZGUiLCJvb3AiOiI0LTMtMyBETSBXaWRlIn0sInRpIjp7IlBBU1NJTkdfRElSRUNUTkVTUyI6IkRFRkFVTFQiLCJURU1QTyI6IkhJR0hFUiIsIkFUVEFDS0lOR19XSURUSCI6IldJREVSIiwiQVRUQUNLSU5HX1RSQU5TSVRJT04iOiJDT1VOVEVSX0FUVEFDSyIsIkNSRUFUSVZFX0ZSRUVET00iOiJERUZBVUxUIiwiVElNRV9XQVNUSU5HIjoiREVGQVVMVCIsIlBMQVlfRk9SX1NFVF9QSUVDRVMiOiJLRUVQX0JBTExfSU5fUExBWSIsIkJVSUxEX1VQX1NUUkFURUdZIjoiUExBWV9USFJPVUdIX1BSRVNTIiwiR09BTF9LSUNLUyI6IlNIT1JUIiwiR09BTEtFRVBFUl9ESVNUUklCVVRJT04iOiJDRU5UUkVfQkFDS1MiLCJHS19ESVNUUklCVVRJT05fKFNQRUVEKSI6IkRFRkFVTFQiLCJQUk9HUkVTU19USFJPVUdIIjoiREVGQVVMVCIsIlBBU1NfUkVDRVBUSU9OIjoiUEFTU19JTlRPX1NQQUNFIiwiU1VQUE9SVElOR19SVU5TIjoiREVGQVVMVCIsIlBBVElFTkNFIjoiREVGQVVMVCIsIkRSSUJCTElORyI6IkRFRkFVTFQiLCJTSE9UU19GUk9NX0RJU1RBTkNFIjoiRElTQ09VUkFHRSIsIkNST1NTSU5HX1NUWUxFIjoiREVGQVVMVCIsIkxJTkVfT0ZfRU5HQUdFTUVOVCI6IkhJR0hfUFJFU1MiLCJERUZFTlNJVkVfTElORSI6IkhJR0hFUiIsIkRFRkVOU0lWRV9MSU5FX0JFSEFWSU9SIjoiREVGQVVMVCIsIlRSSUdHRVJfUFJFU1MiOiJNT1JFX09GVEVOIiwiREVGRU5TSVZFX1RSQU5TSVRJT04iOiJDT1VOVEVSX1BSRVNTIiwiVEFDS0xJTkciOiJERUZBVUxUIiwiUFJFU1NJTkdfVFJBUCI6IkRFRkFVTFQiLCJTSE9SVF9HT0FMS0VFUEVSX0RJU1RSSUJVVElPTiI6IllFUyIsIkNST1NTX0VOR0FHRU1FTlQiOiJERUZBVUxUIn0sInAiOlt7ImluIjp7InBvcyI6IkdLIiwicm9sZSI6IkJhbGwtUGxheWluZyBHb2Fsa2VlcGVyIiwicGkiOltbIlBBU1NJTkdfU1RSQVRFR1kiLCJTSE9SVEVSIl1dfSwib3V0Ijp7InBvcyI6IkdLIiwicm9sZSI6IlN3ZWVwZXIgS2VlcGVyIiwicGkiOltdfX0seyJpbiI6eyJwb3MiOiJEUiIsInJvbGUiOiJXaW5nLUJhY2siLCJwaSI6W1siRFJJQkJMSU5HX0RJUkVDVElPTiIsIlJVTl9XSURFX1dJVEhfQkFMTCJdLFsiRFJJQkJMSU5HX0ZSRVFVRU5DWSIsIkRSSUJCTEVfTEVTUyJdLFsiUEFTU0lOR19TVFJBVEVHWSIsIk1PUkVfRElSRUNUIl0sWyJTSE9PVElORyIsIlNIT09UX0xFU1NfT0ZURU4iXSxbIkNST1NTX0ZST00iLCJCWUxJTkUiXSxbIkNST1NTSU5HX1NUUkFURUdZIiwiRkFSX1BPU1QiXV19LCJvdXQiOnsicG9zIjoiRFIiLCJyb2xlIjoiSG9sZGluZyBGdWxsLUJhY2siLCJwaSI6W1siTUFSS0lORyIsIk1BUktfVElHSFRFUiJdXX19LHsiaW4iOnsicG9zIjoiRENSIiwicm9sZSI6IkNlbnRyZS1CYWNrIiwicGkiOltbIlBBU1NJTkdfU1RSQVRFR1kiLCJTSE9SVEVSIl0sWyJQQVNTSU5HX1JJU0tTIiwiVEFLRV9GRVdFUl9SSVNLUyJdLFsiRFJJQkJMSU5HX0ZSRVFVRU5DWSIsIkRSSUJCTEVfTEVTUyJdXX0sIm91dCI6eyJwb3MiOiJEQ1IiLCJyb2xlIjoiQ292ZXJpbmcgQ2VudHJlLUJhY2siLCJwaSI6W1siTUFSS0lORyIsIk1BUktfVElHSFRFUiJdLFsiVEFDS0xJTkciLCJFQVNFX09GRl9UQUNLTEVTIl1dfX0seyJpbiI6eyJwb3MiOiJEQ0wiLCJyb2xlIjoiQ2VudHJlLUJhY2siLCJwaSI6W1siUEFTU0lOR19TVFJBVEVHWSIsIk1PUkVfRElSRUNUIl0sWyJQQVNTSU5HX1JJU0tTIiwiVEFLRV9NT1JFX1JJU0tTIl1dfSwib3V0Ijp7InBvcyI6IkRDTCIsInJvbGUiOiJDZW50cmUtQmFjayIsInBpIjpbWyJNQVJLSU5HIiwiTUFSS19USUdIVEVSIl0sWyJUQUNLTElORyIsIkVBU0VfT0ZGX1RBQ0tMRVMiXV19fSx7ImluIjp7InBvcyI6IkRMIiwicm9sZSI6IkZ1bGwtQmFjayIsInBpIjpbWyJBVFRBQ0tJTkdfV0lEVEgiLCJTVEFZX1dJREVSIl0sWyJEUklCQkxJTkdfRElSRUNUSU9OIiwiUlVOX1dJREVfV0lUSF9CQUxMIl0sWyJEUklCQkxJTkdfRlJFUVVFTkNZIiwiRFJJQkJMRV9NT1JFIl0sWyJGT1JXQVJEX1JVTlMiLCJNQUtFX01PUkVfUlVOUyJdLFsiU0hPT1RJTkciLCJTSE9PVF9MRVNTX09GVEVOIl0sWyJQQVNTSU5HX1JJU0tTIiwiVEFLRV9NT1JFX1JJU0tTIl0sWyJQQVNTSU5HX1NUUkFURUdZIiwiU0hPUlRFUiJdXX0sIm91dCI6eyJwb3MiOiJETCIsInJvbGUiOiJIb2xkaW5nIEZ1bGwtQmFjayIsInBpIjpbWyJNQVJLSU5HIiwiTUFSS19USUdIVEVSIl1dfX0seyJpbiI6eyJwb3MiOiJNQ1IiLCJyb2xlIjoiTWlkZmllbGQgUGxheW1ha2VyIiwicGkiOltbIlNIT09USU5HIiwiU0hPT1RfTEVTU19PRlRFTiJdLFsiUEFTU0lOR19TVFJBVEVHWSIsIlNIT1JURVIiXV19LCJvdXQiOnsicG9zIjoiRE1SIiwicm9sZSI6IlNjcmVlbmluZyBEZWZlbnNpdmUgTWlkZmllbGRlciIsInBpIjpbXX19LHsiaW4iOnsicG9zIjoiTUNMIiwicm9sZSI6IkNoYW5uZWwgTWlkZmllbGRlciIsInBpIjpbWyJGT1JXQVJEX1JVTlMiLCJNQUtFX01PUkVfUlVOUyJdLFsiU0hPT1RJTkciLCJTSE9PVF9MRVNTX09GVEVOIl0sWyJQQVNTSU5HX1NUUkFURUdZIiwiU0hPUlRFUiJdXX0sIm91dCI6eyJwb3MiOiJETUwiLCJyb2xlIjoiRGVmZW5zaXZlIE1pZGZpZWxkZXIiLCJwaSI6W119fSx7ImluIjp7InBvcyI6IkFNUiIsInJvbGUiOiJQbGF5bWFraW5nIFdpbmdlciIsInBpIjpbWyJEUklCQkxJTkdfRElSRUNUSU9OIiwiQ1VUX0lOU0lERV9XSVRIX0JBTEwiXSxbIkRSSUJCTElOR19GUkVRVUVOQ1kiLCJEUklCQkxFX0xFU1MiXSxbIlBBU1NJTkdfU1RSQVRFR1kiLCJNT1JFX0RJUkVDVCJdLFsiUEFTU0lOR19SSVNLUyIsIlRBS0VfTU9SRV9SSVNLUyJdXX0sIm91dCI6eyJwb3MiOiJNUiIsInJvbGUiOiJUcmFja2luZyBXaWRlIE1pZGZpZWxkZXIiLCJwaSI6W1siVFJJR0dFUl9QUkVTUyIsIk1PUkVfT0ZURU4iXSxbIlRBQ0tMSU5HIiwiRUFTRV9PRkZfVEFDS0xFUyJdXX19LHsiaW4iOnsicG9zIjoiQU1MIiwicm9sZSI6Ikluc2lkZSBGb3J3YXJkIiwicGkiOltbIkRSSUJCTElOR19ESVJFQ1RJT04iLCJDVVRfSU5TSURFX1dJVEhfQkFMTCJdLFsiQVRUQUNLX0JPWF9TSURFIiwiQ0VOVFJFIl0sWyJBVFRBQ0tJTkdfV0lEVEgiLCJTSVRfTkFSUk9XRVIiXSxbIkRSSUJCTElOR19GUkVRVUVOQ1kiLCJEUklCQkxFX01PUkUiXSxbIlBBU1NJTkdfUklTS1MiLCJUQUtFX01PUkVfUklTS1MiXSxbIlBBU1NJTkdfU1RSQVRFR1kiLCJNT1JFX0RJUkVDVCJdLFsiU0hPT1RJTkciLCJTSE9PVF9NT1JFX09GVEVOIl1dfSwib3V0Ijp7InBvcyI6Ik1MIiwicm9sZSI6IlRyYWNraW5nIFdpZGUgTWlkZmllbGRlciIsInBpIjpbWyJUUklHR0VSX1BSRVNTIiwiTU9SRV9PRlRFTiJdLFsiVEFDS0xJTkciLCJFQVNFX09GRl9UQUNLTEVTIl1dfX0seyJpbiI6eyJwb3MiOiJBTUMiLCJyb2xlIjoiQWR2YW5jZWQgUGxheW1ha2VyIiwicGkiOltbIkFUVEFDS19CT1hfU0lERSIsIkZBUl9QT1NUIl0sWyJBVFRBQ0tJTkdfV0lEVEgiLCJNT1ZFX0lOVE9fQ0hBTk5FTFMiXSxbIkRSSUJCTElOR19GUkVRVUVOQ1kiLCJEUklCQkxFX0xFU1MiXSxbIlBBU1NJTkdfU1RSQVRFR1kiLCJNT1JFX0RJUkVDVCJdLFsiU0hPT1RJTkciLCJTSE9PVF9NT1JFX09GVEVOIl1dfSwib3V0Ijp7InBvcyI6Ik1DTCIsInJvbGUiOiJDZW50cmFsIE1pZGZpZWxkZXIiLCJwaSI6W1siVFJJR0dFUl9QUkVTUyIsIk1PUkVfT0ZURU4iXSxbIlRBQ0tMSU5HIiwiRUFTRV9PRkZfVEFDS0xFUyJdXX19LHsiaW4iOnsicG9zIjoiU1RDIiwicm9sZSI6IkNoYW5uZWwgRm9yd2FyZCIsInBpIjpbWyJBVFRBQ0tfQk9YX1NJREUiLCJORUFSX1BPU1QiXSxbIkZPUldBUkRfUlVOUyIsIk1BS0VfTU9SRV9SVU5TIl0sWyJTSE9PVElORyIsIlNIT09UX01PUkVfT0ZURU4iXSxbIlBBU1NJTkdfU1RSQVRFR1kiLCJNT1JFX0RJUkVDVCJdXX0sIm91dCI6eyJwb3MiOiJTVEMiLCJyb2xlIjoiVHJhY2tpbmcgQ2VudHJlIEZvcndhcmQiLCJwaSI6W1siVFJJR0dFUl9QUkVTUyIsIk1PUkVfT0ZURU4iXSxbIlRBQ0tMSU5HIiwiRUFTRV9PRkZfVEFDS0xFUyJdXX19XX0=
```

## A.3 两份代码结构对照

| 版本 | 球队指令 | 位置槽位 | 个人指令 | GEN1 代码长度（字符） | 生成器导入状态 |
|---|---:|---:|---:|---:|---|
| A4.3 BOX LANE ENGINE | 27 | 11 | 5 | 3165 | 未在本次文件构建中验证 |
| A4.11 COMPLETE TASK SPECIALISATION | 27 | 11 | 58 | 5561 | 未在本次文件构建中验证 |

**复制原则：** 不要复制时自行换行、加空格、删除字符或手工修改 Base64。需要变更指令时，先改对应 JSON payload，再用本手册的工具重新编码并运行 `validate`。