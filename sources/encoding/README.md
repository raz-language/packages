# encoding

Allocation-free binary-to-text codecs and checksums for Raz.

Version 0.1.0 provides strict hexadecimal, canonical unpadded base64url, RFC 4648 base32, and incremental IEEE CRC-32 APIs. Every codec writes into caller-owned storage, reports the exact produced length, rejects non-canonical trailing bits, and never performs a hidden allocation.

## Modules

- `encoding::hex` — lower/uppercase encoding and case-insensitive decoding.
- `encoding::base64url` — unpadded URL-safe Base64 used by JOSE/JWT.
- `encoding::base32` — padded-free RFC 4648 encoding with strict decoding.
- `encoding::checksum` — one-shot and incremental IEEE CRC-32.

All decoders treat malformed input as an explicit error and leave the reported output length at zero.
