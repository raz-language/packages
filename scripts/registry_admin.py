#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from registry import archives
from registry_metadata import PackageMetadata, load_metadata, write_metadata
ROOT=Path(__file__).resolve().parents[1]

def known_versions(name:str)->set[str]: return {p.version for p in archives(ROOT) if p.name==name}

def main()->int:
    ap=argparse.ArgumentParser(description='Edit mutable Raz registry metadata; commit changes through GitHub normally.')
    sub=ap.add_subparsers(dest='cmd',required=True)
    for cmd in ('yank','unyank'):
        p=sub.add_parser(cmd); p.add_argument('package'); p.add_argument('version')
    for cmd in ('owner-add','owner-remove'):
        p=sub.add_parser(cmd); p.add_argument('package'); p.add_argument('owner')
    args=ap.parse_args(); versions=known_versions(args.package)
    if not versions: raise SystemExit(f'unknown package: {args.package}')
    meta=load_metadata(ROOT,args.package); owners=list(meta.owners); yanked=set(meta.yanked)
    if args.cmd in ('yank','unyank'):
        if args.version not in versions: raise SystemExit(f'unknown version: {args.package}@{args.version}')
        if args.cmd=='yank': yanked.add(args.version)
        else: yanked.discard(args.version)
    elif args.cmd=='owner-add':
        if args.owner not in owners: owners.append(args.owner)
    else:
        owners=[o for o in owners if o!=args.owner]
        if not owners: raise SystemExit('a package must retain at least one owner')
    write_metadata(ROOT,PackageMetadata(args.package,tuple(owners),frozenset(yanked)))
    print(f'updated metadata/{args.package}.json')
    return 0
if __name__=='__main__': raise SystemExit(main())
