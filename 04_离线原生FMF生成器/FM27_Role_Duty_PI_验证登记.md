# FM27 角色、职责与指令原生数据验证登记

> 登记日期：2026-11-18  
> 对应分支：`main`  
> 证据基线：当前 `catalog.json`、`FM27GEN1_Offline_FMF_Generator.py`、90 条预设索引及仓库审计逻辑。  
> **本登记将原生目录中的角色、职责数据、PI/TI 菜单与选项全部列为“已验证”；游戏内是否导入不是这些数据项的验证前提。**“原生数据已验证”表示其定义、标识和来源有原生资源证据；它不自动表示当前 GEN1 生成器已为每个选项建立写入映射，也不表示某套战术的效果已验证。生成器写入覆盖与具体战术的游戏表现分别记录，不得混为一谈。

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

### 2.2 职责数据：原生职责值目录已验证；角色职责写入映射覆盖 73/79

以下 73 个角色在当前 `ROLE_DUTY` 中有明确映射，并且被 90 条预设索引中的对应分配覆盖、通过职责一致性审计。**这 73 项是当前生成器已有的角色→职责写入映射覆盖量，不是“原生职责数据已验证”的总量；原生职责值目录本身 7/7 已验证。**

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

### 2.3 当前缺少角色→职责写入映射的 6 个角色（角色原生数据仍为已验证）

以下角色本身存在于原生角色目录，且有阶段/角色资格数据；但当前生成器没有对应的 `ROLE_DUTY` 映射：

| 阶段 | 原生角色 ID | 目录显示名 | 状态 |
|---|---|---|---|
| IP | `AdvancedCentreBack` | 前压中卫 | 角色原生数据已验证；`ROLE_DUTY` 映射未登记 |
| IP | `FalseNine` | 伪九号 | 角色原生数据已验证；`ROLE_DUTY` 映射未登记 |
| IP | `HalfBack` | 半后卫 | 角色原生数据已验证；`ROLE_DUTY` 映射未登记 |
| IP | `OverlappingCentreBack` | 套上中卫 | 角色原生数据已验证；`ROLE_DUTY` 映射未登记 |
| IP | `PlaymakingWinger` | 组织型边锋 | 角色原生数据已验证；`ROLE_DUTY` 映射未登记 |
| OOP | `OPCoveringWideCentreBack` | 补位边中卫 | 角色原生数据已验证；`ROLE_DUTY` 映射未登记 |

这 6 个角色的原生角色定义、内部 ID、阶段归属和目录资格均属于已验证数据；当前缺口仅是生成器 `ROLE_DUTY` 没有对应的角色→职责写入映射。不能仅凭角色名称擅自补成 D、S 或 A，因此当前生成器仍会拒绝把它们写入战术。这里的“映射缺口”不撤销其原生角色数据的已验证状态。

## 3. 指令映射验证状态

### 3.1 个人指令（PI）

| 范围 | 数量 | 状态 |
|---|---:|---|
| 原生菜单组 | 17 组 | **17/17 已验证** |
| 菜单选项 | 54 项 | **54/54 已验证** |
| `PI_MAP` 写入映射 | 18 项 | 18 项写入映射已验证（当前生成器覆盖量） |
| 原生权限策略记录 | 1,547 条 | 1,547 条目录及版本/状态结构已验证 |

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

**状态：17 组菜单、54 个选项的原生定义全部已验证。** 其中 18 个选项已经建立 `PI_MAP` 写入映射，可进入生成器权限检查与写入路径；其余 36 个选项的数据定义同样已验证，但当前 GEN1 生成器尚未建立对应写入映射，因此不能称为“当前生成器可写入”。

### 3.2 球队指令（TI）

| 范围 | 数量 | 状态 |
|---|---:|---|
| 原生菜单组 | 29 组 | **29/29 已验证** |
| 菜单选项 | 103 项 | **103/103 已验证** |
| 生成器 `TI_MAP` 明确映射 | 56 项 | 56 项写入映射已验证（当前生成器覆盖量） |

**状态：29 组菜单、103 个选项的原生定义全部已验证。** 其中 56 个选项已经建立 `TI_MAP` 写入映射；其余 47 个选项的数据定义仍然是已验证的，只是当前 GEN1 生成器尚未建立对应写入映射。模板保留的 opaque bits 不属于可编辑指令。

## 4. 后续执行规则

1. 原生角色定义 79/79 已验证；全部 79 个内部角色 ID、阶段归属和原生角色条目均可作为已验证数据使用。
2. 原生职责标志目录 7/7 已验证。当前生成器已登记 73 个角色→职责写入映射；另外 6 个角色的数据定义仍已验证，但生成器尚无对应映射，不得猜测 D/S/A。
3. 原生 PI 菜单 17/17 组、54/54 选项全部已验证；当前生成器仅对 `PI_MAP` 中的 18 个选项开放写入，并逐项通过 `pi_policies` 权限检查。
4. 原生 TI 菜单 29/29 组、103/103 选项全部已验证；当前生成器仅对 `TI_MAP` 中的 56 个选项开放写入，不得猜测隐藏 bit 或把模板保留位当作自由编辑项。
5. 上述原生数据验证不要求 FM27 客户端导入。离线生成/回读、游戏内导入和比赛效果是独立验收事项，不改变本登记中的原生数据验证状态。

## 5. 对应仓库证据文件

- `catalog.json`：角色原始对象、角色/位置资格、指令菜单和 PI 权限目录。
- `FM27GEN1_Offline_FMF_Generator.py`：`ROLE_DUTY`、`PI_MAP`、`TI_MAP` 与实际写入拒绝规则。
- `FM27GEN1_离线原生FMF_字段契约.md`：当前实现契约及覆盖边界。
- `FM27GEN1_Netlify90_OfficialPreset_Audit.py`：90 条预设职责/位置/PI 权限审计脚本。
- `01_网站生成规则/Netlify_90官方预设索引.csv`：90 条网站预设原始索引。
- `01_网站生成规则/Netlify_角色显示名称索引.csv`：网站角色显示名到索引的映射。


## 2026-11-26 源码复核更正：TI/PI 映射覆盖率

本节以当前 `FM27GEN1_Offline_FMF_Generator.py` 的 `TI_MAP`（含 `EXPERIMENTAL_TI_MAP` 扩展）和 `PI_MAP`（含 `EXPERIMENTAL_PI_MAP` 扩展）对照 `catalog.json` 的非默认选项 ID/native_bit 重新核验，覆盖率数字取代本文件前文的 56/18 旧数字。

| 范围 | 原生目录总量 | 非默认选项 | 当前源码映射 | 结论 |
|---|---:|---:|---:|---|
| TI | 29 组 / 103 选项 | 75 | **75/75** | 所有非默认 native_bit 均有源码映射 |
| PI | 17 组 / 54 选项 | 37 | **37/37** | 所有非默认 option ID 均有源码映射 |

说明：目录中值为 0 的标准/默认选项不要求额外映射。这里的“映射覆盖”仅指源码有编码映射，不代表所有指令组合均经过比赛验证。实验映射此前已确认可在游戏界面显示，但其比赛行为仍须独立测试。

另经复核，`raw_roles[].m_rolePlayerInstructions[]` 当前共有 36 个角色、41 条 GameID 默认行为引用。仓库未包含可将这些 GameID 解码为可读指令文本的本地化字典；不能将其猜测为 PI 名称。详见 [角色默认行为与指令映射复核](../tactic_development/FM27_EngineDividend_4Back/ROLE_DEFAULT_BEHAVIOR_AND_MAPPING_RECHECK_20261126.md)。
