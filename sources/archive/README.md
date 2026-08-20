# archive

Safe, allocation-free archive format primitives for Raz.

Version 0.1.0 provides zero-copy USTAR and stored-ZIP readers, caller-owned TAR/ZIP writers, IEEE CRC-32 verification, explicit truncation/feature errors, and extraction-path validation.

## Modules

- `archive::path` rejects absolute paths, backslashes, drive/ADS colons, NUL/control bytes, empty components, and `.`/`..` traversal.
- `archive::tar` validates header checksums and octal fields, bounds every padded record, reads files/directories/links, and writes USTAR records.
- `archive::zip` reads and writes unencrypted stored entries plus central-directory records. Unsupported compression and data descriptors fail explicitly.

## Dependencies

None beyond the Raz standard library.

## Design rules

- Entry views borrow archive memory; callers control copying and extraction.
- Writers preflight capacity and use caller-owned output buffers.
- ZIP compression is deliberately outside this format layer; method 0 is fully supported and other methods return `UnsupportedFeature`.
