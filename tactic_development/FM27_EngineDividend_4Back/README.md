# FM27 引擎红利四后卫｜项目入口

<badge>当前研发版本：N1</badge>

本项目目标：研发利用FM27比赛引擎机制的有球四后卫战术。最终赛季目标为38场至少109分（PPG≥2.85）且全队xG≥100；尚未达标前不得宣称成功。

## 现行规则（只认这四份）
1. [PROJECT_RULES.md](PROJECT_RULES.md)：项目目标、证据纪律、冲突优先级。
2. [TACTIC_FIXED_CONSTRAINTS.md](TACTIC_FIXED_CONSTRAINTS.md)：IP阵型、OOP位置、心态、红框TI及允许调整项。
3. [UPGRADE_GATE.md](UPGRADE_GATE.md)：赛季分析至下一版设计的研发流程。
4. [GENERATION_EXECUTION_POLICY.md](GENERATION_EXECUTION_POLICY.md)：原生预检、FMF生成、独立回读与交付。

AI执行入口：[AGENTS.md](AGENTS.md)。

## 当前战术
- **N1｜窄幅纵向分层 4-1-2-3**： [配方](N1.json) · [设计记录](N1_DESIGN_AND_AUDIT.md) · [构建报告](builds/N1.report.json) · [FMF](builds/N1.fmf)。
- D1-D3已通过；D4游戏内导入、D5完整赛季效果待验证。
- [构建记录](https://github.com/eslaulau/fm-ta/actions/runs/45952680145)。

## 唯一历史依据
- [TACTIC_INSTRUCTION_DECISION_LEDGER.md](TACTIC_INSTRUCTION_DECISION_LEDGER.md)：历史配置、版本差异、证据与四类决策总账。
- [VERSION_CATALOG.md](VERSION_CATALOG.md)：历史版本、FMF、构建报告和赛季复盘索引。
- [ITERATION_LOG.md](ITERATION_LOG.md)：历史研发事件记录。

## 历史资料保留原则
所有历史recipe、FMF、构建报告、赛季报告和设计审计均作为历史证据保留。旧文件中的D0审批、旧阵型范围、旧OOP方案、旧TI可调范围、V0.5强制重生或外部战术研究指令，均不再是现行规则。历史文件不得覆盖现行规则。

## 当前固定边界摘要
- IP仅允许4-2-3-1、4-3-3、4-1-2-3。
- OOP固定11个位置映射，心态固定4。
- 15项红框TI固定；只允许调整角色/职责、PI和14项非红框TI。
- 不使用外部战术资料；不强制从V0.5重新开始。
- 不设D0项目审批门禁。
