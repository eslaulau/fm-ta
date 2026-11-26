# FM27 EngineDividend 4Back｜正式项目研发规则

> **最高目标：PPG ≥ 2.85。** 本文件是本项目规则入口；机器可读参数见 [PPG_TARGET_POLICY.json](PPG_TARGET_POLICY.json)。规则只约束本项目目录内的研发，不改变 FM-TA 通用工具。

## 1. 唯一最高目标与评价方式

本项目的唯一最高研发目标是：在用户管理球队的联赛赛季中达到 **PPG ≥ 2.85**。

`PPG = 联赛总积分 ÷ 已完成联赛场次`

- 38 场联赛至少需要 109 分才能达到 2.85 PPG。
- 目标是研发方向，不是对任何单次赛季结果的保证。
- 每轮优先判断是否提高稳定赢球和积分能力；进攻、防守、机会质量、主客场表现用于解释 PPG 的来源、代价和可持续性。
- 不把某个历史版本的 xGA、进球数、阵型或角色组合设为高于 PPG 的独立终点。
- 不允许为降低 xGA 而无条件牺牲胜率，也不允许以短期高转化掩盖机会控制崩溃。

## 2. 项目硬约束与开放搜索空间

- IP 有球阶段必须且只能包含四个后场位置槽：`DL`、`DCL`、`DCR`、`DR`，每个恰好一次。
- IP 其余七个位置、IP 阵型数字形态、角色、职责、PI、TI、心态均开放。
- OOP 无球阶段阵型、人数、角色、职责、PI、TI、心态及 IP↔OOP 转换均开放；不得误写成 OOP 必须四后卫。
- 每轮只形成一套主线完整战术。可以保留已有独立探索分支，但不得把多套候选交给用户代替研发决策。
- 阵型改变不是禁区；但必须说明它针对什么问题、依据哪些本队/外部证据、预期改善什么 PPG 相关环节、有什么风险，以及如何验证。
- V0.5 是历史起点，不是必须复制的阵型模板；V1.3、V1.6、V1.7、V1.8、R1、R2均是证据来源，不自动成为下一版模板。

## 3. 每轮强制决策流程

必须按顺序完成，不能先生成后补理由：

1. **历史回溯：** 读取最新唯一权威总账、当前父版本、父 FMF SHA-256、recipe、最近 D5 报告和版本目录；从 V0.5 回看全部重要正反证据。
2. **PPG 问题诊断：** 分析胜平负、积分/PPG、进失球、xG/NPxG、xGA、双方绝佳机会、主客场、平局和失利；区分机会创造、机会控制、结果转化和执行因素。
3. **问题优先级：** 选择最可能限制 PPG 的主问题；不得仅因某项指标变化就自动修改战术。
4. **机制与结构研究：** 比较继续现有结构、局部重构和整体重构；结构改变必须有明确证据链。外部 META 只能产生假设，不能替代本队赛季验证。
5. **四类决策：** 每轮必须完整列出：
   - 继承保留
   - 替换淘汰
   - 新增待验证
   - 证据不足
6. **唯一方案设计：** 每项主改动写明“问题 → 机制 → 配置 → 对 PPG 的预期路径 → 风险/失败条件 → D5 指标”。
7. **生成前审计：** 核对 IP 四后场、11 槽/22 阶段、完整角色职责/PI/TI/心态、父版身份与 SHA、历史冲突和四类决策。
8. **构建与独立回读：** 通过项目专属入口后，才调用 FM-TA 原生预检和 FMF 生成能力。
9. **归档与复核：** 更新唯一总账、迭代日志、版本目录、来源登记及本轮审计；提交后 read-back。
10. **实战状态：** D3 只表示离线构建/回读；D4 是游戏内导入；D5 是用户确认版本映射后的赛季报告。三者不得混淆。

## 4. 四类决策和证据等级

每项配置必须归入且仅归入以下一类：

| 类别 | 规则 |
|---|---|
| 继承保留 | 说明继承原因和证据等级；结构性暂留不等于单项已验证 |
| 替换淘汰 | 记录旧值→新值/移除、原因及适用范围；不夸大为所有情境无效 |
| 新增待验证 | 写明假设、预期收益、副作用、失败条件和 D5 指标 |
| 证据不足 | 明确未知内容、缺失数据及是否暂不采用；不得默认为有效 |

证据至少区分：报告直接观察、统计关联、当前 build 外部研究/原生机制、设计假设。多项同时改动只允许先归因到组合层，不得虚构单项因果。

## 5. PPG 导向的分析纪律

- 第一评价指标是联赛 PPG；同时报告总积分、胜/平/负和胜率，避免单看积分总量。
- 进攻评估必须区分 xG/NPxG、绝佳机会、实际进球与转化差额。
- 防守评估必须区分 xGA/对手绝佳机会与实际失球；不能把失球高于 xGA 直接归因于阵型。
- 必须分析主客场差异，以及平局/失利中的机会质量和结果转化。
- 以用户确认的实际战术版本映射为准，不推测每场使用的 tactic。
- 不同存档/随机种子不构成受控 A/B；样本、数据覆盖和解析限制必须明确。
- 犯规、黄牌、红牌不得作为战术质量指标。
- PPG 未达目标时，按诊断结果选择下一轮方向；不允许机械地只改防守或只改进攻。

## 6. 生成前必须通过的项目审计

项目审计至少检查：

- 项目策略文件存在，目标明确为 PPG ≥ 2.85。
- 唯一权威总账已写入 PPG 2.85 目标。
- 本轮设计审计明确写出 PPG 2.85、父版本及 64 位父 FMF SHA-256。
- 四类决策全部出现。
- 写明下一轮 D5 可量化验证指标。
- recipe 含 11 个槽位，每槽均含 IP/OOP 阶段对象。
- IP 位置集合中 DL、DCL、DCR、DR 各恰好出现一次。
- 通过后再调用 FM-TA 原有 catalog-backed preflight；该工具负责原生角色/职责/PI权限等通用技术检查。
- 任一项目审计失败，禁止继续调用生成器。

审计通过不等于战术效果通过；它只说明设计与项目硬规则完整，随后仍需 D1–D3 技术验证、D4 游戏内确认和 D5 赛季验证。

## 7. 工具边界：FM-TA 只是工具

- 本项目规则、PPG 目标、历史台账、生成前审计及项目专属构建入口全部位于 `tactic_development/FM27_EngineDividend_4Back/`。
- FM-TA 通用导出器/生成器只负责读取合法 recipe、原生权限预检、FMF 格式生成和回读；它不决定本项目战术目标、阵型、角色或迭代方向。
- 不修改 FM-TA 通用生成器、导出器、通用工作流或全仓库规则来承载本项目要求。
- 本项目每次正式迭代必须通过 [build_project_tactic.py](build_project_tactic.py)；它强制执行 [validate_project_iteration.py](validate_project_iteration.py)，并要求提供真实父 FMF 文件，核对父 FMF、当前项目规则、决策总账、PPG 策略和本轮 recipe 的 SHA-256；规则或总账更新后，旧审计自动失效。配方与审计文件必须位于本项目目录，构建输出也归档在本项目目录。禁止把直接调用通用 FM-TA 命令视为完成项目迭代。每轮设计审计从 [ITERATION_DESIGN_AUDIT_TEMPLATE.md](ITERATION_DESIGN_AUDIT_TEMPLATE.md) 创建。
- 其他项目使用 FM-TA 时不继承本项目 PPG 目标或规则。

## 8. 权威文件与冲突处理

- 本文件：项目最高规则。
- [PPG_TARGET_POLICY.json](PPG_TARGET_POLICY.json)：本规则的机器可读目标/约束。
- [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)：唯一权威跨版本配置决策与历史总账。
- [UPGRADE_GATE.md](UPGRADE_GATE.md)：每轮研发执行流程。
- [ANALYSIS_AND_ITERATION_RULES.md](ANALYSIS_AND_ITERATION_RULES.md)：战术分析与迭代方法。
- [build_project_tactic.py](build_project_tactic.py)：项目生成入口；调用项目审计后再调用 FM-TA 通用技术工具。
- 如旧文档中的目标或表述与本文件冲突，以本文件为准；历史数据记录保持原样，不追溯改写为新目标下的历史结果。

## 9. 项目专属构建命令

在仓库根目录运行（PowerShell / Python 3.12）。先把父版本 FMF 的真实路径填入 `--parent-fmf`：

```powershell
py -3.12 tactic_development\FM27_EngineDividend_4Back\build_project_tactic.py `
  --recipe tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json `
  --audit tactic_development\FM27_EngineDividend_4Back\<本轮设计审计>.md `
  --parent-fmf D:\<父版本>.fmf `
  --output tactic_development\FM27_EngineDividend_4Back\builds\<本轮版本>.fmf `
  --report tactic_development\FM27_EngineDividend_4Back\builds\<本轮版本>.report.json
```

设计审计中的父 FMF、recipe、项目规则、决策总账和 PPG 策略 SHA-256 必须与当前实际文件一致。每次规则或总账变更后都要重新制作审计。可用 `Get-FileHash -Algorithm SHA256` 分别读取这些文件的哈希，再填写审计文件：

```powershell
Get-FileHash 'D:\<父版本>.fmf' -Algorithm SHA256
Get-FileHash .\tactic_development\FM27_EngineDividend_4Back\<本轮配方>.json -Algorithm SHA256
```

执行顺序固定为：校验父 FMF 与配方 SHA-256 → 项目 PPG/历史规则审计 → FM-TA 通用 catalog 权限预检 → FM-TA 原生 FMF 生成。项目审计失败即退出，不调用后两步；配方、审计和输出必须在项目目录内，输出已存在时拒绝覆盖。

运行项目门禁回归测试：

```powershell
py -3.12 -m unittest discover -s tactic_development\FM27_EngineDividend_4Back -p test_project_iteration_gate.py
```

项目专属入口是本项目正式迭代的唯一有效构建流程。直接调用 FM-TA 通用生成器即使成功生成 FMF，也不构成本项目完成一次合规迭代。
