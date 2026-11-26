# FM27 引擎红利四后卫｜仓库执行指令

本文件是本目录后续自动化/人工研发任务的执行入口。与 `ANALYSIS_AND_ITERATION_RULES.md` 冲突时，以该规则文件的最新强制规则为准。

## 每轮战术研发必须执行
1. 开始前重新读取 `TACTIC_INSTRUCTION_DECISION_LEDGER.md`、`VERSION_CATALOG.md`、`SOURCE_REGISTER.md`、`ITERATION_LOG.md`，并读取唯一父版本recipe、FMF及最近D5分析。禁止只依赖聊天摘要或记忆。
2. 在D0先完成父子版本全量diff和四类决策：继承保留、替换淘汰、新增待验证、证据不足。覆盖IP/OOP 11槽/22阶段、位置转换、角色、职责、所有PI、共享TI、心态、原生风格及opaque字段。
3. 有球后场必须保留DL、DCL、DCR、DR四个位置；其他结构、角色、职责、PI、TI、心态均可按证据和引擎机制优化。
4. D3完成后，把真实构建身份和D0–D3状态同步到总账、迭代日志和版本目录。D4/D5未做必须明确标记pending。
5. 用户确认D5报告版本映射后，完成数据质量审计、战术诊断和四类决策，并在同一任务中继续下一版本D0–D3；除非用户明确暂停或存在真实硬阻断。
6. 每轮必须同步更新：
   - `TACTIC_INSTRUCTION_DECISION_LEDGER.md`
   - `ITERATION_LOG.md`
   - `VERSION_CATALOG.md`
   - `SOURCE_REGISTER.md`
   - 本轮设计审计/构建报告/赛季分析（适用时）
7. 写入后逐个重新读取GitHub文件，核对版本、父版本、Run ID、FMF SHA、报告来源、四类决策和D0–D5状态。read-back失败不得声称完成。
8. 不猜测缺失数据；历史缺项标为“未定位/待补录/证据不足”。D3构建成功不等于D4游戏导入成功或D5实战有效。
9. 不使用犯规、黄牌、红牌评价战术；不把用户未确认的战术映射归因到某份赛季报告。

## 当前项目锚点
- 当前版本：V1.7 / Run163。
- 唯一结构硬约束：IP四后场DL/DCL/DCR/DR。
- V1.7父版：V1.6 / Run162；FMF SHA-256 `e67a5d218c18d3e5f7862889ab04248f8ced1f8c67a7bddb2d232b72d293748d`。
- V1.7 FMF SHA-256 `42a7038c4fe89667d0f1f7c7ff1ff74f31633f52f570d0f8b4d4d9c774ee46ab`；Run163 D3通过；D4/D5待验证。
- 当前权威状态和四类决策以 `TACTIC_INSTRUCTION_DECISION_LEDGER.md` 顶部“当前权威视图”为准。
