# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Dates are ISO 8601 (`YYYY-MM-DD`).

This file records vocabulary-level changes between versions — additions, renames, relocations, mechanism rewrites, retirements, and governance updates that a downstream consumer would want to know about when running `sema pull` — as well as tooling changes that affect how consumers interact with the protocol (CLI flags, MCP tool changes, behavioral defaults).

---

## [Unreleased]

### Added

- Canonical `scripts/verify_vocabulary_change.py` workflow for contributors and
  CI. It refreshes or non-destructively checks the design manual, audit,
  vocabulary root, documentation hash references, database/export parity,
  exported hashes, clean staging, and deterministic reconstruction in one
  command.
- `ExponentialBackoff`, a concrete child for capped geometric delay growth
  with configurable jitter. Retry eligibility, budgets, and reset policy remain
  caller-owned rather than requirements of the delay strategy.
- Lean 4 formal-verification pilot for the handshake decision kernel and
  canonicalization type-tag domain separation. Proofs are pinned to Lean
  4.30.0, checked without `sorry`, independently rechecked by `leanchecker`,
  and enforced by blocking CI.
- Machine-readable `verification/proof-manifest.json` linking theorem names to
  production implementations, conformance tests, and explicit assumptions.
- `sema_handshake(..., strict=true)` mode. Only the full 64-character hash can
  produce `PROCEED`; a matching truncated stub returns `REQUIRE_FULL_HASH`.

### Changed

- `Backoff` now defines the general failure-responsive delay family instead of
  requiring exponential growth, jitter, reset-on-success, and a retry budget.
  `Retry` explicitly selects `ExponentialBackoff` for transient failures,
  `StateLock` composes with the generic policy family, and `Yield` no longer
  links technical retry delay to negotiation concession.
  The vocabulary now contains 453 patterns and its root changes from
  `b7c42bc564f5a8d2ac3cb6140430e9d98feb82a8f9b943f550f554e9ba6360b5`
  to `901130d88dab244cc0d4afc149c5e6eeb9c9565e117c468a8e5326287be8fefa`.
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

### Fixed

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
