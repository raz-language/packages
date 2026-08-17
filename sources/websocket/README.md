# websocket

RFC 6455 WebSocket protocol primitives for Raz.

`websocket` is designed around caller-owned buffers and nonblocking transports. Frame parsing returns zero-copy payload views; frame headers can be emitted separately from payloads for vectored socket writes and reactor-driven state machines.

## Implemented

- RFC 6455 client key generation and `Sec-WebSocket-Accept`
- frame parsing/writing
- 7/16/64-bit payload lengths
- client masking and in-place unmasking
- continuation/text/binary/close/ping/pong opcodes
- fragmentation semantics
- control-frame validation
- configurable payload limits
- zero-copy frame payload views
- allocation-free hot path

The package intentionally provides protocol/state-machine primitives rather than owning a thread or blocking socket loop, which makes it suitable for Raz's readiness-driven reactor APIs.
