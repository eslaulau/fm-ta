#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, copy, hashlib, json, sys
from pathlib import Path
GEN_DIR=Path(__file__).resolve().parents[1]/"04_离线原生FMF生成器"
sys.path.insert(0,str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen

def sha(b): return hashlib.sha256(b).hexdigest()

def details(block, phase, catalog):
    pos={int(x["mask"]):x["id"] for x in catalog["positions"]}
    rolemap={(int(x["flags"]),int(x["phase"])):x for x in catalog["roles"]}
    rf=block.mask & gen.ROLE_MASK
    role=rolemap.get((rf,phase))
    duty=block.mask & ~gen.ROLE_MASK
    active=[x for x in block.items if int(x["key"])==rf]
    pim=int(active[0]["mask2"]) if len(active)==1 else None
    options={}
    for g in catalog.get("player_instructions",[]):
        for o in g.get("options",[]):
            options[int(o["id"])]={"group":g.get("label",g.get("name")),"option":o.get("label"),"group_id":g["id"]}
    decoded=[];unknown=[]
    if pim is not None:
        for bit in range(pim.bit_length()):
            if pim & (1<<bit):
                (decoded if bit in options else unknown).append({"native_option_id":bit,**options[bit]} if bit in options else bit)
    duties={0:"NONE",2097152:"D",4194304:"S",8388608:"A"}
    return {"position":pos.get(int(block.selector),str(block.selector)),
            "role":role["id"] if role else str(rf),
            "role_label":role.get("label") if role else None,
            "duty":duties.get(duty,"NATIVE_"+str(duty)),
            "pi_mask":hex(pim) if pim is not None else None,
            "pi_cache_entries_for_active_role":len(active),
            "pi_options":decoded,"unknown_pi_option_bits":unknown,
            "cached_role_instruction_entries":len(block.items)}

def parse_phase_prefix(data):
    """Read FM27's 11 native phase pairs without assuming a shared footer format."""
    if len(data)<64 or data[:11]!=gen.TAC_PREFIX or data[11]!=27:
        raise ValueError("Not an FM27 source-major 27 TAC")
    p=16
    title,p=gen.lp_read(data,p)
    if data[p:p+12]!=bytes(12):
        raise ValueError("TAC title padding differs from expected native header")
    p+=12
    hdr=bytearray(data[p:p+6]); p+=6
    packed=bytearray(data[p:p+12]); p+=12
    if data[p]!=255:
        raise ValueError("Missing TAC style string marker")
    p+=1
    style,p=gen.lp_read(data,p)
    quad=bytearray(data[p:p+4]); p+=4
    pairs=[]
    while len(pairs)<11 and data[p:p+3]==gen.BLOCK_MARK:
        ip,p=gen.parse_block(data,p)
        oop,p=gen.parse_block(data,p)
        slot=data[p]; p+=1
        pairs.append(gen.Pair(slot,ip,oop))
    if len(pairs)!=11 or sorted(x.slot for x in pairs)!=list(range(11)):
        raise ValueError("Source TAC does not contain exactly 11 valid native phase pairs")
    return {"title":title,"hdr":hdr,"packed":packed,"style":style,"quad":quad,"pairs":pairs}


def merge_ti(v14,b16,catalog):
    if len(v14)!=len(b16): raise ValueError("TI vector sizes differ")
    out=bytearray(v14); rows=[]
    for group in catalog["team_instructions"]:
        phase=int(group.get("possession_phase",-1))
        if phase not in (0,1): raise ValueError("Unsupported possession phase for TI group "+str(group.get("id")))
        src=v14 if phase==0 else b16
        if phase==1:
            for o in group["options"]:
                bit=int(o.get("native_bit") or 0)
                if bit: out[bit//8]&=~(1<<(bit%8))
        selected=[]
        for o in group["options"]:
            bit=int(o.get("native_bit") or 0)
            if bit and (src[bit//8]&(1<<(bit%8))):
                if phase==1: out[bit//8]|=1<<(bit%8)
                selected.append({"native_bit":bit,"label":o.get("label")})
        rows.append({"group_id":int(group["id"]),"label":group.get("label",group.get("name")),
                     "phase":"IP" if phase==0 else "OOP","source":"V14" if phase==0 else "B16",
                     "selected_non_default_options":selected})
    return out,{"in_possession_from":"V14","out_of_possession_from":"B16","groups":rows}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--request",type=Path,required=True)
    ap.add_argument("--catalog",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    a=ap.parse_args()
    req=json.loads(a.request.read_text(encoding="utf-8"))
    name=str(req.get("name") or "V14_IP_B16_OOP_Exact_Merge").strip()
    cat=json.loads(a.catalog.read_text(encoding="utf-8"))
    vb=base64.b64decode(req["sources"]["v14_fmf_base64"],validate=False)
    bb=base64.b64decode(req["sources"]["b16_fmf_base64"],validate=False)
    vf,bf=gen.parse_fmf(vb),gen.parse_fmf(bb)
    for lab,f in (("V14",vf),("B16",bf)):
        if not {".tac",".aom",".img"}.issubset(f.data_by_ext): raise ValueError(lab+" missing FMF members")
    vraw,braw=vf.data_by_ext[".tac"],bf.data_by_ext[".tac"]
    vt=gen.parse_tac(vraw)
    bt=parse_phase_prefix(braw)
    if vf.data_by_ext[".tac"][11]!=27 or bf.data_by_ext[".tac"][11]!=27: raise ValueError("Not FM27 source-major 27")
    vs={p.slot:p for p in vt.pairs};bs={p.slot:p for p in bt["pairs"]}
    if set(vs)!=set(range(11)) or set(bs)!=set(range(11)): raise ValueError("Need slots 0..10 in both files")
    mt=copy.deepcopy(vt);ms={p.slot:p for p in mt.pairs}
    phases=[]
    for s in range(11):
        ms[s].ip=copy.deepcopy(vs[s].ip);ms[s].oop=copy.deepcopy(bs[s].oop)
        phases.append({"slot":s,"ip":details(ms[s].ip,0,cat),"oop":details(ms[s].oop,1,cat),
                       "ip_block_sha256":sha(gen.write_block(ms[s].ip)),
                       "oop_block_sha256":sha(gen.write_block(ms[s].oop))})
    mt.packed,ti=merge_ti(bytes(vt.packed),bytes(bt["packed"]),cat)
    mt.title=name
    out=gen.write_fmf(vf,gen.write_tac(mt),name)
    rf=gen.parse_fmf(out);rt=gen.parse_tac(rf.data_by_ext[".tac"]);rs={p.slot:p for p in rt.pairs}
    checks=[]
    for s in range(11):
        checks.append({"slot":s,
          "ip_exact_v14":gen.write_block(rs[s].ip)==gen.write_block(vs[s].ip),
          "oop_exact_b16":gen.write_block(rs[s].oop)==gen.write_block(bs[s].oop)})
    if not all(x["ip_exact_v14"] and x["oop_exact_b16"] for x in checks): raise ValueError("Exact phase-block readback failed")
    if bytes(rt.packed)!=bytes(mt.packed) or rt.title!=name or rf.root_title!=name: raise ValueError("Header/TI/title readback failed")
    a.output.parent.mkdir(parents=True,exist_ok=True);a.report.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(out)
    report={"status":"native_phase_merge_exact_blocks_verified_not_game_import_verified",
      "name":name,"output":a.output.name,"bytes":len(out),"sha256":sha(out),
      "sources":{"v14":{"file":"v14.fmf","sha256":sha(vb),"used_for":"all 11 IP player blocks"},
                 "b16":{"file":"B16.fmf","sha256":sha(bb),"used_for":"all 11 OOP player blocks"}},
      "shared_metadata_source":"V14 (style, mentality, native header)",
      "team_instruction_merge":ti,
      "exact_phase_copy":{"ip_blocks_from_v14":sum(x["ip_exact_v14"] for x in checks),
                          "oop_blocks_from_b16":sum(x["oop_exact_b16"] for x in checks),
                          "total_blocks":22,"all_exact":True},
      "player_phase_map":phases,
      "checks":{"both_source_archives_parse":True,"both_source_tac_parse":True,
        "11_slots_each_source":True,"11_ip_blocks_exact_v14":True,"11_oop_blocks_exact_b16":True,
        "team_instruction_phase_merge_readback":True,"output_archive_and_tac_parse":True,
        "output_title_readback":True,"game_import":False,"match_engine":False},
      "notes":["All V14 IP blocks and B16 OOP blocks copied natively without reconstructing roles or PI.",
        "IP team instruction groups are from V14; OOP groups are from B16.",
        "Shared style, mentality and native header follow V14.",
        "Opaque/unmapped TI bits are retained from V14.",
        "FM27 in-game import and match performance are not tested."]}
    a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    try: main()
    except Exception as exc: raise SystemExit("Phase merge failed: "+type(exc).__name__+": "+str(exc)) from exc
