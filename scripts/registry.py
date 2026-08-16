#!/usr/bin/env python3
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
NAME_RE=re.compile(r"^[a-z0-9][a-z0-9_-]*$")
VERSION_RE=re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
@dataclass(frozen=True)
class PackageArchive:
    name:str; version:str; path:Path; checksum:str
def decode_archive(path:Path)->dict[str,bytes]:
    lines=path.read_bytes().splitlines()
    if not lines or lines[0]!=b"RAZPKG1": raise ValueError(f"{path}: missing RAZPKG1 header")
    files={}
    for number,raw in enumerate(lines[1:],2):
        if not raw: continue
        parts=raw.split(b" ",2)
        if len(parts)!=3 or parts[0]!=b"F": raise ValueError(f"{path}:{number}: malformed archive record")
        rel=bytes.fromhex(parts[1].decode("ascii")).decode("utf-8"); content=bytes.fromhex(parts[2].decode("ascii")); pure=Path(rel)
        if not rel or pure.is_absolute() or ".." in pure.parts or "\\" in rel: raise ValueError(f"{path}:{number}: unsafe package path {rel!r}")
        normalized=pure.as_posix()
        if normalized in files: raise ValueError(f"{path}:{number}: duplicate package path {normalized!r}")
        files[normalized]=content
    if "raz.toml" not in files: raise ValueError(f"{path}: archive has no raz.toml")
    return files
def tree_hash(files:dict[str,bytes])->str:
    value=1469598103934665603; mask=(1<<64)-1
    for rel in sorted(files):
        for byte in rel.encode("utf-8")+b"\0"+files[rel]+b"\xff": value=((value^byte)*1099511628211)&mask
    return f"{value:016x}"
def manifest_identity(data:bytes)->tuple[str,str]:
    in_package=False; name=""; version=""
    for raw in data.decode("utf-8").splitlines():
        line=raw.strip()
        if not line or line.startswith("#"): continue
        if line.startswith("[") and line.endswith("]"): in_package=line=="[package]"; continue
        if not in_package or "=" not in line: continue
        key,value=(part.strip() for part in line.split("=",1))
        if len(value)>=2 and value[0]==value[-1]=='"': value=value[1:-1]
        if key=="name": name=value
        elif key=="version": version=value
    if not name or not version: raise ValueError("raz.toml must define [package] name and version")
    return name,version
def inspect_archive(root:Path,path:Path)->PackageArchive:
    rel=path.relative_to(root).as_posix(); parts=path.relative_to(root/"packages").parts
    if len(parts)!=2: raise ValueError(f"{rel}: expected packages/<name>/<version>.dpk")
    name,filename=parts; version=filename[:-4] if filename.endswith(".dpk") else ""
    if not NAME_RE.fullmatch(name): raise ValueError(f"{rel}: invalid package name")
    if not VERSION_RE.fullmatch(version): raise ValueError(f"{rel}: invalid semantic version")
    files=decode_archive(path); mn,mv=manifest_identity(files["raz.toml"])
    if (mn,mv)!=(name,version): raise ValueError(f"{rel}: path identity {name}@{version} does not match raz.toml {mn}@{mv}")
    return PackageArchive(name,version,path,tree_hash(files))
def archives(root:Path)->list[PackageArchive]:
    result=[inspect_archive(root,p) for p in sorted((root/"packages").glob("*/*.dpk"))]
    ids=[(p.name,p.version) for p in result]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate package name/version identity")
    return result
