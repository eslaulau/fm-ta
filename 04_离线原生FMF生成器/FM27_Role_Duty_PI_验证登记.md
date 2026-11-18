# FM27 角色、职责与指令证据验证登记

> 登记日期：2026-11-18  
> 对应分支：`main`  
> 证据基线：当前 `catalog.json`、`FM27GEN1_Offline_FMF_Generator.py`、90 条预设索引及仓库审计逻辑。  
> **本登记只确认数据来源、映射覆盖和写入权限证据，不代表战术效果已验证，也不代表 FM27 客户端导入或比赛实测通过。**

## 1. 证据来源结论

### 1.1 角色和菜单定义：同一份原生资源包

`04_离线原生FMF生成器/catalog.json` 的根级来源指纹：

- `source_bundle_sha256`: `c9d98c9c39a278ec7aae5db22e7dc0b9f7af2de398bb8610bab9fe9d094f7f07`
- `resolver_rva`: `0x64fe90`
- `resolver_page_sha256`: `4400b89bb203a79d13f25d0ab626ca238c30c02e1b2afc38f3610e6618314a4f`

同一目录文件中的 `raw_roles` 保留了 FM27 原始角色对象字段，包括 `m_roleID`、`m_pitchGIF`、`m_roleDescriptionTranslation.GameID`、`m_roleLabelsArray`、`m_rolePlayerInstructions` 等；`raw_player_instructions` 保留了个人指令组及选项定义；`team_instructions` 保存球队指令组及选项。

因此，**角色定义、个人指令菜单定义和球队指令菜单定义有同一份资源包指纹作为来源依据**。但当前 `catalog.json` 只记录资源包 SHA256，没有记录原始资源包文件名、提取路径和完整提取日志；本登记不虚构这些缺失的来源信息。

### 1.2 个人指令权限：独立的原生菜单/程序权限证据

`catalog.json.policy_provenance` 保存了以下来源定位：

| 字段 | 记录值 |
|---|---|
| IP 权限数据 RVA | `0x46bf1a0` |
| OOP 权限数据 RVA | `0x8d540` |
| 菜单属性 ID | `0x5a6e5536` |
| 菜单 getter 分支 | `0x634205..0x63439e` |
| IP 角色掩码 RVA | `0x16d5d40` |
| OOP 角色掩码 RVA | `0xbb5b0` |

权限状态定义：

| 状态码 | 含义 |
|---:|---|
| 0 | editable：允许编辑 |
| 1 | unavailable：该上下文不可用 |
| 2 | fixed_off：固定关闭 |
| 3 | fixed_on：固定开启 |

目录包含 **1,547 条** `phase:position:role:duty` 权限记录，目录版本为 `1a080000`、`1b000000`。生成器对具体 PI 逐项查询两个版本；缺少记录、版本冲突或状态不允许写入时拒绝生成。

**边界：** 权限记录存在，不表示所有 PI 菜单选项均已建立 GEN1 写入映射；仍须同时检查下文的 `PI_MAP`。

### 1.3 职责证据：原生 FMF 样本 + 网站 90 条官方预设索引

职责值不是从角色英文名称推断出来的。当前生成器 `ROLE_DUTY` 的来源注释明确区分了原生 TAC 样本、Control Possession 原生样本和 Netlify 90 条预设索引。

网站索引文件 `01_网站生成规则/Netlify_90官方预设索引.csv` 记录 90 条预设；审计脚本 `FM27GEN1_Netlify90_OfficialPreset_Audit.py` 会检查：

1. 预设角色显示名到原生角色 ID 的映射；
2. IP/OOP 阶段和位置资格；
3. 索引中 D/S/A 职责与生成器职责值是否一致；
4. 对应的 PI 权限记录是否存在；
5. 每个阶段是否有 11 个唯一位置。

按该脚本相同规则重新核对当前索引，得到 **90 条预设、10 种风格、1,980 个 IP/OOP 槽位分配、0 项错误**。这证明当前索引实际使用的 73 个角色及其职责映射与目录、权限记录一致。

**来源边界：** 审计脚本本身明确说明，网站索引是网站公开的官方预设数据，不等同于 90 份原始 FMF 文件，也不能据此证明 TAC FourCC、模板二进制或游戏内导入成功。

## 2. 已验证项目

### 2.1 角色定义：79/79 已验证存在

- 原始角色对象：79 个。
- 规范化角色目录：79 个，角色 ID 唯一。
- 阶段分布：IP 40 个；OOP 39 个。
- 位置目录：24 个。
- 角色/位置资格表：覆盖 24 个原生位置；目录中 79 个角色 ID 均能在资格表中找到。

**状态：已验证（角色定义、内部 ID、阶段归属和目录中的位置资格记录）。**  
这不代表每个角色都已经有职责映射，也不代表每个角色适用于所有位置。

### 2.2 职责映射：73/79 已验证

以下 73 个角色在当前 `ROLE_DUTY` 中有明确映射，并且被 90 条预设索引中的对应分配覆盖、通过职责一致性审计：

| 阶段 | 原生角色 ID | 目录显示名 | 已验证职责 |
|---|---|---|---|
| IP | `AdvancedPlaymaker` | 前场组织核心 | A（Attack） |
| IP | `AdvancedWingBack` | 进攻型翼卫 | A（Attack） |
| IP | `AttackingMidfielder` | 前腰 | A（Attack） |
| IP | `BallPlayingCentreBack` | 出球中卫 | D（Defend） |
| IP | `BallPlayingGoalkeeper` | 出球门将 | S（Support） |
| IP | `BoxToBoxMidfielder` | 全能中场 | S（Support） |
| IP | `BoxToBoxPlaymaker` | 全能组织者 | S（Support） |
| IP | `CentralMidfielder` | 中前卫 | S（Support） |
| IP | `CentreBack` | 中后卫 | D（Defend） |
| IP | `CentreForward` | 中锋 | A（Attack） |
| IP | `ChannelForward` | 拉边前锋 | A（Attack） |
| IP | `ChannelMidfielder` | 肋部中场 | A（Attack） |
| IP | `DeepLyingForward` | 拖后前锋 | A（Attack） |
| IP | `DeepLyingPlaymaker` | 拖后组织核心 | S（Support） |
| IP | `DefensiveMidfielder` | 防守中场 | D（Defend） |
| IP | `FreeRole` | 自由人 | A（Attack） |
| IP | `FullBack` | 边后卫 | S（Support） |
| IP | `Goalkeeper` | 门将 | D（Defend） |
| IP | `InsideForward` | 内锋 | A（Attack） |
| IP | `InsideFullBack` | 内收边后卫 | D（Defend） |
| IP | `InsideWingBack` | 内收翼卫 | D（Defend） |
| IP | `InsideWinger` | 内收边锋 | S（Support） |
| IP | `MidfieldPlaymaker` | 中场组织者 | S（Support） |
| IP | `NoNonsenseCentreBack` | 解围中卫 | D（Defend） |
| IP | `NoNonsenseGoalkeeper` | 清道夫式解围门将 | D（Defend） |
| IP | `PlaymakingWingBack` | 组织型翼卫 | S（Support） |
| IP | `Poacher` | 抢点前锋 | A（Attack） |
| IP | `SecondStriker` | 影子前锋 | A（Attack） |
| IP | `TargetForward` | 支点前锋 | A（Attack） |
| IP | `WideCentralMidfielder` | 偏侧中场 | S（Support） |
| IP | `WideCentreBack` | 边中卫 | D（Defend） |
| IP | `WideForward` | 边路前锋 | A（Attack） |
| IP | `WideMidfielder` | 边前卫 | S（Support） |
| IP | `WingBack` | 翼卫 | S（Support） |
| IP | `Winger` | 边锋 | S（Support） |
| OOP | `OPAttackingMidfielder` | 前腰 | S（Support） |
| OOP | `OPCentralMidfielder` | 中前卫 | S（Support） |
| OOP | `OPCentralOutletAttackingMidfielder` | 中路接应前腰 | A（Attack） |
| OOP | `OPCentralOutletCentreForward` | 中路接应中锋 | A（Attack） |
| OOP | `OPCentreBack` | 中后卫 | D（Defend） |
| OOP | `OPCentreForward` | 中锋 | S（Support） |
| OOP | `OPCoveringCentreBack` | 补位中卫 | D（Defend） |
| OOP | `OPDefensiveMidfielder` | 防守中场 | D（Defend） |
| OOP | `OPDroppingDefensiveMidfielder` | 回撤后腰 | D（Defend） |
| OOP | `OPFullBack` | 边后卫 | D（Defend） |
| OOP | `OPGoalkeeper` | 门将 | S（Support） |
| OOP | `OPHoldingFullBack` | 留守边后卫 | D（Defend） |
| OOP | `OPHoldingWingBack` | 留守翼卫 | D（Defend） |
| OOP | `OPInsideOutletWinger` | 内收接应边锋 | A（Attack） |
| OOP | `OPLineKeeper` | 门线门将 | D（Defend） |
| OOP | `OPPressingCentralMidfielder` | 逼抢中场 | A（Attack） |
| OOP | `OPPressingDefensiveMidfielder` | 逼抢后腰 | S（Support） |
| OOP | `OPPressingFullBack` | 逼抢边后卫 | S（Support） |
| OOP | `OPPressingWingBack` | 逼抢翼卫 | S（Support） |
| OOP | `OPScreeningCentralMidfielder` | 屏障中场 | D（Defend） |
| OOP | `OPScreeningDefensiveMidfielder` | 屏障后腰 | D（Defend） |
| OOP | `OPSplittingOutletAttackingMidfielder` | 拉开接应前腰 | A（Attack） |
| OOP | `OPSplittingOutletCentreForward` | 拉开接应中锋 | A（Attack） |
| OOP | `OPStoppingCentreBack` | 上抢中卫 | D（Defend） |
| OOP | `OPStoppingWideCentreBack` | 上抢边中卫 | D（Defend） |
| OOP | `OPSweeperKeeper` | 清道夫门将 | A（Attack） |
| OOP | `OPTrackingAttackingMidfielder` | 回防前腰 | D（Defend） |
| OOP | `OPTrackingCentreForward` | 回防中锋 | D（Defend） |
| OOP | `OPTrackingWideMidfielder` | 回防边前卫 | D（Defend） |
| OOP | `OPTrackingWinger` | 回防边锋 | D（Defend） |
| OOP | `OPWideCentreBack` | 边中卫 | D（Defend） |
| OOP | `OPWideCoverCentralMidfielder` | 边路补位中场 | S（Support） |
| OOP | `OPWideCoverDefensiveMidfielder` | 边路补位后腰 | D（Defend） |
| OOP | `OPWideMidfielder` | 边前卫 | S（Support） |
| OOP | `OPWideOutletWideMidfielder` | 边路接应前卫 | A（Attack） |
| OOP | `OPWideOutletWinger` | 拉边接应边锋 | A（Attack） |
| OOP | `OPWingBack` | 翼卫 | D（Defend） |
| OOP | `OPWinger` | 边锋 | S（Support） |

### 2.3 尚未验证职责映射：6 个

以下角色本身存在于原生角色目录，且有阶段/角色资格数据；但当前生成器没有对应的 `ROLE_DUTY` 映射：

| 阶段 | 原生角色 ID | 目录显示名 | 状态 |
|---|---|---|---|
| IP | `AdvancedCentreBack` | 前压中卫 | 待验证职责 |
| IP | `FalseNine` | 伪九号 | 待验证职责 |
| IP | `HalfBack` | 半后卫 | 待验证职责 |
| IP | `OverlappingCentreBack` | 套上中卫 | 待验证职责 |
| IP | `PlaymakingWinger` | 组织型边锋 | 待验证职责 |
| OOP | `OPCoveringWideCentreBack` | 补位边中卫 | 待验证职责 |

这 6 个项目不能因为角色定义存在，就自动补成 D、S 或 A。职责证据补齐前，生成器应继续拒绝使用它们。

## 3. 指令映射验证状态

### 3.1 个人指令（PI）

| 范围 | 数量 | 状态 |
|---|---:|---|
| 原生菜单组 | 17 组 | 已验证菜单定义 |
| 菜单选项 | 54 项 | 已验证菜单定义 |
| `PI_MAP` 写入映射 | 18 项 | 已验证明确映射的选项 |
| 原生权限策略记录 | 1,547 条 | 已验证目录及版本/状态结构 |

当前已经建立原生 option ID 的 PI 写入映射如下：

| PI 组 | 选项 | 原生 option ID |
|---|---|---:|
| `PASSING_STRATEGY` | `SHORTER` | 1 |
| `PASSING_STRATEGY` | `MORE_DIRECT` | 2 |
| `PASSING_RISKS` | `TAKE_MORE_RISKS` | 3 |
| `PASSING_RISKS` | `TAKE_FEWER_RISKS` | 4 |
| `DRIBBLING_FREQUENCY` | `DRIBBLE_MORE` | 13 |
| `DRIBBLING_FREQUENCY` | `DRIBBLE_LESS` | 14 |
| `DRIBBLING_DIRECTION` | `CUT_INSIDE_WITH_BALL` | 16 |
| `SHOOTING` | `SHOOT_MORE_OFTEN` | 18 |
| `SHOOTING` | `SHOOT_LESS_OFTEN` | 19 |
| `FORWARD_RUNS` | `MAKE_MORE_RUNS` | 22 |
| `ATTACKING_WIDTH` | `STAY_WIDER` | 25 |
| `ATTACKING_WIDTH` | `SIT_NARROWER` | 26 |
| `MARKING` | `MARK_TIGHTER` | 33 |
| `TACKLING` | `EASE_OFF_TACKLES` | 32 |
| `TRIGGER_PRESS` | `MORE_OFTEN` | 29 |
| `ATTACK_BOX_SIDE` | `CENTRE` | 36 |
| `ATTACK_BOX_SIDE` | `NEAR_POST` | 39 |
| `ATTACK_BOX_SIDE` | `FAR_POST` | 40 |

**状态：以上明确列出的 18 个 PI 选项可进入生成器的权限检查与写入路径。** 其余菜单选项即使在游戏菜单目录中存在，也不能仅凭菜单定义就视为 GEN1 已支持；必须先建立 `PI_MAP` 映射并通过对应角色/位置/阶段/职责权限检查。

### 3.2 球队指令（TI）

| 范围 | 数量 | 状态 |
|---|---:|---|
| 原生菜单组 | 29 组 | 已验证菜单定义 |
| 菜单选项 | 103 项 | 已验证菜单定义 |
| 生成器 `TI_MAP` 明确映射 | 56 项 | 已验证明确映射的选项 |

**边界：** 菜单存在、option ID 存在和生成器可写入是三个不同层级。没有 `TI_MAP` 映射的选项不得假装已支持；模板保留的 opaque bits 也不是可编辑指令。

## 4. 后续执行规则

1. 角色定义可以使用全部 79 个已验证原生角色 ID。
2. 职责只能使用已登记并有证据的映射；目前 73 个已验证，6 个保持待验证。
3. PI 只能使用 `PI_MAP` 已映射选项，并逐项通过 `pi_policies` 权限检查。
4. TI 只能使用 `TI_MAP` 已映射选项；不得猜测隐藏 bit 或把模板保留位当作自由编辑项。
5. 离线生成和二进制回读通过，仅证明序列化及当前检查项目通过；游戏内导入、保存重开和比赛效果必须分别验收。

## 5. 对应仓库证据文件

- `catalog.json`：角色原始对象、角色/位置资格、指令菜单和 PI 权限目录。
- `FM27GEN1_Offline_FMF_Generator.py`：`ROLE_DUTY`、`PI_MAP`、`TI_MAP` 与实际写入拒绝规则。
- `FM27GEN1_离线原生FMF_字段契约.md`：当前实现契约及覆盖边界。
- `FM27GEN1_Netlify90_OfficialPreset_Audit.py`：90 条预设职责/位置/PI 权限审计脚本。
- `01_网站生成规则/Netlify_90官方预设索引.csv`：90 条网站预设原始索引。
- `01_网站生成规则/Netlify_角色显示名称索引.csv`：网站角色显示名到索引的映射。
