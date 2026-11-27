> **历史审计记录，已被后续用户指令取代。** 本文中关于D0机器门禁/验证器的记录仅说明当时实施情况，不代表现行规则。现行项目不设D0门禁；构建按 `GENERATION_EXECUTION_POLICY.md` 执行。

# FM27 EngineDividend 4Back｜固定战术边界与旧规则冲突审计

审查日期：2026-11-27  
审查状态：**完成**  
当前有效规则：[TACTIC_FIXED_CONSTRAINTS.md](TACTIC_FIXED_CONSTRAINTS.md)

## 1. 生效的唯一研发边界

| 项目 | 当前规则 |
|---|---|
| IP阵型 | 只允许4-2-3-1、4-3-3、4-1-2-3三种固定11槽布局 |
| IP四后场 | DL、DCL、DCR、DR各一次 |
| OOP位置映射 | 锁定V0.5原始11槽配对，不改位置结构 |
| 心态 | 锁定V0.5原生值4 |
| 固定团队指令 | 用户截图红框内15项，必须精确匹配 |
| 可调团队指令 | 剩余14项非红框TI |
| 球员配置可调项 | IP/OOP角色、职责、个人指令PI |
| TI覆盖 | 29组原生TI全部显式写入recipe |
| 其他配置字段 | 不允许添加未授权recipe字段；原生style/FourCC保持V0.5载体身份 |

### 允许的IP位置布局

- **4-2-3-1：** GK、DR、DCR、DCL、DL、MCR、MCL、AMR、AML、AMC、ST
- **4-3-3：** GK、DR、DCR、DCL、DL、MCR、MCL、AMR、AML、MC、ST
- **4-1-2-3：** GK、DR、DCR、DCL、DL、DMC、MCL、AMR、AML、MCR、ST

### 固定红框团队指令

**IP有球阶段（8项）：** 传球偏好=尽量直传；比赛节奏=极快；进攻宽度=大幅收缩；接球=多传空当；进攻启动=穿透压迫；球门球=短传；门将出球速度=平衡；门将出球=中后卫。

**OOP无球阶段（7项）：** 遭遇线=高位逼抢；后防线=大幅后撤；防守转换=重组队形；抢断=凶狠拼抢；压迫陷阱=平衡；干扰门将短传=是；传中防御=放任传中。

原生recipe映射和截图对应关系以 [TACTIC_FIXED_CONSTRAINTS.md](TACTIC_FIXED_CONSTRAINTS.md) 为准。

### 14项允许调整的非红框TI

`ATTACKING_TRANSITION`、`CREATIVE_FREEDOM`、`TIME_WASTING`、`PLAY_FOR_SET_PIECES`、`PROGRESS_THROUGH`、`SUPPORTING_RUNS`、`SUPPORTING_RUNS_SECONDARY`、`GOALKEEPER_ATTACKING_SET_PIECES`、`PATIENCE`、`DRIBBLING`、`SHOTS_FROM_DISTANCE`、`CROSSING_STYLE`、`DEFENSIVE_LINE_BEHAVIOR`、`TRIGGER_PRESS`。

## 2. 已清理的冲突旧规则

下列表述已从当前有效规则、总入口和执行流程中移除或改写：

- “除IP四后卫外，所有IP阵型/位置完全开放”；
- “OOP阵型、位置转换和位置映射完全开放”；
- “心态属于每轮可调整变量”；
- “全部TI可以自由调整”或固定红框指令可被其他TI/PI覆盖；
- “IP↔OOP位置转换是本轮可设计变量”；
- “任何新位置、额外recipe字段或自定义阶段字段均可带入生成器”。

历史版本和研究记录中的旧结构描述未被篡改；它们已明确标为历史快照，不再是当前设计要求。

## 3. 机器门禁实施

`validate_project_iteration.py` 在原有D0门禁上新增/强化以下检查：

1. `base.ip` 必须精确为三种批准阵型之一，IP 11槽位置布局必须与对应映射一致。
2. OOP 11槽位置按V0.5顺序逐槽精确匹配。
3. `ment` 必须为4。
4. 15项红框TI必须显式存在且每个值精确匹配。
5. 29组TI必须全部显式覆盖；14项可调TI与15项固定TI必须互不重叠、完整组成29组。
6. recipe根字段、base字段、槽位字段和阶段字段均有严格允许列表，拒绝额外配置字段。
7. R5.3和R6列入 `blocked_versions`，禁止旧版本重新作为当前候选。
8. D0审计还核对固定边界文档、项目规则、决策总账、PPG策略和位置绩效标准的SHA-256。
9. 全部项目构建工作流（2.6、R3/R4、R5/R5.1/R5.2/R5.3/R6、V1.6-R1/R2、通用项目入口）统一调用 `build_project_tactic.py`，由同一D0门禁先行校验；未发现可绕过项目D0的正式FMF生成工作流。

## 4. 文档与项目文件更新

| 文件 | 更新内容 |
|---|---|
| `TACTIC_FIXED_CONSTRAINTS.md` | 新增唯一固定规则、15项TI映射、14项可调TI及recipe字段白名单 |
| `PROJECT_RULES.md` / `AGENTS.md` | 替换IP/OOP开放搜索规则，明确当前允许调整范围 |
| `PPG_TARGET_POLICY.json` | 机器可读阵型、OOP、心态、固定/可调TI、候选封锁策略 |
| `validate_project_iteration.py` | D0 fail-closed硬校验 |
| `test_project_iteration_gate.py` | 增加阵型、TI、心态、位置和recipe字段越界测试 |
| `README.md` / `MASTER_UPGRADE_GUIDE.md` / `ANALYSIS_AND_ITERATION_RULES.md` / `UPGRADE_GATE.md` | 更新当前规则和升级执行流程 |
| `GENERATION_EXECUTION_POLICY.md` / `ITERATION_DESIGN_AUDIT_TEMPLATE.md` / `ROLE_PI_AUDIT_TEMPLATE.md` | 更新生成要求及审计模板 |
| `POSITION_PERFORMANCE_ELIMINATION_STANDARD.md` | 加入固定位置、红框TI和心态边界 |
| `VERSION_CATALOG.md` / `ITERATION_LOG.md` / `TACTIC_INSTRUCTION_DECISION_LEDGER.md` / `SOURCE_REGISTER.md` | 重新标记当前状态和历史候选 |
| `PROJECT_REMEDIATION_PLAN.md`、`ARCHITECTURE_REVIEW_20261126.md`及旧研究文档 | 降级为旧规则时期历史研究，不再作为当前候选指令 |

## 5. 旧候选处理

- **R5.3：** 保留公开来源结构改编和D0-D3历史技术记录，撤销当前候选资格；不进入D4/D5。
- **R6：** 旧规则下D0-D3构建成功，但IP为4-2-2-2，且OOP位置映射、心态和多项红框TI不符合新边界；撤销当前候选资格，不进入D4/D5。历史FMF SHA-256：`3eec57f892b6da99bed4e319e85b257732ea35f8546f9a79224675366649338b`。
- R5、R5.1、R5.2、R5.3、R6均在当前机器策略中列为阻止版本。
- 历史recipe、FMF、report、Run/Artifact和赛季报告均保留，不追溯改写成新规则下的测试结果。

## 6. 回归验证

**状态：通过**

- GitHub Actions： [Project Gate Regression Run 45947948722](https://github.com/eslaulau/fm-ta/actions/runs/45947948722)
- 运行结果：**28 tests passed**
- 覆盖项包括：4-2-3-1/4-3-3/4-1-2-3三种布局正向通过、其他阵型拒绝、IP四后场、OOP位置锁定、心态4、15项红框TI、29项TI显式覆盖、14项非红框TI可调整、角色/职责/PI可调整、禁止历史淘汰配置复活、禁止额外recipe字段、22阶段机器决策清单和V0.5父文件SHA。

## 7. 当前项目状态

- 当前没有符合新规则且完成D4/D5的战术候选。
- 下一轮应重新从V0.5原生FMF开始；选择一种批准IP阵型，然后只设计球员角色/职责、PI和非红框TI。
- 最终D5目标不变：完整38场至少109分（PPG≥2.85），且全队xG≥100。
- D3生成成功、D4游戏内导入、D5完整赛季表现必须分开报告，不得混为一谈。
