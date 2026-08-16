# toml

Native TOML parsing for Raz, designed around source-backed documents and low allocation overhead.

## Status

`0.2.0` provides the first functional parser and document index. The public API is still pre-1.0 and may evolve as typed `serde` integration and canonical serialization are added.

## Current capabilities

- borrowed parsing with no source copy
- owned parsing using Raz `String`
- compact node index rather than per-value heap objects
- key/value assignments
- dotted and quoted keys
- standard tables (`[server]`)
- arrays of tables (`[[servers]]`)
- basic and literal strings, including multiline delimiters
- arrays and inline-table spans
- boolean, integer, float, and date/time token classification
- comments and whitespace
- one-based line/column parse diagnostics
- configurable composite nesting limit

Values and keys are exposed as borrowed byte views into the original document. This keeps parsing cheap and lets callers decide which values actually need decoding or ownership.

## Example

```raz
import alloc::string;
import toml;

fn parse_config(String source) -> i64 {
    TomlDocument document = toml::document::empty();
    TomlError error = toml::parser::parse_owned(move source, 64, &mut document);

    if (!toml::error::success(&error)) {
        toml::document::destroy(&mut document);
        return -1;
    }

    i64 count = toml::document::node_count(&document);
    toml::document::destroy(&mut document);
    return count;
}
```

## Design

The parser retains exact source slices for keys and values. A document therefore performs one source allocation for owned input plus geometric growth of a compact `TomlNode` vector. Borrowed parsing avoids even the source allocation.

Typed conversion, full TOML semantic validation, `serde` adapters, canonical formatting, and mutation APIs will build on this representation in later releases.

## Dependency

- `serde` — format-neutral serialization contracts used by the typed adapter layer
