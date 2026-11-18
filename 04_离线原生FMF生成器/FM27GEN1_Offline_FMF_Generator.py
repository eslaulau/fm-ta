#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build native FM27 FMF files from structured JSON tactic recipes.

The primary input is a plain UTF-8 JSON object. Legacy FM27GEN1:Base64 TXT
files remain readable for backward compatibility, but are not required.
This tool operates on local FM27 files and never launches or modifies a
running Football Manager process. It edits a registered native .fmf
container using the inspected FMF/.tac structure.

Scope is deliberately strict: FM27 source-major 27 templates, 11 slots,
the current FM27 catalog, known TI/PI mappings and known role-duty tags.
Unknown recipe fields are rejected instead of silently discarded.
"""
from __future__ import annotations
import argparse, base64, json, os, re, struct, sys, hashlib, subprocess
from pathlib import Path
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HERE = Path(__file__).resolve().parent

OUTER_MAGIC = bytes.fromhex('02016166652e080000')
INNER_MAGIC = bytes.fromhex('0201666d662e080000')
MEMBER_HEADER = bytes.fromhex('1000000010000000')
TAC_PREFIX = bytes.fromhex('03016361742e2200224400')
BLOCK_MARK = bytes.fromhex('440002')
ITEM_MARK = bytes.fromhex('020202')
ROLE_MASK = 0xfffffffbf91fffff
DUTY_FLAGS = {0, 2097152, 4194304, 8388608, 33554432, 67108864, 17179869184}
# Opaque, template-owned native TI bits observed in real FM27 samples.
# They are preserved from the selected native style template and are not user-editable mappings.
PRESERVED_OPAQUE_TI_BITS = {33, 34, 74, 75, 76}

# For the user's current A9.0.2 GEN1 recipe and the common FM27 v1 recipe tokens.
# Values are native PI option IDs from the FM27 tactic catalog.
PI_MAP = {
    ('PASSING_STRATEGY','SHORTER'): 1,
    ('PASSING_STRATEGY','MORE_DIRECT'): 2,
    ('PASSING_RISKS','TAKE_MORE_RISKS'): 3,
    ('PASSING_RISKS','TAKE_FEWER_RISKS'): 4,
    ('DRIBBLING_FREQUENCY','DRIBBLE_MORE'): 13,
    ('DRIBBLING_FREQUENCY','DRIBBLE_LESS'): 14,
    ('DRIBBLING_DIRECTION','CUT_INSIDE_WITH_BALL'): 16,
    ('SHOOTING','SHOOT_MORE_OFTEN'): 18,
    ('SHOOTING','SHOOT_LESS_OFTEN'): 19,
    ('FORWARD_RUNS','MAKE_MORE_RUNS'): 22,
    ('ATTACKING_WIDTH','STAY_WIDER'): 25,
    ('ATTACKING_WIDTH','SIT_NARROWER'): 26,
    ('MARKING','MARK_TIGHTER'): 33,
    ('TACKLING','EASE_OFF_TACKLES'): 32,
    ('TRIGGER_PRESS','MORE_OFTEN'): 29,
    ('ATTACK_BOX_SIDE','CENTRE'): 36,
    ('ATTACK_BOX_SIDE','NEAR_POST'): 39,
    ('ATTACK_BOX_SIDE','FAR_POST'): 40,
    # Remaining native PI option IDs from catalog.json (2026-11-18 coverage audit).
    ('ATTACKING_WIDTH','MOVE_INTO_CHANNELS'): 27,
    ('DRIBBLING_DIRECTION','RUN_WIDE_WITH_BALL'): 15,
    ('FORWARD_RUNS','KEEP_POSITION'): 23,
    ('HOLD_UP_BALL','YES'): 17,
    ('CROSSING_TARGET','CENTRE'): 11,
    ('CROSSING_TARGET','NEAR_POST'): 9,
    ('CROSSING_TARGET','TARGET_FORWARD'): 12,
    ('CROSSING_FREQUENCY','FROM_DEEP'): 7,
    ('MARKING_TARGET','SPECIFIC_PLAYER'): 34,
    ('MARKING_TARGET','SPECIFIC_POSITION'): 35,
    ('ATTACK_BOX_SIDE','LEFT'): 37,
    ('ATTACK_BOX_SIDE','RIGHT'): 38,
    ('ATTACK_BOX_DEPTH','ATTACK_DEFENSIVE_LINE'): 41,
}

# Experimental mappings sourced from catalog.json native option IDs.
# The user confirmed all test instructions are visible after FM27 import on 2026-11-18;
# in-match tactical effects remain unverified.
EXPERIMENTAL_PI_MAP = {
    ('CROSSING_TARGET','BACK_POST'): 10,          # catalog player_instructions group 9
    ('ROAMING','ROAM_FROM_POSITION'): 24,         # catalog group 4
    ('CROSSING_FREQUENCY','BYLINE'): 8,            # catalog group 10
    ('ATTACK_BOX_DEPTH','LATE_RUNS'): 42,          # catalog group 16
    ('TRIGGER_PRESS','LESS_OFTEN'): 30,            # catalog group 11, OOP
    ('TACKLING','GET_STUCK_IN'): 31,               # catalog group 13, OOP
}
PI_MAP.update(EXPERIMENTAL_PI_MAP)

# Native duty bit values are confirmed by FM27 TAC samples. The additional
# role-specific choices below are read directly from the 90-preset index
# (D=Defend, S=Support, A=Attack) and are checked against catalog role/phase/
# position eligibility and PI-policy rows by FM27GEN1_Netlify90_OfficialPreset_Audit.py.
# This index-derived role coverage does NOT establish a native style FourCC.
ROLE_DUTY = {
    'BallPlayingGoalkeeper': 4194304,
    'OPSweeperKeeper': 8388608,
    'BoxToBoxMidfielder': 4194304,
    'OPHoldingFullBack': 2097152,
    # Explicitly selected Support duty for the standard IP Wing-Back role in X2.0.
    'WingBack': 4194304,
    # Explicitly selected Support duty for the standard IP Full-Back role in X2.0.
    'FullBack': 4194304,
    'CentreBack': 2097152,
    'OPCoveringCentreBack': 2097152,
    'BallPlayingCentreBack': 2097152,
    'OPCentreBack': 2097152,
    'DeepLyingPlaymaker': 4194304,
    'OPFullBack': 2097152,
    'DefensiveMidfielder': 2097152,
    'OPScreeningDefensiveMidfielder': 2097152,
    'AdvancedPlaymaker': 8388608,
    'OPCentralMidfielder': 4194304,
    'CentreForward': 8388608,
    'InsideWinger': 4194304,
    'OPTrackingWideMidfielder': 2097152,
    'InsideForward': 8388608,
    'ChannelForward': 8388608,
    'OPTrackingCentreForward': 2097152,
    # OOP tracking attacking-midfielder role uses the native defensive-phase duty tag.
    'OPTrackingAttackingMidfielder': 2097152,
    # Additional roles/duties extracted from the native Control Possession sample.
    'InsideFullBack': 2097152,
    'OPPressingFullBack': 4194304,
    'InsideWingBack': 2097152,
    'OPDefensiveMidfielder': 2097152,
    'ChannelMidfielder': 8388608,
    'OPPressingCentralMidfielder': 8388608,
    'WideForward': 8388608,
    'OPWinger': 4194304,
    'Winger': 4194304,
    'OPTrackingWinger': 2097152,
    'OPCentreForward': 4194304,
    # Additional official-index role/duty pairs (D=Defend, S=Support, A=Attack).
    'Goalkeeper': 2097152,
    'OPGoalkeeper': 4194304,
    'FreeRole': 8388608,
    'OPDroppingDefensiveMidfielder': 2097152,
    'OPWideCoverCentralMidfielder': 4194304,
    'Poacher': 8388608,
    'OPWingBack': 2097152,
    'OPCentralOutletCentreForward': 8388608,
    'OPAttackingMidfielder': 4194304,
    'OPScreeningCentralMidfielder': 2097152,
    'OPHoldingWingBack': 2097152,
    'DeepLyingForward': 8388608,
    'PlaymakingWingBack': 4194304,
    'OPPressingDefensiveMidfielder': 4194304,
    'OPWideMidfielder': 4194304,
    'AdvancedWingBack': 8388608,
    'WideCentreBack': 2097152,
    'OPPressingWingBack': 4194304,
    'OPStoppingWideCentreBack': 2097152,
    'OPWideCentreBack': 2097152,
    'OPWideCoverDefensiveMidfielder': 2097152,
    'OPCentralOutletAttackingMidfielder': 8388608,
    'OPInsideOutletWinger': 8388608,
    'NoNonsenseGoalkeeper': 2097152,
    'NoNonsenseCentreBack': 2097152,
    'AttackingMidfielder': 8388608,
    'WideCentralMidfielder': 4194304,
    'WideMidfielder': 4194304,
    'OPSplittingOutletCentreForward': 8388608,
    'OPSplittingOutletAttackingMidfielder': 8388608,
    'CentralMidfielder': 4194304,
    'SecondStriker': 8388608,
    'OPStoppingCentreBack': 2097152,
    'OPLineKeeper': 2097152,
    'TargetForward': 8388608,
    'BoxToBoxPlaymaker': 4194304,
    'OPWideOutletWideMidfielder': 8388608,
    'MidfieldPlaymaker': 4194304,
    'OPWideOutletWinger': 8388608,
}

# These native role IDs are present in catalog.json but do not yet have a
# source-backed role->duty assignment in the current sample/preset evidence.
# Keep them explicit so future catalog expansion cannot silently overlook them.
ROLE_DUTY_UNMAPPED = frozenset({
    'PlaymakingWinger',
    'OPCoveringWideCentreBack',
    'OverlappingCentreBack',
    'FalseNine',
    'HalfBack',
    'AdvancedCentreBack',
})

DUTY_NAME_TO_FLAG = {
    'D': 2097152, 'DEFEND': 2097152,
    'S': 4194304, 'SUPPORT': 4194304,
    'A': 8388608, 'ATTACK': 8388608,
    'NONE': 0,
}

def resolve_role_duty(roleid: str, phase_item: dict) -> int:
    """Use an explicit native duty when provided; otherwise retain the legacy role default."""
    if 'duty' not in phase_item:
        duty = ROLE_DUTY.get(roleid)
        if duty is None:
            raise ValueError(
                f'角色 {roleid} 没有固定 duty 默认值；请在该阶段对象中显式填写 duty（D/S/A 或原生 duty bit）'
            )
    else:
        selected = phase_item['duty']
        if isinstance(selected, str):
            token = selected.strip().upper()
            if token not in DUTY_NAME_TO_FLAG:
                raise ValueError(f'未知 duty 名称：{selected!r}；使用 D/DEFEND、S/SUPPORT、A/ATTACK 或原生整数 bit')
            duty = DUTY_NAME_TO_FLAG[token]
        elif isinstance(selected, int) and not isinstance(selected, bool):
            duty = selected
        else:
            raise ValueError('duty 必须是 D/S/A 名称或原生整数 bit')
    if duty not in DUTY_FLAGS:
        raise ValueError(f'角色 {roleid} 的 duty 不属于 FM27 原生 duty 集合：{duty}')
    return duty

# Native team-option bits for the non-default A9.0.2 selections.
# Every bit below was cross-checked against the packed 12-byte vector in the
# downloaded A9.0.2 .fmf and the current local catalog.
TI_GROUPS = {
    'PASSING_DIRECTNESS': [1],
    'TEMPO': [21],
    'ATTACKING_WIDTH': [4],
    'ATTACKING_TRANSITION': [3],
    'CREATIVE_FREEDOM': [5],
    'TIME_WASTING': [7],
    'PLAY_FOR_SET_PIECES': [6],
    'BUILD_UP_STRATEGY': [24],
    'GOAL_KICKS': [29],
    'GOALKEEPER_DISTRIBUTION': [16],
    'GK_DISTRIBUTION_(SPEED)': [17],
    'PROGRESS_THROUGH': [30],
    'PASS_RECEPTION': [20],
    'SUPPORTING_RUNS': [28],
    'SUPPORTING_RUNS_SECONDARY': [31],
    'GOALKEEPER_ATTACKING_SET_PIECES': [32],
    'PATIENCE': [18],
    'DRIBBLING': [19],
    'SHOTS_FROM_DISTANCE': [27],
    'CROSSING_STYLE': [26],
    'LINE_OF_ENGAGEMENT': [8],
    'DEFENSIVE_LINE': [9],
    'DEFENSIVE_LINE_BEHAVIOR': [15],
    'TRIGGER_PRESS': [10],
    'DEFENSIVE_TRANSITION': [11],
    'TACKLING': [12],
    'PRESSING_TRAP': [25],
    'SHORT_GOALKEEPER_DISTRIBUTION': [23],
    'CROSS_ENGAGEMENT': [22],
}
TI_MAP = {
    # FM27 Netlify 90-preset style profiles, mapped to native catalog bits.
    ('PASSING_DIRECTNESS','MUCH_SHORTER'): 4,
    ('PASSING_DIRECTNESS','SHORTER'): 3,
    ('PASSING_DIRECTNESS','MORE_DIRECT'): 2,
    ('PASSING_DIRECTNESS','MUCH_MORE_DIRECT'): 1,
    ('TEMPO','NORMAL'): 0,
    ('TEMPO','MUCH_LOWER'): 49,
    ('TEMPO','LOWER'): 48,
    ('TEMPO','MUCH_HIGHER'): 46,
    ('ATTACKING_WIDTH','MUCH_NARROWER'): 53,
    ('ATTACKING_WIDTH','NARROWER'): 52,
    ('ATTACKING_WIDTH','MUCH_WIDER'): 50,
    ('ATTACKING_TRANSITION','HOLD_SHAPE'): 55,
    ('CREATIVE_FREEDOM','MORE_DISCIPLINED'): 20,
    ('CREATIVE_FREEDOM','MORE_EXPRESSIVE'): 19,
    ('TIME_WASTING','MORE_OFTEN'): 78,
    ('TIME_WASTING','LESS_OFTEN'): 79,
    ('PLAY_FOR_SET_PIECES','PLAY_FOR_SET_PIECES'): 18,
    ('BUILD_UP_STRATEGY','BYPASS_PRESS'): 8,
    ('GK_DISTRIBUTION_(SPEED)','SLOW_PACE_DOWN'): 43,
    ('GK_DISTRIBUTION_(SPEED)','DISTRIBUTE_QUICKLY'): 42,
    ('PROGRESS_THROUGH','MIDDLE'): 23,
    ('PROGRESS_THROUGH','BOTH_FLANKS'): 24,
    ('PASS_RECEPTION','PASS_TO_FEET'): 6,
    ('SUPPORTING_RUNS','BOTH_FLANKS'): 28,
    ('PATIENCE','HIT_EARLY_CROSSES'): 9,
    ('DRIBBLING','ENCOURAGE'): 13,
    ('DRIBBLING','DISCOURAGE'): 14,
    ('CROSSING_STYLE','LOW_CROSSES'): 12,
    ('LINE_OF_ENGAGEMENT','STANDARD'): 0,
    ('LINE_OF_ENGAGEMENT','LOW_BLOCK'): 63,
    ('LINE_OF_ENGAGEMENT','MID_BLOCK'): 62,
    ('DEFENSIVE_LINE','LOWER'): 58,
    ('DEFENSIVE_LINE_BEHAVIOR','DROP_OFF_MORE'): 77,
    ('DEFENSIVE_LINE_BEHAVIOR','STEP_UP_MORE'): 76,
    ('TRIGGER_PRESS','LESS_OFTEN'): 67,
    ('TRIGGER_PRESS','MUCH_MORE_OFTEN'): 65,
    ('DEFENSIVE_TRANSITION','REGROUP'): 71,
    ('TACKLING','STAY_ON_FEET'): 73,
    ('TACKLING','GET_STUCK_IN'): 72,
    ('PRESSING_TRAP','TRAP_OUTSIDE'): 81,
    ('CROSS_ENGAGEMENT','INVITE_CROSSES'): 83,

    ('TEMPO','HIGHER'): 47,
    ('ATTACKING_WIDTH','WIDER'): 51,
    ('ATTACKING_TRANSITION','COUNTER_ATTACK'): 54,
    ('PLAY_FOR_SET_PIECES','KEEP_BALL_IN_PLAY'): 0,
    ('BUILD_UP_STRATEGY','PLAY_THROUGH_PRESS'): 7,
    ('GOAL_KICKS','SHORT'): 44,
    ('GOAL_KICKS','LONG'): 45,
    ('GOALKEEPER_DISTRIBUTION','CENTRE_BACKS'): 35,
    ('GOALKEEPER_DISTRIBUTION','FULL_BACKS'): 36,
    ('PASS_RECEPTION','PASS_INTO_SPACE'): 5,
    ('PATIENCE','WORK_BALL_INTO_BOX'): 17,
    ('SHOTS_FROM_DISTANCE','DISCOURAGE'): 16,
    ('LINE_OF_ENGAGEMENT','HIGH_PRESS'): 61,
    ('DEFENSIVE_LINE','HIGHER'): 57,
    ('TRIGGER_PRESS','MORE_OFTEN'): 66,
    ('DEFENSIVE_TRANSITION','COUNTER_PRESS'): 70,
    ('SHORT_GOALKEEPER_DISTRIBUTION','YES'): 69,

    # Remaining explicit native catalog bits from the 2026-11-18 coverage audit.
    ('DEFENSIVE_LINE','MUCH_LOWER'): 59,
    ('TRIGGER_PRESS','MUCH_LESS_OFTEN'): 68,
    ('GOALKEEPER_DISTRIBUTION','WIDE'): 37,
    ('GOALKEEPER_DISTRIBUTION','TARGET_FORWARD'): 40,
    ('GOALKEEPER_DISTRIBUTION','OVER_OPPOSITION_DEFENCE'): 38,
    ('CROSS_ENGAGEMENT','STOP_CROSSES'): 82,
    ('CROSSING_STYLE','HIGH_CROSSES'): 10,
    ('SHOTS_FROM_DISTANCE','ENCOURAGE'): 15,
    ('SUPPORTING_RUNS','LEFT_INSIDE'): 29,
    ('PROGRESS_THROUGH','LEFT'): 21,
    ('SUPPORTING_RUNS_SECONDARY','LEFT_OUTSIDE'): 26,
    ('SUPPORTING_RUNS_SECONDARY','RIGHT_OUTSIDE'): 27,
    ('SUPPORTING_RUNS_SECONDARY','BOTH_OUTSIDE'): 25,
    ('GOALKEEPER_ATTACKING_SET_PIECES','YES'): 60,
}

# Experimental mappings sourced from catalog.json native_bit values.
# The user confirmed all test instructions are visible after FM27 import on 2026-11-18;
# in-match tactical effects remain unverified.
EXPERIMENTAL_TI_MAP = {
    ('DEFENSIVE_LINE','MUCH_HIGHER'): 56,
    ('PRESSING_TRAP','TRAP_INSIDE'): 80,
    ('CROSSING_STYLE','WHIPPED_CROSSES'): 11,
    ('PROGRESS_THROUGH','RIGHT'): 22,
    ('GOALKEEPER_DISTRIBUTION','PLAYMAKER'): 39,
    ('SUPPORTING_RUNS','RIGHT_INSIDE'): 30,
}
TI_MAP.update(EXPERIMENTAL_TI_MAP)


STYLE_CODE = {
    'Gegenpress': b'EGEG',  # fallback for legacy callers without a registry file
}


def resolve_style_definition(style_name: str, registry: dict | None) -> dict:
    """Resolve a style only from a verified registry entry; never infer its native code."""
    if registry is not None:
        matches = [x for x in registry.get('styles', []) if x.get('name') == style_name]
        if len(matches) != 1:
            raise ValueError(f'风格登记表中不存在唯一条目：{style_name}')
        item = matches[0]
        if item.get('status') != 'implemented_sample_verified':
            raise ValueError(f'该风格尚未完成原生样本验证，拒绝生成：{style_name}')
        code_hex = item.get('style_code_hex')
        tac_style = item.get('tac_style_string')
        template = item.get('template')
        if not code_hex or not tac_style or not template:
            raise ValueError(f'风格登记条目缺少原生证据字段：{style_name}')
        try:
            code = bytes.fromhex(code_hex)
        except ValueError as exc:
            raise ValueError(f'风格代码不是有效十六进制：{style_name}') from exc
        if len(code) != 4:
            raise ValueError(f'原生风格代码必须为四字节：{style_name}')
        return {'name': style_name, 'tac_style_string': tac_style,
                'style_code': code, 'template': template}
    code = STYLE_CODE.get(style_name)
    if code is None:
        raise ValueError(f'未知战术风格：{style_name}')
    return {'name': style_name, 'tac_style_string': 'Custom ' + style_name,
            'style_code': code, 'template': None}


def resolve_template_path(style_name: str, registry: dict | None, supplied: Path | None = None) -> Path:
    """Resolve the registered native template; reject cross-style template substitution."""
    definition = resolve_style_definition(style_name, registry)
    registered = definition.get('template')
    if supplied is None:
        if not registered:
            raise ValueError('当前风格没有登记原生模板；请显式提供 --template')
        target = (HERE / registered).resolve()
    else:
        target = supplied.expanduser().resolve()
        if registered:
            expected = (HERE / registered).resolve()
            if target != expected:
                raise ValueError(f'风格 {style_name} 必须使用登记模板 {expected}；拒绝跨风格模板')
    if not target.is_file():
        raise FileNotFoundError(f'找不到该风格登记的原生模板：{target}')
    return target


def u32(b: bytes, p: int) -> int: return struct.unpack_from('<I', b, p)[0]
def u64(b: bytes, p: int) -> int: return struct.unpack_from('<Q', b, p)[0]
def lp_read(b: bytes, p: int) -> tuple[str,int]:
    n=u32(b,p); p+=4
    if n>1_000_000 or p+n>len(b): raise ValueError('损坏的长度前缀字符串')
    return b[p:p+n].decode('utf-8'),p+n
def lp_write(s: str) -> bytes:
    x=s.encode('utf-8'); return struct.pack('<I',len(x))+x

def xxh64(data: bytes, seed: int=0) -> int:
    mask=(1<<64)-1
    p1=11400714785074694791; p2=14029467366897019727; p3=1609587929392839161; p4=9650029242287828579; p5=2870177450012600261
    def rot(x,r): return ((x<<r)|(x>>(64-r)))&mask
    def rnd(acc,x): return rot((acc+x*p2)&mask,31)*p1&mask
    def merge(acc,v): return ((acc^rnd(0,v))*p1+p4)&mask
    n=len(data); p=0
    if n>=32:
        v1=(seed+p1+p2)&mask; v2=(seed+p2)&mask; v3=seed&mask; v4=(seed-p1)&mask
        while p<=n-32:
            v1=rnd(v1,int.from_bytes(data[p:p+8],'little')); p+=8
            v2=rnd(v2,int.from_bytes(data[p:p+8],'little')); p+=8
            v3=rnd(v3,int.from_bytes(data[p:p+8],'little')); p+=8
            v4=rnd(v4,int.from_bytes(data[p:p+8],'little')); p+=8
        h=(rot(v1,1)+rot(v2,7)+rot(v3,12)+rot(v4,18))&mask
        for v in (v1,v2,v3,v4): h=merge(h,v)
    else: h=(seed+p5)&mask
    h=(h+n)&mask
    while p<=n-8:
        h=rot(h^rnd(0,int.from_bytes(data[p:p+8],'little')),27)*p1+p4&mask; p+=8
    if p<=n-4:
        h=rot(h^(int.from_bytes(data[p:p+4],'little')*p1&mask),23)*p2+p3&mask; p+=4
    while p<n:
        h=rot(h^(data[p]*p5&mask),11)*p1&mask; p+=1
    h^=h>>33; h=h*p2&mask; h^=h>>29; h=h*p3&mask; h^=h>>32
    return h&mask

def zstd_raw_frame(data: bytes) -> bytes:
    # Standards-compliant single-segment Zstandard frame, raw blocks + XXH64 checksum.
    # A4: FCS flag 2 (4 bytes), single segment, checksum enabled.
    if len(data)>0x1fffff: raise ValueError('单个原始 Zstandard 块超过 2 MiB')
    header=b'\x28\xb5\x2f\xfd'+b'\xa4'+struct.pack('<I',len(data))
    block_header=((len(data)<<3)|1).to_bytes(3,'little')
    return header+block_header+data+struct.pack('<I',xxh64(data)&0xffffffff)

def zstd_decompress(data: bytes) -> bytes:
    try:
        import zstandard as zstd
        return zstd.ZstdDecompressor().decompress(data, max_output_size=64*1024*1024)
    except ImportError:
        p=subprocess.run(['zstd','-q','-d','-c'],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode: raise ValueError('Zstandard 解压失败：'+p.stderr.decode('utf-8','replace'))
        return p.stdout

def aes_ctr(data: bytes,key: bytes,iv: bytes) -> bytes:
    x=Cipher(algorithms.AES(key),modes.CTR(iv)).encryptor()
    return x.update(data)+x.finalize()

@dataclass
class Block:
    selector:int; flag:int; items:list; mask:int
@dataclass
class Pair:
    slot:int; ip:Block; oop:Block
@dataclass
class Entry:
    ident:int; flag:int; block:Block|None

@dataclass
class Tac:
    magic:bytes; title:str; hdr:bytearray; packed:bytearray; style:str; quad:bytearray; pairs:list; ids:list; lists:list; records:list; end:int


def parse_block(b:bytes,p:int)->tuple[Block,int]:
    if b[p:p+3]!=BLOCK_MARK: raise ValueError(f'战术块标记错误 at {p:x}')
    p+=3; selector=u32(b,p);p+=4
    if b[p:p+2]!=b'\x00\x01': raise ValueError('战术块常量错误')
    p+=2;flag=b[p];p+=1;count=u32(b,p);p+=4
    if flag not in (0,1) or count>4096: raise ValueError('战术块字段越界')
    items=[]
    for _ in range(count):
        key=u64(b,p);p+=8
        if b[p:p+3]!=ITEM_MARK: raise ValueError('PI 条目标记错误')
        p+=3; mask2=u64(b,p);p+=8
        if b[p]!=255: raise ValueError('PI 条目终止字节错误')
        p+=1; value=u32(b,p);p+=4
        items.append({'key':key,'mask2':mask2,'value':value})
    if b[p:p+4]!=bytes(4): raise ValueError('战术块尾部常量错误')
    p+=4;mask=u64(b,p);p+=8
    return Block(selector,flag,items,mask),p

def parse_tac(b:bytes)->Tac:
    if len(b)<64 or b[:11]!=TAC_PREFIX or b[11] not in (26,27): raise ValueError('不是受支持的 FM26/27 TAC 结构')
    p=16;title,p=lp_read(b,p)
    if b[p:p+12]!=bytes(12): raise ValueError('TAC 标题后填充错误')
    p+=12;hdr=bytearray(b[p:p+6]);p+=6
    packed=bytearray(b[p:p+12]);p+=12
    if b[p]!=255: raise ValueError('缺少 style 字符串起始标记')
    p+=1;style,p=lp_read(b,p);quad=bytearray(b[p:p+4]);p+=4
    pairs=[]
    while b[p:p+3]==BLOCK_MARK:
        ip,p=parse_block(b,p);oop,p=parse_block(b,p)
        slot=b[p];p+=1;pairs.append(Pair(slot,ip,oop))
        if len(pairs)>11: raise ValueError('球员阶段对超过 11 组')
    if b[p]!=1: raise ValueError('ID list 标记错误')
    p+=1;n=u32(b,p);p+=4
    if n>4096: raise ValueError('ID list 过长')
    ids=[]
    for _ in range(n):
        ident=u32(b,p);flag=u32(b,p+4);p+=8
        if flag not in (0,1): raise ValueError('ID list flag 无效')
        block=None
        if flag:block,p=parse_block(b,p)
        ids.append(Entry(ident,flag,block))
    if b[p:p+4]!=bytes(4): raise ValueError('footer 前常量错误')
    p+=4;n_lists=u32(b,p);p+=4
    if n_lists>64: raise ValueError('footer list 数量无效')
    lists=[]
    for _ in range(n_lists):
        tag=u32(b,p);count=u32(b,p+4);p+=8
        vals=[]
        if count>4096: raise ValueError('footer ID 数量无效')
        for _ in range(count):
            if b[p:p+2]!=b'\x01\x00': raise ValueError('footer ID 常量错误')
            p+=2;vals.append(u32(b,p));p+=4
        lists.append((tag,vals))
    if b[p:p+4]!=b'\x01\x00\x00\x00': raise ValueError('footer records 标记错误')
    p+=4;records=[b[p+i*13:p+(i+1)*13] for i in range(12)];p+=156
    end=b[p];p+=1
    if b[p:p+30]!=bytes(30): raise ValueError('TAC 尾部零填充错误')
    p+=30
    if p!=len(b): raise ValueError(f'TAC 末尾有 {len(b)-p} 个未解析字节')
    if len(pairs)!=11 or sorted(x.slot for x in pairs)!=list(range(11)): raise ValueError('必须包含 11 个唯一球员槽位')
    return Tac(bytes(b[:16]),title,hdr,packed,style,quad,pairs,ids,lists,records,end)

def write_block(x:Block)->bytes:
    out=bytearray(BLOCK_MARK+struct.pack('<I',x.selector)+b'\x00\x01'+bytes([x.flag])+struct.pack('<I',len(x.items)))
    for z in sorted(x.items,key=lambda y:y['key']):
        out+=struct.pack('<Q',z['key'])+ITEM_MARK+struct.pack('<Q',z['mask2'])+b'\xff'+struct.pack('<I',z['value'])
    out+=bytes(4)+struct.pack('<Q',x.mask)
    return bytes(out)

def write_tac(t:Tac)->bytes:
    out=bytearray(t.magic+lp_write(t.title)+bytes(12)+bytes(t.hdr)+bytes(t.packed)+b'\xff'+lp_write(t.style)+bytes(t.quad))
    for pair in t.pairs:
        out+=write_block(pair.ip)+write_block(pair.oop)+bytes([pair.slot])
    out+=b'\x01'+struct.pack('<I',len(t.ids))
    for e in t.ids:
        out+=struct.pack('<II',e.ident,e.flag)
        if e.flag:
            if e.block is None: raise ValueError('ID list nested block missing')
            out+=write_block(e.block)
    out+=bytes(4)+struct.pack('<I',len(t.lists))
    for tag,vals in t.lists:
        out+=struct.pack('<II',tag,len(vals))
        for ident in vals: out+=b'\x01\x00'+struct.pack('<I',ident)
    out+=b'\x01\x00\x00\x00'+b''.join(t.records)+bytes([t.end])+bytes(30)
    return bytes(out)

@dataclass
class TocEntry:
    name:str; ext:str; offset:int; stored:int; raw:int; t1:int; t2:int; folder:str|None
@dataclass
class Fmf:
    source:bytes; entries:list; root_title:str; directories:list; data_by_ext:dict; envelope_by_ext:dict

def parse_fmf(data:bytes)->Fmf:
    if not data.startswith(OUTER_MAGIC): raise ValueError('FMF outer magic 错误')
    size,second,rev=struct.unpack_from('<QQB',data,9)
    if second!=17 or rev!=3: raise ValueError('不支持的 FMF outer header')
    footer=9+size
    if data[footer:footer+9]!=INNER_MAGIC: raise ValueError('FMF inner marker 不在预期偏移')
    toc=zstd_decompress(data[footer+9:]);p=0;title,p=lp_read(toc,p)
    n=u32(toc,p);p+=4;entries=[];root=[]
    def read_entry(folder):
        nonlocal p
        name,p2=lp_read(toc,p);p=p2;ext,p2=lp_read(toc,p);p=p2
        off,stored,raw,t1,t2=struct.unpack_from('<QQQqq',toc,p);p+=40
        x=TocEntry(name,ext,off,stored,raw,t1,t2,folder);entries.append(x);return x
    for _ in range(n):root.append(read_entry(None))
    nd=u32(toc,p);p+=4;dirs=[]
    for _ in range(nd):
        dirname,p=lp_read(toc,p);count=u32(toc,p);p+=4;files=[]
        for _ in range(count): files.append(read_entry(dirname))
        dirs.append((dirname,files))
    if p+4!=len(toc) or toc[p:p+4]!=bytes(4): raise ValueError('FMF TOC 结束位置或 terminator 不匹配')
    by_ext={};envs={}
    for e in entries:
        start=26+e.offset;raw_env=data[start:start+e.stored]
        if len(raw_env)!=e.stored or raw_env[:8]!=MEMBER_HEADER: raise ValueError(f'{e.ext} envelope 无效')
        key=raw_env[8:24];iv=raw_env[24:40];compressed=aes_ctr(raw_env[40:],key,iv)
        plain=zstd_decompress(compressed)
        if len(plain)!=e.raw: raise ValueError(f'{e.ext} 解压长度与 TOC 不符')
        by_ext[e.ext]=plain;envs[e.ext]=(key,iv,raw_env)
    return Fmf(data,entries,title,dirs,by_ext,envs)

def replace_lp_occurrence(data:bytes,old:str,new:str)->bytes:
    oldb=old.encode('utf-8');newb=new.encode('utf-8');needle=struct.pack('<I',len(oldb))+oldb
    i=data.find(needle)
    if i<0: raise ValueError('AOM 找不到原 tactic title')
    if data.find(needle,i+1)>=0: raise ValueError('AOM title 不唯一，拒绝猜测')
    return data[:i]+struct.pack('<I',len(newb))+newb+data[i+len(needle):]

def write_fmf(template:Fmf, tac:bytes, new_name:str)->bytes:
    entries=[];records={e.ext:e for e in template.entries}
    aom=replace_lp_occurrence(template.data_by_ext['.aom'],template.data_by_ext['.tac'][20:24].decode('latin1') if False else parse_tac(template.data_by_ext['.tac']).title,new_name)
    plain_by_ext=dict(template.data_by_ext);plain_by_ext['.tac']=tac;plain_by_ext['.aom']=aom
    encrypted_by_ext={};
    # Re-encrypt the changed .tac/.aom with their embedded AES keys/IVs; keep .img byte-identical.
    for ext,plain in plain_by_ext.items():
        old=template.envelope_by_ext[ext]
        if ext=='.img': encrypted_by_ext[ext]=old[2]
        else:
            comp=zstd_raw_frame(plain); key,iv=old[0],old[1]
            encrypted_by_ext[ext]=MEMBER_HEADER+key+iv+aes_ctr(comp,key,iv)
    # Preserve the original data-member order, not manifest enumeration order.
    ordered=sorted(template.entries,key=lambda e:e.offset);blob=bytearray()
    for e in ordered:
        env=encrypted_by_ext[e.ext]
        off=len(blob);blob+=env
        entries.append(TocEntry(e.name,e.ext,off,len(env),len(plain_by_ext[e.ext]),e.t1,e.t2,e.folder))
    bykey={(e.folder,e.ext):e for e in entries}
    toc=bytearray(lp_write(new_name))
    roots=[e for e in template.entries if e.folder is None]
    dirs=template.directories
    toc+=struct.pack('<I',len(roots))
    def emit(e):
        x=bykey[(e.folder,e.ext)]
        name=new_name if e.ext=='.tac' else e.name
        toc.extend(lp_write(name));toc.extend(lp_write(e.ext));toc.extend(struct.pack('<QQQqq',x.offset,x.stored,x.raw,x.t1,x.t2))
    for e in roots: emit(e)
    toc+=struct.pack('<I',len(dirs))
    for dirname,files in dirs:
        toc+=lp_write(dirname)+struct.pack('<I',len(files))
        for e in files: emit(e)
    toc+=bytes(4)
    toc_comp=zstd_raw_frame(bytes(toc))
    return OUTER_MAGIC+struct.pack('<QQB',17+len(blob),17,3)+bytes(blob)+INNER_MAGIC+toc_comp


def role_id_from_display(name:str,phase:int,roles_by_id:set[str])->str:
    token=re.sub(r'[^A-Za-z0-9]','',name)
    token_alias={'BoxtoBoxMidfielder':'BoxToBoxMidfielder','BoxtoBoxPlaymaker':'BoxToBoxPlaymaker'}.get(token,token)
    rid=('OP' if phase==1 else '')+token_alias
    # Netlify display names are not always a byte-for-byte catalog identifier.
    # These aliases were verified against catalog.role_eligibility across all 90 presets.
    rid_alias={
        'OPWideCoveringCentralMidfielder':'OPWideCoverCentralMidfielder',
        'OPWideCoveringDefensiveMidfielder':'OPWideCoverDefensiveMidfielder',
        'OPLineHoldingKeeper':'OPLineKeeper',
    }
    rid=rid_alias.get(rid,rid)
    if rid not in roles_by_id:
        raise ValueError(f'角色无法映射到原生目录：phase={phase}, {name} -> {rid}')
    return rid


POSITION_ALIASES={'DM':'DMC','STC':'ST','STCR':'STR','STCL':'STL'}


def native_position_id(position:str,phase:int)->str:
    """Normalize website 90-index position labels to FM27 catalog IDs."""
    return POSITION_ALIASES.get(str(position),str(position))

def encode_ti(gen1:dict,catalog:dict,base:bytearray)->bytearray:
    # Start from the template so native baseline bits not expressed by GEN1
    # (notably the hidden bit 33 and the separate defensive-line-behaviour bit)
    # remain intact. For every GEN1 key, clear its native option group first.
    vec=bytearray(base)
    groups={int(g['id']):g for g in catalog['team_instructions']}
    ti=gen1.get('ti',{})
    for key,value in ti.items():
        if key not in TI_GROUPS: raise ValueError(f'球队指令 key 未映射：{key}')
        group_ids=TI_GROUPS[key]
        for gid in group_ids:
            if gid not in groups: raise ValueError(f'本机目录缺少球队指令组：{gid}')
            for opt in groups[gid]['options']:
                bit=int(opt.get('native_bit') or 0)
                if bit: vec[bit//8]&=~(1<<(bit%8))
        if value=='DEFAULT': continue
        bit=TI_MAP.get((key,value))
        if bit is None: raise ValueError(f'球队指令值尚未建立离线映射：{key}={value}')
        if bit: vec[bit//8]|=1<<(bit%8)
    allowed={int(o.get('native_bit') or 0) for g in catalog['team_instructions'] for o in g['options']}
    for bit in range(96):
        if vec[bit//8]>>(bit%8)&1 and bit not in allowed and bit not in PRESERVED_OPAQUE_TI_BITS:
            raise ValueError(f'球队指令位 {bit} 不在本机目录且不是已知模板隐藏位')
    return vec

def encode_pi(pis:list, catalog:dict, phase:int, position:str, roleid:str, duty:int)->int:
    if not isinstance(pis,list):
        raise ValueError('PI 必须是数组；没有个人指令时使用空数组 []')
    policy_key=f'{phase}:{position}:{roleid}:{duty}'
    policies=catalog.get('pi_policies',{}).get(policy_key)
    if not isinstance(policies,dict) or not policies:
        raise ValueError(f'缺少原生 PI 权限策略：{policy_key}')
    policy_values=list(policies.values())
    if any(not isinstance(value,str) or not value or set(value)-set('0123') for value in policy_values):
        raise ValueError(f'PI 权限策略格式无效：{policy_key}')
    # Different catalog revisions can disagree on unrelated PI options.
    # Resolve conflicts per selected option, rather than rejecting a role whose
    # recipe selects no PI or only options that are identical in every version.
    bits=0
    seen=set()
    for pair in pis:
        if not isinstance(pair,list) or len(pair)!=2: raise ValueError('PI 项必须是 [group, option]')
        key=(str(pair[0]),str(pair[1]))
        if key in seen: raise ValueError(f'PI 项重复：{key[0]}={key[1]}')
        seen.add(key)
        if key not in PI_MAP: raise ValueError(f'个人指令尚未建立离线映射：{key[0]}={key[1]}')
        option_id=PI_MAP[key]
        if any(option_id>=len(value) for value in policy_values):
            raise ValueError(f'PI 选项 ID 超出角色权限表：{key[0]}={key[1]}')
        option_states={value[option_id] for value in policy_values}
        if len(option_states)!=1:
            raise ValueError(f'该 PI 在目录版本间权限冲突，拒绝猜测：{policy_key} / option={option_id}')
        # Catalog provenance: 0=editable, 1=unavailable, 2=fixed off, 3=fixed on.
        state=next(iter(option_states))
        if state=='1': raise ValueError(f'该角色/阶段/位置不提供此 PI：{policy_key} / {key[0]}={key[1]}')
        if state=='2': raise ValueError(f'该 PI 被角色固定关闭，不能写入：{policy_key} / {key[0]}={key[1]}')
        if state=='3':
            # The role already forces this instruction on; do not serialize an override bit.
            continue
        if state!='0': raise ValueError(f'未知 PI 权限状态 {state!r}：{policy_key}')
        bits|=1<<option_id
    return bits

def update_role_entry(block:Block,role_flag:int,pi_flags:int):
    # Each PI cache entry is keyed by the active role flag (not its duty tag).
    matches=[z for z in block.items if z['key']==role_flag]
    if len(matches)>1:
        raise ValueError(f'同一角色存在重复 PI cache 项：{role_flag:#x}')
    if not matches:
        block.items.append({'key':role_flag,'mask2':pi_flags,'value':0})
    else:
        matches[0]['mask2']=pi_flags

def apply_recipe(tac:Tac,recipe:dict,catalog:dict,style_registry:dict|None=None)->dict:
    if recipe.get('v')!=1 or len(recipe.get('p',[]))!=11: raise ValueError('只支持 v=1、11 个球员槽位的 FM27 结构化战术配方')
    title=re.sub(r'[\\/:*?"<>|\x00-\x1f]','-',str(recipe.get('name') or 'FM27 Tactic')).strip(' .')
    if not title: title='FM27 Tactic'
    tac.title=title
    if not 1<=int(recipe.get('ment',0))<=7: raise ValueError('心态必须是 1–7')
    tac.hdr[2]=int(recipe['ment'])
    base=recipe.get('base',{});style_name=str(base.get('g',''))
    style_def=resolve_style_definition(style_name,style_registry)
    tac.style=style_def['tac_style_string']
    tac.quad[:]=style_def['style_code']
    tac.packed[:]=encode_ti(recipe,catalog,tac.packed)
    positions={x['id']:int(x['mask']) for x in catalog['positions']}
    roles={x['id']:x for x in catalog['roles']}
    role_elig=catalog.get('role_eligibility',{})
    by_slot={x.slot:x for x in tac.pairs}
    seen={0:set(),1:set()}
    pi_summary=[]
    for slot,spec in enumerate(recipe['p']):
        pair=by_slot[slot]
        for phase,phase_key,block in [(0,'in',pair.ip),(1,'out',pair.oop)]:
            item=spec[phase_key]
            pos=native_position_id(str(item['pos']),phase)
            if pos not in positions: raise ValueError(f'{slot} 槽位 {phase_key} 位置无原生 ID: {item["pos"]} -> {pos}')
            roleid=role_id_from_display(str(item['role']),phase,set(roles))
            role=roles[roleid]
            if int(role['phase'])!=phase: raise ValueError('角色阶段不匹配')
            if pos not in role_elig or roleid not in role_elig[pos][phase]: raise ValueError(f'{slot} 槽位角色位置不兼容：{pos}/{roleid}')
            if pos in seen[phase]: raise ValueError(f'{phase_key} 阵型重复位置：{pos}')
            seen[phase].add(pos)
            role_flag=int(role['flags'])
            if role_flag<=0 or role_flag&(role_flag-1): raise ValueError(f'角色标识不是 one-hot：{roleid}')
            duty=resolve_role_duty(roleid,item)
            if 'pi' not in item:
                raise ValueError(f'{slot} 槽位 {phase_key} 缺少必填 pi 字段；完整战术不得省略球员指令')
            pi_flags=encode_pi(item['pi'],catalog,phase,pos,roleid,duty)
            # Only use current recipe's PI options for the active role key.
            update_role_entry(block,role_flag,pi_flags)
            block.selector=positions[pos]
            block.mask=role_flag|duty
            pi_summary.append({'slot':slot,'phase':phase_key,'position':pos,'role':roleid,'pi_count':len(item['pi']),'pi_mask':hex(pi_flags),'duty':duty})
    if len(seen[0])!=11 or len(seen[1])!=11: raise ValueError('双阶段必须各有 11 个唯一位置')
    experimental_pi=[]
    for slot,spec in enumerate(recipe['p']):
        for phase_key in ('in','out'):
            for pair in spec[phase_key]['pi']:
                key=(str(pair[0]),str(pair[1]))
                if key in EXPERIMENTAL_PI_MAP:
                    experimental_pi.append({'slot':slot,'phase':phase_key,'group':key[0],'option':key[1],'native_option_id':EXPERIMENTAL_PI_MAP[key]})
    experimental_ti=[{'group':key[0],'option':key[1],'native_bit':bit} for key,bit in EXPERIMENTAL_TI_MAP.items() if recipe.get('ti',{}).get(key[0])==key[1]]
    return {'name':title,'style':style_name,'tac_style_string':style_def['tac_style_string'],'style_code_hex':style_def['style_code'].hex(),'template_name':style_def['template'],'mentality':recipe['ment'],'team_instruction_bits':[i for i in range(96) if tac.packed[i//8]>>(i%8)&1],'players':pi_summary,'experimental_mappings':{'status':'game_import_display_verified_match_unverified','player_instructions':experimental_pi,'team_instructions':experimental_ti}}

# ---- native archive layout and emission -------------------------------------------------
def verify_recipe_roundtrip(tac:Tac,recipe:dict,catalog:dict)->dict:
    positions={int(x['mask']):x['id'] for x in catalog['positions']}
    roles={x['id']:x for x in catalog['roles']}
    role_by_flag_phase={(int(x['flags']),int(x['phase'])):x['id'] for x in catalog['roles']}
    by_slot={x.slot:x for x in tac.pairs}
    seen={0:set(),1:set()};checked=[]
    for slot,spec in enumerate(recipe['p']):
        pair=by_slot[slot]
        for phase,key,block in ((0,'in',pair.ip),(1,'out',pair.oop)):
            wanted_pos=native_position_id(str(spec[key]['pos']),phase)
            wanted_role=role_id_from_display(str(spec[key]['role']),phase,set(roles))
            wanted_duty=resolve_role_duty(wanted_role,spec[key])
            wanted_pi=encode_pi(spec[key].get('pi',[]),catalog,phase,wanted_pos,wanted_role,wanted_duty)
            got_pos=positions.get(block.selector)
            got_role=role_by_flag_phase.get((block.mask & ROLE_MASK,phase))
            got_duty=block.mask & ~ROLE_MASK
            role_flag=int(roles[wanted_role]['flags'])
            active_entries=[x for x in block.items if x['key']==role_flag]
            if len(active_entries)!=1:
                raise ValueError(f'原生 TAC 活跃角色 PI cache 数量错误：slot {slot} {key}; count={len(active_entries)}')
            got_pi=active_entries[0]['mask2']
            if got_pos!=wanted_pos or got_role!=wanted_role or got_pi!=wanted_pi:
                raise ValueError(f'原生 TAC 回读不一致：slot {slot} {key}; pos={got_pos}/{wanted_pos}; role={got_role}/{wanted_role}; PI={got_pi:#x}/{wanted_pi:#x}')
            if got_duty not in DUTY_FLAGS:
                raise ValueError(f'回读 duty 标记无效：slot {slot} {key}: {got_duty}')
            if got_duty != wanted_duty:
                raise ValueError(f'原生 TAC 职责回读不一致：slot {slot} {key}; duty={got_duty}/{wanted_duty}')
            if got_pos in seen[phase]: raise ValueError(f'回读阵型有重复位置：phase={phase}, pos={got_pos}')
            seen[phase].add(got_pos)
            checked.append({'slot':slot,'phase':key,'position':got_pos,'role':got_role,'pi_mask':hex(got_pi),'duty':got_duty})
    if len(seen[0])!=11 or len(seen[1])!=11: raise ValueError('回读阵型不是 11+11 个唯一位置')
    return {'verified_slots':checked,'ip_unique_positions':11,'oop_unique_positions':11}

def parse_gen1(path:Path)->dict:
    """Decode the legacy FM27GEN1:Base64 JSON transport format."""
    text=path.read_text(encoding='utf-8-sig').strip()
    if not text.startswith('FM27GEN1:'): raise ValueError('旧版 GEN1 输入缺少 FM27GEN1: 前缀')
    recipe=json.loads(base64.b64decode(text.split(':',1)[1],validate=True).decode('utf-8'))
    if not isinstance(recipe,dict): raise ValueError('GEN1 解码结果必须是 JSON 对象')
    return recipe

def load_recipe_input(path:Path)->tuple[dict,str]:
    """Load the native structured JSON recipe; retain GEN1 TXT only for compatibility."""
    suffix=path.suffix.lower()
    if suffix=='.json':
        recipe=json.loads(path.read_text(encoding='utf-8-sig'))
        input_format='json'
    elif suffix=='.txt':
        recipe=parse_gen1(path)
        input_format='legacy_gen1_base64'
    else:
        raise ValueError('输入文件必须使用 .json（原生结构化配方）或 .txt（旧版 GEN1 兼容格式）')
    if not isinstance(recipe,dict):
        raise ValueError('战术配方根节点必须是 JSON 对象')
    return recipe,input_format

def validate_recipe_structure(recipe: dict) -> None:
    """Reject malformed or silently ignored fields before native encoding starts."""
    allowed_root = {'v', 'name', 'ment', 'base', 'ti', 'p'}
    required_root = {'v', 'ment', 'base', 'p'}
    unknown_root = set(recipe) - allowed_root
    missing_root = required_root - set(recipe)
    if unknown_root:
        raise ValueError(f'战术配方包含未知根字段：{sorted(unknown_root)}')
    if missing_root:
        raise ValueError(f'战术配方缺少必需根字段：{sorted(missing_root)}')
    if isinstance(recipe['v'], bool) or not isinstance(recipe['v'], int) or recipe['v'] != 1:
        raise ValueError('配方版本 v 必须是整数 1')
    if 'name' in recipe and not isinstance(recipe['name'], str):
        raise ValueError('name 必须是字符串')
    if isinstance(recipe['ment'], bool) or not isinstance(recipe['ment'], int) or not 1 <= recipe['ment'] <= 7:
        raise ValueError('心态 ment 必须是 1–7 的整数')

    base = recipe['base']
    if not isinstance(base, dict):
        raise ValueError('base 必须是对象')
    unknown_base = set(base) - {'g'}
    if unknown_base:
        raise ValueError(f'base 包含未知字段：{sorted(unknown_base)}')
    if not isinstance(base.get('g'), str) or not base['g'].strip():
        raise ValueError('base.g 必须是非空风格名称字符串')

    ti = recipe.get('ti', {})
    if not isinstance(ti, dict):
        raise ValueError('ti 必须是对象')
    for key, value in ti.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError('ti 的组名和值都必须是字符串')

    players = recipe['p']
    if not isinstance(players, list) or len(players) != 11:
        raise ValueError('p 必须是恰好包含 11 个槽位的数组')
    for slot, spec in enumerate(players):
        if not isinstance(spec, dict):
            raise ValueError(f'p[{slot}] 必须是对象')
        if set(spec) != {'in', 'out'}:
            raise ValueError(f'p[{slot}] 只能包含 in 和 out 两个阶段对象')
        for phase_key in ('in', 'out'):
            item = spec[phase_key]
            if not isinstance(item, dict):
                raise ValueError(f'p[{slot}].{phase_key} 必须是对象')
            allowed_phase = {'pos', 'role', 'pi', 'duty'}
            required_phase = {'pos', 'role', 'pi'}
            unknown_phase = set(item) - allowed_phase
            missing_phase = required_phase - set(item)
            if unknown_phase:
                raise ValueError(f'p[{slot}].{phase_key} 包含未知字段：{sorted(unknown_phase)}')
            if missing_phase:
                raise ValueError(f'p[{slot}].{phase_key} 缺少必需字段：{sorted(missing_phase)}')
            for field in ('pos', 'role'):
                if not isinstance(item[field], str) or not item[field].strip():
                    raise ValueError(f'p[{slot}].{phase_key}.{field} 必须是非空字符串')
            if not isinstance(item['pi'], list):
                raise ValueError(f'p[{slot}].{phase_key}.pi 必须是数组')
            for pi_index, pair in enumerate(item['pi']):
                if (not isinstance(pair, list) or len(pair) != 2 or
                        any(not isinstance(value, str) or not value.strip() for value in pair)):
                    raise ValueError(f'p[{slot}].{phase_key}.pi[{pi_index}] 必须是 [group, option] 字符串数组')
            if 'duty' in item and (isinstance(item['duty'], bool) or not isinstance(item['duty'], (str, int))):
                raise ValueError(f'p[{slot}].{phase_key}.duty 必须是 D/S/A 名称或原生整数 bit')

def build_fmf_from_recipe(
    recipe: dict,
    catalog: dict,
    style_registry: dict | None = None,
    template_path: Path | None = None,
    *,
    recipe_input_format: str = 'python_dict',
    recipe_source: str = '<python_dict>',
) -> tuple[bytes, dict]:
    """Build and independently read back a native FM27 FMF directly from a Python dict.

    This is the primary in-process API. Callers that already have a structured
    tactic object do not need to serialize it to JSON or wrap it in GEN1 first.
    The CLI and cloud workflow use this same function after loading their input.
    """
    if not isinstance(recipe, dict):
        raise ValueError('战术配方必须是 Python dict / JSON object')
    validate_recipe_structure(recipe)
    if not isinstance(catalog, dict):
        raise ValueError('catalog 必须是对象')

    if style_registry is None:
        registry_file = HERE / 'style_template_registry.json'
        if registry_file.is_file():
            style_registry = json.loads(registry_file.read_text(encoding='utf-8'))

    base = recipe.get('base', {})
    if not isinstance(base, dict):
        raise ValueError('base 必须是对象，且包含原生风格字段 g')
    style_name = str(base.get('g', ''))
    resolved_template = resolve_template_path(style_name, style_registry, template_path)
    source = resolved_template.read_bytes()
    fmf = parse_fmf(source)
    if '.tac' not in fmf.data_by_ext or '.aom' not in fmf.data_by_ext or '.img' not in fmf.data_by_ext:
        raise ValueError('原生 FMF 缺少 .tac/.aom/.img 成员')

    tac = parse_tac(fmf.data_by_ext['.tac'])
    if fmf.data_by_ext['.tac'][11] != 27:
        raise ValueError('模板不是 FM27 source-major 27 原生战术；请在 FM27 游戏中重新导出')

    before = {
        'pairs': len(tac.pairs),
        'ids': len(tac.ids),
        'lists': len(tac.lists),
        'footer_records': len(tac.records),
        'tac_bytes': len(fmf.data_by_ext['.tac']),
    }
    summary = apply_recipe(tac, recipe, catalog, style_registry)
    if summary.get('template_name'):
        expected = (HERE / summary['template_name']).resolve()
        if resolved_template != expected:
            raise ValueError(
                f'风格 {summary["style"]} 要求使用登记模板 {expected}，当前为 {resolved_template}'
            )

    tac_bytes = write_tac(tac)
    reparsed = parse_tac(tac_bytes)
    if reparsed.title != summary['name'] or len(reparsed.pairs) != 11:
        raise ValueError('写入后的 TAC 自检失败')
    output = write_fmf(fmf, tac_bytes, summary['name'])

    # Full independent read-after-write: outer archive -> member decrypt -> TAC parse.
    verify = parse_fmf(output)
    verified_tac = parse_tac(verify.data_by_ext['.tac'])
    readback = verify_recipe_roundtrip(verified_tac, recipe, catalog)
    if verified_tac.title != summary['name'] or verify.root_title != summary['name']:
        raise ValueError('输出标题回读不一致')
    if verified_tac.style != summary['tac_style_string'] or bytes(verified_tac.quad).hex() != summary['style_code_hex']:
        raise ValueError('原生风格字符串/四字节 style code 回读不一致')
    if bytes(verified_tac.packed) != bytes(tac.packed):
        raise ValueError('球队指令回读不一致')
    if len(verified_tac.pairs) != 11 or len(verified_tac.records) != 12:
        raise ValueError('输出球员槽位或 footer 数量不一致')

    digest = hashlib.sha256(output).hexdigest()
    report = {
        'status': 'offline_binary_roundtrip_verified_not_game_import_verified',
        'output': None,
        'sha256': digest,
        'bytes': len(output),
        'template': str(resolved_template),
        'template_sha256': hashlib.sha256(source).hexdigest(),
        'recipe': recipe_source,
        'recipe_input_format': recipe_input_format,
        'name': summary['name'],
        'style': summary['style'],
        'tac_style_string': summary['tac_style_string'],
        'style_code_hex': summary['style_code_hex'],
        'mentality': summary['mentality'],
        'team_instruction_bits': summary['team_instruction_bits'],
        'experimental_mappings': summary['experimental_mappings'],
        'source_template_version': 27,
        'opaque_sections_preserved': {
            'id_entries': before['ids'],
            'footer_lists': before['lists'],
            'footer_records': before['footer_records'],
            'image_member': 'byte_identical',
        },
        'player_phase_map': summary['players'],
        'readback_player_phase_map': readback['verified_slots'],
        'checks': {
            'fmf_outer_roundtrip': True,
            'all_member_decrypt_and_zstd_checksums': True,
            'tac_full_parse': True,
            '11_ip_oop_pairs': True,
            '22_positions_roles_pi_readback_exact': True,
            'pi_permissions_checked_against_catalog': True,
            'team_instruction_vector_readback': True,
            'native_style_string_and_code_readback': True,
            'game_interactive_import': False,
            'match_engine': False,
        },
        'notes': [
            '通过结构化 Python dict 生成原生 FMF，并执行独立二进制回读。',
            'D/S/A 到 native duty bit 的编码由 FM27 TAC 样本确认；配方可在阶段对象中显式指定 duty，映射表未提供默认值的角色必须明确指定。',
            'PI 权限按指定的 phase/position/role/duty 目录策略检查。',
            '只有结构/自解包核验；必须由用户在 FM27 内手动导入后才能确认游戏接受。',
        ],
    }
    return output, report


def main():
    ap = argparse.ArgumentParser(description='FM27 结构化战术配方离线生成原生 FMF')
    ap.add_argument('recipe', type=Path, help='原生 JSON 配方；旧版 GEN1 TXT 仅作兼容输入')
    ap.add_argument('--template', type=Path, help='可选：覆盖登记表中的原生 .fmf 模板；默认按战术风格自动选择')
    ap.add_argument('--catalog', type=Path, required=True, help='本机 FM27 catalog.json')
    ap.add_argument('--output', type=Path, required=True, help='新 FMF 输出路径')
    ap.add_argument('--report', type=Path, help='JSON 验证报告路径')
    ap.add_argument('--style-registry', type=Path, default=Path(__file__).with_name('style_template_registry.json'), help='原生风格/模板登记表')
    args = ap.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError('拒绝覆盖已有输出文件：' + str(args.output))
        catalog = json.loads(args.catalog.read_text(encoding='utf-8'))
        style_registry = json.loads(args.style_registry.read_text(encoding='utf-8')) if args.style_registry.is_file() else None
        recipe, input_format = load_recipe_input(args.recipe)
        output, report = build_fmf_from_recipe(
            recipe,
            catalog,
            style_registry,
            args.template,
            recipe_input_format=input_format,
            recipe_source=str(args.recipe),
        )
        out = args.output.expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(output)
        report['output'] = str(out)
        report['style_registry'] = str(args.style_registry)
        report_path = args.report or out.with_suffix('.report.json')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        print(f'失败：{type(e).__name__}: {e}', file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())