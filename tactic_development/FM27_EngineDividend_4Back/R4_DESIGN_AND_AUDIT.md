# R4 设计审计｜R3 D5 数据驱动迭代

父版本：V0.5
重生基准：V0.5
重生基准 FMF SHA-256：e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257
父 FMF SHA-256：e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257
项目规则 SHA-256：0000000000000000000000000000000000000000000000000000000000000000
决策总账 SHA-256：0000000000000000000000000000000000000000000000000000000000000000
PPG 策略 SHA-256：0000000000000000000000000000000000000000000000000000000000000000
位置绩效标准 SHA-256：0000000000000000000000000000000000000000000000000000000000000000
本轮配方 SHA-256：0000000000000000000000000000000000000000000000000000000000000000

## 1. 证据来源与本轮目标

- R3 D5 来源：[FM27-Exporter Run 45850910254](https://github.com/eslaulau/FM27-Exporter/tree/main/season-reports/1/45850910254)，完整分析见 `R3_D5_SEASON_REVIEW_45850910254.md`。
- 用户确认该存档赛季使用R3；Exporter本身不导出每场战术配置，版本归属按用户确认。
- R3 38场英超：19胜9平10负、66分、PPG1.737、xG65.00、xGA46.18；109分与xG100双硬门槛均失败。
- 19场非胜场平均xG1.21、平均射门9.84；胜场平均xG2.21、平均射门13.95。R4 的积分收益路径是抬高低产比赛的射门与机会产量，同时保持后场保护。
- 完整位置统计支持保留前场四人槽位：ST19.73xG、AMC15.35、AML13.03、AMR3.88；四位置合计约52.0xG。AMR虽xG较低但有19助攻，不能将其改成纯终结角色。
- 右后卫位置为0.94xG/4助攻，R4提升其IP职责；DMC位置合计9.16xG/7球/4助攻，R4让一侧IP中场获得更多第二线前插，同时OOP继续锁位。
- 传中1,190次、完成192次（16.1%）；越位93次。R4将传入空当改传至脚下、尽早传中改将球做入禁区，保留高球传中与后点目标，检验更好的传球/传中时机。
- 位置码覆盖英超598/598；208条原始位置交叉核对零不匹配。角色码只解码出9类IP角色且覆盖部分记录；没有逐场OOP角色、PI/TI执行映射。不得将位置码冒充战术槽位或PI因果。

## 2. 结构搜索与唯一主线选择

现实足球理论不是战术筛选/否决标准。本轮对照4-2-3-1、4-2-4、4-3-3 DM等四后场IP结构。R3的四个前场位置已经贡献约52.0xG，AMR提供19助攻；因此本轮不删除AMC、不减少前场宽度、不改为双中锋，而是保留IP 4-2-3-1，集中改变OOP前场出口、DMR职责和两项进攻TI。唯一主线为IP 4-2-3-1 / OOP strikerless 5-2-3。

外部参考：metaFM 27.1.1榜首3-4-3使用OOP 5-2-3，2.06 PPG、xG2.51、xGA1.41；该IP三后卫不符合本项目四后场约束，仅参考其OOP五后卫与三前场形态。公开测试数据不是本队赛季预测，也不能证明本轮角色组合有效。

## 3. R4 具体配置变化

### 角色与职责

- IP DR：WingBack Support → WingBack Attack；OOP仍HoldingFullBack Defend。
- IP DMR：DefensiveMidfielder Defend → BoxToBoxMidfielder Support；OOP仍WideCoverDefensiveMidfielder Defend。IP增加第二线前插，OOP恢复宽幅覆盖责任。
- IP DML：DefensiveMidfielder Defend；OOP转换第三中卫CoveringCentreBack Defend。
- IP AMC：保留FreeRole Attack；OOP转换DroppingDefensiveMidfielder Defend。
- IP AML/AMR：保留InsideForward Attack / Winger Support；OOP由TrackingWinger改为InsideOutletWinger Attack / WideOutletWinger Attack。
- IP ST：保留TargetForward Attack；OOP由AttackingMidfielder Support改为CentralOutletAttackingMidfielder Attack。
- IP DL：InsideFullBack Defend；OOP HoldingFullBack Defend。DCL/DCR与OOP第三中卫继续保持低逼抢/补位分工。
- OOP形态仍是5后卫+双后腰+三个高位接应出口；无ST位置。

### 球员指令

- AMC FreeRole：移除Shoot Less Often；团队仍保留减少远射，避免显式PI额外压低中路射门。
- OOP 10名外场球员继续Tackle Harder（GET_STUCK_IN）；原生PI权限目录允许本轮新设的InsideOutletWinger、WideOutletWinger、CentralOutletAttackingMidfielder使用Tackle Harder与Trigger Press More Often。
- OOP双后腰和前场三出口Trigger Press More Often；DCL维持Trigger Press Less Often；CoveringCentreBack与HoldingFullBack不强写原生权限固定关闭的More Often。
- AML/AMR前插、AMR拉宽/下底/后点、DR拉宽/下底/后点；中卫短传少射门、DL短传少冒险、DML保持位置、DMR不再被Keep Position限制。

### 球队指令

- 替换：Pass Into Space → Pass To Feet。
- 替换：Hit Early Crosses → Work Ball Into Box。
- 保留：More Direct、Much Higher Tempo、Wider、Counter Attack、More Expressive、Bypass Press、Long Goal Kicks、Target Forward、Quick Distribution、Both Flanks、Encourage Dribbling、Discourage Long Shots、High Crosses。
- 保留OOP：High Press、Much Lower Defensive Line、Drop Off More、More Often Team Trigger Press、Counter Press、Trap Outside、Invite Crosses。
- 预期：减少传入身后导致的越位与低质量早传中；三个OOP出口提高反击接应点；右侧翼卫更积极提供宽度。所有效果均待D5证伪/验证。

## 4. 四类决策

### 继承保留

- IP四后场DL/DCL/DCR/DR硬约束；IP 4-2-3-1前场四人位置结构。
- IP InsideForward A、FreeRole A、Winger S、TargetForward A、InsideFullBack D；没有充分角色级证据淘汰这些位置角色。
- OOP 5-2-3无锋五后卫+双后腰保护；高位逼抢遭遇线、极低防线、Drop Off More。
- 高球传中、后点目标、Tackle Harder广泛覆盖与差异化Trigger Press。

### 替换淘汰

- R3的OOP TrackingWinger/AttackingMidfielder三出口组合替换为InsideOutletWinger/WideOutletWinger/CentralOutletAttackingMidfielder；这是阶段职责调整，不声称原角色本身已被单项证明低效。
- DR WingBack S改A；DMR DefensiveMidfielder D改BoxToBoxMidfielder S。
- AMC的Shoot Less Often PI删除。
- Pass Into Space与Hit Early Crosses从R4配方中移除，分别改为Pass To Feet与Work Ball Into Box。

### 新增待验证

- IP BoxToBoxMidfielder S ↔ OOP WideCoverDefensiveMidfielder D。
- OOP无锋三出口的Inside/Wide/Central互补组合。
- DR WingBack A ↔ OOP HoldingFullBack D。
- Pass To Feet + Work Ball Into Box + High Crosses + Back Post。
- 前场三出口及双后腰的Trigger Press More Often与全队Tackle Harder组合。

### 证据不足

- 角色码只有部分历史记录，OOP角色/职责/PI/TI没有逐场映射；不能将整季位置统计归因到单一角色。
- 没有传中落点、禁区触球、xA、射门位置和完整回合事件。
- 27.1.1+2511875使用借用的schema-6布局；局部字段核对通过，但整体兼容性标记partial/unverified。
- 角色默认行为的完整自然语言解释尚未解码；本轮以原生角色/PI权限目录作合法性验证，场上执行效果仍待D4/D5。

## 5. 位置绩效高强度审查与低效淘汰

证据等级：A=角色/阶段/球员/分钟直接归因；B=部分角色样本；C=完整位置或球队描述；U=阶段/角色不可判定。任何C/U项目都不能被宣称已通过角色绩效审查。

| 槽位 | 位置/角色/职责 | 分钟/覆盖 | 评分 | 进球/助攻 | xG/xA | 过程指标 | 证据等级 | 本轮判决 |
|---|---|---|---|---|---|---|---|---|
| IP-01 | GK 出球门将 S | 3420/38场 | 6.91 | 0/1 | 0/无 | 传球成功率55.5% | C | 条件保留 |
| IP-02 | DR 翼卫 A | 3445/位置记录 | 6.81 | 0/4 | 0.94/无 | 132次传中、20.5%完成 | C/B | 职责替换待测 |
| IP-03 | DCR 中后卫 D | DC合并6553分钟 | 6.82 | 2/0（DC合并） | 1.89/无 | 203次争顶胜出（DC合并） | C | 角色证据不足 |
| IP-04 | DCL 中后卫 D | DC合并6553分钟 | 6.82 | 2/0（DC合并） | 1.89/无 | 左右中卫无法拆分 | C | 角色证据不足 |
| IP-05 | DL 内收边后卫 D | 3681/位置记录 | 6.76 | 2/3 | 1.03/无 | 181次传中、7.7%完成 | B/C | 条件保留 |
| IP-06 | DML 防守中场 D | DMC合并6947分钟 | 6.88 | 7/4（双后腰合并） | 9.16/无 | 100射门、4绝佳机会 | C | 条件保留 |
| IP-07 | DMR 全能中场 S | DMC合并6947分钟 | 6.88 | 7/4（双后腰合并） | 9.16/无 | DML/DMR无法拆分 | C/U | 新职责待测 |
| IP-08 | AML 内锋 A | 3429/位置记录 | 7.03 | 9/16 | 13.03/无 | 93射门、11绝佳机会、16越位 | B/C | 条件保留 |
| IP-09 | AMC 自由人 A | 3330/位置记录 | 6.88 | 11/6 | 15.35/无 | 98射门、13绝佳机会、21越位 | B/C | 保留角色、移除Shoot Less |
| IP-10 | AMR 边锋 S | 3390/位置记录 | 6.94 | 3/19 | 3.88/无 | 44射门、1绝佳机会、373次传中（含其他位置贡献口径需谨慎） | B/C | 保留供给角色 |
| IP-11 | ST 支点前锋 A | 3423/位置记录 | 6.93 | 30/3 | 19.73/无 | 82射门、23绝佳机会、34越位 | B/C | 条件保留 |
| OOP-01 | GK 门将 S | OOP未导出 | 未导出 | 未导出 | 不适用 | OOP扑救/站位未导出 | U | 未准入 |
| OOP-02 | DR 留守边后卫 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 阶段职责未导出 | U | 新配对待测 |
| OOP-03 | DCR 补位中卫 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 阶段职责未导出 | U | 未准入 |
| OOP-04 | DCL 中后卫 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 阶段职责未导出 | U | 未准入 |
| OOP-05 | DL 留守边后卫 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 阶段职责未导出 | U | 新配对待测 |
| OOP-06 | DC 补位中卫 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 第三中卫位置转换未导出 | U | 未准入 |
| OOP-07 | DML 边路补位后腰 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 双后腰OOP站位未导出 | U | 未准入 |
| OOP-08 | DMR 回撤后腰 D | OOP未导出 | 未导出 | 未导出 | 不适用 | 双后腰OOP站位未导出 | U | 未准入 |
| OOP-09 | AML 内收接应边锋 A | OOP未导出 | 未导出 | 未导出 | 不适用 | 高位出口/反击触球未导出 | U | 新角色待测 |
| OOP-10 | AMR 拉边接应边锋 A | OOP未导出 | 未导出 | 未导出 | 不适用 | 高位出口/反击触球未导出 | U | 新角色待测 |
| OOP-11 | AMC 中路接应前腰 A | OOP未导出 | 未导出 | 未导出 | 不适用 | 高位出口/反击触球未导出 | U | 新角色待测 |

### 低效淘汰清单

- R3整套版本：D5积分/xG双门槛均失败，淘汰为达标候选；保留为历史证据。
- R3的Pass Into Space与Hit Early Crosses组合：从R4移除，原因是93次越位与1,190次传中、16.1%完成率形成需检验的组合风险；不声称已证明单项因果。
- R3的OOP TrackingWinger三出口配置：替换为Outlet角色组合，以验证无锋前场高位出口。
- 没有任何角色仅凭不完整角色样本被宣判单项低效；DCL/DCR、DML/DMR和所有OOP槽位均保留证据边界。

### 准入保留

- 没有任何单个槽位达到A类直接归因；本轮保留的是待测试结构假设，不是绩效认证。
- IP前场四人槽位因完整位置数据的产出而条件保留；角色级表现仍需逐场映射补证。

### 条件保留

- IP GK、DL、DML、AML、AMC、AMR、ST等角色/职责组合进入R4，但不得标记为已通过角色级绩效审查。
- IP DR与DMR采用新职责，需通过D4导入和D5整季数据验证。

### 替换淘汰

- R3的两项球队指令与OOP跟防型前场角色组合按上文替换；R2仍按用户此前决定退役，不恢复。

### D5

- 完整38场联赛：积分≥109（PPG≥2.85）且xG≥100，两项同时满足才通过。
- 过程目标：至少650次射门、xG/射门≥0.154、场均xG≥2.63；非胜场平均xG显著高于R3的1.21。
- 防守护栏：重点监控xGA、对手绝佳机会、客场xGA与客场PPG，防止三个高位出口破坏OOP结构。
- 无逐场阶段/角色映射时，不对单个PI、角色或OOP槽位作直接因果结论。

## 6. PPG改进路径、风险与失败条件

- PPG改进路径：提高非胜场的射门/绝佳机会产量；让OOP三前场出口在夺回球权后保留接应点；通过DR WingBack Attack和DMR BoxToBox Support增加右路及第二线参与；用Pass To Feet降低无效身后传球，用Work Ball Into Box减少低质量早传中。
- 可能副作用：OOP三个高位出口会减少边路回防；DR WingBack Attack可能扩大右侧转换空间；DMR BoxToBox可能在IP推进时留下中场空隙；Work Ball Into Box可能降低早期反击速度；Pass To Feet可能减少直塞穿透。
- 失败条件：38场积分<109或xG<100任一发生，D5整体FAIL；若xG达标但积分不足，重点检查射门转化与防守成本；若积分达标但xG不足，仍判FAIL。
- 风险监控：对手xGA、客场xGA、非胜场xG、越位、传中量/完成率、前场三出口参与和球权转换。

## 7. 强制审计：引擎行为错位设计

现实足球理论不是战术筛选/否决标准。本轮设计阶段职责错位与团队指令错位，所有引擎效果均为待证伪假设。

- 错位类型：IP/OOP位置转换；IP中场推进与OOP防守锁位错位；IP翼卫进攻与OOP留守错位；无锋三出口与低防线五后卫错位；传球接应和传中时机指令错位。
- 错位配置：IP DMR BoxToBoxMidfielder Support → OOP DML WideCoverDefensiveMidfielder Defend；IP DR WingBack Attack → OOP DR HoldingFullBack Defend；IP AML/AMR/ST → OOP InsideOutletWinger/WideOutletWinger/CentralOutletAttackingMidfielder；IP AMC FreeRole → OOP DMR DroppingDefensiveMidfielder。
- 角色/指令默认行为：原生目录确认角色与PI合法性；完整角色默认行为自然语言尚未解码，不对隐藏跑位作确定陈述。翼卫进攻职责、全能中场职责和Outlet角色名只用于定义设计意图。
- FM27引擎预期执行行为：OOP三个Outlet可能在丢球后保持较高接应位置；DMR在IP阶段增加第二线前插、OOP阶段回到宽幅保护；DR在IP阶段更积极推进、OOP阶段回到留守边后卫；传至脚下可能减少无效越位，做入禁区可能让传中发生在更靠近底线/禁区的区域。全部待D5验证。
- 对手AI可能：面对高位三出口可能更频繁使用长传或边路出球；面对极低防线和引诱传中可能增加边路传中；面对更积极的DR/DMR可能攻击右侧转换空间。均为假设。
- 预期创造的空间：前场三出口为反击保留内侧、外侧和中路接应点；DR提供右侧宽度；DMR从第二线进入进攻三区；支点前锋仍为高球传中/后点进攻的主要目标。
- 对PPG的预期收益路径：降低非胜场低产率、提高反击第一传接应成功率、增加第二线和右侧进攻参与，争取将部分平局/败场转为胜场，目标PPG≥2.85且xG≥100。
- 可能副作用：高位出口回防不足；右侧边路暴露；DMR前插破坏中场保护；传至脚下降低身后球穿透；做入禁区减少快速反击；OOP低位防线与高位出口之间出现距离过大。
- D5量化验证指标：积分/PPG、xG/NPxG、射门/射正/绝佳机会、非胜场xG、主客场PPG/xGA、越位、传中尝试/完成、DR助攻与传中、DMR进球/xG/禁区参与、三个Outlet的进攻参与和OOP失球后对手机会。不可观测指标明确标记缺失。

## 8. D4/D5验收

- D4：FM27游戏内导入，确认IP 4-2-3-1四后场、OOP无锋5-2-3、11个槽位角色/职责、三名Outlet、DMR阶段转换、全部PI/TI显示。
- D5：完整38场联赛；109分/PPG2.85与xG100双硬门槛同时通过。
- D3通过只证明原生FMF生成和独立二进制回读，不代表D4导入或D5比赛效果。

## 9. 生成前审计结论

- [x] 父版本严格为V0.5，未继承R3 FMF；R3仅作为D5证据。
- [x] IP四后场DL/DCL/DCR/DR各一次。
- [x] 11槽/22阶段完整定义。
- [x] 单一主线结构及角色/PI/TI变更明确。
- [x] 位置绩效矩阵覆盖IP/OOP 22槽，并标注证据等级。
- [x] 四类决策、低效淘汰清单、引擎错位设计、风险和D5指标齐全。
- [x] 原生目录PI权限已预检：Outlet前场角色允许Tackle Harder与Trigger Press More Often；HoldingFullBack/CoveringCentreBack不强写固定关闭的More Often。
- [ ] D0-D3项目门禁与原生构建待运行。
- [ ] D4游戏内导入待用户确认。
- [ ] D5完整38场赛季报告待补。

审计结论： PASS
