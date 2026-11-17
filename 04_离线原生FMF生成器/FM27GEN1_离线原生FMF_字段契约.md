# FM27GEN1 与离线原生 FMF 生成器字段契约

> **当前实现契约，2026-11-17。** 本文按当前分支的 `FM27GEN1_Offline_FMF_Generator.py`、`catalog.json`、`style_template_registry.json` 与自动测试整理。源码是实现事实的最终依据；旧版本记录不得覆盖当前源码。

## 1. 输入、输出与验收层次

GEN1 是中间配方，不是原生战术文件。正常交付必须实际调用离线生成器，获得新的 FM27 原生 `.fmf` 和同次运行的 `.report.json`。

| 层次 | 输入 | 输出/检查 |
|---|---|---|
| A 战术设计 | 用户目标、比赛/球员数据、预设和样本 | IP/OOP 阵型、22 阶段角色、duty、PI、TI |
| B 原生兼容 | 02 层位置/角色/职责/PI 权限资料 | 兼容配置和未解决项 |
| C GEN1 | 设计结果 | FM27GEN1 v1 TXT，11 个槽位、每槽 in/out |
| D 离线生成 | GEN1、catalog、风格模板注册表、原生 FMF 模板 | 新 FMF、JSON 回读报告 |
| E 游戏内验收 | 新生成的 FMF | 导入、检查、保存、关闭并重开 |

D3 离线回读、D4 游戏内验证和 D5 比赛效果是不同证据等级，不得混称。

## 2. GEN1 v1 结构

- TXT 前缀：`FM27GEN1:`，后接 Base64 编码的 UTF-8 JSON。
- 根字段：`v`、`name`、`ment`、`base`、`ti`、`p`。
- `v=1`；`ment` 必须为 1–7。
- `base.g` 是风格名，必须在 `style_template_registry.json` 中有登记；**当前已登记十种官方风格，不再局限于 Gegenpress**。
- `ti` 是单一共享球队指令对象，不区分 IP/OOP 两套 TI。
- `p` 正好 11 个槽位；每个槽位包含 `in` 和 `out`。
- 每个阶段必须包含 `pos`、`role`、`pi`。
- PI 项格式为 `[group, option]`。重复项、未知映射和权限冲突均拒绝。
- 结构允许 `pi: []`，但本项目正式战术交付规则要求 22 个阶段均完成非空 PI；不能把结构接受等同于满足交付标准。

## 3. 风格与模板解析

当前风格识别由 `style_template_registry.json` 控制。注册表为每种风格登记：

- 风格名称；
- 原生 TAC style 字符串；
- 原生四字节 style code；
- FMF 模板相对路径；
- 样本 SHA256、source-major 和离线回读证据；
- 游戏内导入状态。

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

GEN1 v1 没有独立 duty 字段。生成器按内部角色 ID 查源码 `ROLE_DUTY` 固定映射，并检查其值属于 `DUTY_FLAGS` 允许集合。

- 缺少 `ROLE_DUTY` 映射时直接报错。
- catalog 保存原生 duty/权限资料；实际写入值仍由当前源码映射表决定。
- 不能据此宣称所有 79 个阶段角色 ID 的所有位置/phase/duty 组合都已穷举。
- 回读检查写入 duty 与生成器期望值一致；这证明当前映射被正确写入，不等于每个可能 duty 组合都已游戏内验证。

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

| 指令组 | 当前映射选项 |
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

原生权限资料比当前 `PI_MAP` 写入范围更广。**不要说缺少 PI 权限资料；应准确说明某项 PI 是否“有权限记录、但尚无写入 ID 映射”。** 未映射项目会失败，不得静默丢弃或猜测。

生成器要求 `pi` 字段存在；空数组在代码层可接受。项目正式交付规范另要求 22/22 阶段各有至少一条经过权限核验的 PI。自动测试若用空数组做结构 smoke test，不代表正式战术达到该标准。

## 7. TI 映射、继承与风格 profile

- 网站规则层记录 27 项 TI；原生 `catalog.json` 有 29 组 `team_instructions`，数量口径不同。
- `official_style_team_instruction_profiles.json` 保存十种网站风格的心态与默认 TI；它来自 2026-11-16 HAR 中嵌入的 STYLE 表，不是 SI 原始 FMF 二进制风格证据。
- `TI_GROUPS` 声明可清理/设置的原生指令组；`TI_MAP` 声明已证明的 option→native bit 映射。未知组/选项直接拒绝。
- 每次从所选风格模板当前 12 字节向量开始；配方明确写出的 TI key 才清理对应 option group 并覆盖。GEN1 未出现的 key 保留模板原有状态；值 `DEFAULT` 清空该 key 对应组。
- 已知 template-owned opaque TI bits 为 33、34、74、75、76，按模板保留，不作为通用可编辑选项。
- 当前没有独立 IP/OOP TI 向量。配方中 TI 不可表达成两套阶段指令。
- 十种 profile 数据存在，不等于每一种 TI 选项均已开放写入；应同时检查 `TI_MAP` 和原生目录。

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

下一阶段要扩展的是：以每种角色的非空真实 PI option、完整 TI option 组合、角色/duty/位置组合构造覆盖测试；不能通过降低测试断言或把空 PI 当成“全指令通过”。

## 10. Windows 命令行入口

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 FM27GEN1_Offline_FMF_Generator.py "TACTIC_GEN1.txt" --catalog "catalog.json" --output "TACTIC.fmf" --report "TACTIC.report.json"
```

默认按配方中的风格从 `style_template_registry.json` 自动选模板。若显式传入 `--template`，必须与注册表中该风格指定的模板一致。输出文件存在时拒绝覆盖。

## 11. 规则更新要求

改动 `PI_MAP`、`TI_MAP`、`ROLE_DUTY`、位置别名或 style registry 时，必须同步更新本契约、00 总索引和对应自动测试。源码行为变化后，旧文档中“只支持 Gegenpress”或“PI permissions 未被生成器使用”等过期文字不得继续保留。
