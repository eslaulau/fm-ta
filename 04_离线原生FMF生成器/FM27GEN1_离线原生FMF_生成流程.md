# FM27GEN1 离线原生 FMF 生成流程

> **当前流程版本：2026-11-17。** 当前分支已由 `style_template_registry.json` 接入十种官方风格。旧版本“只实现 Gegenpress”的文字已失效，不得继续引用为当前功能限制。  
> 首次查资料请先阅读上级 [00_资料总索引与检索规范](../00_资料总索引与检索规范.md)。

**执行源码：** `FM27GEN1_Offline_FMF_Generator.py`  
**目标格式：** FM27 source-major 27 原生 FMF  
**运行平台：** Windows / Python 3.12 x64

本流程以当前 Python 源码实际实现为准。正式输入是**普通 UTF-8 JSON 战术配方**，直接进入原生生成器，不再经过 GEN1 前缀或 Base64 包装。旧 GEN1 TXT 仅保留向后兼容读取。正式产物是新生成的原生 `.fmf` 与同次生成的 `.report.json`；正式生成默认通过独立 GitHub Actions 云端构建工作流执行。**D3 原生 FMF 生成与独立回读是本项目唯一最终验收终点。**

## 全仓库战术使用政策（最高优先级）

本仓库的所有战术文件——包括十份原生样本、全部风格模板、历史战术配方、离线重建文件及网站预设——**一律不是推荐战术、不是成功战术，不得作为新战术开发参考**。不得从任何现存文件复制或继承阵型、角色、职责、PI、TI 或攻防结构，也不得以其作为新战术的种子、基准、优化方向或成绩证据。

生成器为满足 FMF 文件格式而读取模板时，只能将其视为必要的技术容器/二进制兼容来源；模板原有战术设置不构成设计依据。因格式兼容而保留的未知/opaque 字节必须标记为技术保留数据，不得解读为推荐设置。战术设计直接从用户当前目标和明确限制开始。只有用户明确要求时，才分析球队阵容、球员属性、历史比赛或对手数据；用户未要求时不主动执行，也不将其设为原创设计和 FMF 生成的前置条件。

## 战术创新原则（必须积极执行）

上述禁止复制和改造仓库现存战术的规则，目的是消除路径依赖，**不是限制创新**。本项目必须积极鼓励原创战术设计：

- 从用户当前目标和明确限制出发，从零提出战术解法；球队阵容、球员属性、历史比赛和对手数据分析只有在用户明确要求时才执行。不得先挑一个旧战术再做局部修改。
- 鼓励探索全新的攻防结构，包括但不限于非对称 IP/OOP 阵型、不同阶段的角色与职责重组、全新的 PI/TI 协同、压迫与回撤结构、攻防转换方式，以及不依赖单一传统风格的混合思路。
- 不受仓库现有战术文件、90 条网站预设、历史配方、模板或十种风格名称的战术思路限制。十种风格及其 style code 只是目前掌握的原生文件身份/格式兼容资料，不是必须遵循的战术蓝图，也不代表只有这十种战术思路才可创新。
- 如果当前 FMF 生成链路要求选择已登记的原生 style code 或技术模板，只能把它们作为文件序列化和兼容性载体；实际阵型、角色、职责、PI、TI 与整体攻防逻辑仍须独立原创，不能继承模板原有战术配置。
- 创新方案必须符合 FM27 当前可验证的位置、角色、职责、PI/TI 写入权限和文件格式约束。超出现有映射的想法应明确标记为待研究/待实现，不得静默降级或假装已经支持；超出现有映射的想法必须明确标记为待研究/待实现，不得伪装支持，也不得静默降级。

**研发方向：不寻找旧战术的改良版，而是从用户目标独立提出新的战术解法，并通过原生 FMF 的 D3 生成与回读完成交付。**

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

## 4. 原生 JSON 输入契约（正式入口）

正式输入是扩展名为 `.json` 的普通 UTF-8 文件，根节点直接是 JSON 对象。**不需要 `FM27GEN1:` 前缀、不需要 Base64 编码，也不需要额外生成 TXT 中间文件。**

对象结构沿用已经验证的战术字段：

- 根版本 `v=1`；
- `p` 为 11 个槽位，每个槽位具有 `in`、`out`；
- `ment` 为 1–7；
- `base.g` 必须精确匹配 `style_template_registry.json` 中已登记的风格；
- `ti` 是一个统一的球队指令对象；
- 每阶段必须提供 `pos`、`role`、`pi` 字段；可选 `duty` 用于明确指定角色职责；
- PI 项为 `[group, option]` 二元数组。

生成器将 JSON 解码为 Python 字典后，直接调用原有 `apply_recipe()`；角色/位置/duty、PI 权限和 TI 编码逻辑没有另写副本。输出报告的 `recipe_input_format` 应为 `json`。

旧版 GEN1 TXT 仍可通过 `.txt` 扩展名读取，输入必须以 `FM27GEN1:` 开头并含 Base64 JSON；其报告格式为 `legacy_gen1_base64`。这只是兼容旧文件的回退入口，不是新战术的正式工作流。

生成器对缺少 `pi` 字段、重复 PI、未知 PI 映射和权限不允许项报错；空数组 `pi: []` 在结构层可被接受。**项目正式交付标准要求 22/22 阶段至少有一条经权限验证的 PI**，所以不能把空 PI 烟雾测试当作正式战术完成。

## 5. 位置、角色和 duty

- 位置 ID 与角色 ID 读取自 `catalog.json`。
- 角色显示名通过 `role_id_from_display()` 转成原生内部 ID；OOP 角色使用 `OP` 前缀。
- 角色 phase 必须与 in/out 阶段一致。
- `role_eligibility[position][phase]` 必须允许该角色。
- IP 与 OOP 分别要求 11 个唯一位置。
- 当前代码位置别名：`DM→DMC`、`STC→ST`、`STCR→STR`、`STCL→STL`。最终以生成报告/回读中的原生位置为准。

### 角色选择政策：主动探索，不向现有映射保守收缩

- **79 个原生角色全部是战术设计候选。** 角色选择必须由本次战术模型、职责分工和位置适配决定；不得因为角色罕见、历史配方没有用过、旧战术很少出现，或当前生成器还没有映射，就将其排除。
- 不得默认只从现有 `ROLE_DUTY` 的 73 个角色中选择，也不得为了方便生成而优先选一个战术适配度较差的常见角色。
- 设计顺序必须是：先选择最能实现战术意图的原生角色，再处理生成器映射；不能让当前代码覆盖范围反过来限制战术设计。
- 目前另有 6 个原生角色没有 `ROLE_DUTY` 写入映射。它们仍然是有效设计候选。若战术方案选中其中任何一个，必须先从原生资源、角色/职责数据及可核对的原生分配证据中补齐其角色→duty 映射和测试，不得仅为绕过代码缺口而自动替换角色。
- 只有在完成证据检索后仍不能确定某个 duty 时，才报告该角色的精确映射缺口；保留原设计选择，不得猜测职责，也不得静默换角。
- 原生 JSON 阶段对象可以包含可选 `duty`，以 D/S/A 或原生 duty 整数明确指定职责；未填写时仍按 73 个有证据的默认映射处理。其余 6 个角色必须显式填写 duty。旧 GEN1 TXT 解码后也使用相同的阶段对象结构。

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

从本目录运行（正式原生 JSON 输入）：

```powershell
py -3.12 FM27GEN1_Offline_FMF_Generator.py "NEW_TACTIC.json" --catalog "catalog.json" --output "NEW_TACTIC.fmf" --report "NEW_TACTIC.report.json"
```

旧版 `NEW_TACTIC_GEN1.txt` 仍可作为兼容输入传入同一命令。

参数说明：

| 参数 | 规则 |
|---|---|
| `recipe` | 必填，普通 UTF-8 JSON；兼容 `.txt` GEN1 |
| `--catalog` | 必填，catalog.json |
| `--output` | 必填，新 FMF 输出路径 |
| `--report` | 可选；建议每次明确传入独立报告路径 |
| `--template` | 可选；若传入，必须与注册表该风格指定模板完全一致 |
| `--style-registry` | 可选；默认使用本目录 `style_template_registry.json` |

输出路径已存在时拒绝覆盖。成功返回 0，失败返回 2。必须确认本次 FMF 实际存在且非空，报告存在并且回读通过。

## 8.1 正式云端战术构建流程（默认正式交付通道）

新战术不需要 GEN1。普通对话中的正式交付采用**助手直接提交仓库 JSON 文件**的方式；Actions 页面内联 JSON 和 `repository_dispatch` 保留给维护/外部自动化，共用同一原生生成器：

1. **正式默认：助手提交仓库 JSON。** 战术设计完成后，助手直接把唯一一份 UTF-8 JSON 请求提交到 `build_requests/`，push 到 `main` 自动触发 **FM27 Tactic Build**。用户无需创建文件、操作 Actions 页面或运行桌面命令。助手负责定位本次 run、下载 artifact、核验 FMF/report 并在对话中交付。
2. **Actions 内联 JSON（维护入口）：** 仓库维护者可在 Actions 页面手动运行 **FM27 Tactic Build**，只填写 `recipe_json`，不填写 `recipe_path`。输入作为 workflow output/env 传给 Python 构建进程，不创建 runner 临时配方文件。
3. **repository_dispatch（外部自动化入口）：** 事件类型为 `fm27_tactic_build`，完整对象放在 `client_payload.recipe`。不创建配方文件。

旧版 `.txt` 的 `FM27GEN1:Base64` 只保留读取兼容。三种正式入口都不需要 GEN1 中间格式。

### A. 输入与项目级配方检查

1. 完成原创战术设计、11 个槽位、22 个 IP/OOP 阶段、角色/职责、TI 和 PI 配置。
2. 每个阶段必须至少有一条有效 PI。`scripts/validate_fm27_tactic_delivery.py` 对正式云端构建强制执行 **22/22 非空 PI**；通用 API 仍允许空数组用于结构烟雾测试。
3. 输入解析由 `scripts/resolve_fm27_tactic_recipe.py` 完成：校验事件类型、JSON 对象、唯一输入和仓库路径边界。内联 JSON 只落在 `$RUNNER_TEMP`，不会写入仓库。

### B. 触发独立构建工作流

正式构建工作流为 `.github/workflows/fm27-tactic-build.yml`。普通对话任务由助手提交 `build_requests/*.json` 触发 push；Actions 页面 `recipe_json` 仅供维护调试；`repository_dispatch` 供具备调用权限的外部自动化使用。`workflow_dispatch` 必须且只能选择 `recipe_path` 或 `recipe_json` 其中一种输入。

仓库路径模式只接受位于 `build_requests/` 直接子目录中的一份 `.json` 或历史 `.txt` 配方。路径穿越、多个请求、空请求、非对象 JSON 均会被拒绝。

### C. 云端环境与原生生成

GitHub Actions 在 `ubuntu-latest` runner 中执行：

1. checkout 生成器源码、`catalog.json`、风格注册表和所有原生模板；内联对象通过 workflow output/env 变量传递，不落地为临时配方文件；
2. 安装 Python 3.12 与生成器依赖；
3. 执行 `validate_fm27_tactic_delivery.py`，强制 22/22 阶段至少一条 PI；
4. 将结构化对象解码为 Python 字典，调用 `build_fmf_from_recipe(dict, catalog)` 同一正式 API；
5. 使用 `apply_recipe()` 现有逻辑执行位置/角色/duty、PI 权限、TI 编码、风格模板选择及 FMF 写入；
6. 生成同次运行的原生 `.fmf` 与 `.report.json`，再执行完整 D3 回读和 SHA256/长度检查。

CLI 等价命令：

```bash
python "04_离线原生FMF生成器/FM27GEN1_Offline_FMF_Generator.py" \
  "build_requests/Vertical_Overload_v1.json" \
  --catalog "04_离线原生FMF生成器/catalog.json" \
  --output "$RUNNER_TEMP/Vertical_Overload_v1_runNN.fmf" \
  --report "$RUNNER_TEMP/Vertical_Overload_v1_runNN.report.json"
```

内联对象报告中的 `recipe_input_format` 为 `python_dict`；仓库 `.json` 文件为 `json`；历史 GEN1 为 `legacy_gen1_base64`。未知角色、职责映射缺口、PI/TI 未映射选项、权限冲突、模板风格不匹配或原生容器异常均必须使构建失败；不得自动删指令、静默降级或擅自替换角色。

### D. 自动回归与 D3 独立回读

云端工作流执行 `tests/test_fm27gen1_direct_json_input.py` 和实验映射测试，并调用 `validate_fm27_tactic_delivery.py` 对本次输入强制检查 22/22 非空 PI；原生生成器再逐项检查映射和具体角色/位置/duty 权限，最后构建本次 FMF。CI 另有 `tests/test_fm27gen1_input_resolution.py` 覆盖内联输入、dispatch 对象、仓库文件、删除事件跳过与路径安全。

必须确认 FMF 文件存在且非空、report 状态为 `offline_binary_roundtrip_verified_not_game_import_verified`，并通过容器/成员校验、TAC 完整解析、11 组 IP/OOP、22 阶段位置/角色/duty/PI、TI 向量和原生风格回读检查，同时核对报告字节数和 SHA-256。任何检查失败都不上传 artifact。

### E. 上传、取回与交付

全部检查通过后，上传一个同名 artifact：

```text
FM27_<配方名>_run<运行号>
├── <战术名>.fmf
└── <战术名>.report.json
```

Artifact 保留 14 天。助手定位本次 Actions run、下载并检查两个文件，再直接交付 FMF 和 report；不要求用户自行寻找 GitHub 下载页面，也不在没有成功取回 artifact 时声称已交付。

### F. 工作流分工与本机备用

- `fm27-tactic-build.yml`：处理某一份指定的 JSON 原创战术，输出该次 FMF、报告和 artifact。
- `fm27-native-tactics-regression.yml`：继续负责原生样本、映射和固定回归测试，不代替指定战术的正式构建入口。
- Windows 本地备用构建可直接把 `.json` 文件传给同一生成器，不需要先编码 GEN1。

## 9. FMF 写入和独立回读

模板必须为 FM27 source-major 27 原生 FMF，且含有 `.tac`、`.aom`、`.img` 成员。当前源码会解析 FMF 容器、更新 TAC/AOM 对应字段、保留规定的原生 opaque 内容，再重建外层文件。

回读检查源码覆盖的容器/成员结构、11 个 IP/OOP pairs、22 阶段位置/角色/duty/PI mask、唯一位置、标题、style 字符串、style code、TI 向量与 footer 等。

状态 `offline_binary_roundtrip_verified_not_game_import_verified` 表示 D3 原生 FMF 二进制生成与独立回读通过；这是本项目的最终交付状态。

## 10. 当前自动测试覆盖范围

- `tests/test_fm27gen1_all_styles_generation.py`：十种风格/模板的生成与回读烟雾测试；构造配方使用 `pi: []`、`ti: {}`，因此不是全部 PI/TI 选项组合测试。
- `tests/test_fm27gen1_native_style_samples.py`：十份原生样本与样本内 PI/角色配置审计。
- `tests/test_fm27gen1_native_readback.py`：原生回读回归。
- `tests/test_fm27gen1_official_preset_index.py`：90 条网站预设索引专项审计。
- `tests/test_fm27gen1_direct_json_input.py`：JSON CLI 与 Python dict API 输出字节一致、完整 D3 回读和严格 schema 测试。
- `tests/test_fm27gen1_input_resolution.py`：三类云端输入、路径边界和 Unicode artifact 命名测试。
- `tests/test_fm27gen1_delivery_contract.py`：22/22 阶段非空 PI 交付门槛。
- GitHub Actions 对样本审计、风格模板和回读测试执行 CI。

样本里已存在的 PI 位通过审计，不等于所有可选 PI 都已映射；十个模板 smoke test 通过，不等于所有角色/位置/duty 组合和所有 TI/PI 组合已经穷举。

## 11. 最终验收与交付

本项目在 D3 完成：指定战术的原生 `.fmf` 已生成；同次 `.report.json` 可解析；容器、TAC、11 组 IP/OOP、22 阶段、角色、职责、PI/TI 和风格字段的源码覆盖范围内回读检查全部通过；文件长度与 SHA-256 和报告一致；GitHub Actions artifact 已成功下载并检查。助手随后直接向用户交付实际 `.fmf` 和 `.report.json`。

上述条件全部满足，即视为战术生成任务完整完成，不设置额外的游戏客户端或比赛测试阶段。
