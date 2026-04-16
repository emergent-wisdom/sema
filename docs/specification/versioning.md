# Versioning, Refinement, and Supersession

Sema's content-addressed identity model and the practical need to refine
patterns over time look, at first glance, like they're at war: how do you
"improve" a pattern whose hash is supposed to be a permanent commitment?
The short answer is that you don't improve a pattern — you mint a new one
that the handle now points to. This document spells out the policy that
falls out of that answer.

## 1. Hashes are immutable, handles are mutable

A pattern's `sema_id` is a cryptographic commitment to a specific
definition. The bytes that produced it are still the bytes; the hash
will resolve to that exact pattern forever.

A pattern's `handle` is a human-readable name. Over time, a handle may
point to different definitions. That's the whole point of having a name
separate from a hash.

- Agents that care about **stability** reference `sema_id` (or the
  `Handle#stub` short form, which is hash-identifying).
- Agents that care about **freshness** reference the bare `handle` and
  let the registry hand them whichever definition is current.

## 2. Refinement produces a new hash, not an edit

When a pattern's mechanism is tightened or its dependencies change, you
re-run `sema apply` and the pipeline computes a new hash. The old hash
remains valid and resolvable forever — content-addressed storage cannot
"forget" something you can still produce the bytes for. The new hash
becomes the current canonical stub for that handle.

Both definitions are legitimate. They are simply different definitions
that happen to share a name.

## 3. Supersession is a metadata claim, not enforcement

When a new version of a handle is meant to replace an older one, list
the older `sema_id` in the new pattern's `_meta.supersedes`:

```json
{
  "handle": "PropheticQuorum",
  "_meta": {
    "layer": "Society",
    "category": "Coordination",
    "ring": 1,
    "tier": 1,
    "supersedes": [
      "sema:PropheticQuorum#mh:SHA-256:21f7..."
    ]
  }
}
```

Two things are true at once:

- This is a **claim**, not an enforcement. Old hashes still resolve, old
  documents still work, and `sema_handshake` still HALTs on stub
  mismatch — that *is* the drift-detection primitive and it shouldn't
  silently swallow disagreements.
- Tooling that wants to walk successor chains can do so. A future
  `sema latest <handle>` could follow `supersedes` pointers from the
  current head back to a known older hash, or vice versa, without
  needing a schema migration.

## 4. `sema_handshake` semantics across versions

`sema_handshake` is strict by design: it verifies byte-level agreement
on a specific definition. Agents that pin to `PropheticQuorum#192e`
continue to resolve that exact definition forever, even if a newer
`PropheticQuorum#192e` exists.

Agents that want "the latest PropheticQuorum" query the bare handle,
get back whichever hash is current, and *then* handshake against that
hash. The same model works for both pinned and floating callers.

The tension that "tightening a pattern breaks downstream handshake" is
real but **asymmetric**: downstream code that referenced the old hash
keeps working unchanged, because the old hash still resolves. Only code
that chose to upgrade to the new version has to update its reference.
This is the same model Git uses for commits, and the same model Docker
uses for image digests.

## 5. Deprecation and removal

Patterns are never removed from the hash space — that would break old
references. To signal that a pattern is obsolete without deleting it,
mark it with both fields:

```json
"_meta": {
  "deprecated": true,
  "supersedes": ["sema:OldThing#mh:SHA-256:..."]
}
```

Again, a claim, not enforcement. Tooling like `sema search` can
optionally filter deprecated patterns from default results without
breaking lookups by hash.

## 6. Short stubs identify versions, not handles

A 4-hex stub like `PropheticQuorum#192e` identifies one specific
version of a handle. When the handle is refined, the new version gets
a different stub: `PropheticQuorum#192e`. Stubs are therefore
**version-identifying**, not handle-identifying.

This is a feature, not a quirk. It lets prose distinguish
"PropheticQuorum as of March 2026" from "PropheticQuorum as of June
2026" with no extra ceremony — the stub already encodes which one you
mean. When stubs disagree in a handshake, that disagreement is
load-bearing information: the two parties are referring to different
artefacts, and pretending otherwise would silently corrupt
coordination.

## What v0.1.3 ships and what it defers

This release ships:

- The policy in this document.
- A schema hook accepting `_meta.supersedes` as a valid optional list
  of `sema_id` strings, so future patterns can record successor
  intent without further schema work.

This release does **not** yet ship:

- Walking supersession chains in `sema_handshake`.
- A `sema latest <handle>` command.
- A `sema deprecated` filter on `sema search`.

Those are deferred to v0.2.0 so that the policy gets some user testing
before it grows tooling around it.
