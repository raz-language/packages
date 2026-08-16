# crypto

Cryptographic primitives and secure utilities for Raz.

> **Status:** pre-1.0 API (`0.4.0`). Hashing, authentication, key derivation, symmetric authenticated encryption, X25519 key agreement, Ed25519 signatures, secure comparison, zeroization, and OS entropy are available.

## Implemented

### Hashes

- SHA-256 and SHA-512, one-shot and streaming
- SHA3-256 and SHA3-512, one-shot and streaming
- BLAKE3-256 portable allocation-free tree hashing

### Authentication and key derivation

- HMAC-SHA-256, one-shot and streaming
- HKDF-SHA-256 extract, expand, and derive
- Poly1305, one-shot and streaming

### Symmetric cryptography

- IETF ChaCha20 with 256-bit keys and 96-bit nonces
- ChaCha20-Poly1305 AEAD with detached tags and AAD
- authentication before plaintext release
- in-place encryption and decryption

### Public-key cryptography

- X25519 scalar multiplication, public-key derivation, and shared-secret derivation in Raz
- Ed25519 key generation, public-key derivation, signing, and verification through Raz's permanent platform-cryptography ABI

### Secure utilities

- constant-work equal-length byte comparison
- secure zeroization through the Raz runtime ABI
- OS CSPRNG integration through `std::random`

## Design

Performance-sensitive APIs use caller-owned storage and raw byte spans. Streaming primitives retain state in caller-owned structs and the portable hashing, MAC, KDF, symmetric-crypto, and X25519 paths do not require heap allocation.

Native code is restricted to permanent platform boundaries. Ed25519 intentionally reuses the same provider-backed ABI used by Raz's own package-signing implementation rather than maintaining a second native signature stack.

## Validation

Known-answer coverage includes SHA-2, SHA-3, BLAKE3, HMAC-SHA-256, HKDF-SHA-256, ChaCha20, Poly1305, ChaCha20-Poly1305, RFC 7748 X25519, and RFC 8032 Ed25519 vectors. Authentication tests include modified-tag/signature rejection.

## Next

- SHAKE128 / SHAKE256
- BLAKE3 keyed and derive-key modes
- architecture-specific SIMD acceleration behind the same APIs
- higher-level key containers and encoding helpers where they add value without hiding ownership
