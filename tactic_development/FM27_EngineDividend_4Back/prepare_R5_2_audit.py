#!/usr/bin/env python3
"""Build the R5.2 exact 22-phase D0 manifest and pin source hashes."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT/"R5.2_DESIGN_AND_AUDIT.md"
RECIPE=ROOT/"R5.2.json"
def sha(path: Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def replace_line(src,label,value):
    out,n=re.subn(rf"(?m)^{re.escape(label)}：.*$",f"{label}：{value}",src)
    if n!=1: raise ValueError(f"Expected one line for {label}; found {n}")
    return out
def main():
    recipe=json.loads(RECIPE.read_text(encoding="utf-8"))
    text=AUDIT.read_text(encoding="utf-8")
    manifest={"schema_version":1,"selected_configurations":[],"retired_configurations":[]}
    explanations={
      ("IP","DCL"):"以前压中卫攻击职责制造从四后场槽位进入肋部/禁区的行为错位，检验对手中卫是否跟随及其身后空间。",
      ("IP","DL"):"以内收边后卫防守职责与右侧组织翼卫形成不对称结构，检验是否增加中路保护而不压缩左翼宽度。",
      ("IP","DR"):"组织型翼卫支援并保持更宽、指定后点传中，检验其能否持续提供高质量宽侧供给。",
      ("IP","MCL"):"肋部中场攻击职责叠加更多前插和自由跑位，检验二线跑动是否产生独立禁区机会。",
      ("IP","MCR"):"前腰攻击职责放在右中场槽并要求更多前插/自由跑位，检验名义位置与进攻通道的错位。",
      ("IP","AML"):"边锋支援职责保持自然宽度，为肋部跑动与中路前锋腾出内侧通道。",
      ("IP","AMR"):"边锋支援职责保持自然宽度，配合右侧组织翼卫形成外侧传中和内侧接应分层。",
      ("IP","ST"):"中锋进攻职责作为纵深与终结点，吸引中卫并为双肋部跑动形成间接空间。",
      ("OOP","DC"):"由IP单后腰变为OOP第三中卫，检验双阶段位置错位能否稳定形成五人后线。",
      ("OOP","DML"):"由IP左中场下沉为左后腰屏障，并提高逼抢，检验边中结合区域的压迫与回收。",
      ("OOP","DMR"):"由IP右中场下沉为右侧覆盖后腰，检验其是否弥补右后卫收回后留下的中场宽侧空隙。",
      ("OOP","AMC"):"由IP中锋转换为前腰压迫点，制造前场角色与名义位置错位；检验是否仍可接应快速反击。"
    }
    for slot in recipe["p"]:
      for phase,key in (("IP","in"),("OOP","out")):
        item=slot[key]; pos=item["pos"]; role=item["role"]; duty=item["duty"]; pi=item.get("pi",[])
        why=explanations.get((phase,pos),f"{phase}/{pos} {role} 的角色与职责仅作为新配置假设；无本队D5槽位级准入证据。")
        manifest["selected_configurations"].append({
          "phase":phase,"pos":pos,"role":role,"duty":duty,"pi":pi,
          "decision":"新增待验证","evidence_grade":"U",
          "rationale":why,
          "hypothesis":f"{why} 当前为待证伪假设，不视为已观察到的引擎事实。",
          "d5_metric":"完整38场联赛的团队PPG、团队xG；若Exporter支持可靠映射，再观察本槽位xG/90、xA/90、禁区触球、压迫/覆盖过程。",
          "failure_condition":"如果没有可归因数据则不作槽位准入；若全队xG<100或积分<109则整套战术D5失败。"
        })
    if len(manifest["selected_configurations"])!=22: raise ValueError("Expected exactly 22 phase entries")
    start="MACHINE_DECISION_MANIFEST_JSON_START"; end="MACHINE_DECISION_MANIFEST_JSON_END"
    a=text.find(start); b=text.find(end)
    if a<0 or b<a: raise ValueError("Missing manifest markers")
    text=text[:a+len(start)]+"\n"+json.dumps(manifest,ensure_ascii=False,indent=2)+"\n"+text[b:]
    inputs={
      "本轮配方 SHA-256":RECIPE,
      "项目规则 SHA-256":ROOT/"PROJECT_RULES.md",
      "决策总账 SHA-256":ROOT/"TACTIC_INSTRUCTION_DECISION_LEDGER.md",
      "PPG 策略 SHA-256":ROOT/"PPG_TARGET_POLICY.json",
      "位置绩效标准 SHA-256":ROOT/"POSITION_PERFORMANCE_ELIMINATION_STANDARD.md"
    }
    for label,path in inputs.items(): text=replace_line(text,label,sha(path))
    AUDIT.write_text(text,encoding="utf-8")
    print("R5.2 D0 manifest and source hashes refreshed")
if __name__=="__main__": main()
