# Delta reconstruction: Sema v0.3.0 to v0.4.0

This experiment asks whether the current Sema graph and hash-cascade code can
reconstruct the public `v0.4.0` vocabulary from the public `v0.3.0`
vocabulary. The data inputs come only from those two public git tags. The
implementation under test comes from the current checkout, not from the tags.
No external proof-of-concept attachment or private test data is used.

## Run it

The two tags must exist in the local clone. From the repository root, with the
project dependencies installed, run:

```bash
.venv/bin/python experiments/delta_reconstruction/reproduce.py
```

The script extracts both tags into a temporary directory, performs every
mutation on temporary databases, and removes them when it exits. It checks the
computed report against [`expected-results.json`](expected-results.json). Use
`--print-only` to inspect new output without the final regression check.
The same regression runs in CI on Python 3.12.

## Two separate target checks

The experiment keeps the published target commitments and the current runtime
materialization separate:

1. The tagged v0.4.0 database supplies the published semantic and catalog roots.
2. The v0.4.0 tagged cards are also compiled into a new empty database with the
   current code. That fresh database is the reference for the current logical
   read model.

The normalized read model includes every logical node type and every edge, with
metadata and multiplicity. It ignores UUIDs, embeddings, edge keys, row order,
indexes, and SQLite page layout. The fresh target contains 2,061 logical nodes
and 3,803 edges, including 457 pattern nodes and 1,745 pattern-to-pattern edges.

The historical tagged database has the same published roots, exact card payload,
and pattern-to-pattern edges as the fresh build. Its older derived materialization
does not match the current one: it is missing 41 current derived nodes, and its
derived edge multiset has 33 extra and 41 missing entries. That is why the tagged
SQLite file is not used as the oracle for current derived nodes.

## Public historical result

The source release has 452 patterns and the target has 457. Five patterns were
added and none were removed. Among the 452 shared handles:

- 426 identities changed.
- 275 cards had direct semantic edits.
- 151 identities changed only through the Merkle dependency cascade.
- `Axiom` changed taxonomy metadata without changing its Sema identity.

| Reconstruction | Delta input | Both tagged roots | Pattern-to-pattern edges | Complete card payload | Complete current read model |
|---|---:|:---:|:---:|:---:|:---:|
| In-place full overlay | All 457 target cards | Yes | Yes | Yes | Yes |
| In-place hash-changed subset | 426 changed IDs + 5 additions | Yes | Yes | No, `Axiom` metadata is missed | No |
| In-place direct semantic subset | 275 direct edits + 5 additions | Yes | Yes | No, 152 metadata payloads differ | No |
| Staged snapshot and fresh build | 275 direct cards + 5 additions + 152 metadata patches + explicit removals | Yes | Yes | Yes | Yes |

The direct in-place reconstruction demonstrates the useful cascade property.
Sema recomputed all 151 omitted cascade-only identities and reached both target
roots without receiving those cards as semantic edits. It did not reconstruct a
complete release. The 152 payload mismatches are the 151 omitted cascade-only
cards, whose target `_meta.supersedes` history was not transmitted, plus the
metadata-only `Axiom` reclassification.

The complete read-model comparison catches what the narrower root and
pattern-edge checks cannot:

- The hash-changed subset retains the old `Axiom` taxonomy edge and misses the
  new one, despite matching both roots.
- The direct subset has 1 extra and 15 missing derived nodes, plus 13 extra and
  16 missing derived edges, under the current materialization.
- The full overlay happens to cleanly reconstruct the complete current read
  model for this release pair. That is an observed result, not a general
  guarantee for arbitrary historical databases.

## Safer reconstruction before activation

The strongest variant does not mutate the source database in place. It:

1. Starts from the complete v0.3.0 card snapshot.
2. Replaces the 275 directly edited cards with their complete v0.4.0 cards.
3. Adds the five new cards and applies an explicit removal set, empty for this
   particular release pair.
4. Applies 152 remaining nonsemantic metadata patches.
5. Compiles a new database with the current code.
6. Compares both roots, every card payload, and the complete normalized read
   model with a separately compiled v0.4.0 target before activation.

That staged fresh build matches the target exactly. It is the appropriate
baseline for a future delta transport because it does not require an active
database to survive a partially applied update and it does not trust root
equality as proof of complete release equivalence.

## Removals and other boundaries

There were no removals from v0.3.0 to v0.4.0, so this historical pair cannot
validate deletion handling. A general delta must carry an explicit removal set;
otherwise stale source patterns remain and the target roots do not match. The
synthetic CI contract covers this in
[`test_target_overlay_without_explicit_removals_keeps_stale_patterns`](../../src/sema/cli/tests/test_delta_reconstruction.py),
and separately covers metadata-only changes in
[`test_metadata_only_change_requires_payload_comparison`](../../src/sema/cli/tests/test_delta_reconstruction.py).
That module also exercises additions, renames, dependency cascades, complete
payload equivalence, and an incorrect delta.

A complete transport delta therefore needs, at minimum:

- added cards;
- direct semantic edits;
- explicit removals;
- nonsemantic metadata patches when complete release equivalence is required;
- the expected semantic and catalog roots; and
- a fresh-build read-model comparison before activation.

This is a local reconstruction baseline, not a transport validation or a
bandwidth benchmark. It does not fetch changed blocks over a network. The
current `sema update` path still downloads the target release's full pattern
ZIP, verifies it, compiles a fresh database, and then activates the new snapshot
atomically. The result validates this historical transition and the
accompanying synthetic cases; it is not a proof that every possible delta
algorithm is correct.
