#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path

from registry import archives, decode_archive, manifest_identity
from registry_metadata import load_metadata

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / 'api' / 'v1'


def manifest_metadata(data: bytes) -> dict[str, str]:
    result: dict[str, str] = {}
    in_package = False
    for raw in data.decode('utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('[') and line.endswith(']'):
            in_package = line == '[package]'
            continue
        if not in_package or '=' not in line:
            continue
        key, value = (part.strip() for part in line.split('=', 1))
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        if key in {'name', 'version', 'description', 'license', 'repository', 'homepage'}:
            result[key] = value
    return result



def readme_description(data: bytes) -> str:
    for raw in data.decode('utf-8', errors='replace').splitlines():
        line=' '.join(raw.replace('\t',' ').strip().split())
        if line and not line.startswith('#') and not line.startswith('>') and not line.startswith('```'):
            return line
    return ''

def render_files() -> dict[str, bytes]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    package_rows: list[dict[str, object]] = []
    output: dict[str, bytes] = {}

    for archive in archives(ROOT):
        files = decode_archive(archive.path)
        name, version = manifest_identity(files['raz.toml'])
        metadata = manifest_metadata(files['raz.toml'])
        if not metadata.get('description') and 'README.md' in files:
            description=readme_description(files['README.md'])
            if description: metadata['description']=description
        registry_meta = load_metadata(ROOT, name)
        rel = archive.path.relative_to(ROOT).as_posix()
        raw_url = f'https://raw.githubusercontent.com/raz-language/packages/main/{rel}'
        version_row: dict[str, object] = {
            'name': name,
            'version': version,
            'checksum': archive.checksum,
            'archive': rel,
            'download': raw_url,
            'yanked': version in registry_meta.yanked,
            'owners': list(registry_meta.owners),
            'metadata': {k: v for k, v in metadata.items() if k not in {'name', 'version'}},
        }
        grouped[name].append(version_row)
        output[f'packages/{name}/{version}.json'] = (json.dumps(version_row, indent=2, sort_keys=True) + '\n').encode()

    for name in sorted(grouped):
        versions = sorted(grouped[name], key=lambda row: str(row['version']))
        registry_meta = load_metadata(ROOT, name)
        package_row = {'name': name, 'owners': list(registry_meta.owners), 'versions': versions}
        latest_row = next((row for row in reversed(versions) if not row['yanked']), None)
        latest_metadata = latest_row['metadata'] if latest_row is not None else {}
        package_rows.append({
            'name': name,
            'owners': list(registry_meta.owners),
            'versions': [row['version'] for row in versions],
            'latest': latest_row['version'] if latest_row is not None else None,
            'description': latest_metadata.get('description', ''),
            'license': latest_metadata.get('license', ''),
        })
        output[f'packages/{name}.json'] = (json.dumps(package_row, indent=2, sort_keys=True) + '\n').encode()

    index = {
        'schema': 'raz-registry-v1',
        'registry': 'raz-language/packages',
        'packages': package_rows,
    }
    output['index.json'] = (json.dumps(index, indent=2, sort_keys=True) + '\n').encode()
    return output


def current_files() -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    if not API_ROOT.exists(): return result
    for path in sorted(p for p in API_ROOT.rglob('*') if p.is_file()):
        result[path.relative_to(API_ROOT).as_posix()] = path.read_bytes()
    return result


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    expected=render_files()
    if args.check:
        actual=current_files()
        if actual!=expected:
            missing=sorted(set(expected)-set(actual)); extra=sorted(set(actual)-set(expected)); changed=sorted(k for k in set(actual)&set(expected) if actual[k]!=expected[k])
            details=[]
            if missing: details.append('missing='+','.join(missing[:8]))
            if extra: details.append('extra='+','.join(extra[:8]))
            if changed: details.append('changed='+','.join(changed[:8]))
            raise SystemExit('api/v1 is stale; run python scripts/generate_api.py'+((' ('+'; '.join(details)+')') if details else ''))
        print(f'registry api: PASS ({len(expected)} generated documents)'); return 0
    shutil.rmtree(API_ROOT,ignore_errors=True)
    for rel,data in expected.items():
        path=API_ROOT/rel; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
    print(f'wrote {API_ROOT} ({len(expected)} documents)'); return 0
if __name__=='__main__': raise SystemExit(main())
