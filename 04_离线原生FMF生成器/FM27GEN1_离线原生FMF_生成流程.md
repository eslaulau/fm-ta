# FM27GEN1 离线原生 FMF 生成流程

> **当前流程版本：2026-11-17。** 当前分支已由 `style_template_registry.json` 接入十种官方风格。旧版本“只实现 Gegenpress”的文字已失效，不得继续引用为当前功能限制。  
> 首次查资料请先阅读上级 [00_资料总索引与检索规范](../00_资料总索引与检索规范.md)。

**执行源码：** `FM27GEN1_Offline_FMF_Generator.py`  
**目标格式：** FM27 source-major 27 原生 FMF  
**运行平台：** Windows / Python 3.12 x64

本流程以当前 Python 源码实际实现为准。正式产物是新生成的原生 `.fmf` 与同次生成的 `.report.json`；GEN1 TXT 只是输入配方。离线回读、FM27 游戏内导入和比赛效果是三个不同验收阶段。

## 全仓库战术使用政策（最高优先级）

本仓库的所有战术文件——包括十份原生样本、全部风格模板、历史战术配方、离线重建文件及网站预设——**一律不是推荐战术、不是成功战术，不得作为新战术开发参考**。不得从任何现存文件复制或继承阵型、角色、职责、PI、TI 或攻防结构，也不得以其作为新战术的种子、基准、优化方向或成绩证据。

生成器为满足 FMF 文件格式而读取模板时，只能将其视为必要的技术容器/二进制兼容来源；模板原有战术设置不构成设计依据。因格式兼容而保留的未知/opaque 字节必须标记为技术保留数据，不得解读为推荐设置。战术设计必须从用户当前目标和真实比赛数据独立开始。

## 1. 本目录运行文件

| 文件 | 用途 |
|---|---|
| `FM27GEN1_Offline_FMF_Generator.py` | 离线生成器源码 |
| `requirements.txt` | Python 依赖 |
| `安装依赖.bat` | 依赖安装入口 |
| `运行离线生成器.bat` | 内置样例/拖入 GEN1 的运行入口 |
| `catalog.json` | 原生位置、角色、角色资格、TI 目录及 PI 权限策略 |
| `style_template_registry.json` | 十种原生风格、FourCC、模板和验证证据登记表 |
| `official_style_team_instruction_profiles.json` | 从网站 HAR 提取的十种风格默认心态/TI 配方 |
| `123_Game_Export_Reference.fmf` | Control Possession 安全重写模板 |
| `FM27_4231_Gegenpress_Template.fmf` | Gegenpress 原生参考模板 |
| `FM27_A9.0.2_GEN1.txt` | 历史技术配方工件；仅用于追溯当时的离线转换输入 |
| `FM27_A9.0.2_Offline_Rebuild.fmf` 与对应 report | 历史离线转换/回读工件；不是成功战术样本 |

**A9.0.2 使用限制：** 这份文件没有完整赛季成功验证。其 report 只证明离线 FMF 二进制生成和回读，且明确记录 `game_interactive_import=false`、`match_engine=false`。因此它不是战术成绩基准，不是推荐模板，不是默认起点；新战术不得复制它的阵型、角色或 TI/PI 设计。除非用户明确要求审计这份旧工件，否则不要主动把它用于战术设计或优化。

十份上传原生样本 `1.fmf`–`10.fmf` 保存在上级战术生成规则根目录。具体风格与模板对应只以 `style_template_registry.json` 为准。

## 2. 当前支持的十种风格

当前注册表有十个 `implemented_sample_verified` 风格条目，包含 TAC 原生 style 字符串、4 字节 style code、模板路径和样本证据：

| 风格 | 注册表模板 |
|---|---|
| Control Possession | `123_Game_Export_Reference.fmf` |
| Gegenpress | 根目录 `2.fmf` |
| Tiki-Taka | 根目录 `3.fmf` |
| Vertical Tiki-Taka | 根目录 `4.fmf` |
| Wingplay | 根目录 `5.fmf` |
| Route One | 根目录 `6.fmf` |
| Fluid Counter Attack | 根目录 `7.fmf` |
| Direct Counter Attack | 根目录 `8.fmf` |
| Catenaccio | 根目录 `9.fmf` |
| Park The Bus | 根目录 `10.fmf` |

上传的 `1.fmf` 仍是 Control Possession 的原生样本证据；其 AOM 内部标题 token 重复，不作为安全重写模板。因此使用已验证的 `123_Game_Export_Reference.fmf`，不表示缺少该风格样本。

风格中文 TAC 字符串和四字节 code 不允许自行拼写或按文件编号猜测，必须由注册表解析。

## 3. 安装环境

安装 Python 3.12 x64。在本目录运行：

```powershell
py -3.12 -m pip install -r requirements.txt
```

依赖为 `cryptography>=42` 与 `zstandard>=0.25`。运行生成器不需要连接网站或游戏平台。

## 4. GEN1 输入契约

输入 TXT 必须以 `FM27GEN1:` 开头，后接严格 Base64 编码的 UTF-8 JSON。源码要求：

- 根版本 `v=1`；
- `p` 为 11 个槽位，每个槽位具有 `in`、`out`；
- `ment` 为 1–7；
- `base.g` 必须精确匹配 `style_template_registry.json` 中的十种风格之一；
- `ti` 是一个统一的球队指令对象；
- 每阶段必须提供 `pos`、`role`、`pi` 字段；
- PI 项为 `[group, option]` 二元数组。

生成器当前对缺少 `pi` 字段、重复 PI、未知 PI 映射和权限不允许项报错；但空数组 `pi: []` 在结构层可被接受。**项目正式交付标准要求 22/22 阶段至少有一条经权限验证的 PI**，所以不能把空 PI 烟雾测试当作正式战术完成。

## 5. 位置、角色和 duty

- 位置 ID 与角色 ID 读取自 `catalog.json`。
- 角色显示名通过 `role_id_from_display()` 转成原生内部 ID；OOP 角色使用 `OP` 前缀。
- 角色 phase 必须与 in/out 阶段一致。
- `role_eligibility[position][phase]` 必须允许该角色。
- IP 与 OOP 分别要求 11 个唯一位置。
- 当前代码位置别名：`DM→DMC`、`STC→ST`、`STCR→STR`、`STCL→STL`。最终以生成报告/回读中的原生位置为准。
- 生成器源码的 `ROLE_DUTY` 按原生角色 ID 固定 duty bit；没有映射的角色直接失败。GEN1 v1 本身没有独立 duty 字段。
- catalog 有完整的原生权限/职责数据，但不等于源码已经为所有角色写出全部可能 duty 变体。未登记项不能推测。

网站显示名 62 个、原生阶段角色 ID 79 个是不同数据口径。角色清单和位置权限详见上级 `02_FM27原生权限规则`。

## 6. PI 权限与映射

PI 的数据来源不是单一白名单：

- 原始权限 CSV：`../02_FM27原生权限规则/FM27_Role_PI_Permissions_Original.csv`；
- STC 查询扩展 CSV：`../02_FM27原生权限规则/FM27_Role_PI_Permissions_Expanded_STC.csv`；
- 程序权限表：`catalog.json` 的 `pi_policies`（当前 1,547 个 policy key）。

当前源码 `encode_pi()` 会按 `phase:position:roleid:duty` 查权限策略，并对当前 `PI_MAP` 中的选项做下列验证：

| 状态码 | 含义 | 生成处理 |
|---|---|---|
| 0 | 可编辑 | 允许写入选项 mask |
| 1 | 不可用 | 拒绝 |
| 2 | 固定关闭 | 拒绝 |
| 3 | 固定开启 | 不重复写入覆盖位 |

如果目录版本对目标选项的权限状态有冲突，生成器拒绝猜测。尚未进入 `PI_MAP` 的选项，即使权限表中存在，也不能直接写入；必须先有原生 option ID/掩码证据并增加测试。

## 7. TI 向量规则

- `official_style_team_instruction_profiles.json` 保存网站 HAR 提取的十种风格级默认心态和 TI 参考配方。
- `catalog.json` 有 29 组原生 TI 目录；网站索引记录 27 项 TI，统计口径不同。
- 当前源码通过 `TI_GROUPS` 和 `TI_MAP` 将已验证的配方值写入原生 bit。
- 未知 key 或未映射非默认 option 会报错；不会静默忽略。
- TI 向量从所选模板当前值开始，长度为 12 字节。仅 GEN1 明确指定的 TI key 会清理对应 option group 并覆盖；未指定 key 保留模板值，`DEFAULT` 清空对应组。
- 已知模板所有 opaque TI bits 为 33、34、74、75、76，按模板保留，不视为通用可编辑选项。
- 当前只有单一共享 TI 向量，没有独立的 IP/OOP 两套 TI。

## 8. 模板选择与生成命令

默认根据 `base.g` 从 `style_template_registry.json` 自动选择模板，不需要手动指定 `--template`。若显式指定模板，必须与该风格在注册表中的路径完全一致。

从本目录运行：

```powershell
py -3.12 FM27GEN1_Offline_FMF_Generator.py "NEW_TACTIC_GEN1.txt" --catalog "catalog.json" --output "NEW_TACTIC.fmf" --report "NEW_TACTIC.report.json"
```

参数说明：

| 参数 | 规则 |
|---|---|
| `recipe` | 必填，GEN1 TXT |
| `--catalog` | 必填，catalog.json |
| `--output` | 必填，新 FMF 输出路径 |
| `--report` | 可选；建议每次明确传入独立报告路径 |
| `--template` | 可选；若传入，必须与注册表该风格指定模板完全一致 |
| `--style-registry` | 可选；默认使用本目录 `style_template_registry.json` |

输出路径已存在时拒绝覆盖。成功返回 0，失败返回 2。必须确认本次 FMF 实际存在且非空，报告存在并且回读通过。

## 9. FMF 写入和独立回读

模板必须为 FM27 source-major 27 原生 FMF，且含有 `.tac`、`.aom`、`.img` 成员。当前源码会解析 FMF 容器、更新 TAC/AOM 对应字段、保留规定的原生 opaque 内容，再重建外层文件。

回读检查源码覆盖的容器/成员结构、11 个 IP/OOP pairs、22 阶段位置/角色/duty/PI mask、唯一位置、标题、style 字符串、style code、TI 向量与 footer 等。

状态 `offline_binary_roundtrip_verified_not_game_import_verified` 只证明离线二进制生成与回读，不代表游戏内已经导入、保存并重开，也不代表实战验证。

## 10. 当前自动测试覆盖范围

- `tests/test_fm27gen1_all_styles_generation.py`：十种风格/模板的生成与回读烟雾测试；构造配方使用 `pi: []`、`ti: {}`，因此不是全部 PI/TI 选项组合测试。
- `tests/test_fm27gen1_native_style_samples.py`：十份原生样本与样本内 PI/角色配置审计。
- `tests/test_fm27gen1_native_readback.py`：原生回读回归。
- `tests/test_fm27gen1_official_preset_index.py`：90 条网站预设索引专项审计。
- GitHub Actions 对样本审计、风格模板和回读测试执行 CI。

样本里已存在的 PI 位通过审计，不等于所有可选 PI 都已映射；十个模板 smoke test 通过，不等于所有角色/位置/duty 组合和所有 TI/PI 组合已经穷举。

## 11. 游戏内验收

只有当用户在 FM27 中实际导入该次生成的 FMF，检查阵型、位置、角色、职责、TI、PI，保存后关闭并重新打开，才可标记 D4。完成统一条件比赛测试后才可标记 D5。

已有某一份历史战术在游戏中载入成功，不得外推为所有风格/所有选项均已验证。
