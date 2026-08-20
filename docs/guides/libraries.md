# Publishing and Installing Vocabulary Libraries

Sema can package any project database as a verified, read-only vocabulary
release. The bundled vocabulary remains the offline default; independently
published libraries are installed alongside it and selected by name.

This guide follows one DeFi library from authoring through publication and
installation.

The official `bootstrap` release uses the same contract. Its `library.json` and
pattern ZIP are generated from the bundled database during each Sema release
and verified to reproduce the bundled semantic and catalog roots. Those files
are distribution artifacts, not a second maintained copy of the patterns, and
installing them leaves the bundled offline fallback intact.

## The complete DeFi workflow

### 1. Create a writable project database

Install Sema, then choose what the DeFi library should contain:

```bash
pip install semahash

# Start with the complete bundled vocabulary when the DeFi patterns extend it.
sema build defi.db --preset full

# Or start with no patterns for an entirely independent vocabulary.
# sema build defi.db --preset empty

sema use ./defi.db
```

Only one vocabulary is active at a time. A published DeFi library does **not**
overlay or merge with the bundled vocabulary. If a DeFi card depends on a
bundled card, the DeFi release must include that card and its complete
transitive dependency closure.

Starting from `--preset full` is the simplest way to guarantee this. To publish
a smaller release later, build a dependency-closed database from selected
top-level handles as shown in step 3.

`SEMA_DB_PATH`, when set, overrides `sema use`. Unset it or point it at
`defi.db` before authoring if you have used that variable previously.

### 2. Author and validate the DeFi cards

Write one Pattern Card per JSON file. Follow the [Pattern Authoring
Guide](authoring.md), [Pattern Card schema](../specification/schema.md), and
[Validation Rules](../specification/validation.md). For example:

```text
patterns/
  AssetPrice.json
  LiquidationGuard.json
```

Check the proposed handles and definitions against the active vocabulary, then
validate and apply the cards as one batch:

```bash
sema search "asset price"
sema search "liquidation guard"
sema apply --check --add patterns/
sema apply --add patterns/
sema resolve LiquidationGuard
sema root
```

`sema apply` calculates the content identities and writes the resolved hashes
back to the input JSON. Keep those authored files in the DeFi repository; the
database is the authoritative working registry, while the files remain the
reviewable source material for the project.

### 3. Choose the release closure

`sema package` packages every pattern in its source database. If `defi.db`
contains exactly what should ship, package it directly in step 4.

To make a smaller library, list the public entry-point handles, one per line:

```text
# release-patterns.txt
LiquidationGuard
```

Then build a new database from the DeFi project database:

```bash
sema build defi-release.db --from release-patterns.txt --source ./defi.db
```

`sema build --from` includes every transitive dependency automatically, so
`defi-release.db` is a complete standalone snapshot rather than an overlay.

### 4. Package and verify the release locally

For a GitHub repository at `acme/sema-defi`, package version `1.0.0` with:

```bash
sema package ./defi-release.db \
  --name defi \
  --version 1.0.0 \
  --output-dir dist/defi-1.0.0 \
  --github-repo acme/sema-defi
```

If you are publishing the complete project database, replace
`./defi-release.db` with `./defi.db`.

The command writes:

```text
dist/defi-1.0.0/
  library.json
  defi-patterns-1.0.0.zip
```

It does more than create a ZIP. Before either final file is exposed, Sema:

1. exports every card from the selected database;
2. creates a deterministic `patterns/<Handle>.json` archive;
3. calculates the artifact SHA-256, byte size, pattern count, semantic root,
   and catalog root;
4. re-reads the archive, validates every card and exact dependency pin, and
   verifies the complete closure;
5. compiles a fresh SQLite read model and verifies it through the same path
   used during installation.

A successful `sema package` is therefore the local pre-publication verification
step. It refuses to package an empty database or overwrite an existing output
directory. The verified manifest and ZIP become visible together through one
atomic directory rename.

`--github-repo` derives both publication URLs:

```text
https://github.com/acme/sema-defi/releases/latest/download/library.json
https://github.com/acme/sema-defi/releases/download/v1.0.0/defi-patterns-1.0.0.zip
```

For a non-GitHub host, supply both URLs explicitly instead:

```bash
sema package ./defi-release.db \
  --name defi \
  --version 1.0.0 \
  --output-dir dist/defi-1.0.0 \
  --update-url https://vocab.example/releases/latest/library.json \
  --artifact-url https://vocab.example/releases/1.0.0/defi-patterns-1.0.0.zip
```

Use HTTPS publication URLs. The artifact URL must end in a path-safe `.zip`
filename.

### 5. Publish both files as GitHub Release assets

Create the version tag expected by the generated artifact URL and attach both
files to the same GitHub Release:

```bash
gh release create v1.0.0 \
  dist/defi-1.0.0/library.json \
  dist/defi-1.0.0/defi-patterns-1.0.0.zip \
  --repo acme/sema-defi \
  --title "DeFi vocabulary 1.0.0" \
  --generate-notes \
  --latest
```

The release must be **published**, not left as a draft, and it must become the
repository's latest ordinary release. Drafts and prereleases do not satisfy the
generated `releases/latest/download/library.json` update URL. If the repository
also publishes unrelated releases, attach a valid `library.json` and matching
ZIP to every release that can become `latest`, or use a dedicated vocabulary
repository.

Do not replace either asset after publication. To change the snapshot or ZIP
content, increment the version and create a new release; Sema rejects changed
release content republished under an already installed version.

The install target is the **GitHub Release asset URL for `library.json`**. It is
not the GitHub repository URL, a branch, a source ZIP, or a `blob/...` page.

### 6. Install and inspect the published library

Another user installs the release index, activates the registered name, and
checks the resulting snapshot:

```bash
sema install https://github.com/acme/sema-defi/releases/latest/download/library.json
sema use defi
sema list
sema root
sema show LiquidationGuard
```

`sema install` registers the verified library but does not activate it; that is
why `sema use defi` is a separate step. In `sema list`, `defi` should be marked
active and read-only. The semantic root, catalog root, and pattern count printed
by `sema root` should match the values printed by `sema package` and stored in
`library.json`.

Return to the bundled vocabulary at any time with:

```bash
sema use --default
```

### 7. Publish and consume an update

For `1.1.0`, update the project database, build the desired release closure
again, and package into a new output directory:

```bash
sema package ./defi-release-1.1.db \
  --name defi \
  --version 1.1.0 \
  --output-dir dist/defi-1.1.0 \
  --github-repo acme/sema-defi
```

Publish `library.json` and `defi-patterns-1.1.0.zip` on a published `v1.1.0`
GitHub Release. Existing installations remain unchanged until their users run:

```bash
sema update defi
sema list
sema root
```

`sema update` follows the stable `update_url`, verifies the complete replacement
snapshot, and atomically repoints an active installation. It never merges the
new release with the old one, another library, or the bundled vocabulary. A
failed update leaves the installed and active snapshot unchanged.

`sema pull` is a different operation: it reconciles one writable local database
with another database. Use `sema update <name>` for a published remote library.

## The release contract

### What `library.json` contains

`library.json` is a small, strict release index. It does not contain the
patterns. `sema package` generates this file; its schema is shown here for
inspection:

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
  "pattern_count": 3
}
```

All fields shown are required. The library `name` is a lowercase slug, and
`version` has exactly the numeric `x.y.z` form. Missing or unknown fields,
invalid types, unsupported artifact formats, unsupported root schemes, and
malformed values are rejected.

The semantic root commits to the set of definitions. The catalog root also
commits to the exact handle-to-definition bindings. Their scheme names travel
with their hashes so a future root algorithm cannot be confused with the
current one.

### Pattern ZIP format

The `sema-patterns-zip-v1` archive contains one file per pattern:

```text
patterns/<Handle>.json
```

The filename must match the card's handle. The number of files must equal
`pattern_count`, and together they must form a complete dependency closure:
every referenced card is present with the exact full Sema ID declared by its
consumer.

Sema validates the card schemas, identities, handle bindings, dependencies,
closure, and roots before compiling its own local SQLite read model.
Publisher-supplied executable or precompiled database state is not accepted;
the portable JSON is the trust and interchange surface.

Each card must pass the Sema version installed by the consumer, including the
current Pattern Card schema and canonical taxonomy paths. Domain-specific cards
can use those paths, but custom taxonomy roots or path profiles are not part of
this release format.

The installer also bounds the interchange surface: the manifest is at most
256 KiB; the archive at most 256 MiB; each card at most 2 MiB; the expanded
archive at most 512 MiB; and a release at most 100,000 cards. ZIP members may
use stored or deflated compression. Unsafe paths, encryption, non-regular
members, additional payload files, case-colliding handles, and suspicious
compression ratios are rejected. Install sources use local files or HTTPS;
credentials embedded in URLs and HTTPS-to-file downgrades are rejected.

## Trust boundary

HTTPS protects the connection to the selected host, and the declared SHA-256
detects changed artifact bytes. The two Sema roots then verify the definitions
and handle bindings reconstructed from those bytes.

This release format does **not** provide publisher signatures. A correct hash
proves that an artifact matches the selected manifest; it does not prove who
authored that manifest. Users must trust the `library.json` Release asset URL
and the account or organization controlling it. Publisher-key signatures,
rotation, and revocation remain future work.
