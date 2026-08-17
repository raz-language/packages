# postgres

Native PostgreSQL wire-protocol client for Raz.

`postgres` keeps protocol state, framing, authentication, row views, pooling, and transport orchestration in Raz. Native code is not used for the PostgreSQL protocol. The package can be driven by blocking TCP today and by reactor/TLS engines without changing its wire representation.

## Implemented

- PostgreSQL v3 startup packets and SSLRequest negotiation packet
- bounded incremental backend-message receive framing
- simple Query messages
- extended protocol: Parse, Bind, Describe, Execute, Sync, and Close
- text parameters including SQL NULL
- prepared-statement orchestration
- Authentication request classification
- complete SCRAM-SHA-256 client proof generation and server-signature verification
- OS-CSPRNG client nonces
- PBKDF2-HMAC-SHA-256 (`Hi`), client/server keys, and stored keys
- zero-copy `DataRow` field views
- `RowDescription` column metadata
- text boolean/integer decoding
- ErrorResponse/NoticeResponse field lookup
- backend key and `ReadyForQuery` state tracking
- BEGIN / COMMIT / ROLLBACK helpers
- caller-owned fixed-capacity connection pooling with generation-safe leases
- caller-owned buffers throughout hot protocol paths

## TLS

PostgreSQL requires an eight-byte SSLRequest before its normal StartupMessage. `postgres::tls::upgrade` sends the request, verifies the server's `S` response, and completes a blocking client TLS handshake on the existing socket using Raz's `std::net::tls::TlsEngine`. The resulting `PgTls` exposes encrypted `write_all`/`read` operations while the wire protocol remains transport-independent.

## Pooling

`postgres::pool` intentionally manages already-connected `Client` values rather than creating connections behind the caller's back. This keeps credentials, TLS policy, timeouts, reactor assignment, and retry policy explicit while still providing bounded round-robin leasing and stale-lease protection.
