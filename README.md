# Raz Package Registry

`raz-language/packages` is the canonical package registry for the [Raz programming language](https://github.com/raz-language/raz).

The registry is intentionally GitHub-backed. There is no mandatory registry server or database: immutable deterministic Raz package archives live under `packages/`, and `index.txt` is generated from those archives.

## Layout

```text
index.txt
packages/
  <name>/
    <version>.dpk
```

The Raz toolchain uses this repository by default. A normal project can install packages with:

```text
raz add json
raz add json@^1.2.0
raz update
```

`RAZ_REGISTRY_URL` can still override the official registry for private registries, mirrors, and tests.

## Publishing

From a Raz package directory:

```text
raz publish
```

Without an explicit private registry URL, this creates a repository-shaped submission under `.raz-publish/` containing `packages/<name>/<version>.dpk` plus a generated index entry. Copy the new package archive into [`raz-language/packages`](https://github.com/raz-language/packages) and open a pull request.

Published versions are immutable. Once `packages/foo/1.2.0.dpk` exists on `main`, changes must be released as a new version such as `1.2.1`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for publication rules and [schema/registry-v1.md](schema/registry-v1.md) for the index/archive contract.
