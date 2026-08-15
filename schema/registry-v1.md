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
