# FM27 EngineDividend 4Back｜构建执行通道政策

> 本文件只约束本项目。项目规则、审计和构建辅助文件不得扩散到 FM-TA 通用工具或其他项目。

## 1. 核心原则

**项目门禁必须严格，生成执行通道必须灵活。**

- D0设计审计是进入生成流程的强制门禁；未通过不得生成。
- 通过D0后，构建执行器可以是项目标准脚本、本地Python工作区、当前会话可用的附件工作区、合规自动化runner，或离线原生生成器。
- “当前GitHub/聊天接口不能远程执行Python”只是工具接口能力描述，不是项目缺陷、战术设计缺陷、D0失败或FMF生成失败。
- 助手不得再以接口只能读取/写入仓库为由停止工作。应改用本地/附件工作区执行，或走本文件的离线原生生成路径。
- 所有通道必须执行同一项目审计、同一原生配置合法性检查和同一D3独立回读。离线通道不是审计旁路。
- 不得使用未运行项目门禁的通用Actions工作流生成正式项目战术；不得为本项目修改FM-TA通用生成器、导出器、工作流或全仓库规则。

## 2. 标准执行路径

在仓库根目录、Python 3.12环境执行：

```powershell
py -3.12 tactic_development\FM27_EngineDividend_4Back\build_project_tactic.py `
  --recipe tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json `
  --audit tactic_development\FM27_EngineDividend_4Back\<本轮审计>.md `
  --parent-fmf D:\<父版本>.fmf `
  --output tactic_development\FM27_EngineDividend_4Back\builds\<版本>.fmf `
  --report tactic_development\FM27_EngineDividend_4Back\builds\<版本>.report.json
```

标准入口按顺序运行项目验证器、原生catalog预检、FM-TA生成器。不得跳过任何失败项。

## 3. 离线原生生成路径（标准入口当前不可调用时）

离线生成路径必须在同一工作区中完成。它不依赖GitHub Actions，也不要求远程执行能力。

### 第一步：项目门禁

```powershell
py -3.12 tactic_development\FM27_EngineDividend_4Back\validate_project_iteration.py `
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
py -3.12 "04_离线原生FMF生成器\FM27GEN1_Offline_FMF_Generator.py" `
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

不得将“GitHub工具没有远程执行Python的接口”单独列为阻断。若确实没有任何可用执行环境，必须说明已完成的设计/审计阶段、实际尝试过的执行路径、精确错误和唯一需要用户协助的动作；不得要求用户重复提供已经在仓库或当前会话中存在的资料。

## 6. 项目范围

本政策及后续项目执行修订只允许写入：

`tactic_development/FM27_EngineDividend_4Back/`

不得修改FM-TA通用生成器、导出器、通用Actions工作流或其他项目目录来承载本项目政策。
