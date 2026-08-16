# testing

Extended testing, fixtures, parameterization, and property testing for Raz.

> **Status:** initial package scaffold. The public API is not stable yet.

## Goals

- [ ] assertion helpers
- [ ] fixtures
- [ ] parameterized cases
- [ ] property generators
- [ ] shrinking
- [ ] benchmark-friendly test utilities

## Dependencies

None.

## Design rules

- Native Raz implementation wherever practical.
- Explicit errors through `Result` for recoverable failures.
- Avoid hidden allocations on hot paths.
- Keep the public surface small and composable.
- Add malformed/adversarial-input tests for parser, protocol, and security code.
