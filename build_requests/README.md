# FM27 战术云端构建请求目录

本目录用于提交一份**本次原创战术的 GEN1 配方**，并自动触发独立的 GitHub Actions 云端 FMF 构建。

## 提交规则

1. 每次构建只提交一个完整的 GEN1 TXT。
2. 文件名示例：`My_Original_Tactic_GEN1.txt`。
3. 文件内容必须是完整的单行 `FM27GEN1:` + Base64 编码 JSON。
4. 将文件新增或更新到本目录的直接子路径，例如 `build_requests/My_Original_Tactic_GEN1.txt`。
5. 每次 push 事件只修改/新增一份要构建的 GEN1 TXT；多份配方应分开 push。提交到 `main` 后会自动触发构建。

## 云端工作流

工作流：`.github/workflows/fm27-tactic-build.yml`

触发方式：
- 默认：向 `main` push 一份 `build_requests/*.txt`。
- 重试：在 GitHub Actions 页面手动运行 **FM27 Tactic Build**，并把 `recipe_path` 指向仓库内已有的 GEN1 TXT。

构建在 GitHub Actions 的 Ubuntu runner 中执行，使用 Python 3.12，安装生成器 requirements，然后调用：

```bash
python "04_离线原生FMF生成器/FM27GEN1_Offline_FMF_Generator.py" \
  "build_requests/My_Original_Tactic_GEN1.txt" \
  --catalog "04_离线原生FMF生成器/catalog.json" \
  --output "$RUNNER_TEMP/My_Original_Tactic.fmf" \
  --report "$RUNNER_TEMP/My_Original_Tactic.report.json"
```

随后检查本次 FMF 和 report，要求 22 个阶段设计表与回读表均完整，并且容器、TAC、位置/角色/职责/PI、TI、原生风格信息的独立回读检查全部通过。

## 输出与交付

成功后上传唯一构建 artifact：`FM27_<配方名>_run<运行号>`，包含：
- 本次新生成的原生 `.fmf`；
- 同次生成的 `.report.json`。

Artifact 保留 14 天。GEN1 源文件留在仓库 `build_requests/`，不与生成产物混淆。

助手通过 GitHub Actions 运行记录定位该 artifact，下载并检查文件后，直接向用户提供 FMF 和报告附件；不要求用户自行寻找 GitHub 下载页面。

## 失败处理

如果配方路径、GEN1 格式、角色/职责映射、TI/PI 写入映射、PI 权限或原生格式回读失败，工作流直接失败，不上传不完整 artifact。助手读取构建日志中的具体报错后，应修复设计/映射/生成器并重新构建；不得静默删去指令、替换角色或把 GEN1 当成 FMF 交付。

## 结果边界

该工作流只完成 D3：云端原生 FMF 生成与独立二进制回读。它不会启动用户本机的 FM27，也不会声称已经完成游戏内导入或比赛效果验证。
