# Official package sources

This directory contains the editable source trees for the official Raz packages maintained alongside the registry.

The public registry remains canonical under `../packages/<name>/<version>.dpk`. Published `.dpk` versions are immutable. Source changes are developed here, tested with the Raz toolchain, assigned a new semantic version, and then published as a new deterministic archive.

## Workspace

`raz.toml` defines all package source directories as one Raz workspace.

```text
sources/
  raz.toml
  crypto/
  serde/
  toml/
  regex/
  uuid/
  semver/
  datetime/
  websocket/
  http-router/
  sqlite/
  postgres/
  jwt/
  multipart/
  archive/
  testing/
```

From this directory, workspace-aware Raz commands can operate across the package sources.
