#!/usr/bin/env python3
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PackageMetadata:
    name: str
    owners: tuple[str, ...]
    yanked: frozenset[str]


def load_metadata(root: Path, name: str) -> PackageMetadata:
    path = root / 'metadata' / f'{name}.json'
    if not path.exists():
        return PackageMetadata(name, tuple(), frozenset())
    raw = json.loads(path.read_text(encoding='utf-8'))
    if raw.get('name') != name:
        raise ValueError(f'{path}: metadata name must be {name!r}')
    owners = raw.get('owners', [])
    yanked = raw.get('yanked', [])
    if not isinstance(owners, list) or not all(isinstance(v, str) and v for v in owners):
        raise ValueError(f'{path}: owners must be a non-empty-string array')
    if len(set(owners)) != len(owners):
        raise ValueError(f'{path}: duplicate owner')
    if not isinstance(yanked, list) or not all(isinstance(v, str) and v for v in yanked):
        raise ValueError(f'{path}: yanked must be a semantic-version string array')
    if len(set(yanked)) != len(yanked):
        raise ValueError(f'{path}: duplicate yanked version')
    return PackageMetadata(name, tuple(owners), frozenset(yanked))


def write_metadata(root: Path, metadata: PackageMetadata) -> None:
    path = root / 'metadata' / f'{metadata.name}.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        'name': metadata.name,
        'owners': sorted(metadata.owners),
        'yanked': sorted(metadata.yanked),
    }
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + '\n', encoding='utf-8')
