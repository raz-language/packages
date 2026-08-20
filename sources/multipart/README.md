# multipart

Streaming MIME multipart/form-data support for Raz.

Version 0.1.0 implements strict boundary validation, zero-copy part iteration, bounded header scanning, form field and file metadata extraction, configurable part/header limits, and a transactional caller-buffer writer.

The reader recognizes quoted `name` and `filename` parameters, exposes the complete borrowed header block, and returns file content type when present. The writer rejects CR/LF and quote injection in disposition parameters and rolls its logical length back if a part cannot fit.

## Dependencies

None.

## Design rules

- No hidden allocation or input copies.
- CRLF framing and final-boundary handling are validated explicitly.
- Resource limits are part of the reader state rather than global policy.
