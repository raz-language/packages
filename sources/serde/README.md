# serde

`serde` defines Raz's format-neutral serialization contracts.

The package is intentionally split between a format-facing event API and type-facing `Serialize` / `Deserialize` traits. Formats can stream directly to buffers, files, sockets, or other sinks without constructing a mandatory intermediate value tree.

## Design

- allocation-neutral serializer/deserializer contracts
- borrowed byte and UTF-8 views during decoding
- static generic dispatch for normal application code
- explicit dynamic serializer/deserializer boundary for format implementations
- structured sequence and map events
- primitive implementations for the core scalar types

`toml`, `cbor`, `msgpack`, configuration libraries, protocol codecs, and application packages can implement these contracts without coupling Raz data types to one wire format.

## Status

Version 0.2 establishes the core contracts. Derive/code-generation support and richer collection implementations will follow as the ecosystem packages begin consuming the API.
