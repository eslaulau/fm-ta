# FM27 原生战术云端构建请求目录

本目录接收**普通 UTF-8 JSON 战术配方**，并自动触发原生 FMF 构建。新战术不需要 GEN1 前缀、Base64 包装或中间 TXT。

## 对话内直接交付（正式默认流程）

用户只需在 ChatGPT 对话中提出战术目标与限制。战术确定后，助手直接通过 GitHub 仓库写入权限，在本目录创建唯一一份完整 JSON 请求文件；该次 `main` 分支 push 自动触发 `FM27 Tactic Build`。助手随后读取本次 Actions 运行结果、下载 artifact、核验 `.fmf` 与同次 `.report.json`，并在对话中直接交付文件。

**用户不需要**打开 GitHub Actions 页面、复制粘贴 JSON、操作桌面、运行 PowerShell、创建本地文件或手动下载 artifact。输入文件由助手直接写进仓库；生成、回读和 artifact 都在 GitHub Actions 中完成。

**仓库可见性：** 当前 `eslaulau/fm-ta` 是公开仓库，因此 `build_requests/*.json` 和 Git 提交历史对公众可见。战术配方不应包含密码、token 或其他秘密内容；如战术本身需要保密，须先将项目改为私有仓库，不能把公开仓库说成私密通道。
## 提交规则

1. 每次构建只提交一个完整 JSON 配方。
2. 文件名示例：`My_Original_Tactic.json`。
3. 文件内容是完整的 JSON 对象，直接包含 `v`、`name`、`ment`、`base`、`ti`、`p` 等战术字段。
4. 将 JSON 文件放在本目录的直接子路径，例如 `build_requests/My_Original_Tactic.json`。
5. 每次 push 事件只新增/修改一份待构建 JSON；多份配方应分开 push。提交到 `main` 后会自动触发构建。

## 快速构建路径（2026-11 更新）

- **Catalog 指纹缓存：** 助手端以 `catalog.json` 的 Git blob SHA / 内容指纹作为缓存键。指纹未变化时复用已读取的角色、职责、位置资格与 PI 权限索引；指纹变化时才重新读取。catalog 始终以仓库当前版本为准，不使用过期缓存做构建验收。
- **PI 预检前移：** `scripts/preflight_fm27_tactic.py` 在正式构建前检查 11 个槽位的 22 个阶段，包括原生位置归一化、角色阶段与位置资格、duty、每条已选择 PI 的 catalog 权限、TI 编码映射和原生风格登记。每阶段必须有 PI 数组，但空数组合法；预检失败不启动 FMF 生成。
- **依赖缓存：** Actions 使用 `setup-python` 的 pip cache，缓存键由 `requirements.txt` 决定；依赖未变化时跳过重复下载。
- **直接 API 触发：** 工作流保留 `repository_dispatch` 的 `fm27_tactic_build` 事件，配方作为 `client_payload.recipe` 直接传入，不创建配方文件、不产生配方 Git commit。调用方需有仓库 `contents:write` 权限。当前对话连接提供 GitHub GET/文件写入操作，但不提供任意 POST dispatch 操作；因此本次已完成工作流接收端和预检接入，不能声称已从本对话直接 POST 触发。可用的文件提交 push 路径仍作为自动构建后备方案。

## 云端工作流

工作流：`.github/workflows/fm27-tactic-build.yml`

触发方式：
- **正式对话交付：** 助手直接创建/提交 `build_requests/*.json`；push 到 `main` 后自动运行，并由助手下载、核验和交付 FMF/report。无需用户操作 GitHub 页面或本地电脑。
- **手动调试：** 在 GitHub Actions 页面手动运行 **FM27 Tactic Build**，只填写 `recipe_json`，不填写 `recipe_path`；用于仓库维护者独立测试，不是用户的日常交付步骤。
- **外部自动化：** `repository_dispatch` 的 `event_type` 为 `fm27_tactic_build`，完整对象放入 `client_payload.recipe`；适合具备 dispatch 写权限的外部调用方。
- **历史兼容：** 手动选择或 push `build_requests/*.txt` 中的 `FM27GEN1:Base64` 文件仍可用，但新战术不应再使用此格式。
- 三种输入路径共用同一个配方解析器和原生 FMF 生成器；内联对象经 `scripts/resolve_fm27_tactic_recipe.py` 作为单行 JSON workflow output 传递，再由 `scripts/build_fm27_tactic.py` 直接解析成 dict 并调用 `build_fmf_from_recipe()`，不创建输入文件。相关路径有独立单元测试。

云端生成器直接读取 JSON 对象并调用原有原生写入逻辑：

```bash
python "04_离线原生FMF生成器/FM27GEN1_Offline_FMF_Generator.py" "build_requests/My_Original_Tactic.json" --catalog "04_离线原生FMF生成器/catalog.json" --output "$RUNNER_TEMP/My_Original_Tactic.fmf" --report "$RUNNER_TEMP/My_Original_Tactic.report.json"
```

原生生成器仍执行角色/位置/duty 验证、每一条 PI 的原生权限检查、TI 编码、模板风格核对，以及 FMF/TAC 独立回读。回读报告中的 `recipe_input_format` 应为 `json`。

`scripts/validate_fm27_tactic_delivery.py` 只检查配方结构、11 个槽位、22 个阶段对象及必需字段。每阶段的 PI 字段必须存在且为数组，但 [] 合法；是否需要额外个人指令由战术设计决定，不得为了通过校验而填充。所选 PI 的具体原生权限由 catalog 预检和生成器逐条验证。

## 自动验收

工作流先运行 direct-JSON 与实验映射回归测试，再运行 catalog-backed preflight：对 22 个阶段逐项检查角色/位置/duty、PI 权限、TI 映射和风格登记；全部通过后才实际生成本次 `.fmf` 与 `.report.json`。要求 22 个阶段设计表与回读表均完整，容器、TAC、位置/角色/职责/PI、TI、原生风格字段的独立回读检查全部通过。

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

该工作流完成 D3：云端原生 FMF 生成、独立二进制回读、SHA-256/长度核验和 artifact 上传。D3 是生成器的技术输出门槛，不声明游戏内导入或比赛效果；持续研发项目可在 D4/D5 继续验证。

## 历史战术迁移兼容通道（仅限用户明确授权）

`build_requests/legacy_migrations/*.json` 使用独立工作流 `.github/workflows/fm27-legacy-migration-build.yml`。该通道只用于将用户明确要求复刻的旧版战术转换为当前原生 FMF，不作为新战术创作入口。

与普通正式交付的区别：
- 历史战术原有的空 PI 阶段必须原样保留；所有合法配方都允许空 PI 数组，不存在普通交付的非空 PI 门槛。
- 角色/位置/duty 兼容性、PI 原生权限、TI 编码、FMF 容器完整性和全部 D3 独立回读仍必须通过。
- D3 只证明原生文件生成和二进制回读，不代表游戏内导入或比赛效果已验证。
- 历史战术迁移必须有用户明确授权；不得将其结果自动作为新战术设计模板或成功战术证据。
