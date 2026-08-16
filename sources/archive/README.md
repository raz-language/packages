# archive

Archive readers and writers for Raz.

> **Status:** initial package scaffold. The public API is not stable yet.

## Goals

- [ ] stream abstraction
- [ ] TAR reader/writer
- [ ] ZIP format layer
- [ ] CRC integration
- [ ] safe path extraction

## Dependencies

None.

## Design rules

- Native Raz implementation wherever practical.
- Explicit errors through `Result` for recoverable failures.
- Avoid hidden allocations on hot paths.
- Keep the public surface small and composable.
- Add malformed/adversarial-input tests for parser, protocol, and security code.
