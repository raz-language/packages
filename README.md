# Raz Package Registry

`raz-language/packages` is the canonical package registry for the [Raz programming language](https://github.com/raz-language/raz).

The registry is intentionally GitHub-backed. There is no Raz registry server or database: immutable deterministic Raz package archives live under `packages/`, `index.txt` is the generated resolver projection, `search.txt` is the generated discovery projection, and `api/v1/` is a generated static registry API served directly by GitHub.

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

## Source code

The editable source for the official packages is kept in [`sources/`](sources/). The registry contract remains unchanged: only deterministic, immutable releases under `packages/<name>/<version>.dpk` are installable registry artifacts.

This keeps the repository useful both as the canonical GitHub-backed registry and as the home of the official package implementations.

## Source verification

Run the production compiler across every current official package with:

```text
RAZ_COMPILER=/path/to/raz ./scripts/compile-all.sh --clean
```

The command performs a clean parse, type, ownership, and MIR validation pass for
each package and exits nonzero if any package fails.

## Static registry API

GitHub itself serves the official registry API. The generated endpoints are normal versioned repository files:

```text
search.txt
api/v1/index.json
api/v1/packages/<name>.json
api/v1/packages/<name>/<version>.json
```

`index.txt` remains the dependency-resolution hot path, while `search.txt` provides package name/latest version/owners/description for rich CLI search. Tooling, websites, IDEs, and future clients can consume the JSON API without a dedicated service. Both representations are generated from the same immutable `.dpk` archives.

## Publishing

From a Raz package directory:

```text
raz publish
```

For maintainers or automation, set `GITHUB_TOKEN` (or `RAZ_REGISTRY_TOKEN`) to a token with contents write access to `raz-language/packages`. Raz uploads the immutable `packages/<name>/<version>.dpk` directly through GitHub; the registry workflow regenerates `index.txt` and `api/v1/`.

Without GitHub write credentials, the exact same command creates a repository-shaped submission under `.raz-publish/`. That directory can be copied into a fork/checkout and submitted as a pull request, so ordinary package authors do not need registry-server credentials.

Published versions are immutable. Once `packages/foo/1.2.0.dpk` exists on `main`, changes must be released as a new version such as `1.2.1`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for publication rules and [schema/registry-v1.md](schema/registry-v1.md) for the index/archive contract.

## Registry policy metadata

Package ownership and yank state live separately from immutable archives:

```text
metadata/<name>.json
```

Example:

```json
{
  "name": "crypto",
  "owners": ["raz-language"],
  "yanked": []
}
```

Yanking never deletes or modifies a `.dpk`. The version is removed from the generated resolver `index.txt` while remaining visible in `api/v1/` with `"yanked": true`, so existing lockfiles stay reproducible.

Maintainers can update this state with `scripts/registry_admin.py`; all changes still flow through ordinary GitHub commits/pull requests.


## Registry administration

The Raz CLI can inspect and queue registry policy changes directly through GitHub:

```text
raz registry status
raz registry owner-add <package> <github-user>
raz registry owner-remove <package> <github-user>
raz registry yank <package> <version>
raz registry unyank <package> <version>
```

The authenticated mutation commands dispatch `.github/workflows/registry-admin.yml`. That workflow applies the metadata change, regenerates `index.txt`, `search.txt`, and `api/v1/`, validates the registry, and commits the generated metadata. This keeps registry administration in GitHub's auditable repository/workflow model with no Raz-operated server.
