#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT/"R6_DESIGN_AND_AUDIT.md"
RECIPE=ROOT/"R6.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def setline(src,label,value):
    src,n=re.subn(rf"(?m)^{re.escape(label)}：.*$",f"{label}：{value}",src)
    if n!=1: raise ValueError(f"Expected one line for {label}, got {n}")
    return src
def main():
    recipe=json.loads(RECIPE.read_text(encoding="utf-8"))
    src=AUDIT.read_text(encoding="utf-8")
    entries=[]
    for slot in recipe["p"]:
        for phase,key in (("IP","in"),("OOP","out")):
            x=slot[key]
            identity=f"{phase}/{x['pos']}"
            rationale=f"{identity} {x['role']}/{x['duty']}作为R6双后腰盒式结构的一部分；没有R6比赛样本，先列为U级待验证。"
            entries.append({
                "phase":phase,"pos":x["pos"],"role":x["role"],"duty":x["duty"],"pi":x.get("pi",[]),
                "decision":"新增待验证","evidence_grade":"U","rationale":rationale,
                "hypothesis":rationale+" 预期作用必须由比赛行为与完整赛季数据证伪或确认。",
                "d5_metric":"完整38场积分/PPG、全队xG/xGA；位置可归因时记录xG/90、xA/90、禁区触球和对手对应区域机会。",
                "failure_condition":"完整38场低于109分或全队xG低于100，整套战术D5失败；可归因位置持续低效则替换。"
            })
    if len(entries)!=22: raise ValueError(f"Expected 22 phase entries, got {len(entries)}")
    start="MACHINE_DECISION_MANIFEST_JSON_START"; end="MACHINE_DECISION_MANIFEST_JSON_END"
    a=src.find(start); b=src.find(end)
    if a<0 or b<a: raise ValueError("Machine manifest markers missing")
    manifest={"schema_version":1,"selected_configurations":entries,"retired_configurations":[]}
    src=src[:a+len(start)]+"\n"+json.dumps(manifest,ensure_ascii=False,indent=2)+"\n"+src[b:]
    files=[
      ("本轮配方 SHA-256",RECIPE),
      ("项目规则 SHA-256",ROOT/"PROJECT_RULES.md"),
      ("决策总账 SHA-256",ROOT/"TACTIC_INSTRUCTION_DECISION_LEDGER.md"),
      ("PPG 策略 SHA-256",ROOT/"PPG_TARGET_POLICY.json"),
      ("位置绩效标准 SHA-256",ROOT/"POSITION_PERFORMANCE_ELIMINATION_STANDARD.md")
    ]
    for label,p in files: src=setline(src,label,sha(p))
    src=AUDIT.write_text(src,encoding="utf-8")
    print(f"R6 audit prepared: {len(entries)}/22 manifest; recipe sha={sha(RECIPE)}")
if __name__=="__main__": main()
