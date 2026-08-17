#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from registry import archives, decode_archive
from registry_metadata import load_metadata
from generate_api import manifest_metadata
ROOT=Path(__file__).resolve().parents[1]

def clean(value:str)->str:
    return ' '.join(value.replace('\t',' ').replace('\r',' ').replace('\n',' ').split())

def semver_key(value:str):
    core=value.split('-',1)[0].split('+',1)[0]
    nums=core.split('.')
    try: return tuple(int(x) for x in nums[:3])
    except ValueError: return (0,0,0)

def render()->str:
    grouped={}
    for a in archives(ROOT):
        meta=load_metadata(ROOT,a.name)
        if a.version in meta.yanked: continue
        prev=grouped.get(a.name)
        if prev is None or semver_key(a.version)>semver_key(prev.version): grouped[a.name]=a
    lines=[]
    for name in sorted(grouped):
        a=grouped[name]; files=decode_archive(a.path); mm=manifest_metadata(files['raz.toml']); rm=load_metadata(ROOT,name)
        owners=','.join(rm.owners)
        desc=clean(mm.get('description',''))
        if not desc and 'README.md' in files:
            for raw in files['README.md'].decode('utf-8', errors='replace').splitlines():
                line=clean(raw)
                if line and not line.startswith('#') and not line.startswith('>') and not line.startswith('```'):
                    desc=line
                    break
        lines.append(f'{name}\t{a.version}\t{owners}\t{desc}')
    return ''.join(x+'\n' for x in lines)

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args(); expected=render(); path=ROOT/'search.txt'
    if args.check:
        actual=path.read_text(encoding='utf-8') if path.exists() else ''
        if actual!=expected: raise SystemExit('search.txt is stale; run python scripts/generate_search.py')
        print(f'registry search: PASS ({len([x for x in expected.splitlines() if x])} packages)'); return 0
    path.write_text(expected,encoding='utf-8'); print(f'wrote {path}'); return 0
if __name__=='__main__': raise SystemExit(main())
