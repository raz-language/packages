# Changelog

All notable changes to the Raz package registry are documented here.

## Unreleased

### Packages

- Completed the official 22-package source matrix, including explicit curated
  support dependencies, removal of unused `std` edges, source-order fixes, and
  package-level corrections for ownership, pointer, trait-object, parser, and
  protocol code.
- Added `scripts/compile-all.sh`; a clean production compiler run now checks all
  22 current packages successfully.
- Published initial `archive`, `jwt`, `multipart`, and `testing` releases from
  their completed source trees.
- Added and published the foundational `encoding`, `json`, and `csv` packages.
- Added and published allocation-conscious `yaml`, `cbor`, `msgpack`, and
  `protobuf` serialization packages with bounded readers and writers.
- Added a deterministic official-source release helper that resolves local
  workspace dependencies to immutable registry checksums.

### Documentation

- Added `SECURITY.md` covering published-version immutability, checksum
  verification, generated-artifact idempotency, and the queued ownership/yank
  workflow.

### Housekeeping

- Registry validation and the index/search/API generators are confirmed
  idempotent: regenerating produces no diff against the committed tree.
