#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")

@dataclass(frozen=True)
class PackageArchive:
    name: str
    version: str
    path: Path
    checksum: str


def decode_archive(path: Path) -> dict[str, bytes]:
    data = path.read_bytes()
    lines = data.splitlines()
    if not lines or lines[0] != b"RAZPKG1":
        raise ValueError(f"{path}: missing RAZPKG1 header")
    files: dict[str, bytes] = {}
    for number, raw in enumerate(lines[1:], 2):
        if not raw:
            continue
        parts = raw.split(b" ", 2)
        if len(parts) != 3 or parts[0] != b"F":
            raise ValueError(f"{path}:{number}: malformed archive record")
        try:
            rel = bytes.fromhex(parts[1].decode("ascii")).decode("utf-8")
            content = bytes.fromhex(parts[2].decode("ascii"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError(f"{path}:{number}: invalid hexadecimal archive record") from exc
        pure = Path(rel)
        if not rel or pure.is_absolute() or ".." in pure.parts or "\\" in rel:
            raise ValueError(f"{path}:{number}: unsafe package path {rel!r}")
        normalized = pure.as_posix()
        if normalized in files:
            raise ValueError(f"{path}:{number}: duplicate package path {normalized!r}")
        files[normalized] = content
    if "raz.toml" not in files:
        raise ValueError(f"{path}: archive has no raz.toml")
    return files


def tree_hash(files: dict[str, bytes]) -> str:
    value = 1469598103934665603
    mask = (1 << 64) - 1
    for rel in sorted(files):
        payload = rel.encode("utf-8") + b"\0" + files[rel] + b"\xff"
        for byte in payload:
            value = ((value ^ byte) * 1099511628211) & mask
    return f"{value:016x}"


def manifest_identity(data: bytes) -> tuple[str, str]:
    text = data.decode("utf-8")
    in_package = False
    name = ""
    version = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_package = line == "[package]"
            continue
        if not in_package or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        if key == "name":
            name = value
        elif key == "version":
            version = value
    if not name or not version:
        raise ValueError("raz.toml must define [package] name and version")
    return name, version


def inspect_archive(root: Path, path: Path) -> PackageArchive:
    rel = path.relative_to(root).as_posix()
    parts = path.relative_to(root / "packages").parts
    if len(parts) != 2:
        raise ValueError(f"{rel}: expected packages/<name>/<version>.dpk")
    directory_name, filename = parts
    if not filename.endswith(".dpk"):
        raise ValueError(f"{rel}: expected .dpk archive")
    path_version = filename[:-4]
    if not NAME_RE.fullmatch(directory_name):
        raise ValueError(f"{rel}: invalid package name")
    if not VERSION_RE.fullmatch(path_version):
        raise ValueError(f"{rel}: invalid semantic version")
    files = decode_archive(path)
    manifest_name, manifest_version = manifest_identity(files["raz.toml"])
    if manifest_name != directory_name or manifest_version != path_version:
        raise ValueError(
            f"{rel}: path identity {directory_name}@{path_version} does not match "
            f"raz.toml {manifest_name}@{manifest_version}"
        )
    return PackageArchive(directory_name, path_version, path, tree_hash(files))


def archives(root: Path) -> list[PackageArchive]:
    result = [inspect_archive(root, p) for p in sorted((root / "packages").glob("*/*.dpk"))]
    identities = [(pkg.name, pkg.version) for pkg in result]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate package name/version identity")
    return result
