#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from registry import archives

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    packages = archives(ROOT)
    index = ROOT / "index.txt"
    rows = [line.split() for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]
    if any(len(row) not in (4, 6) for row in rows):
        raise SystemExit("index.txt contains a malformed row")
    indexed = {(row[0], row[1], row[2], row[3]) for row in rows}
    expected = {
        (p.name, p.version, p.path.relative_to(ROOT).as_posix(), p.checksum)
        for p in packages
    }
    projected = {(a, b, c, d) for a, b, c, d, *rest in rows}
    if projected != expected:
        raise SystemExit("index.txt does not exactly describe packages/")
    print(f"registry validation: PASS ({len(packages)} package versions)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
