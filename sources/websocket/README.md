# websocket

WebSocket client and server protocol support for Raz.

> **Status:** initial package scaffold. The public API is not stable yet.

## Goals

- [ ] HTTP upgrade handshake
- [ ] frame parser/writer
- [ ] masking
- [ ] fragmentation
- [ ] ping/pong/close control frames
- [ ] client and server helpers

## Dependencies

None.

## Design rules

- Native Raz implementation wherever practical.
- Explicit errors through `Result` for recoverable failures.
- Avoid hidden allocations on hot paths.
- Keep the public surface small and composable.
- Add malformed/adversarial-input tests for parser, protocol, and security code.
