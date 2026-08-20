# cbor

An allocation-free CBOR codec for Raz.

Version 0.1.0 supports definite-length RFC 8949 integers, byte and text strings, arrays, maps, tags, simple values, boolean/null values, floating-point bit payloads, bounded recursive skipping, and caller-owned output. Indefinite-length items are rejected explicitly so callers never inherit an unbounded buffering requirement.
