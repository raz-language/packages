# sqlite

Native SQLite integration for Raz with an allocation-conscious Raz API over SQLite's stable C ABI.

## Features

- connection open/close and busy timeout
- prepared statements
- typed bind parameters (`NULL`, `i64`, `f64`, UTF-8 text, blobs)
- typed column access
- zero-copy borrowed text/blob column views
- statement reset/clear/finalize
- affected-row and last-insert-rowid access
- transaction helpers (`DEFERRED`, `IMMEDIATE`, `EXCLUSIVE`, commit, rollback)
- primary/extended SQLite error codes

## Native dependency

`sqlite` calls the upstream SQLite C ABI directly. The package declares `sqlite3` through Raz's generic `[native]` manifest section, so normal `raz build` links the native library automatically, including when `sqlite` is only a transitive dependency. The package intentionally does not copy SQLite into Raz's runtime.

The SQLite 3 development/runtime library must still be installed on the target system or available through a declared native `library-paths` directory.

## Lifetime rules

`column_text` and `column_blob` return borrowed views owned by SQLite. They remain valid only until the next `step`, `reset`, or `finalize` for that statement. Bind text/blob helpers use SQLite's transient-copy policy, so caller buffers need only survive the bind call.
