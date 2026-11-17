# FM27 全位置角色权限目录 v2

## 完整性结论

- 原始权限提取：24 个原生角色菜单位置；IP 40 个不同角色 ID，OOP 39 个不同角色 ID，共 79 个阶段角色 ID。
- 原始权限提取共有 1,547 行：每个角色/位置/阶段组合记录 7 个原生 duty 状态。
- 本版增加 `STC → ST` 中锋中央槽位别名，共复制 70 条中央中锋权限记录（IP 42、OOP 28）；扩展权限表共 1,617 行。
- `SW` 与 `DM` 不在本次提取到的原生角色菜单位置表中；不为其伪造角色权限。

## 关键修正：STC

当前配方（A4.x GEN1）使用 `STC` 表示中央中锋槽位；原生角色权限提取使用 `ST` 作为中央中锋角色菜单上下文。权限表中 `ST` 已包含：
- IP：`CentreForward`, `ChannelForward`, `DeepLyingForward`, `FalseNine`, `Poacher`, `TargetForward`
- OOP：`OPCentralOutletCentreForward`, `OPCentreForward`, `OPSplittingOutletCentreForward`, `OPTrackingCentreForward`

因此，`Central Outlet Centre-Forward` 不应再被判定为“游戏没有这个角色”或“中央中锋不能用”。正确处理是：先把配方位置 `STC` 规范化到权限查询上下文 `ST`，再查角色 ID。**这修正的是静态权限查询映射；最终 FMF 仍须按游戏原生位置 selector 写入。**

## 原生角色菜单位置覆盖

### GK — 门将
- IP（3）：清道夫式解围门将 (`NoNonsenseGoalkeeper`)；出球门将 (`BallPlayingGoalkeeper`)；门将 (`Goalkeeper`)
- OOP（3）：门将 (`OPGoalkeeper`)；门线门将 (`OPLineKeeper`)；清道夫门将 (`OPSweeperKeeper`)

### DR — 右后卫
- IP（5）：组织型翼卫 (`PlaymakingWingBack`)；内收边后卫 (`InsideFullBack`)；内收翼卫 (`InsideWingBack`)；翼卫 (`WingBack`)；边后卫 (`FullBack`)
- OOP（3）：留守边后卫 (`OPHoldingFullBack`)；逼抢边后卫 (`OPPressingFullBack`)；边后卫 (`OPFullBack`)

### DL — 左后卫
- IP（5）：组织型翼卫 (`PlaymakingWingBack`)；内收边后卫 (`InsideFullBack`)；内收翼卫 (`InsideWingBack`)；翼卫 (`WingBack`)；边后卫 (`FullBack`)
- OOP（3）：留守边后卫 (`OPHoldingFullBack`)；逼抢边后卫 (`OPPressingFullBack`)；边后卫 (`OPFullBack`)

### DC — 中后卫（中）
- IP（6）：解围中卫 (`NoNonsenseCentreBack`)；套上中卫 (`OverlappingCentreBack`)；边中卫 (`WideCentreBack`)；出球中卫 (`BallPlayingCentreBack`)；中后卫 (`CentreBack`)；前压中卫 (`AdvancedCentreBack`)
- OOP（6）：边中卫 (`OPWideCentreBack`)；补位中卫 (`OPCoveringCentreBack`)；补位边中卫 (`OPCoveringWideCentreBack`)；上抢边中卫 (`OPStoppingWideCentreBack`)；中后卫 (`OPCentreBack`)；上抢中卫 (`OPStoppingCentreBack`)

### DCR — 右中卫
- IP（6）：解围中卫 (`NoNonsenseCentreBack`)；套上中卫 (`OverlappingCentreBack`)；边中卫 (`WideCentreBack`)；出球中卫 (`BallPlayingCentreBack`)；中后卫 (`CentreBack`)；前压中卫 (`AdvancedCentreBack`)
- OOP（6）：边中卫 (`OPWideCentreBack`)；补位中卫 (`OPCoveringCentreBack`)；补位边中卫 (`OPCoveringWideCentreBack`)；上抢边中卫 (`OPStoppingWideCentreBack`)；中后卫 (`OPCentreBack`)；上抢中卫 (`OPStoppingCentreBack`)

### DCL — 左中卫
- IP（6）：解围中卫 (`NoNonsenseCentreBack`)；套上中卫 (`OverlappingCentreBack`)；边中卫 (`WideCentreBack`)；出球中卫 (`BallPlayingCentreBack`)；中后卫 (`CentreBack`)；前压中卫 (`AdvancedCentreBack`)
- OOP（6）：边中卫 (`OPWideCentreBack`)；补位中卫 (`OPCoveringCentreBack`)；补位边中卫 (`OPCoveringWideCentreBack`)；上抢边中卫 (`OPStoppingWideCentreBack`)；中后卫 (`OPCentreBack`)；上抢中卫 (`OPStoppingCentreBack`)

### WBR — 右翼卫
- IP（4）：进攻型翼卫 (`AdvancedWingBack`)；组织型翼卫 (`PlaymakingWingBack`)；内收翼卫 (`InsideWingBack`)；翼卫 (`WingBack`)
- OOP（3）：留守翼卫 (`OPHoldingWingBack`)；翼卫 (`OPWingBack`)；逼抢翼卫 (`OPPressingWingBack`)

### WBL — 左翼卫
- IP（4）：进攻型翼卫 (`AdvancedWingBack`)；组织型翼卫 (`PlaymakingWingBack`)；内收翼卫 (`InsideWingBack`)；翼卫 (`WingBack`)
- OOP（3）：留守翼卫 (`OPHoldingWingBack`)；翼卫 (`OPWingBack`)；逼抢翼卫 (`OPPressingWingBack`)

### DMC — 防守中场（中）
- IP（5）：全能组织者 (`BoxToBoxPlaymaker`)；半后卫 (`HalfBack`)；全能中场 (`BoxToBoxMidfielder`)；拖后组织核心 (`DeepLyingPlaymaker`)；防守中场 (`DefensiveMidfielder`)
- OOP（5）：屏障后腰 (`OPScreeningDefensiveMidfielder`)；防守中场 (`OPDefensiveMidfielder`)；回撤后腰 (`OPDroppingDefensiveMidfielder`)；边路补位后腰 (`OPWideCoverDefensiveMidfielder`)；逼抢后腰 (`OPPressingDefensiveMidfielder`)

### DMR — 右后腰
- IP（5）：全能组织者 (`BoxToBoxPlaymaker`)；半后卫 (`HalfBack`)；全能中场 (`BoxToBoxMidfielder`)；拖后组织核心 (`DeepLyingPlaymaker`)；防守中场 (`DefensiveMidfielder`)
- OOP（5）：屏障后腰 (`OPScreeningDefensiveMidfielder`)；防守中场 (`OPDefensiveMidfielder`)；回撤后腰 (`OPDroppingDefensiveMidfielder`)；边路补位后腰 (`OPWideCoverDefensiveMidfielder`)；逼抢后腰 (`OPPressingDefensiveMidfielder`)

### DML — 左后腰
- IP（5）：全能组织者 (`BoxToBoxPlaymaker`)；半后卫 (`HalfBack`)；全能中场 (`BoxToBoxMidfielder`)；拖后组织核心 (`DeepLyingPlaymaker`)；防守中场 (`DefensiveMidfielder`)
- OOP（5）：屏障后腰 (`OPScreeningDefensiveMidfielder`)；防守中场 (`OPDefensiveMidfielder`)；回撤后腰 (`OPDroppingDefensiveMidfielder`)；边路补位后腰 (`OPWideCoverDefensiveMidfielder`)；逼抢后腰 (`OPPressingDefensiveMidfielder`)

### MR — 右边前卫
- IP（4）：组织型边锋 (`PlaymakingWinger`)；内收边锋 (`InsideWinger`)；边锋 (`Winger`)；边前卫 (`WideMidfielder`)
- OOP（3）：回防边前卫 (`OPTrackingWideMidfielder`)；边路接应前卫 (`OPWideOutletWideMidfielder`)；边前卫 (`OPWideMidfielder`)

### ML — 左边前卫
- IP（4）：组织型边锋 (`PlaymakingWinger`)；内收边锋 (`InsideWinger`)；边锋 (`Winger`)；边前卫 (`WideMidfielder`)
- OOP（3）：回防边前卫 (`OPTrackingWideMidfielder`)；边路接应前卫 (`OPWideOutletWideMidfielder`)；边前卫 (`OPWideMidfielder`)

### MC — 中前卫（中）
- IP（6）：中场组织者 (`MidfieldPlaymaker`)；前腰 (`AttackingMidfielder`)；偏侧中场 (`WideCentralMidfielder`)；中前卫 (`CentralMidfielder`)；前场组织核心 (`AdvancedPlaymaker`)；肋部中场 (`ChannelMidfielder`)
- OOP（4）：中前卫 (`OPCentralMidfielder`)；逼抢中场 (`OPPressingCentralMidfielder`)；边路补位中场 (`OPWideCoverCentralMidfielder`)；屏障中场 (`OPScreeningCentralMidfielder`)

### MCR — 右中前卫
- IP（6）：中场组织者 (`MidfieldPlaymaker`)；前腰 (`AttackingMidfielder`)；偏侧中场 (`WideCentralMidfielder`)；中前卫 (`CentralMidfielder`)；前场组织核心 (`AdvancedPlaymaker`)；肋部中场 (`ChannelMidfielder`)
- OOP（4）：中前卫 (`OPCentralMidfielder`)；逼抢中场 (`OPPressingCentralMidfielder`)；边路补位中场 (`OPWideCoverCentralMidfielder`)；屏障中场 (`OPScreeningCentralMidfielder`)

### MCL — 左中前卫
- IP（6）：中场组织者 (`MidfieldPlaymaker`)；前腰 (`AttackingMidfielder`)；偏侧中场 (`WideCentralMidfielder`)；中前卫 (`CentralMidfielder`)；前场组织核心 (`AdvancedPlaymaker`)；肋部中场 (`ChannelMidfielder`)
- OOP（4）：中前卫 (`OPCentralMidfielder`)；逼抢中场 (`OPPressingCentralMidfielder`)；边路补位中场 (`OPWideCoverCentralMidfielder`)；屏障中场 (`OPScreeningCentralMidfielder`)

### AMR — 右边锋
- IP（5）：组织型边锋 (`PlaymakingWinger`)；内锋 (`InsideForward`)；内收边锋 (`InsideWinger`)；边锋 (`Winger`)；边路前锋 (`WideForward`)
- OOP（4）：拉边接应边锋 (`OPWideOutletWinger`)；边锋 (`OPWinger`)；内收接应边锋 (`OPInsideOutletWinger`)；回防边锋 (`OPTrackingWinger`)

### AML — 左边锋
- IP（5）：组织型边锋 (`PlaymakingWinger`)；内锋 (`InsideForward`)；内收边锋 (`InsideWinger`)；边锋 (`Winger`)；边路前锋 (`WideForward`)
- OOP（4）：拉边接应边锋 (`OPWideOutletWinger`)；边锋 (`OPWinger`)；内收接应边锋 (`OPInsideOutletWinger`)；回防边锋 (`OPTrackingWinger`)

### AMC — 前腰（中）
- IP（5）：前腰 (`AttackingMidfielder`)；影子前锋 (`SecondStriker`)；自由人 (`FreeRole`)；前场组织核心 (`AdvancedPlaymaker`)；肋部中场 (`ChannelMidfielder`)
- OOP（4）：前腰 (`OPAttackingMidfielder`)；中路接应前腰 (`OPCentralOutletAttackingMidfielder`)；回防前腰 (`OPTrackingAttackingMidfielder`)；拉开接应前腰 (`OPSplittingOutletAttackingMidfielder`)

### AMCR — 右前腰
- IP（5）：前腰 (`AttackingMidfielder`)；影子前锋 (`SecondStriker`)；自由人 (`FreeRole`)；前场组织核心 (`AdvancedPlaymaker`)；肋部中场 (`ChannelMidfielder`)
- OOP（4）：前腰 (`OPAttackingMidfielder`)；中路接应前腰 (`OPCentralOutletAttackingMidfielder`)；回防前腰 (`OPTrackingAttackingMidfielder`)；拉开接应前腰 (`OPSplittingOutletAttackingMidfielder`)

### AMCL — 左前腰
- IP（5）：前腰 (`AttackingMidfielder`)；影子前锋 (`SecondStriker`)；自由人 (`FreeRole`)；前场组织核心 (`AdvancedPlaymaker`)；肋部中场 (`ChannelMidfielder`)
- OOP（4）：前腰 (`OPAttackingMidfielder`)；中路接应前腰 (`OPCentralOutletAttackingMidfielder`)；回防前腰 (`OPTrackingAttackingMidfielder`)；拉开接应前腰 (`OPSplittingOutletAttackingMidfielder`)

### ST — 中锋（中）
- IP（6）：支点前锋 (`TargetForward`)；拖后前锋 (`DeepLyingForward`)；伪九号 (`FalseNine`)；中锋 (`CentreForward`)；拉边前锋 (`ChannelForward`)；抢点前锋 (`Poacher`)
- OOP（4）：拉开接应中锋 (`OPSplittingOutletCentreForward`)；回防中锋 (`OPTrackingCentreForward`)；中锋 (`OPCentreForward`)；中路接应中锋 (`OPCentralOutletCentreForward`)

### STR — 右侧前锋
- IP（6）：支点前锋 (`TargetForward`)；拖后前锋 (`DeepLyingForward`)；伪九号 (`FalseNine`)；中锋 (`CentreForward`)；拉边前锋 (`ChannelForward`)；抢点前锋 (`Poacher`)
- OOP（4）：拉开接应中锋 (`OPSplittingOutletCentreForward`)；回防中锋 (`OPTrackingCentreForward`)；中锋 (`OPCentreForward`)；中路接应中锋 (`OPCentralOutletCentreForward`)

### STL — 左侧前锋
- IP（6）：支点前锋 (`TargetForward`)；拖后前锋 (`DeepLyingForward`)；伪九号 (`FalseNine`)；中锋 (`CentreForward`)；拉边前锋 (`ChannelForward`)；抢点前锋 (`Poacher`)
- OOP（4）：拉开接应中锋 (`OPSplittingOutletCentreForward`)；回防中锋 (`OPTrackingCentreForward`)；中锋 (`OPCentreForward`)；中路接应中锋 (`OPCentralOutletCentreForward`)

## 未覆盖的位置代码

- `SW`：当前原生角色权限表没有独立权限行，不得直接套用 GK/中卫角色。
- `DM`：当前原生角色权限表没有独立权限行；防守中场角色权限按 `DMC`、`DMR`、`DML` 等具体槽位提取，不得直接把 DMC 角色表复制到 DM。

## 使用边界

1. 生成战术时，`STC` 的角色权限查询应使用 `ST`；最终配方/原生战术槽位字段是否写 `STC`，仍按导出器接口要求，不要把查询别名直接覆盖写入战术位置字段。
2. 对其他 24 个原生位置代码，按扩展 CSV 中对应原始位置行查询。
3. PI 可编辑项随角色、阶段及 duty 状态变化；完整逐 duty 记录在 `FM27_Role_PI_Permissions_Expanded.csv`，不要只使用汇总样例。
4. 本目录覆盖当前提取源中的 24 个原生角色上下文及本项目需要的 STC 别名；不宣称是跨游戏版本的永久官方清单。

