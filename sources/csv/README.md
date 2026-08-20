# csv

A streaming, zero-copy CSV reader and allocation-free writer for Raz.

Version 0.1.0 supports RFC 4180 quoting, doubled-quote escapes, CRLF and LF input, configurable single-byte delimiters, optional UTF-8 BOM input, exact row/column tracking, empty fields, and caller-owned decode/output buffers.

The reader returns borrowed raw fields and only copies when a quoted field must be unescaped. The writer preflights each field so `OutputFull` never leaves a partially written field in the destination buffer.
