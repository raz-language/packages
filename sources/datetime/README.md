# datetime

High-performance civil date/time, UTC offset, duration, Unix timestamp, and RFC 3339 utilities for Raz.

## Features

- Proleptic Gregorian `Date` with leap-year and calendar validation.
- Constant-time civil date ↔ Unix-day conversion.
- Weekday and day-of-year calculations.
- `Time`, `DateTime`, `UtcOffset`, and `OffsetDateTime` value types.
- Normalized second/nanosecond `Duration` and `Timestamp` types.
- Current wall-clock timestamps through `std::time`.
- UTC-offset-aware timestamp conversion.
- Strict RFC 3339 parsing with 1–9 fractional-second digits.
- Allocation-free canonical RFC 3339 formatting into caller-owned buffers.

## Design

The package keeps calendar math and text conversion native to Raz. Parsing and formatting do not allocate, and timestamp conversion uses integer arithmetic rather than platform calendar APIs so behavior stays deterministic across supported hosts.
