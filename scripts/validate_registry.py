#!/usr/bin/env python3
from pathlib import Path
from registry import archives
from registry_metadata import load_metadata
from generate_api import render_files as render_api_files
from generate_search import render as render_search
ROOT=Path(__file__).resolve().parents[1]
def main():
    pkgs=archives(ROOT)
    names={p.name for p in pkgs}
    rows=[line.split() for line in (ROOT/'index.txt').read_text(encoding='utf-8').splitlines() if line.strip()]
    if any(len(r) not in (4,6) for r in rows): raise SystemExit('index.txt contains a malformed row')
    active=[]
    for p in pkgs:
        meta=load_metadata(ROOT,p.name)
        if not meta.owners: raise SystemExit(f'metadata/{p.name}.json must have at least one owner')
        if p.version not in meta.yanked: active.append(p)
    for name in names:
        meta=load_metadata(ROOT,name)
        known={p.version for p in pkgs if p.name==name}
        unknown=sorted(meta.yanked-known)
        if unknown: raise SystemExit(f'metadata/{name}.json yanks unknown versions: {unknown}')
    expected={(p.name,p.version,p.path.relative_to(ROOT).as_posix(),p.checksum) for p in active}
    projected={(a,b,c,d) for a,b,c,d,*rest in rows}
    if projected!=expected: raise SystemExit('index.txt does not exactly describe active (non-yanked) packages/')
    api_root=ROOT/'api'/'v1'; expected_api=render_api_files(); actual_api={p.relative_to(api_root).as_posix():p.read_bytes() for p in api_root.rglob('*') if p.is_file()} if api_root.exists() else {}
    if actual_api!=expected_api: raise SystemExit('api/v1 does not exactly describe packages/ + metadata/')
    expected_search=render_search(); actual_search=(ROOT/'search.txt').read_text(encoding='utf-8') if (ROOT/'search.txt').exists() else ''
    if actual_search!=expected_search: raise SystemExit('search.txt does not exactly describe active package metadata')
    print(f'registry validation: PASS ({len(pkgs)} package versions; {len(active)} active; {len(expected_api)} API documents; {len([x for x in expected_search.splitlines() if x])} searchable packages)'); return 0
if __name__=='__main__': raise SystemExit(main())
