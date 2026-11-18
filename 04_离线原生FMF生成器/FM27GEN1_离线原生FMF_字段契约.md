# FM27GEN1 与离线原生 FMF 生成器字段契约

> **当前实现契约，2026-11-18。** 本文按当前分支的 `FM27GEN1_Offline_FMF_Generator.py`、`catalog.json`、`style_template_registry.json` 与自动测试整理。源码是实现事实的最终依据；旧版本记录不得覆盖当前源码。

## 1. 输入、输出与验收层次

正式输入是普通 UTF-8 JSON 战术对象，直接进入原生生成器；旧 GEN1 是为历史文件保留的兼容输入，不是正式流程必需步骤。正常交付必须实际调用离线生成器，获得新的 FM27 原生 `.fmf` 和同次运行的 `.report.json`，并通过完整 D3 独立回读。

| 层次 | 输入 | 输出/检查 |
|---|---|---|
| A 战术设计 | 用户目标和明确限制 | IP/OOP 阵型、22 阶段角色、duty、PI、TI |
| B 原生兼容 | 02 层位置/角色/职责/PI 权限资料 | 兼容配置和明确记录的未解决项 |
| C 原生 JSON | 设计结果 | 普通 UTF-8 JSON 对象，11 个槽位、每槽 in/out |
| D 云端原生生成与独立回读 | JSON、catalog、风格模板注册表、原生 FMF 模板 | 新 FMF、同次回读报告、D3 检查 |

**D3 是本项目唯一最终验收与交付标准。**

## 2. 原生 JSON 配方结构与旧 GEN1 兼容格式

### 2.1 正式原生 JSON 输入

- 文件扩展名：`.json`；内容为普通 UTF-8 JSON，根节点必须是对象。
- 不需要 `FM27GEN1:` 前缀、不需要 Base64 编码，不需要 GEN1 TXT 中间文件。
- 根字段：`v`、`name`、`ment`、`base`、`ti`、`p`。
- `v=1`；`ment` 必须为 1–7。
- `base.g` 是风格名，必须在 `style_template_registry.json` 中有登记；**当前已登记十种官方风格，不再局限于 Gegenpress**。
- `ti` 是单一共享球队指令对象，不区分 IP/OOP 两套 TI。
- `p` 正好 11 个槽位；每个槽位包含 `in` 和 `out`。
- 每个阶段必须包含 `pos`、`role`、`pi`；可选 `duty` 用于显式指定原生职责位。
- PI 项格式为 `[group, option]`。重复项、未知映射和权限冲突均拒绝。
- 生成器直接将 JSON 对象加载成 Python 字典，传入现有 `apply_recipe()`，然后执行原生 FMF 序列化和独立回读。报告字段 `recipe_input_format` 应为 `json`。
- 结构允许 `pi: []`，但本项目正式战术交付规则要求 22 个阶段均完成非空 PI；不能把结构接受等同于满足交付标准。

### 2.2 进程内结构化对象 API

- 正式生成核心公开函数：`build_fmf_from_recipe(recipe, catalog, style_registry=None, template_path=None)`。
- `recipe` 是已经解析的 Python `dict`；不需要先写成 JSON 文件，也不需要经过 `FM27GEN1:` 或 Base64。
- `base` 除必需的 `g` 外，兼容可选的 `ip`/`oop` 字符串元数据（官方风格回归配方使用）；实际 IP/OOP 位置与角色仍只从 `p[*].in/out` 读取。
- `validate_recipe_structure()` 会在读取原生模板前检查版本、心态、风格、11 个槽位、双阶段必填字段、PI 数组类型和未知字段；错误字段会直接拒绝，不会静默丢弃。
- 函数直接调用同一套 `apply_recipe()`、原生 FMF 写入和独立回读逻辑；CLI JSON 与历史 GEN1 入口也调用该函数，避免多套编码实现。
- 返回 `(fmf_bytes, report)`；报告的 `recipe_input_format` 默认为 `python_dict`，状态为 `offline_binary_roundtrip_verified_not_game_import_verified`，表示报告已确认离线二进制生成与回读。
- 此接口为 ChatGPT/其他宿主将对话设计结果直接交给原生生成器提供正式调用面；函数返回 FMF 字节和 D3 回读报告。
### 2.3 旧 GEN1 TXT 兼容输入

- 仅为读取历史文件保留：TXT 前缀 `FM27GEN1:`，后接 Base64 编码的 UTF-8 JSON。
- 生成器通过 `parse_gen1()` 读取该旧格式，报告 `recipe_input_format=legacy_gen1_base64`。
- 旧文件解码后仍进入相同的 `apply_recipe()`，不会形成第二套 FMF 编码分支。
- 新战术和正式云端构建不再要求 GEN1。

## 3. 风格与模板解析

当前风格识别由 `style_template_registry.json` 控制。注册表为每种风格登记：

- 风格名称；
- 原生 TAC style 字符串；
- 原生四字节 style code；
- FMF 模板相对路径；
- 样本 SHA256、source-major 和离线回读证据；

十种风格已登记并通过十风格生成烟雾测试。Control Possession 的上传样本 `1.fmf` 保留用于身份/样本审计，但因其 AOM 内部标题 token 重复，安全重写模板是 `123_Game_Export_Reference.fmf`。不得按文件名或风格中文名自行推测 FourCC/模板。

## 4. 位置与角色映射

- `catalog.json` 当前目录含 24 个原生位置、79 个阶段角色 ID（IP 40、OOP 39）及 24 个位置的角色资格矩阵。
- 网站层 62 个显示名称来自 `01_网站生成规则/Netlify_角色显示名称索引.csv`；它们与原生 79 个阶段 ID 属于不同口径。
- `role_id_from_display()` 将显示名规范化为内部 ID，并执行源码中明确登记的角色别名。未知角色直接拒绝。
- 当前位置别名：`DM→DMC`、`STC→ST`、`STCR→STR`、`STCL→STL`。生成器的 `native_position_id()` 当前会在写入路径使用这些规范化结果；最终应以回读报告中的位置为准。
- 每个 phase 要求 11 个唯一位置；角色 phase 必须匹配，且角色必须属于该位置的 `role_eligibility`。
- 不能将显示名称、内部角色 ID、位置代码或权限查询上下文混为一列，也不能仅凭近似名称匹配。
- `SW`、`DM` 不属于当前原生角色菜单权限的独立上下文；按 02 层 crosswalk 处理，不要伪造权限。

## 5. Duty

原生 JSON 的阶段对象允许可选 `duty` 字段；旧 GEN1 TXT 解码后的对象也遵循同一字段结构。优先采用此字段的显式原生 duty；未提供时再查源码 `ROLE_DUTY` 固定默认映射。

- 原生角色 duty 是独立于 role flag 的字段。当前 `ROLE_DUTY` 为 73/79 个角色提供历史样本/预设支持的默认 duty；其余 6 个没有可证明的固定默认值，不能按名称或相似角色猜测。
- 6 个需要显式选择的角色是 `PlaymakingWinger`、`OPCoveringWideCentreBack`、`OverlappingCentreBack`、`FalseNine`、`HalfBack`、`AdvancedCentreBack`。它们均存在于原生角色目录和位置资格数据中。
- JSON 每个阶段对象可选填写 `duty`：`"D"`/`"DEFEND"`、`"S"`/`"SUPPORT"`、`"A"`/`"ATTACK"`，或 `catalog.json.duties` 中的准确原生整数 bit。显式字段优先于角色默认值；未填写时才读取 `ROLE_DUTY`。如果该角色既无默认值又未显式指定，生成器报错。
- 显式 duty 仍必须属于 `DUTY_FLAGS`；随后 `encode_pi()` 使用选定的 phase/position/role/duty 查询权限策略。6 个角色的测试位置均具备 7 种目录 duty policy key，回归测试逐一确认可解析。
- 这使全部 79 个原生角色都能进入生成流程；其中 6 个需要战术配方作者明确选职责，而不是伪造一个默认映射。
- 回读检查写入 duty 与配方指定/解析出的期望值一致；这证明本次选择的 duty 映射被正确写入。

## 6. PI 映射与权限检查

### 6.1 数据来源

- 原始权限文件：`02_FM27原生权限规则/FM27_Role_PI_Permissions_Original.csv`。
- STC 查询扩展：`FM27_Role_PI_Permissions_Expanded_STC.csv`。
- 程序权限目录：`catalog.json` 的 `pi_policies`，当前有 1,547 个 policy key。
- 网站 serializer 的 7 类 `PI_KEY` 仅代表网页直接编码范围，不是原生权限数据的总范围。

### 6.2 当前执行逻辑

`encode_pi()` 按 `phase:position:roleid:duty` 生成 policy key，从 `catalog.pi_policies` 读取策略值，并对配方中的每个 `[group, option]`：

1. 检查格式、重复项与当前 `PI_MAP` 是否有原生 option ID。
2. 检查该 option ID 在适用 policy 记录中的索引范围。
3. 检查目录版本之间对该选项的状态是否一致；有冲突时拒绝猜测。
4. 按状态处理：`0=editable`（可写入）、`1=unavailable`（不可用）、`2=fixed off`（固定关闭）、`3=fixed on`（固定开启）。
5. 仅将可编辑项写入 mask；固定开启由角色本身提供，不重复序列化。

### 6.3 映射范围与边界

当前 `PI_MAP` 已有明确原生 option ID 的组合包括：

截至 2026-11-18 的目录对账，`catalog.json.player_instructions` 的 17 组中共有 37 个非默认原生 Option ID；当前 `PI_MAP` 已全部覆盖 37/37：

| 指令组 | 当前映射选项 |
|---|---|
| PASSING_STRATEGY | SHORTER、MORE_DIRECT |
| PASSING_RISKS | TAKE_MORE_RISKS、TAKE_FEWER_RISKS |
| DRIBBLING_FREQUENCY | DRIBBLE_MORE、DRIBBLE_LESS |
| DRIBBLING_DIRECTION | CUT_INSIDE_WITH_BALL、RUN_WIDE_WITH_BALL |
| SHOOTING | SHOOT_MORE_OFTEN、SHOOT_LESS_OFTEN |
| FORWARD_RUNS | MAKE_MORE_RUNS、KEEP_POSITION |
| ATTACKING_WIDTH | STAY_WIDER、SIT_NARROWER、MOVE_INTO_CHANNELS |
| ROAMING | ROAM_FROM_POSITION |
| HOLD_UP_BALL | YES |
| CROSSING_TARGET | BACK_POST、CENTRE、NEAR_POST、TARGET_FORWARD |
| CROSSING_FREQUENCY | BYLINE、FROM_DEEP |
| MARKING | MARK_TIGHTER |
| MARKING_TARGET | SPECIFIC_PLAYER、SPECIFIC_POSITION |
| TACKLING | GET_STUCK_IN、EASE_OFF_TACKLES |
| TRIGGER_PRESS | MORE_OFTEN、LESS_OFTEN |
| ATTACK_BOX_SIDE | CENTRE、NEAR_POST、FAR_POST、LEFT、RIGHT |
| ATTACK_BOX_DEPTH | LATE_RUNS、ATTACK_DEFENSIVE_LINE |

每项 ID 均直接取自 `catalog.json.player_instructions` 对应原生组。对 13 项本轮补齐的 PI ID，1,547 个 policy key 中均未发现跨目录版本状态冲突；`encode_pi()` 仍逐条按当前 phase/position/role/duty 检查，仅在状态为 `0=editable` 时写入。不可用、固定关闭和固定开启的选项不会被强制覆盖。

**指定盯防的边界：** `MARKING_TARGET=SPECIFIC_PLAYER/SPECIFIC_POSITION` 映射的是原生 PI option ID（34/35）及对应 mask。当前原生配方结构没有额外的被盯防球员 ID 或目标位置字段；因此这次补齐的是指令菜单标志写入，不宣称已实现具体盯防对象的选择/序列化。

生成器要求 `pi` 字段存在；空数组在代码层可接受。项目正式交付规范另要求 22/22 阶段各有至少一条经过权限核验的 PI。自动测试若用空数组做结构 smoke test，不代表正式战术达到该标准。

### 6.4 2026-11-18 首轮实验性 PI 映射历史记录

本次新增 6 项实验性 PI 映射。数字来自 `catalog.json.player_instructions` 中对应组的原生 Option ID，所选角色/位置/阶段权限已由 `pi_policies` 检查。离线写入及 TAC 回读通过。2026-11-18 用户将实验 FMF 导入 FM27 后反馈：**全部新增指令均已显示**，因此保留该批 PI 曾在 FM27 中显示的用户反馈，作为原生映射历史证据。

| 输入组 | 输入选项 | 原生 Option ID |
|---|---|---:|
| CROSSING_TARGET | BACK_POST | 10 |
| ROAMING | ROAM_FROM_POSITION | 24 |
| CROSSING_FREQUENCY | BYLINE | 8 |
| ATTACK_BOX_DEPTH | LATE_RUNS | 42 |
| TRIGGER_PRESS | LESS_OFTEN | 30 |
| TACKLING | GET_STUCK_IN | 31 |

本批映射由 `EXPERIMENTAL_PI_MAP` 单独登记，再并入生成路径。当时的实验报告曾使用 `game_import_display_verified_match_unverified` 状态标签；该标签仅是历史报告数据，不属于当前生成流程或项目验收状态。首次生成时的历史报告仍保留原始记录，不追改历史文件。

## 7. TI 映射、继承与风格 profile

- 网站规则层记录 27 项 TI；原生 `catalog.json` 有 29 组 `team_instructions`，数量口径不同。
- `official_style_team_instruction_profiles.json` 保存十种网站风格的心态与默认 TI；它来自 2026-11-16 HAR 中嵌入的 STYLE 表，不是 SI 原始 FMF 二进制风格证据。
- `TI_GROUPS` 声明可清理/设置的原生指令组；`TI_MAP` 声明 option→native bit 映射。当前 29/29 个原生组均已接入；75/75 个非零原生选项 bit 均有映射。未知组/选项直接拒绝。
- 每次从所选风格模板当前 12 字节向量开始；配方明确写出的 TI key 才清理对应 option group 并覆盖。JSON 配方未出现的 key 保留模板原有状态；值 `DEFAULT` 清空该 key 对应组。
- `SUPPORTING_RUNS`（原生组 28，肋部内套）与 `SUPPORTING_RUNS_SECONDARY`（原生组 31，外侧套上）现在分别清理各自组，避免设置一个维度时误清另一个维度。
- `GOALKEEPER_ATTACKING_SET_PIECES` 已接入原生组 32、bit 60。
- `ATTACKING_TRANSITION=HOLD_SHAPE` 已修正为原生 bit 55；旧映射 0 错误地把该选项当成默认值。
- 已知 template-owned opaque TI bits 为 33、34、74、75、76，按模板保留，不作为通用可编辑选项。
- 当前没有独立 IP/OOP TI 向量。配方中 TI 不可表达成两套阶段指令。

### 7.1 2026-11-18 首轮实验性 TI 映射（游戏导入显示验证通过）

本次新增 6 项 TI 映射。每一 bit 均与 `catalog.json.team_instructions` 对应原生组中的 `native_bit` 一致，通过离线向量回读。2026-11-18 用户反馈导入实验 FMF 后**全部新增指令均已显示**，因此保留该批 TI 曾在 FM27 中显示的用户反馈，作为原生映射历史证据。

| 输入组 | 输入选项 | 原生 bit |
|---|---|---:|
| DEFENSIVE_LINE | MUCH_HIGHER | 56 |
| PRESSING_TRAP | TRAP_INSIDE | 80 |
| CROSSING_STYLE | WHIPPED_CROSSES | 11 |
| PROGRESS_THROUGH | RIGHT | 22 |
| GOALKEEPER_DISTRIBUTION | PLAYMAKER | 39 |
| SUPPORTING_RUNS | RIGHT_INSIDE | 30 |

这些映射单独登记于 `EXPERIMENTAL_TI_MAP`。用户已确认本批新增项目在 FM27 导入后显示正常。

### 7.2 2026-11-18 原生目录剩余 TI 选项全量接入

通过 `catalog.json.team_instructions` 的原生组与 `native_bit` 对账，将剩余 14 个非零 bit 接入，并修正 `HOLD_SHAPE`。现有 6 项实验映射与新增映射合并后，75 个非零原生 bit 全部有且仅有一个写入映射：

| TI key | option | 原生组 ID | native bit |
|---|---|---:|---:|
| ATTACKING_TRANSITION | HOLD_SHAPE | 3 | 55 |
| DEFENSIVE_LINE | MUCH_LOWER | 9 | 59 |
| TRIGGER_PRESS | MUCH_LESS_OFTEN | 10 | 68 |
| GOALKEEPER_DISTRIBUTION | WIDE | 16 | 37 |
| GOALKEEPER_DISTRIBUTION | TARGET_FORWARD | 16 | 40 |
| GOALKEEPER_DISTRIBUTION | OVER_OPPOSITION_DEFENCE | 16 | 38 |
| CROSS_ENGAGEMENT | STOP_CROSSES | 22 | 82 |
| CROSSING_STYLE | HIGH_CROSSES | 26 | 10 |
| SHOTS_FROM_DISTANCE | ENCOURAGE | 27 | 15 |
| SUPPORTING_RUNS | LEFT_INSIDE | 28 | 29 |
| PROGRESS_THROUGH | LEFT | 30 | 21 |
| SUPPORTING_RUNS_SECONDARY | LEFT_OUTSIDE | 31 | 26 |
| SUPPORTING_RUNS_SECONDARY | RIGHT_OUTSIDE | 31 | 27 |
| SUPPORTING_RUNS_SECONDARY | BOTH_OUTSIDE | 31 | 25 |
| GOALKEEPER_ATTACKING_SET_PIECES | YES | 32 | 60 |

这批目录驱动映射均有明确原生组/bit 数据并通过新的自动对账测试；12 项首轮实验（6 PI + 6 TI）仍是当前已由用户确认 FM27 导入显示的项目。其余新接入项不被错误标记为已逐项游戏导入测试。

## 8. FMF 写入与独立回读

生成器要求 FM27 source-major 27 原生模板，并要求模板中存在 `.tac`、`.aom`、`.img` 成员。当前实现解包、解密/解压相关成员，更新 TAC/AOM 标题与战术字段，保持不应改动的原生封装/成员信息，再重建 FMF。

离线回读会检查 FMF/TAC 结构、11 个槽位、22 个阶段、唯一位置、角色/duty、PI mask、TI 向量、标题与 footer 等当前源码明确覆盖的字段。报告状态：

`offline_binary_roundtrip_verified_not_game_import_verified`

它只代表离线二进制生成与回读通过，不代表 FM27 客户端导入、保存/重开或比赛测试通过。

## 9. 当前自动测试覆盖

- `tests/test_fm27gen1_all_styles_generation.py`：十种风格模板和 style code 的生成/回读烟雾测试；当前 recipe 从样本提取角色/位置，但 PI 用 `[]`，TI 用 `{}` 继承模板。**它不是全 PI/TI 组合测试。**
- `tests/test_fm27gen1_native_style_samples.py`：原生样本解析/权限审计。
- `tests/test_fm27gen1_native_readback.py`：原生回读。
- `tests/test_fm27gen1_official_preset_index.py`：90 条网站预设索引审计。
- CI workflow 的具体断言范围以各 workflow 和测试源码为准。

当前新增回归测试对 37/37 PI 原生 option ID、75/75 TI native bit、29/29 TI 组和全部 TI 编码值逐项对账。角色职责层有 73 个有证据的默认 duty；其余 6 个可通过显式 duty 字段进入生成流程，不需要猜固定默认值。

## 10. Windows 命令行入口

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 FM27GEN1_Offline_FMF_Generator.py "TACTIC.json" --catalog "catalog.json" --output "TACTIC.fmf" --report "TACTIC.report.json"
```

正式入口直接使用普通 JSON 文件。旧版 `TACTIC_GEN1.txt` 仍可作为兼容输入传入同一 CLI。默认按 JSON 对象中的 `base.g` 从 `style_template_registry.json` 自动选模板。若显式传入 `--template`，必须与注册表中该风格指定的模板一致。输出文件存在时拒绝覆盖。

直接 JSON→FMF 的真实端到端构建由 `tests/test_fm27gen1_direct_json_input.py` 回归验证；该测试会调用正式生成器 CLI，验证生成文件和 D3 独立回读。

## 11. 规则更新要求

改动 `PI_MAP`、`TI_MAP`、`ROLE_DUTY`、位置别名或 style registry 时，必须同步更新本契约、00 总索引和对应自动测试。源码行为变化后，旧文档中“只支持 Gegenpress”或“PI permissions 未被生成器使用”等过期文字不得继续保留。
