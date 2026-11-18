# FM27 原生战术云端构建请求目录

本目录接收**普通 UTF-8 JSON 战术配方**，并自动触发原生 FMF 构建。新战术不需要 GEN1 前缀、Base64 包装或中间 TXT。

## 提交规则

1. 每次构建只提交一个完整 JSON 配方。
2. 文件名示例：`My_Original_Tactic.json`。
3. 文件内容是完整的 JSON 对象，直接包含 `v`、`name`、`ment`、`base`、`ti`、`p` 等战术字段。
4. 将 JSON 文件放在本目录的直接子路径，例如 `build_requests/My_Original_Tactic.json`。
5. 每次 push 事件只新增/修改一份待构建 JSON；多份配方应分开 push。提交到 `main` 后会自动触发构建。

## Windows 剪贴板一键构建（无需保存配方文件）

仓库提供 `scripts/Invoke-FM27TacticBuild.ps1`。它用 GitHub `workflow_dispatch` API 将剪贴板中的完整 JSON 作为内联 `recipe_json` 提交；在 Python 构建进程里直接解析为 dict，生成后自动下载 FMF 和 report，并在本机核验 SHA-256、22 阶段回读及全部 D3 检查。配方不会写入本地 JSON 文件，也不会作为 Git commit 提交。

### 一次性配置

1. 在 GitHub 为 `eslaulau/fm-ta` 创建 fine-grained personal access token，只选此仓库，并授予 **Actions: Read and write**。GitHub 的 workflow dispatch API 对 fine-grained token 要求 Actions 写权限。
2. 在 Windows PowerShell 中运行：

```powershell
.\scripts\Invoke-FM27TacticBuild.ps1 -SetupToken
```

按提示粘贴 token。脚本通过 Windows DPAPI 将凭据加密保存到当前 Windows 用户的 `%APPDATA%`，不会写入仓库。

### 每次生成

1. 将 ChatGPT 给出的完整战术 JSON 复制到剪贴板。
2. 在仓库目录运行：

```powershell
.\scripts\Invoke-FM27TacticBuild.ps1
```

脚本会直接触发 Actions、等待本次构建、下载 artifact、核验 FMF/report，并将两个文件放入桌面的 `FM27_Builds` 文件夹。默认在本机验证完成后删除 GitHub 云端 artifact；如需保留在线 artifact，运行时加 `-KeepCloudArtifact`。

**公开仓库隐私提示：** `eslaulau/fm-ta` 当前为 public。内联配方不会进入 Git 历史或本地 JSON 文件，但会发送给 GitHub Actions；构建结果在下载前会短暂成为该仓库的 Actions artifact。脚本默认下载并删除 artifact，以缩短公开可见时间。不要通过此公开仓库发送你不愿交给 GitHub 处理的战术资料。
## 云端工作流

工作流：`.github/workflows/fm27-tactic-build.yml`

触发方式：
- **推荐：直接手动输入 JSON。** 在 GitHub Actions 页面手动运行 **FM27 Tactic Build**，只填写 `recipe_json`，粘贴完整 JSON 对象；不要填写 `recipe_path`。请求只作为 workflow output/env 单行 JSON 传递；不会写入仓库，也不会创建 runner 临时配方文件。
- **自动文件触发：** 向 `main` push 一份 `build_requests/*.json`；适合需要在仓库留档的配方。
- **API 直接对象：** 对仓库发送 `repository_dispatch`，`event_type` 使用 `fm27_tactic_build`，并在 `client_payload.recipe` 传完整 JSON 对象；不创建配方文件。
- **历史兼容：** 手动选择或 push `build_requests/*.txt` 中的 `FM27GEN1:Base64` 文件仍可用，但新战术不应再使用此格式。
- 三种输入路径共用同一个配方解析器和原生 FMF 生成器；内联对象经 `scripts/resolve_fm27_tactic_recipe.py` 作为单行 JSON workflow output 传递，再由 `scripts/build_fm27_tactic.py` 直接解析成 dict 并调用 `build_fmf_from_recipe()`，不创建输入文件。相关路径有独立单元测试。

云端生成器直接读取 JSON 对象并调用原有原生写入逻辑：

```bash
python "04_离线原生FMF生成器/FM27GEN1_Offline_FMF_Generator.py" "build_requests/My_Original_Tactic.json" --catalog "04_离线原生FMF生成器/catalog.json" --output "$RUNNER_TEMP/My_Original_Tactic.fmf" --report "$RUNNER_TEMP/My_Original_Tactic.report.json"
```

原生生成器仍执行角色/位置/duty 验证、每一条 PI 的原生权限检查、TI 编码、模板风格核对，以及 FMF/TAC 独立回读。回读报告中的 `recipe_input_format` 应为 `json`。

正式交付额外要求 **22/22 个阶段均至少填写一条 PI**。云端在原生 FMF 写入之前运行 `scripts/validate_fm27_tactic_delivery.py`，任何空 PI 阶段都会明确报出槽位/阶段并中止构建；这与生成器为通用烟雾测试保留空数组兼容不同。

## 自动验收

工作流先运行 direct-JSON 到原生 FMF 的端到端回归测试，再对本次请求检查 PI/TI 映射和 22 个阶段权限，随后实际生成本次 `.fmf` 与 `.report.json`。要求 22 个阶段设计表与回读表均完整，容器、TAC、位置/角色/职责/PI、TI、原生风格字段的独立回读检查全部通过。

### 直接 API 载荷示例

```json
{
  "event_type": "fm27_tactic_build",
  "client_payload": {
    "recipe": {
      "v": 1,
      "name": "My Original Tactic",
      "ment": 5,
      "base": { "g": "Gegenpress" },
      "ti": {},
      "p": []
    }
  }
}
```

示例中的 `p` 仅展示外层载荷形状；实际战术必须完整包含 11 个槽位与各自 `in`、`out` 阶段，不能直接用空数组生成。
## 输出与交付

成功后上传唯一构建 artifact：`FM27_<配方名>_run<运行号>`，包含：
- 本次新生成的原生 `.fmf`；
- 同次生成的 `.report.json`。

Artifact 保留 14 天。直接 JSON 源配方留在本目录；无需额外生成 GEN1 文件。助手通过 GitHub Actions 运行记录定位 artifact，下载并检查文件后，直接向用户提供 FMF 和报告附件。

## 失败处理

如果 JSON 结构、角色/职责映射、TI/PI 写入映射、PI 权限或原生格式回读失败，工作流直接失败，不上传不完整 artifact。读取构建日志中的具体错误后，应修复配方/映射/生成器并重新构建；不得静默删去指令或替换角色。

## 结果边界

该工作流只完成 D3：云端原生 FMF 生成与独立二进制回读。它不会启动用户本机的 FM27，也不会声称已经完成游戏内导入或比赛效果验证。
