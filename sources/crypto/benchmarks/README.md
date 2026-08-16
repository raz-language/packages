# crypto benchmarks

Performance qualification for `crypto` belongs here.

Benchmark groups should include:

- SHA-256, SHA-512, SHA3-256, SHA3-512, and BLAKE3 throughput over small, 1 KiB, 64 KiB, and multi-megabyte buffers
- streaming versus one-shot hashing
- HMAC-SHA-256 and HKDF-SHA-256
- ChaCha20 throughput
- Poly1305 throughput
- ChaCha20-Poly1305 encrypt/decrypt throughput

Results should report bytes per second and cycles per byte where the platform exposes a stable cycle counter. Benchmarks must not change algorithm behavior or introduce benchmark-specific implementation paths.
