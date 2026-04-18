# Changelog

This file records vocabulary-level changes between versions — additions, renames, relocations, mechanism rewrites, retirements, and governance updates that a downstream consumer would want to know about when running `sema pull`. It also records tooling changes that affect how consumers interact with the protocol (CLI flags, MCP tool changes, behavioral defaults).

Format draws loosely on [Keep a Changelog](https://keepachangelog.com/) and on game patch notes: grouped and scannable rather than prose.

---

## [Unreleased] — 0.1.28 — Foundation Audit + Pull Loop (2026-04-17)

Two coherent threads shipped in this release:

1. **Foundation audit** — a cross-pattern refinement pass (dual-LLM proposal/review: Claude Opus 4.7 + Gemini 3.1 Deep Think, adjudicated by the author) tightened the governing rules and applied them to the entire library.
2. **Pull loop closure** — `sema pull` now reads `_meta.supersedes` and redirects retired handles to their replacements by default (opt-out via `--preserve-superseded`); a new `sema_pull` MCP tool exposes the same behavior to agents; `sema_mint` flipped from opt-in to opt-out.

**Vocabulary root:** `sema:vocab#mh:SHA-256:39ca671a4dcb3075855cb293380d1796105e2eca0de49b0537279b798b675ee6`
**Pattern count:** 452 (default) + experimental shelf.
**Scope of changes:** 31 new patterns, 5 renames, 1 moved to experimental, 71 layer relocations, 71 mechanism rewrites, 50 additional structural fixes (dedup / split / broken-ref cleanup), 3 new `derived_from` wirings, full supersedes population against the live users' db (360 patterns), plus hash cascades through the dependency DAG (399 pattern files differ from v0.1.27 in total — 31 new + 368 updated).

### Breaking changes for consumers

- **Old renamed handles are removed on `sema pull`.** The default behavior reads upstream `_meta.supersedes` and removes the local copy of any superseded pattern. Use `sema pull --preserve-superseded` (CLI) or `sema_pull({preserve_superseded: true})` (MCP) to keep both the old and new handles. The pre-pull snapshot is still retained — `sema pull --undo` restores everything.
- **`sema_mint` is now exposed by default in the MCP server.** Previously required `SEMA_ALLOW_MINT=true`. Deployments that want to keep mint disabled must now set `SEMA_DISABLE_MINT=true` (or leave the legacy `SEMA_ALLOW_MINT=false` in place — honored for one deprecation cycle).
- **Pattern hashes shifted widely.** The foundation audit rewrote 71 mechanisms and relocated 71 patterns; canonicalization (see below) changed hashes for 4 new patterns plus their dependents. Consumers who pinned specific hashes will see `sema pull` update them automatically via the supersedes chain. Code that references handles (not full hashes) is unaffected.

### Migration guide (from 0.1.27)

For a consumer running 0.1.27 who pulls to 0.1.28, the expected transcript is:

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

### Tooling (new in 0.1.28)

- **`sema_pull` MCP tool** (new). Lets Claude / MCP-compatible agents pull upstream vocabulary without falling back to `Bash("sema pull")`. Structured JSON output: `added`, `updated`, `superseded_removed`, `superseded_kept_orphan`, `upstream_removed`, `cascaded_user`, `vocabulary_root_before`, `vocabulary_root_after`.
- **`sema pull --preserve-superseded`** (new CLI flag). Keeps locally superseded patterns alongside their upstream replacements instead of cleaning them up.
- **Orphan guard on supersession cleanup.** If a user-only local pattern still depends on a superseded one (via `sema_id` reference), pull keeps the superseded pattern in place and reports `superseded_kept_orphan`. Fix the dependent and re-run to complete the cleanup.
- **Design manual** (`docs/manuals/vocabulary-design.md`, new). Per-pattern design commentary rendered from a sidecar — the authoritative review surface for vocabulary quality. Replaces the ad-hoc audit markdown previously kept under `audits/`.
- **Design-critique sidecar** (`data/design_critique.json`, new). Editable source of commentary (452 entries, one per pattern). Kept out of the hash input, so edits to commentary do not cascade into pattern sema_ids.
- **`scripts/generate_design_manual.py`** (new). Staging-aware generator — prefers `data/staging/<Handle>.json` over `data/vocabulary/<Handle>.json` when present, so the manual reflects in-progress edits without requiring an apply round-trip.
- **`scripts/migrate_design_commentary.py`** (new, one-shot). Consolidated the per-pattern audit markdown under `audits/2026-04-17/` into the sidecar. Idempotent on re-run (preserves hand-edited fields).
- **Env-var opt-outs**:
  - `SEMA_DISABLE_PULL=true` — hides the `sema_pull` MCP tool (for deployments pinning a fixed vocabulary).
  - `SEMA_DISABLE_MINT=true` — hides the `sema_mint` MCP tool.
  - `SEMA_ALLOW_MINT=false` — legacy alias for `SEMA_DISABLE_MINT=true`; honored one deprecation cycle.

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

### Full supersedes population (360 patterns)

Beyond the 5 rename supersessions above, every pattern whose current sema_id differs from the sema_id in the live users' db (the pip-installed `taxonomy.db`, reflecting the last public release) now carries the old sema_id in `_meta.supersedes`. This gives `sema pull` a clean upgrade path for every pattern that changed between releases, not just the renames.

Breakdown of the 452-pattern library:
- **358 patterns** — content edited since v0.1.27; now carry the v0.1.27 sema_id in `_meta.supersedes`.
- **2 patterns** — rename-only inheritors (`PolymorphicSolver`, `RootSolver`) retain their pre-existing rename supersedes (`CognitiveSolver`, `SolverRoot`); no additional entry needed since these handles didn't exist under these names in v0.1.27.
- **63 patterns** — unchanged since v0.1.27 (sema_id matches live exactly); no supersede entry needed.
- **31 patterns** — new since v0.1.27 (not in the live db); no supersede needed.

`_meta.supersedes` is not hashed (excluded from `SEMANTIC_FIELDS` in `src/sema/core/hashing.py`), so adding these entries did not change any pattern's sema_id.

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

*Pre-0.1.28 vocabulary changes are in git history; this file begins with the foundation audit.*
