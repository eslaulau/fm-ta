#!/usr/bin/env python3
"""Recreate the exact V0.5 FMF bytes embedded in the archived native snapshot."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
SNAPSHOT = PROJECT_DIR / "V0.5_NATIVE_SNAPSHOT.json"
EXPECTED_SHA256 = "e9a82cf273187b20567c38e25f362e7aed4e2a38ac525789c69d7abf641c7257"
EXPECTED_SIZE = 4214


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize and verify the immutable V0.5 reset baseline.")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_DIR / "builds" / "V0.5.fmf",
        help="Output FMF path (default: project/builds/V0.5.fmf).",
    )
    args = parser.parse_args()

    if not SNAPSHOT.is_file():
        raise FileNotFoundError(f"V0.5 native snapshot is missing: {SNAPSHOT}")
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite existing baseline file: {args.output}")

    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    identity = snapshot.get("identity", {})
    encoded = snapshot.get("native_preservation", {}).get("source_fmf_base64")
    if not isinstance(encoded, str) or not encoded:
        raise ValueError("Snapshot does not contain native_preservation.source_fmf_base64.")
    if identity.get("source_sha256") != EXPECTED_SHA256:
        raise ValueError("Snapshot identity SHA-256 does not match the fixed V0.5 baseline.")
    if identity.get("source_size_bytes") != EXPECTED_SIZE:
        raise ValueError("Snapshot identity size does not match the fixed V0.5 baseline.")

    raw = base64.b64decode(encoded, validate=True)
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise ValueError(
            f"Embedded V0.5 FMF integrity failure: bytes={len(raw)}, sha256={actual_sha}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print(f"V0.5_BASELINE_READY: {args.output}")
    print(f"BYTES: {len(raw)}")
    print(f"SHA256: {actual_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
