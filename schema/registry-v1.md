# Raz Registry v1

The canonical registry is a static repository served over HTTPS.

## Index

`index.txt` is UTF-8 text. Each non-empty line has four required whitespace-separated fields and two optional signing fields:

```text
<name> <version> <archive-path> <tree-checksum> [key-id signature]
```

Example:

```text
json 1.4.2 packages/json/1.4.2.dpk 0123456789abcdef
```

The index is generated; package submissions should not hand-edit records.

## Archives

A `.dpk` is Raz's deterministic `RAZPKG1` archive. Its payload contains package-relative paths and file bytes encoded as hexadecimal records. Absolute paths and traversal are invalid.

The registry checksum is the 64-bit FNV-1a hash used by Raz over every package file in sorted relative-path order. For each file, the hash input is:

```text
relative/path + NUL + file-bytes + 0xff
```

The extracted archive must contain `raz.toml`, and its `[package]` name/version must match the registry path.

## Canonical archive path

```text
packages/<package-name>/<semantic-version>.dpk
```

A path that has appeared on `main` is immutable.


## Static GitHub API

The official registry publishes a generated JSON view under `api/v1/`. It is a projection of the immutable archive set, not a second source of truth.

- `api/v1/index.json` lists package names and versions.
- `api/v1/packages/<name>.json` lists all known versions and their archive metadata.
- `api/v1/packages/<name>/<version>.json` describes one immutable version, including checksum, repository-relative archive path, and raw GitHub download URL.

`packages/**/*.dpk` remains authoritative. `index.txt` and `api/v1/` must be reproducibly generated from that directory and are checked in CI.

## Mutable policy metadata

Immutable archives are intentionally separated from mutable package policy. `metadata/<name>.json` contains:

- `name`: package identity;
- `owners`: GitHub users/organizations permitted by project policy to maintain the package;
- `yanked`: published versions that must not participate in new resolution.

Yanked archives remain present and downloadable. `index.txt` contains only active releases; `api/v1` contains both active and yanked releases and explicitly marks yank state.


## Search projection

`search.txt` is a generated, tab-separated discovery projection. Each active package contributes one row:

```text
<name>\t<latest-active-version>\t<comma-separated-owners>\t<description>
```

It is derived from immutable package archives plus `metadata/<name>.json`. It is not authoritative storage and must be regenerated whenever archives, ownership, or yank state changes. Yanked releases are not selected as the latest active version.

## Mutable policy metadata

`metadata/<name>.json` stores owners and yanked versions. Package archives remain immutable. Generated `index.txt`, `search.txt`, and `api/v1/` are projections and must never become independent sources of truth.
