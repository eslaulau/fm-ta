# 01｜网站生成规则：fmtacticlab.netlify.app

> 统一资料入口：先阅读上级 [00_资料总索引与检索规范](../00_资料总索引与检索规范.md)。本文件是网站快照/网页规则资料，不替代 02 层 FM27 原生角色与 PI 权限资料。

本层是网站生成器的设计参考层，不是 FM27 原生权限表，也不构成实际导入成功证明。

## 1. 快照来源与边界
- 页面：https://fmtacticlab.netlify.app/
- HAR 页面开始时间：2026-11-16 05:39:48 UTC。
- 页面内嵌 JavaScript 约 291,441 字符。
- HAR 共 4 条记录：页面主文档、Google Fonts、两次 Netlify HUD 脚本。主文档为 HTTP 304，但 HAR 保存了响应正文。
- HAR 没有记录 tactics.sortitoutsi.net 的实际 API 请求/响应体；本层关于下游 API 的说明来自页面内嵌 bookmarklet 源码，而非 API 响应实测。

网站源码自述：90 条官方 FM27 预设来源于 Sports Interactive 的预设，并通过 tactics.sortitoutsi.net 读取；高级战术思路参考 FM27 试用版、完整版和社区测试。这是网站自身的来源声明，不是本项目独立验证了原始 SI 预设包。

## 2. 页面数据规模
| 数据项 | 数量 | 说明 |
|---|---:|---|
| 预设 P | 90 | 10 个风格组，每组 9 条 |
| 自定义 4-4-2 模板 | 2 | 不计入上述 90 条 |
| 有球阵型选项 | 10 | FORMATIONS |
| 角色显示名 | 62 | ROLES 数组 |
| 教练模板 | 29 | COACHES |
| 球队指令 | 27 | TI |
| 页面直接映射的 PI 类型 | 7 | PI_KEY |
| 页面语言 | 8 | 包含中文 |

预设组为：Catenaccio、Control Possession、Direct Counter Attack、Fluid Counter Attack、Gegenpress、Park The Bus、Route One、Tiki-Taka、Vertical Tiki-Taka、Wingplay。

10 种 IP 阵型：
1. 4-2-3-1 DM AM Wide
2. 4-3-3 DM Wide
3. 4-4-2
4. 4-2-4 DM Wide
5. 4-2-2-2 DM
6. 4-4-2 Diamond Narrow
7. 5-2-3 DM Wide
8. 5-3-2 DM WB
9. 5-2-1-2 DM AM
10. 5-2-2-1 DM AM

## 3. 用户风格与预设组映射
| 用户风格 | 窄 | 平衡 | 宽 |
|---|---|---|---|
| 控球 possession | Tiki-Taka | Control Possession | Control Possession |
| 逼抢 press | Vertical Tiki-Taka | Gegenpress | Gegenpress |
| 反击 counter | Fluid Counter Attack | Fluid Counter Attack | Direct Counter Attack |
| 直接进攻 direct | Route One | Route One | Wingplay |
| 防守 defence | Catenaccio | Park The Bus | Park The Bus |

网站会先按预设组和 IP 阵型寻找候选池；没有精确匹配时，按 NEAR 表寻找相近风格组。选定 OOP 阵型变体后，再按球队实力、进攻宽度和模式调整球队指令。

## 4. 普通模式、高级模式与教练模式
- 普通模式：载入 STYLE 中的心态与 TI，再根据宽度修改进攻宽度、推进方向、传中方式等。
- 高级模式：进攻/控球侧有 17 条候选 TI 覆写规则；防守高级模式另有一组低位、防线、退守、反击和纪律性方向的 TI。规则会按风格和宽度跳过部分设置。
- 结构特例：特定 4-2-4 高级配置会调整双后腰、边锋、双前锋和 OOP 角色；检测到 DC+DCL+DCR 三中卫结构时，会重新配置中卫与翼卫角色。
- 教练模式：内置 29 名教练模板。页面明确表示这是将教练风格“诠释”为 FM27 设置，并非声称还原教练的官方真实战术。

这些逻辑是生成器的策略，不是任何阵容都适用的必胜公式。页面自己的建议是先应用，再根据约 5–6 场表现调整。

## 5. 页面评分的正确用法
网站 0–100 分为启发式评分：
- 战术一致性 30 分；
- 与页面参考设置的匹配度 35 分；
- 无球防守结构 20 分；
- 指令复杂度 15 分。

评分不代表胜率、预期积分或正式比赛结果。战术好坏最终应由同口径实战数据验证。

## 6. 两个 4-4-2 模板的 base 差异
页面 TEMPLATES 中的两个模板，IP 都是 4-4-2，OOP 分别为 4-4-2 和 4-2-2-2 DM；但 serializer 的 TEMPLATE_BASE 固定写为 Gegenpress / 4-2-4 DM Wide / 4-2-2-2 DM。下游 importer 又要求 base 风格组和 IP/OOP 阵型精确匹配预设。此处必须以实际导入测试确认，不应擅自修正或假定一定可用。

## 7. 角色名称精确匹配
页面 ROLES 数组和 ROLE 字典中的标准名称是 **Central Outlet Centre Forward**，Centre 与 Forward 之间只有空格，没有连字符。旧配方中的 **Central Outlet Centre-Forward** 是不同字符串。名称 token 不匹配与位置槽不兼容是两个独立问题，必须先用准确名称隔离测试。

## 8. 当前 serializer 的输出限制
页面 serializer 当前：
- 输出 v=1、战术名称、心态、base、27 项 TI 和 11 个位置槽；
- 每个阶段写入位置、角色和 PI，但不写 duty；
- 页面直接映射的 PI 类型只有 7 种；
- OOP PI 固定输出空数组；
- 槽位按后卫线以及 DMR/DML/AMR/AML/AMC/STC 的固定参照顺序排序；其他阵型使用坐标最近匹配。

这些是当前网页实现的限制，不应误称为 GEN1 v1 格式所有可能的能力。需重新抓取 HAR/源码才能确认未来网站版本是否变化。
