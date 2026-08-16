# jwt

JWT, JWS, and JWK support for Raz.

> **Status:** initial package scaffold. The public API is not stable yet.

## Goals

- [ ] compact serialization
- [ ] JWS signing and verification
- [ ] registered claims
- [ ] JWK model
- [ ] algorithm policy

## Dependencies

`crypto`, `serde`

## Design rules

- Native Raz implementation wherever practical.
- Explicit errors through `Result` for recoverable failures.
- Avoid hidden allocations on hot paths.
- Keep the public surface small and composable.
- Add malformed/adversarial-input tests for parser, protocol, and security code.
