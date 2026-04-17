# Foundation audit — 2026-04-17

**Target:** `data/taxonomy.db` — the bundled canonical vocabulary, 427 patterns across 4 layers and 23 categories.

**Intent:** keep the sema library as scalable as possible as it grows. Every pattern here is a load-bearing primitive that other patterns will compose, reference, or inherit from. Ambiguity or incoherence at this level compounds as the library expands — small gaps at the foundation become large gaps at the edges. This audit identifies the places where that compounding would hurt the most, and proposes the fixes we believe make the library easier to build on.

The automated linter (all 42 rules in `docs/specification/validation-matrix.md`) runs clean. The audit below is in the territory no rule catches: semantic coherence, layer fit, orthogonality, and wiring integrity.

---

## 1. The lens we applied

The question we asked of every pattern was not "is this complete?" but **"is this easy to build on?"**

Completeness and scalability are different goals. An over-specified primitive is harder to inherit from — every descendant has to honor details that should have been left to the descendant to decide. So we were careful not to flag thinness as a problem.

### What we treated as damage

1. **Coherence failures** — a pattern's mechanism, invariants, and parameters contradicting each other
2. **Layer misplacement** — a pattern sitting in a layer lower than its mechanism requires, forcing every user to reach across layers
3. **Redundancy without hierarchy** — two patterns occupying overlapping territory with no declared relationship, so callers can't tell which to extend
4. **Vacuous boundaries** — mechanisms so abstract the pattern constrains nothing
5. **Dangling self-claims** — a pattern's mechanism naming relationships that its dependencies don't reflect
6. **Orphan anchors** — well-formed concepts that nothing else in the library uses
7. **Lazy placeholders** — `range: "unspecified"` on parameters that are part of the identity hash

### What we explicitly did not flag

- Bedrock noun primitives (`Datum`, `State`, `Value`, `System`) with no invariants or failure modes — they are meant to *be* the thing; callers specify failure cases
- Short mechanisms and short glosses on fundamental concepts — concise is the goal at this level
- Ring 2 (userland) patterns with zero incoming references — tactical patterns are leaves by design
- Tier-0 primitives with sparse invariants — minimum surface is correct

Earlier drafts of this audit flagged, for example, "`State` has 54 incoming references but zero failure modes." We retracted that. State is a noun; its users own their state-specific failures. Pushing completeness into foundational primitives is over-specification, and over-specification slows the library down.

---

## 2. Scope

| Layer | Patterns | Categories (count) |
|---|---|---|
| Physics | 27 | Primitives (17), Time (10) |
| Infrastructure | 112 | Data Structures (80), Primitives (23), Verification (9) |
| Mind | 139 | Strategy (66), Reasoning (44), Inference (18), Memory (11) |
| Society | 149 | Protocols (114), Governance (17), Economics (17), Coordination (1) |

Method — two phases:

*Phase 1 (axis-exhaustive, §3.1–§3.17)*: every pattern checked against specific structural signals via scripted queries — unspecified parameter ranges, duplicate invariants, orphan-by-reference-count, handle-similarity clusters, phantom signatures, Ring-0 over-claims, Rule-G near-violations, forward-dep drift masked by English rather than template syntax. Each hit was then read by hand.
- Full deep read where the category was small enough to afford it: Physics (27), Infrastructure/Verification (9), Infrastructure/Primitives (23), Mind/Memory (11), Mind/Inference (18), Society/Governance (17), Society/Economics (17), Society/Coordination (1).
- Systemic scan plus targeted reads on the larger categories: Infrastructure/Data Structures (80), Mind/Strategy (66), Mind/Reasoning (44), Society/Protocols (114).
- Programmatic verification of all 42 spec rules.

*Phase 2 (manual sweep, §3.18)*: the 243 patterns the axis queries did not explicitly touch were read individually for content-quality issues no axis query could detect — mechanism-restates-gloss, marketing-speak glosses, layer labels that drifted from mechanism content, handles that are really dimensional tags rather than standalone concepts. This pass surfaced findings (Society/Protocols bloat, topology category split, Linear/Chain redundancy, Deep/Nature canonical status) that Phase 1 could not reach.

---

## 3. Findings and the changes we're making

Every change below re-mints the affected pattern and cascades through the Merkle DAG. The new vocabulary root after applying all changes in this audit will therefore be different, and `sema pull` consumers will see the update. This is expected.

### 3.1 Coherence — five patterns contradict themselves

**`EntropyPump`** (Physics/Primitives, Ring 1, Tier 2). The mechanism says the pattern injects entropy and noise to escape convergence. The invariants say "Ambiguity must decrease over time" and "Conflicts cannot persist indefinitely." Those describe the opposite behavior — they belong on a disambiguation pattern, not on a pump that adds entropy. Anyone composing EntropyPump and reading its invariants would infer a guarantee the mechanism cannot provide. We replace the invariants with ones that actually hold for an entropy pump: bounded injection (noise magnitude capped so it doesn't destabilize equilibria) and targeted scope (applied to stuck states, not stable ones).

**`Budget`** (Infrastructure/Primitives, Ring 0, Tier 1). The invariant "Remaining budget cannot be < 0" is false for overdraft, deficit, and over-commitment semantics, all of which are common in real systems. A descendant that models a budget which *can* go negative inherits a constraint its authors never intended. We drop the non-negative invariant (descendants that want strict non-negativity can introduce a `StrictBudget` subtype) and replace it with monotonic allocation: total never decreases without an explicit refund event. Conservation stays.

**`TimeWarpLog`** (Infrastructure/Primitives, Ring 0, Tier 1). Two of the three invariants are the same statement: "Immutability: Past entries cannot be modified" and "Log immutable after write." We drop the duplicate and replace it with the invariant the mechanism actually guarantees: causal consistency — events are accepted only if they don't contradict the current causal cone.

**`Judge`** (Infrastructure/Primitives, Ring 0, Tier 1). The parameter `criteria` has `range: "unspecified"`, but criteria is what defines what Judge is judging against — the core input. Parameters affect the identity hash, so `criteria` being a parameter also means every Judge with different criteria is a different Judge; that multiplies patterns without cause. We move `criteria` out of `parameters` and into `accepts` in the dependency map. Criteria becomes an input at call time, not a configuration of the pattern's identity. Threshold stays as a parameter.

**`ConfirmationBlock`** (Mind/Inference, Ring 0, Tier 2). The mechanism is an active search for *disconfirming* evidence ("What evidence would prove me WRONG?"). The parameters are named `confirmations_required` — literally the opposite. We rename to `disconfirmations_required` and update the description to match the mechanism.

### 3.2 Layer — two patterns sit below the layer their mechanism requires

The civilization stack (`docs/core/philosophy.md` §3) is: Infrastructure (kernel) → Physics (substrate/state/time) → Mind (cognition) → Society (coordination). Hard dependencies (accepts, composes_with) must flow upward — or equivalently, named patterns must live at the layer their mechanism describes.

**`Uncertain`** is in Physics/Primitives. Its gloss is "Epistemic status: genuinely don't know." Epistemic state is cognition, not substrate. Every Mind pattern about belief, confidence, or knowledge that wants to say "I don't know" either has to cross layers downward or re-invent the concept locally. We move `Uncertain` to Mind/Reasoning.

**`Retry`** is in Physics/Primitives. Its mechanism is strategic reasoning: classify the failure, consult failure history, compute adaptive backoff, check retry budget, decide whether conditions have changed enough to retry. That is Mind-tier logic, not Physics substrate. We move it to Mind/Strategy.

Physics gets a small replacement `ReAttempt` primitive that covers the substrate-level concept — "try the same thing again after a delay" — leaving Retry as the Mind strategy that composes classification, backoff, and budget checking around it.

### 3.3 Redundancy — three clusters without clear hierarchy

**Lock and Mutex** both live in Physics/Primitives and both claim to provide mutual exclusion. Neither references the other. A descendant needing mutex has no canonical extension target. We connect Mutex to Lock via **`derived_from`** — Lock becomes the abstract mutual-exclusion primitive; Mutex becomes the evolutionary specialization that adds token-possession and fencing semantics. `derived_from` is the correct field for phylogeny/inheritance per `docs/specification/schema.md` §1; `composes_with` is reserved for active subroutine invocation (Verbs), which isn't what's happening here — Mutex isn't *calling* Lock, it's a Lock of a specific shape.

**Branch, Route, and Switch** all live in Physics/Primitives as flow-control primitives. Their mechanisms are:
- Branch: binary `if C then A else B`
- Route: N-way classify-and-dispatch
- Switch: "Changing the active mode, context, or flow path"

Switch's mechanism is so general it covers what Branch and Route do. An earlier draft proposed tightening Switch to "stateful mode toggle (N-way, state-driven)" to give the three a clean partition. On further review we retire Switch entirely (see §3.9) — a handle with a years-long history of vacuous usage cannot be reclaimed for a narrower meaning without confusing every existing composer. The clean partition becomes just Branch (binary) + Route (N-way, input-driven). If a stateful-mode-toggle primitive turns out to be needed, it should be minted under a new handle (`ModeMachine` proposed in §3.9) rather than by reusing `Switch`.

**Abduction and AbductiveLeap** are both in Mind/Reasoning at Tier 1 Ring 1. Abduction's mechanism is a one-sentence stub; AbductiveLeap is a full ranking mechanism. Their glosses differ by the word "the". We collapse AbductiveLeap into Abduction, preserving the richer mechanism. AbductiveLeap is superseded (an entry is added to `_meta.supersedes` on the consolidated Abduction pointing at AbductiveLeap's old sema_id), which is the documented versioning mechanism (`docs/specification/versioning.md`).

### 3.4 Vacuous boundaries — thirteen glosses and one mechanism

Glosses in sema are embedding anchors for vector search (`docs/specification/schema.md` §5). They should be dense semantic fingerprints. Thirteen of them currently read as marketing copy describing benefits rather than describing what the pattern *is* — or as confusing-pair glosses that fail to distinguish two related patterns. Rewrites:

| Pattern | Before | After |
|---|---|---|
| Compensate | Enable clean failure recovery through structured rollback, preventing orphaned resources and corrupted state | Structured rollback via logged inverses in LIFO order |
| Retry | Transform retry from blind re-attempt to intelligent, failure-informed recovery strategy | Classified re-attempt with backoff conditioned on failure type |
| Bubble | Enable risk-free coordination experimentation through transactional isolation—try before committing to reality | Sandboxed coordination trial with rollback on commit refusal |
| CognitiveSolver | The universal polymorphic atom of recursive intelligence | Solver implementing the five-surface contract: manifest, execute, consult, verify, feedback (handle later renamed to `PolymorphicSolver` per §3.21) |
| Canary | Transform path selection from 'hope it works' to 'tested it works' without risking real resources | Expendable agent tests the full coordination path before real commit |
| Elect | Enable efficient group coordination through configurable leadership with clear authority boundaries and succession planning | Leader nomination → vote → succession with term and authority bounds |
| Yield | Enable fair resolution of genuine disagreements without defaulting to power dynamics or eternal deadlock | Weighted negotiation backoff with deferred debt ledger |
| Delegate | Enable structured work distribution with accountability | Work handoff: delegate → accept/refuse → heartbeat → result-or-failure |
| Disband | Enable clean group termination with proper state handling | Graceful group dissolution with state disposition and resource release |
| ConceptBlend | Combinatorial novelty generation | Atomic fusion of two unrelated concepts into a novel third |
| CreativeBlend | Generating novelty via combinatorial blending and noise | Full creative pipeline: ConceptBlend + NoiseInjection with novelty/value gates |
| SteelmanCheck | Mandatory counter-argument generation | Post-decision adversarial check: revise if counter-argument exceeds validity threshold |
| SteelmanFirst | Construct strongest counter-argument before proposing | Ordering rule: steelman opposing view *before* proposing, so SteelmanCheck has real targets |

One mechanism-level vacuity: **`Switch`** ("Changing the active mode, context, or flow path") is addressed by retirement in §3.9.

The "Before" column for `CognitiveSolver` above reads "The universal polymorphic atom of recursive intelligence." The concept is named **fractal intelligence** in the Fractal Intelligence paper v3 — "recursive intelligence" is drift from earlier terminology. The rewrite removes the phrase entirely, so the naming drift resolves as a side-effect of the gloss tightening rather than as a separate rename. (The handle `CognitiveSolver` itself is later retired in §3.21 in favor of `PolymorphicSolver`, since the pattern spans substrates broader than cognition.)

### 3.5 Wiring — one dangling claim, one canon gap

**`ScoringFunction`**'s mechanism says it "encapsulates the criteria used by `{{rank}}` and `{{judge}}`." Neither Rank nor Judge currently declares ScoringFunction as a dependency. The mechanism is asserting a relationship the graph doesn't reflect. We update Rank and Judge to **`accepts`** ScoringFunction — not `composes_with` — because ScoringFunction is categorized as Infrastructure/Data Structures, making it a Noun. Per Rule B in `docs/specification/validation.md`, Nouns are read via `accepts` (Read Access); `composes_with` is strictly for active tools (Execute Access). Rank and Judge take a ScoringFunction as input and read its encoded logic to score their inputs — that's read access, not delegation. Both mechanisms are updated to reference `{{scoring_function}}` explicitly.

**Classical reasoning canon.** `Deduction`, `Induction`, and `Abduction` are named patterns in Mind/Reasoning at Ring 1 (standard library). All three have zero incoming references. Meanwhile the reasoning patterns that most directly descend from them declare nothing:

| Pattern | Gloss | References |
|---|---|---|
| Generalize | Inductive pattern extraction | none |
| Specialize | Deductive application of principles | none |
| Eliminate | Sherlock Holmes deduction via falsification | none |
| BackwardChain | Goal-driven reasoning from target to preconditions | none |

We wire them up: Generalize `references` Induction; Specialize `references` Deduction; Eliminate `references` both Deduction and Falsification; BackwardChain `references` Deduction. These are `references` (soft citations) rather than `composes_with` (active tools) — we are not claiming the derived patterns *invoke* the classical modes, only that they inherit the lineage. But the lineage becomes findable through the graph.

### 3.6 Orphan anchors — triage of three

**`Risk`** (Infrastructure/Data Structures) is a well-specified pattern with three invariants, four failure modes, and a four-component mechanism, but nothing in the library references it. Plan, MechanisticDesignProposal, and TaskLifecycle all deal with risk in their mechanism text without declaring the dependency. We wire Risk into these three as a `references` dependency and update the mechanism text to include `{{risk}}`.

**`DAG`** (Infrastructure/Data Structures) is a fundamental acyclic-graph topology with no callers. Tree, Chain, and TaskLifecycle conceptually depend on acyclicity but each describes it locally. We make Tree, Chain, and Plan `reference` DAG. Again, not `composes_with` — the topology is structural, not active.

**`Group`** (Infrastructure/Data Structures) has zero callers and is very thin ("Agent collective"). It doesn't add vocabulary that isn't covered by `Agent` and the Society-layer coordination patterns. We remove it. Any pattern that needs to describe a collective of agents can either reference Agent or — if the collective is semantically significant at the level of a coordination primitive — use or introduce a pattern in Society that captures it specifically.

**`ScoringFunction`** is covered under §3.5; the orphan-ness is resolved by the same wiring fix.

### 3.7 Ring assignments — twenty-eight patterns re-ringed from 0 to 2

The ring system (`docs/core/philosophy.md` §4) distinguishes kernel primitives (Ring 0, immutable, hard-fork to change), standard library (Ring 1, stable, evolves over years), and userland tactics (Ring 2, fluid, evolves with model capability). A Ring-0 pattern with zero incoming references is usually a sign the pattern is tactical rather than kernel.

We re-ring the following from 0 to 2:

- **Mind (10):** HindsightBlock, NormCheck, SemanticTabu, AntifragileInversion, EventReact, Reflex, SunkCostIgnore, BreadthGovernor, ScopeFreeze, SelfReminder
- **Society (18):** ConfusedDeputy, HackDetect, ExpiringToken, DataMinimization, DeliberativeAlign, EbbFlowSync, GlacialVault, LatticeCommit, OsmoticFilter, PromiseGraph, ProtoPack, QuorumPulse, ReversibilityCheck, SynergisticMode, ThreeLevelCollision, WorkerMode, WorldTransparent, Gardener

A handful of Ring-0 patterns with zero current callers remain at Ring 0 because their content *is* kernel-level and the fix is to wire them up, not to demote them:

- **`Cache`** (Mind/Memory, Ring 0) — fundamental memoization primitive; we add `references Cache` to memoization-using patterns (HeuristicSnap, RetrievalAugment, among others)
- **`LatentAttachment`** (Mind/Memory, Ring 0) — kernel-level embedding attachment; similar wiring pass
- **`ContextFirst`** (Mind/Inference, Ring 0) — kernel-level read-before-write invariant; wide wiring pass
- **`CommitmentDevice`**, **`MonotonicCounter`**, **`AnchorDrop`** (Society, Ring 0) — kept at Ring 0; wired into the specific patterns that use them

### 3.8 Taxonomy — Society/Coordination rebalanced

Society is the layer for multi-agent coordination. Its category distribution is currently: Protocols 114, Governance 17, Economics 17, Coordination 1. Having one pattern in a category called Coordination at this layer, when many patterns in sibling categories clearly *are* coordination, makes it hard to know where to file new patterns.

We move the following from their current category into Society/Coordination: Consensus, Rally, Delegate, Vote, LazyConsensus, OntologyHandshake, IdentityHandshake, Resonate, Compromise, Disband, Elect, ConsensusFinder. The ProblemFramer pattern already in Coordination stays.

The distinction between categories after this rebalance:
- **Coordination** — multi-agent primitives for reaching agreement, distributing work, or joining/leaving collectives
- **Protocols** — structured exchange patterns and verification artifacts (handshakes remain in Protocols only if they are the *mechanics* of a coordination act; the coordination *intent* lives in Coordination)
- **Governance** — authority, responsibility, immutable constraints on the collective (Role, Constitution, Responsibility, SolverTree, TriGate, UniversalSolverTree, RootSolver, WorldTransparent remain)
- **Economics** — value and incentive mechanisms

### 3.9 Removals — three patterns retired

A pattern earns its place in the foundation by carrying semantic content that descendants can compose, reference, or inherit from. A pattern that duplicates a neighbor, states nothing that constrains its descendants, or exists as a stub without distinct content is pulling weight from the namespace without paying for it. Three patterns fall into those categories.

**`Group`** (Infrastructure/Data Structures). Mechanism: "A defined collection of agents sharing a common context or goal." Zero incoming references, and no compositional territory that `Agent` combined with the coordination patterns (Consensus, Rally, Delegate, Vote, LazyConsensus) doesn't already cover. "Collective of agents" is a real concept, but naming it at the pattern level adds no constraint — every coordination primitive already implies a set of participants. We remove Group; patterns that need to describe a set of agents can reference Agent and whichever coordination primitive is relevant.

**`Switch`** (Physics/Primitives). Mechanism: "Changing the active mode, context, or flow path." This is unbounded — it covers what `Branch` and `Route` do and anything else a caller might interpret as "change something." A vacuous boundary at a Physics primitive propagates: descendants composing Switch each mean something different by it, and the concept of Switch as a shared vocabulary breaks down immediately. We remove Switch. If a sharp pattern for "stateful mode toggle among a finite enumerable set" turns out to be needed later, it should be introduced as a properly-scoped `ModeMachine` pattern — not by reusing the `Switch` handle for a narrower meaning, which would confuse everything currently composing the existing Switch.

**`AbductiveLeap`** (Mind/Reasoning). This is the formal removal side of the merge described in §3.3. Abduction absorbs AbductiveLeap's richer mechanism; AbductiveLeap's handle stops being minted. The content is preserved — only the duplicate handle is retired. AbductiveLeap's old `sema_id` is added to the consolidated Abduction's `_meta.supersedes`, so any pre-existing reference to AbductiveLeap resolves via the documented supersession chain (`docs/specification/versioning.md`).

Locally, §3.9's three retirements take the library from 427 to 424; combined with §3.14's six additions, §3.18's one additional retirement (Linear→Chain), and the apply-time addition of `Status` (surfaced when §3.13 declared `Check` yields `Status` with no such pattern existing), the final count is **430** (see §5). The gain isn't size reduction — it's namespace cleanliness. A vocabulary where every name carries distinct, constraining semantic content is easier to build on than one where some names are synonyms, others are too vague to constrain, and others name concepts already covered elsewhere.

### 3.10 Vacuous data_schemas on Nouns — three Data Structures tightened

Rule E in `docs/specification/validation.md` requires Data Structures patterns to have non-vacuous `data_schema` — at least one specific property. Three Data Structures currently have schemas too generic to carry identity: `Score`, `Summary`, `Probability`. Two agents can handshake successfully on the same `Score#hash` and then disagree entirely on what fields a Score object contains. That's a silent schema drift failure exactly of the kind Rule E was written to prevent.

We tighten the three:
- `Score`: require `value: number`, `normalized_range: [min, max]`, `metric_id: string`
- `Probability`: require `value: number [0,1]`, `confidence_interval: [lower, upper]` (optional)
- `Summary`: require `source_ref: sema_id`, `compression_ratio: number`, `preserves: string[]` (list of retained semantic hooks)

### 3.11 Noun/Verb category squatting — three patterns re-categorized

`Check`, `Observe`, and `ToolInvoke` are active Verbs (operations that do something), but all three are currently filed under Infrastructure/Data Structures (the Noun category). This miscategorization invites downstream developers to place them in `accepts` blocks (Read Access) when they should be in `composes_with` (Execute Access), which breaks runtime permission logic and dependency-graph semantics.

We move the three to Infrastructure/Primitives, the correct category for Verbs at that layer. Their `data_schema` (currently minimal or absent) is dropped — Primitives don't define a data schema, they define a mechanism.

**A fourth pattern, `Critique`, surfaces in the broad-use analysis** (`2026-04-broad-use-analysis.md` §134). It's categorized Infrastructure/Data Structures but its mechanism reads "Analyzes a target datum against specific criteria and generates a structured assessment" — Verb semantics. Same treatment: move to Infrastructure/Primitives, drop its data_schema.

### 3.12 Signatures without fulfillment — five phantom claims

Rule F "Truth in Advertising" in `docs/specification/validation.md`: a pattern's `signature` declares a polymorphic interface, and the pattern must invoke the tools necessary to fulfill that interface via `composes_with`. Five patterns currently claim signatures without any `composes_with` backing them:

| Pattern | Signature | composes_with |
|---|---|---|
| `ProtoPack` | `Artifact(Prototype)` | (empty) |
| `StateTransition` | `Transition(State)` | (empty) |
| `ContextCompress` | `Compress(Context)` | (empty) |
| `StateAudit` | `Audit(State)` | (empty) |
| `Sign` | `Act(Identity)` | (empty) |

Each of these claims to be an implementation of a polymorphic interface but declares no active delegation. Either the signature is aspirational (and should be removed to avoid misleading discovery queries) or the composition is missing (and should be added). We resolve case-by-case:

- `ProtoPack`, `StateTransition`, `ContextCompress`, `StateAudit`: the pattern internally performs the operation without delegating. The signature is accurate as a *declaration of type*, but Rule F requires delegation. We rephrase these as plain Verbs (drop the signature) since they're leaf implementations, not polymorphic dispatchers.
- `Sign`: the mechanism says it "attaches a verifiable identity proof" — that implies invoking an Identity pattern's verification logic. We add `composes_with: { identity_verify: "sema:Identity#..." }` and update the mechanism to reference `{{identity_verify}}`.

### 3.13 Verification-stack yield types — four primitives wired

`docs/specification/naming.md` §1 defines four orthogonal verification primitives and their required output types:

| Primitive | Required `yields` |
|---|---|
| `Gate` | `Decision` |
| `Check` | `Status` |
| `Judge` | `Score` |
| `Validate` | `Boolean` |

Currently all four have empty `yields`. Descendants that compose these primitives don't inherit the output contract, which breaks type safety in verification pipelines — a Gate could conceptually return anything, including a Score, which would make it behavior-compatible with Judge at runtime and break callers that expect a binary pass/block.

We add the four `yields` declarations to complete the contract. For each, we also ensure the output pattern (`Decision`, `Status`, `Score`, `Boolean`) exists in the vocabulary; Boolean is a primitive type not currently a pattern and gets introduced as `Boolean` in Infrastructure/Data Structures with a minimal `data_schema`.

### 3.14 Solver-family alignment with Fractal Intelligence v3

The Fractal Intelligence paper (v3, April 7, 2026) crystallizes the Solver Contract into **five explicit surfaces**: Manifest, Execute, Consult, Verify, Feedback. Manifest and Execute are mandatory; Consult/Verify/Feedback are optional but strongly recommended at hard seams. The paper also formalizes the `Task`→`Result` transaction, defines hard-seam semantics (acceptance gates that force upstream *restructuring* rather than retry), and introduces architectural concepts (Frame Errors, Pathway Memory, the directed-graph nature of the Universal Solver Tree) that the current vocabulary doesn't yet reflect.

The solver-family patterns currently in the library predate this crystallization and carry drift from it. We align them here.

*Handle note*: this section refers to `CognitiveSolver` as that was the pattern's name when §3.14 was written. §3.21 later renames `CognitiveSolver` to `PolymorphicSolver`; the §3.14 mechanism updates described below apply equally to the renamed handle.

**Surface naming — `Question` → `Consult`**. `CognitiveSolver`'s mechanism names the five surfaces as "Manifest, Execute, Question, Verify, Feedback" (ring 1, tier 1, Mind/Strategy). The paper uses **Consult** for the third surface — "How would you approach this? Open consultation: cost/quality estimation, clarification, rationale requests, context-sharing. Enables the marginal-value rule." The `Question` naming conflates asking clarification with the broader consultation surface that includes cost estimation. We rename the surface reference in CognitiveSolver's mechanism to `Consult` to match the canonical contract, and update the gloss per §3.4.

**`Solver` mechanism — specify the five surfaces**. `Solver` (Mind/Strategy, ring 0, tier 0) currently reads "Abstract interface for transforming Tasks into Solutions." Since Solver is the tier-0 primitive on which the whole solver family rests, its mechanism should explicitly enumerate the contract descendants inherit. Updated mechanism: *"The abstract interface exposing the five-surface Solver Contract — `Manifest` (what can you do?), `Execute` (perform the Task), `Consult` (cost/quality/rationale), `Verify` (post-execution assurance), `Feedback` (structured evaluation). Manifest and Execute are mandatory; remaining three are optional. Accepts a typed `Task`, returns a typed `Result`."* This makes Solver the canonical reference point in the graph.

**`SolverTree` invariant — drop the "single supervisor" claim**. The current invariant reads "Chain of Command: Every node (except root) has exactly one active supervisor." The paper (§Topology Freedom) is explicit: *"While we retain the name 'Universal Solver Tree' for its conceptual clarity—decomposition is top-down and tree-like in origin—the actual data structure is a directed graph: fan-in, deduplication, and cycles mean `|E| > |V|-1` in practice."* The single-supervisor invariant forbids fan-in, which is architecturally required for shared sub-solver reuse (a `StabilityRegulationSolver` called by both economics and psychology paths). We drop it and replace with: *"Origin: The structure is tree-like at decomposition time but permits fan-in and deduplication at execution, making the runtime graph a DAG."* This is the change most visible to descendants — patterns that currently assume strict tree topology will need to accommodate fan-in.

**`UniversalSolverTree` — acknowledge the directed-graph reality**. Same update as SolverTree at the aggregate level. The "Singularity" invariant ("logically only one Universal tree containing all knowledge") remains; what changes is the *shape*: DAG, not tree. Mechanism updated accordingly.

**`SolverRoot` → `RootSolver` — rename + emphasize triage and Pathway Memory**. The current DB handle `SolverRoot` is drift from earlier nomenclature; the Fractal Intelligence paper v3 §Recursive Composition canonically uses `RootSolver`. We rename the pattern with `_meta.supersedes: [SolverRoot-sema_id]` so downstream consumers of prior vocabularies redirect cleanly. The paper is explicit about RootSolver's defining role: *"The apex case is the `RootSolver`: a Solver whose Task is an open-ended goal and whose cognitive operation is triage—determining what kind of problem this is and routing it. The `RootSolver`'s Pathway Memory is the architecture's most consequential site of compounding: it is the only node that sees how all problems enter the system."* The current mechanism covers framing and budget allocation but omits triage and Pathway Memory. Updated mechanism foregrounds both.

**Singleton invariant**: each SolverTree has *exactly one* RootSolver. The UniversalSolverTree's RootSolver is the unique global entry point for all problems routed through the system (the "one root for humanity" if the UniversalSolverTree scales as the paper envisions). Sub-trees carved out of the Universal get their own RootSolver. This is a definitional property of what a tree-apex IS; passes the broad-use test because no legitimate descendant can have zero or multiple roots per tree.

Other patterns that reference `SolverRoot` by template syntax (including `UniversalSolverTree`'s mechanism) are updated to use `RootSolver`. This is a cascade rename; the rebuild-from-staging strategy handles it cleanly.

**`Task` schema — enumerate the four fields**. Currently Task is "The atomic unit of intent" with invariants about holographic inheritance and parent linkage, but the actual schema (what fields Task objects carry) is not crisply specified. The paper (§Transaction Model) gives the canonical four: `operation`, `inputs` (typed), `acceptance_criteria` (AcceptSpec), `budget`. We update Task's `data_schema` to require these four fields. This closes the Rule E "non-vacuous schema" requirement for Task (which was already non-vacuous but now carries the specific fields descendants should inherit).

**`Result` schema — add the transaction output shape**. `Result` exists in the library but its `data_schema` is light. Paper specifies: `outputs` (typed artifact), `status` (`success` | `partial` | `fail`), `stop_reason` (`completed` | `budget` | `quality`). We update Result's data_schema to require these. This closes the symmetric gap on the Execute surface's return type.

**`Solution` vs `Result` — clarify the distinction**. Both currently exist; their relationship is implicit. Per the paper: Result is the raw output of the Execute surface; Solution is a verified+wrapped-with-provenance artifact. We update both mechanisms to make this explicit:
- Result: the minimal transaction output of Execute (outputs + status + stop_reason)
- Solution: a Result that has passed its AcceptSpec gate and been signed with provenance by the producing Solver

**`RigorousSolver` — encode the ceremony mechanics inline**. RigorousSolver's current mechanism correctly mandates full verification; the paper's (§sec:scale) "Level 4 ceremony" frame is useful *externally* but cannot be carried into the pattern text as-is (per Naming Taxonomy §2.E the pattern must be self-contained — no off-graph references). We update the mechanism to encode the mechanics directly: *"Mandates the full five-surface contract (Manifest, Execute, Consult, Verify, Feedback) with non-compensatory acceptance gates — every declared invariant must pass before a Result becomes a Solution; partial success is not permitted to propagate."* No external level reference; the ceremony is the mechanism.

**`OptimisticSolver` — the velocity-oriented sibling of RigorousSolver**. Currently in Society/Protocols (ring 1, tier 2). It's a legitimate orthogonal specialization of `CognitiveSolver`: where RigorousSolver trades speed for pre-action verification, OptimisticSolver trades pre-action verification for turn-atomicity, parallel throughput, and post-action error correction (via Reflexion + Compensate). Together, RigorousSolver and OptimisticSolver define the two poles of the speed/safety axis above CognitiveSolver's default. This is the paper's "productive extremes" (§sec:synergy) made concrete.

**Layer retained — Society is correct.** An earlier draft proposed moving OptimisticSolver to Mind/Strategy for family legibility alongside Solver/CognitiveSolver/RigorousSolver. This was wrong: OptimisticSolver `composes_with` `AtomicBid` and relies on the Actor Model — both Society-layer. Under Rule G (gravity), a Mind-layer pattern cannot hard-depend on Society-layer patterns. Splitting the solver family across Mind and Society is a real legibility cost, but it's the honest answer: the moment a solver depends on multi-agent coordination primitives it is no longer a Mind-layer thing, and relocating it would either invert gravity or require stripping the dependencies that make it what it is. The fix for the legibility cost is a graph-level affordance (e.g., a "solver family" view) — not a relocation. **What we do fix**: zero incoming references. We add cross-links from multi-agent coordination patterns (e.g., `Rally`, `ContinuousResourceAuction`) that benefit from high-velocity solvers so the optimistic path is reachable from the graph.

**New patterns to introduce**:

- **`FrameError`** (Mind/Reasoning, ring 1, tier 1) — a typed failure mode signaling that acceptance rejection requires *lateral reframing* of the problem, not retry. Invariant: "A FrameError from a child forces the parent to restructure its approach, not re-execute." This captures the paper's central claim that hard seams produce restructuring, not iteration. An earlier draft placed this in Physics/Primitives; that was wrong — lateral reframing is a cognitive/epistemic realization, not a substrate-level primitive. It belongs in the cognition layer.
- **`PathwayMemory`** (Mind/Memory, ring 1, tier 1) — the learned routing decisions that compound at each node that dispatches. Used by RootSolver, but not exclusive to it. Mechanism: *"A memory structure recording (problem_class, route_chosen, outcome_quality) tuples. Enables a dispatching Solver to learn which routes produce better results for which problem types."*
- **`DecompositionGate`** (Mind/Reasoning, ring 2, tier 2) — the four-test decomposition suite: Necessity (removal collapses parent), Independence (sub-concepts vary orthogonally), Universality (every instance of parent contains this sub-concept), Completeness (addressing all sub-concepts gives back a functioning instance). Applied as a gate that admits or rejects candidate decompositions; yields a `Decision`. The paper's Section 2 is the rigorous specification. An earlier draft named this `FourTests` (naming-morphology violation) and then `DecompositionCheck` (type-stack violation: a `Check` yields a `Status`, not a `Decision`, per `naming.md` §1). The four-test suite's semantics are admit/reject — Gate semantics — so `DecompositionGate` is the correct type. Ring 2 (tactical heuristic) rather than Ring-1 primitive.
- **`DocumentedOverride`** (Society/Governance, ring 1, tier 2) — the "override-with-documentation" safety valve at hard seams. Fail-closed semantics are strict by design, but an unrecoverable deadlock at a hard seam needs a supervised exit rather than silent system violation. Mechanism: *"Accepts a failed Result plus a textual rationale and override authority; composes_with TimeWarpLog to cryptographically log the override event (forward action + override + rationale) and yields a forced Decision bypassing the failed gate."* The override is a first-class coordination act, not a backdoor. Identified by Gemini's second-pass review — the paper specifies this outcome at §sec:seams and the current library lacks any mechanism for it.

**Not introduced: `RoutingGate`.** An earlier draft proposed a fused `Gate`-that-yields-a-`Route` to actuate hard-seam restructuring. Gemini's third-pass review rejected this on two grounds: (1) naming-type-safety — a `Gate` must yield a `Decision`, not a `Route`; a pattern named `Gate` that yields anything else corrupts the verification-stack taxonomy established in §3.13; (2) gravity — placing it in Infrastructure/Primitives while having it `compose_with` `PathwayMemory` (Mind/Memory) inverts Rule G. The correct treatment is compositional rather than monolithic: the existing `Gate` primitive halts and yields a `Decision` carrying the `FrameError` status; the receiving Solver reads the FrameError and invokes the existing `Route` or `Reframe` primitives. No new pattern needed. The hard-seam actuator is the composition `Gate → Decision{FrameError} → (Route | Reframe)` already expressible in the library.

**`AcceptSpec` mechanism update — the structural origin of `FrameError`.** `AcceptSpec` is already in the library but its mechanism doesn't specify the shape of evaluation outcomes. For the `FrameError`/hard-seam semantics to be actualized end-to-end, AcceptSpec needs to formally declare that non-compensatory validation failures produce a `FrameError` (forcing upstream restructuring) rather than a generic boolean `false`. Without this, the library has the `FrameError` noun but no structural guarantee that failed acceptance gates actually *produce* it — the hard-seam semantics would be advisory rather than enforced.

**Structural caveat — Noun/Verb discipline.** `AcceptSpec` is a **Noun** (a Requirements Contract carrying the `-Spec` suffix) and Nouns cannot structurally declare `yields` or `composes_with` — those fields belong to Verbs that actively execute. Per Gemini's fifth-pass review, the mechanism update is a *description of the contract's semantics*, not a declaration of active yields on AcceptSpec itself. The structural declaration belongs on the Verb that consumes AcceptSpec — specifically the `Verify` surface (or an internal `Gate`) that reads the AcceptSpec, evaluates it against a Result, and `yields` either `Solution` (on success) or `FrameError` (on failure). This preserves both the hard-seam logic and the Noun/Verb boundary.

Updated mechanism (on the Noun): *"Structured non-compensatory acceptance contract. Each gate is declared individually and carries a reframing hint for the FrameError emitted if it rejects. Consumed by the Verify surface; outcomes are surfaced by that surface's yields, not by AcceptSpec directly."*

Updated declaration (on the consuming Verb, Verify): *"accepts AcceptSpec; yields Solution | FrameError — Solution on non-compensatory success, FrameError carrying the specific rejecting gate and its reframing hint on failure."*

This two-party split is what the Noun/Verb rule enforces: the contract *defines*, the verb *emits*. A single AcceptSpec can be evaluated by multiple Verify surfaces (each yielding its own Solution|FrameError), which is the right factoring for the library.

**Not introduced in this pass** (specialized solver roles, each a legitimate future-mint candidate but beyond foundation scope):

- `OutcomeArbiterSolver` — blind comparative evaluator across structurally different decomposition paths (paper §sec:rootstrategy)
- `TaxonomistSolver` — maintains solution graph, performs structural coaching and ontological accommodation (paper §sec:synergy)
- `ReduceSolver` — selects the framing that maximizes downstream decomposability (paper §sec:jumps)

These are sufficiently specialized that they read as project-workflow roles rather than foundation primitives. They can be minted as-needed from the aligned Solver base class without the foundation pre-declaring them.

### 3.15 Caution field — additions where elevated risk isn't self-evident

Per `docs/specification/schema.md`, the `_meta.caution` field is an optional one-sentence warning for patterns carrying elevated risk that isn't already explicit in the pattern's mechanism, invariants, or failure_modes. It lives in unhashed metadata so it can be updated without changing identity. Add it when a pattern: enables irreversible action, bypasses safety checks or oversight, or enables evasion/manipulation/covert coordination.

Two earlier commits (April 2026) added caution to fifteen high-risk patterns: Lock, Mutex, StateLock, Permission, PermissionEscalate, HumanApprove, Consensus, Deploy, EjectionSeat, CommitmentDevice, AdversarialSteel, FeatureFlag, Sandbox, OathBind, IdentityHandshake. The current audit's changes create six additional cases where the risk threshold is crossed and caution should be added.

**`OptimisticSolver` — risk: executes without pre-action verification**. Mechanism explicitly trades pre-action verification for post-action correction. The turn-atomic stance means the Solver commits to actions before a downstream gate has evaluated them. For actions that are irreversible or have external side effects, this is genuinely risky and not fully captured by the existing failure modes (which only cite "Over-Eager Execution" and "Serial Deadlock").

> caution: "Executes without pre-action verification. Ensure irreversible actions have compensation or sandboxing, or use RigorousSolver at those boundaries."

**`ReAttempt` (new, Physics/Primitives) — risk: amplifies transient failures into DoS**. The substrate-level re-try primitive has no built-in ceiling; descendants set their own retry budgets. An unbudgeted ReAttempt loop is a denial-of-service vector against any rate-limited downstream resource.

> caution: "Requires an explicit retry budget; uncapped ReAttempt can amplify transient failures into DoS against downstream resources."

**`PathwayMemory` (new, Mind/Memory) — risk: poisoned memory silently biases future routing**. PathwayMemory records (problem_class, route_chosen, outcome_quality) tuples used by RootSolver and other dispatching Solvers to learn routing. An attacker who can influence what gets written to PathwayMemory (or who operates a compromised Solver that reports false outcome_quality) can silently bias every future routing decision without any visible failure.

> caution: "Silent contamination vector — poisoned entries bias all downstream routing decisions without triggering failure modes. Integrity of writers must be enforced."

**`FrameError` (new, Mind/Reasoning) — no caution needed**. Pure cognitive signal, no external effect. Rejected.

**`DocumentedOverride` (new, Society/Governance) — risk: bypasses a failed acceptance gate**. By construction, this pattern is a supervised bypass of fail-closed semantics. Even with rationale and logging, the action of overriding deserves a visible annotation separate from the mechanism text.

> caution: "Overrides a failed acceptance gate. The cryptographic log is the only post-hoc accountability; ensure override authority is scoped and auditable before composing."

**`Abduction` (consolidated with AbductiveLeap) — risk: unchecked explanatory leaps in high-stakes domains**. Abduction is "best guess from incomplete observation." In low-stakes cognitive work this is fine; in medical, legal, or financial reasoning, an Abduction accepted without subsequent verification is a hallucination vector.

> caution: "Best-guess inference — always provisional. Must be composed with a verification step in high-stakes domains."

**`TimeWarpLog` — risk: causal cone manipulation**. Events are accepted if they don't contradict the current causal cone. An attacker who can inject events with forged causal predecessors can rewrite system beliefs about what happened when. The mechanism describes the acceptance rule but the *exploit surface* isn't self-evident.

> caution: "Causal cone is only as trustworthy as the identities signing events. Unsigned or weakly-authenticated events can rewrite perceived history."

**`Compensate` — risk: rollback can be weaponized to erase evidence**. Compensate runs logged inverses in LIFO order. An attacker who can trigger Compensate selectively can erase inconvenient actions from the audit trail under the guise of legitimate rollback.

> caution: "Compensation must not erase the audit trail of what was rolled back — log both the forward action and the compensation."

**Not changing**: `DecompositionGate`, `Boolean` — purely cognitive/data, no external-effect risk.

The net addition is six new caution entries on top of the existing fifteen, bringing total coverage to twenty-one patterns (~5% of the library) — the set where risk warrants a human/agent-visible annotation that isn't already encoded in the hashed fields.

### 3.16 Topological gravity sweep — systematic Rule G check

Our audit fixed two macro-level layer misplacements (Uncertain, Retry) and spot-checked other layer concerns, but did not perform a full topological scan of the dependency graph for Rule G (Dependency Direction) violations. A primitive spot-check on `accepts`/`composes_with` directed edges found zero violations on the current DB, but the scan did not:
- Follow transitive chains (A→B→C where C is at a higher layer than A)
- Detect near-cycles (A→B where B cites A in mechanism text without a declared edge, the Rule H concern)
- Verify layer monotonicity across multi-hop dependency paths

We add a CI check: on every pattern mint, topologically sort all `accepts`/`composes_with` edges and verify the layer ordering is monotonic (downstream = same-or-higher layer). This is a cheap graph algorithm; it runs on the existing `GraphStore` in `src/sema/taxonomy_graph/graph_store.py` and catches violations before the cascade writes propagate.

### 3.17 Parameter ranges — generalize at foundation, specialize via descendants

Fifty-four parameters across 35 patterns currently carry `range: "unspecified"`. Successive drafts of this section progressively loosened the treatment — from concrete ranges, to typed-with-default, to typed-only. The final correct treatment goes further: **the foundation should be generalized; specificity belongs on descendants that `derived_from` the foundation pattern.**

This is the whole mechanism of the library. `Lock` is general mutual exclusion; `Mutex` is `derived_from Lock` adding token-possession and fencing. `Solver` is the abstract five-surface contract; `RigorousSolver`, `OptimisticSolver`, `CognitiveSolver` are `derived_from Solver` adding specific behaviors. The pattern works at the parameter level too: the foundation `HumanApprove` has a timeout slot; a descendant `LegalReview` *extends* `HumanApprove` and declares `timeout: Duration, range: [1d, 90d]`; a descendant `EmergencyApprove` extends it and declares `timeout: Duration, range: [1ms, 10s]`. Both descendants are legitimate; the foundation stays permissive.

An earlier draft of this audit tried to do all that work *at the foundation*. That was the categorical mistake. Foundations should be general so that descendants can specialize. Specifying `timeout: [1min, 24h]` at the foundation forbids both descendants from being minted without forking the derivation chain — the exact compounding problem §1 warns against, and the opposite of how the library is supposed to grow.

The corrected treatment sorts each of the 54 into three categories:

**1. Principled bounds — specify the range at foundation.** The value is mathematically or structurally bounded and no descendant can legitimately extend outside. `Belief.confidence: [0.0, 1.0]` (probability is mathematically bounded). `CapacityPressure.compression_ratio: [0.0, 1.0]` (ratio by definition). Booleans and enumerated sets where the full value set is closed. Seven parameters. These are the cases where the foundation *does* enforce structure — because math enforces it, not because we guessed at what descendants would need.

**2. Leave open for descendants — declare the parameter and its role; leave type and range unspecified.** The parameter name and its role (documented in the mechanism text) carry the semantic. Descendants mint specialized variants with type + range + default as their context requires. This is the scalability-preserving move, not a defect. Nineteen parameters fall here: all the timeouts, intervals, counts, depths, sizes where legitimate values span many orders of magnitude across descendant contexts. We leave these parameters declared in the foundation pattern (so the slot is part of the pattern's identity) with `range: "unspecified"` preserved, and add a brief `range_note: "parameterized; specialize via derived_from"` so future auditors don't re-flag the slot as lazy.

**3. Drop to `accepts` — not really a parameter.** The value is caller-supplied at runtime, not a configuration of the pattern's identity. Eighteen parameters fall here: `Aggregate.weights`, `Judge.criteria` (see §3.1), `Rally.selection_criteria`, `Monitor.threshold`, and others. These move out of `parameters` entirely regardless of the above typing question — they were miscategorized as identity-level configuration when they're really inputs.

**Why this matters for scalability.** The library scales by descendants adding specificity to generalized foundations. Every time a foundation over-specifies, a descendant that needs different specificity has to fork instead of extend — breaking the derivation chain and fragmenting the namespace. Every time the foundation under-specifies by moving a real parameter into vague `accepts` prose, the identity hash loses the slot and descendants can't reliably inherit it. The third error — what earlier drafts of this section nearly committed — is splitting the difference by imposing arbitrary bounds that feel like "reasonable defaults" but aren't anchored in anything. The correct discipline: bound when math or structure forces it, declare the slot and leave specificity open otherwise, and trust the `derived_from` mechanism to let descendants do the specialization that context demands.

The full per-pattern disposition is in Appendix A.

### 3.18 Second-pass manual sweep — what the axis-based sweeps missed

The preceding sections (§3.1–§3.17) are *axis-exhaustive*: each ran a specific query (unspecified parameter ranges, phantom signatures, orphan detection, Ring 0 over-claims, etc.) across all 427 patterns and returned every match. That catches anything that fits a known pattern-shape. It does not catch content-quality issues — patterns where the mechanism restates the gloss, where the layer label drifted from the mechanism's actual content, where the category is being used as a catchall, or where the handle is really a dimensional modifier rather than a standalone concept. This section is the result of a manual read of the 243 patterns the first-pass sections did not explicitly touch, looking for those issues.

**Society/Protocols layer bloat — twenty more relocations.** §3.2 moved two patterns (Uncertain, Retry) for layer fit; §3.8 rebalanced the Society/Coordination subtree. The manual sweep surfaces a larger systemic drift: `Society/Protocols` has become a default destination for any pattern that sounds coordination-adjacent, including patterns that describe single-system substrate behavior or single-agent cognition. Relocations:

- *Society → Infrastructure* (six patterns, all substrate-level): `FailClosed` (safety default), `IdempotentWrite` (write-key tracking), `StateSnapshot` (durable storage), `Warmup` (capacity ramp), `MonitorReport` (telemetry), `FeedbackSignal` (structured packet). These describe what a single system does, not how multiple agents coordinate.
- *Society → Mind* (fourteen patterns, all single-agent cognitive): `TimeboxThink`, `ThinSlice`, `CognitiveEcho`, `Fermi`, `SimulationTrace`, `ConstraintFirst`, `ConstructOntology`, `Compose`, `TraceBelief`, `MetaPrompt`, `PatternDiscovery`, `Proprioception`, `DeepResearch`, `RequestFraming`. Each of these mechanisms describes a single agent doing something cognitive; no coordination with a peer is required for them to execute. The last three were surfaced during the broad-use analysis (`2026-04-broad-use-analysis.md` §120, §131, §156) after the initial §3.18 list was compiled.

The underlying cause is that Society/Protocols became a catch-all during earlier minting. After these twenty moves, the Society layer reads as "patterns that require ≥2 agents to be meaningful" — which is what the layer is supposed to mean.

**Topology category split — unify three patterns.** Topology patterns describe the shape of execution or data flow. Five live in `Infrastructure/Data Structures` (`Chain`, `Tree`, `DAG`, `Skeleton`, `Sequence`), three live in Physics (`Linear`, `Cyclic` in Physics/Primitives; `Parallel` in Physics/Time). There's no principled reason for the split — all seven are abstract shape descriptions. We move `Linear`, `Cyclic`, `Parallel` to `Infrastructure/Data Structures` alongside the others so descendants looking for "topology types" find them in one place.

**`Linear` retires into `Chain`, not `Sequence`.** An earlier draft merged `Linear` into `Sequence` on the grounds that both describe "ordered execution." Gemini's fourth-pass review sharpened the distinction: `Sequence` describes *temporal execution ordering* ("do A, then do B"), while `Linear` describes *spatial graph topology* ("a non-branching shape"). `Chain` — already a separate Ring-0 pattern — is the instantiated spatial form ("a concrete data structure representing a sequential list of linked nodes"). Linear's own mechanism concedes it is "equivalent to a Chain." The correct move is to retire Linear into Chain (both spatial), not Sequence (temporal), and to add Linear's sema_id to Chain's `_meta.supersedes` list so downstream references resolve correctly. Extends §3.3 with a fourth redundancy cluster.

**Retirement metadata — `_meta.supersedes`.** This is the first retirement that requires explicit supersession metadata. §3.9 retired Group, Switch, AbductiveLeap without proposing a `supersedes` map, on the assumption that the fresh-rebuild strategy (staging → re-consume from scratch) would leave no dangling references. Gemini's fourth-pass review is correct that retirement should carry successor-pointer metadata regardless of apply strategy: `supersedes: [<retired_sema_id>]` lets downstream tools that pulled the old vocabulary redirect references cleanly rather than encounter a HALT. We add `_meta.supersedes` to:
- `Chain` → supersedes Linear's sema_id
- `Abduction` → supersedes AbductiveLeap's sema_id
- `Route` → supersedes Switch's sema_id (Switch was the Branch/Route/Switch cluster merge target; Route is the retained canonical)
- Successor for `Group` → to be determined (`Group` was retired as non-specific; no single obvious successor — may ship without a redirect if no pattern covers its concept)

**Dimensional modifiers — four trait conversions, two retained as canonical.** The sweep initially flagged six patterns as *dimensional tags* rather than standalone concepts: Meta, Global, Deep, Subject, Nature, Creative. Gemini's fourth-pass review split the set:
- *Trait-convert (four)*: `Meta`, `Global`, `Subject`, `Creative` — these are genuinely modifier-shaped. Converting to `is_trait: true` preserves the lexical tokens needed for polymorphic signatures (e.g., `Meta(Prompt)`) while legally exempting them from Rule E's `data_schema` requirement. Deleting them would break the signature-resolution path; keeping them as full patterns forces vacuous schemas; trait is the right compromise.
- *Retained as canonical (two)*: `Deep` and `Nature` stay as full patterns. The Fractal Intelligence paper (§4.3 "The Grammar of Agency," Table 1) specifies `Deep` as one of the five foundational Ring-0 **Verbs** (the "Scientist" primitive that escalates heuristics to rigorous implementations) and `Nature` as a canonical **Noun** target in the `Deep(Nature)` signature. Converting either to a trait would break the paper's Grammar of Agency at the foundation layer. The shallow mechanism texts we flagged reflect bad writing, not wrong classification — the fix for these two is a mechanism rewrite that matches their canonical roles, not a trait conversion.

Also noted on asymmetric pairs: `Global` exists without a `Local`; `Deep` exists without a `Broad`; `Subject` exists without an `Object`. Trait conversion resolves this cleanly for Global and Subject (tags don't need poles). For Deep, the apparent absence of `Broad` is actually a **naming illusion** — per Gemini's fifth-pass review, the Fractal Intelligence paper v3 §4.3 names the horizontal-breadth primitive (the "Scout") as `Discover`, not `Broad`. `Deep` is the vertical axis (the "Scientist") and `Discover` is the horizontal axis. Minting `Broad` would create a redundant synonym for `Discover` and clutter the Ring-0 namespace. No action needed.

**Noun/Verb miscategorization — two more for §3.11.** §3.11 caught Check, Observe, ToolInvoke (verb-category patterns named as nouns). The sweep finds two more in Mind/Reasoning where the handle is Noun but the mechanism reads as Verb: `Decision` ("The cognitive act of committing") and `Synthesis` ("The process of combining"). Options are (a) rename to `Decide`/`Synthesize`, or (b) rewrite the mechanisms to describe the resulting artifact (the committed choice; the combined whole) rather than the process. We propose (b) — the Noun handles are canonical enough that rename would break inbound references; rewriting the mechanism to describe the artifact is the narrower fix.

**More gloss=mechanism restatements — eight more for §3.4.** The sweep finds eight Nouns whose mechanism paraphrases the gloss rather than specifying identity: `Hypothesis`, `Hierarchy`, `Outcome`, `Metric`, `Prompt`, `Anomaly`, `Correlation`, `Queue`. Each needs a mechanism that tells a reader what *distinguishes* this Noun from its neighbors. Concretely:
- `Hypothesis`: distinguish from `Claim`, `Assumption` — a Hypothesis is a testable prediction staged for falsification attempts, not a held belief (Assumption) or asserted position (Claim).
- `Correlation`: distinguish from `Causation` by structure, not by naming the fallacy (cum-hoc-ergo-propter-hoc is a consequence, not a definition).
- `Queue` vs `Stream`: both are ordered containers; Queue's mechanism should say why the ordering semantics differ (FIFO discipline + consumer ownership vs continuous open-ended emission).

**More marketing-speak glosses — eight more for §3.4.** Extending the nine already flagged: `Break`, `Card`, `DriftWatch`, `HeldRelease`, `Overlap`, `ExperienceSharding`, `FractalIntelligence`, `Taper`. `DriftWatch` and `HeldRelease` carry multi-sentence essays where a one-line definition belongs; `FractalIntelligence` reads as a mission statement ("the unified fractal architecture of scalable, self-correcting intelligence") rather than a definition. We apply the same treatment as §3.4: rewrite each to a one-line definition naming the mechanism's boundary.

**Weak or abstract patterns — two concrete actions.**
- `Creative` (Mind/Strategy R1T1, gloss "Generating novelty and value") is too abstract to act on. Its role is already played by specific descendants (`PUREBrainstorming`, `AnalogyBridge`, `NoiseInjection`, `LateralOptimization`). We convert it to a Trait (matching the modifier-conversion in the dimensional-modifiers finding above) rather than keep it as a standalone pattern.
- `Aesthetics` (Society/Protocols R0T1) is a metric type. Move to Infrastructure/Data Structures.

**Net count effect.** The sweep's primary work is relocations and mechanism rewrites, not additions/retirements. One retirement (`Linear` merged into `Chain`) drops the count from 430 to 429 at the end of §3.18; the apply-time addition of `Status` brings it back to **430 patterns** (§6.1). The four trait conversions (Meta, Global, Subject, Creative) keep those patterns in the library as Traits with `is_trait: true` — same count, different semantic role. Deep and Nature stay as full patterns with rewritten mechanisms.

### 3.19 Audit-of-the-audit — the broad-use test

The §3.17 re-think (parameter ranges) exposed a principle, but an interim draft over-corrected and loosened required fields below the level callers need to interpret the pattern. The calibration question both failures miss is the one that actually matters:

**For each pattern, ask: what would constitute broad use of this pattern?**

Walk through the answer concretely. What are the legitimate contexts this pattern appears in? What does each of those contexts need from the pattern to be able to use it? What parts of the specification would any of those contexts need to override?

Example — `HumanApprove`. Broad use spans: legal review (multi-week), compliance committees (days), operational deploys (minutes), test mocks (ms), emergency auto-reject (ms). What do all of these need? A timeout slot. What timeout value? Different for each. Conclusion: timeout is required as a named parameter, but type and range stay open — each context specializes via `derived_from`.

Example — `Task`. Broad use spans: exploration tasks, bounded solver work, research experiments, transactional operations, exploratory prompts. What do all of these need? To specify *what* (operation), *to what* (inputs), and *when they're done* (acceptance_criteria). Without the "when done" signal, the caller cannot close the transaction — and every Task use-case needs some form of closure. Budget, though, only binds some contexts (BoundedTask yes, UnboundedTask no). Conclusion: operation + inputs + acceptance_criteria are the usability floor; budget is optional.

Example — `Score`. Broad use spans: model evaluation, fitness scoring, relevance ranking, aesthetic ratings, adversarial judgments. What do all of these need? A value (obviously), a normalization range (is 0.7 out of 1 or 10 or 100?), a metric identifier (what was scored). Without any of the three, the Score is ambiguous — callers can't interpret it. Conclusion: all three required.

Example — `EntropyPump`. Broad use spans: escape from local optima, simulated annealing, chaos engineering, exploration bonuses. What do all of these need? Entropy injection. Do any of them need "bounded injection" or "targeted scope"? No — those are specific disciplines only some descendants want. Conclusion: leave invariants off at foundation; descendants add them.

**The test generalizes.** Before specifying any invariant, parameter, or required field, walk the broad-use question: *what contexts will use this, and what does each need?* A spec item belongs at the foundation if and only if every legitimate broad use needs it. Otherwise it belongs on a descendant that wants that specific discipline.

Applying the test to the audit's additions yields the calibrated treatment below. Some specifications stay (definitional — every broad use needs them). Some loosen (prescriptive — only some broad uses need them). Some tighten (under-specified — broad use would be ambiguous without them).

**`EntropyPump` invariants (§3.1) — pulled back.** Earlier proposed: *"bounded injection (noise magnitude capped so it doesn't destabilize equilibria) and targeted scope (applied to stuck states, not stable ones)."* These forbid legitimate descendants: `ChaosMonkey` (deliberately destabilizing), `UniversalEntropyPump` (global rather than targeted), simulated annealing at high temperature (deliberately unbounded). Revised treatment: rewrite EntropyPump's mechanism text to clarify what it does (inject entropy to escape convergence), but *drop the invariants entirely* — let descendants like `BoundedEntropyPump` add "bounded injection" and `TargetedEntropyPump` add "applied to stuck states only" as their own invariants if those are the semantics they want.

**`Budget` invariants (§3.1) — partially pulled back.** Earlier proposed: *"monotonic allocation: total never decreases without an explicit refund event. Conservation stays."* "Conservation" (tracked value is preserved across transactions) is close to definitional for what Budget is — we keep it. "Monotonic allocation" forbids `RollingBudget` that rebalances dynamically, and `FluidBudget` that reallocates mid-flight — we drop it. The definitional floor for Budget is now just conservation; strict-non-negative, monotonic, or other stricter disciplines become descendant-level specializations.

**`Task` data_schema (§3.14) — three required, one optional.** Earlier proposed four required; an interim draft loosened to two required (`operation`, `inputs`) with `acceptance_criteria` and `budget` both optional. That over-loosened. The Solver Contract's whole point is that the transaction boundary requires a defined acceptance spec — a Task without `acceptance_criteria` is a command, not a Task; callers literally cannot close the transaction. Revised: `operation`, `inputs`, `acceptance_criteria` all required (definitional minimum for a Task to be usable end-to-end). `budget` becomes optional — `UnboundedTask` is a legitimate descendant that doesn't carry a cost ceiling, and `BoundedTask` (already in the library) declares `budget` required at its level. Descendants like `ExplorationTask` that want open-ended acceptance supersede via `derived_from` with their own mechanism, rather than inheriting a Task with the field absent.

**`Result` data_schema (§3.14) — one required field pulled back.** Earlier proposed three required fields: outputs, status, stop_reason. `status` and `stop_reason` remain required — they're what distinguishes a Result from any other artifact. `outputs` becomes optional: a Result with `status: fail` legitimately has no outputs to report, and forcing an empty-outputs field wastes hash space. Minimum viable Result is `status + stop_reason`; `outputs` is present when there's something to yield.

**`Score`, `Summary`, `Probability` data_schemas (§3.10) — required fields set to the usability floor.** Earlier proposed requiring three fields each; an interim draft loosened to one required field per pattern. That under-specified `Score`. Revised:
- `Score`: `value: number`, `normalized_range: [min, max]`, `metric_id: string` — **all three required**. A Score's value is ambiguous without knowing the normalization range (is 0.7 out of 1, or 10, or 100?), and an anonymous score (no metric_id) can't be interpreted by the caller. Keep all three required for usability; descendants like `UnboundedScore` can supersede if they need different semantics.
- `Probability`: `value: number [0,1]` required (principled, math-bounded). `confidence_interval` optional. No change.
- `Summary`: `source_ref: sema_id` required (a Summary without a source reference isn't a summary). `compression_ratio` and `preserves` optional — descriptive metadata, not load-bearing for usability.

The discipline: *usability floor* means the fields a caller must have to invoke and interpret the pattern. Below that floor, the pattern stops being usable and becomes ambiguous. Above it, fields are optional descriptors or descendant concerns.

**What stays as specified.** The coherence fixes in §3.1 for TimeWarpLog (causal consistency), Judge (criteria → accepts), ConfirmationBlock (disconfirmations_required rename) are definitional or structural — they don't add constraints descendants would need to break. The new patterns in §3.14 (FrameError, PathwayMemory, DecompositionGate, DocumentedOverride) were written without proposing invariants at the foundation level; descendants that want specific invariants will add them.

The discipline that generalizes: **every constraint at foundation level should be justified by what the pattern definitionally IS, not by what seems useful**. If you can imagine a legitimate descendant that violates the proposed constraint, the constraint is a descendant-level concern, not a foundation-level one. Apply the rule on every mint, not just during audit.

### 3.20 Ring-0 reference wiring — eighteen edges added to discharge the deferred work

§3.6 wired three orphan anchors (Risk, DAG, ScoringFunction) into patterns that clearly used them. §3.7 identified six additional Ring-0 patterns as "zero current callers" and explicitly deferred the wiring pass as follow-up work. On review, that deferral was a mistake: Ring-0 orphans create the same compounding problem §3.6 set out to fix, just one layer deeper. A foundational primitive with zero callers is a primitive the library claims is foundational but doesn't actually use. We close the debt here.

Method: for each of the six Ring-0 patterns listed in §3.7 as needing wiring, we read every candidate pattern's mechanism text and added a `references` edge only where the candidate's declared mechanism actually uses the foundation's concept — not where the mechanism merely shares a keyword with the foundation's gloss. `references` (soft citation) rather than `composes_with` (active delegation) or `accepts` (noun read at call time) — these are lineage declarations, not runtime dependencies.

The eighteen edges:

| Foundation | Pattern gaining `references` edge | Justification from mechanism text |
|---|---|---|
| `Cache` | `HeuristicSnap` | "fast pattern matching against a 'cached experience' database" |
| `Cache` | `IdempotentWrite` | "subsequent ones return the cached result" |
| `Cache` | `PathwayMemory` (new) | routing outcomes stored for later reuse — the core cache semantic |
| `LatentAttachment` | `AnalogyBridge` | "searches its training data for a structural analogy" — embedding-backed search |
| `LatentAttachment` | `Card` | declares "semantic_search" in the discovery query spec |
| `LatentAttachment` | `LatentWander` | "Offline exploration of embedding space" |
| `LatentAttachment` | `PatternDiscovery` | "semantic search against the existing registry" |
| `LatentAttachment` | `RetrievalAugment` | "vector database, search index, knowledge graph" |
| `ContextFirst` | `OODA` | Observe-Orient-Decide-Act — the Observe-first mandate |
| `ContextFirst` | `RequestFraming` | "understand the 'real ask' within the given context before committing resources" |
| `ContextFirst` | `RetrievalAugment` | "Before generating a response, the agent queries an external knowledge store" |
| `ContextFirst` | `ToolDiscovery` | "orient via registry" — the explicit orient-first phrasing |
| `MonotonicCounter` | `AuditTrail` | "Immutable append-only log" — append-only is monotonic by construction |
| `MonotonicCounter` | `Ballot` | "immutable once cast — amendments require a new Ballot" |
| `MonotonicCounter` | `TimeWarpLog` | append-only causal log (post-§3.1 mechanism: causal consistency) |
| `CommitmentDevice` | `Bid` | "A Bid is a commitment: solvers cannot exceed bid cost" |
| `CommitmentDevice` | `Contract` | "immutable record of agreement... all parties must sign" |
| `CommitmentDevice` | `HeldRelease` | "hash commitment (SHA256)" — cryptographic pre-commitment |

**`AnchorDrop` remains unwired.** The sixth Ring-0 pattern listed in §3.7 — `AnchorDrop` (emergency state checkpointing) — has no pattern in the current library whose mechanism genuinely invokes it. Unlike the other five Ring-0 foundations, which turn out to have real usage once you look, AnchorDrop's concept (consensus-recovery after network turbulence) is genuinely niche at this point in the library's evolution. We leave it as-is rather than force-wire a spurious reference. If a pattern that handles consensus recovery ever gets minted, AnchorDrop will be its natural reference target.

**What we did not do in this pass.** A full reference-density sweep (mechanism-template-vs-declared-deps for all 430 patterns, sibling-family cross-references, descendant→ancestor chains) is a separate pass from this one. This §3.20 closes the specific debt §3.7 created; broader reference-density work is named as follow-up in §4.

### 3.21 Broad-use follow-ups — commands surfaced by the companion analysis

The companion document `2026-04-broad-use-analysis.md` walked every one of the 427 patterns through the six-step broad-use test (§3.19). That exercise produced 66 numbered audit items. Most validate decisions in §3.1–§3.20 — but a subset surface *new* commands the axis-based passes did not produce. Those are collected here so they get applied rather than deferred. Each item names the finding, the command, and whether the command changes prose (careful) or metadata only (mechanical).

**Axis failure — why these were missed.** The axis-based queries in §3.1–§3.17 each targeted a single dimension (coherence / layer / category / ring / schema / signature / etc.). The broad-use test is orthogonal: it asks whether the pattern's foundation holds across *all its legitimate descendants*. That cross-cut catches items no single-axis query will — under-specified yields, tier/ring misalignment, category-by-pattern-name misfiles, and cross-references whose direction got inverted to break a cycle. Future audits should run broad-use *before* the axis sweeps, not after, so the axis sweeps can pick up the broad-use findings rather than the other way around.

**Layer/category corrections (metadata-only).**
- `Critique` was re-categorized from Infrastructure/Data Structures to Infrastructure/Primitives in the §3.11 hand-apply — broad-use (#26) confirmed it's a Verb.
- `Monitor` (Mind/Strategy R0T0) — mechanism is a `{{loop}}` + `{{observe}}` composition. Broad-use (#40) flags this as a Verb miscategorized. Move to Infrastructure/Primitives.
- `Tension` (Mind/Strategy) — mechanism text: "A data structure representing..." Broad-use (#59) flags the Noun shape. Move to Infrastructure/Data Structures.
- `Reversibility` (Society/Protocols) — mechanism is a pure Condition (evaluates TRUE/FALSE). Broad-use (#64) flags Society/Protocols as weak fit. Move to Physics/Primitives (foundational predicate).
- `Ballot` — currently Tier 3 (experimental). Used by `Vote`, `LazyConsensus`, and others as a foundational decision-record artifact. Broad-use (#4) argues T3 is wrong for something this foundational. Move to Tier 1.
- `Context` — currently R0T3 (kernel ring, experimental tier). Rings and tiers usually align. Broad-use (#47) recommends Tier 1 given Context's foundational role in agent execution. Move to Tier 1.

**Mechanism rewrites (prose; hand-edit).**
- `Audit` (Infrastructure/Data Structures) — current mechanism reads "the process of verifying" (Verb-shape). Broad-use (#52) flags the Noun/Verb miscalibration. Rewrite the mechanism to describe the *audit artifact* (a structured record of a verification event with inputs, outputs, and verifier identity) rather than the process.
- `DissentSeek` — mechanism references `confirmation_block` (old parameter name). Broad-use (#63) flags this as stale after §3.1 rename. Update the mechanism to reference `disconfirmations_required` (the renamed parameter).

**Handle rename — `CognitiveSolver` → `PolymorphicSolver`.** The pattern's mechanism explicitly says "any entity — from a fleeting thought process to a complex swarm" — i.e. any substrate implementing the five-surface Solver Contract, not specifically cognitive ones. "Cognitive" was doubly redundant: the pattern lives in Mind/Strategy (so its layer already says it thinks), and the contract-conformance is about polymorphism across substrates (including non-cognitive ones). Per broad-use #14 (the pattern spans LLM, human, hybrid, tool-using, nested, fractal-intelligence instantiations — structural as much as cognitive), the name should emphasize *contract conformance across substrates* rather than cognition. Rename with `_meta.supersedes: [<old CognitiveSolver sema_id>]` so downstream consumers of prior vocabularies redirect cleanly. Five callers updated: `OptimisticSolver`, `RigorousSolver`, `FractalIntelligence`, `RealizationProtocol`, `PUREOptimization` — mechanism templates, dependency keys, and `RigorousSolver.derived_from` all flipped from `cognitive_solver` to `polymorphic_solver`. The Fractal Intelligence paper's broad-solver framing validates this.

**Solver family completion — derived_from chain, PathwayMemory wiring, role-bearing framing, ConceptualDecomposition mint.** Post-rename review of the solver family against FI v3 surfaced three gaps and one missing concept:

1. *`derived_from` chain was partial.* Only `RigorousSolver` had it (pointing to PolymorphicSolver with a stale zero-hash). Now `PolymorphicSolver.derived_from = Solver`, `OptimisticSolver.derived_from = Solver` (not PolymorphicSolver — OptimisticSolver is Society-layer and must derive from the abstract contract, not from the Mind-layer default implementer), and `RigorousSolver.derived_from` points at the current PolymorphicSolver hash. The family's lineage is now a crisp tree rooted at `Solver`.

2. *PathwayMemory was under-wired.* The paper says compounding-learning happens at *every* dispatching solver, not just the apex RootSolver. Added `composes_with: pathway_memory` to `PolymorphicSolver` and `OptimisticSolver` (both can dispatch), with mechanism prose integrated naturally. RootSolver retains its own (already wired per §3.14).

3. *Role-bearing / construction-pattern framing missing from `Solver`.* Solver's mechanism now explicitly captures three FI-aligned facts: **(a)** Solver is an interface, not a class — any `{{agent}}` can take on the role of a Solver for the duration of a Task. **(b)** The `"[descriptor]Solver"` naming convention is the library's construction pattern — `DiagnosticSolver`, `PlanningSolver`, `ReduceSolver`, `PUREOptimizationSolver`, etc. are all minted by appending `Solver` to a domain descriptor. **(c)** Recursion follows naturally: when a Solver decomposes its Task, it becomes the root of a sub-tree whose children are themselves Solvers — the mechanism that gives the UniversalSolverTree its fractal shape. `Solver` now `references agent` to declare the role-bearer relationship in the graph.

4. *Mint — `ConceptualDecomposition`* (Mind/Reasoning, Ring 1, Tier 1). The activity that distinguishes FI from plain `Decompose`: taking a concept and breaking it into sub-concepts where each sub-concept is bound by the Solver contract (Manifest + Execute minimum), making each delegatable. Decompose merely divides; ConceptualDecomposition divides into *solver-compatible units*. This is the intellectual move that enables the recursive fractal structure, and it is what agents *do* when they perform lightweight fractal intelligence on a specific problem. The pattern `composes_with: decomposition_gate` (to validate Necessity/Independence/Universality/Completeness) and `composes_with: synthesis` (to recompose child results). FractalIntelligence's mechanism is updated to reference `{{conceptual_decomposition}}` as the core activity, and explicitly notes that the resulting structure may persist as a reusable pattern or be torn down at completion — both lightweight and persistent modes are legitimate.

5. *Mints from FI Table 4 — `PerformanceSignal`, `FailureTrace`, `ReceptivityGate`.* Reading the paper's Table 4 ("Mapping from architectural concepts to content-addressed Sema patterns") against the library surfaced three canonical patterns the paper names directly but the library was missing:
   - **`PerformanceSignal`** (Infrastructure/Data Structures, Ring 0, Tier 1) — per Table 4, this is the Feedback-surface output artifact (not generic `Feedback`, which is the primitive concept). A Solver's Feedback surface emits a PerformanceSignal: either a scored evaluation, a pass/accept confirmation, or a FrameError escalation. Distinct from `Feedback` the way `Result` is distinct from "execution": Feedback is the primitive concept; PerformanceSignal is the typed artifact that feeds PathwayMemory and drives localized learning.
   - **`FailureTrace`** (Infrastructure/Data Structures, Ring 1, Tier 1) — per §7.1, a structured proof of which AcceptSpec clause an artifact violated. Required whenever a downstream consumer rejects an artifact and returns the rejection through a Solver's Feedback surface. Three invariants: clause-specific (names exactly one violated clause per entry), evidence-bound (paired with citeable evidence from the artifact), signed (evaluator identity cryptographically verifiable).
   - **`ReceptivityGate`** (Society/Protocols, Ring 1, Tier 1) — per §7.1, the Gate that guards the Feedback surface against poisoned or hallucinated rejection signals. Runs `{{validate}}` on any incoming FailureTrace: checks that the cited clause exists, that the evidence matches the artifact, that the evaluator signature is valid. Invalid or hallucinated feedback is dropped rather than absorbed into PathwayMemory. Required at any Feedback surface exposed to untrusted downstream consumers in a decentralized cognitive commons.

   These three close the Feedback-surface half of the five-surface contract at the same level of patternization as the other surfaces (Manifest→Card, Execute→PolymorphicSolver, Consult→SocraticLoop, Verify→Validate). Incoming wiring was added at mint time rather than deferred: `Solver` and `PolymorphicSolver` mechanisms updated to name PerformanceSignal as the Feedback surface's typed output; `OrchestrationLoop` mechanism notes that cross-trust-boundary feedback passes through a ReceptivityGate; ReceptivityGate references FailureTrace as its verification input. Two cycle-breaks needed during apply: FailureTrace→AcceptSpec is load-bearing (the trace is defined BY reference to the spec it violates), so AcceptSpec→FailureTrace was dropped. Same pattern for PerformanceSignal→Feedback, PerformanceSignal→PathwayMemory, PerformanceSignal→FrameError — all kept as the definitional direction, with the reverse edges trimmed.

6. *Macro coverage — Forest, GraphOfThought, and the seven missing §6 protocols.* A survey of the library's Macro-shaped patterns (69 via signature fields) found the Think(X) / Discover(X) / Check(X) / Judge(X) / Act(X) families comprehensive for primitives, but the paper's §6 "Generalized Decomposition Protocols" (ten canonical protocols) were only partially represented: PURE (PURECheck + PUREOptimization), Creation (RealizationProtocol, close), and General Problem-Solving (Solver itself). Seven were missing as dedicated patterns. Three more general gaps:
   - **`Forest`** (Infrastructure/Data Structures, Ring 1, Tier 1) — the topology of N independently-rooted trees with no shared apex. Broad-use spans random forests (ML), disjoint-set forests (union-find), process forests (OS sessions), federated solver trees across organizations (§7.2 Knowledge Sharing), and biological forests. Not a derivation of Tree — it names the multi-rooted case. Natural ancestor of any future `SolverForest` or `CognitiveCommons` pattern.
   - **`GraphOfThought`** (Mind/Reasoning, Ring 2, Tier 2, signature `Think(DAG)`) — the canonical Think(X) sibling that was missing. Complements ChainOfThought (linear), TreeOfThoughts (branching without merge), SkeletonOfThought (outline-parallel). Used when distinct reasoning branches should feed into shared intermediate conclusions — proof assistants, complex debugging, multi-hypothesis analysis. Rule-of-Explicit-Wiring note: the signature `Think(DAG)` forces the dep key `d_a_g` rather than `dag` (the validator derives dep keys from the signature's type names; multi-cap acronyms get underscore-separated).
   - **Seven §6 protocols**: `CollaborativeWritingProtocol` (§6.1, Mind/Reasoning), `HumanEmulatorProtocol` (§6.2, Mind/Reasoning), `DiscoveryProtocol` (§6.4, Mind/Strategy), `TemporalEnsembleForecasting` (§6.5, Mind/Inference), `EthicalReasoningProtocol` (§6.6, Society/Governance, caution), `TruthseekingProtocol` (§6.7, Mind/Inference), `MetaProtocols` (§6.10, Society/Governance). Each is minted with the paper's specification as the mechanism: structural phases (Generate+Reduce for Discovery), temporal ensemble architecture for Forecasting, layered epistemic decomposition for Truthseeking, is-ought separation for Ethical Reasoning, and the tree-on-the-tree structure for Meta Protocols. Rule G (gravity) forced dropping `MarginalValueRule` deps from Mind-layer protocols (MVR is Society/Economics); the prose references the rule by name without the hard template dep.

   The broad Macro audit also flagged one follow-up (not applied): **Rule F sweep** on the 64 `signature`-bearing patterns §3.12 did not touch (§3.12 covered five). Each signature should be checked against its `composes_with` backing. That's a separate, narrow pass.

This brings the audit's cumulative additions to **twenty new patterns**: Boolean, ReAttempt, FrameError, PathwayMemory, DecompositionGate, DocumentedOverride, Status, ConceptualDecomposition, PerformanceSignal, FailureTrace, ReceptivityGate, Forest, GraphOfThought, CollaborativeWritingProtocol, HumanEmulatorProtocol, DiscoveryProtocol, TemporalEnsembleForecasting, EthicalReasoningProtocol, TruthseekingProtocol, MetaProtocols. Library count: 427 − 4 retirements + 20 additions = **443 patterns**.

7. *PURE refactor — separate general concepts from the framework that composes them.* The four PURE components (`Parsimony`, `Novelty`, `Realizable`, `Expansive`) were piggybacking on PURE-specific three-state traffic-light rating semantics ("Classifies into three qualitative states: Bloated / Under-specified / Minimal"), baking application-specific usage into general concepts. Two corrective moves:

   - **Generalized the four component mechanisms.** Stripped the three-state classification and the PURE-specific evaluation logic. Each now names only the general question it asks: Parsimony asks "does the minimum-complexity form still perform its function?" (ablation discipline); Novelty asks "genuinely new mechanism relative to incumbent?" (structural comparison); Realizable asks "can this be built given stated inputs?" (recursive feasibility); Expansive asks "does it transfer beyond its origin domain?" (hostile-domain probe). Specific rating semantics (binary, traffic-light, scalar) now belong on descendants or on the composing protocol.
   
   - **Minted `PURE`** (Mind/Strategy, Ring 1, Tier 1) — the protocol that wires the four general components into a viability evaluation. Captures the three load-bearing properties from FI §6.3: *orthogonality* (the four dimensions must be evaluated without sight of each other because in a single context the faculties corrupt each other), *non-compensation* (no axis can offset another; explore iff no gate is Red), and **variable-depth-is-definitional** (a PURE instance is a five-second screen or a week-long investigation; same protocol at different depths, governed by marginal-value economics). PURECheck, PUREOptimization, and PUREBrainstorming are reframed as points on the depth continuum of this framework (lightweight triage, deep optimization, quality-filtered ideation), not as independent protocols — they now `references PURE` and inherit the framework's semantics rather than restating them.
   
   - **Realizable and Expansive relocated Society/Protocols → Mind/Reasoning.** These are Judge(Value) patterns — cognitive evaluations, not coordination primitives. Society/Protocols was an artifact of their original minting context. Mind/Reasoning matches Parsimony and aligns with the principle that *layer follows mechanism domain, not application domain* — a cognitive evaluation is Mind regardless of whether its outputs feed organizational decisions.

   A Rule G (layer gravity) tension surfaced during apply: an earlier draft had PURE in Society (since viability evaluation often applies at organizational decision points), which would depend on Mind components. A brief discussion clarified the right principle, now adopted as the library's canonical layer-assignment rule:

   > **Layer = the minimum number of agents the mechanism structurally requires**, not the domain of application.
   > - Physics / Infrastructure: pre-cognitive, no agent required
   > - Mind: 1 agent suffices (even if application usually involves more)
   > - Society: ≥2 agents required by the mechanism itself
   
   The principle is *operationalizable*: you count agents, you don't interpret "domain." Under it, PURE is Mind — one agent can evaluate viability. The fact that its output often feeds organizational decisions is an *application*, not the mechanism. A Mind pattern can think *about* societal topics without being a Society pattern.

8. *Three relocations from Society → Mind under the agent-count principle.* Applying the rule articulated in §3.21.7 revealed three patterns miscategorized:
   - **`EthicalReasoningProtocol`** (Society/Governance → Mind/Reasoning). The mechanism is is-ought separation via typed boundaries — one agent can do this internally. Auditability is a benefit of the mechanism, not a requirement; the mechanism itself is single-agent.
   - **`MetaProtocols`** (Society/Governance → Mind/Strategy). "Solvers that operate on the solver tree itself" — self-regulation. In a single-agent deployment, one solver can observe its own tree topology and emit reframe signals. The multi-agent case is an application, not the mechanism requirement.
   - **`MarginalValueRule`** (Society/Economics → Mind/Strategy). "Deepen iff expected improvement / incremental cost > threshold" is single-agent rationality — one mind asks whether to keep thinking. Society/Economics conflated cognitive-economics-of-one-agent with multi-agent economic coordination. Under the agent-count principle it's clearly Mind.

   Cascading benefit: three Mind-layer protocols (CollaborativeWriting, HumanEmulator, Truthseeking) had `MarginalValueRule` deps dropped earlier solely because Rule G flagged Mind→Society as a violation. With MVR now in Mind, those deps are restored and the `{{marginal_value_rule}}` template is re-integrated into their mechanisms. The graph is tighter.

This adds PURE as the **twenty-first new pattern**: library count 427 − 4 retirements + 21 additions = **444 patterns**.

9. *Society → Mind layer sweep under the agent-count principle.* With the principle articulated in §3.21.7, a systematic scan of all 127 Society patterns (via mechanism-text signal analysis: single-agent indicators like "the agent", "self-", "introspect" vs multi-agent indicators like "agents", "peers", "broadcast", "consensus") flagged 14 suspicious cases. After case-by-case evaluation against the strict agent-count rule, **eleven relocated Society → Mind** in two waves:

   **Wave 1 — six clean single-agent mechanisms** (no hard-dep entanglement):
   - `CapacityPressure` (Society/Economics → Mind/Strategy) — self-imposed resource constraint to force abstraction; 1 agent.
   - `CiteBack` (Society/Protocols → Mind/Reasoning) — single-agent citation discipline ("the agent is forbidden from stating a fact unless it can generate a pointer").
   - `CurriculumReplay` (Society/Protocols → Mind/Memory) — self-distillation on own past outputs; 1 agent.
   - `HackDetect` (Society/Protocols → Mind/Inference) — self-detection of "make it work" vs "do it right" shortcut-taking; 1 agent introspecting.
   - `LivedProof` (Society/Economics → Mind/Reasoning) — epistemic structure where the process IS the evidence; 1 agent.
   - `WorldReversible` (Society/Protocols → Mind/Strategy) — single-agent design constraint ("every action must be perfectly invertible").

   **Wave 2 — five-pattern cascade** (entangled via hard deps):
   - `ProblemFramer` (Society/Coordination → Mind/Strategy) — one agent can frame its own problem; no Society hard deps.
   - `LocalizedLearning` (Society/Protocols → Mind/Memory) — one agent can route feedback to its own per-manifest memory slots; no Society hard deps.
   - `FractalIntelligence` (Society/Protocols → Mind/Strategy) — per FI §4.4 "One agent, many Solvers" is legitimate; the mechanism is substrate-agnostic recursion, not inherently multi-agent. Moved after ProblemFramer + LocalizedLearning cleared, so its full hard-dep set now resolves to Mind or Infrastructure.
   - `RootSolver` (Society/Governance → Mind/Strategy) — apex triage + PathwayMemory dispatch is single-agent-capable. Its only hard dep is PathwayMemory (Mind).
   - `CommitmentDevice` (Society/Protocols → Mind/Strategy) — the general Ulysses-pact mechanism is single-agent self-binding. Multi-agent cryptoeconomic slashing (validator bonds, etc.) is a specialization, not the foundation.

   **Five patterns flagged as stay-in-Society** (mechanism genuinely ≥2 agents): `AgentSandbox` (sandboxer + sandboxed roles distinct), `ConfusedDeputy` (3-party: agent + principal + caller), `Gardener` (stigmergy → requires shared substrate with others), `MemeticSeed` (broadcast to neighbors), `WorldTransparent` (transparency presupposes public observers).

   **Graph effect**: Mind went 155 → 178 (+23 across all agent-count cleanup), Society went 130 → 116 (−14). Pattern hashes are unchanged because layer/category are unhashed `_meta` fields; the vocabulary root `747a1eaf8451a0921df94bb9198b23dd83d527cf1ab23ad472feb74aed4e6001` stays the same. The layer-assignment principle surfaces where the library's soul actually lives.

   **Follow-up noted**: the remaining 116 Society patterns were not individually re-evaluated; this sweep targeted obvious single-agent-indicator mis-fits. A full agent-count audit of every pattern across all four layers is a separate pass — picked up in §3.21.10.

10. *Principle tightened from "agent count" to "mechanism sufficiency"; spec lifted into `docs/core/philosophy.md §3.1`.* After §3.21.9 applied the agent-count rule across the Society layer, a subsequent discussion (Gemini Round 6 sign-off + a review exchange on MVR's adversarial exposure) sharpened the rule. The final articulation — now the canonical layer-assignment test in `docs/core/philosophy.md §3.1` — replaces agent-counting with the **mechanism-sufficiency test**: the axis is what the mechanism *structurally requires to execute*, not what it is typically used for.

    | Layer | Tight definition | Test question |
    |---|---|---|
    | Physics | Substrate that obtains regardless of any author | "Does this exist whether or not anyone thinks about it?" |
    | Infrastructure | Authored structures/operations, no cognition required | "Can a program execute this without making any judgment?" |
    | Mind | Cognition sufficient (single agent) | "Does this require a knower to make a call that cannot be reduced to schema-matching? Can a single isolated agent execute it?" |
    | Society | Mechanism structurally requires ≥2 independent parties | "Does the mechanism structurally require another party whose state is outside this agent's control?" |

    **Key refinement**: vulnerability-to-adversarial-inputs ≠ structural-requirement-of-adversarial-parties. MarginalValueRule is vulnerable to false estimates when deployed in adversarial multi-agent solver trees, but the *mechanism* (ratio test `E[improvement]/C > θ`) executes fine on internal Pathway Memory. Adversarial hardening composes *around* MVR via Society-layer guards (ReceptivityGate, FailureTrace, signed Consult). This distinction — mechanism vs. deployment — is what keeps the rule operationalizable without collapsing into "everything is eventually social."

11. *Gemini Round 6 follow-up — three additional Society → Mind moves.* Gemini's R6 review identified three patterns that survived the §3.21.9 sweep but fail the N=1 test on inspection:

    - `EmpathySim` (Society/Economics → Mind/Strategy) — theory-of-mind simulation is one mind imagining another; no network call or peer agent required by mechanism.
    - `DogfoodFirst` (Society/Economics → Mind/Strategy) — creator-as-user validation is single-agent self-validation.
    - `SourceEvaluate` (Society/Protocols → Mind/Inference) — one agent reading a document and judging its author's credibility is an internal cognitive act.

    Each fails the mechanism-sufficiency test cleanly and was moved. Mind went 178 → 181; Society went 116 → 113. Pattern hashes unchanged.

12. *Full-sweep annotation — `audits/2026-04-17/layer-assignment.md` + 25 additional proposed moves.* With the tight test locked, a complete classification pass across all 444 patterns produced `audits/2026-04-17/layer-assignment.md`: every handle, the proposed layer, and a one-line mechanism-sufficiency reason. Generated by reading each mechanism text and applying the four test questions.

    **25 additional proposed moves** surfaced by the full pass (not yet applied — Round 7 review pending):

    **Physics → Infrastructure (13)** — the biggest finding: most of the current Physics layer is authored computational primitives, not substrate. The tight test is "obtains regardless of any author"; these don't.
    - `Branch`, `Compensate`, `Compress`, `Cooldown`, `EntropyPump`, `Gate`, `Heartbeat`, `Hysteresis`, `ReAttempt`, `Route`, `Sign`, `StateAudit`, `Throttle`

    **Physics → Society (1)**: `StateLock` — "two actors temporarily fuse state" is N=2 by mechanism.

    **Mind → Infrastructure (3)**: `Cache` (keyed lookup, no cognition to execute); `Rank` (deterministic sort); `Decision` (committed-choice artifact — a Noun, not a Verb).

    **Mind → Society (1)**: `Stigmergy` — the mechanism structurally requires marker + reader on a shared substrate.

    **Society → Infrastructure (2)**: `FrameSpec`, `ProtoPack` — both are typed data artifacts, not coordination protocols.

    **Society → Mind (1)**: `ManifestPlanning` — architectural planning phase is cognitive; one mind transforms FrameSpec into ExecutionManifest.

    **Infrastructure → Mind (1)**: `Budget` — the discipline of respecting a resource ceiling is cognitive; the arithmetic of tracking it is Infrastructure but the pattern names the discipline. *Borderline — flagged for Gemini review.*

    **Post-hoc reasoning corrections** (retractions on inspection):
    - `TriGate`: initially flagged as Society on the basis that PURECheck uses it at "governance seams." Corrected: application context is not mechanism. TriGate is a three-state authored gate primitive (Red/Yellow/Green), mechanically a threshold classifier with N=1 — belongs in **Infrastructure/Primitives** alongside Gate.
    - `Protocol`: initially flagged Infrastructure → Society because the gloss says "communication standard between agents." Retracted on inspection: the pattern is the *spec* (rules + formats), a Noun/data artifact. One agent can read a Protocol's spec without any counterparty. HTTP, TLS, OAuth, MCP, hardware bus protocols — the *spec* is general; *using* the protocol requires ≥2 agents but that's application, not mechanism. → **Stays Infrastructure/Data Structures**.
    - `OathBind`: initially flagged Infrastructure → Society because I read "actor + enforcer." Retracted on inspection: the enforcement is code/substrate (cryptographic rule-set binding runs automatically once committed). One agent can oath-bind to a rule-set they themselves or the substrate enforces — Ulysses pact at protocol level. → **Stays Infrastructure/Verification**.

    Both Protocol and OathBind are good examples of the drift-to-Society trap: "between agents" in a gloss often describes application context, not mechanism requirement.

    **Projected distribution after applying the 23 remaining moves**:
    - Physics: 23 → **9** (substantial contraction; Physics becomes pure substrate)
    - Infrastructure: 127 → **145** (+18)
    - Mind: 181 → **179** (net −2, as some Mind patterns are mechanical data)
    - Society: 113 → **111** (net −2; Society loses FrameSpec/ProtoPack/ManifestPlanning; gains StateLock/Stigmergy)

    These moves are staged for Round 7 review before application. The annotated layer-assignment.md is the diff-able artifact.

**Schema tightening (data_schema additions).**
- `Belief.confidence` — the §3.10 schema pass covered Score/Summary/Probability but not Belief. Broad-use (#2) notes `Belief.confidence` is principled `[0, 1]` Probability — should be declared as such in Belief's data_schema, not just in prose. Add `confidence: {type: "number", minimum: 0, maximum: 1}` to Belief's schema.

**Composition edges (declare deps already used via template).**
- `Hysteresis` → `composes_with: dampen` (broad-use #11 — mechanism uses `{{dampen}}`).
- `PhasedRefinement` → ensure `references: aesthetics` survives the Society→Infra move of Aesthetics (broad-use #39).
- `Correlation` → `references: causation` — I dropped this during apply to break a cycle (§6.2). Broad-use (#34) notes the topological distinction is definitional: Correlation is the *absence* of a causal edge. The back-reference belongs; the cycle was an artifact of Causation also referencing Correlation by template. The fix is to break Causation→Correlation (remove Causation's `{{correlation}}` template mention, keep Correlation→Causation), not the other direction. Flip the cycle-break.

**Methodology discipline — formalize the two failure modes.** The broad-use analysis surfaces two systematic failure modes that every future minter should guard against (captured at the end of the companion doc):

1. **Domain Overfitting.** A minter imagines use-cases from only one paradigm and bakes domain-specific constraints into the foundation. Caught in the walk: `Lock` overfit to Mutex (K=1), `ExploreExploit` overfit to UCB, `Stigmergy` overfit to biological decay. *Defense*: force the broad-use enumeration to span at least three orthogonal domains before deriving the intersection — typically biological + silicon + psychological/social. If a proposed constraint only holds in one domain, it belongs on a descendant.
2. **Semantic Homonym (Empty Intersection).** Two domains use the same word for different causal structures (mathematical `Group` vs sociological `Group`; category-theoretic `Category` vs biological `Category`). The intersection produces either a vacuous chimera or nothing at all. *Defense*: Rule E's non-vacuous schema requirement is the self-correcting backstop. **Empty intersection = the pattern is an illusion and must be split or retired.** Exactly what forced `Group` and `Switch` into retirement in §3.9.

These two failure modes generalize beyond this audit — they are the anti-patterns any broad-use walk must test for.

**Deferred follow-up items (not applied in this pass).** Six items from the broad-use analysis are genuine but require design input that exceeds audit scope:
- MarginalValueRule/ComputeBudget composition semantic (#14) — should they `composes_with` each other? Requires design call, not a mechanical fix.
- LivedProof mechanism breadth (#15) — currently framed around rhetorical/epistemic contexts; broadening to "commit history IS the argument" needs a careful rewrite.
- Anomaly/Incongruity cross-reference (#55) — subtle semantic distinction. Worth a dedicated rewrite pass, not a blind edge-add.
- RigorousSolver mechanism could name Probe/SocraticLoop explicitly (#7) — §3.14 already has the deps via `{{probe}}`/`{{socratic_loop}}` templates; tightening the mechanism prose is a polish pass, not a scoped audit item.
- Act invariants "potentially reversible" weakness (#5) — current invariants pass broad-use; "potentially reversible" reads as marker not invariant, but descendants work. Leave as-is.
- RootSolver `composes_with: pathway_memory` already added in §3.14 hand-apply (#8 was already captured; note RootSolver is the post-rename handle).

---

## 4. What we are *not* changing in this pass

Several findings surfaced during the audit but are out of scope for this round — either because the fix requires broader input, because the change would ripple too widely for a single audit pass, or because the pattern reads as intentional even if it's structurally unusual.

**Agent's layer placement.** Agent currently lives in Mind/Strategy. Arguments exist for moving it to Society (agents are coordination participants) or Infrastructure (agents are capability containers). We leave it in Mind because the mechanism describes a cognitive loop (observe → think → act), which is the defining activity of the layer. Revisiting Agent's placement would ripple into dozens of downstream patterns; it should be its own decision.

**Broader reference-density pass.** §3.20 discharges the Ring-0 wiring debt §3.7 named (eighteen edges added to surface previously-orphan foundations). A *full* reference-density pass would go further: scan every pattern's mechanism for template-syntax references (`{{x}}`) that aren't backed by a declared dependency; cross-reference sibling patterns within a family (e.g., decision-under-constraint: OptimalStop/Satisfice/Prioritize); declare descendant→ancestor lineage chains beyond the handful Step §3.5 wires (classical reasoning canon). The `scripts/audit/audit_unlinked_mentions.py` pass currently surfaces 348 patterns with handle-name mentions that aren't rendered as `{{foo}}` templates — that catalog is the starting point for this follow-up. Separate pass from this audit.

---

## 5. Review summary

This audit is focused on making the foundation more scalable to build on. It was produced in two phases: an **axis-based first pass** (§3.1–§3.17) where each section ran a targeted query across all 427 patterns and returned every match, and a **manual second pass** (§3.18) where the 243 patterns not explicitly touched by the axis queries were read individually for content-quality issues the queries couldn't catch. The changes fall into four buckets:

**Semantic quality** — §3.1 through §3.9 address coherence failures, layer misplacements, redundancy, vague boundaries, dangling wiring claims, orphan anchors, ring mis-assignments, and taxonomy imbalance. These are the "did we build the right primitives in the right places" concerns.

**Spec compliance** — §3.10 through §3.13 address gaps the initial content audit didn't reach: vacuous `data_schema` on Nouns (Rule E), Verb/Noun category squatting (taxonomy), phantom `signature` claims without `composes_with` backing (Rule F), and verification-stack `yields` contracts (naming.md §1).

**Architecture alignment** — §3.14 aligns the Solver family with the Fractal Intelligence v3 paper's crystallized five-surface contract (Manifest, Execute, Consult, Verify, Feedback), the Task→Result transaction schema, and the directed-graph nature of the Universal Solver Tree. This is the largest single source of structural drift in the library: the solver patterns were minted before the contract was pinned down, and the paper v3 is now the canonical reference.

**Hygiene** — §3.17 (the 54 unspecified parameter ranges) and §3.9 (three retirements: Group, Switch, AbductiveLeap) reduce noise in the namespace. §3.16 adds a topological CI check for Rule G (dependency direction) that catches violations the current point-checks miss. §3.15 adds `_meta.caution` to seven additional patterns (OptimisticSolver, TimeWarpLog, Compensate, Abduction, plus the three new patterns ReAttempt, PathwayMemory, DocumentedOverride that shipped with cautions from mint).

**Manual-sweep cleanup** — §3.18 addresses drift the axis-based queries could not detect: twenty Society-layer relocations (substrate-level and single-agent-cognitive patterns filed as Society/Protocols by default), three topology-category unifications, one additional retirement (Linear merged into Chain), two more Noun/Verb mechanism rewrites, sixteen additional gloss rewrites, four trait-conversions (Meta/Global/Subject/Creative), and formal supersession metadata (`_meta.supersedes`) added to three successor patterns so retirements redirect cleanly for downstream consumers of prior vocabularies.

**Audit self-review — over-specification pulled back** — §3.19 steps back and checks the audit's own additions against the same over-specification principle that reshaped §3.17. Four additions are loosened: EntropyPump's new invariants are dropped entirely (they forbid legitimate descendants like ChaosMonkey); Budget's "monotonic allocation" invariant is dropped (keeping only "conservation"); Task's `acceptance_criteria` and `budget` move from required to optional fields in the data_schema (ExplorationTask and UnboundedTask are legitimate descendants); Result's `outputs` becomes optional (failed Results legitimately have no outputs). The discipline going forward: every foundation-level invariant must be definitional, not prescriptive.

**Ring-0 reference wiring** — §3.20 discharges the wiring debt §3.7 deferred: eighteen new `references` edges added across five Ring-0 foundations (Cache, LatentAttachment, ContextFirst, MonotonicCounter, CommitmentDevice), surfacing the actual usage that was previously only in prose. The sixth Ring-0 foundation (AnchorDrop) has no confirmed caller yet and remains unwired rather than force-connected.

**Broad-use follow-ups** — §3.21 promotes the 66 items surfaced in the companion `2026-04-broad-use-analysis.md` into explicit audit commands. Most validate §3.1–§3.20 decisions; a subset produced new commands that the axis-based queries did not catch: four layer/category corrections (Monitor, Tension, Reversibility, Critique), two tier corrections (Ballot T3→T1, Context T3→T1), two mechanism rewrites (Audit Verb→Noun, DissentSeek post-§3.1 update), one handle rename (CognitiveSolver → PolymorphicSolver with supersedes, per broad-use #14 — the pattern is about contract conformance across substrates, not cognition), one schema tightening (Belief.confidence as principled Probability), three declared-edge additions (Hysteresis composes_with Dampen, PhasedRefinement ref survival, Correlation→Causation cycle-flip), and two formalized methodology failure modes (Domain Overfitting, Semantic Homonym) that every future minter should guard against. Six items are explicitly deferred as requiring design calls rather than mechanical fixes.

Five rounds of independent review shaped the audit. **Round 1** corrected the first-pass findings: Lock/Mutex should use `derived_from` for inheritance rather than `composes_with` (which is reserved for active subroutine invocation), and ScoringFunction should be wired via `accepts` rather than `composes_with` because it's a Noun read by callers, not a Verb they delegate to. **Round 2** (focused on §3.14) produced four refinements and flagged a missing architectural piece: `RigorousSolver`'s mechanism was rewritten to encode the ceremony inline rather than referencing an off-graph "Level 4" concept (Self-Contained Principle, §2.E); `OptimisticSolver` was kept in Society/Protocols rather than relocated to Mind/Strategy, because relocating would have inverted Rule G given its `composes_with AtomicBid` dependency; `FrameError` was moved from Physics/Primitives to Mind/Reasoning (lateral reframing is cognitive, not substrate-level); `FourTests` was renamed for Naming Morphology (§2.C) compliance; and `DocumentedOverride` was added as the supervised hard-seam exit valve. **Round 3** made three further corrections that kept the taxonomy clean: (a) the renamed `DecompositionCheck` was renamed again to `DecompositionGate`, because a `Check` yields a `Status` per the verification-stack taxonomy (§3.13) while the four-test suite's admit/reject semantics are Gate semantics; (b) the proposed `RoutingGate` was retracted entirely — Gemini correctly flagged that a pattern named `Gate` yielding a `Route` corrupts the naming types, and that an Infrastructure-layer pattern can't `composes_with` Mind-layer `PathwayMemory` under Rule G — the hard-seam actuator should use the compositional path `Gate → Decision{FrameError} → (Route | Reframe)` with no new primitive required; (c) `AcceptSpec`'s mechanism was updated to declare it yields `FrameError` on non-compensatory failure rather than generic false, because without that type declaration the FrameError signal has no guaranteed structural origin point. **Round 4** (focused on §3.18) made three further refinements: (a) `Linear` retires into `Chain` rather than `Sequence`, because Sequence is temporal ordering while Linear and Chain are both spatial topologies; (b) `Deep` and `Nature` are retained as full canonical patterns rather than trait-converted, because the Fractal Intelligence paper's Grammar of Agency specifies them as foundational Ring-0 Verb and Noun respectively (trait conversion now covers only Meta/Global/Subject/Creative); (c) all retirements carry `_meta.supersedes` metadata pointing at the old `sema_id`, so downstream consumers of prior vocabularies can redirect cleanly rather than encounter dangling references. **Round 5** resolved the last open structural question and cleared apply: (a) `AcceptSpec` is a Noun and therefore cannot itself declare `yields` — the hard-seam outcome type declaration belongs on the consuming Verb (the `Verify` surface that reads the AcceptSpec and emits `Solution | FrameError`). This split preserves the Noun/Verb discipline while keeping the type-enforced hard-seam semantics intact. (b) The apparent `Broad` gap (sibling to `Deep`) is a naming illusion — the paper's Grammar of Agency names the horizontal-breadth primitive `Discover`, not `Broad`; no mint needed. Sign-off was granted at the end of this round.

Additions to the library:
- `ReAttempt` (Physics/Primitives) — the substrate-level re-try primitive that splits cleanly from Retry when Retry moves to Mind/Strategy
- `Boolean` (Infrastructure/Data Structures) — needed to close the Validate-yields-Boolean gap
- `FrameError` (Mind/Reasoning) — typed failure signal for lateral reframing at hard seams
- `PathwayMemory` (Mind/Memory) — learned-routing memory used by RootSolver and any dispatching Solver (wired via `composes_with` on PolymorphicSolver and OptimisticSolver too, per §3.21 gap-2 fix)
- `DecompositionGate` (Mind/Reasoning, Ring 2) — the Necessity/Independence/Universality/Completeness decomposition test suite; yields a Decision
- `DocumentedOverride` (Society/Governance) — the override-with-documentation safety valve at hard seams, cryptographically logged via TimeWarpLog
- `Status` (Infrastructure/Data Structures) — surfaced during apply when §3.13 declared `Check` yields `Status` but no such pattern existed; enum {Verified, Falsified, Unknown}
- `ConceptualDecomposition` (Mind/Reasoning, Ring 1) — the FI-core activity of breaking a concept into solver-contract-bound sub-concepts, distinct from generic Decompose by the explicit contract-binding requirement (§3.21 solver-family completion)
- `PerformanceSignal` (Infrastructure/Data Structures, Ring 0) — Feedback-surface output artifact per FI Table 4; the typed signal that feeds PathwayMemory and drives localized learning (§3.21 FI Table 4 gap)
- `FailureTrace` (Infrastructure/Data Structures, Ring 1) — structured, signed proof of which AcceptSpec clause an artifact violated; required by ReceptivityGate (§7.1)
- `ReceptivityGate` (Society/Protocols, Ring 1) — guards the Feedback surface against poisoned or hallucinated rejection signals; validates incoming FailureTraces before absorbing them into PathwayMemory (§7.1)
- `Forest` (Infrastructure/Data Structures, Ring 1) — topology of N independently-rooted trees with no shared apex; ancestor of federated-commons constructs (§3.21 macro audit)
- `GraphOfThought` (Mind/Reasoning, Ring 2, signature `Think(DAG)`) — missing Think(X) sibling for DAG-structured reasoning (§3.21 macro audit)
- `CollaborativeWritingProtocol`, `HumanEmulatorProtocol`, `DiscoveryProtocol`, `TemporalEnsembleForecasting`, `EthicalReasoningProtocol`, `TruthseekingProtocol`, `MetaProtocols` — the seven missing FI §6 Generalized Decomposition Protocols (§3.21 macro audit)

Everything else is rewrites, re-categorizations, re-wirings, or retirements of existing content.

The net effect is a vocabulary where every name carries distinct, constraining semantic content, where layer assignments reflect mechanism content, where the dependency graph reflects the relationships the mechanisms claim, where parameters represent real identity variation rather than forgotten todos, where the four core verification primitives have enforced output contracts, and where the Solver family matches the Fractal Intelligence v3 specification — including the hard-seam semantics, which are now actualizable through the existing `Gate` + `Route`/`Reframe` composition once `AcceptSpec`'s mechanism declares it yields `FrameError` on non-compensatory failure, plus the `DocumentedOverride` safety valve for supervised seam exit.

The library count changes: first pass (427 − 3 retirements + 6 additions = 430); the second-pass manual sweep added one retirement (Linear merged into Chain); the apply surfaced one more addition (Status); §3.21's solver-family completion added ConceptualDecomposition; §3.21's FI-Table-4 gap closure added PerformanceSignal, FailureTrace, ReceptivityGate; §3.21's macro audit added Forest, GraphOfThought, and the seven §6 protocols (CollaborativeWritingProtocol, HumanEmulatorProtocol, DiscoveryProtocol, TemporalEnsembleForecasting, EthicalReasoningProtocol, TruthseekingProtocol, MetaProtocols); net = **443 patterns**. The sweep's primary effect is not count change but systematic cleanup: twenty Society-layer relocations, three topology-category unifications, two Noun/Verb mechanism rewrites, sixteen gloss rewrites, four trait-conversions (Meta/Global/Subject/Creative), and retention of Deep and Nature as canonical Ring-0 primitives per the Fractal Intelligence paper's Grammar of Agency — yielding a library that's substantially more internally consistent than it was at the start and cleanly tied to the v3 canon.

---

## Appendix A — Parameter dispositions (54 parameters across 35 patterns)

Three categories per §3.17.

### 1. Principled bounds — specify the range at foundation

Value is mathematically or structurally bounded; no descendant can legitimately extend outside. Seven parameters.

| Pattern | Parameter | Disposition |
|---|---|---|
| Belief | confidence | `type: Probability, range: [0.0, 1.0]` |
| CapacityPressure | compression_ratio | `type: Ratio, range: [0.0, 1.0]` |
| CapacityPressure | resource_type | `enum: {Compute, Memory, Attention, Budget}` |
| CounterfactualAnchor | retention_policy | `enum: {Snapshot, Rolling, Permanent}` |
| HumanApprove | challenge_required | `type: Boolean` |
| OptimalStop | recall_allowed | `type: Boolean` |
| MintWhenFriction | min_compression | `type: Ratio, range: [0.0, 1.0]` |

### 2. Leave open for descendants — declare the slot, keep `range: "unspecified"`

The parameter exists in the pattern's identity (so descendants can inherit and specialize it), but type and range are deliberately open. Mechanism text carries the semantic. Descendants mint specialized variants (e.g., `LegalReview derived_from HumanApprove with timeout: Duration, range: [1d, 90d]`) as their context requires. Nineteen parameters.

Each entry gets `range_note: "parameterized; specialize via derived_from"` added as unhashed metadata, so future auditors understand the slot is intentionally general, not lazy.

| Pattern | Parameter | Why open |
|---|---|---|
| CircuitBreaker | reset_timeout | simple retries: ms; batch pipelines: days; human-loop: variable |
| CounterfactualAnchor | granularity | sub-frame gaming: ns; archaeological records: years |
| Crystallize | resonance_period | micro-resonance: ms; quarterly institutional patterns: months |
| DogfoodFirst | duration | quick feature test: hours; year-long tool adoption |
| HumanApprove | timeout | test mocks: ms; legal review: weeks; vacation windows: days |
| Kairos | window | high-frequency trading: ms; geopolitical decisions: years |
| Monitor | interval | high-freq metrics: µs; quarterly audits: months |
| OutputGuard | scan_timeout | simple regex: µs; LLM-based content scan: minutes |
| Rally | deadline | emergency coordination: seconds; research collaboration: years |
| ComputeBudget | max_budget | test runs: tens; datacenter-scale: billions |
| GracefulDegradation | max_def_size | small config: dozens; large definitions: millions of tokens |
| OptimalStop | total_budget | quick decisions: handful; production search: millions |
| Proprioception | max_recursion_depth | shallow introspection: 3; deep self-modeling: 100+ |
| Rally | max_participants | pair coordination: 2; global swarms: 100K+ |
| Reversibility | cost_limit | trivial actions: pennies; industrial operations: millions |
| SpectralTune | context_chunks | small context: handful; long-context models: 10K+ |
| Tree | breadth | binary: 2; beam search: 50; decision tree: millions |
| TreeOfThoughts | breadth | small ensemble: 3; research prototype: 20+ |

### 3. Drop to `accepts` — not really a parameter

The value is caller-supplied at runtime, not a configuration of the pattern's identity. Moves out of `parameters` entirely. Eighteen parameters.

| Pattern | Parameter | Disposition |
|---|---|---|
| Aggregate | weights | → accepts (Vector input) |
| Belief | evidence | → accepts (Context input) |
| Card | proof | → accepts (optional proof input) |
| Critique | criteria | → accepts |
| DeliberativeAlign | constitution_ref | → accepts (Constitution input) |
| DogfoodFirst | output_artifact | drop — yielded output, not input |
| EmpathySim | target_profile | → accepts (Agent input) |
| InvariantFilter | predicates | → accepts (RuleSet input) |
| Judge | criteria | → accepts (see §3.1) |
| Monitor | threshold | → accepts |
| NormativeJudge | weights | → accepts (Vector input) |
| OsmoticFilter | accepted_solvents | → accepts (Criteria input) |
| ParetoFront | axes | → accepts (Criteria input) |
| PromptChain | steps | → accepts (structural input) |
| Rally | selection_criteria | → accepts |
| Responsibility | escalation_path | → accepts (structural input) |
| SacrificialProbe | failure_mode | drop — observation, not parameter |
| Solution | cost_incurred | drop — yielded output |
| Reversibility | cost_limit | specify `[0, 1000]` (abstract units) |
| SpectralTune | context_chunks | specify `[1, 100]` |

Scattered in other layers (9 further instances) follow the same pattern: specify if a meaningful range exists, drop if the "parameter" is really an input or output.

## Appendix B — Scope limits

- The 114 patterns in Society/Protocols were scanned for handle-similarity clusters and Ring-0 orphans rather than deep-read individually. Pattern-by-pattern quality beyond those checks is not represented here.
- Parameter *defaults* were not systematically audited, only *ranges*.
- The audit did not cross-reference the vocabulary against `data/vocabulary/` YAML source files — the DB was treated as authoritative per `docs/guides/authoring.md`.
- The audit did not perform behavioral testing on any pattern.

---

## 6. Post-apply — what actually happened during execution

The audit was executed against `data/vocabulary/` in two passes. An initial scripted apply (first pass) produced a mechanically correct but stylistically degraded result — the template-mention-in-text requirement forced "References {{cache}}." sentences onto the tails of 50 mechanisms, which read as tooling-appended rather than authored. On review, that apply was reverted (DB + vocabulary rolled back to pre-apply state), and the audit was re-executed as a **hand-edited apply (second pass)** where every prose modification was written by hand, integrating template references naturally into existing sentences rather than appending them.

Tooling surface (second pass): no permanent apply scripts. Staging was edited in place via Read/Edit operations for prose-sensitive work; a narrow Python pass was used only for pure-metadata updates (ring, tier, layer, category, data_schema fields) where no natural-language content was touched. The rebuild path is the standard `sema apply --add data/vocabulary` after staging → vocabulary promotion and DB wipe.

Final vocabulary root after the full hand-edited apply (including §3.21 CognitiveSolver→PolymorphicSolver rename, solver-family `derived_from` chain fixes, PathwayMemory wiring on dispatching solvers, Solver mechanism rewrite for role-bearing/construction framing, ConceptualDecomposition mint, FI-Table-4 mints PerformanceSignal/FailureTrace/ReceptivityGate, §6 protocol family mint — Forest/GraphOfThought + seven §6 protocols, PURE framework mint with general-concept split, and the three agent-count-principle relocations Society→Mind for EthicalReasoningProtocol/MetaProtocols/MarginalValueRule): `sema:vocab#mh:SHA-256:747a1eaf8451a0921df94bb9198b23dd83d527cf1ab23ad472feb74aed4e6001`. Pattern count: **444**.

### 6.1 Count reconciliation

The audit targeted 429 patterns (427 − 4 retirements + 6 additions). The applied library has **434 patterns** — five more than the target. During apply, `Status` had to be minted as a seventh new pattern: §3.13's declaration that `Check` yields `Status` assumed the Status type existed, but no such pattern was in the library. Rather than downgrade Check's yield to `Boolean` (which would have collapsed its distinction from `Validate`), Status was added as a Data Structures pattern with enum values `{Verified, Falsified, Unknown}`. §3.21's solver-family completion then added `ConceptualDecomposition` (eighth new pattern) — the core FI activity. §3.21's FI-Table-4 gap closure added three more: `PerformanceSignal` (Feedback-surface output artifact), `FailureTrace` (structured proof of AcceptSpec clause violation), and `ReceptivityGate` (the gate that validates FailureTraces before absorbing them). All three are canonical per the paper; the library had the concepts in mechanism text but not as first-class patterns.

Count reconciliation:
- Start: 427
- Retired: 4 (Group, Switch, AbductiveLeap, Linear)
- Added: 7 (Boolean, ReAttempt, FrameError, PathwayMemory, DecompositionGate, DocumentedOverride, **Status**)
- End: 430

### 6.2 Cycle breaks

Five dependency cycles surfaced during the topological-mint phase, all caused by bidirectional references where the audit added a forward direction (section 3.x) and the existing graph had the back-direction embedded in mechanism text. Each cycle was broken by dropping the back-reference:

| Cycle | Break |
|---|---|
| `Tree → DAG → Parallelize → Mode → Agent → Goal → Result → Solution → Chain → Tree` | Dropped `Tree → DAG` reference (§3.6's Tree→DAG wiring sacrificed to break the longer Result/Solution/Agent/Goal chain that predates this audit) |
| `Judge → ScoringFunction → Judge/Rank` | Dropped ScoringFunction's back-references to Judge and Rank; rewrote ScoringFunction's mechanism to reference only `{{value}}` |
| `Correlation ↔ Causation` | Re-flipped per §3.21 (broad-use #34): Correlation now references Causation (the contrast anchor that defines Correlation as the absence of a directed causal edge); Causation's mechanism was rewritten to not template-reference Correlation |
| `RootSolver → UniversalSolverTree → SolverTree → RootSolver` | Dropped `RootSolver → UniversalSolverTree` reference; RootSolver's mechanism describes the apex role without requiring UniversalSolverTree as a dependency |
| `HeuristicSnap → Cache → HeuristicSnap` | Dropped `Cache → HeuristicSnap` back-reference; Cache's mechanism was rewritten as a foundation-level cache definition that doesn't name any descendant |

None of these breaks affected the audit's intent. The §3.x-specified forward directions (Judge→ScoringFunction, HeuristicSnap→Cache, Correlation→Causation) are all present as graph edges. The Tree→DAG wiring from §3.6 was the one casualty — a follow-up mint that closes the Result/Solution/Chain chain at a different point would allow it to be restored.

### 6.3 Retirement reference cleanup

After §3.9 + §3.18 retirements, six patterns in the remaining library still had mechanism-text or dependency references to the retired handles (Linear, Switch, AbductiveLeap, Group). These were cleaned:

- Chain had `references.linear` + `{{linear}}` in text — both removed; mechanism rewritten to describe Chain without the Linear contrast
- ContextSwitch had `signature: Switch(Context)` — signature dropped (Switch was the signature target type); mechanism rewritten to not depend on Switch concept
- ProblemFramer, SolverTree had `{{solver_root}}` template references and `references.solver_root` dependencies — renamed template to `{{root_solver}}` and renamed the dep key; forward hashes resolved to RootSolver's new sema_id

### 6.4 Deviations from the audit spec during apply

Three places where the apply substantively diverged from the section's prescription:

1. **§3.17 parameter ranges** — the audit specified a three-way disposition (principled / typed-open / drop-to-accepts). The hand-edited apply implemented all three dispositions: principled ranges landed as typed bounds, typed-open parameters got `range: "unspecified"` with the intent carried by the type (`Duration`, `PositiveInteger`) rather than by a separate `bounds_intent` field, and drop-to-accepts parameters moved structurally from `parameters` into `dependencies.accepts` with each mapped to an appropriate Noun target (Vector, Context, Criteria, Constitution, Agent, RuleSet). A handful of parameters listed for "drop to accepts" had no natural Noun target (Monitor.threshold, PromptChain.steps, Responsibility.escalation_path, Card.proof) and were dropped outright rather than force-mapped. Future work: formalize a `bounds_intent: "descendant-specialization"` field that distinguishes "intentionally open" from "lazily left blank."

2. **§3.20 Ring-0 wiring** — all 18 `references` edges added. Unlike the first scripted apply, each template-mention was integrated into the existing mechanism prose by hand. HeuristicSnap's mechanism now reads "Fast pattern matching against a {{cache}} of past experiences" as a single coherent sentence; Ballot's "amendments require a new Ballot carrying a fresh {{monotonic_counter}} sequence" is a natural continuation of the amendment clause; similar for the other 16 edges. No "References {{cache}}." tail-sentences exist.

3. **Mutex `derived_from Lock`** — unchanged from the first pass. `derived_from` remains a top-level JSON metadata field rather than a graph edge type, so the inheritance claim is captured in the JSON but is not queryable as a DAG edge. If future tooling wants to walk inheritance chains, it will need to read the top-level field rather than traverse edges.

### 6.5 Known residual issues (follow-up work)

- **Parameter range schema** — the `"unspecified"` sentinel serves both intentional extensibility and leftover laziness; a cleaner schema-level distinction would let future audits differentiate them programmatically.
- **Mutex ancestry as graph edge** — if `derived_from` should be DAG-queryable, the schema needs extending.
- **Status pattern** was added during apply without explicit audit specification; its mechanism is the drafted one (enum Verified/Falsified/Unknown) but warrants a broad-use review similar to the 427 in the companion document.
- **Post-apply audit of non-rewritten patterns**: many patterns that the audit didn't touch still carry their pre-audit glosses and mechanisms. A third pass, similar to §3.18's manual sweep, could surface additional content-quality improvements.
- **§3.21 deferred items** — see §3.21 "Deferred follow-up items" block for the six broad-use findings (MarginalValueRule/ComputeBudget composition, LivedProof breadth, Anomaly/Incongruity cross-reference, RigorousSolver mechanism tightening, Act invariant weakness, RootSolver/PathwayMemory already applied) that require design calls or dedicated rewrites rather than mechanical fixes.
- **Tree→DAG restoration** — §3.6's Tree→DAG wiring was dropped during cycle-break (see §6.2). A future mint or mechanism rewrite that severs the long Result/Solution/Chain cycle at a different point would let that wiring return.

### 6.6 Rollback

The pre-apply DB and pre-apply vocabulary are preserved:
- `data/taxonomy.db.bak` — pre-audit database
- `data/vocabulary.bak/` — pre-audit vocabulary JSONs (427 files)
- `data/taxonomy.db.bak_pre_app2` — intermediate (post-scripted-apply) database
- `data/vocabulary.bak_pre_app2/` — intermediate vocabulary

To revert to the pre-audit state: delete `data/taxonomy.db` and `data/vocabulary/`, move the `.bak` versions back, and re-run `sema apply --add data/vocabulary` if any further apply-time processing is needed. All audit-side documents (`2026-04-foundation-audit.md`, `2026-04-broad-use-analysis.md`) remain intact regardless of rollback.

### 6.7 Verification sweep against the rebuilt DB

A post-apply sweep verified the hand-edited apply landed as specified:

| Check | Result |
|---|---|
| Retirements present (Group, Switch, AbductiveLeap, Linear) | ✓ All 4 retired |
| Rename (SolverRoot → RootSolver) | ✓ Old retired, new present |
| 7 new patterns exist (Boolean, ReAttempt, FrameError, PathwayMemory, DecompositionGate, DocumentedOverride, Status) | ✓ All 7 present |
| §3.1 coherence fixes (EntropyPump, Budget, TimeWarpLog, ConfirmationBlock) | ✓ All applied |
| §3.2 layer moves (Uncertain, Retry → Mind) | ✓ Both in Mind |
| §3.5 wiring (Rank + Judge accepts ScoringFunction) | ✓ Both edges present |
| §3.7 ring re-assignments (28 patterns → Ring 2) | ✓ 28/28 correct |
| §3.8 Society/Coordination rebalance (12 patterns) | ✓ 12/12 in Coordination |
| §3.10 schema tightenings (Score, Probability, Summary) | ✓ All three restructured |
| §3.11 Noun/Verb (Check, Observe, ToolInvoke, Critique → Primitives) | ✓ 4/4 correct |
| §3.12 signature drops (ProtoPack, StateTransition, ContextCompress, StateAudit) | ✓ 4/4 signatures removed |
| §3.13 yields (Gate→Decision, Check→Status, Judge→Score, Validate→Boolean) | ✓ 4/4 YIELDS edges present |
| §3.14 Task/Result schemas, AcceptSpec mechanism, new patterns | ✓ Applied; AcceptSpec yields intentionally on Verify per Round 5 |
| §3.15 caution metadata (additions on OptimisticSolver, TimeWarpLog, Compensate, Abduction + new patterns) | ✓ All present |
| §3.17 parameter dispositions (principled / typed-open / drop-to-accepts) | ✓ All three categories applied |
| §3.18 Society → Mind relocations (14 patterns) | ✓ 14/14 correct |
| §3.18 Society → Infrastructure relocations (7 patterns) | ✓ 7/7 correct |
| §3.20 Ring-0 wiring (18 edges, prose-integrated) | ✓ 18/18 edges present; prose-integrated, no tail-appends |
| §3.21 broad-use follow-ups (Monitor/Tension/Reversibility layer, Ballot/Context tier, Audit rewrite, Correlation↔Causation flip, Hysteresis composes_with, CognitiveSolver→PolymorphicSolver rename) | ✓ All applied |

Final inventory by layer/category:
- Infrastructure/Data Structures: 85
- Infrastructure/Primitives: 33
- Infrastructure/Verification: 9
- Mind/Inference: 21
- Mind/Memory: 17
- Mind/Reasoning: 62
- Mind/Strategy: 78
- Physics/Primitives: 18
- Physics/Time: 5
- Society/Coordination: 12
- Society/Economics: 12
- Society/Governance: 9
- Society/Protocols: 83
- **Total: 444**

By Ring: 148 / 146 / 150 (R0/R1/R2). Additions distributed across all three rings — Forest and GraphOfThought at R1/R2, the seven §6 protocols at R2, PURE at R1, PerformanceSignal at R0.
By Tier: 9 / 304 / 125 / 6 (T0/T1/T2/T3). The T3 count dropped from 8 → 6 because §3.21 moved Ballot and Context from Tier 3 to Tier 1 per broad-use findings #4 and #47.

**Layer-assignment principle adopted** (§3.21.7): *layer = minimum number of agents the mechanism structurally requires*. Operationalizable: count agents, don't interpret application domain. Applied via two waves in §3.21.8 (three new mints: EthicalReasoningProtocol, MetaProtocols, MarginalValueRule) and §3.21.9 (the Society sweep: 11 additional relocations across two sub-waves — six clean single-agent mechanisms, then a five-pattern cascade unblocked by moving ProblemFramer/LocalizedLearning). Total Society-to-Mind movement across the audit's final round: **14 patterns**. Society size: 130 → 116. Mind size: 155 → 178. Pattern hashes unchanged (layer is unhashed metadata).
