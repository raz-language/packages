# protobuf

An allocation-free Protocol Buffers wire codec for Raz.

Version 0.1.0 implements strict varint decoding, zigzag signed integers, fixed-width values, length-delimited strings and bytes, field-number validation, unknown-field iteration, transactional bounded writes, and explicit rejection of deprecated groups. Schema generation is intentionally separate from this wire-level package.
