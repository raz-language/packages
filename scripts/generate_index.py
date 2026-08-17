#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from registry import archives
from registry_metadata import load_metadata
ROOT=Path(__file__).resolve().parents[1]

def render()->str:
    lines=[]
    for p in archives(ROOT):
        meta=load_metadata(ROOT,p.name)
        # Yanked releases remain immutable/downloadable for existing lockfiles,
        # but are omitted from the resolver index so new resolution cannot select them.
        if p.version in meta.yanked:
            continue
        lines.append(f'{p.name} {p.version} {p.path.relative_to(ROOT).as_posix()} {p.checksum}')
    return ''.join(line+'\n' for line in lines)

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    expected=render(); path=ROOT/'index.txt'
    if args.check:
        actual=path.read_text(encoding='utf-8') if path.exists() else ''
        if actual!=expected: raise SystemExit('index.txt is stale; run python scripts/generate_index.py')
        print(f'registry index: PASS ({len([l for l in expected.splitlines() if l])} active versions)'); return 0
    path.write_text(expected,encoding='utf-8'); print(f'wrote {path}'); return 0
if __name__=='__main__': raise SystemExit(main())
