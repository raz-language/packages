# Security policy

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Report it privately to
the maintainer with the affected package and version, reproduction steps, and
the observed impact.

Report package content separately from registry infrastructure: a malicious or
compromised published package is handled by yanking the version, while a flaw in
the registry's own validation or metadata handling is a defect here.

## Security boundaries

This repository is a package registry, so the assets it protects are the
integrity of published metadata and the resolution decisions clients make from
it.

- **Immutability.** A published version is immutable. Corrections are made by
  publishing a new version and yanking the old one, never by rewriting an
  existing entry.
- **Checksums.** Registry entries carry checksums, and clients verify them
  before extraction. `scripts/validate_registry.py` checks the tree's internal
  consistency; run it before any registry change lands.
- **Generated artifacts.** `index.txt`, `search.txt`, and the `api/` documents
  are generated. Regenerating them must be idempotent — a diff after a
  regeneration run means either a generator bug or a hand edit that will be
  silently reverted.
- **Ownership.** Owner changes, yanks, and unyanks are queued through the
  registry admin workflow rather than applied by direct edits, so the change has
  a reviewable trail.

Report anything that would let a client resolve a package version to content
whose checksum was never published, or that lets an entry mutate in place.
