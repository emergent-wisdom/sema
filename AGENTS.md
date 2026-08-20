# Repository Agent Guide

This file is the repository-level operating context for coding agents. Detailed
domain rules remain in the linked specifications; do not duplicate or invent
them from prompt context.

## Development Workflow

- Work on a focused feature branch and use a pull request. Do not merge until
  required CI is green.
- Keep unrelated user changes intact and surface unrelated defects separately.
- Use `Henrik Westerberg <henrik.westerberg@emergentwisdom.org>` for locally
  authored commits. GitHub-created merge commits may use the account's noreply
  address; merge locally when every commit must use the organization address.
- Website and frontend experiments must remain on an isolated branch and
  staging service until Henrik explicitly approves production deployment.
- Paper typography or stylesheet work must remain separate from semantic paper
  updates unless visual redesign is the stated scope.
- Any change that touches `paper/` must be built with `scripts/compile_paper.sh`,
  never bare `pdflatex`. The script regenerates the tables, the pattern-card
  appendix, the prose hash references and the stats macros, then runs bibtex and
  three pdflatex passes. Bare pdflatex leaves those stale: it once shipped 49
  outdated hash stubs in the prose and a wrong pattern count, and a stale
  generated `docs/information/audit.md` from the same class of mistake failed CI
  on the 3.12 job, which is the only job that runs the vocabulary-workflow check.

## Vocabulary Changes

Read these before editing patterns:

- `docs/guides/authoring.md`
- `docs/guides/lifecycle.md`
- `docs/specification/schema.md`
- `docs/specification/validation.md`

The database is authoritative. Copy exported JSON from `data/vocabulary/` into
`data/staging/`, edit staging, update `data/design_critique.json`, preview the
manual, then apply. Never edit canonical vocabulary exports directly.

To apply, prefer:

```bash
python scripts/apply_vocabulary_change.py
```

It runs the four steps in the only order that works and stops at the first
failure. It ignores any database selected by `sema use` and pins every
subprocess to this checkout's authoritative `data/taxonomy.db`.

**Run it as its own command, after the sidecar edit has landed.** Chaining a
`design_critique.json` edit and the apply in one shell invocation lets the
reversible step fail while the irreversible one proceeds: a script that died
part-way through writing the sidecar still allowed the apply to change four cards
and clear staging, leaving the corpus edited with the argument for it unwritten.
Note also that `design.critique` is a list on some patterns and a string on others,
which is what killed that script — handle both, or read the type first. The order is load-bearing: `sema apply` writes the database,
`export_sema.py` writes `data/vocabulary/` from the database, and
`rebuild_vocabulary.py` reads `data/vocabulary/` to recompute hashes so that
dependents of an edited pattern pick up its new hash. Rebuilding before
exporting rehashes the previous state instead, which once let a dependency cycle
survive a fix that had already been applied.

Validation refuses a cycle before anything is written, including a cycle between
a staged pattern and an already-committed one, and including one formed by a
`references` edge in each direction. Where the reverse edge already exists the
relationship is in the graph from the side that does not cycle, so name the other
pattern in prose rather than adding the edge. `rebuild_vocabulary.py --replace`
keeps the rebuilt database only when the rebuild succeeded; a failed rebuild
restores the backup, and backups are timestamped so a later run cannot destroy an
earlier one.

`scripts/audit/dangling_handles.py` reports CapitalisedNames in pattern text that
resolve to no pattern. It covers backticked names and multi-part CamelCase; single
bare capitalised words are not detectable, for reasons measured in its docstring.
Resolving a name is mechanical, but deciding whether to mint, redirect or
lowercase is not — that is Henrik's call.

General handles contain only the broad-use intersection. Put qualitatively
different strategies in descendants, quantitative identity axes in parameters,
deployment policy in callers, and contextual risks in the design sidecar.
Missing invariants or failure modes are not automatically defects. Sidecar
critique is diagnostic evidence, not a backlog of contracts to add.

## Vocabulary Review

Before proposing any pattern change, read the "Governing principles" section of
`docs/manuals/vocabulary-design.md`. It states the library's purpose before its
rules: the library is a seed, and a good seed is usable first, extensible second,
absorbable third, forkable fourth. Do not work from a summary of those rules,
including a summary written by another agent earlier in the same session.

The manual is a deliberation instrument, not a lookup table. Its per-pattern
commentary exists so a reviewer reads one pattern, thinks about it, and forms a
judgment before moving on. Bulk ranking of the corpus by a metric is the wrong
mode and will produce confident findings that fail the placement test.

The obligation on a pattern scales with fan-in, the number of patterns that
transitively depend on it, not with layer and not with derivation depth. Use
`scripts/audit/fan_in.py` rather than ad-hoc extraction; note that dependencies
are nested as `{"references": {placeholder: ref}}` and a traversal that does not
descend one level will silently report zero. Measure the cascade before
proposing any edit to a hashed field.

Fan-in remains the right measure of obligation and has stopped being a useful
*prioritiser*. Above roughly 45 transitive dependents the corpus holds only a
handful of patterns; below that the distribution collapses, with about half the
remainder at 1–5 dependents and half at zero. Once the high-fan-in patterns are
read, order by fan-in-above-zero first and alphabetically within the tier, and say
that is what you are doing — an order that no longer encodes obligation should not
be presented as though it does.

Some review questions are decidable and some are not. A contradiction between a
`data_schema` requirement and the pattern's own `varies` line is mechanical, so
report it as measured. Whether a pattern is useful is not mechanical, so state
the framing your judgment depends on, give the competing reading, and say what
would change your mind. Do not present a judgment as a determination.

Three biases have produced bad reviews of this library before, all observed:
completing empty fields because they are empty; framing a test so that it yields
a conclusion already reached; and swinging from ignoring the governing policy to
treating it as beyond question. Anything consequential should be checked by an
independent reviewer that measured for itself, because none of the three is
self-detectable.

### The improvement loop, per pattern

Asked to improve the vocabulary, work one pattern at a time through this loop.
There is no batch shortcut: a detector that nominates patterns for attention
lets you skip the ones it does not nominate, and a pattern that turns out sound
is a result worth recording, not a wasted read.

1. **Ask what a consuming agent does with this card, and where that goes wrong**,
   before asking which rule it violates. The verifier of a Sema contract is a
   reasoner, not a compiler, so the defects that matter are found by following a
   consequence and missed by matching a shape. `CiteBack` required every assertion
   to cite a source and required the source to exist — both satisfied by attaching
   a real source ID to an unrelated claim, so a pattern built to prevent
   hallucination permitted a hallucination with a footnote. No rule was violated.

   `docs/guides/review-method.md` catalogues the classes that recur, and it is a
   cross-check to run *after* this question, never instead of it. A checklist read
   as a lens will crowd out the reasoning that produced it.

2. **Read the pattern's section in `docs/manuals/vocabulary-design.md`**, not its
   JSON. The card alone gives you the mechanism and contracts; the manual section
   adds why it exists, the enumerated broad-use contexts, the declared
   intersection, what varies, the design tensions, the critique, and the family
   discussion. Reviewing from the JSON misses most of what decides a judgment.
3. **Reason the card against its own commentary**, in both directions. The card
   can be wrong about itself, and the commentary can be wrong about the card.
   Both happen, and the second is invisible from the JSON. Two of the sidecar's
   fields carry most of the weight: `usage.every_context_needs` is what a
   contract proposal has to survive, and `usage.varies` is what disqualifies one.
   **33 of 455 patterns have an empty `usage` block**, so for those neither test
   is available — reason from the tensions, tradeoffs and critique instead, and
   say in the sidecar that you did. Do not fill the block to give yourself
   something to test against; that manufactures the evidence.
4. **Let the commentary supply the fix where it can.** It frequently already
   contains the answer. `Decompose` asserted "Subproblems must be independent"
   while its own critique conceded that "the independence invariant is almost
   always violated in practice" — and its intersection said independence
   *criterion*. A criterion is a declared test and is decidable; absolute
   independence is not. That reframing came from the manual, not from judgment.
5. **Write the claim on the card and the reason in the sidecar. Never both.**
   The card is not documentation — it is *payload*. Every hashed field is loaded
   into the context of every agent that resolves the pattern, and an agent
   hydrating a twenty-pattern subgraph pays for all of it. The sidecar costs a
   consumer nothing, because nothing resolves it at runtime; it is the review
   surface. So an invariant states what must hold, and the argument for why that
   is the right constraint goes in `data/design_critique.json`.

   The test is one word: if a sentence contains *because*, *which is why*, *this
   is what makes X detectable*, or names the defect it repairs, it is addressed
   to a reviewer and belongs in the sidecar. Compare:

   - Payload — "Baseline recomputation interval and source window are declared."
   - Review surface — "…because a baseline that follows recent behaviour cannot
     detect behaviour that changes more slowly than it rebuilds, which is the
     attack this pattern exists to catch."

   Both sentences are true and only the first belongs on the card.

   **This rule is about card versus sidecar. It does not license moving a guarantee
   from `invariants` into `mechanism`.** Those are both payload and they differ in
   *force*: the mechanism describes, the invariants bind. A compliant implementation
   can satisfy every invariant and do nothing that appears only in mechanism prose.

   So before shortening an invariant by relocating a clause into the mechanism, ask
   whether the clause is a property a caller relies on. `Rollout`'s cleanup path —
   invoke `break`, then `compensate` every effectful-or-`unknown` armed entry, then
   freeze the manifest — reads like a procedure and *is* the safety guarantee of a
   deployment pattern. Moved to prose it stopped being enforceable, and the check
   "is the text still present in the mechanism?" passed for all seven clauses while
   proving nothing. Where a procedure is repeated across several invariants, the fix
   is to name it once and reference it, not to delete it.

   This was measured, and it is easy to do without noticing. One reviewer's
   rewrites inflated 78 patterns from 55,586 to 94,790 bytes of hashed text —
   **1.71×, +39,204 bytes** — with worst cases at 9.8× (`Parallel`, 87 → 852)
   and 8.2× (`Variable`, 127 → 1041), and exactly one pattern made shorter. The
   cause was writing to justify each change to a human reader, and the prose was
   *duplicated*, because the same reasoning had already been written into the
   sidecar in the same pass. Deleting it from the cards lost nothing.

   Growth is not automatically bloat: a card that had no invariants at all will
   get bigger when it gains two, and `Dampen` going 227 → 651 for four new
   contract statements is correct. Judge the ratio against what was added, not
   against zero.
6. **Stage, then diff.** Copy to `data/staging/`, edit, and diff the staged card
   against the export before applying. The diff is what tells you whether you
   changed what you intended. **Replacing any hashed text field wholesale drops
   whatever placeholders it held**, and the dependency stays declared. Five
   occurrences in one pass: twice in an invariant's *label* (`Entropy
   {{constraint}}:`, `{{synthesis}} Quality:`), once in a sentence removed with a
   failure mode, and twice in a mechanism rewritten from scratch — where the lost
   sentence was load-bearing, since `MonotonicCounter`'s said the guarantee
   "relies on a `{{state_lock}}` (or CRDT logic)", which is *how* the counter is
   enforced. The Inverse rule catches it every time, and the fix is a Deep Fix
   Protocol question rather than a deletion: read the original, decide whether the
   relationship is real, and if it is, put the reference where it now belongs.
   Diff the placeholder set before and after, not just the prose.
7. **Before wiring any dependency, look for the reverse edge.** Validation now
   refuses a cycle, including one formed by a `references` edge in each direction
   and one between a staged pattern and an already-committed one, so this no
   longer costs you work — but it still costs you a rewrite, and the validator
   cannot tell you what the fix is. Reading the target card takes one call and
   has changed the verdict repeatedly: wiring `Card` → `Greet` was correct
   because Greet does not reference Card, while the identical-looking `Interpret`
   → `Translate` would have cycled, since Translate already references Interpret.
   Where the reverse edge exists, the relationship is already in the graph from
   the side that does not cycle, and the right move is prose or a lowercase
   concept per Rule H — not deleting the sentence that needed the reference.
8. **Update `data/design_critique.json` in the same pass — every field that
   referred to what you changed, not only `critique`.** Writing the commentary is
   where the thinking happens; a card edited without it leaves the review surface
   asserting something false. The fields are
   `motivation.{why_this_layer, why_it_exists, removability}`,
   `design.{tensions, tradeoffs, critique}`, `usage.{intended,
   every_context_needs, varies, notes}` and `family_discussion`.

   Doing half of this is the easy failure and it has happened at scale. A 2026-07
   pass wrote `critique` on 224 patterns and left the siblings alone; 62 of those
   cards ended up with commentary naming an invariant that no longer existed, and
   that count is a floor, because it matched deleted invariant *labels* and not
   paraphrases. The worst subset was `motivation.removability` at 28 cards — that
   field answers "should this pattern exist at all" and usually answers by citing
   an invariant, so a card whose cited invariant was deleted now argues for its own
   existence from a contract that is gone. `design.tensions` at 61 has a second
   failure mode: a tension the pass *resolved* still reads as live. Move a resolved
   tension into `critique`, described as resolved.

   Two checks after a batch: does any sidecar field still name a contract you
   removed, and does any tension pose as open a question you closed?
9. **Measure the cascade, then apply.** Reason read-only across many patterns and
   apply once, in one ordered tranche. Applying per batch rehashes the trunk
   repeatedly. Treat any deliberate `extends` retargeting as its own reviewed
   semantic edit. The protocol permits an older pin when its exact parent remains
   resolvable, but the current single-version workspace rejects such a parent
   update; stage reviewed children and retarget them explicitly.

### Resuming a review someone else started

A review pass is long enough that it will outlive a session. Four places hold the
state, and only the first three travel with a clone:

| Where | What it holds |
|---|---|
| `docs/guides/review-method.md` | The judgment layer: scenario-first framing, the ordered checks with their counter-examples, the recurring defect classes, and the negative results — tools and theories already tried and abandoned. **Read this before building any tooling.** |
| `docs/manuals/vocabulary-design.md` | Per-pattern worked examples. Each `critique` entry records not just what changed but what was considered and rejected. This is what teaches the judgment, which does not otherwise transfer. |
| `git log --oneline -- data/vocabulary` | Batch-level reasoning. Commit bodies carry the argument for each change; the last vocabulary commit names where the pass stopped. |
| `../sema-seed-review/LEDGER.py` | Every verdict including `SOUND`, keyed by handle, with the reasoning. **Outside the repo by design** — voluminous, mid-flight, no value to a consumer. If it is absent, reconstruct position from the git log and treat unread patterns as unread; do not assume a pattern is sound because no record exists. |

The loop instruction itself should be a pointer, not a payload. A wake-up prompt
that carries the method inline dies with the session and has to be reconstructed
from memory; one that says *read the method file, do a batch, update the method
file* survives. Anything learned about how to review belongs in
`review-method.md`, where it can be edited and reviewed like any other artifact —
and that document states the discipline for adding to it, including the
repository-local rule that a defect class earns a place only on its third
instance. That threshold is policy for this review method, not a universal
`MintWhenFriction` contract.

### Why this cannot be scripted

The reading is the method, not a slow path to it. This is not a preference about
craft; it is what the work has repeatedly turned out to require, and the attempts
to automate it were measured.

**Detectors written for the classes below performed like this.** A check
comparing `data_schema.required` against the card's own `varies` line flagged 18
patterns of which 10 were genuine — 56%. A check for preconditions assuming what
the mechanism determines flagged 20, of which 3 were genuine — 15%. A check for a
`data_schema` defining no properties flagged 1, which was a false positive
(`Probability`'s schema is a scalar `{type: number, minimum: 0, maximum: 1}`,
highly specific but not an object; Rule E's wording silently assumes objects). A
regex for parameter-values contradicting invariants found 4, missed two that
reading had already found, and matched `Kairos` on the word "window". Every one of
those flags still had to be read to be adjudicated, so the detector saved nothing
and cost a false sense of coverage.

**A detector's silence is not a result.** It cannot distinguish "checked and
sound" from "not checked", and the sound verdicts are the larger half of this
work — they are what stops the next reviewer re-deriving the same conclusion.
Reading produces a positive finding either way.

**Three of the defect classes are prose against prose, and no field comparison
reaches them.** The card can be wrong about itself, but the commentary can also
be wrong about the card: `Noise`'s critique asserted that task-dependency was
"unmentioned in the mechanism" when the mechanism says "irrelevant to the current
`{{task}}`" and references it as a dependency. `Prioritize`'s tradeoff states
that impact-effort is "deliberately not urgency-weighted" while the card carries
an `urgency_weight` parameter. Nothing that reads only the JSON will ever look at
those sentences, and nothing that reads only the commentary will notice they are
false.

**The fix often comes from the commentary rather than from judgment**, and only
reading finds it. `Decompose` asserted "Subproblems must be independent"; its own
critique conceded the invariant "is almost always violated in practice"; and its
broad-use intersection said independence *criterion*. Criterion, not property —
that single word is the whole repair, it was already written down, and no
detector would surface it because nothing in the card is malformed.

**The judgment calls are irreducibly semantic.** `Greet` mandating cryptographic
verification is defensible because first contact is between parties who cannot
yet trust each other; `SpotAudit` mandating a verifiable random function is not,
because an audit inside one trust boundary needs no such thing. Same surface
shape, opposite verdicts, and the difference is knowledge about the world rather
than a property of the text. The sharpest instances turn on a single external
fact: `Compress`'s size invariant is unsatisfiable because of the pigeonhole
principle, and `Parallel`'s simultaneity claim is false because async/await
interleaves on one thread. Both cards are internally consistent and well-formed.
Nothing in the repository contains the fact that decides either one.

**Verification passing is not the same as being right, in both directions.** A
staged edit that clears `sema apply --check` can still be wrong — the check does
not see cycles through `references`, and one such edit passed validation and
surfaced later as two dozen mismatched hashes. It also fails on edits that are
correct: an invariant rewritten to use a concept the card does not yet declare
trips the Forward rule, and the fix is to reason about whether the dependency is
real rather than to drop the wording. Treat a failure as a question about the
change, and a pass as silence rather than agreement.

Use the list below as a reading aid — the thing you hold each card against — and
not as a specification to implement.

### What to look for

These classes were each found by reading, and each has multiple instances. They
are what to hold a card against; none is detectable by a validator today.

- A **required schema property absent from the card's own
  `every_context_needs`** — the schema excludes contexts the commentary admits.
- The **mechanism enumerating components the schema cannot hold** ("It specifies:
  1. Preconditions, 2. Action, 3. Postconditions, 4. Rollback" against a schema
  carrying none of the last three).
- An **invariant contradicted by its own failure mode**, where the failure mode
  says the invariant *cannot* hold rather than merely that it can be violated.
  Invariant-plus-matching-failure-mode is the correct division; the defect is
  narrower than it looks.
- An **escape clause in an invariant** — `should`, `(optional)`, `unless`,
  `significantly`. A hedged invariant is not one.
- A **parameter value contradicting an invariant**: a `Random` strategy under a
  Determinism invariant, a `Lenient` setting under a non-compensatory one, a
  documented "willingness to overspend" under a hard ceiling.
- An **invariant that is a definitional identity** and so cannot fail
  (`Allocated + Remaining = Total` where allocated is defined as the difference),
  or **vacuous** (`within [0.0, 1.0] or [-inf, +inf]`).
- An **undecidable invariant**: `~`, `>>`, "significant", "relevant",
  "semantically opposite", "truthfully reflects".
- An **invariant referencing a quantity no parameter defines** (`T_max`,
  `Max_Retries`, an unnamed `Threshold`).
- A **circular precondition** that assumes what the mechanism determines
  ("Transient failure" on a pattern whose first step is classifying transience).
- **Gloss or mechanism overclaiming the contract** ("strictly increasing" over an
  invariant permitting equality; "quantitative or qualitative" over a
  numeric-only schema).
- **One handle carrying several concepts.** Find these by reading how dependents
  actually use the `{{placeholder}}` in their own sentences — across *all* hashed
  text fields, not only mechanisms. `Identity` was serving agent identity,
  equality of meaning, the algebraic unit element, and individuation; two of the
  borrowers were visible only in invariant labels.
- **A contract falsified by the card's own enumerated broad-use contexts.** Read
  the invariants against `usage.broad_contexts` one context at a time and ask
  whether the invariant survives each. `Compress` required output "strictly less
  than" input, which no lossless coder can satisfy on every input — pigeonhole,
  2^n inputs against 2^n-1 shorter strings — and gzip and zstd, listed *first* in
  its own contexts, carry stored blocks for exactly that case. `Parallel` claimed
  "A and B simultaneously" while listing async/await, which is interleaving on
  one thread. `Deep` stated an invariant over parent and child nodes that held in
  none of its four contexts, because not one of them produces a tree. The
  contexts are the card's own admission of scope, so a contract they falsify is
  wrong about itself.
- **A schema and a `varies` line that disagree about the same field, in either
  direction.** A field can be required while the commentary assigns it to
  descendants, and a field the intersection names can be left optional.
  `Hypothesis` had both at once: `confidence` required though confidence
  tracking is declared descendant territory, and `status` optional though the
  intersection names it. Also check invariants against the schema — `FrameSpec`
  mandated success criteria in an invariant while leaving `success_criteria`
  optional, so an instance could validate and breach the invariant at once.
- **An invariant that *causes* the failure mode listed beneath it.** Stronger and
  rarer than one that merely fails to prevent it, and the direction is what makes
  it a defect. `Dialectic` required a synthesis resolving a contradiction and its
  postcondition required a synthesis, so correctly finding a thesis unsalvageable
  breached the contract — leaving one compliant escape, weakening the antithesis
  until something fit, which is the Strawman Critic failure named directly below.
  `Card` was a three-way version: immutable by invariant, refreshed by mechanism,
  with "CARD not updated" as its first failure mode.
- **A relative judgment stated as an absolute one.** The repair is always to name
  the frame: `Realizable` grounded leaves in "known primitives" without saying
  known to whom or in which environment, so no second party could recheck the
  claim; `Interpret` asserted that meaning depends on context, which no
  implementation can violate, where the operational content was to record the
  context used. `Equivalence` carries the pattern to copy — an explicitly
  canonicalization-relative invariant.
- **A failure mode naming a quantity the card mentions nowhere else.**
  `Realizable` listed Resource Blindness — "physically impossible given the
  budget" — with no budget invariant, no budget parameter and no budget
  dependency, so the failure was named and undetectable. This is the same defect
  as an invariant referencing an undefined quantity, one field over.
- **Commentary that is wrong about the card.** A defect class in its own right,
  because the manual is the review surface the next reviewer trusts, and no
  field comparison reaches it. Measured on one pass: `Dialectic`'s tension said
  infinite regress had "no depth limit" while its `rounds` parameter is bounded
  at [1, 5]; `Deep`'s intersection named `Discover` as its horizontal sibling,
  which is a `Society`/`Protocols` network broadcast; `Realizable`'s
  `usage.intended` and `usage.every_context_needs` both declared a fixed 3-class
  rating scheme as intersection while the mechanism says in as many words that
  rating semantics belong to descendants; `Interpret`'s tension read
  Non-Destructive as forcing a caller to retain originals forever. Correct these
  in the sidecar in the same pass, and say they were corrections.
- **A handle the library does not have.** Backticked CapitalisedNames in a
  mechanism are cheap to resolve against the corpus and are not always there:
  `Deep` and `DeepResearch` both contrast against `Broad`, which does not exist —
  `BreadthGovernor` limits fan-out and is not the axis — leaving `Deep` as half
  of a declared pair. Resolving one is mechanical; the response is not. Minting
  the counterpart is a naming decision and belongs to Henrik, so describe the
  missing side in prose, and flag it.

Before minting anything, satisfy the library's own gates and this repository's
declared authoring policy rather than your judgment. `PatternDiscovery` requires
a declared search method followed by structural comparison against retrieved
prior art; similarity may nominate candidates but cannot decide coverage.
`MintWhenFriction` requires recorded friction evaluated under a sufficiency rule
declared before the decision. This repository currently uses three instances of
explanation overhead or one critical coordination failure as that local rule.
Under it, one ordinary borrower is not enough — fix the borrowing site instead,
lowercasing the concept per Rule H.

Record every verdict, including the sound ones and the reason they are sound.
Sound results are the larger half of the work and they are what stops the next
reviewer re-deriving the same conclusion.

### If the database is ever lost anyway

A cycle used to destroy the vocabulary: validation missed it, the rebuild caught
it only after replacing the database with an empty one, and the next verify run
overwrote the sole backup. All three are fixed, and
`scripts/apply_vocabulary_change.py` runs the steps in the order that works. Use
it, and this section should stay theoretical.

It is worth knowing the recovery anyway, because the same recovery covers any lost
database. `data/vocabulary/` is tracked, so the exports can be restored from git
and the database rebuilt from them — the JSON is sufficient, and the database is
never the only copy. Keep a `git stash create` snapshot while working: it records
tracked and untracked files into `stash@{0}` *without* reverting the working tree,
unlike plain `git stash`.

**Stage explicit paths. Never `git add -A` here.** More than one agent works in this
tree, and the apply chain leaves the worktree dirty across four steps, so `-A`
commits whatever anyone else has in flight. It has already happened: a tension-sweep commit
also carried another agent's edits to `paper/sema.tex` — a new abstract sentence and
an introduction paragraph — which were invisible in the log and attributed to the
wrong change. It was repaired by splitting the commit (`a80cd3d` is now the paper
change), which was only possible because nothing had been pushed. Name the paths you
touched.

The same non-atomicity affects readers. `sema apply` writes the database,
`export_sema.py` rewrites `data/vocabulary/`, `rebuild_vocabulary.py` rewrites it
again, and `verify --refresh` regenerates the manuals and the paper's hash
references. Anything reading the repo during that window — a paper build especially
— can capture a state that never existed as a consistent whole. A build run
concurrently with an apply was observed resolving the same paper references to
different hashes on successive runs, with `HEAD` never moving. Until there is a
lock or a snapshot, do not run `scripts/compile_paper.sh` while a vocabulary change
is in flight, and check `git status` is clean before starting either.

`data/design_critique.json` and this file are not derived from the database and
survive independently of it. That is a further reason to write the reasoning down
in the same pass as the card edit rather than afterwards: a card can be replayed
from a script in minutes, and the argument for why it changed cannot.

After apply/export and staging cleanup, run:

```bash
python scripts/verify_vocabulary_change.py --refresh
python scripts/verify_vocabulary_change.py
```

`--refresh` retains regenerated manuals, audit reports, vocabulary information,
and current documentation hash references. Check mode is non-destructive and
also verifies database/export parity, every exported hash, and a clean
deterministic rebuild. Review all generated changes before committing.

If paper content or a paper-cited hash changes, also run
`scripts/compile_paper.sh` using the existing style. Do not use semantic work as
an opportunity to alter typography.
