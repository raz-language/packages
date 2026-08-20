#!/usr/bin/env python3
"""Create immutable deterministic archives from official source packages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from registry import archives, inspect_archive, manifest_identity


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
PATH_DEPENDENCY = re.compile(
    r'^(?P<indent>\s*)(?P<name>[a-z0-9][a-z0-9_-]*)\s*=\s*"\.\./(?P<target>[a-z0-9][a-z0-9_-]*)"\s*$'
)
IGNORED_DIRECTORIES = {".git", "__pycache__", "target"}
IGNORED_FILES = {".DS_Store", "raz.lock"}


def semver_key(version: str) -> tuple[int, int, int, int, str]:
    core, separator, suffix = version.partition("-")
    numbers = core.split("+")[0].split(".")
    major, minor, patch = (int(value) for value in numbers[:3])
    return major, minor, patch, 1 if not separator else 0, suffix


def registry_checksums() -> dict[str, str]:
    latest: dict[str, tuple[str, str]] = {}

    for archive in archives(ROOT):
        previous = latest.get(archive.name)

        if previous is None or semver_key(archive.version) > semver_key(previous[0]):
            latest[archive.name] = (archive.version, archive.checksum)
    return {name: value[1] for name, value in latest.items()}


def publish_manifest(data: bytes, checksums: dict[str, str]) -> bytes:
    lines: list[str] = []

    for line in data.decode("utf-8").splitlines():
        match = PATH_DEPENDENCY.fullmatch(line)

        if match is None:
            lines.append(line)
            continue
        dependency = match.group("target")
        checksum = checksums.get(dependency)

        if checksum is None:
            raise ValueError(f"dependency {dependency!r} has no published archive")
        lines.append(f'{match.group("indent")}{match.group("name")} = "registry:{checksum}"')
    return ("\n".join(lines) + "\n").encode("utf-8")


def source_files(source: Path, checksums: dict[str, str]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}

    for path in sorted(item for item in source.rglob("*") if item.is_file()):
        relative = path.relative_to(source)

        if any(part in IGNORED_DIRECTORIES for part in relative.parts) or path.name in IGNORED_FILES:
            continue
        key = relative.as_posix()
        result[key] = path.read_bytes()
    result["raz.toml"] = publish_manifest(result["raz.toml"], checksums)
    return result


def encode(files: dict[str, bytes]) -> bytes:
    output = bytearray(b"RAZPKG1\n")

    for relative in sorted(files):
        output.extend(b"F ")
        output.extend(relative.encode("utf-8").hex().encode("ascii"))
        output.extend(b" ")
        output.extend(files[relative].hex().encode("ascii"))
        output.extend(b"\n")
    return bytes(output)


def release(name: str, checksums: dict[str, str]) -> str:
    source = SOURCES / name

    if not source.is_dir():
        raise ValueError(f"unknown official source package: {name}")
    files = source_files(source, checksums)
    manifest_name, version = manifest_identity(files["raz.toml"])

    if manifest_name != name:
        raise ValueError(f"source directory {name!r} declares package {manifest_name!r}")
    destination = ROOT / "packages" / name / f"{version}.dpk"

    if destination.exists():
        raise FileExistsError(f"published version is immutable: {destination.relative_to(ROOT)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(encode(files))
    archive = inspect_archive(ROOT, destination)
    checksums[name] = archive.checksum
    return f"published {name}@{version} ({archive.checksum})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="+", help="official source packages in dependency order")
    arguments = parser.parse_args()
    checksums = registry_checksums()

    for name in arguments.packages:
        print(release(name, checksums))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
