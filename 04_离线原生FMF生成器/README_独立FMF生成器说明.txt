FM27GEN1 离线 FMF 生成器 · 原型说明
====================================

用途
----
将 FM27GEN1 v1 TXT 配方转换为 FM27 source-major 27 的原生 FMF。
程序直接解析本地 FMF 模板并重建 TAC 与 FMF 封装。
仅使用本地 GEN1 配方和 FMF 模板，不调用在线服务，
不连接或修改正在运行的 Football Manager 进程。

本目录文件
----------
FM27GEN1_Offline_FMF_Generator.py       生成器源码
catalog.json                            原生目录资料
FM27_4231_Gegenpress_Template.fmf       BAT 默认原生模板
123_Game_Export_Reference.fmf           原生导出参考
FM27_A9.0.2_GEN1.txt                    A9.0.2 输入样本
FM27_A9.0.2_Offline_Rebuild.fmf         A9.0.2 输出样本
FM27_A9.0.2_Offline_Rebuild.report.json 离线回读报告
requirements.txt                        依赖
安装依赖.bat / 运行离线生成器.bat       Windows 运行入口

当前实现范围
------------
1. GEN1 v1、11 个球员槽位，每个槽位有 in/out 两个阶段。
2. 仅支持 Gegenpress 风格映射。
3. 要求 FM27 source-major 27 原生模板，含 .tac/.aom/.img。
4. 角色按 catalog 和 role/position/phase eligibility 检查。
5. duty 由源码 ROLE_DUTY 固定映射，不是 GEN1 独立输入字段。
6. PI/TI 使用源码有限白名单；未知值报错停止。
7. OOP 的 STC 会在写入 native position selector 时规范化为 ST。
8. TI 使用单一 12 字节向量；未在 GEN1 中出现的 TI key 会保留模板 bits。

A9.0.2 样本
------------
随附报告记录：
- FMF 外层、成员解密/解压和 TAC 结构独立回读通过；
- 11 个 IP/OOP pair；
- 22 个阶段位置、角色、PI mask 与配方相符；
- 球队指令向量回读一致。

输出大小：3,588 bytes
SHA256：
c2ac1719f202d00b1a058e44da0c241e0f72b10bcdc3a04c89b295ed73029d10

此后用户已确认该 A9.0.2 文件在 FM27 内成功载入阵型。
原始 JSON 报告中的 game_interactive_import=false 和 match_engine=false
是程序生成报告时的机器验证状态，不能代替游戏内逐项验收或比赛效果测试。

安装与运行
----------
1. 安装 Python 3.12 x64。
2. 双击“安装依赖.bat”，或运行：
   py -3.12 -m pip install -r requirements.txt
3. 双击“运行离线生成器.bat”使用内置样本；
   或将另一份 GEN1 TXT 拖到 BAT 上。

手动命令：
py -3.12 FM27GEN1_Offline_FMF_Generator.py "FM27_A9.0.2_GEN1.txt" --template "FM27_4231_Gegenpress_Template.fmf" --catalog "catalog.json" --output "FM27_A9.0.2_Offline.fmf" --report "FM27_A9.0.2_Offline.report.json"

--template、--catalog、--output 必填；--report 可选。
输出文件已存在时拒绝覆盖。省略 --report 时默认生成同名 .report.json。

重要边界
--------
当前源码未执行完整逐位置/角色/duty PI 权限矩阵的自动预检。
catalog 有更多 PI 元数据，但当前脚本的 PI 写入依赖固定 PI_MAP 白名单；
不能把 PI mask 回读成功称为完整原生 PI 权限验证。
