# testing

Reusable assertions, deterministic property generators, shrinking, and benchmark statistics for Raz.

Version 0.1.0 provides caller-buffered structured failures, case-index tracking for parameterized tests, scalar/byte assertions, unbiased deterministic ranges, byte generation and in-place shuffling, reproducible property-runner state, scalar shrinking, and Welford benchmark statistics.

The package deliberately does not own output or process termination. Test executables decide how to render recorded failures and which exit code to return.

## Dependencies

None.

## Design rules

- Seeds and failing case indices are always available for reproduction.
- Assertion failure storage is caller-owned and bounded.
- Random generation is deterministic and is not presented as cryptographic randomness.
