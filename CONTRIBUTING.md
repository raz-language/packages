# Contributing Packages

## Publish a new version

1. Set the package `name` and semantic `version` in `raz.toml`.
2. Run the package tests.
3. Run `raz publish` from the package root.
4. Copy `.raz-publish/packages/<name>/<version>.dpk` to the same path in this repository.
5. Run `python scripts/generate_index.py`.
6. Run `python scripts/validate_registry.py`.
7. Commit the archive and regenerated `index.txt`, then open a pull request.

## Immutability

Existing package archives on `main` are immutable. Pull requests may add new `.dpk` versions but may not modify, rename, or delete a published archive. If a release is wrong, publish a new semantic version.

## Package names

Names must be lowercase ASCII and may contain lowercase letters, digits, `-`, and `_`. A name must start with a lowercase letter or digit. Version filenames must be semantic versions of the form `MAJOR.MINOR.PATCH`, optionally followed by a prerelease/build suffix accepted by Raz.

## Review and CI

CI verifies archive syntax, package path/manifest identity, deterministic package-tree checksums, index generation, duplicate identities, and published-version immutability.
