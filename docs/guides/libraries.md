# Remote Vocabulary Libraries

Sema's bundled vocabulary remains the default. The remote-library workflow
adds verified, named snapshots alongside it:

```bash
sema install https://github.com/acme/sema-defi/releases/latest/download/library.json
sema use defi
sema update defi

# Return to the bundled vocabulary
sema use --default
```

Only one vocabulary is active at a time. Installing `defi` does not merge it
with the bundled vocabulary or with another installed library. An installed
library is a read-only release snapshot; create a separate project database if
you need to modify or extend it.

## What `library.json` is

`library.json` is a small, strict release index. It does not contain the
patterns themselves. The MVP schema has these fields:

```json
{
  "manifest_schema": 1,
  "name": "defi",
  "version": "1.0.0",
  "update_url": "https://github.com/acme/sema-defi/releases/latest/download/library.json",
  "patterns": {
    "format": "sema-patterns-zip-v1",
    "url": "https://github.com/acme/sema-defi/releases/download/v1.0.0/defi-patterns-1.0.0.zip",
    "sha256": "<64 lowercase hexadecimal characters>",
    "size_bytes": 12345
  },
  "roots": {
    "semantic": {
      "scheme": "sema-semantic-set-v1",
      "sha256": "<64 lowercase hexadecimal characters>"
    },
    "catalog": {
      "scheme": "sema-catalog-v1",
      "sha256": "<64 lowercase hexadecimal characters>"
    }
  },
  "pattern_count": 3,
  "database": {
    "format": "sema-sqlite-v1",
    "schema_version": 1,
    "url": "https://github.com/acme/sema-defi/releases/download/v1.0.0/defi-1.0.0.db",
    "sha256": "<64 lowercase hexadecimal characters>",
    "size_bytes": 98765
  }
}
```

The `database` object is optional. All other fields shown above are required.
The library `name` is a lowercase slug, and `version` has exactly the numeric
`x.y.z` form. A manifest with a different schema version, missing or unknown
fields, invalid types, unsupported artifact formats, or malformed values is
rejected.

The two roots make different commitments: the semantic root identifies the set
of definitions, while the catalog root also commits to the exact handle-to-
definition bindings. Their scheme names travel with their hashes so a future
root algorithm cannot be mistaken for the current one.

## Pattern ZIP format

The patterns artifact uses `sema-patterns-zip-v1`. Its ZIP entries are exactly:

```text
patterns/<Handle>.json
```

There is one JSON file per pattern, no additional payload files, and the file's
`<Handle>` matches the handle in that Pattern Card. The number of files equals
`pattern_count`. Together they must form a complete dependency closure: every
referenced pattern is present with the declared full Sema ID.

The JSON files are the canonical portable release content. Sema validates their
schemas, identities, handle bindings, dependencies, and closure; builds a local
SQLite read model; then recomputes both roots and compares them with the
manifest. Installation fails closed on a mismatch and does not rewrite the
downloaded JSON.

Each card must pass the Sema version installed by the consumer, including its
current Pattern Card schema and canonical taxonomy paths. A library can contain
domain-specific patterns such as DeFi contracts under those paths, but custom
taxonomy roots or path profiles are not part of this MVP.

When the optional database is present and compatible, Sema may use it as a fast
path only after checking its size, SHA-256, schema version, pattern count, and
recomputed roots. A missing or incompatible database falls back to rebuilding
from the pattern ZIP. The ZIP remains authoritative.

## Publishing from GitHub

Use two different kinds of URL:

- GitHub's stable `releases/latest/download/library.json` URL as the update
  pointer that `sema update <name>` checks. It resolves to the manifest asset
  attached to the latest versioned release, rather than to a mutable branch.
- Versioned GitHub release URLs for the pattern ZIP and optional SQLite DB.
  Treat those assets as immutable: never replace the bytes at a published
  release URL. Their declared size and SHA-256 bind the manifest to the exact
  release bytes.

For example:

```text
https://github.com/acme/sema-defi/releases/latest/download/library.json
https://github.com/acme/sema-defi/releases/download/v1.0.0/defi-patterns-1.0.0.zip
https://github.com/acme/sema-defi/releases/download/v1.0.0/defi-1.0.0.db
```

Attach `library.json` itself to each GitHub release alongside the versioned ZIP
and optional database. To publish `1.1.0`, upload the new assets and verified
manifest; GitHub then moves the `releases/latest/download/library.json` pointer
to that release. Existing installations do not change until their users run:

```bash
sema update defi
```

An update is installed and verified as a complete replacement snapshot. It is
not merged with the installed release, another library, or the bundled
vocabulary. A failed verification leaves the installed and active snapshot
unchanged.

## Trust boundary

HTTPS protects the connection to the selected host, and the declared SHA-256
values detect changed artifact bytes. The Sema roots then verify the definitions
and handle bindings reconstructed from those bytes.

This MVP does **not** provide publisher signatures. A correct hash proves that
an artifact matches the selected manifest; it does not prove who authored that
manifest. Users must therefore trust the `library.json` URL and the account or
organization controlling it. Publisher-key signatures, rotation, and
revocation are future work.
