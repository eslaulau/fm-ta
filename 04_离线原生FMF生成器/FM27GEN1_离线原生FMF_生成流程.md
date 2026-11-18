# FM27GEN1 离线原生 FMF 生成流程

> **当前流程版本：2026-11-17。** 当前分支已由 `style_template_registry.json` 接入十种官方风格。旧版本“只实现 Gegenpress”的文字已失效，不得继续引用为当前功能限制。  
> 首次查资料请先阅读上级 [00_资料总索引与检索规范](../00_资料总索引与检索规范.md)。

**执行源码：** `FM27GEN1_Offline_FMF_Generator.py`  
**目标格式：** FM27 source-major 27 原生 FMF  
**运行平台：** Windows / Python 3.12 x64

本流程以当前 Python 源码实际实现为准。正式产物是新生成的原生 `.fmf` 与同次生成的 `.report.json`；GEN1 TXT 只是输入配方。正式生成默认通过独立 GitHub Actions 云端构建工作流执行；本地命令作为备用。离线回读、FM27 游戏内导入和比赛效果是三个不同验收阶段。

## 全仓库战术使用政策（最高优先级）

本仓库的所有战术文件——包括十份原生样本、全部风格模板、历史战术配方、离线重建文件及网站预设——**一律不是推荐战术、不是成功战术，不得作为新战术开发参考**。不得从任何现存文件复制或继承阵型、角色、职责、PI、TI 或攻防结构，也不得以其作为新战术的种子、基准、优化方向或成绩证据。

生成器为满足 FMF 文件格式而读取模板时，只能将其视为必要的技术容器/二进制兼容来源；模板原有战术设置不构成设计依据。因格式兼容而保留的未知/opaque 字节必须标记为技术保留数据，不得解读为推荐设置。战术设计必须从用户当前目标和真实比赛数据独立开始。

## 战术创新原则（必须积极执行）

上述禁止复制和改造仓库现存战术的规则，目的是消除路径依赖，**不是限制创新**。本项目必须积极鼓励原创战术设计：

- 从用户当前目标、球队球员特点、真实比赛数据和对手问题出发，从零提出战术解法；不得先挑一个旧战术再做局部修改。
- 鼓励探索全新的攻防结构，包括但不限于非对称 IP/OOP 阵型、不同阶段的角色与职责重组、全新的 PI/TI 协同、压迫与回撤结构、攻防转换方式，以及不依赖单一传统风格的混合思路。
- 不受仓库现有战术文件、90 条网站预设、历史配方、模板或十种风格名称的战术思路限制。十种风格及其 style code 只是目前掌握的原生文件身份/格式兼容资料，不是必须遵循的战术蓝图，也不代表只有这十种战术思路才可创新。
- 如果当前 FMF 生成链路要求选择已登记的原生 style code 或技术模板，只能把它们作为文件序列化和兼容性载体；实际阵型、角色、职责、PI、TI 与整体攻防逻辑仍须独立原创，不能继承模板原有战术配置。
- 创新方案必须符合 FM27 当前可验证的位置、角色、职责、PI/TI 写入权限和文件格式约束。超出现有映射的想法应明确标记为待研究/待实现，不得静默降级或假装已经支持；通过 D4 游戏内验收和 D5 统一条件实战验证后，才能评价其可用性和效果。

**研发方向：不寻找旧战术的改良版，而是提出新的战术解法，再用真实比赛数据验证、迭代。**

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

### 角色选择政策：主动探索，不向现有映射保守收缩

- **79 个原生角色全部是战术设计候选。** 角色选择必须由本次战术模型、职责分工和位置适配决定；不得因为角色罕见、历史配方没有用过、旧战术很少出现，或当前生成器还没有映射，就将其排除。
- 不得默认只从现有 `ROLE_DUTY` 的 73 个角色中选择，也不得为了方便生成而优先选一个战术适配度较差的常见角色。
- 设计顺序必须是：先选择最能实现战术意图的原生角色，再处理生成器映射；不能让当前代码覆盖范围反过来限制战术设计。
- 目前另有 6 个原生角色没有 `ROLE_DUTY` 写入映射。它们仍然是有效设计候选。若战术方案选中其中任何一个，必须先从原生资源、角色/职责数据及可核对的原生分配证据中补齐其角色→duty 映射和测试，不得仅为绕过代码缺口而自动替换角色。
- 只有在完成证据检索后仍不能确定某个 duty 时，才报告该角色的精确映射缺口；保留原设计选择，不得猜测职责，也不得静默换角。
- GEN1 v1 本身没有独立 duty 字段；duty 由生成器按原生角色 ID 映射写入。因此需要新角色时，应先扩展生成器，再继续该战术的 FMF 生成。

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

## 8.1 正式云端战术构建流程（默认正式交付通道）

正式开发新战术时，默认由 GitHub Actions 云端运行本目录的 Python 生成器。这样，战术研发与 FMF 序列化分工明确：设计阶段产出 GEN1，云端构建阶段负责调用现有生成器、生成原生文件、执行独立回读和打包交付。

### A. 输入：准备本次唯一 GEN1 配方

1. 完成原创战术设计、22 个阶段角色/职责配置、TI/PI 配置和 GEN1 预检。
2. 将本次完整 GEN1 配方保存为 UTF-8 TXT，文件内容为单行 `FM27GEN1:` + 标准 Base64 JSON。
3. 将文件放入仓库根目录的 `build_requests/`，例如：

```text
build_requests/Vertical_Overload_v1_GEN1.txt
```

4. 每个构建 commit 只新增或修改一份要构建的 `build_requests/*.txt`。配方文件本身作为本次构建输入留在仓库，便于追溯；不把输出 FMF 提交到源码目录。

### B. 触发：独立构建工作流

正式构建工作流：

```text
.github/workflows/fm27-tactic-build.yml
```

默认触发方式：将一份 GEN1 TXT 提交并 push 到 `main` 分支的 `build_requests/` 目录。该路径变化只触发独立的 **FM27 Tactic Build** 工作流，不需要修改或借用 `fm27-native-tactics-regression.yml` 回归测试工作流。

也可以在 GitHub Actions 页面手动运行 **FM27 Tactic Build**，将 `recipe_path` 输入为仓库中已有的配方路径，用于重新构建同一配方。

工作流会检查：
- 输入路径必须位于 `build_requests/`；
- 文件必须存在且为 TXT；
- 本次触发必须只对应一份 GEN1 配方；
- 不允许路径穿越、空文件名或不明确的多配方构建。

### C. 云端环境：准备原生生成器

GitHub Actions 在 `ubuntu-latest` runner 中执行：

1. checkout 当前仓库，取得 GEN1、生成器源码、`catalog.json`、风格注册表和所有原生模板；
2. 安装 Python 3.12；
3. 执行 `pip install -r 04_离线原生FMF生成器/requirements.txt`；
4. 根据配方名称生成唯一输出名，输出路径放在 runner 临时目录，不覆盖仓库文件或历史构建产物。

云端构建不需要启动用户本机 FM27，也不需要连接 Steam 或游戏平台。

### D. 实际生成：调用正式 Python 生成器

工作流调用的实际命令等价于：

```bash
python "04_离线原生FMF生成器/FM27GEN1_Offline_FMF_Generator.py" \
  "build_requests/Vertical_Overload_v1_GEN1.txt" \
  --catalog "04_离线原生FMF生成器/catalog.json" \
  --output "$RUNNER_TEMP/Vertical_Overload_v1_runNN.fmf" \
  --report "$RUNNER_TEMP/Vertical_Overload_v1_runNN.report.json"
```

生成器实际负责：
- 解码 GEN1 并解析战术结构；
- 按 `base.g` 查询 `style_template_registry.json`，自动选取匹配的原生风格模板；
- 读取 FMF 容器并解析原生 TAC；
- 将 IP/OOP 位置、角色、职责、PI mask、TI 向量、心态、标题和 style code 写入对应原生字段；
- 按原生封装规则重建 FMF，保留需要保持不变的成员和 opaque 数据；
- 在同一次运行中生成 JSON 报告。

未知角色、职责映射缺口、PI/TI 未映射选项、权限冲突、模板风格不匹配或原生容器异常，均必须使构建失败。工作流不得自动删掉指令、静默降级、擅自替换角色或用旧 FMF 冒充本次输出。

### E. 自动验收：D3 独立回读

生成器执行后，工作流继续检查本次 `.fmf` 和同次 `.report.json`：

1. FMF 文件存在且非空；
2. report 存在、可解析，状态必须为 `offline_binary_roundtrip_verified_not_game_import_verified`；
3. FMF 外层容器往返、成员解密/解压及校验、TAC 完整解析全部通过；
4. 11 组 IP/OOP 槽位通过；
5. 22 个阶段的设计表与独立回读表均完整；
6. 22 个阶段的位置、角色、职责、PI 回读与本次配方一致；
7. PI 权限查询、TI 向量、原生风格字符串和四字节 style code 回读检查通过。

只要生成器退出码非 0、FMF/report 缺失、报告状态不符或任一 D3 检查失败，工作流即失败，并且不上传成功构建 artifact。失败时读取日志中的精确错误，补齐对应映射/权限或修正配方，再重新触发；不能通过静默删减配置来换取构建成功。

### F. 打包：上传本次构建 Artifact

全部 D3 检查通过后，工作流使用 `actions/upload-artifact@v4` 上传一个同名构建包：

```text
FM27_<配方名>_run<运行号>
├── <战术名>.fmf
└── <战术名>.report.json
```

Artifact 保留 14 天。GEN1 源文件则保留在仓库的 `build_requests/` 中。工作流摘要会列出配方路径、FMF 文件名、文件大小、SHA256、风格和 D3 状态，便于核对是哪一次构建。

### G. 取回并交付给用户

构建完成后，助手通过 GitHub Actions 运行记录定位本次 run 和 artifact，下载 ZIP，在当前工作环境解压并检查其中的两个文件，然后直接向用户提供：
- 实际生成的 `.fmf` 附件；
- 同次生成的 `.report.json` 附件；
- 本次 GEN1 配方源文件和简短战术说明。

不能只把 GitHub 仓库路径或 Actions 页面地址交给用户自行寻找，也不能在未成功取回 artifact 时声称文件已经交付。

### H. 与回归测试工作流的分工

- `fm27-tactic-build.yml`：处理某一份指定原创战术，输出该次 FMF、报告和可下载 artifact。
- `fm27-native-tactics-regression.yml`：继续执行原生样本、映射、自动测试和固定 smoke test；它不是每次原创战术的正式构建入口。

### I. 本机备用构建

如果 GitHub Actions 暂时不可用，可在 Windows/Python 3.12 环境使用本节前面的本地命令完成同样的生成和回读；但正式云端交付默认以独立构建工作流为准。

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
