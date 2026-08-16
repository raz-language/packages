#!/usr/bin/env python3
from pathlib import Path
from registry import archives
ROOT=Path(__file__).resolve().parents[1]
def main():
    pkgs=archives(ROOT); rows=[line.split() for line in (ROOT/"index.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    if any(len(r) not in (4,6) for r in rows): raise SystemExit("index.txt contains a malformed row")
    expected={(p.name,p.version,p.path.relative_to(ROOT).as_posix(),p.checksum) for p in pkgs}; projected={(a,b,c,d) for a,b,c,d,*rest in rows}
    if projected!=expected: raise SystemExit("index.txt does not exactly describe packages/")
    print(f"registry validation: PASS ({len(pkgs)} package versions)"); return 0
if __name__=="__main__": raise SystemExit(main())
