# Versioning, Refinement, and Supersession

Sema's content-addressed identity model and the practical need to refine
patterns over time look, at first glance, like they're at war: how do you
"improve" a pattern whose hash is supposed to be a permanent commitment?
The short answer is that you don't improve a pattern — you mint a new one
that the handle now points to. This document spells out the policy that
falls out of that answer.

## 1. Hashes are immutable, handles are mutable

A pattern's `sema_id` is a cryptographic commitment to a specific
definition. The identifier remains valid for those bytes forever, but
resolution is a storage property: a registry must retain the definition if it
promises to serve that identifier later.

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
remains a valid identifier for the old bytes, but it is resolvable only where
those bytes were retained. The current GraphStore keeps one active definition
per handle and does not archive the replaced record. The new hash becomes the
current canonical stub for that handle.

Both definitions can be legitimate. They are different definitions that share
a name, provided a version-aware registry retains both.

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

- This is a **claim**, not an archive. `sema_handshake` still HALTs on stub
  mismatch — that *is* the drift-detection primitive and it should not
  silently swallow disagreements — but old documents resolve only when their
  exact definitions remain available in a historical content store.
- Tooling that wants to walk successor chains can do so. A future
  `sema latest <handle>` could follow `supersedes` pointers from the
  current head back to a known older hash, or vice versa, without
  needing a schema migration.

## 4. `sema_handshake` semantics across versions

<!-- doc-refs: pinned -->
`sema_handshake` is strict by design: it verifies byte-level agreement
on a specific definition. An agent pinned to `PropheticQuorum#912b` can
continue to verify that exact definition if its registry retained the bytes,
even though `PropheticQuorum#91f6` has since superseded it.
<!-- doc-refs: end -->

Agents that want "the latest PropheticQuorum" query the bare handle,
get back whichever hash is current, and *then* handshake against that
hash. The same model works for both pinned and floating callers.

The tension that "tightening a pattern breaks downstream handshake" is
real but **asymmetric**: downstream code that referenced the old hash
keeps its meaning unchanged, but it keeps working only if the old definition is
retained. Code that chooses to upgrade must update its reference. Git and
digest-addressed image registries provide this model because they retain
immutable objects; Sema's current single-version GraphStore does not yet make
the same retention guarantee.

## 5. Deprecation and removal

A durable registry should not remove a definition that published references
still use. To signal that a pattern is obsolete without deleting it, a
version-aware registry can mark it with both fields:

```json
"_meta": {
  "deprecated": true,
  "supersedes": ["sema:OldThing#mh:SHA-256:..."]
}
```

Again, this is policy rather than enforcement. Tooling like `sema search` can
optionally filter deprecated patterns from default results while exact lookup
continues through a historical store. The current GraphStore cannot retain two
versions of the same handle, so this archival behavior is not shipped.

## 6. Short stubs identify versions, not handles

<!-- doc-refs: pinned -->
A 4-hex stub like `PropheticQuorum#912b` identifies one specific
version of a handle. When the handle is refined, the new version gets
a different stub: `PropheticQuorum#91f6`. Stubs are therefore
**version-identifying**, not handle-identifying.
<!-- doc-refs: end -->

This is a feature, not a quirk. It lets prose distinguish
"PropheticQuorum as of March 2026" from "PropheticQuorum as of June
2026" with no extra ceremony — the stub already encodes which one you
mean. When stubs disagree in a handshake, that disagreement is
load-bearing information: the two parties are referring to different
artefacts, and pretending otherwise would silently corrupt
coordination.

## What ships and what is still deferred

Shipped:

- The policy in this document.
- A schema hook accepting `_meta.supersedes` as a valid optional list
  of `sema_id` strings, so patterns can record successor intent without
  further schema work. Patterns use it: `PropheticQuorum` carries three
  superseded versions.
- Exact, hashed specialization claims through `extends`. Apply never silently
  retargets them; in the current single-version workspace it fails before a
  parent change could strand a child, unless reviewed child cards are staged
  and explicitly retargeted.

Still not shipped in 0.4.0:

- Historical content storage and exact lookup across multiple versions of one
  handle.
- Walking supersession chains in `sema_handshake`.
- A `sema latest <handle>` command.
- A `sema deprecated` filter on `sema search`.

These were originally deferred to v0.2.0 so the policy could get some
user testing first. Two releases later the policy has had that testing
and the tooling has not arrived, which is worth stating plainly rather
than leaving a deferral note that reads as a plan. Nothing depends on
them: supersession is a metadata claim by design (Section 3), so a
consumer that wants to walk a chain can read `_meta.supersedes`
directly, and hash lookups never needed the tooling.
