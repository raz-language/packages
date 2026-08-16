# multipart

MIME multipart and form-data support for Raz.

> **Status:** initial package scaffold. The public API is not stable yet.

## Goals

- [ ] boundary parser
- [ ] streaming multipart reader
- [ ] form-data fields
- [ ] file parts
- [ ] multipart writer

## Dependencies

None.

## Design rules

- Native Raz implementation wherever practical.
- Explicit errors through `Result` for recoverable failures.
- Avoid hidden allocations on hot paths.
- Keep the public surface small and composable.
- Add malformed/adversarial-input tests for parser, protocol, and security code.
