# FM27 EngineDividend 4Back｜构建执行通道政策

> 本文件只约束本项目。项目规则、审计和构建辅助文件不得扩散到 FM-TA 通用工具或其他项目。

## 1. 核心原则

**项目门禁必须严格，生成执行通道必须灵活。**

- D0设计审计是进入生成流程的强制门禁；未通过不得生成。
- 通过D0后，构建执行器可以是项目标准脚本、本地Python工作区、当前会话可用的附件工作区、合规自动化runner，或离线原生生成器。
- “当前GitHub/聊天接口不能远程执行Python”只是工具接口能力描述，不是项目缺陷、战术设计缺陷、D0失败或FMF生成失败。
- 助手不得再以接口只能读取/写入仓库为由停止工作。应改用本地/附件工作区执行，或走本文件的离线原生生成路径。
- 所有通道必须执行同一项目审计、同一原生配置合法性检查和同一D3独立回读。离线通道不是审计旁路。
- 任何执行通道（包括GitHub Actions）都不得跳过D0项目门禁、原生权限预检、D3独立回读和产物归档。允许创建或修改项目专用工作流来执行这些门禁；不得为此修改FM-TA通用生成器、导出器或其他项目目录。

## 2. 标准执行路径

在任意满足项目依赖的Python环境执行；不限定必须是本地Python 3.12。可使用本地/附件工作区、GitHub Actions或其他合规自动化runner。

```powershell
py tactic_development\FM27_EngineDividend_4Back\build_project_tactic.py `
  --recipe tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json `
  --audit tactic_development\FM27_EngineDividend_4Back\<本轮审计>.md `
  --parent-fmf D:\V0.5.fmf `
  --output tactic_development\FM27_EngineDividend_4Back\builds\<版本>.fmf `
  --report tactic_development\FM27_EngineDividend_4Back\builds\<版本>.report.json
```

标准入口按顺序运行项目验证器、原生catalog预检、FM-TA生成器。不得跳过任何失败项。

## 3. 备用原生生成路径（项目标准入口当前不可调用时）

备用生成路径可在任意具备项目文件和依赖的执行环境中完成，包括本地/附件工作区或GitHub Actions runner。

### 第一步：项目门禁

```powershell
py tactic_development\FM27_EngineDividend_4Back\validate_project_iteration.py `
  --recipe tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json `
  --audit tactic_development\FM27_EngineDividend_4Back\<本轮审计>.md `
  --parent-fmf D:\<父版本>.fmf
```

必须看到 `PASS`。若失败，修正项目审计或配方后重新计算SHA-256并重做审计；不得继续生成。

### 第二步：原生权限预检（如果仓库内脚本可用）

```powershell
py -3.12 scripts\preflight_fm27_tactic.py `
  --recipe tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json `
  --catalog "04_离线原生FMF生成器\catalog.json" `
  --style-registry "04_离线原生FMF生成器\style_template_registry.json"
```

如果当前运行包没有该预检脚本，不得因此停止；下一步离线原生生成器仍会执行其原生角色、职责、位置和PI权限检查。若预检脚本存在且报告失败，则必须先修复失败项。

### 第三步：离线原生FMF生成

```powershell
py "04_离线原生FMF生成器\FM27GEN1_Offline_FMF_Generator.py" `
  "tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json" `
  --catalog "04_离线原生FMF生成器\catalog.json" `
  --style-registry "04_离线原生FMF生成器\style_template_registry.json" `
  --output "tactic_development\FM27_EngineDividend_4Back\builds\<版本>.fmf" `
  --report "tactic_development\FM27_EngineDividend_4Back\builds\<版本>.report.json"
```

生成器必须成功完成原生FMF构建及二进制独立回读。若报告具体指出角色/职责/PI权限或字段编码错误，应修正设计/映射后重跑完整门禁；不得静默删除设计指令或把未写入的配置宣称为已生成。

## 4. D3验收与交付

D3通过必须同时具备：

1. 本轮项目审计验证结果为PASS；
2. 原生权限预检通过，或离线生成器完成等价原生权限检查；
3. 实际生成的FMF文件；
4. 同次生成的JSON report；
5. report确认FMF容器、TAC、11个位置槽、22个IP/OOP阶段、角色/职责/PI/TI和原生风格字段回读；
6. FMF与report的文件大小及SHA-256；
7. 文件与报告均归档在本项目目录，且不覆盖任何历史产物。

D3不等于D4游戏内导入，也不等于D5赛季表现。没有实际FMF和同次report，不得宣称构建成功。

## 5. 何时允许报告阻断

只有以下真实问题可构成阻断：

- 父版本FMF、recipe、项目审计或原生catalog/模板等生成必需输入确实缺失；
- 项目门禁失败且尚未修复；
- 原生生成器对所选配置给出可复现的权限/格式错误；
- 所有当前可用执行环境均无法启动或执行，并且已明确尝试路径及具体错误。

不得将某一种执行接口不可用单独列为阻断。若确实没有任何可用执行环境，必须说明已完成的设计/审计阶段、实际尝试过的执行路径、精确错误和唯一需要用户协助的动作；不得要求用户重复提供已经在仓库或当前会话中存在的资料。

## 6. 项目范围

本政策及后续项目执行修订只允许写入：

`tactic_development/FM27_EngineDividend_4Back/`

不得修改FM-TA通用生成器、导出器或其他项目目录来承载本项目政策。允许维护本项目目录内的专用Actions工作流与自动化配置。


## 每轮先恢复 V0.5 原始 FMF

仓库已归档完整 `V0.5_NATIVE_SNAPSHOT.json`，其中嵌入原始 FMF 字节。每轮构建前运行：

```powershell
py -3.12 tactic_development\\FM27_EngineDividend_4Back\\materialize_v05_baseline.py
```

默认输出 `tactic_development/FM27_EngineDividend_4Back/builds/V0.5.fmf`；脚本会验证 4,214 bytes 和固定 SHA-256，拒绝覆盖已有文件。构建入口的 `--parent-fmf` 必须指向该文件。

## 重生基准强制说明

无论标准入口还是离线原生生成器，本轮传入的父 FMF 都必须是 V0.5 原始文件，SHA-256 固定为 `e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257`。任何 V1.x 文件不得作为 `--parent-fmf`。离线执行不得绕过 `validate_project_iteration.py` 的 V0.5 哈希检查。
