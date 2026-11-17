FM27GEN1 离线原生 FMF 生成器说明

【当前版本说明】
本文件曾记录早期原型，仅支持 Gegenpress 的限制已经过期。当前分支已接入十种原生风格，请以同目录 README.md、FM27GEN1_离线原生FMF_字段契约.md 和上级 00_资料总索引与检索规范.md 为准。
不得再引用本历史说明中的“仅支持 Gegenpress”或“生成器未检查 PI 权限”作为当前源码结论。

当前资料入口：
../00_资料总索引与检索规范.md
README.md
FM27GEN1_离线原生FMF_字段契约.md

当前实际风格、FourCC 与模板路径以 style_template_registry.json 为准。
当前 PI 权限检查以 catalog.json 的 pi_policies 和源码 encode_pi() 为准。
当前 TI 写入映射以源码 TI_GROUPS / TI_MAP 为准。
当前角色职责以源码 ROLE_DUTY 为准。
所有未映射值均拒绝猜测，不会静默写入。

【验收边界】
十风格离线生成回读，不等于 FM27 客户端导入、保存重开或比赛实测通过。
