# Changelog

All notable changes to the Raz package registry are documented here.

## Unreleased

### Documentation

- Added `SECURITY.md` covering published-version immutability, checksum
  verification, generated-artifact idempotency, and the queued ownership/yank
  workflow.

### Housekeeping

- Registry validation and the index/search/API generators are confirmed
  idempotent: regenerating produces no diff against the committed tree.
