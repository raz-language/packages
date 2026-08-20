# msgpack

An allocation-free MessagePack codec for Raz.

Version 0.1.0 implements compact signed and unsigned integers, nil and boolean values, binary and UTF-8 string payloads, arrays, maps, floating-point bit payloads, bounded recursive skipping, strict truncation handling, and caller-owned output. Extension values are rejected explicitly until a typed extension API is introduced.
