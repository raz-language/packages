# jwt

JWT, JWS, registered-claim, and JWK support for Raz.

Version 0.1.0 implements compact HS256 signing and constant-work verification, strict unpadded base64url, JSON validation, symmetric JWK decoding, registered claim parsing, time validation with explicit leeway, and caller-configured algorithm/key/token-size policy.

## Security defaults

- `strict_policy()` permits only HS256, requires a 32-byte key, caps tokens at 1 MiB, and applies no implicit clock leeway.
- The protected header must explicitly select HS256; unrecognized `crit` headers are rejected.
- The algorithm is chosen by caller policy, never by dynamically dispatching on untrusted token text.
- Signatures are compared in constant work and temporary MAC buffers are zeroized.

## Dependencies

`crypto`, `encoding`, `json`

## Design rules

- Token and payload output storage is caller-owned.
- Registered string claim views borrow the decoded payload.
- Unsupported JOSE algorithms fail closed and can be added as separate policy-gated implementations.
