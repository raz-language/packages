# http-router

High-performance, allocation-conscious HTTP routing for Raz.

`http-router` compiles route patterns once into caller-owned route/segment storage and matches directly against borrowed `std::net::http::HttpRequestView` data. The hot path does not allocate or copy path/parameter strings.

## Features

- method-aware dispatch (`GET`, `HEAD`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`, `CONNECT`, `TRACE`, or `Any`)
- static routes such as `/health`
- named path parameters such as `/users/:id`
- final wildcard tails such as `/assets/*path`
- query-string exclusion during path matching
- duplicate-route and malformed-pattern rejection
- allowed-method masks for 405/`Allow` handling
- indexed and named borrowed parameter lookup
- static-first specificity ranking independent of registration order
- first-static-segment hash prefilter
- borrowed parameter spans into the original request target
- caller-owned route, segment, and parameter storage
- middleware-chain and handler IDs with typed dispatcher hooks
- direct adapter for Raz stdlib `HttpRequestView`
- no hidden allocation in route compilation or matching

## Pattern rules

Patterns must begin with `/`. Parameter names begin with `:` and wildcard names begin with `*`. A wildcard must be the final segment. Duplicate parameter names inside one route are rejected.

```text
/
/health
/users/:id
/teams/:team/members/:member
/assets/*path
```

## Integration

The router deliberately does not own sockets, a blocking server loop, response buffers, or application closures. Use it with `std::net::http`, `std::net::http::server`, and `std::net::reactor`. A match returns stable application handler/middleware IDs; the application can dispatch those IDs to normal Raz functions or closures.

## Performance model

Compiled route metadata and request parameters live in caller-provided storage. Static first segments are hash-prefiltered, and matching returns borrowed `BytesView` values instead of constructing strings. This keeps routing suitable for retained-buffer/reactor servers.
