# regex

`regex` is the official allocation-conscious regular-expression package for Raz.

Version 0.2 introduces a compact Thompson/Pike-style NFA engine. Patterns compile into caller-owned storage and matching uses bounded active-state arrays, avoiding exponential recursive backtracking.

## Supported syntax

- literals and escapes
- `.` (any byte except newline)
- `^` and `$`
- character classes and ranges: `[abc]`, `[a-z]`, `[^0-9]`
- grouping: `(expr)`
- alternation: `a|b`
- quantifiers: `*`, `+`, `?`
- escaped `\n`, `\r`, and `\t`

The v0.2 engine is byte-oriented. UTF-8 input is safe to search, but `.` and character classes operate on encoded bytes; Unicode scalar/property semantics are planned separately rather than hidden behind locale-dependent behavior.

## Performance model

The engine does not use recursive input backtracking. At most `MAX_INSTRUCTIONS` NFA states are active for each input byte, providing predictable matching behavior for adversarial repetition and alternation patterns.

Compiled regex programs live in storage supplied by the caller, so hot-path matching does not require heap allocation.
