# FM27GEN1 离线原生 FMF 战术生成器

> 统一资料入口：先阅读上级 [00_资料总索引与检索规范](../00_资料总索引与检索规范.md)。当前源码字段和映射的准确说明以同目录 [FM27GEN1_离线原生FMF_字段契约](FM27GEN1_离线原生FMF_字段契约.md) 为准。

**正式生成器：** `FM27GEN1_Offline_FMF_Generator.py`

本版本已接入用户上传的 `1.fmf`–`10.fmf` 十份 FM27 原生样本，完成十种官方风格的 TAC 身份识别、原生四字节 style code 登记、模板验证和按风格自动选模板。

## 全仓库战术使用政策（必须遵守）

本仓库所有 FMF 战术、十份原生样本、各风格模板、历史重建文件和其他战术配方，**全部非推荐战术、非成功战术，不得作为新战术开发参考**。不得复制或继承其中的阵型、角色、职责、PI、TI 或整体攻防配置，也不得把离线生成/回读成功理解为战术实战成功。

这些文件只允许在必要时用于原生 FMF 容器、字段编码、style code、二进制结构和生成器兼容性研究。技术模板作为容器基础时，不代表其战术内容被采纳；未知/opaque 数据若因格式兼容而保留，也不得视为战术建议或性能证据。新战术的战术设计必须独立完成。

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

**不得把 A9.0.2 当作成功案例、推荐战术、默认生成模板、优化起点或其他战术的设计基准。** 它没有完成完整赛季成功验证；对应报告中的 `game_interactive_import=false`、`match_engine=false` 也明确表示没有游戏内导入与比赛引擎证据。除非用户明确要求检查这份历史文件，否则生成新战术时应从用户当前目标、完整比赛数据、原生权限资料和十种原生风格证据独立设计，不能因 A9.0.2 曾被生成就复制其阵型、角色或指令。

## Windows 使用方法

1. 先运行 `安装依赖.bat`。
2. 将完整的 `FM27GEN1:...` 配方保存为 UTF-8 的 `.txt` 文件。
3. 把配方 TXT 拖到 `运行离线生成器.bat`，或在本目录运行下面的命令。

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 FM27GEN1_Offline_FMF_Generator.py "NEW_TACTIC_GEN1.txt" --catalog "catalog.json" --output "NEW_TACTIC.fmf" --report "NEW_TACTIC.report.json"
```

**无需手动指定模板。** 生成器读取配方中的 `base.g`，自动从 `style_template_registry.json` 选择对应原生模板。也可显式提供 `--template`，但必须与该风格登记的模板完全一致；不允许把其他风格的模板改名冒用。

输出文件已存在时，生成器拒绝覆盖。每次新战术必须使用新的输出文件名。

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
