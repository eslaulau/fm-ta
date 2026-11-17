# 04｜离线原生 FMF 生成器

**本目录是原生 FMF 的唯一正式输出工具。** GEN1 TXT 只是输入配方；正常的战术生成任务必须实际运行本目录的 Python 生成器，生成新 .fmf 和对应的 .report.json。

## 当前源码与运行文件

- `FM27GEN1_Offline_FMF_Generator.py`：唯一离线二进制生成器源码。
- `requirements.txt`、`安装依赖.bat`、`运行离线生成器.bat`：运行环境与 Windows 入口。
- `catalog.json`：目录数据。
- `FM27_4231_Gegenpress_Template.fmf`：BAT 默认原生模板。
- `123_Game_Export_Reference.fmf`：原生导出参考样本。
- `FM27_A9.0.2_GEN1.txt`、`FM27_A9.0.2_Offline_Rebuild.fmf`、`FM27_A9.0.2_Offline_Rebuild.report.json`：回归样本和报告。
- [详细生成流程](FM27GEN1_离线原生FMF_生成流程.md)
- [字段契约](FM27GEN1_离线原生FMF_字段契约.md)

## 新战术标准命令（正式生产）

在本目录运行，使用本次新生成的 GEN1 TXT 和独立输出文件名：

```powershell
py -3.12 -m pip install -r requirements.txt

py -3.12 FM27GEN1_Offline_FMF_Generator.py "NEW_TACTIC_GEN1.txt" --template "FM27_4231_Gegenpress_Template.fmf" --catalog "catalog.json" --output "NEW_TACTIC.fmf" --report "NEW_TACTIC.report.json"
```

只有命令成功、FMF 文件存在且非空、对应报告存在且回读通过，才算完成 D3。输出路径已存在时生成器拒绝覆盖，必须使用新的输出名，不得跳过本次实际生成。

## 回归样本命令（仅用于生成器测试）

以下命令重建 A9.0.2 历史样本，只用于回归测试，不是新战术生产命令：

```powershell
py -3.12 FM27GEN1_Offline_FMF_Generator.py "FM27_A9.0.2_GEN1.txt" --template "FM27_4231_Gegenpress_Template.fmf" --catalog "catalog.json" --output "FM27_A9.0.2_Offline_Rebuild_Test.fmf" --report "FM27_A9.0.2_Offline_Rebuild_Test.report.json"
```

也可运行 `安装依赖.bat` 后，将本次 GEN1 TXT 拖入 `运行离线生成器.bat`。不拖入文件双击 BAT 时使用的是内置 A9.0.2 回归配方，不代表当前新战术已生成。

## D3 输出与交付

每次成功的新战术生成至少应有两个本次新文件：

1. 战术名称.fmf：原生 FM27 战术文件。
2. 战术名称.report.json：同一次生成产生的独立回读报告。

GEN1 TXT 是可选的审计/复现源文件，可以一并交付，但绝不能代替上面两个输出。报告状态 offline_binary_roundtrip_verified_not_game_import_verified 只代表离线回读，不代表 D4 游戏内验收。

## 当前实现边界

- GEN1 v1、11 槽位、IP/OOP 两阶段；当前只支持 Gegenpress。
- 模板必须包含 `.tac/.aom/.img` 且 source-major 为 27。
- 角色检查包括 catalog role、phase 和 role/position eligibility。
- PI/TI 仅支持源码白名单；未知值失败。
- duty 使用硬编码 `ROLE_DUTY`，不是 GEN1 的独立字段。
- OOP STC 写入时规范化为 native ST。
- 当前未调用完整 `pi_policies` 或第 02 层 PI 权限 CSV 逐项验证 PI 可编辑/固定状态。
- TI 为单一共享的 12 字节向量，以模板为基线；GEN1 未提供的 key 保留模板值。不能当作独立 IP/OOP 两套团队指令。

## A9.0.2 样本证据

随附报告记录输出大小 3,588 bytes，SHA256：

`c2ac1719f202d00b1a058e44da0c241e0f72b10bcdc3a04c89b295ed73029d10`

报告记录 FMF/TAC 独立回读、11 对 IP/OOP、22 阶段位置/角色/PI mask 和 TI 向量通过。用户已确认该样本在 FM27 内成功载入阵型；这不代表全部 PI/TI、其他模板或比赛效果已验收。

后续开发必须直接基于本目录这份源码，不另建重复生成器，不引入网站/API/游戏平台依赖。
