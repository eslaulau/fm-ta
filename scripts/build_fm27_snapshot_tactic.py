from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "04_离线原生FMF生成器" / "FM27GEN1_Offline_FMF_Generator.py"
CATALOG = ROOT / "04_离线原生FMF生成器" / "catalog.json"

def load_gen():
    spec = importlib.util.spec_from_file_location("fm27_snapshot_native_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load native generator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def sha(data):
    return hashlib.sha256(data).hexdigest()

def decode(block, phase, catalog):
    positions = {int(x["mask"]): x["id"] for x in catalog["positions"]}
    pos = positions.get(int(block.selector))
    if pos is None:
        raise ValueError("Unknown selector " + str(block.selector))
    roles = []
    for role in catalog["roles"]:
        flag = int(role["flags"])
        if int(role["phase"]) == phase and flag > 0 and (int(block.mask) & flag) == flag:
            roles.append(role)
    if len(roles) != 1:
        raise ValueError("Cannot resolve unique role at " + pos)
    role = roles[0]
    duty = int(block.mask) ^ int(role["flags"])
    if duty not in (0,2097152,4194304,8388608,33554432,67108864,17179869184):
        raise ValueError("Unknown duty " + str(duty))
    eligibility = catalog.get("role_eligibility", {}).get(pos)
    if not eligibility or role["id"] not in eligibility[phase]:
        raise ValueError("Role eligibility failed at " + pos + "/" + role["id"])
    return {"position":pos,"role":role["id"],"role_flag":int(role["flags"]),"duty":duty}

def block_for(pair, phase):
    return pair.ip if phase == 0 else pair.oop

def verify_parent_change(gen, block, change, catalog, roles):
    phase = 0 if change["phase"].upper() == "IP" else 1
    old = change["old"]
    actual = decode(block, phase, catalog)
    pos = gen.native_position_id(change["position"], phase)
    role = gen.role_id_from_display(old["role"], phase, set(roles))
    duty = gen.resolve_role_duty(role, {"duty":old["duty"]})
    if actual["position"] != pos or actual["role"] != role or actual["duty"] != duty:
        raise ValueError("Parent position/role/duty mismatch at slot " + str(change["slot"]))
    expected = gen.encode_pi(old["pi"], catalog, phase, pos, role, duty)
    entries = [x for x in block.items if int(x["key"]) == int(roles[role]["flags"])]
    if len(entries) != 1 or int(entries[0]["mask2"]) != expected:
        raise ValueError("Parent PI mismatch at slot " + str(change["slot"]))

def build(request_path, output_path, report_path):
    gen = load_gen()
    req = json.loads(request_path.read_text(encoding="utf-8"))
    parent_path = ROOT / req["parent_file"]
    parent_bytes = parent_path.read_bytes()
    parent_hash = sha(parent_bytes)
    if parent_hash.lower() != req["parent_sha256"].lower():
        raise ValueError("Parent SHA256 mismatch: " + parent_hash)
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    source = gen.parse_fmf(parent_bytes)
    for ext in (".tac",".aom",".img"):
        if ext not in source.data_by_ext:
            raise ValueError("Missing FMF member " + ext)
    parent = gen.parse_tac(source.data_by_ext[".tac"])
    lock = req["native_style_lock"]
    expected_style = lock["style_string"]
    expected_fourcc = bytes.fromhex(lock["fourcc_hex"])
    if parent.style != expected_style or bytes(parent.quad) != expected_fourcc:
        raise ValueError("Parent style string/FourCC mismatch")
    if int(parent.hdr[2]) != int(req["mentality_native_value"]):
        raise ValueError("Parent mentality mismatch")
    if len(parent.pairs) != 11:
        raise ValueError("Parent must have exactly eleven phase pairs")
    by_slot = {p.slot:p for p in parent.pairs}
    if set(by_slot) != set(range(11)):
        raise ValueError("Parent slots must be 0..10")
    roles = {x["id"]:x for x in catalog["roles"]}
    for change in req["player_changes"]:
        phase = 0 if change["phase"].upper() == "IP" else 1
        verify_parent_change(gen, block_for(by_slot[int(change["slot"])],phase), change, catalog, roles)

    tac = copy.deepcopy(parent)
    parent_ti = bytes(parent.packed)
    ti_vector = gen.encode_ti({"ti":req["team_instructions"]}, catalog, tac.packed)
    tac.packed[:] = ti_vector
    pos_masks = {x["id"]:int(x["mask"]) for x in catalog["positions"]}
    phase_map = {"IP":0,"OOP":1}
    changed = set()
    role_changes = []
    for change in req["player_changes"]:
        slot = int(change["slot"])
        pname = change["phase"].upper()
        phase = phase_map[pname]
        pair = next(p for p in tac.pairs if p.slot == slot)
        block = block_for(pair,phase)
        pos = gen.native_position_id(change["position"],phase)
        role_id = gen.role_id_from_display(change["role"],phase,set(roles))
        role = roles[role_id]
        if int(role["phase"]) != phase:
            raise ValueError("Role phase mismatch: " + role_id)
        eligible = catalog.get("role_eligibility",{}).get(pos)
        if not eligible or role_id not in eligible[phase]:
            raise ValueError("Role not eligible: " + pname + "/" + pos + "/" + role_id)
        duty = gen.resolve_role_duty(role_id,{"duty":change["duty"]})
        pi_mask = gen.encode_pi(change["pi"],catalog,phase,pos,role_id,duty)
        old = decode(block,phase,catalog)
        block.selector = pos_masks[pos]
        block.mask = int(role["flags"]) | duty
        gen.update_role_entry(block,int(role["flags"]),pi_mask)
        changed.add((slot,pname))
        role_changes.append({"slot":slot,"phase":pname,"position":pos,"old_role":old["role"],"new_role":role_id,"old_duty":old["duty"],"new_duty":duty,"pi":change["pi"],"pi_mask":hex(pi_mask)})

    title = req["title"]
    tac.title = title
    tac_bytes = gen.write_tac(tac)
    gen.parse_tac(tac_bytes)
    output = gen.write_fmf(source,tac_bytes,title)
    parsed = gen.parse_fmf(output)
    result = gen.parse_tac(parsed.data_by_ext[".tac"])
    result_by_slot = {p.slot:p for p in result.pairs}
    if set(result_by_slot) != set(range(11)):
        raise ValueError("Readback missing slots")
    matrix = []
    for slot in range(11):
        pair = result_by_slot[slot]
        matrix.append({"slot":slot,"phase":"IP",**decode(pair.ip,0,catalog)})
        matrix.append({"slot":slot,"phase":"OOP",**decode(pair.oop,1,catalog)})
        before = by_slot[slot]
        if before.ip.selector != pair.ip.selector or before.oop.selector != pair.oop.selector:
            raise ValueError("Position changed at slot " + str(slot))
        if gen.write_block(before.oop) != gen.write_block(pair.oop):
            raise ValueError("OOP block changed at slot " + str(slot))
        if (slot,"IP") not in changed and gen.write_block(before.ip) != gen.write_block(pair.ip):
            raise ValueError("Untargeted IP block changed at slot " + str(slot))
    defenders = sorted(x["position"] for x in matrix if x["phase"]=="IP" and x["position"] in ("DL","DCL","DCR","DR"))
    if defenders != ["DCL","DCR","DL","DR"]:
        raise ValueError("In-possession back four check failed")
    pi_readback = []
    for change in req["player_changes"]:
        slot = int(change["slot"]); phase = phase_map[change["phase"].upper()]
        block = block_for(result_by_slot[slot],phase)
        pos = gen.native_position_id(change["position"],phase)
        role_id = gen.role_id_from_display(change["role"],phase,set(roles))
        role_flag = int(roles[role_id]["flags"])
        duty = gen.resolve_role_duty(role_id,{"duty":change["duty"]})
        expected = gen.encode_pi(change["pi"],catalog,phase,pos,role_id,duty)
        entries = [x for x in block.items if int(x["key"]) == role_flag]
        if len(entries) != 1 or int(entries[0]["mask2"]) != expected or int(block.mask) != (role_flag|duty):
            raise ValueError("New PI/role/duty readback mismatch at slot " + str(slot))
        pi_readback.append({"slot":slot,"phase":change["phase"],"role":role_id,"duty":duty,"pi_mask":hex(expected)})
    if bytes(result.packed) != bytes(ti_vector):
        raise ValueError("TI native vector readback mismatch")
    if result.style != expected_style or bytes(result.quad) != expected_fourcc:
        raise ValueError("Style string/FourCC did not remain locked")
    if int(result.hdr[2]) != int(req["mentality_native_value"]):
        raise ValueError("Mentality changed unexpectedly")
    if result.ids != parent.ids or result.lists != parent.lists or result.records != parent.records or result.end != parent.end:
        raise ValueError("TAC ID/footer/opaque records changed")
    expected_aom = gen.replace_lp_occurrence(source.data_by_ext[".aom"],parent.title,title)
    if parsed.data_by_ext[".aom"] != expected_aom:
        raise ValueError("AOM changed beyond title")
    if parsed.envelope_by_ext[".img"][2] != source.envelope_by_ext[".img"][2]:
        raise ValueError("IMG envelope changed")
    other_changed = [e for e in source.data_by_ext if e not in (".tac",".aom") and parsed.data_by_ext.get(e) != source.data_by_ext[e]]
    if other_changed:
        raise ValueError("Other FMF members changed: " + ", ".join(other_changed))
    if parsed.root_title != title or result.title != title:
        raise ValueError("Tactic title readback mismatch")

    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_bytes(output)
    report = {
      "version":req["version"],"parent_file":req["parent_file"],"parent_sha256":parent_hash,
      "output_file":output_path.name,"bytes":len(output),"sha256":sha(output),
      "native_style_string":result.style,"native_fourcc_hex":bytes(result.quad).hex(),
      "mentality_native_value":int(result.hdr[2]),"parent_ti_vector_hex":parent_ti.hex(),
      "output_ti_vector_hex":bytes(result.packed).hex(),"team_instruction_changes":req["team_instruction_changes"],
      "role_changes":role_changes,"ip_back_four":defenders,"phase_matrix":matrix,"pi_readback":pi_readback,
      "checks":{
        "parent_sha256_verified":True,"parent_fmf_members_parsed":True,"11_ip_oop_pairs":True,
        "22_phase_role_duty_catalog_checks":True,"ip_four_back_dl_dcl_dcr_dr":True,
        "all_positions_preserved":True,"only_declared_ip_blocks_changed":True,
        "all_11_oop_blocks_byte_identical":True,"changed_pi_masks_read_back_exactly":True,
        "team_instruction_vector_read_back_exactly":True,"native_style_string_and_fourcc_preserved":True,
        "mentality_preserved":True,"tac_ids_footer_and_opaque_records_preserved":True,
        "aom_title_only_updated":True,"img_envelope_byte_identical":True,
        "other_fmf_members_unchanged":True,"output_fmf_reparsed":True
      },
      "status":"offline_binary_roundtrip_verified_not_game_import_verified",
      "game_import":False,"match_performance":False,
      "limitations":[
        "Save build 27.1.1+2511875 is not registered in fmsave 0.14.3 upstream; report used borrowed schema-6 layout with local cross-checks.",
        "Non-goalkeeper position-code semantics and role_code are not fully verified in FM27 UI.",
        "Native FMF build/readback does not verify in-game import or match performance."
      ]
    }
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    args = parser.parse_args()
    report = build(args.request.resolve(),args.output.resolve(),args.report.resolve())
    print(json.dumps({"status":report["status"],"file":report["output_file"],"bytes":report["bytes"],"sha256":report["sha256"],"checks":report["checks"]},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
