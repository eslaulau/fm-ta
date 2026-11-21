#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, copy, hashlib, json, sys
from pathlib import Path

GEN_DIR=Path(__file__).resolve().parents[1]/"04_离线原生FMF生成器"
sys.path.insert(0,str(GEN_DIR))
import FM27GEN1_Offline_FMF_Generator as gen

# The field contract identifies these as template-owned opaque TI bits.
# They are not assigned to IP or OOP and must remain from the V14 template.
OPAQUE_TEMPLATE_BITS={33,34,74,75,76}

def sha(b): return hashlib.sha256(b).hexdigest()

def bit_is_set(vec,bit): return bool(vec[bit//8] & (1 << (bit%8)))
def set_bit(vec,bit,value):
    mask=1 << (bit%8)
    if value: vec[bit//8] |= mask
    else: vec[bit//8] &= ~mask

def set_bits(vec):
    return [i for i in range(len(vec)*8) if bit_is_set(vec,i)]

def build_phase_bitsets(catalog):
    by_phase={0:set(),1:set()}
    owners={}
    for group in catalog.get("team_instructions",[]):
        phase=int(group.get("possession_phase",-1))
        if phase not in (0,1): raise ValueError("Unsupported TI phase: "+str(group.get("id")))
        for option in group.get("options",[]):
            bit=int(option.get("native_bit") or 0)
            if not bit: continue
            if bit in owners and owners[bit]!=phase:
                raise ValueError(f"Native TI bit {bit} is assigned to both phases")
            owners[bit]=phase
            by_phase[phase].add(bit)
    overlap=by_phase[0]&by_phase[1]
    if overlap: raise ValueError("Overlapping IP/OOP TI bits: "+str(sorted(overlap)))
    return by_phase

def merge_ti(v14,b16,catalog,ip_source_label='IP source',oop_source_label='OOP source'):
    if len(v14)!=len(b16): raise ValueError("TI vector sizes differ")
    bits=build_phase_bitsets(catalog)
    out=bytearray(v14)
    for bit in bits[0]: set_bit(out,bit,bit_is_set(v14,bit))
    for bit in bits[1]: set_bit(out,bit,bit_is_set(b16,bit))
    unclassified=[]
    owned=bits[0]|bits[1]
    for bit in range(len(out)*8):
        if bit not in owned and bit_is_set(v14,bit)!=bit_is_set(b16,bit):
            unclassified.append(bit)
    report={
      "in_possession_source":ip_source_label,"out_of_possession_source":oop_source_label,
      "ip_native_bits":sorted(bits[0]),"oop_native_bits":sorted(bits[1]),
      "opaque_template_bits_retained_from_ip_template":sorted(OPAQUE_TEMPLATE_BITS),
      "opaque_template_bit_differences_retained_from_ip_template":[b for b in unclassified if b in OPAQUE_TEMPLATE_BITS],
      "unclassified_source_differences_retained_from_ip_template":unclassified,
      "ip_source_set_bits":set_bits(v14),"oop_source_set_bits":set_bits(b16),
      "merged_set_bits":set_bits(out),
      "groups":[]
    }
    for group in catalog["team_instructions"]:
        phase=int(group["possession_phase"])
        src=v14 if phase==0 else b16
        selected=[]
        for option in group.get("options",[]):
            bit=int(option.get("native_bit") or 0)
            if bit and bit_is_set(src,bit):
                selected.append({"native_bit":bit,"label":option.get("label")})
        report["groups"].append({
          "group_id":int(group["id"]),
          "label":group.get("label",group.get("name")),
          "phase":"IP" if phase==0 else "OOP",
          "source":ip_source_label if phase==0 else oop_source_label,
          "selected_non_default_options":selected
        })
    unclassified_not_template=sorted(set(unclassified)-OPAQUE_TEMPLATE_BITS)
    if unclassified_not_template:
        raise ValueError("Unclassified TI bits differ between sources and are not documented template-owned opaque bits: "+str(unclassified_not_template))
    # Verify every catalogued phase-owned bit against its source.
    for bit in bits[0]:
        if bit_is_set(out,bit)!=bit_is_set(v14,bit):
            raise ValueError(f"IP TI bit {bit} did not survive merge")
    for bit in bits[1]:
        if bit_is_set(out,bit)!=bit_is_set(b16,bit):
            raise ValueError(f"OOP TI bit {bit} did not survive merge")
    return out,report

def parse_phase_prefix(data):
    """Read the 11 native phase pairs and retain the unparsed B16 suffix for audit."""
    if len(data)<64 or data[:11]!=gen.TAC_PREFIX or data[11]!=27:
        raise ValueError("Not an FM27 source-major 27 TAC")
    p=16
    title,p=gen.lp_read(data,p)
    if data[p:p+12]!=bytes(12): raise ValueError("TAC title padding differs from expected native header")
    p+=12
    hdr=bytearray(data[p:p+6]); p+=6
    packed=bytearray(data[p:p+12]); p+=12
    if data[p]!=255: raise ValueError("Missing TAC style string marker")
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
    return {"title":title,"hdr":hdr,"packed":packed,"style":style,"quad":quad,
            "pairs":pairs,"pairs_end_offset":p,"suffix":data[p:]}

def all_cache_details(block,phase,catalog):
    rolemap={(int(x["flags"]),int(x["phase"])):x for x in catalog["roles"]}
    options={}
    for group in catalog.get("player_instructions",[]):
        for option in group.get("options",[]):
            options[int(option["id"])]={"group":group.get("label",group.get("name")),
              "option":option.get("label"),"group_id":group["id"]}
    caches=[]
    for item in block.items:
        key=int(item["key"])
        role=rolemap.get((key,phase))
        mask=int(item["mask2"])
        decoded=[]
        for bit in range(mask.bit_length()):
            if mask & (1<<bit):
                meta=options.get(bit)
                decoded.append({"native_option_id":bit,**meta} if meta else {"native_option_id":bit,"unknown":True})
        caches.append({
          "role_key_hex":hex(key),
          "role_id":role.get("id") if role else None,
          "role_label":role.get("label") if role else None,
          "mask2_hex":hex(mask),
          "value":int(item["value"]),
          "selected_pi_options":decoded
        })
    return caches

def details(block,phase,catalog):
    pos={int(x["mask"]):x["id"] for x in catalog["positions"]}
    rolemap={(int(x["flags"]),int(x["phase"])):x for x in catalog["roles"]}
    rf=block.mask & gen.ROLE_MASK
    role=rolemap.get((rf,phase))
    duty=block.mask & ~gen.ROLE_MASK
    duties={0:"NONE",2097152:"D",4194304:"S",8388608:"A"}
    caches=all_cache_details(block,phase,catalog)
    active=[x for x in caches if x["role_key_hex"]==hex(rf)]
    active_count=len(active)
    selected=[x for x in active[0]["selected_pi_options"]] if active_count==1 else []
    return {
      "position":pos.get(int(block.selector),str(block.selector)),
      "role":role["id"] if role else str(rf),
      "role_label":role.get("label") if role else None,
      "duty":duties.get(duty,"NATIVE_"+str(duty)),
      "selected_role_pi_options":selected,
      "all_role_instruction_caches":caches,
      "all_role_cache_count":len(caches),
      "active_role_cache_count":active_count
    }

def footer_diagnostic(tac):
    return {
      "id_entries":len(tac.ids),
      "id_entries_with_nested_blocks":sum(1 for e in tac.ids if e.flag),
      "id_nested_block_sha256":[sha(gen.write_block(e.block)) for e in tac.ids if e.flag],
      "footer_lists":len(tac.lists),
      "footer_list_sizes":[len(v) for _,v in tac.lists],
      "footer_records":len(tac.records),
      "end_marker":tac.end
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--request",type=Path,required=True)
    ap.add_argument("--catalog",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    a=ap.parse_args()
    req=json.loads(a.request.read_text(encoding="utf-8"))
    name=str(req.get("name") or "FM27_IP_OOP_Phase_Fusion").strip()
    cat=json.loads(a.catalog.read_text(encoding="utf-8"))
    sources=req["sources"]
    ip_label=str(sources.get("ip_source_label","IP source"))
    oop_label=str(sources.get("oop_source_label","OOP source"))
    ip_file=str(sources.get("ip_source_file","IP source.fmf"))
    oop_file=str(sources.get("oop_source_file","OOP source.fmf"))
    vb=base64.b64decode(sources["v14_fmf_base64"],validate=False)
    bb=base64.b64decode(sources["b16_fmf_base64"],validate=False)
    vf,bf=gen.parse_fmf(vb),gen.parse_fmf(bb)
    for lab,f in ((ip_label,vf),(oop_label,bf)):
        if not {".tac",".aom",".img"}.issubset(f.data_by_ext):
            raise ValueError(lab+" missing FMF members")
    vraw,braw=vf.data_by_ext[".tac"],bf.data_by_ext[".tac"]
    vt=gen.parse_tac(vraw)
    bt=parse_phase_prefix(braw)
    if vraw[11]!=27 or braw[11]!=27: raise ValueError("Not FM27 source-major 27")
    vs={p.slot:p for p in vt.pairs};bs={p.slot:p for p in bt["pairs"]}
    if set(vs)!=set(range(11)) or set(bs)!=set(range(11)):
        raise ValueError("Need slots 0..10 in both sources")
    mt=copy.deepcopy(vt);ms={p.slot:p for p in mt.pairs}
    phases=[]
    for s in range(11):
        ms[s].ip=copy.deepcopy(vs[s].ip)
        ms[s].oop=copy.deepcopy(bs[s].oop)
        phases.append({"slot":s,
          "ip":details(ms[s].ip,0,cat),"oop":details(ms[s].oop,1,cat),
          "ip_block_sha256":sha(gen.write_block(ms[s].ip)),
          "oop_block_sha256":sha(gen.write_block(ms[s].oop))})
    mt.packed,ti=merge_ti(bytes(vt.packed),bytes(bt["packed"]),cat,ip_label,oop_label)
    mt.title=name
    out=gen.write_fmf(vf,gen.write_tac(mt),name)
    rf=gen.parse_fmf(out)
    rt=gen.parse_tac(rf.data_by_ext[".tac"])
    rs={p.slot:p for p in rt.pairs}
    checks=[]
    for s in range(11):
        checks.append({"slot":s,
          "ip_exact_source":gen.write_block(rs[s].ip)==gen.write_block(vs[s].ip),
          "oop_exact_source":gen.write_block(rs[s].oop)==gen.write_block(bs[s].oop)})
    if not all(x["ip_exact_source"] and x["oop_exact_source"] for x in checks):
        raise ValueError("Exact phase-block readback failed")
    if bytes(rt.packed)!=bytes(mt.packed) or rt.title!=name or rf.root_title!=name:
        raise ValueError("Header/TI/title readback failed")
    # Verify every phase-owned TI bit against the requested source after FMF round-trip.
    phase_bits=build_phase_bitsets(cat)
    ti_readback=[]
    for bit in sorted(phase_bits[0]):
        ti_readback.append({"bit":bit,"phase":"IP","source":bit_is_set(vt.packed,bit),
                            "output":bit_is_set(rt.packed,bit),"match":bit_is_set(vt.packed,bit)==bit_is_set(rt.packed,bit)})
    for bit in sorted(phase_bits[1]):
        ti_readback.append({"bit":bit,"phase":"OOP","source":bit_is_set(bt["packed"],bit),
                            "output":bit_is_set(rt.packed,bit),"match":bit_is_set(bt["packed"],bit)==bit_is_set(rt.packed,bit)})
    if not all(x["match"] for x in ti_readback):
        raise ValueError("Phase-owned team-instruction readback failed")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(out)
    report={
      "status":"native_phase_merge_verified_not_game_import_verified",
      "name":name,"output":a.output.name,"bytes":len(out),"sha256":sha(out),
      "sources":{"ip_source":{"label":ip_label,"file":ip_file,"git_blob_sha":sources.get("ip_source_git_blob_sha"),"sha256":sha(vb),"used_for":"all 11 IP player blocks and IP TI bits"},
                 "oop_source":{"label":oop_label,"file":oop_file,"git_blob_sha":sources.get("oop_source_git_blob_sha"),"sha256":sha(bb),"used_for":"all 11 OOP player blocks and OOP TI bits"}},
      "shared_metadata_source":ip_label+" (style, mentality, native header, non-phase TAC footer and archive artwork)",
      "team_instruction_merge":ti,
      "team_instruction_bit_readback":{"checked_bits":len(ti_readback),
        "ip_bits_checked":sum(1 for x in ti_readback if x["phase"]=="IP"),
        "oop_bits_checked":sum(1 for x in ti_readback if x["phase"]=="OOP"),
        "all_match":all(x["match"] for x in ti_readback),"details":ti_readback},
      "exact_phase_copy":{"ip_blocks_from_source":sum(x["ip_exact_source"] for x in checks),
        "oop_blocks_from_source":sum(x["oop_exact_source"] for x in checks),
        "total_blocks":22,"all_exact":True},
      "source_tac_metadata":{"ip_source_footer":footer_diagnostic(vt),
        "oop_source_suffix_after_11_pairs":{"offset":bt["pairs_end_offset"],
          "length":len(bt["suffix"]),"hex":bt["suffix"].hex()}},
      "player_phase_map":phases,
      "checks":{"both_source_archives_parse":True,"both_source_tac_prefixes_parse":True,
        "11_slots_each_source":True,"all_11_ip_blocks_exact_source":True,
        "all_11_oop_blocks_exact_source":True,"all_role_cache_records_included_in_audit":True,
        "team_instruction_phase_bits_readback":True,"output_archive_and_tac_parse":True,
        "output_title_readback":True,"game_import":False,"match_engine":False},
      "notes":["All role-cache records from each copied player block are preserved; the report enumerates every cache entry, not only the selected role.",
        "All catalogued IP team-instruction bits are copied from "+ip_label+".",
        "All catalogued OOP team-instruction bits are copied from "+oop_label+"; TI remains one shared 12-byte native vector with phase-owned groups.",
        "Opaque template bits 33/34/74/75/76 are retained from the IP-source template according to the repository field contract.",
        "Unclassified raw bit differences are explicitly listed and must match the documented template-owned opaque set.",
        "The non-phase TAC footer, common native header, style, and archive artwork follow "+ip_label+".",
        "FM27 in-game import and match-engine performance are not tested."]}
    a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    try: main()
    except Exception as exc: raise SystemExit("Phase merge failed: "+type(exc).__name__+": "+str(exc)) from exc
