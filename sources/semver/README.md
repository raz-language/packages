# semver

Strict Semantic Versioning 2.0.0 parsing, precedence, and package-manager version requirements for Raz.

## Features

- zero-allocation borrowed version parsing
- strict `major.minor.patch` validation
- prerelease and build metadata validation
- SemVer precedence including numeric/alphanumeric prerelease identifiers
- build metadata ignored for precedence as required by SemVer 2.0.0
- exact requirements
- partial and wildcard requirements (`1`, `1.2`, `1.2.x`, `*`)
- caret requirements (`^1.2.3`)
- tilde requirements (`~1.2.3`)
- `<`, `<=`, `>`, `>=`, and `=` comparators
- whitespace or comma AND groups
- `||` alternatives
- hyphen ranges (`1.2.0 - 1.9.0`)

The parser stores prerelease/build metadata as borrowed byte spans into the original input. Keep the source bytes alive for as long as the `Version` is used.

## Package

```toml
[dependencies]
semver = "^0.2.0"
```

## Example

```raz
import semver;

u8 text[5] = [49, 46, 53, 46, 50];
u8 requirement[6] = [94, 49, 46, 50, 46, 51];
Version version = semver::version::empty();

if (semver::version::parse(&text[0]as usize, 5, &mut version)) {
    bool accepted = semver::requirement::satisfies(
        &version,
        &requirement[0]as usize,
        6,
    );
}
```
