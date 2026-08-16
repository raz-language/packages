# uuid

Fast UUID primitives for Raz.

`uuid` uses a compact 128-bit value representation and caller-owned buffers for parsing and formatting. Generation is allocation-free and uses Raz's operating-system CSPRNG through the official `crypto` package.

## Features

- RFC 9562 UUIDv4 generation
- RFC 9562 UUIDv7 generation
- Unix-millisecond extraction from UUIDv7
- strict canonical parser
- lowercase canonical formatter
- 16-byte binary import/export
- nil/equality/lexicographic ordering helpers
- version and RFC-variant inspection
- no mandatory heap allocation

## Example

```raz
import uuid;

fn main() -> i64 {
    Uuid id = uuid::nil();
    if (!uuid::v7(&mut id)) {
        return 1;
    }

    u8 text[36];
    if (!uuid::format(&id, &mut text[0]as usize, 36)) {
        return 2;
    }
    return 0;
}
```

## Representation

`Uuid` stores two `u64` words in canonical/network byte order. Comparing `high` and then `low` therefore produces the same ordering as comparing the canonical 16 UUID bytes. UUIDv7 values naturally sort by their 48-bit Unix-millisecond prefix.
