# Raz Package Registry

`raz-language/packages` is the canonical package registry for the [Raz programming language](https://github.com/raz-language/raz), and the home of the official package implementations.

The registry is intentionally GitHub-backed. There is no registry server and no database: immutable, deterministic Raz package archives live under `packages/`, and `index.txt` is generated from those archives. Cloning this repository gives you the entire registry.

## Using packages

The Raz toolchain resolves from this repository by default, so a normal project needs no configuration:

```text
raz search crypto
raz info crypto
raz add crypto
raz add serde@^0.2.0
raz update
```

Dependencies are recorded in `raz.toml` as version constraints and pinned exactly in `raz.lock`. Archives are integrity-checked against the index checksum and stored in a shared content-addressed cache, so `build`, `check`, `run`, and `test` hydrate missing locked packages automatically — a clean checkout needs no separate install step.

`RAZ_REGISTRY_URL` overrides the official registry for private registries, mirrors, and tests. See [Package management](https://github.com/raz-language/raz/blob/main/docs/PACKAGE-MANAGEMENT.md).

## Available packages

| Package | Latest | Description |
|---|---|---|
| [`crypto`](sources/crypto) | 0.4.0 | SHA-2/SHA-3/BLAKE3, HMAC, Poly1305, ChaCha20-Poly1305, X25519, Ed25519, HKDF, secure random |
| [`serde`](sources/serde) | 0.2.0 | Serialization and deserialization contracts |
| [`toml`](sources/toml) | 0.2.0 | TOML parser and document model |
| [`regex`](sources/regex) | 0.2.0 | Thompson/Pike NFA regular-expression engine |
| [`uuid`](sources/uuid) | 0.2.0 | RFC 9562 UUID v4 and v7 |
| [`semver`](sources/semver) | 0.2.0 | Semantic-version parser and requirement engine |
| [`datetime`](sources/datetime) | 0.2.0 | Civil time, timestamps, durations, UTC offsets, RFC 3339 |
| [`websocket`](sources/websocket) | 0.2.0 | RFC 6455 protocol core |
| [`http-router`](sources/http-router) | 0.2.0 | Compiled, allocation-conscious HTTP router |
| [`sqlite`](sources/sqlite) | 0.3.0 | Connections, statements, and transactions over the `sqlite3` ABI |
| [`postgres`](sources/postgres) | 0.3.0 | PostgreSQL wire-protocol client with auth, TLS, and connection pooling |

Packages under active development that have not been published yet: `jwt`, `multipart`, `archive`, and `testing`. Every published version, including superseded ones, remains available and is listed in [`index.txt`](index.txt); [`sources/PACKAGES.md`](sources/PACKAGES.md) tracks status and future candidates.

## Repository layout

```text
index.txt              generated registry index — one line per published version
packages/              published archives: packages/<name>/<version>.dpk
sources/               editable source workspace for the official packages
schema/registry-v1.md  the index and archive contract
scripts/               index generation and registry validation
```

Two directories look similar and are not interchangeable:

- **`packages/`** is the registry. Only `packages/<name>/<version>.dpk` archives are installable, and once a path has appeared on `main` it is immutable.
- **`sources/`** is where those packages are developed. It is a single Raz workspace (`sources/raz.toml`) covering every official package, so workspace-aware commands operate across all of them.

```text
cd sources
raz check --workspace
raz test --workspace
```

Source changes are developed and tested in `sources/`, assigned a new semantic version, and then published as a new deterministic archive under `packages/`.

## The index

`index.txt` is UTF-8 text with one whitespace-separated record per published version:

```text
<name> <version> <archive-path> <tree-checksum> [key-id signature]
```

```text
crypto 0.4.0 packages/crypto/0.4.0.dpk 29c5d0340794fcfe
```

The checksum is the 64-bit FNV-1a hash Raz computes over every package file in sorted relative-path order, which is what makes installs verifiable and builds reproducible. The index is **generated** — never hand-edit it. Regenerate with:

```bash
python scripts/generate_index.py
```

The full contract, including the `RAZPKG1` archive format, is specified in [schema/registry-v1.md](schema/registry-v1.md).

## Publishing

From a Raz package directory:

```text
raz publish
```

Without an explicit private registry URL, this creates a repository-shaped submission under `.raz-publish/` containing `packages/<name>/<version>.dpk`. Copy that archive to the same path in this repository, regenerate the index, validate, and open a pull request:

```bash
python scripts/generate_index.py && python scripts/validate_registry.py
```

Published versions are immutable. Once `packages/foo/1.2.0.dpk` exists on `main`, a correction must ship as a new version such as `1.2.1`.

CI on every pull request verifies that no existing `.dpk` path was modified or deleted, that `index.txt` exactly matches the archives in `packages/`, and that archive syntax, manifest identity, and deterministic tree checksums all agree.

Full rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The official packages are licensed under the [Apache License 2.0](LICENSE).
