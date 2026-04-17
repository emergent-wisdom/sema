# Changelog

This file records vocabulary-level changes between versions — additions, renames, relocations, mechanism rewrites, retirements, and governance updates that a downstream consumer would want to know about when running `sema pull`.

Code-only changes (CLI flags, MCP tool signatures, internal refactors) live in the git history rather than here.

Format draws loosely on [Keep a Changelog](https://keepachangelog.com/) and on game patch notes: grouped and scannable rather than prose.

---

## [Unreleased] — 0.1.28 — Foundation Audit (2026-04-17)

A cross-pattern refinement pass (dual-LLM proposal/review — Claude Opus 4.7 + Gemini 3.1 Deep Think, adjudicated by the author) tightened the governing rules and applied them to the entire library. Pattern hashes on renamed/relocated/rewritten items update as usual; retired handles carry `_meta.supersedes` so `sema pull` redirects automatically.

**Vocabulary root:** `sema:vocab#mh:SHA-256:747a1eaf...`
**Pattern count:** 452 (default) + experimental shelf.
**Scope of changes:** 31 new patterns, 5 renames, 1 moved to experimental, 71 layer relocations, 71 mechanism rewrites, 3 new `derived_from` wirings, plus hash cascades through the dependency DAG (349 pattern files modified in total).

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

### Hash cascades

Because dependency references carry target hashes, any change to a referenced pattern propagates through the Merkle DAG. In total **349 pattern files were modified** on this release: the 31 additions, 5 rename records, 71 layer moves, 71 mechanism rewrites, 3 new `derived_from` wirings, and downstream dependents whose hashes changed because their referenced patterns did. Consumers running `sema pull` will see most of their pinned hashes update; the handshake remains valid because the redirect/supersession metadata is preserved.

### Governance

- `docs/core/philosophy.md §3.1` rewritten: the **mechanism-sufficiency test** is now the governing rule for layer placement. *What does the mechanism structurally require to execute? Substrate → Physics. Authored structure, no cognition → Infrastructure. Cognition, single-agent sufficient → Mind. ≥2 independent parties → Society.*
- **Two-criteria minting rule** is now explicit: a concept earns a pattern if it meets either *protocol consistency* (shared semantics required across agents) or *structured thinking* (invariant-bearing specification sharpens a loose concept). English suffices when neither is met.
- **Broad-use test** added: a pattern's mechanism must capture only what every legitimate deployment context needs; context-specific variation belongs in descendants via `derived_from`.
- **Rule G** (layer direction) is now enforced as a compile-time `sema apply` gate; zero current patterns violate the rule.

### Compatibility

- All renames preserve old handles via `_meta.supersedes`. `sema pull` redirects automatically.
- `derived_from` lineage now wires canonical parent→descendant pairs: `Lock#051c → Mutex#f52f` (K=1 specialization), `Task#b328 → BoundedTask#eaf4` (budget-carrying), plus 1 other.
- 15 template-reference migrations wire the 8 new Physics primitives into existing patterns (Budget, ChunkMerge, Mutex, Nucleate, OntologyAdapt, FractalIntelligence, ConceptBlend, DriftWatch, Optimize, SurprisalUpdate, Judge, MemeticSeed, Crystallize, EntropyPump, and others).
- Distribution split: higher-risk patterns (`AmendLaws`, `ChaosDrift`, `CryptoShred`, `IdentityMask`, `MirrorStake`, others) live on the experimental shelf. Default install stays conservative; engaging the experimental shelf requires explicit opt-in.

---

*Pre-0.1.28 vocabulary changes are in git history; this file begins with the foundation audit.*
