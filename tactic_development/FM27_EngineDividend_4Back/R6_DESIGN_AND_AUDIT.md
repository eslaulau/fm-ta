# R6｜IP 4-2-2-2 Box / OOP 5-3-2｜构建审计

版本：R6
父版本：V0.5
重生基准：V0.5
重生基准 FMF SHA-256：e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257
父 FMF SHA-256：e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257
本轮配方 SHA-256：PLACEHOLDER
项目规则 SHA-256：PLACEHOLDER
决策总账 SHA-256：PLACEHOLDER
PPG 策略 SHA-256：PLACEHOLDER
位置绩效标准 SHA-256：PLACEHOLDER
审计结论： PASS

## 1. 版本与目标

R6从固定V0.5原生FMF重新生成，不继承R5.3的阵型/角色布局。IP采用4-2-2-2 Box，OOP采用5-3-2。IP后场严格使用DL、DCL、DCR、DR各一次。OOP由IP的DML转为DC，形成三中卫加两侧后卫；双前腰回落为ML/MR，中场屏障落在MC，双前锋保留为前场出口。

比赛心态：进攻（原生值6）。全部29组团队指令均明确设置或显式DEFAULT，不留空白继承项。

硬目标：完整38场联赛至少109分（PPG ≥ 2.85），同时全队xG≥100。任一未达标，D5失败。现实足球理论不是战术筛选/否决标准；只按FM27原生合法性和游戏实测结果判断。

## 2. R6实际配置

- IP：GK；DL FullBack S；DCL CentreBack D；DCR BallPlayingCentreBack D；DR WingBack A；DML DefensiveMidfielder D；DMR DeepLyingPlaymaker S；AMCL AttackingMidfielder S；AMCR SecondStriker A；STL DeepLyingForward S；STR Poacher A。
- OOP：GK OPSweeperKeeper A；DL OPFullBack S；DCL/DCR OPCentreBack D；DC OPCoveringCentreBack D；DR OPPressingFullBack S；ML/MR OPWideMidfielder S；MC OPScreeningCentralMidfielder D；双前锋 OPCentreForward A。
- 团队指令：直传、高节奏、较宽、立刻反击、绕过压迫、长球门球、快速发球、寻找两侧、传球进入空当、鼓励盘带、减少远射、低平球传中、高位逼抢起点、较低防线、更多回撤防线、较多逼抢、立即反抢、引导向边路、阻止短门将出球、阻止传中；其余可映射组选项显式设为DEFAULT。
- 当前PI为空，避免未经必要验证的PI覆盖影响首轮结构测试；D4导入后根据实际引擎表现单独增补PI。

## 3. 四类决策

### 继承保留
- 仅保留V0.5作为原生二进制格式载体；不继承其阵型、角色和可映射球队指令配置。
- 保留项目既定的11槽、22个阶段、完整38场双门槛验收规则。

### 替换淘汰
- 不沿用R5.3的IP 4-1-2-3前五人布局及OOP 5-2-3角色转换。
- 本轮不采用未经验证的个人指令覆盖，先隔离阵型/角色/TI组合。

### 新增待验证
- 新增双后腰与双前腰菱形盒式通道、双前锋错层、DML→DC五后卫转换。
- 预期通过两名前腰与双前锋之间的短距离连接提升禁区进入次数；后腰下沉增加无球最后一线覆盖，减少失球波动，从而提高PPG。
- 假设尚未经过本队D4/D5实测；D4导入和D5完整赛季分别验收。

### 证据不足
- 当前没有R6的比赛样本，不能宣称任何位置、角色或指令已被证明有效。
- 目前没有个人指令贡献证据；保持PI为空，不把未配置内容描述为已生效。

## 4. D5量化验收

| 指标 | 通过条件 |
|---|---:|
| 英超场次 | 38 |
| 联赛积分 | ≥109 |
| PPG | ≥2.85 |
| 全队xG | ≥100 |
| 主客场 | 分开统计 |
| 平局/失利 | 逐场复核机会质量与丢球 |

## 7. 强制审计：引擎行为错位设计

- 错位类型：IP双后腰位置与OOP三中卫结构错位。
- 错位配置：IP DML防守中场在OOP改为DC补位中卫；两名攻击中场在OOP变为ML/MR边前卫。
- 角色/指令默认行为：IP后腰角色留在后场前方，OOP角色转换把其位置槽移入最后一线；前腰角色不再停留在前腰区域。
- FM27引擎预期执行行为：阵型切换按两个阶段位置/角色配置改变球员的起始职责和占位；实际移动路线仍须通过比赛观察验证。
- 对手AI可能：对手前场压迫目标和中场盯防对象会随阶段转换重新分配，可能产生短暂错位。
- 预期创造的空间：双前腰与双前锋之间的中路接应区域，以及边前卫回撤后边中场区域的保护。
- 对PPG：如果前场接应和无球防守转换同时改善，可减少平局/失利并提升场均积分；需以完整38场数据确认。
- 可能副作用：边路宽度不足、双前腰回撤不及时、单MC被压制、DML沉底后中场二点保护不足。
- D5量化验证指标：38场积分/PPG、全队xG/xGA、进球/失球、主客场积分、平局/失利场次和每场关键机会。

## 位置绩效高强度审查与低效淘汰

| 槽位 | 阶段位置/角色 | PI | 证据等级 | 当前决定 | 主要核验 | D5指标 | 低效淘汰清单 | 准入状态 |
|---|---|---|---|---|---|---|---|
| IP-01 | GK Goalkeeper D | 空 | U | 新增待验证 | 出球与失球 | 失误、xGA | 低效则替换 | D4导入/D5待验证 |
| IP-02 | DL FullBack S | 空 | U | 新增待验证 | 左侧推进 | 传中、xA | 低效则替换 | D4导入/D5待验证 |
| IP-03 | DCL CentreBack D | 空 | U | 新增待验证 | 中路保护 | 对手xG | 低效则替换 | D4导入/D5待验证 |
| IP-04 | DCR BallPlayingCentreBack D | 空 | U | 新增待验证 | 出球推进 | 向前传球 | 低效则替换 | D4导入/D5待验证 |
| IP-05 | DR WingBack A | 空 | U | 新增待验证 | 右侧推进 | xA、禁区触球 | 低效则替换 | D4导入/D5待验证 |
| IP-06 | DML DefensiveMidfielder D | 空 | U | 新增待验证 | 双相转换 | 夺回球权、失球 | 低效则替换 | D4导入/D5待验证 |
| IP-07 | DMR DeepLyingPlaymaker S | 空 | U | 新增待验证 | 组织输送 | xA、关键传球 | 低效则替换 | D4导入/D5待验证 |
| IP-08 | AMCL AttackingMidfielder S | 空 | U | 新增待验证 | 肋部接应 | xG+xA | 低效则替换 | D4导入/D5待验证 |
| IP-09 | AMCR SecondStriker A | 空 | U | 新增待验证 | 第二得分点 | xG、射门 | 低效则替换 | D4导入/D5待验证 |
| IP-10 | STL DeepLyingForward S | 空 | U | 新增待验证 | 前场串联 | xA、机会创造 | 低效则替换 | D4导入/D5待验证 |
| IP-11 | STR Poacher A | 空 | U | 新增待验证 | 纵深终结 | xG、进球 | 低效则替换 | D4导入/D5待验证 |
| OOP-01 | GK OPSweeperKeeper A | 空 | U | 新增待验证 | 身后覆盖 | xGA、失误 | 低效则替换 | D4导入/D5待验证 |
| OOP-02 | DL OPFullBack S | 空 | U | 新增待验证 | 左路防守 | 对手左路机会 | 低效则替换 | D4导入/D5待验证 |
| OOP-03 | DCL OPCentreBack D | 空 | U | 新增待验证 | 中路保护 | 对手中路xG | 低效则替换 | D4导入/D5待验证 |
| OOP-04 | DCR OPCentreBack D | 空 | U | 新增待验证 | 中路保护 | 对手中路xG | 低效则替换 | D4导入/D5待验证 |
| OOP-05 | DR OPPressingFullBack S | 空 | U | 新增待验证 | 右路压迫 | 对手右路机会 | 低效则替换 | D4导入/D5待验证 |
| OOP-06 | DC OPCoveringCentreBack D | 空 | U | 新增待验证 | 第三中卫补位 | 身后机会 | 低效则替换 | D4导入/D5待验证 |
| OOP-07 | MC OPScreeningCentralMidfielder D | 空 | U | 新增待验证 | 中路屏障 | 对手中路xG | 低效则替换 | D4导入/D5待验证 |
| OOP-08 | ML OPWideMidfielder S | 空 | U | 新增待验证 | 左侧回撤 | 对手左路机会 | 低效则替换 | D4导入/D5待验证 |
| OOP-09 | MR OPWideMidfielder S | 空 | U | 新增待验证 | 右侧回撤 | 对手右路机会 | 低效则替换 | D4导入/D5待验证 |
| OOP-10 | STL OPCentreForward A | 空 | U | 新增待验证 | 前场出口 | 转换机会 | 低效则替换 | D4导入/D5待验证 |
| OOP-11 | STR OPCentreForward A | 空 | U | 新增待验证 | 前场出口 | 转换机会 | 低效则替换 | D4导入/D5待验证 |

低效淘汰清单：任何槽位在完整38场中持续低贡献、导致对应区域机会质量恶化，或团队未达到109分/xG100门槛时，按可归因数据替换；无可归因数据时标记证据不足，不伪造单项因果。

证据等级：U=尚无R6比赛证据。准入保留、条件保留、替换淘汰均以D5报告复核；D3生成通过不代表比赛表现准入。

MACHINE_DECISION_MANIFEST_JSON_START
PLACEHOLDER
MACHINE_DECISION_MANIFEST_JSON_END

审计结论不代表游戏导入成功或赛季目标达成。D3仅指项目门禁、原生权限预检、FMF生成及独立回读完成；D4和D5仍待验证。
