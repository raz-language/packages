#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from registry import archives
ROOT=Path(__file__).resolve().parents[1]
def render():
    lines=[f"{p.name} {p.version} {p.path.relative_to(ROOT).as_posix()} {p.checksum}" for p in archives(ROOT)]
    return "\n".join(lines)+("\n" if lines else "")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args(); expected=render(); path=ROOT/"index.txt"; current=path.read_text(encoding="utf-8") if path.exists() else ""
    if args.check:
        if current!=expected: raise SystemExit("index.txt is stale; run python scripts/generate_index.py")
        print(f"registry index: PASS ({len(expected.splitlines())} versions)"); return 0
    path.write_text(expected,encoding="utf-8"); print(f"wrote {path} ({len(expected.splitlines())} versions)"); return 0
if __name__=="__main__": raise SystemExit(main())
