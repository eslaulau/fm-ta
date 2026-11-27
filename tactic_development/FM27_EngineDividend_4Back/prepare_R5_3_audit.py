#!/usr/bin/env python3
"""Pin R5.3 audit hashes and write the exact 22-phase machine decision manifest."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
AUDIT=ROOT/"R5.3_DESIGN_AND_AUDIT.md"
RECIPE=ROOT/"R5.3.json"

def sha(path: Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replace_line(src,label,value):
    out,n=re.subn(rf"(?m)^{re.escape(label)}：.*$",f"{label}：{value}",src)
    if n!=1:
        raise ValueError(f"Expected exactly one line for {label}; found {n}")
    return out

RATIONALE={
 "IP/GK":"门将由有球门将防守切换为无球清道夫门将进攻，测试角色切换对较高防线身后覆盖的影响。",
 "IP/DR":"右侧组织型翼卫以支援职责保持外侧宽度，并通过底线低平传中及后点目标给前五人供球。",
 "IP/DCR":"右中卫保持出球中卫防守职责，为双翼卫前移时提供稳定的四后场基础。",
 "IP/DCL":"左中卫保持出球中卫防守职责，与右侧构成对称中卫平台，避免前压中卫扰乱四后场。",
 "IP/DL":"左侧组织型翼卫以支援职责保持外侧宽度，并通过底线低平传中及后点目标给前五人供球。",
 "IP/DMC":"单后腰留在四后场之前承担保护与第一连接，失去球权后下降为第三中卫。",
 "IP/AMCL":"左肋部中场攻击职责配合更多前插、自由跑位和晚插禁区，形成双攻击中场中的动态跑动点。",
 "IP/AMCR":"右侧影子前锋攻击职责自由移动并进入肋部，和左侧肋部中场形成不同跑动路线。",
 "IP/STL":"左侧拉边前锋攻击职责从内侧前场槽攻击对方后卫线，为双翼卫外侧推进腾出宽度。",
 "IP/ST":"中锋攻击职责配合护球，作为前场第一落点并为双攻击中场/拉边前锋做球。",
 "IP/STR":"右侧拉边前锋攻击职责从内侧前场槽攻击对方后卫线，和左侧形成双侧纵深威胁。",
 "OOP/GK":"无球阶段切换清道夫门将进攻职责，作为较高防线后的补位假设；当前没有比赛验证。",
 "OOP/DR":"右侧逼抢边后卫支援职责承担外线接近与压迫，凶狠铲抢只在原生PI权限可用时启用。",
 "OOP/DCR":"右中卫较少主动离开保护区，个人逼抢较少并使用凶狠铲抢，兼顾纵深防守和对抗。",
 "OOP/DCL":"左中卫较少主动离开保护区，个人逼抢较少并使用凶狠铲抢，兼顾纵深防守和对抗。",
 "OOP/DL":"左侧逼抢边后卫支援职责承担外线接近与压迫，凶狠铲抢只在原生PI权限可用时启用。",
 "OOP/DC":"IP单后腰转为OOP补位中卫，填充五后卫中路并保护两名外侧中卫身后的空间。",
 "OOP/DML":"左侧防守中场在无球阶段提高触发逼抢并使用凶狠铲抢，争取夺回第二点和中路球权。",
 "OOP/DMR":"右侧防守中场在无球阶段提高触发逼抢并使用凶狠铲抢，争取夺回第二点和中路球权。",
 "OOP/AML":"左边锋无球阶段留在前场线并提高触发逼抢，以三人前场线限制对手出球。",
 "OOP/AMC":"前腰无球阶段留在前场中路并提高触发逼抢，压迫对方后腰与中卫之间的传球线。",
 "OOP/AMR":"右边锋无球阶段留在前场线并提高触发逼抢，以三人前场线限制对手出球。"
}

def main():
    recipe=json.loads(RECIPE.read_text(encoding="utf-8"))
    src=AUDIT.read_text(encoding="utf-8")
    manifest={"schema_version":1,"selected_configurations":[],"retired_configurations":[]}
    for slot in recipe["p"]:
        for phase,key in (("IP","in"),("OOP","out")):
            item=slot[key]
            identity=f"{phase}/{item['pos']}"
            rationale=RATIONALE.get(identity,
                f"{identity} {item['role']}/{item['duty']}是本轮新配置，必须通过完整38场数据检验，不将角色名称或外部样本当作有效证据。")
            manifest["selected_configurations"].append({
                "phase":phase,"pos":item["pos"],"role":item["role"],"duty":item["duty"],"pi":item.get("pi",[]),
                "decision":"新增待验证","evidence_grade":"U","rationale":rationale,
                "hypothesis":rationale+" 该机制链是可证伪假设，不表示已观察到比赛中的因果行为。",
                "d5_metric":"完整38场球队积分/PPG、团队xG；可归因时补充该槽xG/90、xA/90、禁区触球、射门质量或对手对应侧威胁。",
                "failure_condition":"证据覆盖不足则不准入；完整38场积分低于109或球队xG低于100，整套战术D5失败。"
            })
    if len(manifest["selected_configurations"])!=22:
        raise ValueError("R5.3 manifest must contain 22 phase entries")
    start="MACHINE_DECISION_MANIFEST_JSON_START"
    end="MACHINE_DECISION_MANIFEST_JSON_END"
    a=src.find(start); b=src.find(end)
    if a<0 or b<a:
        raise ValueError("Missing machine manifest markers")
    src=src[:a+len(start)]+"\n"+json.dumps(manifest,ensure_ascii=False,indent=2)+"\n"+src[b:]
    inputs={
        "本轮配方 SHA-256":RECIPE,
        "项目规则 SHA-256":ROOT/"PROJECT_RULES.md",
        "决策总账 SHA-256":ROOT/"TACTIC_INSTRUCTION_DECISION_LEDGER.md",
        "PPG 策略 SHA-256":ROOT/"PPG_TARGET_POLICY.json",
        "位置绩效标准 SHA-256":ROOT/"POSITION_PERFORMANCE_ELIMINATION_STANDARD.md"
    }
    for label,path in inputs.items():
        src=replace_line(src,label,sha(path))
    AUDIT.write_text(src,encoding="utf-8")
    print("R5.3 manifest: 22/22; project source hashes pinned.")

if __name__=="__main__":
    main()
