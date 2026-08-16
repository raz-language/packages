# postgres

Native PostgreSQL wire-protocol client for Raz.

> **Status:** initial package scaffold. The public API is not stable yet.

## Goals

- [ ] startup/authentication
- [ ] simple query protocol
- [ ] extended query protocol
- [ ] prepared statements
- [ ] typed values
- [ ] TLS integration
- [ ] connection pooling building blocks

## Dependencies

`crypto`

## Design rules

- Native Raz implementation wherever practical.
- Explicit errors through `Result` for recoverable failures.
- Avoid hidden allocations on hot paths.
- Keep the public surface small and composable.
- Add malformed/adversarial-input tests for parser, protocol, and security code.
