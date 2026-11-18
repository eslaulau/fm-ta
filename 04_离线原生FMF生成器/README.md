# FM27GEN1 离线原生 FMF 战术生成器

> 统一资料入口：先阅读上级 [00_资料总索引与检索规范](../00_资料总索引与检索规范.md)。当前源码字段和映射的准确说明以同目录 [FM27GEN1_离线原生FMF_字段契约](FM27GEN1_离线原生FMF_字段契约.md) 为准。

**正式生成器：** `FM27GEN1_Offline_FMF_Generator.py`

本版本已接入用户上传的 `1.fmf`–`10.fmf` 十份 FM27 原生样本，完成十种官方风格的 TAC 身份识别、原生四字节 style code 登记、模板验证和按风格自动选模板。

## 全仓库战术使用政策（必须遵守）

本仓库所有 FMF 战术、十份原生样本、各风格模板、历史重建文件和其他战术配方，**全部非推荐战术、非成功战术，不得作为新战术开发参考**。不得复制或继承其中的阵型、角色、职责、PI、TI 或整体攻防配置，也不得把离线生成/回读成功理解为战术实战成功。

这些文件只允许在必要时用于原生 FMF 容器、字段编码、style code、二进制结构和生成器兼容性研究。技术模板作为容器基础时，不代表其战术内容被采纳；未知/opaque 数据若因格式兼容而保留，也不得视为战术建议或性能证据。新战术的战术设计必须独立完成。

## 战术创新原则（必须积极执行）

上述禁止复制和改造仓库现存战术的规则，目的是消除路径依赖，**不是限制创新**。本项目必须积极鼓励原创战术设计：

- 从用户当前目标和明确限制出发，从零提出战术解法；球队阵容、球员属性、历史比赛和对手数据分析只有在用户明确要求时才执行。不得先挑一个旧战术再做局部修改。
- 鼓励探索全新的攻防结构，包括但不限于非对称 IP/OOP 阵型、不同阶段的角色与职责重组、全新的 PI/TI 协同、压迫与回撤结构、攻防转换方式，以及不依赖单一传统风格的混合思路。
- 不受仓库现有战术文件、90 条网站预设、历史配方、模板或十种风格名称的战术思路限制。十种风格及其 style code 只是目前掌握的原生文件身份/格式兼容资料，不是必须遵循的战术蓝图，也不代表只有这十种战术思路才可创新。
- 如果当前 FMF 生成链路要求选择已登记的原生 style code 或技术模板，只能把它们作为文件序列化和兼容性载体；实际阵型、角色、职责、PI、TI 与整体攻防逻辑仍须独立原创，不能继承模板原有战术配置。
- 创新方案必须符合 FM27 当前可验证的位置、角色、职责、PI/TI 写入权限和文件格式约束。超出现有映射的想法应明确标记为待研究/待实现，不得静默降级或假装已经支持；通过 D4 游戏内验收和 D5 统一条件实战验证后，才能评价其可用性和效果。

**研发方向：不寻找旧战术的改良版，而是提出新的战术解法，再用真实比赛数据验证、迭代。**

## 十种官方风格

| 官方风格 | 原生 style code | 模板 |
|---|---|---|
| Control Possession | `544e4f43` | `123_Game_Export_Reference.fmf` |
| Gegenpress | `45474547` | `../2.fmf` |
| Tiki-Taka | `494b4954` | `../3.fmf` |
| Vertical Tiki-Taka | `54524556` | `../4.fmf` |
| Wingplay | `474e4957` | `../5.fmf` |
| Route One | `54554f52` | `../6.fmf` |
| Fluid Counter Attack | `49554c46` | `../7.fmf` |
| Direct Counter Attack | `45524944` | `../8.fmf` |
| Catenaccio | `45544143` | `../9.fmf` |
| Park The Bus | `4b524150` | `../10.fmf` |

风格名称、TAC 原生字符串和 style code 均以样本实际解析结果为准，不按文件编号猜测。上传的 `1.fmf` TAC 已识别为 Control Possession，代码为 `544e4f43`；但它的 AOM 内部标题重复，不能安全地作为重写模板，因此 Control Possession 继续使用已验证的 `123_Game_Export_Reference.fmf`。


## 样本使用边界：A9.0.2 不是成功战术

仓库中的 `FM27_A9.0.2_GEN1.txt`、`FM27_A9.0.2_Offline_Rebuild.fmf` 和对应 report 只作为历史技术工件保存。它们证明的是当时的 GEN1→FMF 离线转换与二进制回读，不是完整赛季战术表现证据。

**不得把 A9.0.2 当作成功案例、推荐战术、默认生成模板、优化起点或其他战术的设计基准。** 它没有完成完整赛季成功验证；对应报告中的 `game_interactive_import=false`、`match_engine=false` 也明确表示没有游戏内导入与比赛引擎证据。除非用户明确要求检查这份历史文件，否则生成新战术时应从用户当前目标和明确限制独立设计；只有用户明确要求时才分析球队/比赛数据。不能因 A9.0.2 曾被生成就复制其阵型、角色或指令。

## 实验性未映射指令导入测试

2026-11-18 新增一批实验性 PI/TI 映射，并构建 `build_requests/Unmapped_Mapping_Import_Test_v1.txt` 进行 FMF 实验。原生目录对照、22 个阶段 PI 权限及离线 FMF 回读均通过。2026-11-18 用户反馈导入 FM27 后新增球队指令和球员指令全部显示，故本批映射已通过游戏内导入显示验证；比赛效果仍未验证。对应测试为 `tests/test_fm27gen1_experimental_unmapped_mapping.py`，明细见 [字段契约](FM27GEN1_离线原生FMF_字段契约.md)。

## 内存对象直连 API（不经过文件中间层）

生成器现在公开 `build_fmf_from_recipe(recipe, catalog, style_registry=None, template_path=None)`。

调用方若已在内存中得到完整 Python `dict`，可直接得到原生 FMF 字节和同次回读报告；不需要先保存 `.json`，更不需要 GEN1/Base64。命令行 JSON 和旧 GEN1 输入也共用该函数，因此不会分叉出第二套 FMF 编码路径。 `validate_recipe_structure()` 会先拒绝未知根字段/阶段字段、缺失的 `pi`、错误心态类型、非 11 槽阵型等结构错误。

```python
import json
from pathlib import Path
import sys

generator_dir = Path(r"04_离线原生FMF生成器")
sys.path.insert(0, str(generator_dir.resolve()))
import FM27GEN1_Offline_FMF_Generator as gen

recipe = json.loads(Path("NEW_TACTIC.json").read_text(encoding="utf-8"))
catalog = json.loads((generator_dir / "catalog.json").read_text(encoding="utf-8"))
fmf_bytes, report = gen.build_fmf_from_recipe(recipe, catalog)
Path("NEW_TACTIC.fmf").write_bytes(fmf_bytes)
Path("NEW_TACTIC.report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
)
```

返回报告默认标记 `recipe_input_format=python_dict`，并已完成 FMF 外层、成员解密、TAC、22 个阶段与 PI/TI/风格字段的 D3 独立回读。D4 游戏内导入和 D5 比赛效果仍需分别验收。
## Windows 使用方法

1. 先运行 `安装依赖.bat`。
2. 将战术配方保存为普通 UTF-8 JSON 文件（扩展名 `.json`），根节点直接是 JSON 对象，不需要 `FM27GEN1:` 前缀，也不需要 Base64 编码。
3. 把 JSON 配方拖到 `运行离线生成器.bat`，或在本目录运行下面的命令。

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 FM27GEN1_Offline_FMF_Generator.py "NEW_TACTIC.json" --catalog "catalog.json" --output "NEW_TACTIC.fmf" --report "NEW_TACTIC.report.json"
```

**无需手动指定模板。** 生成器直接读取 JSON 对象中的 `base.g`，自动从 `style_template_registry.json` 选择对应原生模板。也可显式提供 `--template`，但必须与该风格登记的模板完全一致；不允许把其他风格的模板改名冒用。

旧版 `.txt` 的 `FM27GEN1:Base64` 输入仍可读取，仅用于兼容已有配方；新战术不再需要生成或提交 GEN1。输出文件已存在时，生成器拒绝覆盖。每次新战术必须使用新的输出文件名。

## 正式战术云端构建

原创战术的正式 FMF 构建使用独立工作流：`.github/workflows/fm27-tactic-build.yml`。

1. 将本次直接生成的 UTF-8 JSON 配方放入仓库根目录 `build_requests/`，例如 `build_requests/My_Original_Tactic.json`。文件根节点是完整战术 JSON 对象，不经过 GEN1 前缀/Base64 包装。
2. 每次 push 到 `main` 只提交一份待构建 JSON；一次 push 不要包含多份待构建配方。
3. GitHub Actions 自动触发 **FM27 Tactic Build**，在 Ubuntu runner 安装 Python 3.12 和生成器依赖。
4. 云端把 JSON 对象直接交给本目录正式生成器，按风格注册表选择 FMF 模板，生成全新的 `.fmf` 和同次 `.report.json`。
5. 工作流检查 D3 独立回读：FMF 容器/TAC、11 组 IP/OOP、22 个阶段、角色/职责/PI、TI 和原生风格字段。
6. 只有全部检查通过才上传 artifact：`FM27_<配方名>_run<运行号>`，包含 FMF 与 report，保留 14 天。
7. 助手取回 artifact、检查文件，再直接向用户交付附件。正式流程不再要求 GEN1 TXT。

也可在 GitHub Actions 页面手动运行 **FM27 Tactic Build**，通过 `recipe_path` 选择仓库中已有的 JSON 配方用于重试。旧版 `.txt` GEN1 仅保留兼容读取。完整触发、验收、失败处理和交付说明见 [FM27GEN1_离线原生FMF_生成流程](./FM27GEN1_离线原生FMF_生成流程.md) 与 [build_requests/README](../build_requests/README.md)。

该工作流只负责 D3 云端原生生成与独立回读，不会启动用户本机 FM27，也不声称游戏内导入或实战效果已验证。原有 `fm27-native-tactics-regression.yml` 继续只负责回归测试，不作为指定新战术的构建入口。

## 角色、职责与指令证据登记

角色、职责与指令的原生数据状态见 [FM27_Role_Duty_PI_验证登记](./FM27_Role_Duty_PI_验证登记.md)：79/79 个角色定义、7/7 个职责标志值、17/17 组 PI 菜单及 54/54 个 PI 选项、29/29 组 TI 菜单及 103/103 个 TI 选项均有原生数据证据。2026-11-18 全量映射对账后，当前生成器写入覆盖为：**PI 37/37 个非默认 Option ID、TI 75/75 个非零 native bit、TI 菜单组 29/29**。角色层保留 **73/79 个有证据的默认 duty**；另外 6 个角色现在可通过阶段对象的可选 `duty` 字段显式指定 D/S/A 或原生整数 bit，因此 **79/79 个角色均可进入生成流程**，不再需要猜测默认职责。12 项首轮新增映射（6 PI + 6 TI）已由用户确认 FM27 导入显示；本轮其余映射来自原生 catalog 编号/bit 并通过自动映射和编码测试，不能一概描述为逐项游戏导入测试通过。

## 2026-11-18 PI/TI 全量目录映射

本轮依据 `catalog.json` 的原生 Option ID 和 `native_bit`，将生成器可编码的 PI/TI 菜单选项补齐，并增加全覆盖回归测试：

- **PI：37/37** 个非默认原生 Option ID 已接入 `PI_MAP`；`encode_pi()` 继续按 1,547 个角色/位置/阶段/duty 权限策略判断是否允许写入。
- **TI：75/75** 个非零原生 bit 已接入 `TI_MAP`；`TI_GROUPS` 已覆盖 **29/29** 个原生 TI 组。
- 修正 `ATTACKING_TRANSITION=HOLD_SHAPE` 为 native bit 55；将肋部内套与外侧套上拆为两个独立原生组；新增门将参与进攻定位球组（ID 32）。
- 首轮 12 项映射已由用户确认在 FM27 导入后全部显示。其余本轮新增/补齐项目通过目录对应、编码及自动回归检查，但没有逐项向用户声称完成游戏导入验证。
- 两项“指定盯防” PI（Option ID 34/35）目前写入的是原生菜单标志；GEN1 v1 尚未承载具体盯防对象的独立目标字段。
- 仍待原生 duty 证据的角色为 `PlaymakingWinger`、`OPCoveringWideCentreBack`、`OverlappingCentreBack`、`FalseNine`、`HalfBack`、`AdvancedCentreBack`；这 6 项不阻止其他已映射角色与指令正常使用。

详细 PI/TI 清单、原生编号及编码边界见 [字段契约](FM27GEN1_离线原生FMF_字段契约.md)。

## 角色 duty 的显式指定

每个 IP/OOP 阶段对象可以可选包含 `duty`：

- `"duty":"D"` / `"DEFEND"`：防守；
- `"duty":"S"` / `"SUPPORT"`：策应；
- `"duty":"A"` / `"ATTACK"`：进攻；
- 或直接填写 `catalog.json.duties` 中的原生整数 bit。

不填写时，生成器继续使用原有 73 个角色的默认 duty。其余 6 个原生角色必须显式填写 duty；写入前检查 duty 是否属于原生集合，并依据该阶段选定的角色/位置/duty 权限 policy 校验 PI。旧配方无需修改。

## 原生验证与权限规则

- 所有十种风格均有独立原生 TAC 字符串、四字节 style code 和已登记 FM27 模板。
- 生成器检查 source-major 27、FMF 成员、11 个槽位、IP/OOP 位置、角色阶段、位置资格、职责标签及 PI 权限。
- 全部十种官方风格的默认心态和 TI 配置已纳入 `official_style_team_instruction_profiles.json`；所有配置项必须在 `TI_MAP` 中有明确映射，未知项直接拒绝。
- 真实样本含有尚未映射为可编辑选项的原生 TI 位 `34/74/75`，以及模板原有的 `33/76`。这些位作为模板所有的 opaque bits 原样保留，不允许配方伪造或自行切换。
- PI 按 phase/position/role/duty 查询 `catalog.pi_policies`；不允许的 PI、跨目录版本冲突和缺失权限策略均拒绝生成。
- 生成后独立回读 FMF/TAC，核对 style 字符串、style code、心态、TI 向量、22 个 IP/OOP 槽位、角色、职责和 PI mask。

## 审计与回归

检查十份上传的原生样本：

```powershell
py -3.12 FM27GEN1_Audit_Uploaded_Style_Samples.py
```

检查全部 90 条网站预设索引：

```powershell
py -3.12 FM27GEN1_Netlify90_OfficialPreset_Audit.py
```

运行回归测试：

```powershell
py -3.12 -m unittest discover -s tests -p "test_fm27gen1_*.py" -v
```

GitHub Actions 会自动执行样本解析、模板回读、十种风格映射、TI/PI 权限和生成器回归检查。

## 验证边界

报告状态 `offline_binary_roundtrip_verified_not_game_import_verified` 表示离线 FMF 二进制重建和回读通过。它**不等于**已经在 FM27 游戏界面导入成功，也不等于完成比赛引擎实战验证。游戏内导入与比赛效果仍需单独验证。
