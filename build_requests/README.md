# FM27 原生战术云端构建请求目录

本目录接收**普通 UTF-8 JSON 战术配方**，并自动触发原生 FMF 构建。新战术不需要 GEN1 前缀、Base64 包装或中间 TXT。

## 提交规则

1. 每次构建只提交一个完整 JSON 配方。
2. 文件名示例：`My_Original_Tactic.json`。
3. 文件内容是完整的 JSON 对象，直接包含 `v`、`name`、`ment`、`base`、`ti`、`p` 等战术字段。
4. 将 JSON 文件放在本目录的直接子路径，例如 `build_requests/My_Original_Tactic.json`。
5. 每次 push 事件只新增/修改一份待构建 JSON；多份配方应分开 push。提交到 `main` 后会自动触发构建。

## 云端工作流

工作流：`.github/workflows/fm27-tactic-build.yml`

触发方式：
- 默认：向 `main` push 一份 `build_requests/*.json`。
- 重试：在 GitHub Actions 页面手动运行 **FM27 Tactic Build**，并把 `recipe_path` 指向仓库内已有的 JSON 文件。
- 旧版兼容：仍接受 `build_requests/*.txt` 中的 `FM27GEN1:Base64` 文件，但新战术不应再使用此格式。

云端生成器直接读取 JSON 对象并调用原有原生写入逻辑：

```bash
python "04_离线原生FMF生成器/FM27GEN1_Offline_FMF_Generator.py" "build_requests/My_Original_Tactic.json" --catalog "04_离线原生FMF生成器/catalog.json" --output "$RUNNER_TEMP/My_Original_Tactic.fmf" --report "$RUNNER_TEMP/My_Original_Tactic.report.json"
```

原生生成器仍执行角色/位置/duty 验证、每一条 PI 的原生权限检查、TI 编码、模板风格核对，以及 FMF/TAC 独立回读。回读报告中的 `recipe_input_format` 应为 `json`。

## 自动验收

工作流先运行 direct-JSON 到原生 FMF 的端到端回归测试，再对本次请求检查 PI/TI 映射和 22 个阶段权限，随后实际生成本次 `.fmf` 与 `.report.json`。要求 22 个阶段设计表与回读表均完整，容器、TAC、位置/角色/职责/PI、TI、原生风格字段的独立回读检查全部通过。

## 输出与交付

成功后上传唯一构建 artifact：`FM27_<配方名>_run<运行号>`，包含：
- 本次新生成的原生 `.fmf`；
- 同次生成的 `.report.json`。

Artifact 保留 14 天。直接 JSON 源配方留在本目录；无需额外生成 GEN1 文件。助手通过 GitHub Actions 运行记录定位 artifact，下载并检查文件后，直接向用户提供 FMF 和报告附件。

## 失败处理

如果 JSON 结构、角色/职责映射、TI/PI 写入映射、PI 权限或原生格式回读失败，工作流直接失败，不上传不完整 artifact。读取构建日志中的具体错误后，应修复配方/映射/生成器并重新构建；不得静默删去指令或替换角色。

## 结果边界

该工作流只完成 D3：云端原生 FMF 生成与独立二进制回读。它不会启动用户本机的 FM27，也不会声称已经完成游戏内导入或比赛效果验证。
