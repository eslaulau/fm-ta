#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
audit=p/"R5.1_DESIGN_AND_AUDIT.md"
recipe=p/"R5.1.json"
text=audit.read_text(encoding="utf-8")
manifest={"schema_version":1,"selected_configurations":[],"retired_configurations":[]}
r=json.loads(recipe.read_text(encoding="utf-8"))
for slot in r["p"]:
  for phase,key in (("IP","in"),("OOP","out")):
    x=slot[key]
    rationale=f"{phase}/{x['pos']} 本轮全新组合，无本队D5槽位级准入证据；仅作为可证伪的新假设。"
    manifest["selected_configurations"].append({
      "phase":phase,"pos":x["pos"],"role":x["role"],"duty":x["duty"],"pi":x["pi"],
      "decision":"新增待验证","evidence_grade":"U","rationale":rationale,
      "hypothesis":f"{phase}/{x['pos']} {x['role']} {x['duty']} 的行为将与相邻槽位形成新的阶段分工；当前仅为假设。",
      "d5_metric":"完整38场报告中该槽位可归因的职责过程指标；同时全队xG和PPG。",
      "failure_condition":"无法归因或职责过程无改善则不准入；全队xG<100或积分<109则整套战术D5失败。"
    })
manifest_text=json.dumps(manifest,ensure_ascii=False,indent=2)
text=text.replace("__MANIFEST__",manifest_text)
for token,path in [
("__RECIPE_SHA__",recipe),
("__RULES_SHA__",p/"PROJECT_RULES.md"),
("__LEDGER_SHA__",p/"TACTIC_INSTRUCTION_DECISION_LEDGER.md"),
("__POLICY_SHA__",p/"PPG_TARGET_POLICY.json"),
("__POSITION_SHA__",p/"POSITION_PERFORMANCE_ELIMINATION_STANDARD.md")]:
  text=text.replace(token,hashlib.sha256(path.read_bytes()).hexdigest())
audit.write_text(text,encoding="utf-8")
print("R5.1 audit pinned; manifest entries:",len(manifest["selected_configurations"]))
