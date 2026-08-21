# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Dates are ISO 8601 (`YYYY-MM-DD`).

This file records vocabulary-level changes between versions — additions, renames, relocations, mechanism rewrites, retirements, and governance updates that a downstream consumer would want to know about when running `sema pull` — as well as tooling changes that affect how consumers interact with the protocol (CLI flags, MCP tool changes, behavioral defaults).

---

## [Unreleased]

### Added

- Published versioned canonicalization-v2 golden vectors with exact preimages,
  digests, normalized values, and rejection cases for independent implementations.

### Fixed

- Canonical hashing now rejects non-finite numbers, overflowing JSON reals,
  duplicate JSON members, invalid Unicode scalar strings, non-string object keys,
  and other Python-only values before graph mutation. Local apply and remote
  library installation now share the same strict JSON parser. String whitespace
  normalization now uses an explicit protocol repertoire rather than the host
  runtime's evolving whitespace classification. The previously unversioned NFC
  database is documented as a v2 compatibility boundary rather than silently
  changed; all 457 official pattern identities remain unchanged.

## [0.5.2] - 2026-08-21

### Fixed

- Removed 19 stale handles from the built-in `standard` preset. Those handles
  were absent from the current bootstrap vocabulary, so selective builds warned
  and skipped them. A regression test now requires every standard-preset handle
  to exist in the authoritative `taxonomy.db`.

### Deprecated

- `data/experimental.db` is now explicitly a frozen historical snapshot. It
  remains in the repository for review, but is not maintained, packaged, or
  selected by any built-in Sema tooling. The bundled tool and its built-in
  presets use only the authoritative bootstrap vocabulary in `data/taxonomy.db`.

## [0.5.1] - 2026-08-20

### Fixed

- MCP now advertises the conditionally exposed write tools under their documented
  public names, `sema_mint` and `sema_pull`, instead of underscore-prefixed
  implementation names that clients could not call.

## [0.5.0] - 2026-08-12

457 -> 457 patterns. Aggregate roots: semantic set
`5b6be2ac2db98eedbc89b1c240fe3660db5d01784db5bbb1177b1d7a76c05f64`,
catalog `87a541595288b870daa23487a44feeb46517e9eca0416f46dc61ebe43da36064`.

### Added

- Verified third-party vocabulary installation through `sema install <library.json>`,
  name-based selection with `sema use <name>`, and explicit `sema update <name>`.
  Releases carry one JSON file per pattern in a checksummed ZIP, declare semantic
  and catalog roots, and compile to an immutable local SQLite snapshot. The
  bundled vocabulary remains the offline default.
- Deterministic official-bootstrap release packaging. Each tool release attaches
  a generated `library.json` and versioned pattern ZIP whose identities and roots
  are verified against the bundled database, allowing the bootstrap vocabulary
  to be installed through the same public contract as a third-party library.
- Self-service third-party publishing through `sema package`. The command exports
  a project database as one JSON file per pattern, creates a deterministic ZIP,
  computes its checksum and both aggregate roots, writes `library.json`, and then
  recompiles and verifies a fresh local read model before exposing the release
  files. GitHub shorthand generates a stable manifest URL and a version-pinned
  artifact URL.

### Changed

- A follow-up audit of the 0.4 delegated decisions corrected decisions that
  were incomplete or left the durable record and hashed card in disagreement.
  `Assessment` now makes strengths and weaknesses optional while requiring a
  non-empty recommendation list; `Solution` makes component trees conditional
  on composite outputs and requires creator and creation time within provenance;
  `Mutex` is an ownership-based `Lock` specialization in Infrastructure rather
  than a distributed-fencing protocol; `SteelmanCheck` separates
  counter-argument adequacy (`Judge`) from decision robustness (`Check`);
  `PromptChain` replaces the undefined Skip path with bounded retry-or-halt
  semantics; and `FailureTrace` binds evaluator, clause, evidence, and signing
  time in a content signature that `ReceptivityGate` verifies over the exact
  payload. `Trace` now states partial coverage directly. These are semantic
  corrections; canonicalization is unchanged. The canonical rebuild changes
  267 of 457 identities: eight repaired definitions, two explicitly reviewed
  exact-parent retargets, and 257 transitive dependency updates. Every changed
  pattern records its public 0.4 identity in `_meta.supersedes`.
- `sema build --source` accepts an installed library name as well as a database
  path. Managed sources are reverified before copying, and the resulting project
  database is writable even though installed releases remain read-only.

### Security

- Remote libraries cannot supply executable or precompiled database state. Sema
  accepts only the bounded JSON pattern archive and always builds its own local
  read model. Managed-database verification now also rejects missing runtime
  indexes, unknown node or edge types, malformed metadata, missing endpoints,
  and invalid embedding payloads before activation.

## [0.4.0] - 2026-08-04

**The 0.4 reasoning pass re-mints 426 of 452 pattern identities (94%) relative to 0.3.0.** No canonicalization change: hashes move because definitions improved -- 324 patterns were reasoned through individually against the design manual (254 changed, 57 confirmed sound, and 13 OPEN pattern verdicts subsequently adjudicated; a separate sidecar question on `Solution` was also decided) -- and cascades propagated the rest. Every identity-changed pattern carries the 0.3.0 `sema_id` in `_meta.supersedes`, so 0.3.0 consumers converge via `sema pull` instead of orphaning.

452 -> 457 patterns. Aggregate roots under the schemes introduced below:
semantic set `502d7f981a29a4a134e3080cdc4f361049a30f30ece026224a668bda80a83661`, catalog `146db4c0b6172432a0694baa74263a2e33edfce2c5ba7756c33622f7bc69e324`.

### Added

- Two explicit aggregate commitments: `sema-semantic-set-v1` for the
  unordered set of unique definition digests, and `sema-catalog-v1` for exact
  handle-to-definition bindings. Both use domain-separated leaves and the
  RFC 9162 Merkle Tree Hash construction. `sema_root()` exposes both;
  `sema_handshake(ref="catalog")` verifies the namespace mapping.
- Canonical `scripts/verify_vocabulary_change.py` workflow for contributors and
  CI. It refreshes or non-destructively checks the design manual, audit,
  vocabulary root, documentation hash references, database/export parity,
  exported hashes, clean staging, and deterministic reconstruction in one
  command.
- `ExponentialBackoff`, a concrete child for capped geometric delay growth
  with configurable jitter. Retry eligibility, budgets, and reset policy remain
  caller-owned rather than requirements of the delay strategy.
- `MetricReading`, a definition-bound quantitative value with optional
  observation context and dimensions. It references the Metric definition that
  supplies its derivation rule and value schema; it does not declare `extends`
  because a reading is an output under a definition, not a kind of definition.
- Claude Code ref-gate hook (`hooks/ref_gate.py`), registered by the Claude
  Code plugin on `UserPromptSubmit` and `PreToolUse` (`Agent|Task|SendMessage`).
  Scans inbound messages for content-addressed refs (`Handle#stub`) and
  verdicts them against the active registry: stale refs are reported as
  model-visible context by default (`SEMA_REF_GATE=warn`) or blocked with a
  repair message in opt-in enforce mode. Unknown handles never block; the gate
  fails open if the registry is unavailable. See `hooks/README.md`.
- `sema check`: verdict content-addressed refs in stdin text against the
  active registry (`--db` override, `--json` for the versioned verdict
  document; exit 0 clean, 3 stale, 1 registry error). The scan/verdict
  logic lives in `sema.core.check` and is shared by harness shims — the
  Claude Code ref-gate hook is now a thin adapter over it. Ships with a
  conformance fixture set that any future harness shim replays.
- Lean 4 formal-verification pilot for the handshake decision kernel and
  canonicalization type-tag domain separation. Proofs are pinned to Lean
  4.30.0, checked without `sorry`, independently rechecked by `leanchecker`,
  and enforced by blocking CI.
- Machine-readable `verification/proof-manifest.json` linking theorem names to
  production implementations, conformance tests, and explicit assumptions.
- `sema_handshake(..., strict=true)` mode. Only the full 64-character hash can
  produce `PROCEED`; a matching truncated stub returns `REQUIRE_FULL_HASH`.
- `scripts/apply_vocabulary_change.py`, running apply, export, rehash and
  re-export in the one order that works, stopping at the first failure. The
  order matters because `rebuild_vocabulary.py` reads the exports while
  `sema apply` writes the database, so rebuilding before exporting rehashes the
  previous state.
- `scripts/audit/dangling_handles.py`, reporting CapitalisedNames in pattern
  text that resolve to no pattern, with the instance count used by this
  repository's declared three-instance authoring policy. Covers backticked
  names and multi-part CamelCase; its docstring records why single bare
  capitalised words are not detectable in this corpus.
- `EpistemicCascade` (Mind/Reasoning): a conclusion inherits the verification
  assurance of its weakest load-bearing premise. Assurance is graded by how a
  premise was checked (Independent / Self / None); a `Check` yields a `Status`,
  and this pattern grades what that outcome is worth given how it was obtained.
  References `Verification`, `Assumption`, `EpistemicCalibrate`,
  `BeliefTracking`, `Check`, `Status`.
- New handles relative to 0.3.0, besides the above: `Equivalence` (from the
  `Identity` untangling), `ExponentialBackoff` (split from generic `Backoff`),
  `MetricReading` (readings separated from `Metric` definitions), and `Trait`.

### Changed

- `Role` now defines a bearer-independent contextual function rather than an
  already assigned permission/responsibility bundle. Every role declares its
  expected contribution; authority and obligation identifiers remain optional
  facets, while assignment, occupancy, enforcement, and conflict resolution
  stay with descendants or callers. Because canonical `Permission` and
  `Responsibility` are already Agent-bound instances, the broad parent no
  longer claims either as a component. The authored definition moves from
  `Society/Governance` to `Infrastructure/Data Structures`; only `Workflow` and
  `OrchestrationLoop` receive dependency-hash cascades. Its supersession
  metadata now lists all six distinct Role identities shipped from v0.1.18
  through v0.3.0 and excludes an unreleased rebuild identity.
- `Refine` now operates on immutable artifact versions: it accepts the current
  `Artifact` and a caller-defined `Condition`, composes `Critique`, and yields a
  successor `Artifact` for return or another pass. It no longer requires an
  external-state `Act` or narrows every revision target to an `Incongruity`.
  `PhasedRefinement` no longer requires a mutable artifact; its other contract
  and placement questions remain explicitly open for its own review. The
  semantic change cascades only to `StyleSpec`, and both edited cards now cite
  their exact public v0.1, v0.2, and v0.3 identities.
- `ProphetFanOut` now defines bounded, causally traceable generation of
  multiple distinct scenarios from a contemplated action and starting context.
  Binary branching is valid; computational abundance, a fixed three-scenario
  output, entropy thresholds, mandatory tail weighting, desirability
  judgments, aggregation, and quorum policy are no longer universal
  requirements. `BreadthGovernor` no longer claims that `ProphetFanOut`
  pre-scores or prunes candidates: generation remains upstream, while the
  governor owns prioritization and reduction. The semantic change cascades
  only to `NormCheck`.
- `UniqueHandle` now makes authority linear without claiming that a digital
  representation cannot be copied. One authoritative holder-generation pair
  governs use and transfer; the representation alone grants nothing, a
  conditional transfer has one commit point and one winner, stale generations
  fail closed, and an unobserved result must be resolved before use or retry.
  The false `Break` recovery link and implementation-specific `StateLock` and
  `Agent` requirements are removed; `Resource` is now the sole conceptual
  dependency. The change cascades through `HeldRelease`, `Award`, and `Oracle`
  without altering their payloads, and all four cards now cite exact public
  v0.3 supersession IDs.
- `Rollout` now executes the approved `ExecutionManifest.operation_sequence`
  rather than treating prototype-only `Build` as a production executor. A
  durable `RolloutManifest` write-ahead record precedes each canary or forward
  action; only Canary `proceed` authorizes wider execution, while non-proceed,
  inverse-admission failure, and breaker paths emit `Break`, compensate, record,
  freeze, and require a new Rollout. `EjectionSeat` mode takes precedence,
  including PAUSE remaining open and EMERGENCY promising neither cleanup nor a
  final write. The false `WorldReversible` and `MonitorReport` promises are
  removed. The semantic rewrite cascades to
  `Deploy`, `OrchestrationLoop`, and `RealizationProtocol`; their payloads are
  unchanged and their supersession metadata now cites exact public v0.3 IDs.
- `Rally` now selects responders before MUSTER, counts only confirmed selected
  participants, terminates both phases at one deadline, and always yields an
  identified formed-or-dissolved `Outcome`. Its participant bounds match
  `Select`, while ballot-specific `Quorum`, optional leadership, authentication,
  and contextual selection policy no longer masquerade as parent requirements.
  `Delegate` now transfers an existing `Task` only after explicit acceptance,
  preserves single ownership across refusal and failure, and treats `Break` as
  an invoked protocol; auction, probing, holographic inheritance, and unsupported
  dependency/cycle enforcement remain caller or descendant policy. The semantic
  rewrites cascade to `Handoff` and `Nucleate`.
- `Work` now requires only `effort_cost`; `timestamp` remains an optional
  provenance property. Directed resource expenditure is therefore still Work
  when a context cannot or need not record a clock reading, while descendants
  remain free to require one. The release-scale dependency cascade changes 272
  of 455 pattern identities. `RolloutWatch`, `OptimisticSolver`, and
  `RigorousSolver` were independently reviewed before their exact `extends`
  pins were retargeted to the resulting `Monitor` and `PolymorphicSolver`
  identities; no authored contract on either parent or any child changed.
- `Metric` now defines quantitative meaning rather than conflating that
  definition with one timestamped observation. Its required fields are the
  target property, derivation rule, and quantitative value schema; observed
  values move to `MetricReading`. `Feedback` and `Result` now consume readings,
  while `Optimize` retains the Metric objective and compares baseline and
  candidate readings. `Score` is explicitly an evaluative result rather than a
  generic measurement. The batched split changes 251 of 456 identities,
  including independently reviewed retargets of `OptimisticSolver` and
  `RigorousSolver` to the resulting `PolymorphicSolver` identity.
- Seven independently reviewed consistency repairs preserve broad parents while
  making their enforceable boundaries explicit. `Workflow` now requires only
  steps and directed prerequisites; typed edge data, acceptance specifications,
  role bindings, recursion, and daemon semantics remain declared options.
  `RetrievalAugment` is neutral across vector, index, graph, and other stores,
  with selection policy delegated to callers or descendants. `CreativeBlend`
  owns novelty/value admission without universally invoking `NoiseInjection` or
  duplicating its temperature. `RealizationProtocol` now composes the actual
  FrameSpec producer, judges an ExecutionManifest against a Budget and Criteria
  before Rollout, distinguishes RolloutManifest from Outcome, and delegates
  iteration to `OrchestrationLoop`; that loop now has an explicit per-run
  `iteration_limit`. `MutualInformation` uses the general KL definition and
  scopes its entropy bound, while `Compare` permits declared cross-type rules.
  The batch changes 16 of 456 identities through seven authored definitions and
  nine ordinary dependency cascades; no exact specialization pin moves.
- `Critique` now remains the reasoning operation over a target and declared
  criteria, while its yielded `Assessment` remains the authoritative output
  record. The duplicate output-shaped `Critique.data_schema` is removed
  without deciding Assessment's separate schema questions. The repair changes
  51 of 456 identities through the ordinary dependency closure; the two exact
  `PolymorphicSolver` children were reviewed and retargeted without changing
  their authored contracts.
- **Breaking aggregate-root migration (semahash 0.4.0):** aggregate identities
  now use two domain-separated RFC 9162 schemes: `sema-semantic-set-v1` for the
  unordered set of unique definitions and `sema-catalog-v1` for exact
  handle-to-definition bindings. Root payloads carry their scheme; malformed
  inputs and scheme mismatches fail closed. The aggregate migration itself does
  not change pattern IDs; reviewed card edits in this release do. The final
  456-pattern snapshot commits semantic-set root
  `1b90a7b9f4756e60457dcf88e6d5117e6a35affbf387a5a572cca585d08e532b`
  and catalog root
  `44427e40b46c728fd2e929b3816aab3f22661f2bae5d2729d01e294a0069b484`.
- `extends` replaces `derived_from` for new specialization claims. It is
  hashed, pins the exact full Sema ID of the parent definition, emits `IS_A`,
  and does not silently follow later definitions sharing the handle.
- `sema apply` preserves exact `extends` pins by default. In the current
  single-version workspace, an unresolved pin or a parent edit that would
  strand a child fails preflight before mutation. After reviewing the
  relationship, stage the child and pass `--retarget-extends`; only staged
  claims move. Pull and direct minting enforce the same boundary.
- Pre-0.4 cards using `derived_from` remain readable and hash-verifiable under
  their original key. The key is not normalized to `extends`, does not acquire
  `IS_A`, ordering, or active-parent semantics, and cannot coexist with
  `extends`; explicit migration mints a new identity.
- Context negotiation now derives its set commitment from stored pattern
  identities using the catalog Merkle construction, rather than a second
  hand-written JSON hash path. This binds every requested handle to its
  definition, so swapped name mappings cannot falsely agree. The MCP tool
  still returns an eight-hex-character cooperative drift prefix, and
  verification now requires its scheme.
- `Backoff` now defines the general failure-responsive delay family instead of
  requiring exponential growth, jitter, reset-on-success, and a retry budget.
  `Retry` explicitly selects `ExponentialBackoff` for transient failures,
  `StateLock` composes with the generic policy family, and `Yield` no longer
  links technical retry delay to negotiation concession.
- The shorthand vocabulary reference is now generated on demand instead of
  tracked and silently staged by the pre-commit hook. Its exporter uses the
  current `_meta.path` taxonomy and the database remains the source of truth.
- Cooperative handshake behavior remains the default for non-adversarial drift
  detection, but successful responses now report `assurance: "prefix"` or
  `assurance: "full_hash"` plus the selected mode. Documentation no longer
  describes a truncated prefix match as byte-exact identity proof.
- Pattern authoring now includes an explicit constraint-placement test: general
  parents contain only cross-context, identity-defining contracts, while
  strategy, deployment policy, and contextual diagnostics belong in
  descendants, callers, parameters, or design commentary.
- The design manual now labels broad-use intersections as review hypotheses
  and critiques as diagnostics rather than contract requirements. Foundational
  examples no longer treat field counts as evidence that a pattern is weak.
- `BearerToken` now defines representation-neutral possession semantics.
  Opaque tokens validated by lookup or introspection and structured tokens
  validated locally both satisfy the parent; signatures, expiry, revocation,
  and transfer policy are descendant or deployment choices.
- The thirteen OPEN pattern verdicts left by the reasoning pass, plus a
  separate `Solution` sidecar question, were adjudicated, each with its
  governing principle recorded in the external reasoning ledger: `Trace`
  (fan-in 203) states best-effort coverage instead of promising that every
  modification is recorded, with a Silent-gap failure mode; `Mutex` moves
  Physics -> Society/Coordination and its `accepts` edge is corrected from
  `task` to `actor`; `Axiom` moves Society -> Mind/Reasoning; `NormCheck` is
  restated around what all three `action_on_detect` modes share; `Branch` is
  kept rather than retired and now differentiates itself from `Gate` with a
  reference edge; `Assessment`'s Reference invariant admits systemic scope;
  `MutualInformation` gains an estimator-conflation failure mode; and
  `SteelmanCheck`, `Translate`, `PromptChain`, `CreativeBlend`,
  `RealizationProtocol`, and `FailureTrace` were adjudicated without further
  hash changes at release time. The separate `Solution` sidecar question was
  likewise recorded without a hash change. Follow-up corrections are
  documented under 0.5.0.
- Review method: when a parameter's values differ in what happens after an
  invariant's property holds, the invariant was mis-scoped; restate it around
  the property all values share (`docs/guides/review-method.md`, third
  occurrence of the defect class).
- Paper: the introduction now states the value proposition explicitly --
  memory that survives summarization, the mechanism-scoped reasoning claim
  with its boundary as a prediction, binding steps, the standard-library
  framing, and why the gaps humans left in text are gaps in the model. Paper
  builds go through `scripts/compile_paper.sh` (now an AGENTS.md rule).

### Fixed

- `PolymorphicSolver` no longer calls all five Solver surfaces mandatory in its
  Interface Non-Compliance failure mode. Manifest and Execute remain mandatory;
  Consult, Verify, and Feedback fail conformance only when advertised but not
  provided.
- The design manual now describes `Lock` as the K=1 mutual-exclusion contract
  its payload actually defines. Following the base-lock semantics used by Linux,
  starvation and convoying remain queue-discipline concerns for descendants
  rather than universal Lock failure modes.
- The canonical vocabulary-apply wrapper now forwards the reviewed
  `--retarget-extends` option and pins both the database and Python imports to
  its own checkout. An isolated worktree can no longer silently execute an
  editable `sema` installation from a sibling checkout while mutating the
  local database.
- Supersession metadata for `OptimalStop`, `PURE`, `PURECheck`, `ParetoFront`,
  `PatternDiscovery`, `PatternEmergence`, `MintWhenFriction`, `PreMortem`,
  `ProphetFanOut`, and `BreadthGovernor` now lists the distinct exact
  identities shipped in v0.1, v0.2, and v0.3 and excludes unreleased rebuild
  identities. Eight of these corrections are metadata-only and therefore do
  not alter the patterns' semantic hashes.
- `update_doc_refs.py` no longer overwrites refs that are cited precisely
  because they are not current. `docs/specification/versioning.md` illustrates
  stub divergence by contrasting a superseded version with the one that replaced
  it, and the rewriter overwrote both sides with the current stub — so both
  illustrations ended up quoting the same stub twice, which cannot demonstrate
  stubs differing. A region fenced with `<!-- doc-refs: pinned -->` is now left
  alone, and refs outside the fence in the same file are still refreshed. Both
  examples in the versioning spec are repaired and now cite real members of
  `PropheticQuorum`'s supersession chain.
- `rebuild_vocabulary.py --replace` keeps the rebuilt database when it reports
  hash drift. Drift means the stored hashes were stale — typically a dependency
  changed and its dependents were never rehashed — and the rebuild has just
  corrected them in place, so the database it built is the better copy.
  Restoring the backup discarded that correction, and because a caller
  re-exports afterwards, the stale hashes were written straight back and the
  next rebuild found the same files again. Observed looping on a 207-dependent
  cascade. The exit code is still non-zero so the finding stays visible, and the
  message now says the hashes were corrected rather than lost.
- `sema apply --check` now refuses a dependency cycle instead of passing it.
  The topological sort dropped every edge leaving the batch, so a cycle between
  a staged pattern and an already-committed one was invisible to it, and the
  sort ran after `--check` had already returned. A mutual `references` pair —
  a dependency one way and a citation back — is a cycle and is now reported
  with its path. Only cycles containing a pattern being added are reported, so
  a pre-existing cycle elsewhere cannot block an unrelated change.
- `rebuild_vocabulary.py --replace` no longer discards the vocabulary when the
  rebuild fails. It kept the freshly created database and deleted the backup on
  the failure path, and a failed rebuild has no rebuilt database to keep — only
  an empty one — so the next export wrote zero patterns over `data/vocabulary/`.
  `--replace` is now honoured only on success, `--check` never keeps its empty
  database, and backups are timestamped so a later run cannot overwrite the
  backup an earlier one took.
- MCP extras now exclude the incompatible 2.x SDK line, which removed the
  `mcp.server.fastmcp` API used by the server.
- Vocabulary information statistics now derive layer and category from the
  canonical `_meta.path` instead of classifying every current pattern as
  unclassified.
- The generated design manual no longer embeds the current date, keeping its
  CI freshness check stable across calendar days.
- CI now lints and format-checks the manual and vocabulary-information
  generators enforced by the canonical verification workflow.
- Handshake examples no longer embed stale pattern or vocabulary hashes; they
  reuse the canonical challenge response returned by `sema_handshake`.
- Deterministic rebuilds isolate temporary `sema init` registry writes instead
  of modifying the developer's real `~/.config/sema` registry.
- Updating an existing pattern now replaces superseded schema edges and removes
  orphaned contract facets instead of leaving old invariants, preconditions, or
  postconditions attached to the graph.
- Updating or removing a pattern signature or `_meta.related` declaration now
  prunes its stale graph edges without disturbing parallel relationship types.
- Vocabulary export always loads the current checkout's hashing code, and the
  deterministic rebuild compares against its pre-rebuild input snapshot. This
  avoids stale installed-package hashes and false drift reports on intentional
  uncommitted vocabulary edits.
- Vocabulary audits now validate current `path`/`ring`/`tier` metadata and
  report missing contract fields as advisory coverage rather than structural
  problems. Broad primitives are no longer labeled defective merely because
  their contracts are intentionally absent.

---
- 98 identity-changed patterns did not carry the published 0.3.0 `sema_id` in
  `_meta.supersedes`, so `sema pull` could not map consumers' pinned hashes
  forward -- they would have been orphaned rather than replaced. Backfilled per
  `docs/guides/lifecycle.md`; all 426 identity-changed patterns now carry
  complete chains. The field is unhashed, so the backfill cascaded nothing.
- `docs/information/audit.md` had gone stale against the database, which is
  what fails CI's vocabulary-workflow check (3.12 job only).

## [0.3.0] - 2026-07-06

**Breaking: canonicalization v2 — every pattern hash and the vocabulary root change.** No dual-hash migration is shipped, deliberately: pre-0.3.0 vocabularies HALT on handshake against 0.3.0 registries (fail-closed working as designed) and converge via `sema pull`.

New vocabulary root: `46e651aeeb832fdc654d6e48ba2b9c9049f8585a5423371624426c1ab6d3f15b` (452 patterns, previously `39ca671a4dcb3075…`).

### Fixed — hash spec

v1 canonicalization allowed structurally different definitions to share one content address, breaking `word = hash(canonical(definition))`:

- **No domain separation**: `merkle_hash("1") == merkle_hash(1)`, `"" == [] == {}`, and a 2-element list collided with a 1-entry dict — two schema-valid patterns differing only in `data_schema` shape produced the same `sema_id`. Every hash-tree node input is now prefixed with a type tag (`s:`/`p:`/`l:`/`d:`).
- **Raw-key ordering**: dict entries were sorted by raw key but hashed by normalized key, so the same canonical form could hash two ways, and keys colliding after normalization silently dropped an entry (now a `ValueError` — fail closed).
- **Dependency alias collapse**: multiple aliases referencing the same handle collapsed to one insertion-order-dependent entry, silently dropping a dependency from the hash input. Multiple refs to one handle now hash as a sorted list (arity is semantic; alias spelling is not).

### Fixed — reproducibility

- `sema apply` write-back now refreshes dependency ref values in the source JSON (the batch is topo-sorted, so dep hashes are final). Previously files kept whatever dep hashes they were authored with, so stored `sema_id`s could not be recomputed from the files alone.
- `scripts/test_hash_verification.py` (the dependency-free independent verifier) updated to v2 and taught the dependency-canonicalization step. All 452 patterns now verify from their JSON files alone — this did not hold under v1.
- First pytest coverage for the hashing core (`src/sema/core/tests/test_hashing.py`): every v1 collision pair is a regression test.

### Changed

- All 452 pattern hashes, refs, and stubs regenerated; `docs/information/vocabulary_information.md` and `skills/sema-usage/SKILL.md` examples updated. Historical `_meta.supersedes` refs keep their original v1 hashes (archival provenance).

---

## [0.2.3] - 2026-04-18

Docs-only release. No code or vocabulary changes.

### Changed

- Safety section rewritten in `README.md` and `docs/README.md` to scope the sandbox recommendation to pattern-execution (not to sema itself) and to split **intended use** (reasoning and reference) from **executing patterns as recipes** (untested research territory).
- Stale `SEMA_ALLOW_MINT=true` instructions in `install.md`, `docs/guides/getting-started.md`, `skills/sema-mint/SKILL.md`, and `skills/sema-seed/SKILL.md` replaced with the 0.2.2 opt-out model (`SEMA_DISABLE_MINT=true`, `SEMA_DISABLE_PULL=true`). Tools tables gain `sema_pull` / `sema_root` / `sema_graph_skeleton`.

---

## [0.2.2] - 2026-04-18

Doc-vs-code drift fix for the MCP surface. 0.2.0's CHANGELOG, SKILL, and test file all claimed `sema_pull` was an MCP tool and `sema_mint` was exposed by default, but the server module still had `sema_mint` behind `SEMA_ALLOW_MINT=true` and no `sema_pull` at all. This release lands the code that matches the claims.

### Added

- `sema_pull` MCP tool — wraps `cli.main.update_db`. Returns structured JSON with `success`, `added`, `updated`, `skipped`, `cascaded_user`, `superseded_removed`, `superseded_kept_orphan`, `upstream_removed`, `vocabulary_root_before`, `vocabulary_root_after` (and `dry_run` / `error` when applicable).
- `SEMA_DISABLE_PULL=true` environment variable to hide `sema_pull` in read-only / pinned-vocabulary deployments.
- `src/sema/mcp/tests/` registered in `pytest` testpaths. The 6 tests for `sema_pull` / `sema_mint` registration and structured-output shape now run in the default suite.

### Changed

- `sema_mint` flipped from opt-in (`SEMA_ALLOW_MINT=true` required) to opt-out (`SEMA_DISABLE_MINT=true` to hide). Exposed by default.
- `update_db()` now returns a structured dict instead of a bare bool. CLI callers read `result["success"]` for the exit code; the MCP tool serializes the whole dict.

### Removed

- Legacy `SEMA_ALLOW_MINT` environment variable. Clean break, no back-compat shim.

---

## [0.2.1] - 2026-04-18

### Added

- `web/public/llms.txt` — served at `semahash.org/llms.txt` after the next web build (previously the file existed only in the gitignored `web/dist/` and was not deployed).

### Changed

- `reference/all_patterns_short.md` moved to `data/shorthand/all_patterns_short.md`. Generator (`scripts/export/export_short_hand.py`), pre-commit hook, installer hook, and lifecycle doc all updated to the new path.
- `install.md` refreshed for 0.2.0 (adds `sema_root` / `sema_graph_skeleton` to the MCP tools table; CLI section mentions `sema pull` / `sema categorize`; new "Keeping a project DB fresh" section).
- `experiments/orchestrator` submodule pointer bumped to the latest upstream commit.

---

## [0.2.0] - 2026-04-17 — Foundation Audit + Pull Loop

Two coherent threads shipped in this release:

1. **Foundation audit** — a cross-pattern refinement pass (dual-LLM proposal/review: Claude Opus 4.7 + Gemini 3.1 Deep Think, adjudicated by the author) tightened the governing rules and applied them to the entire library.
2. **Pull loop closure** — `sema pull` now reads `_meta.supersedes` and redirects retired handles to their replacements by default (opt-out via `--preserve-superseded`); `sema_mint` flipped from opt-in to opt-out.

**Vocabulary root:** `sema:vocab#mh:SHA-256:39ca671a4dcb3075855cb293380d1796105e2eca0de49b0537279b798b675ee6`
**Pattern count:** 452 (default) + experimental shelf.
**Scope of changes:** 31 new patterns, 5 renames, 1 moved to experimental, 71 layer relocations, 71 mechanism rewrites, 50 additional structural fixes (dedup / split / broken-ref cleanup), 3 new `derived_from` wirings, full supersedes population against the live users' db (360 patterns), plus hash cascades through the dependency DAG (399 pattern files differ from v0.1.27 in total — 31 new + 368 updated).

**Per-pattern reasoning:** This changelog lists *what* changed. For *why* each pattern exists, what its mechanism commits to, and the design commentary behind each rename / relocation / rewrite, see the design manual at [`docs/manuals/vocabulary-design.md`](docs/manuals/vocabulary-design.md). The manual ships with this release and is the authoritative review surface for vocabulary quality.

### Breaking changes for consumers

- **`_meta.layer` + `_meta.category` consolidated into `_meta.path: list[str]`.** The taxonomy is now represented as an ordered list — `["Society", "Governance"]` instead of `{"layer": "Society", "category": "Governance"}` — so deeper hierarchies (`["Society", "Governance", "Voting"]`) don't require a schema bump. Consumers reading `pattern["_meta"]["layer"]` or `pattern["_meta"]["category"]` should read `pattern["_meta"]["path"][0]` and `pattern["_meta"]["path"][1]`. The top-level `sema_layer` and `sema_category` fields are preserved as **derived** (read-only) exports for one deprecation cycle; new code should read `_meta.path`. Graph representation follows: `LAYER` + `CATEGORY` node types are superseded by `TAXONOMY_PATH` nodes (one per valid path prefix), linked toward the root by `PARENT_PATH` edges; patterns attach via a single `IN_PATH` edge to their leaf. Pattern `sema_id`s are unaffected (path lives in `_meta`, excluded from the Merkle input).
- **Old renamed handles are removed on `sema pull`.** The default behavior reads upstream `_meta.supersedes` and removes the local copy of any superseded pattern. Use `sema pull --preserve-superseded` to keep both the old and new handles. The pre-pull snapshot is still retained — `sema pull --undo` restores everything.
- **`sema_mint` is now exposed by default in the MCP server.** Previously required `SEMA_ALLOW_MINT=true`. Deployments that want to keep mint disabled must now set `SEMA_DISABLE_MINT=true`. (Note: the code change for this actually landed in 0.2.1 — 0.2.0 described the intended behaviour but shipped with the old gate still in place.)
- **Pattern hashes shifted widely.** The foundation audit rewrote 71 mechanisms and relocated 71 patterns; canonicalization (see below) changed hashes for 4 new patterns plus their dependents. Consumers who pinned specific hashes will see `sema pull` update them automatically via the supersedes chain. Code that references handles (not full hashes) is unaffected.

### Schema migration — path-based taxonomy

**Before (≤ 0.1.27):**
```json
"_meta": {"layer": "Society", "category": "Governance", "ring": 1, "tier": 1}
```

**After (0.2.0+):**
```json
"_meta": {"path": ["Society", "Governance"], "ring": 1, "tier": 1}
```

**Rationale.** Categories are sub-scopes of layers, not flat labels. `Physics/Primitives` and `Infrastructure/Primitives` were always distinct concepts that happened to share a leaf name; the pre-0.2 representation forced them onto one `CATEGORY` node with two `IN_LAYER` edges — a topology lie the queries had to paper over. The list form makes the scope explicit, supports arbitrary depth (`["Society", "Governance", "Voting"]`) without schema changes, and removes ambiguity at the graph level.

**Stricter validation (Pydantic, enforced on `sema apply`):**
- `path`: list of non-empty strings, length ≥ 1, first segment in `{Physics, Infrastructure, Mind, Society}`, full tuple in `VALID_PATHS`.
- Path segments cannot contain `/` (reserved separator).
- Pattern `handle` cannot contain `/` (avoids collision with taxonomy path text).
- `ring` ∈ {0, 1, 2}, `tier` ∈ {0, 1, 2, 3} — stricter than before.

**New CLI command:** `sema categorize <handle> --path Physics/Primitives` — validates against `VALID_PATHS` and rewires the pattern's `TAXONOMY_PATH` linkage atomically via the existing apply path.

**Migration for downstream consumers.** Run `scripts/migrate_taxonomy_to_path.py` against your `data/vocabulary/*.json` directory; it's deterministic, idempotent, and leaves `sema_id`s untouched. Then `sema apply --add data/vocabulary/` or `scripts/rebuild_vocabulary.py --replace` to get the `TAXONOMY_PATH` graph nodes. Mixed-state DBs (some patterns on `_meta.path`, others still on `_meta.layer`) are handled gracefully — the graph builder reads either shape and normalizes on write.

### Migration guide (from 0.1.27)

For a consumer running 0.1.27 who pulls to 0.2.0, the expected transcript is:

```
  + 31 new            (Physics primitives, FI Table 4 gap, §6 protocols, etc.)
  ~ 368 updated       (mechanism rewrites + structural fixes + cascading hashes)
  = 53 unchanged      (fast-path)
⚠️  5 user pattern(s) had hashes auto-updated due to upstream changes:
    AbductiveLeap, CognitiveSolver, Group, SolverRoot, Switch
→ 5 pattern(s) superseded by upstream, removed locally:
    CognitiveSolver   → PolymorphicSolver
    Linear            → Chain
    AbductiveLeap     → Abduction
    Switch            → Route
    SolverRoot        → RootSolver
ℹ️  Upstream removed 1 pattern(s); they remain locally as user patterns:
    Group
```

After pull, `sema pull --verify` confirms all stored hashes match recomputed values.

### Tooling (new in 0.2.0)

- **`sema pull --preserve-superseded`** (new CLI flag). Keeps locally superseded patterns alongside their upstream replacements instead of cleaning them up.
- **Orphan guard on supersession cleanup.** If a user-only local pattern still depends on a superseded one (via `sema_id` reference), pull keeps the superseded pattern in place and reports `superseded_kept_orphan`. Fix the dependent and re-run to complete the cleanup.
- **Post-pull warning for stale user-owned `_meta`.** When retained user patterns (absent from upstream) still carry pre-0.2.0 `_meta.layer` + `_meta.category` instead of `_meta.path`, pull flags them by name and points at `scripts/migrate_taxonomy_to_path.py`. Notify, don't auto-migrate — user owns those patterns and the migration is a content decision.
- **Post-pull notice for orphan sub-nodes.** When supersession cleanup leaves INVARIANT/PRECONDITION/POSTCONDITION nodes with no incoming edges (their parent pattern was removed), pull lists them with their text so consumers can do a follow-up cleanup. No auto-GC.
- **Design manual** (`docs/manuals/vocabulary-design.md`, new). Per-pattern design commentary rendered from a sidecar — the authoritative review surface for vocabulary quality. Replaces the ad-hoc audit markdown previously kept under `audits/`.
- **Design-critique sidecar** (`data/design_critique.json`, new). Editable source of commentary (452 entries, one per pattern). Kept out of the hash input, so edits to commentary do not cascade into pattern sema_ids.
- **`scripts/generate_design_manual.py`** (new). Staging-aware generator — prefers `data/staging/<Handle>.json` over `data/vocabulary/<Handle>.json` when present, so the manual reflects in-progress edits without requiring an apply round-trip.
- **`scripts/migrate_design_commentary.py`** (new, one-shot). Consolidated the per-pattern audit markdown under `audits/2026-04-17/` into the sidecar. Idempotent on re-run (preserves hand-edited fields).
- **Env-var opt-outs**:
  - `SEMA_DISABLE_MINT=true` — hides the `sema_mint` MCP tool.
  - `SEMA_ALLOW_MINT=false` — legacy alias for `SEMA_DISABLE_MINT=true`; honored one deprecation cycle.

### Bug fix: `_meta.related` edges lost during apply

Two compounding bugs caused `RELATED_TO` edges to be under-populated. Before this release, the DB had 24-34 such edges for ~117 `_meta.related` refs in the vocabulary — only ~20-30% of soft-links showed up as graph edges. Effect on consumers: `sema resolve Foo` missed "related" siblings; graph-based exploration tools silently skipped the weakest but still-valid link class.

1. **Prefix-stripping wasn't applied.** `_meta.related` accepts both bare-handle (`"Foo"`) and full (`"sema:Foo#mh:SHA-256:..."`) refs. The edge-creation code used `item.split("#")[0]`, which for full refs yields `"sema:Foo"` — not a real handle. Fixed: use `extract_handle_from_ref(item)` to strip the `sema:` prefix before lookup.

2. **Topological-order race.** Patterns apply in topological order by **hard** dependencies (`accepts`, `composes_with`, etc.). `_meta.related` is a soft link and doesn't participate in the sort. When pattern A declares `related: [B]` but B is minted after A, A's edge-creation attempt finds no B in `_handle_to_id` and silently skips. Fixed: added `GraphStore.sweep_related_edges()` — a second-pass method that walks all patterns once the full DB is loaded and creates any missing `RELATED_TO` edges. `sema apply` now calls it automatically at the end of a batch; downstream code can call it explicitly when needed.

Post-fix: 105 `RELATED_TO` edges (up from 34), matching the 105 resolvable refs in the vocabulary. 12 refs remain unedged because they point to handles no longer present in the default shelf (e.g., experimental-shelf-only patterns like `ChaosDrift`, `GhostTrail`). Silent skip for those is correct — they're stale but flagged for a future cleanup pass.

Pattern sema_ids unaffected; `RELATED_TO` is metadata and not part of the hash input.

### Bug fix: CATEGORY node collapse across layers

`_add_or_update_pattern` in `graph_store.py` looked up `CATEGORY` nodes by text alone. When the foundation audit added Physics/Primitives patterns after Infrastructure/Primitives already existed, it matched the Infrastructure node (same text "Primitives") and bolted a second `IN_LAYER` edge onto it pointing at Physics — instead of creating a distinct Physics/Primitives node. The graph ended up with 12 CATEGORY nodes and 13 IN_LAYER edges: topology that can't represent "which-category-in-which-layer" unambiguously via edges alone (only via pattern-metadata lookup).

Fix: composite-key lookup — `(category_name, layer_id)` must both match. If a node with the right text exists but no `IN_LAYER` edge to the target layer, a new node is created. After a clean rebuild: 13 CATEGORY nodes, 13 IN_LAYER edges, each `(layer, category)` combo uniquely represented. Pattern `sema_id`s are unaffected (category/layer live in `_meta`, not hashed).

### Bug fix: hash canonicalization

`generate_sema_hash()` produced different hashes for three semantically-equivalent representations of "no dependencies": (a) missing `dependencies` key, (b) `dependencies: {}`, (c) `dependencies: {accepts: {}, yields: {}, composes_with: {}, references: {}}`. This hadn't surfaced before because all dep-less patterns in 0.1.27 used form (a); the audit introduced 4 new patterns (`Boolean`, `Conservation`, `Distance`, `Status`) authored in form (b), triggering `sema pull --verify` false-positives for ~291 patterns via hash cascade.

Fix: `generate_sema_hash` now strips empty dep sub-blocks and drops the `dependencies` key entirely when no real deps remain. All three representations now hash identically. The full library was re-hashed and re-applied; `--verify` passes cleanly on the new DB.

### Added

**Physics primitives** (8, minted under the structured-thinking criterion):
- `Gradient#480b` — directional rate of change of a scalar field
- `Equilibrium#f7c5` — dynamical system's stationary state
- `Conservation#d63a` — invariant quantity under closed-system transformation
- `Distance#3e1e` — metric-axiom function on a state space
- `PhaseTransition#edf8` — discontinuous reorganization at a threshold
- `Attractor#487f` — state-space region dynamics pull toward
- `MutualInformation#da31` — information-theoretic shared entropy
- `Measurement#5da6` — substrate act of extracting information

**Solver-family completion** (Mind/Strategy, Mind/Memory, Mind/Reasoning):
- `PolymorphicSolver#c28a` — five-surface contract (supersedes `CognitiveSolver`)
- `RootSolver#13e8` — apex triage node with Pathway Memory (supersedes `SolverRoot`)
- `ConceptualDecomposition#e06a` — contract-bound sub-concept decomposition
- `PathwayMemory#7899` — problem_class → route → outcome_quality
- `DecompositionGate#7fbd` — Necessity/Independence/Universality/Completeness
- `FrameError#579f` — typed failure signaling lateral reframing required

**Fractal Intelligence Table 4 gap** (Infrastructure/Data Structures, Society/Protocols, Society/Governance):
- `PerformanceSignal#6308` — Feedback-surface typed output
- `FailureTrace#f80b` — structured proof of AcceptSpec clause violation
- `ReceptivityGate#9f9c` — guards Feedback surface from poisoned rejection signals
- `DocumentedOverride#c0fb` — supervised hard-seam bypass, cryptographically logged

**FI §6 generalized protocols** (Mind):
- `CollaborativeWritingProtocol#7400`, `HumanEmulatorProtocol#307c`, `DiscoveryProtocol#2cd0`, `TemporalEnsembleForecasting#9e5f`, `EthicalReasoningProtocol#0287`, `TruthseekingProtocol#cf2b`, `MetaProtocols#27dc`

**Other additions**:
- `PURE#87ea` (Mind/Strategy) — viability framework parent
- `GraphOfThought#226a` (Mind/Reasoning) — `Think(DAG)` sibling
- `Forest#5eda` (Infrastructure/Data Structures) — N independently-rooted trees
- `Boolean#2e6b` (Infrastructure/Data Structures) — binary truth value
- `Status#1cf9` (Infrastructure/Data Structures) — verified/falsified/unknown
- `ReAttempt#bd00` (Infrastructure/Primitives) — substrate-level re-try

### Renamed (old handles redirect via `_meta.supersedes`)

- `CognitiveSolver` → `PolymorphicSolver#c28a`
- `SolverRoot` → `RootSolver#13e8`
- `AbductiveLeap` → `Abduction`
- `Linear` → `Chain`
- `Switch` → `Route`

### Relocated (71 patterns; mechanism-sufficiency test applied)

Layer metadata is not hashed, so layer changes do not by themselves change pattern identity — but mechanism rewrites paired with relocation do change hashes. Rule G (hard dependencies flow higher→lower) is now enforced as a `sema apply` gate.

**Society → Mind (30)** — mechanism is single-agent cognition, not multi-party:
CapacityPressure, CiteBack, CognitiveEcho, CommitmentDevice, Compose, ConstraintFirst, ConstructOntology, CurriculumReplay, DeepResearch, DogfoodFirst, EmpathySim, Expansive, Fermi, FractalIntelligence, HackDetect, LivedProof, LocalizedLearning, ManifestPlanning, MarginalValueRule, MetaPrompt, ProblemFramer, Proprioception, Realizable, RequestFraming, SimulationTrace, SourceEvaluate, ThinSlice, TimeboxThink, TraceBelief, WorldReversible.

**Society → Infrastructure (15)** — data structures / mechanical operations, not multi-party mechanisms:
AcceptSpec, Aesthetics, ExecutionManifest, FailClosed, FeedbackSignal, FrameSpec, IdempotentWrite, MonitorReport, ProtoPack, RolloutManifest, SolverManifest, StateSnapshot, StyleSpec, TriGate, Warmup.

**Physics → Infrastructure (14)** — authored foundational primitives, not substrate:
Branch, Compensate, Compress, Cooldown, Cyclic, EntropyPump, Gate, Heartbeat, Hysteresis, Parallel, Route, Sign, StateAudit, Throttle.

**Mind → Infrastructure (6)** — mechanical, no judgment required:
Cache, Compare, Decision, Monitor, Rank, Tension.

**Physics → Mind (2)** — mechanism requires cognition:
Retry, Uncertain.

**Infrastructure → Mind (1)** — requires judgment, not schema-matching:
Critique.

**Physics → Society (1)** — structurally requires counterparty:
StateLock.

**Mind → Society (1)** — structurally requires multiple parties:
Stigmergy.

**Society → Physics (1)** — substrate property:
Reversibility.

### Mechanism rewrites (71 patterns)

Rewritten during refinement for reasons including: invariant/mechanism contradiction (e.g., `EntropyPump` had invariants describing a disambiguation pattern rather than an entropy pump); forward-dependency removal; renamed dependency uptake (e.g., `Solver`/`PolymorphicSolver` updated for the five-surface contract with Consult instead of Question); Noun/Verb morphology cleanup; cycle breaks in the dependency DAG. Full list:

Abduction, AcceptSpec, Aggregate, AnalogyBridge, Anomaly, Audit, AuditTrail, BackwardChain, Ballot, Belief, Bid, Cache, Card, Causation, Chain, Check, ContextSwitch, Contract, Correlation, DriftWatch, Eliminate, EmpathySim, Expansive, FractalIntelligence, Gate, Generalize, HeldRelease, HeuristicSnap, Hypothesis, HypothesisLadder, IdempotentWrite, InvariantFilter, Judge, LatentWander, MechanisticDesignProposal, NormativeJudge, Novelty, OODA, OptimisticSolver, Optimize, OrchestrationLoop, OsmoticFilter, PUREBrainstorming, PURECheck, PUREOptimization, ParetoFront, Parsimony, PatternDiscovery, Plan, ProblemFramer, Prompt, Queue, Rally, Rank, Realizable, RealizationProtocol, RedTeam, RequestFraming, RetrievalAugment, RigorousSolver, ScoringFunction, Solver, SolverTree, Specialize, TaskLifecycle, TimeWarpLog, ToolDiscovery, Tree, UniversalSolverTree, Validate, WorkerMode.

### Retired / Moved to Experimental Shelf

- `Group` — ambiguous between Society coordination and general data structure; moved to experimental for refinement before re-inclusion in the default library.

### Additional structural fixes (50 patterns)

Post-audit surgical cleanup of internal defects found via systematic scans. None change pattern scope; they repair the pattern-as-specification. Verified: 58/58 structural checks pass.

- **Duplicate invariants / ambiguity (5)** — `ConfidenceCalibrate` (post-calibration disambiguation), `Throttle` (redundant rate-limit), `HypothesisLadder` (duplicate Falsifiability), `PreMortem` (two duplicate pairs), `UptakeAsGround` (operational + Wittgensteinian merge).
- **Duplicate failure modes (4)** — `OsmoticFilter`, `TieredAccess`, `Rally` (8→6), `Resonate` (9→6).
- **Failure-mode restructure (1)** — `DriftWatch` (mitigations folded into parent failures, 8→4).
- **Jammed failure modes split (3)** — `Proprioception`, `CapacityPressure`, `CounterfactualAnchor`.
- **Jammed preconditions/postconditions split (10)** — `BackwardChain`, `BayesUpdate`, `Compose`, `Decompose`, `Delegate`, `Mutex`, `OntologyHandshake`, `Quorum`, `Satisfice`, `Eliminate` (also promoted a miscategorized precondition to real invariants — `Monotonic Reduction`, `Evidence-Required Exclusion`).
- **Formatting / capitalization (5)** — `Backoff`, `Context`, `ExperienceSharding`, `Reframe`, `SemanticTabu`.
- **Broken fragment (1)** — `Warmup` (`"(e.g. cache)"` split across entries by a stray comma; reassembled).
- **Nested list header (1)** — `Mutex` (`"Failure modes: (1)..."` with numbered sub-items flattened to atomic entries).
- **Bare-label invariants promoted (2)** — `BoundedTask` (`Budget Enclosure` / `Quality Gate` now have statements), `ConceptAnchor` (redundant `Immutable Reference` removed).
- **FeedbackSignal invariants (1)** — bare adjectives `Targeted` / `Structured` made specific, tied to the data_schema.
- **Template leaks in gloss (2)** — `Crystallize` (`{{phase_transition}}` → plain text, orphan dep removed), `Decay` (`{{state}}` → plain text).
- **SacrificialProbe (1)** — semicolon-jammed failure modes split.
- **`_meta.related` refs to full format (6)** — `Entropy`, `Experiment`, `Falsification`, `RecursionDive` (also: `SolutionNode` → `SolverNode` rename followed), `Snapshot`, `Vector`.
- **`derived_from` fixes (10)** — `AdversarialProof` (bare handle → full sema_id), `BoundedTask` (stale), `ManifestPlanning` (legacy stub), `OptimisticSolver` (stale), `PolymorphicSolver` (stale), `RequestFraming` (legacy stub), `RigorousSolver` (all-zeros placeholder fixed), `RolloutWatch` (legacy stub), `FractalIntelligence` (`RecursiveIntelligence` retired — removed), `RealizationProtocol` (`CreationProtocol` retired — removed).

### Full supersedes chain (v0.1.18 + v0.1.27 predecessors)

`_meta.supersedes` is an **append-only chain** of prior public-release sema_ids, not a pointer to the most recent. Every pattern whose current sema_id differs from the sema_id it carried in a prior public release now lists that prior sema_id. `sema pull` iterates the chain, so a consumer pinned to any version in the chain gets their old handle cleaned up on upgrade — not just consumers on the most recent prior.

This release populates the chain against **two distinct published DB states**: v0.1.18 (the earliest 0.1.x tag with a non-trivial DB) and v0.1.27 (the last public release). The intermediate v0.1.23 tag contributed zero new entries — its sema_ids coincide with either v0.1.18 or v0.1.27 for every pattern (no pattern changed in both the 02:20→12:11 and 12:11→17:47 windows on 2026-04-16).

**Rename-aware population.** For the 5 rename/collapse successors, the chain must include the predecessor's entries too — not just the successor's same-handle history. Two cases:
- **Collapse** (`Abduction`, `Chain`, `Route`): successor handle existed in v0.1.18 and v0.1.27 as a separate pattern; its chain carries both the absorbed handle's old sema_id (`AbductiveLeap` / `Linear` / `Switch`) and its own same-handle old sema_id. For these three, the absorbed predecessor was stable across v0.1.18 → v0.1.27, so one absorbed-predecessor entry covers both tags.
- **Pure rename** (`PolymorphicSolver`, `RootSolver`): successor handle is new in 0.2.0; the chain carries both the v0.1.27 and the v0.1.18 sema_ids of the absorbed handle (`CognitiveSolver` / `SolverRoot`), which *did* change between those tags. Without the v0.1.18 entry, a consumer pinned to a v0.1.18 install would keep the old handle orphaned on pull.

**Chain-length distribution across 452 patterns:**
- **88 patterns** — no chain. 31 new in 0.2.0 + 57 bit-identical across all three tags.
- **263 patterns** — 1 entry. Changed once in the chain's history (either between v0.1.18 and v0.1.27, or between v0.1.27 and current).
- **101 patterns** — 2 entries. Changed in both windows, or one of the 5 rename-aware cases.
- Max chain length: 2.

**Verified via round-trip pull test.** Point a copy of the v0.1.18 taxonomy.db at the current DB and run `sema pull`: 5 superseded-removed (all 5 rename-source handles cleaned up), 1 upstream-removed (`Group` — intentionally moved to the experimental shelf), 0 orphans. Same test from v0.1.27: identical result.

`_meta.supersedes` is excluded from `SEMANTIC_FIELDS` in `src/sema/core/hashing.py`, so populating the chain — including retroactively adding older predecessors — does not cascade new hashes through the DAG.

### Hash cascades

Because dependency references carry target hashes, any change to a referenced pattern propagates through the Merkle DAG. In total **399 of 452 pattern files differ from v0.1.27** on this release: 31 additions, 5 rename records, 71 layer moves, 71 mechanism rewrites, 50 additional structural fixes, 3 new `derived_from` wirings, and downstream dependents whose hashes changed because their referenced patterns did. 53 patterns are bit-identical to v0.1.27 (fast-path on pull). Consumers running `sema pull` will see their pinned hashes update; the handshake remains valid because the redirect/supersession metadata is preserved.

### Governance

- `docs/core/philosophy.md §3.1` rewritten: the **mechanism-sufficiency test** is now the governing rule for layer placement. *What does the mechanism structurally require to execute? Substrate → Physics. Authored structure, no cognition → Infrastructure. Cognition, single-agent sufficient → Mind. ≥2 independent parties → Society.*
- **Two-criteria minting rule** is now explicit: a concept earns a pattern if it meets either *protocol consistency* (shared semantics required across agents) or *structured thinking* (invariant-bearing specification sharpens a loose concept). English suffices when neither is met.
- **Broad-use test** added: a pattern's mechanism must capture only what every legitimate deployment context needs; context-specific variation belongs in descendants via `derived_from`.
- **Rule G** (layer direction) is now enforced as a compile-time `sema apply` gate; zero current patterns violate the rule.

### Compatibility

- **Full-library supersedes coverage.** All 5 renames plus all 358 content-edited patterns carry their v0.1.27 sema_id in `_meta.supersedes`. A consumer on v0.1.27 running `sema pull` gets pinned hashes mapped forward cleanly for every pattern that changed. One orphan (`Group`) is retained locally as a user pattern because the release moved it to the experimental shelf.
- `derived_from` lineage now wires canonical parent→descendant pairs: `Lock#051c → Mutex#f52f` (K=1 specialization), `Task#b328 → BoundedTask#eaf4` (budget-carrying), plus 1 other.
- 15 template-reference migrations wire the 8 new Physics primitives into existing patterns (Budget, ChunkMerge, Mutex, Nucleate, OntologyAdapt, FractalIntelligence, ConceptBlend, DriftWatch, Optimize, SurprisalUpdate, Judge, MemeticSeed, Crystallize, EntropyPump, and others).
- Distribution split: higher-risk patterns (`AmendLaws`, `ChaosDrift`, `CryptoShred`, `IdentityMask`, `MirrorStake`, others) live on the experimental shelf. Default install stays conservative; engaging the experimental shelf requires explicit opt-in.

---

*Pre-0.2.0 vocabulary changes are in git history; this file begins with the foundation audit.*
