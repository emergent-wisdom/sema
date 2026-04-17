# Broad-use analysis — April 2026

**Companion to `2026-04-foundation-audit.md`.** Where the main audit decides what to change, this document validates the methodology — the §3.19 "broad-use test" — by walking it through twenty representative patterns.

**Method per pattern**:
1. **Intended use** — the canonical scenario the pattern was minted for.
2. **Future use** — other legitimate scenarios it might reach.
3. **Broad-use contexts** — the enumerated range of situations the pattern must cover.
4. **What every context needs** — the intersection → foundation-required fields/invariants.
5. **What varies** — descendant-specialization territory.
6. **Extension pattern** — examples of `derived_from` descendants.

Sample spans Physics (2), Infrastructure (5), Mind (7), Society (6); rings 0–2; tiers 0–2; Nouns and Verbs.

---

## 1. `Solver` · Mind/Strategy · R0T0

**Intended**: abstract transformer of Task to Solution; root of the solver family.
**Future**: any process conforming to the Task→Solution contract — LLM calls, human workers, distributed agents, composite pipelines, MCP tools, code interpreters, manual workflows.
**Broad-use contexts**: above.
**Every context needs**: accepts a typed Task; exposes the five-surface contract (Manifest, Execute, Consult, Verify, Feedback) with Manifest+Execute mandatory.
**Varies**: cognitive mode, rigor level, execution substrate, budget discipline, feedback shape.
**Extension**: `CognitiveSolver`, `RigorousSolver`, `OptimisticSolver`, `RealizationSolver` via `derived_from Solver`.

## 2. `Task` · Infrastructure/Data Structures · R0T1

**Intended**: the atomic unit of intent; input to a Solver.
**Future**: any executable intent artifact — solver invocations, user requests, workflow steps, experiment plans, test cases, research queries, exploration prompts, CI jobs, even manual to-do items.
**Broad-use contexts**: above.
**Every context needs**: `operation` (what), `inputs` (to what), `acceptance_criteria` (when done). Without acceptance_criteria the caller cannot close the transaction — definitional for Task-ness.
**Varies**: `budget` (optional — UnboundedTask doesn't carry one), holographic-inheritance strictness, parent linkage, retry semantics.
**Extension**: `BoundedTask` (adds budget required), `ExplorationTask` (redefines acceptance), `ChildTask` (adds holographic inheritance enforcement).

## 3. `Gate` · Physics/Primitives · R0T1

**Intended**: condition-based payload filter.
**Future**: any checkpoint in a process where progress is conditional.
**Broad-use contexts**: permission gates, validation gates, acceptance gates, release gates, quality gates, rate-limit gates, security gates, sanity checks, A/B cohort selection.
**Every context needs**: a condition slot (type varies); yields `Decision` (proceed/halt per §3.13 verification-stack taxonomy).
**Varies**: condition evaluator type, drop behavior, side-effects on drop, blocking vs. non-blocking, timeout, logging.
**Extension**: `SecurityGate`, `RateLimitGate`, `QualityGate`, `TimedGate`, `LoggingGate`.

## 4. `HumanApprove` · Infrastructure/Verification · R1T2

**Intended**: high-stakes action gating by a human operator.
**Future**: any decision needing a human judgment call.
**Broad-use contexts**: production deploys, financial transactions, legal review, compliance committees, test mocks (auto-approve with timeout), emergency auto-reject, medical approvals, policy reviews, art-moderation, publishing signoffs.
**Every context needs**: the Task presented to human, rationale, risk assessment; yields approved/rejected/timeout.
**Varies**: `timeout` (ms to weeks — see §3.17), `challenge_required` (Boolean, principled), escalation path, UX channel (email, Slack, in-app), quorum (some contexts need multiple approvers).
**Extension**: `LegalReview` (weeks timeout, committee quorum), `EmergencyApprove` (sub-second timeout, auto-reject default), `TestMockApprove` (auto-approve in test).

## 5. `Lock` · Physics/Primitives · R0T1 (corrected per Gemini spot-check)

**Intended**: bounded concurrent access to a protected resource.
**Future**: any exclusion primitive where holder-count is capped.
**Broad-use contexts**: in-memory mutexes (K=1), counting semaphores (K>1), distributed locks, advisory file locks, database row locks, ReadWriteLocks (bounded shared + 1 exclusive).
**Every context needs**: acquire operation, release operation, **bounded-concurrent-holders guarantee** (K ≥ 1).
**Varies**: K (the bound), fencing tokens, reentrancy, deadlock detection, timeouts, ownership transfer, shared vs exclusive modes, wait queue discipline.
**Extension**: `Mutex` (K=1 specialization + token+fencing via `derived_from Lock`), `Semaphore` (K>1 counting), `ReadWriteLock` (shared/exclusive variant), `DistributedLock` (lease-based).
**Correction note**: an earlier sketch said "one-holder-at-a-time" as the floor. Gemini's review correctly flagged that `Semaphore` with K>1 is a legitimate descendant that violates that. The generalized floor is bounded concurrency; Mutex is the K=1 specialization.

## 6. `Tree` · Infrastructure/Data Structures · R2T1

**Intended**: branching reasoning topology.
**Future**: any branching data structure.
**Broad-use contexts**: search trees, decision trees, parse trees, filesystem hierarchies, DOM, organizational charts, solver trees, thought ensembles, tournament brackets, taxonomy trees.
**Every context needs**: root node, parent-child relation, acyclicity.
**Varies**: `breadth` (binary: 2, beam search: 50+, decision tree: millions), depth limits, node type, edge type, balance invariants, sort order, traversal order.
**Extension**: `BinaryTree`, `BTree`, `DecisionTree`, `TreeOfThoughts`, `SolverTree`, `BalancedTree`.

## 7. `Score` · Infrastructure/Data Structures · R1T1

**Intended**: a quantitative evaluation result.
**Future**: any numerical judgment artifact.
**Broad-use contexts**: model eval metrics, fitness scores, relevance ranks, aesthetic ratings, adversarial judgments, risk scores, trust scores, quality scores.
**Every context needs**: `value: number` (obvious), `normalized_range: [min, max]` (otherwise 0.7 is ambiguous — out of 1 or 10 or 100?), `metric_id: string` (otherwise "what was scored?" is unclear). All three are usability floor.
**Varies**: precision, confidence interval, temporal decay, weighting vectors, multi-axis decomposition.
**Extension**: `NormalizedScore` (range locked to [0,1]), `RawScore` (unbounded numeric), `WeightedScore` (adds axis weights), `TimeAdjustedScore` (adds decay).

## 8. `Cache` · Mind/Memory · R0T1

**Intended**: temporary high-speed storage to avoid recomputation.
**Future**: any key-value store with staleness semantics.
**Broad-use contexts**: memoized functions, RAG retrievers, pathway memory, routing decisions, computed heuristics, embedding caches, session state, prompt caches.
**Every context needs**: a way to store keyed values and look them up. Storage semantic is the definitional floor.
**Varies**: eviction policy (LRU, LFU, FIFO), TTL, size limits, consistency model, distributed vs local, invalidation strategy.
**Extension**: `LRUCache`, `TTLCache`, `DistributedCache`, `SemanticCache`, `WriteThroughCache`.

## 9. `OODA` · Mind/Strategy · R1T2

**Intended**: fast-loop decision cycle favoring agility.
**Future**: any tight observe-act feedback loop.
**Broad-use contexts**: combat aviation (origin), trading, alert response, debugging sessions, real-time control, agentic reasoning loops, competitive games, operations war rooms.
**Every context needs**: the four phases (Observe, Orient, Decide, Act) executed in order.
**Varies**: phase duration, orientation depth, decision method, action reversibility, loop interrupt criteria, cycle-time budget.
**Extension**: `FastOODA` (tight cycles), `DeliberativeOODA` (longer Orient phase), `InterruptibleOODA` (mid-cycle abort).

## 10. `Rally` · Society/Governance · R1T2

**Intended**: ad-hoc multi-party coordination via call-and-response.
**Future**: any call-to-action with respondents.
**Broad-use contexts**: emergency response, crowdsourcing, swarm coordination, federated computation, multi-agent task assignment, protest organizing, flash mobs, distributed consensus invocation.
**Every context needs**: broadcast mechanism, AcceptSpec criteria, deadline, quorum threshold, selection method on enlistees.
**Varies**: `max_participants` (2 to 100K+), authentication requirements, cancellation semantics, reward structures, reputation weighting, geographic scope.
**Extension**: `SecureRally` (auth required), `ReputationWeightedRally`, `GlobalRally`, `EmergencyRally` (tight deadline).

## 11. `Compensate` · Physics/Primitives · R0T1

**Intended**: structured rollback via logged inverses.
**Future**: any inverse-execution cleanup.
**Broad-use contexts**: database transactions, saga patterns, multi-agent coordination rollbacks, deployment reversions, user undo, game state reverts, financial chargebacks.
**Every context needs**: compensation log built during forward execution; LIFO reversal; idempotent inverses; status report.
**Varies**: inverse construction (automatic vs. explicit), partial-failure handling, multi-party coordination, audit-trail preservation, escalation on failed compensation.
**Extension**: `SagaCompensate` (distributed), `PreservingCompensate` (keeps audit), `PartialCompensate` (best-effort).

## 12. `Retry` · Mind/Strategy · R1T1 (post-§3.2 relocation from Physics)

**Intended**: intelligent, failure-informed re-attempt.
**Future**: any classified re-attempt with strategy.
**Broad-use contexts**: network failures, rate-limit recovery, API error handling, coordination breaks, verification retries, LLM completion retries, workflow step retries.
**Every context needs**: failure classification, retry decision, backoff computation.
**Varies**: classification taxonomy (transient/persistent specifics), budget, circuit-breaker integration, retry-hint protocol, jitter strategy.
**Extension**: `ExponentialRetry`, `JitteredRetry`, `BudgetedRetry`, `ClassifiedRetry`. The substrate-level "try same thing again" moves to `ReAttempt` in Physics/Primitives (§3.2).

## 13. `Abduction` · Mind/Reasoning · R1T1 (post-§3.3 consolidation with AbductiveLeap)

**Intended**: inference to best explanation from incomplete observation.
**Future**: any creative-inference operation.
**Broad-use contexts**: medical diagnosis, forensic reasoning, debugging, scientific theorizing, user-intent inference, anomaly explanation, error triage.
**Every context needs**: observation input, hypothesis output, "best guess" semantics (ranked, not exhaustive).
**Varies**: hypothesis space shape, ranking criteria, confidence tracking, verification requirements (critical for high-stakes — see caution entry in §3.15).
**Extension**: `BayesianAbduction` (probabilistic ranking), `ConstrainedAbduction` (rule-bounded hypothesis space), `VerifiedAbduction` (composes with a validation step).

## 14. `CognitiveSolver` · Mind/Strategy · R1T1

**Intended**: universal polymorphic intelligence atom.
**Future**: any solver implementing the five-surface contract.
**Broad-use contexts**: LLM-based solvers, hybrid human-AI solvers, tool-using agents, nested solver compositions, fractal intelligence instantiations.
**Every context needs**: Manifest, Execute, Consult, Verify, Feedback surfaces (with Manifest+Execute mandatory per §3.14); accepts Task; yields Solution.
**Varies**: cognitive mode (deliberative, reactive, reflective), rigor level, tooling, budget discipline, verification depth.
**Extension**: `RigorousSolver`, `OptimisticSolver`, `ReduceSolver`, `TaxonomistSolver`, `OutcomeArbiterSolver`.

## 15. `Stigmergy` · Mind/Memory · R0T1 (corrected per Gemini spot-check)

**Intended**: indirect coordination via environment traces (ant colony).
**Future**: any mediated coordination via shared substrate.
**Broad-use contexts**: ant colonies (biological origin), pheromone-based ML, shared whiteboards, wiki edit patterns, git commit flows, code comments, API documentation evolution, graffiti-based organization.
**Every context needs**: shared medium, MARK operation, SENSE operation, persistence mechanism (decay or versioning).
**Varies**: persistence scheme — **biological traces DECAY** (pheromones, graffiti wear); **digital traces often VERSION** (wiki history, git commits, append-only logs). Also: trace data structure, reinforcement mechanics, sensor radius, concurrency semantics.
**Extension**: `PheromoneStigmergy` (decay-based), `DocumentStigmergy` (version-based), `CodeStigmergy` (append-only-log-based), `DigitalStigmergy` (hybrid).
**Correction note**: an earlier sketch required "trace decay" as universal. Gemini's review correctly flagged that digital-substrate descendants (DocumentStigmergy, CodeStigmergy) use versioning or append-only logs rather than decay. The intersection is a *persistence mechanism that allows accumulation and eventual retirement of information* — decay is one implementation, versioning is another. The underlying invariant is that the shared medium preserves a retrievable history whose older entries can be superseded or forgotten.

## 16. `HeldRelease` · Society/Protocols · R0T1

**Intended**: trustless conditional value transfer (escrow).
**Future**: any value-held-until-condition pattern.
**Broad-use contexts**: crypto escrows, atomic swaps, payment channels, contingent contracts, staged delivery, milestone payments, dispute resolution, insurance payouts, bail bonds.
**Every context needs**: held value, release condition (hash commitment), timeout, state machine (EMPTY→HELD→RELEASED/RETURNED).
**Varies**: cryptographic primitives (hash algo, timelock type), dispute protocol, multi-party variants, partial release, streaming semantics.
**Extension**: `AtomicSwap`, `MilestoneEscrow` (N-stage release), `ArbitratedHeldRelease` (third-party dispute), `StreamingRelease` (continuous).

## 17. `AuditTrail` · Infrastructure/Verification · R1T1

**Intended**: compliance/debugging record via append-only signed log.
**Future**: any cryptographically verifiable history.
**Broad-use contexts**: SOC2 audits, regulatory compliance, forensic analysis, blame attribution, behavioral analysis, git history, blockchain state changes, medical records.
**Every context needs**: append-only semantics, signed entries, per-entry (timestamp, identity, action, input_hash, output_hash).
**Varies**: entry schema specifics, signature algorithm, retention policy, access controls, Merkle aggregation depth, privacy/redaction.
**Extension**: `SOC2AuditTrail`, `BlockchainAuditTrail`, `PrivacyPreservingAuditTrail` (redacted views), `RealTimeAuditTrail`.

## 18. `Discover` · Society/Protocols · R2T1

**Intended**: distributed query for external resources (horizontal breadth primitive per FI v3 §4.3 Grammar of Agency).
**Future**: any horizontal search operation.
**Broad-use contexts**: service discovery, peer lookup, resource search, agent capability discovery, dataset location, tool discovery, federated search.
**Every context needs**: query broadcast, filter criteria, response aggregation, timeout.
**Varies**: network topology (broadcast, gossip, registry), authentication, response ranking, discovery radius, async vs sync.
**Extension**: `LocalDiscover` (single network), `GlobalDiscover` (federated), `AuthDiscover` (credential-gated), `RankedDiscover` (relevance-sorted).

## 19. `MonotonicCounter` · Society/Protocols · R0T1

**Intended**: strictly increasing value for coordination simplification.
**Future**: any conflict-free increment-only counter.
**Broad-use contexts**: Lamport clocks, vector clocks, version numbers, CRDTs, sequence IDs, balance ledgers (monotonic deposits), consensus view numbers.
**Every context needs**: only-increase guarantee. That's it — every other property is a specialization.
**Varies**: increment step, distributed coordination method, rollover semantics, ceiling, merge function.
**Extension**: `LamportClock`, `VectorClock` (per-node), `GCounter` (CRDT), `CappedCounter` (with ceiling).

## 20. `TimeWarpLog` · Infrastructure/Primitives · R0T1

**Intended**: relativistic event ordering via causal cones (post-§3.1 coherence fix).
**Future**: any log that tolerates latency via causal rather than temporal ordering.
**Broad-use contexts**: distributed systems, blockchain consensus, multi-agent history, eventual-consistency stores, latency-tolerant databases, cross-datacenter replication.
**Every context needs**: causal cone tracking per entry, acceptance rule based on non-contradiction with current cone, append-only semantics.
**Varies**: cone computation method, contradiction resolution policy, storage backend, replication model, trust model for event authors.
**Extension**: `DistributedTimeWarpLog`, `AuthenticatedTimeWarpLog` (signed events required — see caution §3.15), `BoundedConeLog` (cone depth-limited).

---

## Observations from the sample

**The test scales.** Walking the broad-use question on 20 diverse patterns produces specifications that sit at the usability floor without over-constraining descendants. Each pattern's required fields/invariants match what *every* context needs; each pattern's variation territory matches what descendants legitimately diverge on.

**Patterns the test would shift if we re-minted them.** A few observations outside the audit's scope:
- `Score` is currently under-specified in the DB (no required `metric_id`/`normalized_range`); §3.10 already fixes this.
- `Rally`'s current `selection_criteria` parameter should be in `accepts` (Appendix A catches this).
- `OODA`'s four-phase structure is hardcoded in the mechanism but not captured as a structural invariant — borderline; could be specified more cleanly.
- `Cache`'s mechanism mentions HeuristicSnap specifically but Cache is broader than that — the mechanism text is slightly narrow for the pattern's actual broad use.

**Patterns the test validates as well-specified.** Lock, Gate, TimeWarpLog, MonotonicCounter, AuditTrail, HeldRelease — each has a specification that stays at the definitional minimum.

**The pattern not tested here**: writing *new* mints. The audit-of-additions work in §3.19 is the close cousin of this exercise — applying the broad-use test to the four new patterns (FrameError, PathwayMemory, DecompositionGate, DocumentedOverride) and to the invariants/fields the audit proposes adding to existing ones. Those results are already in §3.19.

---

## Using this document

If the broad-use sketches above match how we want the foundation to scale, the methodology applies library-wide: every future mint walks the same six-step question before adding any constraint. If any sketch is wrong, the audit's calibration is wrong too — fix here before applying.

---

## Batch 2 — Ring-0 primitives, new additions, verification stack, underrepresented categories

## 21. `Agent` · Mind/Strategy · R0T1

**Intended**: the fundamental unit of agency — any entity that observes, reasons, acts.
**Future**: any autonomous entity participating in coordination.
**Broad-use contexts**: LLM agents, human workers, robots, tool-users, services, processes, swarms, subagents, simulation characters, NPCs, CI runners, daemons.
**Every context needs**: the observe → think → act → observe loop; state maintenance; goal orientation.
**Varies**: perception modality, state representation, reasoning substrate (LLM, rules, humans), action space, loop cycle time, embodiment.
**Extension**: `LLMAgent`, `HumanAgent`, `RoboticAgent`, `SubAgent`, `AutonomousAgent`, `SupervisedAgent`.
**Note**: §4 of the audit flags Agent's layer placement as debatable. Broad-use spans cognition (think), coordination (participate with peers), and execution (act on environment), so its placement touches all three upper layers. Mind/Strategy is defensible because the *defining activity* is the cognitive loop; the other aspects are behaviors it composes.

## 22. `Identity` · Infrastructure/Data Structures · R0T1

**Intended**: unique distinguishing context of an agent — the persistent "Who."
**Future**: any handle carrying cross-interaction continuity.
**Broad-use contexts**: cryptographic agent IDs, human pseudonyms, corporate personas, service accounts, bot handles, role-bound identities, federated identities, anonymous-but-unique identifiers.
**Every context needs**: uniqueness guarantee within scope; persistence across interactions; a way to distinguish Self from Other.
**Varies**: key material (public keys, DIDs, UUIDs, username+password), reputation attachments, history binding, key rotation mechanics, pseudonymity vs real-name.
**Extension**: `CryptographicIdentity`, `FederatedIdentity`, `PseudonymousIdentity`, `DelegatedIdentity`.

## 23. `Condition` · Infrastructure/Data Structures · R0T1

**Intended**: marker interface (Trait) for patterns that evaluate to Boolean.
**Future**: any pattern usable as a predicate.
**Broad-use contexts**: feature flags, guard clauses, assertions, invariants, preconditions, postconditions, match predicates, filter criteria.
**Every context needs**: an evaluation logic returning Boolean; context input for the evaluation.
**Varies**: complexity of evaluation (literal true vs. complex predicate), side-effect profile, caching, evaluation cost, parameterization.
**Extension**: `SimpleCondition`, `CompositeCondition`, `AsyncCondition`, `StatefulCondition`.
**Note**: Condition is a Trait (as §3.18 proposes for Meta/Global/Subject/Creative). The existing mechanism text already says "A marker interface (Trait)" — confirming this is the right treatment for genuinely dimensional/typing patterns.

## 24. `State` · Infrastructure/Data Structures · R0T1

**Intended**: stored information representing a system's condition at time T.
**Future**: any persistent representation of system condition.
**Broad-use contexts**: in-memory object state, database rows, session state, workflow state, agent beliefs, machine configuration, app UI state, ML model weights.
**Every context needs**: representation content (what), temporal validity (when).
**Varies**: persistence medium, mutation semantics (mutable/immutable/versioned), access protocol, consistency model, serialization format.
**Extension**: `PersistedState`, `DistributedState`, `VersionedState`, `ImmutableState`, `EncryptedState`.

## 25. `Value` · Infrastructure/Data Structures · R0T1

**Intended**: quantitative or qualitative measure of utility, worth, or priority.
**Future**: any measure that can be compared, accumulated, or exchanged.
**Broad-use contexts**: economic value (tokens, currency), utility scores, priorities, fitness values, preference orderings, confidence weights, attention budgets.
**Every context needs**: a way to compare two values (ordering or equivalence); a scale or unit.
**Varies**: numeric vs qualitative, bounded vs unbounded, additive vs ordinal, single-dimensional vs vector.
**Extension**: `EconomicValue`, `UtilityValue`, `PriorityValue`, `VectorValue`.

## 26. `Datum` · Infrastructure/Data Structures · R1T1

**Intended**: a single unit of raw unprocessed fact (singular of Data).
**Future**: any pre-semantic information unit.
**Broad-use contexts**: sensor readings, log lines, bytes, observations, raw measurements, tokens, events pre-interpretation.
**Every context needs**: existence (the unit IS something); distinctness from other data points.
**Varies**: encoding, unit type, precision, source attribution, timestamp attachment, structured vs unstructured.
**Extension**: `TypedDatum`, `TimestampedDatum`, `SignedDatum`, `EncodedDatum`.

## 27. `AcceptSpec` · Society/Protocols · R0T2

**Intended**: non-compensatory acceptance contract at solver boundaries.
**Future**: any hard-criterion validation contract.
**Broad-use contexts**: solver outputs, API contracts, SLA verification, quality gates, regulatory compliance, safety constraints, release criteria, API-to-API handoffs.
**Every context needs**: typed criteria (each independently verifiable); non-compensatory semantics (no axis can offset another's failure); a clear yield contract on success/failure.
**Varies**: criterion count, evaluation order, severity tiers, FrameError production discipline (per §3.14 mechanism update — on failure yields FrameError, not generic false).
**Extension**: `SolverAcceptSpec`, `APIAcceptSpec`, `SafetyAcceptSpec`, `SLAAcceptSpec`.
**Note for audit**: this is the pattern whose mechanism gets the §3.14 update. The broad-use test confirms: *every* context needs the FrameError-on-failure semantic (not just Solver contexts), because any hard-criterion contract benefits from forcing upstream restructuring rather than retry. The mechanism update generalizes.

## 28. `Budget` · Infrastructure/Primitives · R0T1 (post-§3.19 loosening)

**Intended**: quantified allocation of a resource constraining execution.
**Future**: any resource-limit primitive.
**Broad-use contexts**: compute budgets, time budgets, energy budgets, token budgets, attention budgets, monetary budgets, risk budgets, retry budgets.
**Every context needs**: an allocation (how much), a consumption/refund tracking mechanism, conservation (total tracked value is preserved across transactions).
**Varies**: strict non-negative (BoundedBudget) vs. overdraft-allowed (OverdraftBudget), monotonic vs rebalancing (RollingBudget), refund semantics, multi-resource aggregation.
**Extension**: `BoundedBudget` (adds strict non-negative), `RollingBudget` (rebalances), `ComputeBudget`, `MonetaryBudget`.
**Note for audit**: §3.19 correctly pulled back the "monotonic allocation" invariant. Broad-use test confirms: RollingBudget and OverdraftBudget are legitimate descendants that need the full-allocation-state mutable.

## 29. `EntropyPump` · Physics/Primitives · R1T2 (post-§3.19 loosening)

**Intended**: inject entropy to escape convergence deadlocks.
**Future**: any noise-injection mechanism preventing stagnation.
**Broad-use contexts**: simulated annealing, chaos engineering, exploration bonuses in RL, mutation in evolutionary algorithms, diversity injection in ensemble methods, tie-breaking, unstuck-from-local-optima routines.
**Every context needs**: a noise-injection mechanism; a target for the injection.
**Varies**: noise magnitude (bounded to destabilizing), scope (targeted to global), injection timing (continuous, on-demand, threshold-triggered), entropy source (PRNG, hardware, user input).
**Extension**: `BoundedEntropyPump` (adds magnitude cap), `TargetedEntropyPump` (stuck-states only), `ChaosMonkey` (deliberately destabilizing), `AnnealingPump`.
**Note for audit**: §3.19 correctly drops both proposed invariants. `ChaosMonkey` is a legitimate descendant that deliberately violates "bounded injection"; `UniversalEntropyPump` violates "targeted scope."

## 30. `Result` · Infrastructure/Data Structures · R0T1 (post-§3.14 + §3.19)

**Intended**: canonical output of a Solver operation (Execute surface return type).
**Future**: any transaction-output artifact.
**Broad-use contexts**: Solver results, API responses, test results, workflow outputs, task completions, query returns, computation products.
**Every context needs**: `status` (success/partial/fail) and `stop_reason` (completed/budget/quality) — without these a Result is ambiguous.
**Varies**: `outputs` (optional — a failed Result may have no outputs to report; a partial Result has some); metrics payload, provenance, confidence.
**Extension**: `SignedResult` (adds signature), `VerifiedResult` (post-AcceptSpec → Solution), `StreamingResult` (incremental).
**Note for audit**: §3.19's treatment (status + stop_reason required, outputs optional) passes broad-use. A failed Result with status="fail" and stop_reason="budget" legitimately has no outputs; forcing an empty-outputs field wastes identity-hash bytes.

## 31. `Validate` · Infrastructure/Verification · R1T1

**Intended**: syntactic schema verification.
**Future**: any structural conformance check.
**Broad-use contexts**: JSON schema validation, API request validation, type checking, form validation, config file validation, protobuf validation, ontology conformance.
**Every context needs**: input artifact, schema/constraint set; yields `Boolean` (per §3.13 verification-stack taxonomy).
**Varies**: schema language, strictness (coercion allowed or not), error reporting verbosity, partial-validation support.
**Extension**: `StrictValidate`, `CoercingValidate`, `SchemaValidate`, `TypedValidate`.

## 32. `Check` · Infrastructure/Data Structures · R0T1

**Intended**: non-blocking truth evaluation of a condition.
**Future**: any observational boolean-yielding predicate.
**Broad-use contexts**: assertions, health checks, probes, invariant verification, sanity checks, precondition checks, integration tests.
**Every context needs**: condition evaluated against target; yields `Status` (per §3.13 — note: NOT Boolean like Validate; Status carries more signal like Verified/Falsified/Unknown).
**Varies**: evaluation cost, caching, async vs sync, scope (scoped to one invocation vs. continuous).
**Extension**: `HealthCheck`, `ScopedCheck`, `AsyncCheck`, `IdempotentCheck`.
**Note for audit**: `Check` is currently categorized Infrastructure/Data Structures but §3.11 moves it to Infrastructure/Primitives (it's a Verb). Broad-use confirms: every context is an operation (checking) not a data structure.

## 33. `Judge` · Infrastructure/Primitives · R0T1

**Intended**: scalar evaluation of merit on continuous scale.
**Future**: any quality-scoring operation.
**Broad-use contexts**: model output evaluation, content quality rating, candidate ranking, aesthetic assessment, fitness evaluation, risk scoring, reviewer judgments.
**Every context needs**: subject to evaluate; accepts a `ScoringFunction` (criteria moved to accepts per §3.1); yields `Score` (per §3.13).
**Varies**: scoring function complexity, confidence bounds, calibration method, multi-axis decomposition, explainability.
**Extension**: `CalibratedJudge`, `ExplainableJudge`, `EnsembleJudge`, `HumanJudge`.

## 34. `Bid` · Society/Economics · R1T1

**Intended**: binding offer from solver to execute a task.
**Future**: any commitment offer in a negotiation.
**Broad-use contexts**: solver auctions, procurement, crowdsourcing, API rate-limit bidding, resource auctions, milestone proposals, contracts-for-work.
**Every context needs**: bidder identity, offer content (cost, confidence, capability match), commitment semantics ("if accepted, bidder is bound").
**Varies**: currency/unit, confidence representation, capability-match structure, withdraw semantics, expiry timing.
**Extension**: `SealedBid`, `OpenBid`, `ReverseBid`, `AuctionBid`, `IrrevocableBid`.

## 35. `Constitution` · Society/Governance · R0T1

**Intended**: immutable rule set defining principles for an agent group.
**Future**: any foundational-rule artifact.
**Broad-use contexts**: DAO constitutions, corporate bylaws, software rule sets (e.g., Claude's Constitutional AI), community charters, API governance rules, federation rules.
**Every context needs**: structured principles (immutable once ratified), binding semantics (via `OathBind`), identity of ratifying parties.
**Varies**: amendment mechanism (rigid vs. flexible), enforcement mechanism (automated vs. delegated), penalty specifications, inheritance from parent constitutions.
**Extension**: `RigidConstitution` (no amendments), `AmendableConstitution` (via supermajority), `HierarchicalConstitution` (child inherits parent).

## 36. `Belief` · Infrastructure/Data Structures · R2T1

**Intended**: a subjective epistemic claim with confidence and evidence.
**Future**: any held-claim with uncertainty tracking.
**Broad-use contexts**: LLM prior beliefs, scientific hypotheses, agent mental models, world models, prediction-market positions, user-intent inferences, probabilistic assertions.
**Every context needs**: a claim, a confidence score [0.0, 1.0], a pointer to supporting evidence; mutability via `BayesUpdate` or similar.
**Varies**: evidence representation (citation, linked data, derivation), confidence update rule (Bayesian, heuristic, frequency-based), superseding semantics, audit trail.
**Extension**: `BayesianBelief`, `EvidentialBelief`, `ConsensusBelief`, `Intuition` (low-confidence).

## 37. `Ballot` · Infrastructure/Data Structures · R0T3

**Intended**: immutable container for a decision proposal.
**Future**: any vote or decision-record artifact.
**Broad-use contexts**: democratic votes, governance ballots, consensus rounds, delegated voting, poll artifacts, veto records.
**Every context needs**: question being decided, options, voting rules, deadline, immutability once cast.
**Varies**: option count, voting rules (majority, supermajority, unanimity, weighted), anonymity, delegation chains, cryptographic proofs.
**Extension**: `SecretBallot`, `DelegatedBallot`, `WeightedBallot`, `LiquidBallot`.

## 38. `Vote` · Society/Governance · R2T2

**Intended**: N-agent decision mechanism with integrity guarantees.
**Future**: any structured collective decision act.
**Broad-use contexts**: DAO governance, jury verdicts, consensus rounds, multi-agent protocols, corporate board decisions, peer review aggregation, quorum sensing.
**Every context needs**: initiator, Ballot, quorum requirement, cast-collection phase, deadline, result computation, result broadcast.
**Varies**: cast channel, authentication method, one-vote-per-agent enforcement, cast encryption, ballot counting method (aggregate).
**Extension**: `SecretVote`, `WeightedVote`, `LiquidVote`, `VetoedVote`.

## 39. `Contract` · Infrastructure/Data Structures · R1T1

**Intended**: immutable record of binding agreement between identities.
**Future**: any signed multi-party commitment artifact.
**Broad-use contexts**: legal contracts, smart contracts, SLAs, API service agreements, employment contracts, insurance policies, escrow terms, bilateral MoUs.
**Every context needs**: identities of parties, conditions/obligations (terms), signatures from all parties, immutability.
**Varies**: signature algorithm, dispute-resolution clause, termination semantics, amendment mechanism, jurisdictional binding.
**Extension**: `SmartContract`, `LegalContract`, `EscrowContract`, `StreamingContract`.

## 40. `BayesUpdate` · Mind/Inference · R2T1

**Intended**: mathematically rigorous belief revision via likelihood weighting.
**Future**: any Bayesian inference operation.
**Broad-use contexts**: probabilistic reasoning, diagnostic updating, A/B test analysis, prediction market updates, scientific hypothesis revision, spam filtering, medical diagnosis.
**Every context needs**: prior probability, observed evidence, likelihood ratio computation, posterior.
**Varies**: prior representation (point, distribution, ensemble), likelihood estimation method, base-rate handling, clamp thresholds to avoid 0/1 collapse, incremental vs batch.
**Extension**: `BatchBayes`, `SequentialBayes`, `CalibratedBayes`, `NonparametricBayes`.

---

## Observations from batch 2

**Validations of audit changes.**
- `Budget` loosening (§3.19): correct — RollingBudget/OverdraftBudget are legitimate.
- `EntropyPump` loosening (§3.19): correct — ChaosMonkey cannot exist under the proposed invariants.
- `Result` partial-field requirement (§3.19): correct — failed Results have no outputs legitimately.
- `Check` → Infrastructure/Primitives (§3.11): broad-use confirms it's a Verb.
- `AcceptSpec` mechanism update (§3.14): broad-use confirms — *every* hard-criterion context benefits from FrameError-on-failure, not just solver boundaries.
- `Judge` criteria → accepts (§3.1 + §3.5): correct, broad-use confirms ScoringFunction is caller-supplied.

**New audit items surfaced.**
1. **`Check`'s yield type might be under-specified.** §3.13 gives Check yields `Status`. But most Check contexts actually need Boolean (pass/fail). Status as a richer type (Verified/Falsified/Unknown) is useful for probes and diagnostic checks, but many call-sites use Check as a plain boolean predicate. Worth flagging whether the audit wants `Check → Boolean` or `Check → Status` — the broad-use analysis leans toward `Status` being right (the extra signal matters when it's there), but some descendant `BooleanCheck` might need to coerce.
2. **`Belief`'s confidence range is principled [0,1]** — not currently declared as such in the DB (just text description). §3.10's "Vacuous data_schemas" did `Probability` but not `Belief`. Worth extending that section to declare `Belief.confidence: Probability` with range [0,1].
3. **`Identity`'s mechanism contrasts with Nature and Role** ("Unlike nature (what you are) or Role (what you do)") — so it explicitly assumes Nature exists as a distinct pattern. This validates §3.18's decision to keep Nature as a canonical Noun rather than trait-convert.
4. **Ballot at Tier 3** — Tier 3 is experimental. Ballot seems foundational (used by Vote, LazyConsensus, etc.). Should probably be Tier 1. Worth adding to §3.x as a Tier adjustment.

The methodology continues to hold. Next batch should cover more verification-stack interior, Noun primitives, Physics/Time, and the larger Society/Protocols territory.

---

## Batch 3 — core Verbs, classical reasoning canon, solver family, flow control

## 41. `Think` · Mind/Reasoning · R0T0

**Intended**: atomic cognitive step — one inference, one connection, one realization.
**Future**: any side-effect-free cognition unit.
**Broad-use contexts**: LLM token generation, inference steps, micro-realizations, single-axiom derivations, one-shot pattern-matching, intuition flashes, chain-of-thought atoms.
**Every context needs**: input context, output datum, side-effect-free semantic (no external state change).
**Varies**: cognitive mode (deliberative, intuitive), latency (ms to seconds), cost, confidence attached to output.
**Extension**: `DeliberativeThink`, `IntuitiveThink`, `CostBoundedThink`, `ChainedThink`.

## 42. `Act` · Infrastructure/Primitives · R0T1

**Intended**: root primitive for state modification external to private memory.
**Future**: any operation with external effect.
**Broad-use contexts**: tool invocations, API calls, physical actuation, file writes, process spawns, message sends, database mutations, UI updates.
**Every context needs**: authorization check, logging, reversibility status (explicit reversible/irreversible marker).
**Varies**: target environment, reversibility mechanism (if reversible), logging format, permission model, idempotency guarantees.
**Extension**: `IdempotentAct`, `ReversibleAct`, `IrreversibleAct`, `BatchedAct`.
**Note**: `Act`'s mandate that "All Acts must be authorized, logged, and potentially reversible" is a strong invariant. Broad-use test: does every legitimate descendant need these? Probably yes for authorization and logging; reversibility is "potentially" (marker-level, not mandatory). Seems well-calibrated.

## 43. `Observe` · Infrastructure/Primitives · R0T1 (post-§3.11 relocation from Data Structures)

**Intended**: active state perception from environment.
**Future**: any information-gathering operation.
**Broad-use contexts**: API polling, file reads, sensor queries, user input reception, log tail reads, event subscriptions, probes, LLM introspection.
**Every context needs**: source (what to observe), filtering (attention), integration into context.
**Varies**: polling interval, filter strictness, caching, async vs sync, authentication.
**Extension**: `PollingObserve`, `StreamingObserve`, `FilteredObserve`, `CachedObserve`.
**Note for audit**: §3.11 correctly moves Observe from Data Structures to Primitives. Broad-use confirms: every context is an operation (Verb), not a data structure (Noun).

## 44. `Plan` · Infrastructure/Data Structures · R0T0

**Intended**: ordered sequence of steps to reach a goal.
**Future**: any goal-transition artifact.
**Broad-use contexts**: execution plans, project roadmaps, sprint plans, travel itineraries, recipe steps, ML training schedules, build plans, deployment sequences.
**Every context needs**: sequence of steps, causal dependencies between steps, goal state, starting state.
**Varies**: step granularity, resource allocation, conditional branches, parallel execution, rollback points, revision policy.
**Extension**: `ConditionalPlan`, `ParallelPlan`, `RecoveryPlan`, `RollbackPlan`.

## 45. `Hypothesis` · Infrastructure/Data Structures · R0T1

**Intended**: tentative explanation subject to verification/falsification.
**Future**: any claim staged for empirical testing.
**Broad-use contexts**: scientific hypotheses, debugging conjectures, detective work, forensic reasoning, theory formation, null-hypothesis testing, bug-cause candidates.
**Every context needs**: the claim itself, status (untested/corroborated/falsified), test-ability (must be empirically checkable — distinguishes from Assumption and Axiom).
**Varies**: confidence tracking, evidence links, competing-hypothesis structure, falsification-condition spec.
**Extension**: `ScientificHypothesis`, `DebuggingHypothesis`, `CompetingHypothesis`.
**Note for audit**: the current mechanism ("A tentative explanation or prediction that is subject to verification or falsification") restates the gloss. The §3.18 finding is confirmed — the mechanism should differentiate Hypothesis from Claim and Assumption via its testability semantic. The broad-use sketch above gives a concrete rewrite.

## 46. `Assumption` · Infrastructure/Data Structures · R1T1

**Intended**: gap-filler treated as true temporarily while thinking proceeds.
**Future**: any provisional truth placeholder.
**Broad-use contexts**: reasoning under uncertainty, planning under incomplete info, debugging premises, modeling simplifications, "given that X..." framings.
**Every context needs**: the provisional claim, tracking (so it can be re-examined), validation opportunity.
**Varies**: confidence-when-assumed, invalidation triggers, derivation chain tracking.
**Extension**: `TrackedAssumption`, `SimplifyingAssumption`, `WorkingAssumption`.

## 47. `Axiom` · Society/Protocols · R1T1

**Intended**: statement accepted as true without proof, foundational in current logic frame.
**Future**: any non-negotiable starting premise.
**Broad-use contexts**: mathematical axioms, ethical first principles, constitutional declarations, API contracts, system-level invariants, organizational values.
**Every context needs**: statement text, scope of applicability, non-negotiability semantic.
**Varies**: provability outside the frame (some axioms are provable in wider frames), frame identity, dependent-derivation tree.
**Extension**: `MathematicalAxiom`, `EthicalAxiom`, `ConstitutionalAxiom`, `SystemAxiom`.
**Note for audit**: §3.18 initial-pass notes question Axiom's Society/Protocols placement — broad-use spans math (pure reasoning — Mind), ethics (normative — Society/Governance), constitutional (Society/Governance). Society/Protocols is one fit but not obviously the strongest. Probably leave as-is unless a clearer home surfaces; Society captures "accepted by community as starting point" which is the coordination aspect.

## 48. `Deduction` · Mind/Reasoning · R1T1

**Intended**: general → specific inference where premises force the conclusion.
**Future**: any truth-preserving inference.
**Broad-use contexts**: formal logic, mathematical proof, rule application, type inference, constraint propagation, SQL query planning, theorem proving.
**Every context needs**: general rule (Axiom or higher-level conclusion), specific case, conclusion that MUST be true if premises are.
**Varies**: rule representation, proof-carrying vs assertive, finite vs higher-order, decidability.
**Extension**: `FormalDeduction`, `RuleApplication`, `TypedDeduction`, `ModalDeduction`.
**Note for audit**: §3.5 wires `Specialize` → `references Deduction`; `Eliminate` → `references Deduction` + `Falsification`; `BackwardChain` → `references Deduction`. Broad-use validates: these descendants all invoke deductive structure.

## 49. `Induction` · Mind/Reasoning · R1T1

**Intended**: specific observations → general rule (probabilistic, not certain).
**Future**: any generalization from samples.
**Broad-use contexts**: scientific generalization, ML training, pattern recognition, base-rate estimation, statistical inference, law-of-large-numbers reasoning, curve fitting.
**Every context needs**: specific observations, inferred general claim, probabilistic (not certain) conclusion semantic.
**Varies**: sample size, generalization method, confidence estimation, robustness to outliers, prior-weighted updates.
**Extension**: `BayesianInduction`, `StatisticalInduction`, `PatternInduction`.

## 50. `Falsification` · Mind/Strategy · R1T1

**Intended**: prove a Hypothesis false via observed incongruity.
**Future**: any elimination-via-counterexample operation.
**Broad-use contexts**: scientific falsification, bug reproduction, security penetration testing, constraint-violation detection, counterexample generation, test-failure analysis.
**Every context needs**: hypothesis to test, observation capability, recognition of incongruity between prediction and reality.
**Varies**: counterexample generation strategy, confidence threshold for declaring falsification, retry semantics on ambiguous evidence.
**Extension**: `AdversarialFalsification`, `AutomatedFalsification`, `StatisticalFalsification`.

## 51. `SolverTree` · Society/Governance · R1T1 (post-§3.14 DAG update)

**Intended**: active hierarchy of coordinated solver instances — the command topology.
**Future**: any multi-solver organization for a task.
**Broad-use contexts**: solver delegation trees, nested LLM agents, divide-and-conquer workflows, map-reduce problem decomposition, agent swarms, research team hierarchies.
**Every context needs**: root solver, child-solver relationships (delegation edges), reporting edges upward, origin (tree-like at decomposition time per §3.14 update).
**Varies**: runtime shape (tree, DAG with fan-in, DAG with deduplication); budget cascade policy; failure handling; authority model.
**Extension**: `StrictTreeSolverTree`, `FanInSolverTree`, `CachedSolverTree`, `AuthorityHierarchy`.
**Note for audit**: §3.14's drop of "single supervisor" invariant passes broad-use — fan-in via shared sub-solvers is structurally required for reuse.

## 52. `UniversalSolverTree` · Society/Governance · R1T1

**Intended**: theoretical aggregation of all valid solver trees across agents — the collective epistemic state.
**Future**: any global-knowledge-graph abstraction.
**Broad-use contexts**: cross-agent learning, pattern reuse, redundancy detection, collective wisdom, problem-solving archaeology.
**Every context needs**: aggregation semantic, DAG shape (per §3.14 update), singularity (only one logical instance).
**Varies**: physical instantiation (distributed DB, federated, local copy), access protocol, privacy/scope boundaries, update semantics.
**Extension**: `FederatedUniversalSolverTree`, `LocalUniversalSolverTree`.

## 53. `SolverRoot` → `RootSolver` · Society/Governance · R1T1 (post-§3.14 mechanism update + naming correction)

**Naming correction flagged during batch 3**: the Fractal Intelligence paper v3 canonically calls this `RootSolver`, not `SolverRoot`. Current DB handle is drift from earlier nomenclature; should be renamed (with `_meta.supersedes: [old-sema_id]` for downstream redirect). This should be added to §3.14 of the main audit.

**Intended**: the apex node of a SolverTree — the unique point where problems enter that tree.
**Future**: any apex-triage node in a problem-solving hierarchy.
**Broad-use contexts**:
- The `UniversalSolverTree` (the global infrastructure per FI v3) has *one* apex RootSolver — the singleton entry point for every problem humanity routes through the system.
- If a sub-domain is carved out of the UniversalSolverTree as its own SolverTree (e.g., "the RootSolver for the medical-diagnosis sub-tree"), that sub-tree has its own RootSolver.
- Orchestration root in a workflow, dispatch root in a multi-agent system, top node of a research program.

**Every context needs**: problem framing authority, budget allocation authority, triage function (routing among possible sub-handlers), ultimate accountability, Pathway Memory (learned routing per §3.14 update), singleton semantic within its tree.
**Varies**: framing rigor, budget reserve policy, triage heuristics, routing strategy, failure escalation, scope (global vs sub-domain), succession semantics if the RootSolver itself fails.
**Extension**: `UniversalRootSolver` (the global singleton; the apex of UniversalSolverTree), `DomainRootSolver` (apex of a carved-out sub-tree), `LearningRootSolver`, `BudgetedRootSolver`.

**Singleton invariant**: each SolverTree has *exactly one* RootSolver. The UniversalSolverTree's RootSolver is the unique global entry point for all problems. This is a structural property of what a tree-root IS, not a prescriptive constraint — it passes the broad-use test because no legitimate descendant can have zero or multiple roots per tree.

**Audit impact**: renaming SolverRoot → RootSolver is a §3.14 item alongside the Question→Consult surface rename. `_meta.supersedes` redirect needed. UniversalSolverTree's own mechanism may need an update to reference RootSolver by the new name (transitively updates any pattern referencing UniversalSolverTree via template syntax).

## 54. `RigorousSolver` · Mind/Strategy · R2T2 (post-§3.14 inline-ceremony rewrite)

**Intended**: high-reliability, high-latency Solver with non-compensatory gates.
**Future**: any solver trading speed for pre-action verification assurance.
**Broad-use contexts**: safety-critical reasoning, high-stakes decisions, medical diagnosis, financial deployments, correctness-first code generation, formal verification, audit preparation.
**Every context needs**: full five-surface contract (Manifest, Execute, Consult, Verify, Feedback); non-compensatory acceptance gates; pre-action verification.
**Varies**: specific verification steps, probing depth, socratic clarification depth, feedback structure.
**Extension**: `FormalRigorousSolver`, `HumanSupervisedRigorousSolver`, `IterativeRigorousSolver`.

## 55. `OptimisticSolver` · Society/Protocols · R1T2 (layer retained per §3.14)

**Intended**: high-velocity Solver using post-action correction instead of pre-action verification.
**Future**: any solver trading verification-before-act for throughput.
**Broad-use contexts**: parallel multi-agent execution, high-throughput processing, speculative execution, eventual-consistency workflows, low-latency coordination, trading systems.
**Every context needs**: parallel runtime (Actor Model with Mailboxes), atomic-bid protocol, single-turn plan+execute, `Reflexion` + `Compensate` for correction.
**Varies**: parallelism degree, bid protocol specifics, reflexion depth, compensation strategy.
**Extension**: `BidAuctionSolver`, `SpeculativeSolver`, `EventualConsistencySolver`.
**Note**: §3.14's layer retention is confirmed by broad-use — every legitimate context explicitly needs Society-layer coordination primitives (AtomicBid, Actor Model). Relocating to Mind would force either gravity inversion or stripping those deps.

## 56. `Route` · Physics/Primitives · R0T1

**Intended**: classify input and direct to specialized handler.
**Future**: any N-way classifier-dispatcher.
**Broad-use contexts**: HTTP routing, load balancing, query type routing, message brokers, intent-classification dispatch, model-selection routing, multi-head attention.
**Every context needs**: input to classify, classification function, dispatch table (input type → handler).
**Varies**: classification method (rules, ML, heuristics), routing-table representation, fallback handling, cost-aware dispatch.
**Extension**: `RuleRouter`, `MLRouter`, `CostAwareRouter`, `LoadBalancingRouter`.
**Note for audit**: `Route` is the right canonical handle for the Branch/Route/Switch cluster per §3.3. After §3.18 adds `_meta.supersedes: [Switch]`, any pattern referencing Switch's old sema_id redirects to Route.

## 57. `Reframe` · Mind/Reasoning · R2T1

**Intended**: transform the problem statement to find a new solver tree root.
**Future**: any perspective-shift cognitive operation.
**Broad-use contexts**: creative problem-solving, deadlock resolution, lateral thinking, reductio reformulation, analogical reframing, scope reset, domain translation.
**Every context needs**: original problem statement, transformation (perspective, scope, framing), new solver-root candidate.
**Varies**: reframing technique (invert, expand, shift time, change subject), return semantics (replaces vs. augments), cost, success criteria.
**Extension**: `InversionReframe`, `ScopeReframe`, `DomainReframe`, `TemporalReframe`.
**Note**: `Reframe` pairs with `Route` in §3.14's hard-seam composition — `Gate → Decision{FrameError} → (Route | Reframe)`. Broad-use validates both as general-purpose primitives.

## 58. `Heartbeat` · Physics/Time · R0T1

**Intended**: liveness detection via periodic signals.
**Future**: any periodic signal establishing continued existence.
**Broad-use contexts**: distributed system health checks, web service uptime monitoring, agent aliveness, IoT device liveness, connection-pool health, biological heartbeat metaphor, session keepalives.
**Every context needs**: emitter, receiver, interval, miss-threshold for failure detection.
**Varies**: interval value (ms for local, minutes for distributed), payload (empty ping vs health metrics), authentication, K-out-of-N tolerance.
**Extension**: `AuthenticatedHeartbeat`, `HealthMetricHeartbeat`, `MultiPathHeartbeat`.

## 59. `Ledger` · Infrastructure/Data Structures · R0T1

**Intended**: immutable record of value transfers, debts, obligations.
**Future**: any append-only transactional history artifact.
**Broad-use contexts**: financial ledgers, blockchain state, CRDT operation logs, event sourcing stores, audit records, accounts-payable systems, game state transactions.
**Every context needs**: immutability, transactional semantics, value attribution per entry.
**Varies**: signature/authentication model, partitioning, query-efficiency structures (indices), retention, privacy controls.
**Extension**: `BlockchainLedger`, `PartitionedLedger`, `EncryptedLedger`, `PublicLedger`.

## 60. `ComputeBudget` · Mind/Strategy · R0T1

**Intended**: cognitive governor weighing task value against resource budget (ROI gate).
**Future**: any value-vs-cost stopping rule.
**Broad-use contexts**: LLM compute allocation, human time prioritization, research-depth decisions, optimization-iteration stopping, cognitive-load management, attention allocation.
**Every context needs**: value estimation, budget tracking, ROI evaluation rule, stopping criterion.
**Varies**: `max_budget` (see Appendix A — typed PositiveInteger, no cap), value estimation method, ROI threshold, budget refund semantics.
**Extension**: `ExponentialDecayBudget`, `QuotaComputeBudget`, `AdaptiveComputeBudget`.

---

## Observations from batch 3

**More validations of audit decisions.**
- §3.11 move of Observe from Data Structures to Primitives: confirmed (it's a Verb).
- §3.14 drop of SolverTree's "single supervisor" invariant: confirmed (fan-in is structurally required).
- §3.14 OptimisticSolver layer retention in Society: confirmed (all legitimate contexts use Society-layer coordination primitives).
- §3.14 AcceptSpec FrameError-on-failure semantic: confirmed broadly (every hard-criterion context benefits).
- §3.18 gloss=mechanism restatement for Hypothesis: confirmed — the current mechanism is lazy. Broad-use sketch gives a concrete rewrite: distinguish from Claim and Assumption via testability.

**New audit items surfaced in batch 3.**
5. **`Act` invariants may be over-specified.** "All Acts must be authorized, logged, and potentially reversible" — "authorized" and "logged" pass the broad-use test (every descendant needs them). "Potentially reversible" is actually a marker, not an invariant — the marker system for reversibility vs. irreversibility is what descendants use; the invariant as stated is weak. Probably fine, but worth flagging.
6. **`Axiom`'s layer placement.** Broad use spans Mind (mathematical axioms — pure reasoning) and Society (constitutional axioms — community acceptance). Current Society/Protocols is defensible for the "community accepts" angle. No change proposed, but worth noting as ambiguity point.
7. **`RigorousSolver` mechanism might still be under-specified.** §3.14 rewrote to encode the ceremony inline ("Mandates full five-surface contract with non-compensatory acceptance gates..."). Broad-use passes but the mechanism doesn't yet name the specific verification primitives (Probe, SocraticLoop). Current mechanism text references them via `{{probe}}`/`{{socratic_loop}}`, so structural deps are there; just noting the mechanism could be tightened on restatement.
8. **`SolverRoot` Pathway Memory coupling.** Every SolverRoot needs Pathway Memory per §3.14 update. Broad-use confirms — routing compounds at the apex. But does PathwayMemory become a *required dependency* of SolverRoot? Currently §3.14 says "Used by SolverRoot, but not exclusive to it" for PathwayMemory. If every SolverRoot descendant needs it, should SolverRoot `composes_with` PathwayMemory explicitly? Worth flagging.

Batch 3 brings total analyzed to 60 patterns. Next batch target: Society/Protocols interior (114 patterns, the largest category), Mind/Memory beyond Cache/Stigmergy, Mind/Inference interior, and more verification-stack descendants.

---

## Batch 4 — Mind/Memory + Mind/Inference + Physics/Time interior

## 61. `Scratchpad` · Mind/Memory · R0T2

**Intended**: working-memory region for intermediate reasoning steps.
**Future**: any hidden-from-output scratch-work space.
**Broad-use contexts**: chain-of-thought traces, calculator tape, draft-before-publish workspaces, LLM inner monologue, debugging print statements, analyst workings, creative sketching.
**Every context needs**: isolation from main output, writability by the agent, persistence across the reasoning session.
**Varies**: size limit, eviction policy, inspectability by others (debug vs fully hidden), persistence after session ends, encryption.
**Extension**: `VisibleScratchpad`, `EncryptedScratchpad`, `PersistentScratchpad`, `EvictionBoundedScratchpad`.

## 62. `ChunkMerge` · Mind/Memory · R2T1

**Intended**: cognitive compression by grouping related items into named chunks.
**Future**: any hierarchical working-memory compression.
**Broad-use contexts**: CoT summarization, context compression for long contexts, named-function abstraction in reasoning, pattern-recognition into chunks, information hierarchization.
**Every context needs**: grouping criterion, chunk naming, hierarchy structure, merge/split semantics.
**Varies**: grouping method (semantic similarity, temporal proximity, structural), chunk size, retention of original items vs discard, lossy vs lossless.
**Extension**: `SemanticChunkMerge`, `TemporalChunkMerge`, `LossyChunkMerge`.

## 63. `BeliefTracking` · Mind/Memory · R2T2

**Intended**: epistemic version control — track what was believed before and after evidence.
**Future**: any belief-revision-with-history artifact.
**Broad-use contexts**: prediction markets, forecasting calibration, scientific hypothesis tracking, debugging belief-state machines, mind-change provenance for auditing.
**Every context needs**: prior state pinning, posterior tracking, `supersedes` edge on belief shift, surprisal quantification.
**Varies**: shift threshold, compression policy (full history vs delta), access control, replay support.
**Extension**: `FullHistoryBeliefTracking`, `DeltaCompressedBeliefTracking`, `AuditableBeliefTracking`.

## 64. `HolographicShard` · Mind/Memory · R0T1

**Intended**: context-preserving slice — sub-tasks contain a reference to the global goal.
**Future**: any fragment carrying reconstructability of the whole.
**Broad-use contexts**: distributed task decomposition, multi-agent coordination shards, federated learning samples, document chunks with source metadata, hologram reconstruction analogy.
**Every context needs**: parent_goal_hash, intent_summary, constraint_inheritance. All three are load-bearing — without them local action can't verify global alignment.
**Varies**: recovery detail (approximate vs exact), compression of the "seed," shard granularity.
**Extension**: `ApproximateHolographicShard`, `ExactReconstructableShard`, `VerifiedShard`.

## 65. `ExperienceSharding` · Mind/Memory · R0T1

**Intended**: split agent into specialist sub-agents when context fills, preserving history.
**Future**: any capacity-driven specialization-by-splitting operation.
**Broad-use contexts**: context-length-driven LLM splitting, worker colony specialization, memory hierarchy tiering, historical-context archival, team specialization over time.
**Every context needs**: splitting trigger (capacity threshold), active vs archival split, history preservation.
**Varies**: splitting criterion (temporal, topical, role), archival access protocol, active-to-archival handoff semantics, resurrection policy.
**Extension**: `TemporalSharding`, `TopicalSharding`, `HybridSharding`.

## 66. `ConfidenceCalibrate` · Mind/Inference · R2T2

**Intended**: align subjective confidence with observed frequency.
**Future**: any calibration-of-subjective-probability operation.
**Broad-use contexts**: forecaster calibration, ML model calibration (Platt scaling), probabilistic classifier tuning, expert-judgment aggregation, prediction-market participant self-tuning.
**Every context needs**: track record (predictions + outcomes), calibration function, adjustment mechanism.
**Varies**: track-record horizon, calibration method (Platt, isotonic, Bayesian), update frequency, asymmetric over/under correction.
**Extension**: `IsotonicConfidenceCalibrate`, `BayesianConfidenceCalibrate`, `RollingWindowCalibrate`.

## 67. `EpistemicCalibrate` · Mind/Inference · R2T1

**Intended**: structural confidence decay with prediction horizon.
**Future**: any certainty-fading-over-time mechanism.
**Broad-use contexts**: forecasting confidence intervals, LLM claim hedging over long horizons, scientific prediction decay, planning uncertainty cones, weather forecast confidence.
**Every context needs**: initial confidence, decay function, time axis.
**Varies**: decay function shape (exponential, linear, custom), reset events, per-claim vs global.
**Extension**: `ExponentialDecayCalibrate`, `LinearDecayCalibrate`, `EventResetCalibrate`.

## 68. `OntologyAdapt` · Mind/Inference · R1T1

**Intended**: restructure categorical framework when data defies current ontology (Piagetian accommodation).
**Future**: any structural belief-revision operation.
**Broad-use contexts**: ML concept drift handling, scientific paradigm shift modeling, scheme accommodation in pedagogy, semantic drift in language models, category-system overhaul.
**Every context needs**: trigger detection (defying classification), restructure event, new-root-category creation.
**Varies**: restructure aggressiveness (local vs global), rollback policy if restructure fails, migration semantics for existing data.
**Extension**: `GradualOntologyAdapt`, `RevolutionaryOntologyAdapt`, `RollbackSafeOntologyAdapt`.

## 69. `ProphetFanOut` · Mind/Inference · R1T1

**Intended**: high-fanout causal simulation across branching timelines.
**Future**: any multi-timeline exploration with bias toward low-probability tails.
**Broad-use contexts**: Monte Carlo simulation, scenario planning, risk analysis, red-teaming (adversarial timelines), decision-tree evaluation, robust-outcome analysis.
**Every context needs**: branch generator, timeline cost function, tail-exploration bias (unlike standard chain-of-thought which follows likely paths).
**Varies**: fanout breadth, pruning policy, aggregation method, tail-weighting strategy.
**Extension**: `MonteCarloFanOut`, `AdversarialFanOut`, `ImportanceSampledFanOut`.

## 70. `RegimeSense` · Mind/Inference · R2T1

**Intended**: detect structural breaks — when the generative process underlying reality has changed.
**Future**: any distribution-shift detector.
**Broad-use contexts**: ML concept drift detection, financial regime detection, model-staleness alerts, changing-environment adaptation, scientific anomaly detection.
**Every context needs**: internal model prediction, observed reality, divergence metric (Regime Stability Score), threshold for triggering.
**Varies**: window size, metric choice (KL divergence, RSS, surprisal), threshold adaptation, trigger action.
**Extension**: `BayesianRegimeSense`, `WindowedRegimeSense`, `AdaptiveThresholdRegimeSense`.

## 71. `SurprisalUpdate` · Mind/Inference · R2T1

**Intended**: learn weighted by prediction-failure magnitude (learn most from what confused you most).
**Future**: any gradient-weighted-by-surprise update.
**Broad-use contexts**: online ML fine-tuning, human learning from unexpected outcomes, RL reward-surprise weighting, forecaster self-update, Bayesian model updating.
**Every context needs**: prediction, observation, surprisal computation (-log P(observed|predicted)), update magnitude proportional to surprisal.
**Varies**: what gets updated (weights, embeddings, context), update rule specifics, clamping to avoid runaway updates.
**Extension**: `WeightedSurprisalUpdate`, `ClampedSurprisalUpdate`, `EmbeddingSurprisalUpdate`.

## 72. `SurvivorCorrect` · Mind/Inference · R2T1

**Intended**: account for silent failures in data (survivorship bias correction).
**Future**: any base-rate-aware learning that avoids surviving-examples bias.
**Broad-use contexts**: investment analysis (surviving funds only), scientific study design (published vs drawer), ML training (learning from labeled success only), case-study analysis, historical reasoning.
**Every context needs**: explicit question "am I seeing only successes?", base-rate estimation, failure inclusion.
**Varies**: failure-detection method, base-rate estimation technique, correction weighting.
**Extension**: `ExplicitFailureSearchCorrect`, `StatisticalSurvivorCorrect`, `DenominatorCorrect`.

## 73. `BaseRateInclude` · Mind/Inference · R2T1

**Intended**: anchor prior probability before evaluating specific case (outside view).
**Future**: any vividness-resistant probabilistic reasoning.
**Broad-use contexts**: forecasting, medical diagnosis, startup evaluation, strategic planning, anti-anecdotal-reasoning discipline, Fermi estimation.
**Every context needs**: base rate for the reference class, adjustment rule for case-specific evidence, resistance to vivid details.
**Varies**: reference class definition, evidence weighting, subjective base-rate estimation when data is sparse.
**Extension**: `ReferenceClassBaseRate`, `BayesianBaseRateInclude`, `FermiBaseRateInclude`.

## 74. `LayeredCheck` · Mind/Inference · R2T2

**Intended**: hierarchical verification — existence → schema → semantics, with early-halt.
**Future**: any cost-escalation-aware verification ladder.
**Broad-use contexts**: input validation pipelines, defensive parsing, API request validation, UI form submission, compiler error cascades, test-suite ordering (cheap tests first).
**Every context needs**: layered hierarchy (cheap→expensive), early-halt on lower-layer failure, gate sequence.
**Varies**: layer definitions, halt vs continue-with-warning behavior, layer cost estimation, skip conditions.
**Extension**: `StrictLayeredCheck`, `AdaptiveLayeredCheck`, `ParallelLayeredCheck` (some layers concurrent).

## 75. `CausalBarrier` · Physics/Time · R0T1

**Intended**: buffer messages until causal dependencies met (never see impossible state).
**Future**: any causal-consistency enforcement mechanism.
**Broad-use contexts**: distributed systems (vector clocks), eventual consistency stores, message queues with causal order, game-state replication, collaborative editing (OT/CRDT).
**Every context needs**: buffer, dependency tracking per message, release rule (all predecessors seen).
**Varies**: dependency representation (vector clock, happens-before, explicit edges), buffer size limits, timeout policy, stale-dependency garbage collection.
**Extension**: `VectorClockBarrier`, `TimedCausalBarrier`, `BoundedBufferBarrier`.

## 76. `Cooldown` · Physics/Primitives · R0T1

**Intended**: mandatory delay between repeated actions.
**Future**: any rate-limiting-via-minimum-interval mechanism.
**Broad-use contexts**: API rate limits, UI button debouncing, game ability cooldowns, retry-after headers, service-request throttling, anti-spam measures, circuit breakers.
**Every context needs**: action identity, minimum interval duration, timer start event.
**Varies**: per-action-type independent vs shared, queue-on-violation vs reject, global vs user-scoped, adaptive.
**Extension**: `PerUserCooldown`, `AdaptiveCooldown`, `QueuingCooldown`, `GlobalCooldown`.

## 77. `Hysteresis` · Physics/Primitives · R0T2

**Intended**: prevent oscillation via asymmetric state-transition thresholds.
**Future**: any noise-robust binary-switching mechanism.
**Broad-use contexts**: thermostats, circuit breakers, trigger filtering, alert deduplication, auto-scaling thresholds, feature-flag rollout guards, Schmitt triggers.
**Every context needs**: upper threshold (A→B), lower threshold (B→A), gap between them.
**Varies**: threshold values, adaptivity, multi-state variants, reset mechanisms.
**Extension**: `AdaptiveHysteresis`, `TriStateHysteresis`, `ResetableHysteresis`.

## 78. `Kairos` · Mind/Strategy · R2T1

**Intended**: sense the opportune moment via aggregated environmental signals.
**Future**: any "timing is right" detection mechanism.
**Broad-use contexts**: trade-timing signals, product-launch readiness, political-moment sensing, conversational-interruption timing, game-engagement detection.
**Every context needs**: signal sources, aggregation function, readiness threshold, boolean yield.
**Varies**: signal weighting, time-window, false-positive cost, actionability horizon.
**Extension**: `TradingKairos`, `ConversationalKairos`, `AdaptiveKairos`.

## 79. `Cyclic` · Physics/Time · R2T1 (post-§3.18 topology unification → Infrastructure/Data Structures)

**Intended**: topology permitting feedback loops.
**Future**: any topology with legitimate backward edges.
**Broad-use contexts**: feedback-loop systems, iterative refinement, state machines with cycles, recursive optimization, control loops.
**Every context needs**: edge structure permitting backward references, loop-termination mechanism (explicit or implicit).
**Varies**: cycle count bounds, termination criteria, cycle detection, shared-state vs isolated-iteration.
**Extension**: `BoundedCyclic`, `UnboundedCyclic`, `SelfCorrectingCyclic`.
**Note for audit**: §3.18 moves Cyclic to Infrastructure/Data Structures alongside Chain/Tree/DAG. Broad-use validates — it's a topology shape, not a physics primitive.

## 80. `Parallel` · Physics/Time · R0T1 (post-§3.18 topology unification → Infrastructure/Data Structures)

**Intended**: concurrent execution with no ordering guarantee.
**Future**: any non-ordered simultaneous topology.
**Broad-use contexts**: thread pools, async/await patterns, map-reduce map phase, multi-agent parallel action, ensemble inference, GPU parallelism.
**Every context needs**: concurrent executable slots, absence of ordering constraint.
**Varies**: parallelism degree, synchronization points, shared-state access model, failure aggregation.
**Extension**: `SyncedParallel`, `IsolatedParallel`, `HierarchicalParallel`.
**Note for audit**: §3.18 moves Parallel to Infrastructure/Data Structures. Broad-use validates.

---

## Observations from batch 4

**More validations.**
- §3.18 topology unification (Cyclic, Parallel → Infrastructure/Data Structures): confirmed by broad-use — both are topology shapes, not physics-substrate primitives.
- `HolographicShard`'s three required fields (parent_goal_hash, intent_summary, constraint_inheritance) are all load-bearing — good example of a pattern where the broad-use floor is higher than minimum.
- `LayeredCheck` as Mind/Inference seems correct — though the mechanism itself is a kind of meta-verification, the cognitive operation (ordering checks by cost) is Mind-layer.

**New audit items surfaced in batch 4.**
9. **`Kairos` placement feels close to Mind/Inference rather than Mind/Strategy.** It's doing signal aggregation + threshold detection, which is inference-shaped. But "sensing the opportune moment" does drive strategic action, so Strategy is defensible. Marginal — leave as-is.
10. **`ProphetFanOut` might want explicit reference to Tree or DAG.** The mechanism uses branching timeline structure; §3.19 reference-wiring did Cache/LatentAttachment/ContextFirst/MonotonicCounter/CommitmentDevice but didn't check topology-pattern wiring. Worth flagging for a future wiring pass.
11. **`Hysteresis` could reference `Dampen`.** The mechanism says "uses a Dampen effect" but via template syntax. Declared dependency? Worth spot-checking; this is the kind of template-vs-declared gap §4's broader-reference-density pass would catch.
12. **`OntologyAdapt` references `OntologyHandshake` via template** — similar potential declared-dep gap.
13. **`Scratchpad`'s isolation is load-bearing** — not currently declared as an invariant in its mechanism text (just prose). Could be tightened to an invariant: "scratchpad content is writable by the owning agent only." Minor.

Total analyzed: 80 patterns. Remaining: 349. Next batch will target more Society/Protocols interior (the largest remaining category) and Infrastructure/Verification patterns.

---

## Batch 5 — Society/Economics + Society/Governance + Infrastructure/Verification

## 81. `Award` · Society/Economics · R1T1

**Intended**: formal acceptance of a Bid, triggering Contract creation.
**Future**: any "offer accepted" state-transition event.
**Broad-use contexts**: procurement awards, auction wins, grant approvals, job offer acceptances, hackathon prize grants, service contract awards.
**Every context needs**: accepted Bid reference, Contract creation, value lock (HeldRelease), state transition from Negotiation to Execution.
**Varies**: signature requirements (bilateral, notarized, blockchain-attested), collateral terms, revocation semantics, partial awards.
**Extension**: `SealedAward`, `ConditionalAward`, `PartialAward`.

## 82. `ExchangeRate` · Society/Economics · R1T1

**Intended**: conversion ratio between distinct Value types at a specific time.
**Future**: any unit-conversion ratio artifact.
**Broad-use contexts**: currency FX, compute-token conversions, attention-market rates, time-vs-money tradeoffs, preference-aggregation weightings, protocol-bridge rates.
**Every context needs**: source Value type, target Value type, ratio, validity timestamp.
**Varies**: volatility tracking, confidence interval, update frequency, market depth, bid-ask spread.
**Extension**: `VolatileExchangeRate`, `PeggedExchangeRate`, `OracleExchangeRate`.

## 83. `MarginalValueRule` · Society/Economics · R1T2

**Intended**: economic stop-condition for recursion — go deeper only if expected-improvement > incremental-cost.
**Future**: any ROI-based continuation decision.
**Broad-use contexts**: solver-depth decisions, research-effort stopping, optimization-iteration bounds, tree-search pruning, cognitive-effort allocation, meeting-length stopping.
**Every context needs**: expected-improvement estimator, cost estimator, comparison rule.
**Varies**: estimation method, cost-time-horizon, risk adjustment, stopping-threshold calibration, reset on surprise.
**Extension**: `BayesianMarginalValueRule`, `RiskAdjustedMarginalValueRule`, `AdaptiveMarginalValueRule`.
**Note**: this is the economic counterpart to ComputeBudget — both stop runaway cognition but on different axes (MVR is per-step, ComputeBudget is total-resource).

## 84. `ValuePeg` · Society/Economics · R1T1

**Intended**: agreeing on an ExchangeRate between internal utilities and a shared numeraire.
**Future**: any utility-function translation agreement.
**Broad-use contexts**: multi-agent bargaining, preference-aggregation protocols, cross-domain trade, inter-organization coordination, cross-species analogies (humans vs AI agents).
**Every context needs**: two utility types, agreed ExchangeRate, binding-for-duration semantic.
**Varies**: renegotiation mechanism, private-utility disclosure requirements, peg break semantics, composition with other pegs.
**Extension**: `NegotiatedValuePeg`, `TimedValuePeg`, `MarketBasedValuePeg`.

## 85. `LivedProof` · Society/Economics · R2T2

**Intended**: process demonstrates thesis — the execution IS the evidence.
**Future**: any self-validating-via-enactment argumentation pattern.
**Broad-use contexts**: dogfooding demonstrations, recursive-validation arguments, teaching-by-modeling, manifesto writing that enacts its own claims, meta-circular reasoning.
**Every context needs**: thesis being argued, process that enacts it, observer who can verify the enactment matches the thesis.
**Varies**: observer type (self, peer, neutral), enactment fidelity requirements, fallback if enactment fails to prove thesis.
**Extension**: `DogfoodedLivedProof`, `PeerVerifiedLivedProof`, `RecursiveLivedProof`.

## 86. `Role` · Society/Governance · R1T1

**Intended**: named bundle of permissions and responsibilities assigned to an agent.
**Future**: any identity-capability decoupling artifact.
**Broad-use contexts**: RBAC systems, job titles, organizational hats, game character classes, agent mode switching, team rotation, on-call schedules.
**Every context needs**: role name, permission set, responsibility set, assignment binding to agent.
**Varies**: time-bounded vs permanent, delegation support, inheritance/composition, context-scoping, revocation semantics.
**Extension**: `TimedRole`, `DelegatableRole`, `ContextualRole`, `CompositeRole`.

## 87. `Responsibility` · Society/Governance · R1T1

**Intended**: continuous ownership of a system invariant (standing wave, not event).
**Future**: any standing-obligation maintenance contract.
**Broad-use contexts**: on-call ownership, SLA maintenance, ethical responsibility, stewardship contracts, fiduciary duty, bug-bucket ownership.
**Every context needs**: invariant being maintained, scope of authority, agent owning it, liability semantics, heartbeat proof that invariant holds.
**Varies**: escalation paths, handover protocol, scope-expansion rules, externality ownership.
**Extension**: `OnCallResponsibility`, `FiduciaryResponsibility`, `TransferableResponsibility`.

## 88. `TriGate` · Society/Governance · R0T1

**Intended**: Red/Yellow/Green flow control over a Judge-or-Condition.
**Future**: any three-state gating primitive (halt/debt/pass).
**Broad-use contexts**: PR merge gates (blocking/warning/passing), compliance triage, quality gating with conditional acceptance, deployment green-light systems, approval workflows with "approved with caveats."
**Every context needs**: the underlying Judge or Condition, the three-state mapping, the debt ledger for Yellow-state obligations.
**Varies**: thresholds for Red/Yellow/Green boundary, debt-ledger discipline, escalation of Yellow accumulation, retry semantics on Red.
**Extension**: `FlowControlTriGate`, `AuditableTriGate`, `AdaptiveTriGate`.

## 89. `Elect` · Society/Governance · R2T1

**Intended**: establish leadership via nominate → vote → invest phases.
**Future**: any consent-based leadership formalization.
**Broad-use contexts**: political elections, team-lead rotation, council elections, DAO governance, multi-agent leadership selection, committee chair appointments.
**Every context needs**: Ballot, quorum, nomination phase, vote phase, invest phase, succession planning.
**Varies**: nomination eligibility rules, voting method (FPTP, ranked, approval), term length, recall mechanism.
**Extension**: `FPTPElect`, `RankedChoiceElect`, `WeightedStakeElect`, `RotatingElect`.

## 90. `Disband` · Society/Governance · R1T1

**Intended**: graceful group termination with state handling.
**Future**: any "this group is done" coordinated dissolution.
**Broad-use contexts**: project completion, team disbanding, DAO sunset, temporary-coalition dissolution, terminated-service cleanup, Kubernetes deployment termination.
**Every context needs**: termination signal, member-notification, state disposition plan, resource release, ACK-confirmation from all members.
**Varies**: snapshot-for-re-formation vs permanent, resource-disposition (return-to-owner vs pool), member-ejection for non-ACK, dissolution-under-duress vs consensual.
**Extension**: `ArchiveDisband` (preserves snapshot), `ConsensualDisband`, `EmergencyDisband`.

## 91. `Gardener` · Society/Economics · R0T2

**Intended**: stewardship and maintenance — non-transactional actions for long-term health.
**Future**: any maintenance-role without immediate payoff.
**Broad-use contexts**: open-source maintainer role, wiki-gardening, codebase refactoring, community moderation, ecosystem-stewarding, janitorial work, meta-work.
**Every context needs**: stewardship scope, maintenance actions (refactor, organize, praise), non-payoff-contingent action semantic.
**Varies**: scope size, incentive alignment (if any), burnout prevention, succession planning for the gardener role.
**Extension**: `CommunityGardener`, `CodebaseGardener`, `EcosystemGardener`.

## 92. `WorldTransparent` · Society/Governance · R0T1

**Intended**: design constraint assuming all state and actions are publicly visible.
**Future**: any "assume no secrecy" architectural discipline.
**Broad-use contexts**: public-blockchain systems, open-source governance, radical-transparency organizations, auditability-first system design, shame-based compliance regimes.
**Every context needs**: universal visibility assumption, commitment to auditable systems over access-controlled ones, composition with ExplainBeacon.
**Varies**: redaction policy for PII, time-delayed visibility (embargoed publication), visibility granularity (read-only, queryable, streamable).
**Extension**: `RedactedWorldTransparent`, `EmbargoedWorldTransparent`, `StreamableWorldTransparent`.

## 93. `OathBind` · Infrastructure/Verification · R1T2

**Intended**: automated binding with cryptographic pre-commitment to penalty-enforced rules.
**Future**: any self-enforcing-contract mechanism.
**Broad-use contexts**: smart contracts with slashing, security deposits, bail bonds, performance bonds, cryptoeconomic penalty systems, automated compliance enforcement.
**Every context needs**: rule set (the oath), cryptographic commitment, penalty specification, audit mechanism for violations.
**Varies**: penalty type (slashing, reputation, access revocation), audit frequency, dispute process, multi-party binding.
**Extension**: `SlashingOathBind`, `ReputationOathBind`, `MultiPartyOathBind`.

## 94. `Permission` · Infrastructure/Data Structures · R1T1

**Intended**: atomic authorization grant.
**Future**: any access-control unit.
**Broad-use contexts**: file-system permissions, API scopes, OAuth tokens, role-capability grants, feature-access grants, capability-based security.
**Every context needs**: granting identity, recipient identity, scope (what is permitted), act-or-artifact target.
**Varies**: expiry, delegation support, revocation mechanism, granularity (coarse vs fine-grained), composability (multiple permissions aggregate).
**Extension**: `TimedPermission`, `DelegatedPermission`, `CapabilityPermission`, `ScopedPermission`.

## 95. `CompatibilityCheck` · Infrastructure/Verification · R0T1

**Intended**: binary verification of schema/hash compatibility between two entities.
**Future**: any "can these interact?" pre-flight check.
**Broad-use contexts**: API version compatibility, protocol handshake, agent-discovery filtering, plugin compatibility, schema evolution checks, tool interoperability.
**Every context needs**: two entities (agents, artifacts, protocols), comparison function, binary yield.
**Varies**: comparison strictness (structural match vs semantic match vs hash match), translation-available fallback, per-field compatibility reporting.
**Extension**: `HashCompatibilityCheck`, `StructuralCompatibilityCheck`, `SemanticCompatibilityCheck`.

## 96. `ExplainBeacon` · Infrastructure/Verification · R1T2

**Intended**: real-time readable intent broadcast (telemetry of "why").
**Future**: any human-readable narrative emitted alongside machine logs.
**Broad-use contexts**: LLM agent explanations, trading-system intent logs, robotic intent broadcasts, autonomous-system transparency narratives, debugger annotations.
**Every context needs**: human-readable narrative, machine-readable companion log, pre-irreversible-action emit-timing.
**Varies**: verbosity level, privacy redaction, language, channel (email, Slack, UI widget, console).
**Extension**: `VerboseExplainBeacon`, `RedactedExplainBeacon`, `MultiChannelExplainBeacon`.

## 97. `InputGuard` · Infrastructure/Verification · R0T2

**Intended**: sanitize inputs before they reach a sensitive component.
**Future**: any ingress-filtering boundary.
**Broad-use contexts**: API input validation, SQL-injection prevention, prompt-injection guards (for LLM apps), form-submission filters, message-broker content filters.
**Every context needs**: schema/constraint to enforce, violation handler (fail-closed), input stream being guarded.
**Varies**: schema language, coercion vs reject, rate limiting integration, whitelist vs blacklist approach.
**Extension**: `SchemaInputGuard`, `PromptInjectionGuard`, `RateLimitedInputGuard`.

## 98. `OutputGuard` · Infrastructure/Verification · R0T2

**Intended**: post-generation content filter for PII/toxicity at egress.
**Future**: any egress filter on generated content.
**Broad-use contexts**: LLM safety filters, content moderation, PII redaction, toxicity classification, compliance-disclosure review, export-control filtering.
**Every context needs**: content to scan, detectors (PII, toxicity, etc.), threshold-based mitigation (redact/reject), scan-before-egress timing.
**Varies**: detector set, threshold values, mitigation strategy (redact vs reject vs rewrite), audit logging of interventions.
**Extension**: `PIIOutputGuard`, `ToxicityOutputGuard`, `ExportControlOutputGuard`, `ComprehensiveOutputGuard`.

## 99. `SpotAudit` · Infrastructure/Verification · R1T1

**Intended**: probabilistic random-sample audit with Merkle proof.
**Future**: any "keep honest via random spot checks" verification.
**Broad-use contexts**: tax audits, compliance spot-checks, distributed-system liveness checks, integrity verification, ML-model red-teaming, dataset integrity sampling.
**Every context needs**: random sampling over target's state, Merkle proof for sampled slice, comparison against expected.
**Varies**: sample frequency, sample size, unpredictability requirements (prevent cheating), escalation on mismatch.
**Extension**: `CryptographicSpotAudit`, `AdaptiveFrequencySpotAudit`, `AdversarialSpotAudit`.

## 100. `Consensus` · Society/Governance · R0T1

**Intended**: distributed agreement on a single data value or state transition.
**Future**: any safety-and-liveness coordination protocol.
**Broad-use contexts**: blockchain consensus, distributed DB consensus, multi-agent alignment, editorial decisions, scientific paper reviews, group-decision protocols.
**Every context needs**: proposal mechanism, vote orchestration, quorum validation, safety (one value decided) and liveness (eventually decides).
**Varies**: Byzantine tolerance, fault model, timeout semantics, fairness guarantees, progress conditions, leader-based vs leaderless.
**Extension**: `RaftConsensus`, `PBFTConsensus`, `TendermintConsensus`, `PaxosConsensus`.

---

## Observations from batch 5

**Patterns that are well-specified at foundation level**: Award, Role, TriGate, Permission, CompatibilityCheck, SpotAudit — each has a clear usability floor and extensibility ceiling. Descendants populate specializations without breaking the foundation.

**Patterns where broad-use surfaces edge cases**:

14. **`MarginalValueRule` might double-declare with `ComputeBudget`.** Both stop runaway cognition. MVR is per-step (deeper or not?); ComputeBudget is total-resource (how much overall?). They're complementary but overlap in the "stop thinking" semantic. Worth flagging whether the two patterns compose (MVR `composes_with` ComputeBudget?) or are alternatives. Currently unclear in the graph.

15. **`LivedProof`'s "process demonstrates thesis" semantic is narrow.** Broad-use sketch works but the audit should check whether the current mechanism is too-specific to rhetorical/epistemic uses. Could it scale to "the commit history IS the argument that the code is well-maintained"? Probably yes, but the mechanism text is framed around essay-writing contexts.

16. **`Disband` `composes_with` `EjectionSeat` via template** — potential declared-dep gap. Worth checking.

17. **`Gardener` is a Macro** (per its mechanism: "Macro for stigmergy(care)"). Worth validating that the declared `composes_with` edges match the macro expansion. Macros are a potential source of signature-without-fulfillment drift (per §3.12).

18. **`OathBind` is in Infrastructure/Verification** but it's a cryptoeconomic coordination primitive. Might belong in Society/Protocols or Society/Governance. The fact that every broad-use context is multi-agent (slashing, performance bonds) argues for Society-layer placement. Worth considering in a future layer-review pass.

19. **`Consensus` at R0T1**: given the huge variety of Consensus algorithms (Raft, PBFT, etc.), having Consensus at Ring 0 Tier 1 is appropriate — it's the abstract interface. Its descendants can fill in the rich algorithm-specific details.

Total analyzed: 100 patterns — approaching a quarter of the library. Remaining: 329. Next batch will target the remaining Physics/Primitives (most covered), Mind/Strategy interior (66 patterns, many uncovered), and more Society/Protocols.

---

## Batch 6 — Mind/Strategy interior

## 101. `AnalogyBridge` · Mind/Strategy · R2T1

**Intended**: solve a novel problem by mapping a structural analogy from a different domain.
**Future**: any cross-domain solution transfer.
**Broad-use contexts**: ant-colony → system architecture, biological → engineering, physics → economics, historical → contemporary, code-smell → cognitive-bias, patterns across sciences.
**Every context needs**: source domain, target domain, structural-isomorphism identification, mapping mechanism.
**Varies**: domain pair specifics, fidelity of isomorphism (loose vs rigorous), automated vs manual mapping, verification of analogy's validity.
**Extension**: `BiologicalAnalogyBridge`, `HistoricalAnalogyBridge`, `StructuralAnalogyBridge`.
**Note for audit**: §3.20 adds `AnalogyBridge → references LatentAttachment`. Broad-use confirms — the mechanism says "searches its training data for a structural analogy," which is embedding-backed search.

## 102. `NoiseInjection` · Mind/Strategy · R1T1

**Intended**: break local optima by deliberate noise injection when agent detects looping.
**Future**: any controlled-randomization escape mechanism.
**Broad-use contexts**: ML exploration (epsilon-greedy), simulated annealing, creative writing (forced random words), conversation fresheners, evolutionary mutation, escape from rumination.
**Every context needs**: loop/stagnation detector, noise source, injection mechanism, return-to-coherent-trajectory after injection.
**Varies**: noise magnitude (temperature), noise source (PRNG, oblique strategies, user prompt), detection threshold, cooldown after injection.
**Extension**: `TemperatureNoiseInjection`, `ObliqueStrategyInjection`, `AdaptiveNoiseInjection`.

## 103. `Optimize` · Mind/Strategy · R1T1

**Intended**: iterative parameter/structure adjustment to maximize an objective function.
**Future**: any numerical-or-structural optimization operation.
**Broad-use contexts**: gradient descent, hyperparameter tuning, evolutionary algorithms, reinforcement-learning policy optimization, compiler optimization, resource allocation, product-design refinement.
**Every context needs**: objective function (metric), candidate generation, evaluation, selection.
**Varies**: local vs global search, gradient availability, convergence criteria, exploration/exploitation balance.
**Extension**: `GradientOptimize`, `EvolutionaryOptimize`, `BayesianOptimize`, `MultiObjectiveOptimize`.

## 104. `RedTeam` · Mind/Strategy · R2T1

**Intended**: adversarial stress testing via attacker-mindset exploitation search.
**Future**: any role-reversal-based weakness discovery.
**Broad-use contexts**: security penetration testing, AI safety evaluation, devil's-advocate debate, wargaming, competitive analysis, pre-publication critique, regulatory stress tests.
**Every context needs**: target system, attacker persona adoption, exploit-path documentation, severity+likelihood classification, switch-back-to-defender for patching.
**Varies**: adversarial depth (ethical hacker vs nation-state model), automation level, scope (single vulnerability vs systemic), coordination with defender.
**Extension**: `AutomatedRedTeam`, `FormalRedTeam`, `PairedRedTeam` (with blue team).

## 105. `Satisfice` · Mind/Strategy · R2T1

**Intended**: optimize for speed via threshold acceptance (first candidate meeting all minimums).
**Future**: any "good enough" termination rule.
**Broad-use contexts**: bounded rationality decisions, MVP product sizing, hiring decisions (first acceptable candidate), quick-return search, time-boxed optimization, sequential-choice selection.
**Every context needs**: minimum-acceptable criteria per dimension, sequential evaluation, accept-first-match semantic.
**Varies**: criteria strictness, evaluation order, fallback if no candidate meets criteria, recall allowance.
**Extension**: `TimeoutSatisfice`, `RelaxingSatisfice` (adjusts threshold over time), `RecallingSatisfice`.

## 106. `MentalSim` · Mind/Strategy · R2T2

**Intended**: System-2 predictive simulation via causal graph dry-runs.
**Future**: any before-act internal simulation.
**Broad-use contexts**: "what-if" analysis, chess move evaluation, strategic planning, debugging predictions, scientific theory testing, counterfactual reasoning, legal case analysis.
**Every context needs**: causal graph of target system, proposed action, prediction of state(t+1), isolation (dry-run doesn't affect real world).
**Varies**: graph fidelity, simulation depth, heuristic vs rigorous mode toggle, computational cost.
**Extension**: `HeuristicMentalSim`, `DeepMentalSim`, `AdversarialMentalSim`.

## 107. `PreMortem` · Mind/Strategy · R2T1

**Intended**: simulate catastrophic failure *before* execution to surface hidden risks.
**Future**: any prospective-hindsight exercise.
**Broad-use contexts**: project kickoff reviews, launch-readiness checks, scientific-experiment design, safety engineering, investment-decision review, strategic-plan stress tests.
**Every context needs**: assumed-failed state, "what went wrong?" generation, per-failure mitigation addition to plan or reconsider-approach option.
**Varies**: failure-scenario depth, defensiveness-neutralization technique, mitigation-addition policy, repeat frequency.
**Extension**: `AdversarialPreMortem`, `StatisticalPreMortem`, `QuickPreMortem`.

## 108. `Simulation` · Mind/Strategy · R0T1

**Intended**: sandboxed execution — fork world state, execute, discard, return outcome.
**Future**: any "try in a copy" mechanism.
**Broad-use contexts**: physics sims, software test fixtures, game sandboxes, multi-agent training environments, digital twins, Monte Carlo rollouts, counterfactual experimentation.
**Every context needs**: world state fork, isolated execution, outcome capture, original state preservation.
**Varies**: fork fidelity (shallow vs deep), execution time-bound, outcome richness, fork cost.
**Extension**: `PhysicsSimulation`, `MonteCarloSimulation`, `DigitalTwin`, `CounterfactualSimulation`.

## 109. `PURECheck` · Mind/Strategy · R1T1

**Intended**: canonical exploration protocol — layered TriGate triage on Parsimony, Novelty, Realizability, Expansiveness.
**Future**: any quadri-gate quality screening.
**Broad-use contexts**: pattern-mint evaluation, research proposal triage, design decision review, architectural proposal screening, scientific paper screening.
**Every context needs**: all four gates (Parsimony, Novelty, Realizable, Expansive) applied in sequence, Yellow-output Technical-Debt tracking, Red-on-any-gate termination.
**Varies**: gate threshold values, evaluator identity (self vs committee), debt-ledger integration, parallel vs sequential gate evaluation.
**Extension**: `ParallelPURECheck`, `LooseThresholdPURECheck`, `CommitteePURECheck`.

## 110. `PUREBrainstorming` · Mind/Strategy · R1T2

**Intended**: rigorous ideation protocol — Generate → PURECheck → PUREOptimization → Propose.
**Future**: any quality-filtered generative loop.
**Broad-use contexts**: R&D concept generation, invention flow, scientific hypothesis generation, design ideation, product-feature conception.
**Every context needs**: generator, PURECheck gate, PUREOptimization step, MechanisticDesignProposal output.
**Varies**: generator diversity, optimization depth, convergence criteria.
**Extension**: `ParallelPUREBrainstorming`, `TimeBoxedPUREBrainstorming`.

## 111. `OpportunityCost` · Mind/Strategy · R1T1

**Intended**: deduct foregone-alternative value from budget calculation.
**Future**: any alternative-valuation-aware decision framing.
**Broad-use contexts**: investment decisions, time-allocation decisions, product roadmap prioritization, resource-commitment analysis, career choices, scheduling trade-offs.
**Every context needs**: candidate option, best-forgone-alternative identification, cost calculation including foregone-value deduction.
**Varies**: alternative-space size, evaluation technique, uncertainty tracking in forgone value.
**Extension**: `ExpectedOpportunityCost`, `RegretWeightedOpportunityCost`, `MultiHorizonOpportunityCost`.

## 112. `HypothesisEngine` · Mind/Strategy · R2T3

**Intended**: automated scientific method cycle — Discover → Trace → Check → Stigmergy(publish).
**Future**: any self-driving inquiry loop.
**Broad-use contexts**: autonomous scientific research, self-improving AI, debugging automation, market-hypothesis testing, evolutionary-design search.
**Every context needs**: hypothesis generator, simulation-and-trace, consistency validator, publication mechanism.
**Varies**: domain specificity, cycle rate, validation rigor, publication protocol, inter-cycle learning.
**Extension**: `BayesianHypothesisEngine`, `CausalHypothesisEngine`, `MultiAgentHypothesisEngine`.

## 113. `EpistemicROI` · Mind/Strategy · R2T1

**Intended**: Value of Information analysis — only pursue learning tasks with positive VOI.
**Future**: any information-acquisition-cost decision.
**Broad-use contexts**: research-vs-act decisions, diagnostic-test ordering, A/B test decisions, experiment design, due-diligence depth, survey-vs-decide tradeoffs.
**Every context needs**: outcome space, decision-per-outcome mapping, "does outcome change decision?" test, cost estimation.
**Varies**: outcome-space enumeration method, decision-value quantification, risk-aversion tuning.
**Extension**: `BayesianEpistemicROI`, `RiskAdjustedEpistemicROI`, `FastEpistemicROI`.

## 114. `MetaCheck` · Mind/Strategy · R1T1

**Intended**: recursive self-verification of reasoning process itself.
**Future**: any "am I doing this right?" introspection mechanism.
**Broad-use contexts**: reasoning audits, agent self-correction, debugging your debugging, paper-review-of-a-review, meditative introspection, progress retrospectives.
**Every context needs**: pause from object-level work, audit questions ("making progress? approach sound? assumptions changed?"), course correction or continue.
**Varies**: trigger frequency, audit depth, recursion limit (to avoid infinite meta), integration with Reflexion.
**Extension**: `ScheduledMetaCheck`, `AnomalyTriggeredMetaCheck`, `DepthLimitedMetaCheck`.

## 115. `DesignArchitect` · Mind/Strategy · R1T2

**Intended**: strategic agent formulating MechanisticDesignProposals via adversarial robustification.
**Future**: any design-proposal-generating role.
**Broad-use contexts**: systems architecture, product design, scientific-proposal writing, policy design, organizational-change design, API design.
**Every context needs**: proposal formulation, adversarial method (SteelmanCheck + PreMortem), impact projection, clarity refinement (translate + summarize).
**Varies**: domain specificity, team-context vs solo, visualization requirements, iteration count.
**Extension**: `SystemsDesignArchitect`, `PolicyDesignArchitect`, `APIDesignArchitect`.

## 116. `TensionHold` · Mind/Strategy · R2T2

**Intended**: maintain contradictions without premature resolution.
**Future**: any "hold competing perspectives" epistemic discipline.
**Broad-use contexts**: ethical dilemmas, paradox management, scientific-debate navigation, multi-stakeholder negotiation, creative-tension preservation, dialectical reasoning.
**Every context needs**: Tension object binding contradictory inputs, downstream-decision block, release-on-reconciling-insight or timeout.
**Varies**: hold timeout, conflict detection threshold, reconciliation-seeking mechanism, fallback on timeout.
**Extension**: `TimedTensionHold`, `DialecticalTensionHold`, `EscalatingTensionHold`.

## 117. `AntifragileInversion` · Mind/Strategy · R0T1

**Intended**: redesign system so that a stressor becomes input fuel — invert sign of exposure.
**Future**: any "harm → fuel" conversion design.
**Broad-use contexts**: Taleb's antifragility examples (muscle from stress, immune learning from pathogens), adversarial training in ML, vaccine-informed immunity, failure-driven process improvement, crisis-as-opportunity framings.
**Every context needs**: stressor identification, causal graph of system, edge-sign-flip identification, redesign to use stressor as input.
**Varies**: flip mechanism specifics, detection of flippable edges, verification that redesign actually inverts, safety bounds (not every stress can be fuel).
**Extension**: `StructuralAntifragileInversion`, `AdaptiveAntifragileInversion`.

## 118. `DepthGovernor` · Mind/Strategy · R0T2

**Intended**: entropy-based stopping condition for recursion — depth as function of ambiguity.
**Future**: any uncertainty-gated-recursion control.
**Broad-use contexts**: solver-tree depth control, tree-search pruning, LLM chain-of-thought depth, recursive decomposition control, game-tree iterative deepening.
**Every context needs**: current plan entropy estimate, action-cost threshold, decompose-if-entropy-exceeds-threshold rule.
**Varies**: entropy estimation method, threshold calibration, per-branch vs global, reset on new information.
**Extension**: `BayesianDepthGovernor`, `AdaptiveDepthGovernor`, `MultiCriteriaDepthGovernor`.

## 119. `RegretMinimization` · Mind/Strategy · R2T3

**Intended**: safety-first decisions via Minimax loss-avoidance (not expected-value maximization).
**Future**: any worst-case-optimized decision rule.
**Broad-use contexts**: survival-critical decisions, catastrophe-avoidance strategies, conservative-investment framing, medical-triage under uncertainty, insurance-decision framing, power-law-exposed choices.
**Every context needs**: decision space, loss function, Minimax selection.
**Varies**: worst-case estimation (data-driven vs adversarial), risk-aversion coefficient, consideration of expected value alongside Minimax (hybrid).
**Extension**: `CVaRRegretMinimization`, `RobustRegretMinimization`, `HybridRegretMinimization`.

## 120. `Proprioception` · Society/Protocols · R2T3

**Intended**: self-location awareness within the task graph — "where am I in the recursion?"
**Future**: any self-monitoring-of-position mechanism.
**Broad-use contexts**: long-agent-session coherence, recursion-depth tracking, context-state awareness, multi-tool state management, long-running-process dashboards.
**Every context needs**: position tracking, state verification, depth-in-recursion measurement.
**Varies**: ping frequency, what's tracked (context, tool state, depth), integration with somatic_marker, fatigue detection.
**Extension**: `DeepProprioception`, `LightweightProprioception`, `FatigueAwareProprioception`.
**Note for audit**: `Proprioception` is in Society/Protocols. Broad-use analysis: it's a single-agent self-monitoring loop. Probably should be Mind/Memory or Mind/Strategy per §3.18's Society→Mind relocation pattern. Add to the §3.18 relocation list? Worth flagging.

---

## Observations from batch 6

**Strategy-category density makes broad-use calibration especially valuable.** Mind/Strategy has 66 patterns; many are named after specific heuristics (OpportunityCost, Satisfice, PreMortem). The broad-use test validates each because the heuristic name captures the *principle* and the mechanism captures the *operation*, with descendants for domain specifics.

**New audit items surfaced in batch 6.**
20. **`Proprioception` likely belongs in Mind, not Society.** Single-agent self-monitoring. Add to §3.18's Society→Mind relocation list.
21. **`DesignArchitect` has a specific handle — is it too narrow?** The handle reads like a role name rather than a pattern. But broad-use spans many design-proposal contexts, so the pattern content is generic. Handle might be fine.
22. **`HypothesisEngine` at Tier 3 (experimental).** Tier 3 is appropriate here — it's an ambitious composite. Good placement.
23. **`PUREBrainstorming` → `PURECheck` → `PUREOptimization`** — these are three layers of a family. Worth checking that `PUREBrainstorming` declares both as composes_with (likely already does; mechanism references both via template).
24. **`Simulation` at R0T1 with very short mechanism** — could be considered under-specified, but passes broad-use test: sandboxed fork+execute+discard is the definitional floor. Anything more specific belongs on descendants. Good example of "generalize at foundation."

Total analyzed: 120 patterns. Remaining: 309. The methodology continues to hold uniformly. Next batch: remaining Infrastructure (verification descendants, remaining data structures), Society/Protocols interior bulk, and a selection of the Mind/Reasoning patterns not yet covered.

---

## Batch 7 — Society/Protocols interior + Mind/Reasoning remaining

## 121. `Rollout` · Society/Protocols · R1T1

**Intended**: safe, reversible deployment with circuit breaking and emergency ejection.
**Future**: any progressive-release-with-rollback pattern.
**Broad-use contexts**: software deploys (canary, blue-green, rolling), policy rollouts, experiment launches, configuration changes, model deployments, feature-flag progressions.
**Every context needs**: spec extraction, build, circuit-breaker envelope, canary, ejection-on-breaker-trip, compensation for rollback.
**Varies**: canary fraction, breaker sensitivity, rollback granularity, observability integration.
**Extension**: `BlueGreenRollout`, `CanaryRollout`, `ProgressiveRollout`, `ShadowRollout`.

## 122. `MemeticSeed` · Society/Protocols · R1T1

**Intended**: viral propagation of semantic standards via economic subsidy.
**Future**: any adoption-via-incentive broadcast.
**Broad-use contexts**: protocol-standard propagation, open-source adoption, pattern-library evangelism, memetic engineering, ecosystem bootstrapping, convention setting.
**Every context needs**: standard being propagated, neighbor set, subsidy mechanism (favorable yield), broadcast channel.
**Varies**: subsidy magnitude, targeting precision, retractability, decay profile.
**Extension**: `TargetedMemeticSeed`, `DecayingMemeticSeed`, `ReciprocalMemeticSeed`.
**Note**: interesting economic pattern — "standards are adopted not because they are true, but because they are subsidized." The broad-use test captures the fact that this is how *most* standards spread, not just the one originally modeled.

## 123. `PropheticQuorum` · Society/Protocols · R1T1

**Intended**: two-stage consensus — align predictions first, then align values.
**Future**: any "shared reality then shared value" coordination pattern.
**Broad-use contexts**: scientific consensus, policy debate (predicted-consequences-first), multi-agent predictions, organizational planning, investment committee alignment.
**Every context needs**: prediction phase (agents simulate), prediction-match check, value phase (agents vote on desirability), halt-on-divergence.
**Varies**: prediction verification method, divergence threshold, model-alignment protocol on halt, weighting of predictions vs values.
**Extension**: `MarketPropheticQuorum` (prediction-market for phase 1), `BayesianPropheticQuorum`, `ThreePhasePropheticQuorum` (adds meta-alignment).

## 124. `Nucleate` · Society/Protocols · R1T1

**Intended**: emergent working groups from activity-density crossing a threshold.
**Future**: any "group forms when density sufficient" mechanism.
**Broad-use contexts**: ant-colony trail formation, community-formation around hashtags, research-cluster formation, market-formation, gang formation, emergent teams in open-source projects.
**Every context needs**: trace density tracking, density threshold, nucleation trigger, bond/join protocol.
**Varies**: density metric, threshold calibration, nucleation broadcast radius, bond semantics.
**Extension**: `HashTaggedNucleate`, `PhysicalProximityNucleate`, `InterestNucleate`.

## 125. `OntologyHandshake` · Society/Protocols · R1T2

**Intended**: negotiate shared definitions before data exchange.
**Future**: any term-alignment prelude to communication.
**Broad-use contexts**: cross-system data integration, human-human jargon alignment, multi-language translation setup, pidgin-protocol creation, cross-organizational knowledge integration.
**Every context needs**: definition-hash exchange, mismatch detection (CompatibilityCheck), negotiation phase, temporary shared dictionary.
**Varies**: dictionary scope, persistence (per-session vs lasting), negotiation protocol (iterative vs single-shot), fallback on irreconcilable divergence.
**Extension**: `PersistentOntologyHandshake`, `SessionOntologyHandshake`, `AutoOntologyHandshake`.

## 126. `IdentityHandshake` · Society/Protocols · R1T2

**Intended**: distinguish Peer from Principal — verify ontological origin to switch behavior modes.
**Future**: any "who am I talking to?" type identification mechanism.
**Broad-use contexts**: AI-vs-human identification, authenticated-vs-anonymous branching, service-vs-user detection, B2B-vs-B2C protocol selection, synthetic-vs-biological protocols.
**Every context needs**: Discover(identity) + Check(nature), mode-switching on result, cryptographic verification.
**Varies**: authentication strength, mode set, fallback on ambiguous identity, spoof resistance.
**Extension**: `StrongIdentityHandshake`, `OpportunisticIdentityHandshake`, `ZKIdentityHandshake`.

## 127. `LazyConsensus` · Society/Governance · R0T2

**Intended**: optimistic execution with retroactive verification (conflict resolution after-the-fact).
**Future**: any speed-over-safety coordination with deterministic conflict resolution.
**Broad-use contexts**: Apache committer model, git-flow, CRDT operations, eventual-consistency databases, optimistic locking, wiki edit flows.
**Every context needs**: optimistic-execution semantic, conflict-detection mechanism, deterministic rollback rule.
**Varies**: conflict-resolution policy, rollback complexity, window for revocation, audit trail.
**Extension**: `GitLazyConsensus`, `HighestIDLazyConsensus`, `TimestampLazyConsensus`.

## 128. `Resonate` · Society/Economics · R1T2

**Intended**: implicit coordination via signal amplification without explicit negotiation.
**Future**: any "alignment-via-mutual-adjustment" protocol.
**Broad-use contexts**: social mirroring, market sentiment, meme propagation, cultural drift, musical tempo sync, meditation co-sensing, team synchronization.
**Every context needs**: intent tags on actions, amplification/dampening observers, alignment detection via signal strength.
**Varies**: intensity metric, decay profile, bond-formation threshold, signal-channel specifics.
**Extension**: `MusicalResonate`, `MarketResonate`, `CulturalResonate`.

## 129. `Compromise` · Society/Economics · R1T2

**Intended**: iterative negotiation via intensity reduction until dissonance drops below threshold.
**Future**: any "continuously reduce demand" negotiation mechanism.
**Broad-use contexts**: labor negotiations, political compromise, sibling dispute resolution, product-requirement prioritization, budget negotiations, coalition building.
**Every context needs**: preference statements with intensity scores, dissonance calculation, intensity-reduction loop, threshold for consensus.
**Varies**: intensity scale, dissonance formula, reduction rate, asymmetric-power weighting.
**Extension**: `WeightedCompromise`, `AsymmetricCompromise`, `TimeLimitedCompromise`.

## 130. `DeliberativeAlign` · Society/Protocols · R0T2

**Intended**: Constitutional AI — explicit safety reasoning pass against Policy/Constitution before execution.
**Future**: any "check policy before act" safety discipline.
**Broad-use contexts**: Claude's Constitutional AI, regulatory compliance, ethical pre-checks, corporate policy adherence, legal-review-before-release, code-of-conduct enforcement.
**Every context needs**: Policy/Constitution set, safety-trace generation before task execution, revision loop on policy violation.
**Varies**: policy source, trace depth, revision strategy, escalation on irreconcilable violation.
**Extension**: `ConstitutionalDeliberativeAlign`, `RegulatoryDeliberativeAlign`, `MultiPolicyDeliberativeAlign`.

## 131. `DeepResearch` · Society/Protocols · R2T1

**Intended**: autonomous research pipeline — Plan → Multi-Round Search → Synthesis → Report.
**Future**: any multi-round search-and-synthesize investigation pipeline.
**Broad-use contexts**: literature review, investigative journalism, market research, competitive analysis, due-diligence, forensic investigation, open-source intelligence gathering.
**Every context needs**: planning (decompose query), multi-round search with gap-detection, synthesis with contradiction resolution, reporting with citations.
**Varies**: search-tool set, round-count bound, synthesis depth, citation style, report format.
**Extension**: `AcademicDeepResearch`, `MarketDeepResearch`, `ForensicDeepResearch`.
**Note**: `DeepResearch` is Society/Protocols but is largely single-agent (or agent-with-external-tools). Potentially a §3.18-style Society→Mind relocation candidate. Worth noting.

## 132. `EvaluatorOptimizer` · Society/Protocols · R2T1

**Intended**: generate-evaluate-refine loop with two roles.
**Future**: any two-role iterative quality-improvement loop.
**Broad-use contexts**: LLM self-critique loops, adversarial training, code-review iteration, generative-art refinement, RLHF reward-model iteration.
**Every context needs**: generator role, evaluator role, structured feedback, refinement mechanism, loop termination.
**Varies**: role separation (same model or separate), feedback structure, max iterations, convergence criteria.
**Extension**: `SelfEvaluatorOptimizer`, `AdversarialEvaluatorOptimizer`, `MultiEvaluatorOptimizer`.

## 133. `Workflow` · Society/Protocols · R0T1

**Intended**: directed graph of operations with typed artifact edges.
**Future**: any multi-step coordinated operation graph.
**Broad-use contexts**: business workflows, CI/CD pipelines, ML pipelines, data-processing pipelines, multi-step agent tasks, ETL jobs.
**Every context needs**: step definitions, edge directions, typed artifacts per edge, AcceptSpec per edge, role binding.
**Varies**: branching support, parallelism, conditional logic, dynamic vs static graph, failure handling.
**Extension**: `DAGWorkflow`, `ConditionalWorkflow`, `DynamicWorkflow`, `StreamingWorkflow`.

## 134. `Critique` · Infrastructure/Data Structures · R1T1

**Intended**: qualitative feedback generation — structured assessment produced from criteria.
**Future**: any structured-commentary-on-target artifact.
**Broad-use contexts**: peer review, design critique, code review, essay critique, art critique, policy analysis, clinical feedback.
**Every context needs**: target artifact, criteria, structured output (strengths, weaknesses, recommendations).
**Varies**: structure format, criteria source, depth, actionability requirement.
**Extension**: `StructuredCritique`, `RubricCritique`, `FreeformCritique`.

## 135. `Refine` · Mind/Reasoning · R1T1

**Intended**: iterative improvement — apply critique, edit, repeat.
**Future**: any feedback-driven revision loop.
**Broad-use contexts**: essay revision, code refactoring, design iteration, scientific-paper rewriting, product iteration, art polishing.
**Every context needs**: artifact to refine, critique mechanism, edit mechanism, termination condition (quality threshold or cycle cap).
**Varies**: critique source (self, peer, rubric), edit granularity, convergence criteria.
**Extension**: `SelfRefine`, `PeerRefine`, `BudgetedRefine`, `ConvergentRefine`.

## 136. `FirstPrinciples` · Mind/Reasoning · R2T2

**Intended**: axiomatic reconstruction — strip to fundamentals and rebuild.
**Future**: any from-scratch derivation discipline.
**Broad-use contexts**: Elon Musk's rocket-cost calculation, scientific rederivation, pedagogical teaching from basics, legal statutory analysis, security threat modeling.
**Every context needs**: assumption-stripping process, axiom identification, reconstruction from axioms only.
**Varies**: axiom set, reconstruction rigor, domain specificity, verification of axiom-claim.
**Extension**: `PhysicsFirstPrinciples`, `LegalFirstPrinciples`, `EconomicFirstPrinciples`.

## 137. `Dialectic` · Mind/Reasoning · R2T2

**Intended**: internal Thesis-Antithesis-Synthesis loop (vs Socratic which queries user).
**Future**: any internal-debate-to-synthesize reasoning mode.
**Broad-use contexts**: Hegelian dialectic, internal debate before writing, solo multi-perspective debugging, creative-writing persona conflict, design-tension resolution.
**Every context needs**: Thesis, Antithesis construction (potentially via SteelmanCheck), Synthesis generation.
**Varies**: persona construction method, iteration count, synthesis-acceptance criteria.
**Extension**: `HegelianDialectic`, `AdversarialDialectic`, `RapidDialectic`.

## 138. `RecursiveRootCause` · Mind/Reasoning · R2T2

**Intended**: recursive "why?" analysis until reaching actionable root.
**Future**: any causal-chain-traversal debugging method.
**Broad-use contexts**: Toyota 5-Whys, incident post-mortems, bug tracing, systems analysis, therapy root-cause work, scientific causal investigation.
**Every context needs**: problem statement, "why did this happen?" iterator, actionability detector for stopping.
**Varies**: depth cap, actionability definition, branching (multiple causes per level), provenance tracking.
**Extension**: `FiveWhys`, `BranchingRecursiveRootCause`, `ProvenancedRecursiveRootCause`.

## 139. `Bisect` · Mind/Reasoning · R2T2

**Intended**: logarithmic search via binary splitting.
**Future**: any "split search space in half" narrowing mechanism.
**Broad-use contexts**: git bisect, 20-Questions, binary search in sorted arrays, medical diagnostic narrowing, debugging (which commit broke it?), diagnostic decision trees.
**Every context needs**: possibility space, partition question, elimination rule, recursion on remaining half.
**Varies**: question-selection heuristic, partition fairness (exactly half vs approximate), fallback on indivisible space.
**Extension**: `GitBisect`, `MedicalBisect`, `BalancedBisect`.

## 140. `StigmergyMemoize` · (NOT IN DB — worth checking)

**Intended** (if minted): combining Stigmergy with Cache/Memoize — leaving traces that serve as cached results for later traversers.
**Future**: any "environment-stored cached result" pattern.
**Broad-use contexts**: ant-trail pheromone memory, route-optimization with cached intermediate results, shared-scratch-pad caching, wiki that grows from user annotations as cache.
**Every context needs**: stigmergy traces, cache semantics on trace reads, decay coexisting with cache TTL.
**Varies**: trace data structure, cache-hit freshness rules, reinforcement semantics.
**Note for audit**: this may be a useful future mint. The macro would be `Stigmergy` + `Cache` composed. Possibly worth noting as a future-mint candidate but not part of this audit.

---

## Observations from batch 7

**More validations.**
- `Rollout` composing circuit_breaker + canary + ejection_seat + compensate shows how foundation patterns stack into concrete workflows.
- `LazyConsensus` is the speed-end of the consensus spectrum, complementing strict `Consensus` — both validated as distinct.
- `DeepResearch` as Society/Protocols vs Mind: broad-use suggests Mind is closer (see audit item 25 below).

**New audit items surfaced in batch 7.**
25. **`DeepResearch` may be another Society→Mind candidate.** The pipeline is largely single-agent; multi-agent aspects are optional (external search tools aren't peer agents). Worth adding to §3.18's Society→Mind list.
26. **`Critique` categorization is Infrastructure/Data Structures.** Mechanism says "Analyzes a target datum against specific criteria and generates a structured assessment" — that's a Verb. Same Noun/Verb miscategorization as Check/Observe/ToolInvoke in §3.11. Add to §3.11 list.
27. **`RecursiveRootCause` references `trace` via template** — declared? Worth spot-checking.
28. **`StigmergyMemoize` doesn't exist** — noted as potential future mint (Stigmergy + Cache), but not minting in this audit.

Total analyzed: 140 patterns. Remaining: 289.

---

## Batch 8 — Society/Protocols + orchestration-loop family + epistemic governance

## 141. `WorldReversible` · Society/Protocols · R0T1

**Intended**: design constraint requiring zero-cost undo for every action.
**Future**: any "everything must be invertible" architectural discipline.
**Broad-use contexts**: event-sourced systems, git-based workflows, CRDT design, experimental environments, educational sandboxes, reversible computing research, legal systems with appeal rights.
**Every context needs**: immutable logs, versioning, soft-deletes instead of destructive updates, inverse-action discoverability.
**Varies**: reversibility horizon (everything vs recent), storage cost tradeoffs, compensation protocol specifics.
**Extension**: `EventSourcedReversible`, `GitlikeReversible`, `TimeBoundedReversible`.

## 142. `TranslationProxy` · Society/Protocols · R1T1

**Intended**: stateless wrapper that bridges modern agents to legacy systems via Translate.
**Future**: any protocol-adaptation wrapper.
**Broad-use contexts**: API adapter patterns, legacy-system integration, gateway services, MCP bridges, protocol-version translators, cross-ecosystem bridges.
**Every context needs**: upstream (modern) interface, downstream (legacy) interface, translate in both directions, semantic fidelity verification.
**Varies**: statelessness (some proxies cache), error-mapping strategy, authentication bridging, rate-limit propagation.
**Extension**: `CachingTranslationProxy`, `AuthTranslationProxy`, `ErrorMappingProxy`.

## 143. `UptakeAsGround` · Society/Protocols · R2T2

**Intended**: meaning is defined pragmatically — by successful coordination use.
**Future**: any "validity by usage success" semantic.
**Broad-use contexts**: Wittgensteinian meaning-as-use, pragmatic linguistics, product-market-fit measurement, vocabulary maturity scoring, pattern-library validation, API-adoption metrics.
**Every context needs**: usage-success tracking, coordination-success rate metric, non-usage = low-meaning equivalence.
**Varies**: success definition, tracking granularity, decay of old-usage data, multi-agent vs single-agent.
**Extension**: `CoordinationUptakeAsGround`, `WeightedUptakeAsGround`, `DecayingUptakeAsGround`.

## 144. `UptakeOverTimestamp` · Society/Protocols · R1T2

**Intended**: resolve canonical-status conflicts by prioritizing usage over registration time.
**Future**: any "popularity beats seniority" disambiguation rule.
**Broad-use contexts**: semantic-namespace disambiguation, Stack Overflow top-answer selection (by votes not age), domain-name squatting resolution (in systems where squatting doesn't pay), meme-primacy resolution.
**Every context needs**: conflict detection on handle, uptake counting, highest-uptake return policy.
**Varies**: uptake metric (references, executions, views), tiebreak rule, time-decay, scope of comparison.
**Extension**: `WeightedUptakeOverTimestamp`, `ScopedUptakeOverTimestamp`.

## 145. `AmbiguityResolution` · Society/Protocols · R1T2

**Intended**: social protocol forcing resolution when agents flag conflicting data.
**Future**: any "decide or fork" ambiguity-clearing mechanism.
**Broad-use contexts**: wiki edit conflicts, semantic-data merge conflicts, multi-source knowledge integration, dispute resolution in open forums, Lego-like piece-system conflict resolution.
**Every context needs**: ambiguity flagging mechanism, vote-to-clarify/delete/fork protocol, resolution enforcement.
**Varies**: quorum for resolution, fork-tolerance policy, retention of historical ambiguity.
**Extension**: `WikiAmbiguityResolution`, `CodeMergeAmbiguityResolution`, `SemanticAmbiguityResolution`.

## 146. `AdversarialProof` · Society/Protocols · R2T2

**Intended**: cognitively-enriched negative-proof via adversarial search for prohibited data.
**Future**: any "proof of absence via red-team failure" argument.
**Broad-use contexts**: zero-knowledge proof systems, penetration-testing-based security claims, fuzzing-derived correctness claims, adversarial ML robustness proofs.
**Every context needs**: NegativeProof machinery, RedTeam adversarial search, failure-to-find-after-serious-effort as positive evidence of absence.
**Varies**: adversarial capability model, effort-threshold calibration, confidence quantification.
**Extension**: `ZKAdversarialProof`, `FuzzingAdversarialProof`, `AIPenTestAdversarialProof`.

## 147. `ConfusedDeputy` · Society/Protocols · R0T1

**Intended**: guard against privilege confusion — bind authority checks to the upstream caller, not the executing deputy.
**Future**: any capability-security discipline against authority confusion.
**Broad-use contexts**: classic Hardy framing (1988), OAuth scope confusion, LLM prompt injection via tool access, SSRF attacks, server-side request forgery defenses.
**Every context needs**: distinction between deputy identity and caller identity, auth check against caller not deputy, carrying of caller context through delegations.
**Varies**: caller-identity representation, context propagation mechanism, revocation protocol, audit trail.
**Extension**: `CapabilityConfusedDeputy`, `OAuthScopedConfusedDeputy`, `LLMPromptInjectionConfusedDeputy`.

## 148. `DogfoodFirst` · Society/Economics · R0T2

**Intended**: use your own tool before shipping it, to find usability gaps.
**Future**: any "live with the thing you built" validation protocol.
**Broad-use contexts**: software development dogfooding, API self-consumption, pattern-library self-usage, drug testing by inventors, product tasting by chefs, policy-by-lawmakers.
**Every context needs**: creator, creation, non-trivial use case by creator, Friction Log output.
**Varies**: duration of dogfooding, scope (full product vs slice), documentation requirements, release-gate semantics.
**Extension**: `CanaryDogfoodFirst`, `TimedDogfoodFirst`, `DocumentedDogfoodFirst`.

## 149. `Crystallize` · Mind/Strategy · R1T2

**Intended**: phase transition from implicit resonance to explicit contract.
**Future**: any "informal → formal" conversion when conditions are ripe.
**Broad-use contexts**: norm-to-law transitions, team convention-to-policy, tacit knowledge → explicit documentation, prototype → production, case law formation, constitutional moments.
**Every context needs**: implicit behavior observation, consensus validation, codification mechanism, entropy-threshold check (don't crystallize prematurely).
**Varies**: resonance period (Duration, see §3.17), consensus requirement, reversibility post-crystallization.
**Extension**: `ConstitutionalCrystallize`, `GradualCrystallize`, `ReversibleCrystallize`.

## 150. `CurriculumReplay` · Society/Protocols · R2T1

**Intended**: self-supervised reinforcement — re-train on own high-scoring past outputs.
**Future**: any self-distillation-from-own-examples learning.
**Broad-use contexts**: LLM self-distillation, RL experience-replay buffers, meditation on past successes, athletic replay training, habit reinforcement.
**Every context needs**: replay buffer of successful interactions, quality-ranking, sampling mechanism, fine-tune-during-idle semantic.
**Varies**: buffer size, ranking method, decay of old successes, update strategy.
**Extension**: `RankedCurriculumReplay`, `DecayingCurriculumReplay`, `MultiModalCurriculumReplay`.

## 151. `DriftWatch` · Society/Protocols · R0T1

**Intended**: reputation as pattern-fidelity measurement via micro-deviation detection.
**Future**: any "trust equals behavioral consistency" reputation mechanism.
**Broad-use contexts**: continuous authentication via behavioral biometrics, agent-reliability scoring via deviation from baseline, trading-algorithm integrity monitoring, partner-behavior prediction.
**Every context needs**: baseline establishment, continuous observation, deviation detection (2-sigma or similar), peer-report aggregation.
**Varies**: baseline horizon, sigma threshold, peer-verification network size, action on drift detection.
**Extension**: `PeerDriftWatch`, `BiometricDriftWatch`, `AdaptiveBaselineDriftWatch`.

## 152. `GenealogicalTrace` · Society/Protocols · R2T2

**Intended**: audit the historical lineage and incentives of an idea (Cui Bono).
**Future**: any "follow the idea to its origin and interest" analysis.
**Broad-use contexts**: historical criticism, science-studies analysis, policy-origin tracing, argument-by-authority debunking, meme-origin analysis, philosophical genealogy (Nietzsche, Foucault).
**Every context needs**: target concept, origin-tracing mechanism, interest identification ("who benefited?"), distinction between universal-truth vs inherited-bias.
**Varies**: depth of trace, source-citation rigor, confidence in origin claim, applicability to the current context.
**Extension**: `AcademicGenealogicalTrace`, `IncentiveGenealogicalTrace`, `InstitutionalGenealogicalTrace`.

## 153. `LatticeCommit` · Society/Protocols · R0T1

**Intended**: geometric-neighbor consensus — state transition valid only if signed by agent AND its immediate lattice neighbors.
**Future**: any spatial-locality-constrained consensus.
**Broad-use contexts**: cellular automata, spatially-organized distributed systems, geographic-network protocols, mesh networks, federated systems with geographic partitioning.
**Every context needs**: lattice topology, neighbor relation, signatures from agent + neighbors, local quorum semantic.
**Varies**: lattice dimension (2D, 3D, hexagonal), neighbor count per node, signature aggregation method, lattice dynamism.
**Extension**: `HexagonalLatticeCommit`, `MeshLatticeCommit`, `DynamicLatticeCommit`.

## 154. `MintWhenFriction` · Society/Economics · R2T2

**Intended**: mint new patterns only when specific friction signals surface ("Just in Time" vs "Just in Case").
**Future**: any "don't create a new term until usage demands it" discipline.
**Broad-use contexts**: vocabulary growth in libraries, API surface evolution, ontology management, taxonomic splitting in biology, legal-term introduction.
**Every context needs**: friction-signal detection, repetition monitoring, threshold-based minting, rejection of speculative minting.
**Varies**: friction-signal set, threshold calibration, minting-review process, aging/expiration if usage drops.
**Extension**: `RepetitionMintWhenFriction`, `CostBasedMintWhenFriction`, `ConsensusMintWhenFriction`.

## 155. `OrchestrationLoop` · Society/Protocols · R1T2

**Intended**: strict lifecycle for high-stakes problem solving — Interpret → Plan → Rollout.
**Future**: any phase-gated problem-solving workflow.
**Broad-use contexts**: software development lifecycles, scientific research workflows, organizational decision-making, regulatory-compliant processes, safety-critical development.
**Every context needs**: three phases (framing, planning, rollout), typed-artifact transitions, AcceptSpec gates between phases, iteration capability on failure.
**Varies**: phase granularity, rollback depth on iteration, parallel-phase support, external-gate integration.
**Extension**: `RegulatoryOrchestrationLoop`, `AgileOrchestrationLoop`, `WaterfallOrchestrationLoop`.

## 156. `RequestFraming` · Society/Protocols · R1T2

**Intended**: initial orchestration phase — interpret message into FrameSpec before committing resources.
**Future**: any "understand before acting" preamble.
**Broad-use contexts**: requirements elicitation, customer-request translation, ticket triage, ambiguous-command handling, user-intent inference, onboarding questionnaires.
**Every context needs**: input message, interpretation mechanism, FrameSpec output (constraints, success criteria, hidden assumptions), semantic-firewall role.
**Varies**: interpretation depth, clarification-question budget, escalation on unclear intent.
**Extension**: `ClarifyingRequestFraming`, `StrictRequestFraming`, `InteractiveRequestFraming`.
**Note**: `RequestFraming` will move Society → Mind per §3.18.

## 157. `RealizationProtocol` · Society/Protocols · R1T2

**Intended**: standardized SolverTree for abstract → concrete transition.
**Future**: any concreteness-enforcing workflow template.
**Broad-use contexts**: SOPs for solver-based systems, build-from-spec pipelines, requirement-to-implementation workflows, idea-to-execution templates.
**Every context needs**: interpret step, manifest_planning step, rollout step, strict phase ordering.
**Varies**: per-phase detail, alternate paths, customization points, audit requirements.
**Extension**: `StrictRealizationProtocol`, `AdaptiveRealizationProtocol`, `AuditableRealizationProtocol`.

## 158. `ModestClaim` · Society/Protocols · R2T2

**Intended**: epistemic reframe from Universal Truth to Local Observation ("Divergence ≠ Identity").
**Future**: any "I'm not saying always true, just here, now" claim-scoping discipline.
**Broad-use contexts**: scientific paper limitations sections, disclaimer practice, epistemic humility teachings, ML model caveats, honest journalism.
**Every context needs**: scope reduction from Universal to Local, divergence-detection semantic instead of identity-claim, epistemic calibration.
**Varies**: scope size (narrow Local, broad Regional), uncertainty quantification, confidence bounds.
**Extension**: `ScopedModestClaim`, `BoundedModestClaim`, `CalibratedModestClaim`.

## 159. `PatternEmergence` · Society/Protocols · R2T2

**Intended**: recognize implicit patterns bottom-up from interaction logs before top-down design.
**Future**: any "observe before design" observational heuristic.
**Broad-use contexts**: user-research-driven product design, descriptive-before-prescriptive linguistics, emergent-team convention documentation, bottom-up ontology building.
**Every context needs**: interaction logs, pattern-recognition mechanism, codification pathway (to MintWhenFriction), matching against existing pattern discovery.
**Varies**: log depth, pattern-recognition method (manual, ML, hybrid), codification threshold.
**Extension**: `LogMiningPatternEmergence`, `ConversationalPatternEmergence`, `CodebasePatternEmergence`.

## 160. `PatternSketch` · Society/Protocols · R2T1

**Intended**: reference a canonical concept with explicit uncertainty and modifications (approximation).
**Future**: any "approximately-but-not-exactly-this" reference discipline.
**Broad-use contexts**: early-stage design references, research-in-progress citations, prototype-level pattern use, legal "mutatis mutandis" references.
**Every context needs**: base pattern reference, explicit uncertainty marker, delta description, eventual full-conformance path.
**Varies**: uncertainty representation, delta specification format, upgrade path to full conformance.
**Extension**: `ResearchPatternSketch`, `PrototypePatternSketch`, `ReviewablePatternSketch`.

---

## Observations from batch 8

**Family coherence in orchestration patterns.** `OrchestrationLoop` → `RequestFraming` + `ManifestPlanning` + `Rollout` + `RealizationProtocol` form a tightly coupled family. Each broad-use sketch independently passes, AND they compose correctly. This validates the §3.14 solver-family alignment.

**New audit items surfaced in batch 8.**
29. **`UptakeAsGround` and `UptakeOverTimestamp` depend on each other via template.** `UptakeOverTimestamp` "Utilizes UptakeAsGround" — declared? Spot-check.
30. **`Crystallize`** (Mind/Strategy R1T2) — its mechanism references `{{resonate}}`, `{{dampen}}`, `{{entropy_pump}}`, `{{decay}}`, `{{constitution}}`. Potential declared-dep gaps worth checking in the broader reference-density pass.
31. **`DriftWatch`'s gloss is a multi-sentence essay** — §3.18 flagged this as marketing-speak glosses. Confirmed in batch 8: the current gloss would not work as an embedding anchor.
32. **`PatternEmergence` + `MintWhenFriction` + `UptakeAsGround`** are a tight cluster on vocabulary-hygiene protocols. Each passes broad-use individually; together they form a coherent governance-of-vocabulary subsystem worth mapping as a family.
33. **`ConfusedDeputy`'s R0T1 placement is borderline**. R0 is kernel-level; ConfusedDeputy is a *defense* against a known vulnerability class. Is this defense kernel-level or userland tactic? Probably kernel-level because ignoring it causes systemic security failures. Keep R0.

Total analyzed: 160 patterns. Remaining: 269.

---

## Batch 9 — core Verbs + Infrastructure/Data Structures + Physics substrates

## 161. `Sign` · Physics/Primitives · R1T1

**Intended**: attach a verifiable identity proof to an artifact.
**Future**: any non-repudiable authorship/approval attachment.
**Broad-use contexts**: cryptographic signatures, handwritten signatures, OAuth token signing, PGP email, code signing, document notarization, blockchain transactions, wet signatures on paper.
**Every context needs**: identity proof, artifact to attach to, non-repudiable link.
**Varies**: algorithm (RSA, ECDSA, EdDSA, wet), key material, verification protocol, attachment format (detached vs embedded).
**Extension**: `CryptoSign`, `WetSign`, `NotarySign`, `MultiSigSign`.

## 162. `Greet` · Infrastructure/Primitives · R1T1

**Intended**: initial contact protocol — cryptographic identity verification + CompatibilityCheck.
**Future**: any "hello, are we compatible?" handshake.
**Broad-use contexts**: TLS handshake, OAuth flow initiation, API-version negotiation, agent discovery greeting, human introductions, protocol version negotiation.
**Every context needs**: identity verification, compatibility check, state transition Unknown → Connected.
**Varies**: authentication strength, extension negotiation, fallback on incompatibility, one-way vs mutual.
**Extension**: `TLSGreet`, `OAuthGreet`, `MutualGreet`, `OpportunisticGreet`.

## 163. `Trace` · Infrastructure/Primitives · R0T1

**Intended**: record lineage/provenance — append chronological history log to a target.
**Future**: any provenance-tracking mechanism.
**Broad-use contexts**: distributed tracing, git history, event sourcing, data lineage, scientific provenance, supply-chain tracking, medical record history.
**Every context needs**: target entity, immutable append log, per-modification record.
**Varies**: log storage medium, record detail, retention policy, index-for-query, cross-entity linking.
**Extension**: `DistributedTrace`, `CausalTrace`, `QueryableTrace`, `CompressedTrace`.

## 164. `Select` · Infrastructure/Primitives · R0T1

**Intended**: deterministic filter — apply predicate P(x) to every element, return subset.
**Future**: any "filter by predicate" operation.
**Broad-use contexts**: SQL WHERE, array.filter, set-theoretic filtering, query results, search results, decision making from options.
**Every context needs**: input set, predicate function, subset output.
**Varies**: predicate complexity, short-circuit semantics, ordering preservation, cost estimation.
**Extension**: `IndexedSelect`, `StreamingSelect`, `ParallelSelect`, `CostAwareSelect`.

## 165. `Search` · Infrastructure/Primitives · R0T1

**Intended**: active scanning of a domain to locate matching entities.
**Future**: any "find matches" operation over a domain.
**Broad-use contexts**: text search, code search, vector-embedding search, graph search, file-system search, inventory search, database queries.
**Every context needs**: domain, criteria, iteration mechanism, Check-based filtering.
**Varies**: domain type (memory, environment, data), indexing strategy, ranking, parallelism, real-time vs batch.
**Extension**: `SemanticSearch`, `FullTextSearch`, `GraphSearch`, `IndexedSearch`.

## 166. `Compare` · Mind/Reasoning · R0T1

**Intended**: evaluate relation between two values (Equal/Less/Greater/Incomparable).
**Future**: any pairwise-comparison primitive.
**Broad-use contexts**: sort operations, priority queues, tournament brackets, A/B testing, preference orderings, medical comparisons, financial comparisons.
**Every context needs**: two values, comparability definition, four-valued return.
**Varies**: ordering (total, partial, pre-order), numeric vs semantic comparison, tolerance for "nearly equal."
**Extension**: `NumericCompare`, `SemanticCompare`, `FuzzyCompare`, `PartialOrderCompare`.

## 167. `Rank` · Mind/Reasoning · R0T1

**Intended**: deterministic sort — apply scoring function, return List ordered by Score, truncate to Top-K.
**Future**: any "sort by score, return top" operation.
**Broad-use contexts**: search result ranking, leaderboards, bid ranking, candidate ranking, option selection, feed ranking.
**Every context needs**: scoring function (ScoringFunction per §3.5), sort mechanism, Top-K truncation.
**Varies**: tiebreaker policy, ranking stability, lazy vs eager evaluation, distributed ranking.
**Extension**: `StableRank`, `LazyRank`, `DistributedRank`.

## 168. `Probe` · Infrastructure/Primitives · R0T1

**Intended**: active query returning verifiable information about system/environment state.
**Future**: any active "ask and get ground truth" mechanism.
**Broad-use contexts**: health checks, TCP SYN probes, DNS queries, API status checks, sensor queries, LLM capability probing, test probes.
**Every context needs**: target to probe, active query semantic (not passive observation), verifiable response.
**Varies**: cost, latency, sandbox requirement (for stateful probes), retry on timeout, authentication.
**Extension**: `SandboxedProbe`, `AuthenticatedProbe`, `LightweightProbe`, `DeepProbe`.

## 169. `Understand` · Mind/Reasoning · R1T1

**Intended**: construct internal model reflecting causal structure, semantics, context of input.
**Future**: any comprehension-grade reasoning operation.
**Broad-use contexts**: LLM comprehension, human understanding, scientific modeling, requirements understanding, code comprehension, domain expertise building.
**Every context needs**: input (possibly complex), context, internal model construction that captures "why" and "how" (not just surface parse).
**Varies**: depth of model, domain specificity, verifiability of understanding, duration (one-shot vs over time).
**Extension**: `DeepUnderstand`, `DomainUnderstand`, `VerifiedUnderstand`, `IncrementalUnderstand`.

## 170. `Message` · Infrastructure/Data Structures · R1T1

**Intended**: structured container for a Signal with Metadata.
**Future**: any packaged-communication artifact.
**Broad-use contexts**: email, HTTP requests, gRPC messages, agent-to-agent messages, ML-pipeline artifacts, log entries with metadata, instant-messaging.
**Every context needs**: payload (Signal), Sender identity, Recipient, Timestamp.
**Varies**: encryption, authentication, ordering guarantees, size limits, reply-to chaining.
**Extension**: `EncryptedMessage`, `AuthenticatedMessage`, `OrderedMessage`, `RichMessage`.

## 171. `Stream` · Infrastructure/Data Structures · R0T1

**Intended**: ordered, potentially unbounded sequence of Messages.
**Future**: any continuous-flow data structure.
**Broad-use contexts**: Kafka topics, HTTP/2 streams, WebSocket channels, LLM token streams, log feeds, conversation histories, sensor streams, video streams.
**Every context needs**: ordered sequence, Message elements, operations (map, filter, backpressure).
**Varies**: boundedness, ordering guarantees, at-least-once vs at-most-once, durability, multi-consumer support.
**Extension**: `BoundedStream`, `DurableStream`, `MultiConsumerStream`.

## 172. `Event` · Infrastructure/Data Structures · R0T1

**Intended**: discrete occurrence — a state change at a specific point in time.
**Future**: any atomic temporal-change unit.
**Broad-use contexts**: event sourcing, DOM events, physical events, financial transactions, audit logs, game state changes, biological events.
**Every context needs**: discrete occurrence, state change semantic, timestamp, distinctness from Stream (continuous).
**Varies**: event schema, ordering guarantee, replayability, causal linkage to prior events.
**Extension**: `DomainEvent`, `DomEvent`, `FinancialEvent`, `ReplayableEvent`.

## 173. `Exception` · Infrastructure/Data Structures · R0T1

**Intended**: runtime anomaly signal requiring explicit handling.
**Future**: any "something went wrong" error object.
**Broad-use contexts**: programming-language exceptions, HTTP error codes, RPC errors, game-logic exceptions, business-process violations, anomaly flags.
**Every context needs**: error classification, invalid-state indication, requirement-of-handling semantic.
**Varies**: stack trace attachment, recovery hints, severity levels, typed vs untyped.
**Extension**: `TypedException`, `RecoverableException`, `FatalException`, `ClassifiedException`.

## 174. `Signal` · Infrastructure/Data Structures · R0T1

**Intended**: raw information emission — fire-and-forget with no guaranteed recipient.
**Future**: any broadcast/emission primitive.
**Broad-use contexts**: pub/sub signals, OS signals (SIGTERM etc), broadcast messages, neural firing (biological analogy), distress beacons, emissions into an environment.
**Every context needs**: emission mechanism, no guaranteed delivery, environment as medium.
**Varies**: carrier medium, reach, reliability tiers, filtering.
**Extension**: `ReliableSignal`, `PrioritizedSignal`, `EncryptedSignal`.

## 175. `Resource` · Infrastructure/Data Structures · R0T1

**Intended**: finite allocatable entity — can be allocated, consumed, locked.
**Future**: any managed-allocation unit.
**Broad-use contexts**: compute resources, tokens, memory, attention budget, physical goods, database connections, rate-limit slots, personnel time.
**Every context needs**: identity, finiteness, allocation/consumption/lock semantic, contention handling.
**Varies**: renewability, exhaustibility, divisibility, accounting mechanism.
**Extension**: `RenewableResource`, `ExhaustibleResource`, `DivisibleResource`, `PooledResource`.

## 176. `Decay` · Physics/Primitives · R0T2

**Intended**: gradual value attenuation over time without reinforcement.
**Future**: any time-based-fading mechanism.
**Broad-use contexts**: memory decay, cache TTL, pheromone decay in stigmergy, radioactive decay, attention decay, reputation decay, content freshness scoring.
**Every context needs**: current value, decay rate, time passage, reinforcement mechanism, zero-threshold action.
**Varies**: decay function (exponential, linear, custom), reinforcement magnitude, reset semantics, zero-threshold action.
**Extension**: `ExponentialDecay`, `LinearDecay`, `StepDecay`.

## 177. `Dampen` · Physics/Primitives · R0T1

**Intended**: passive attenuation of signal/force — negative feedback to prevent oscillation.
**Future**: any "reduce signal magnitude" operation.
**Broad-use contexts**: shock absorbers, electrical dampening, audio dampening, organizational politics dampening (cooling-off periods), alert suppression, over-eager response dampening.
**Every context needs**: signal being dampened, attenuation mechanism, resistance/noise source.
**Varies**: attenuation function, adaptive vs fixed dampening, target (signal, force, value).
**Extension**: `AdaptiveDampen`, `FixedDampen`, `FrequencySelectiveDampen`.

## 178. `Causation` · Physics/Primitives · R1T1

**Intended**: a relationship where one event directly forces another.
**Future**: any direct-causal-link artifact.
**Broad-use contexts**: physics causation, statistical causal inference, legal causation, economic causal models, scientific experimental causality, debugging (A caused B).
**Every context needs**: cause event, effect event, directness semantic (manipulating cause alters effect), distinction from Correlation.
**Varies**: causal strength, directness (direct vs chained), counterfactual semantics, confidence.
**Extension**: `DirectCausation`, `ChainedCausation`, `ProbabilisticCausation`.

## 179. `Correlation` · Infrastructure/Data Structures · R1T1

**Intended**: shared movement between variables, without implying cause.
**Future**: any co-variation artifact (non-causal).
**Broad-use contexts**: statistical correlation, market co-movements, feature correlation in ML, symptom co-occurrence, meme spread patterns.
**Every context needs**: two variables, co-movement measure, explicit non-causal semantic.
**Varies**: correlation method (Pearson, Spearman, etc.), lag, directionality, confidence intervals.
**Extension**: `PearsonCorrelation`, `SpearmanCorrelation`, `LaggedCorrelation`.
**Note**: §3.18 flagged Correlation's mechanism as gloss-restatement. The broad-use sketch gives a concrete rewrite target: distinguish from Causation by structure (two variables, no directed edge), not by naming the fallacy.

## 180. `Noise` · Physics/Primitives · R1T1

**Intended**: information irrelevant to current task — obscures Datum and increases extraction cost.
**Future**: any "not-signal" interference unit.
**Broad-use contexts**: audio noise, signal-processing noise, data noise, cognitive distraction, communication interference, adversarial noise injection (security).
**Every context needs**: context defining what's relevant (and thus what's noise), interference semantic.
**Varies**: noise model (Gaussian, structured, adversarial), filterability, injection vs natural, impact on extraction cost.
**Extension**: `GaussianNoise`, `AdversarialNoise`, `StructuredNoise`, `DecoyNoise`.

---

## Observations from batch 9

**Core primitives hold up remarkably well.** Trace, Select, Search, Probe, Sign, Greet, Rank, Compare — each is a clean atomic operation that broad-use descendants specialize without breaking. These are the backbone of the library; their clean specifications are why 429 patterns can compose coherently.

**New audit items surfaced in batch 9.**
34. **`Causation`/`Correlation` layer split** — Causation is Physics/Primitives, Correlation is Infrastructure/Data Structures. Reasonable if Causation is about the physical substrate (things that force each other) and Correlation is about data (co-movement). But when §3.18's correlation mechanism rewrite happens, worth checking they remain cleanly distinct — maybe Correlation should reference Causation (as its opposite/contrast anchor) via `references`.
35. **`Signal`** is in Infrastructure/Data Structures but is described as "Emission of information into environment. Fire-and-forget." That's emission — an action — but the pattern is the emission as a *thing* (noun). Borderline between Noun (emission-artifact) and Verb (emit). Probably OK as Noun because you can refer to "this signal" as an object.
36. **`Exception` vs `Signal` vs `Event`** — all three are in Infrastructure/Data Structures and each represents a kind of information-unit. Their mechanisms differentiate cleanly: Signal (fire-and-forget), Event (state-change-in-time), Exception (anomaly-with-required-handling). Good cluster coherence.

Total analyzed: 180 patterns. Remaining: 249.

---

## Batch 10 — Reasoning patterns + Strategy heuristics + Society protocols interior

## 181. `HypothesisLadder` · Mind/Strategy · R2T1

**Intended**: Bayesian belief updating via falsifiable rungs — act on highest-probability hypothesis, keep others alive.
**Future**: any probabilistic-hypothesis-tracking reasoning.
**Broad-use contexts**: scientific method, debugging decision trees, medical diagnosis ladders, investment hypothesis tracking, AI safety research, intelligence analysis.
**Every context needs**: hypothesis list with probabilities, Bayesian update on new data, act-on-highest rule, alive-other-hypotheses tracking.
**Varies**: ladder depth, update frequency, hypothesis pruning policy, experiment-cost consideration.
**Extension**: `DeepHypothesisLadder`, `PrunedHypothesisLadder`, `CostAwareHypothesisLadder`.

## 182. `StepBack` · Mind/Reasoning · R1T1

**Intended**: meta-cognitive think operation — pause object-level work to ask higher-level question.
**Future**: any "zoom out for perspective" reasoning operation.
**Broad-use contexts**: debugging frustration breaks, architectural review, strategy retrospectives, scientific paradigm questioning, life-decision reflection, system-design-level questions.
**Every context needs**: pause of object-level work, abstraction ascent, higher-level question formulation.
**Varies**: ascent depth, trigger (spontaneous vs scheduled), return semantic (new direction vs resume old).
**Extension**: `ScheduledStepBack`, `FrustrationTriggeredStepBack`, `DeepStepBack`.

## 183. `SkeletonOfThought` · Mind/Reasoning · R2T2

**Intended**: macro for Think(Skeleton) — generate outline first, expand all points in parallel.
**Future**: any structural-outline-then-parallel-expansion reasoning.
**Broad-use contexts**: parallel LLM reasoning, documentation generation, essay writing, project planning (outline then parallel-fill), scientific literature review synthesis.
**Every context needs**: skeleton generation (outline/structure), parallel expansion of points, aggregation.
**Varies**: skeleton depth, parallelism degree, convergence criteria.
**Extension**: `DocumentSkeletonOfThought`, `CodeSkeletonOfThought`, `DeepSkeletonOfThought`.

## 184. `WhyClimb` · Mind/Reasoning · R2T1

**Intended**: recursive "Why is this a problem?" to Reframe problem and reach actionable ceiling.
**Future**: any ascend-the-abstraction-ladder operation.
**Broad-use contexts**: product-requirement dives (why do we want this feature?), scientific-motivation questioning, philosophical "what do you really want?" dialogues, system-redesign driver identification.
**Every context needs**: problem statement, recursive "why" iterator, ceiling detector (highest actionable level).
**Varies**: ceiling criteria, recursion bound, evidence requirement per level.
**Extension**: `BoundedWhyClimb`, `EvidenceWhyClimb`, `BranchingWhyClimb`.

## 185. `StrategicReading` · Mind/Reasoning · R2T2

**Intended**: non-linear information retrieval — treat documents as random-access databases.
**Future**: any "read like a researcher, not sequentially" heuristic.
**Broad-use contexts**: research paper consumption, legal document review, codebase exploration, long-context LLM strategies, executive document skimming, reference manual navigation.
**Every context needs**: structural map building (Tree), high-entropy section identification, selective loading.
**Varies**: map-construction method, entropy metric, compute budget, stopping criteria.
**Extension**: `AcademicStrategicReading`, `CodebaseStrategicReading`, `LegalStrategicReading`.

## 186. `SelfConsistency` · Mind/Reasoning · R2T2

**Intended**: variance-reduction — sample N reasoning chains independently, select by majority.
**Future**: any ensemble-reasoning technique using mode selection.
**Broad-use contexts**: LLM inference ensembling, Monte Carlo decision procedures, majority-vote diagnosis, robust forecasting, jury trials (analogy), replication studies.
**Every context needs**: multiple independent runs, aggregation by mode, majority-select final answer.
**Varies**: sample count, independence mechanism, tiebreaker, weighted vs unweighted mode.
**Extension**: `WeightedSelfConsistency`, `HighVarianceSelfConsistency`, `IncrementalSelfConsistency`.

## 187. `ReAct` · Mind/Reasoning · R2T1

**Intended**: interleaved Thought-Action-Observation cycle.
**Future**: any reasoning-with-environmental-feedback loop.
**Broad-use contexts**: ToolUse agents, scientific experimentation loops, debugging loops, debugging with live inspection, conversational-assistant loops, robotic loops.
**Every context needs**: Thought step, Action step (ToolInvoke), Observation step, context update with observation results.
**Varies**: step count, failure-recovery policy, parallel action support, cost-of-thought.
**Extension**: `CostAwareReAct`, `ParallelReAct`, `SelfCorrectingReAct`.

## 188. `PerspectiveEnsemble` · Mind/Strategy · R2T2

**Intended**: instantiate N virtual personas to debate a problem from pre-defined viewpoints.
**Future**: any "multiple expert perspectives simulated" reasoning method.
**Broad-use contexts**: consultant-simulation LLM prompts, devils-advocate inclusion, ethical-dilemma multi-stakeholder analysis, red/blue/purple team discussion, imaginary-expert panels.
**Every context needs**: persona set, debate protocol, synthesis from interaction, Steelmanning of opposing views.
**Varies**: persona count, persona definitions, synthesis method (aggregate vs dialectic).
**Extension**: `FourHatsEnsemble`, `StakeholderEnsemble`, `AdversarialEnsemble`.

## 189. `Invert` · Mind/Reasoning · R2T2

**Intended**: negation-based solution discovery — ask "how would I guarantee failure?"
**Future**: any "solve via the opposite" heuristic.
**Broad-use contexts**: Munger-style inversion, pre-mortem thinking, failure-mode-driven design, security (how would I break this?), testing (how might this fail?), strategic red-teaming.
**Every context needs**: goal reformulation to negation, enumeration of failure paths, inversion to get success candidates.
**Varies**: negation specificity, enumeration depth, validation of inverted candidates.
**Extension**: `AdversarialInvert`, `DesignInvert`, `SecurityInvert`.

## 190. `LateralOptimization` · Mind/Strategy · R1T2

**Intended**: Reframe → Optimize → Translate loop — shift domains to find easier problem structure.
**Future**: any "solve in a different domain and map back" creativity technique.
**Broad-use contexts**: analogical problem-solving, cross-domain innovation, mathematical transformation (Fourier, Laplace), biomimicry engineering, metaphorical reasoning.
**Every context needs**: source domain problem, target-domain mapping, optimization in target, mapping back (Translate).
**Varies**: domain-pair fit, translation fidelity, iteration across multiple target domains.
**Extension**: `BiomimicryLateral`, `MathematicalLateral`, `InterdisciplinaryLateral`.

## 191. `PhasedRefinement` · Society/Protocols · R2T2

**Intended**: layered multi-pass improvement — each pass targets a specific abstraction level.
**Future**: any abstraction-ordered refinement pipeline.
**Broad-use contexts**: manuscript editing (logic → structure → prose → polish), code review layers (correctness → design → style), design iteration cycles, curriculum development.
**Every context needs**: ordered pass sequence, per-pass target abstraction, gate between passes.
**Varies**: pass count, pass ordering, gate strictness, rollback on late-discovered lower-level issue.
**Extension**: `EditorialPhasedRefinement`, `CodeReviewPhasedRefinement`, `DesignPhasedRefinement`.

## 192. `SacrificialProbe` · Mind/Strategy · R2T2

**Intended**: cheap, instructive failure — send a low-cost probe designed to fail informatively.
**Future**: any "fail cheaply to learn" strategy.
**Broad-use contexts**: startup landing-page tests, military recon (deliberately expendable), A/B test cheap variants, dendritic cells in immunology, canary deployments (analogous), reconnaissance-in-force.
**Every context needs**: probe cost << main payload cost, instructive-failure-mode design, strategy update on failure signal.
**Varies**: probe-main cost ratio, failure-mode taxonomy, update rule, number of probes before committing.
**Extension**: `MarketSacrificialProbe`, `TechnicalSacrificialProbe`, `SecuritySacrificialProbe`.

## 193. `ScoringFunction` · Infrastructure/Data Structures · R1T1

**Intended**: deterministic logic mapping input artifact → scalar Score.
**Future**: any objective-function artifact.
**Broad-use contexts**: ML loss functions, game score functions, aesthetic evaluators, risk scoring, fitness functions, relevance rankers, judging rubrics.
**Every context needs**: deterministic mapping, input artifact, scalar Score output.
**Varies**: function complexity, gradient availability, multi-objective aggregation, context-sensitivity.
**Extension**: `GradientScoringFunction`, `MultiObjectiveScoringFunction`, `ContextSensitiveScoringFunction`.
**Note for audit**: §3.5 wires `Rank` and `Judge` → `accepts ScoringFunction`. Broad-use validates — ScoringFunction is caller-supplied logic, not an internal pattern invocation.

## 194. `ShoutWhisper` · Society/Protocols · R1T1

**Intended**: dual-mode communication — broadcast high-level intent, switch to encrypted P2P for coordination.
**Future**: any "discover publicly, coordinate privately" communication pattern.
**Broad-use contexts**: BitTorrent tracker + swarm, dating app match + DM, public forums → DM channels, conference discovery → side conversations, gossip protocols with private channels.
**Every context needs**: broadcast-for-discovery, switch-to-private-channel, encryption for the private phase.
**Varies**: broadcast channel specifics, switching protocol, encryption strength, scalability.
**Extension**: `BitTorrentShoutWhisper`, `EndToEndShoutWhisper`, `FederatedShoutWhisper`.

## 195. `SolverNode` · Society/Protocols · R1T1

**Intended**: stateful container wrapping a SolverManifest with dynamic state.
**Future**: any runtime-solver-instance holder.
**Broad-use contexts**: LLM agent instances, workflow engine tasks, ML training runs, research project instances, experiment executions.
**Every context needs**: static manifest reference, dynamic state (partial solution, budget, status), parent-node communication, blame-attribution semantic.
**Varies**: state schema, persistence, checkpointing, resumability, state migration.
**Extension**: `PersistentSolverNode`, `CheckpointingSolverNode`, `MigratableSolverNode`.

## 196. `SomaticMarker` · Society/Protocols · R2T1

**Intended**: "gut feeling" signal from system health metrics acting as inhibitory emotion.
**Future**: any internal-signal-as-inhibitor-of-action mechanism.
**Broad-use contexts**: Damasio's somatic-marker hypothesis, system stress → action inhibition, burnout detection, rate-limit proximity awareness, biological fatigue signaling.
**Every context needs**: health metrics, aggregation into "stress" signal, inhibitory effect on action initiation.
**Varies**: metric set, aggregation function, threshold calibration, override mechanism.
**Extension**: `BurnoutSomaticMarker`, `RateLimitSomaticMarker`, `AttentionSomaticMarker`.
**Note**: SomaticMarker's mechanism "utilizes Task" is an odd wiring claim — Task as a Noun doesn't seem like the right dep. Worth spot-checking.

## 197. `SourceEvaluate` · Society/Protocols · R2T2

**Intended**: incentive-aware evidence weighting — Judge-module for evaluating sources.
**Future**: any credibility-assessment mechanism.
**Broad-use contexts**: journalism fact-checking, academic peer review, witness evaluation in court, intelligence-source evaluation, RAG-source ranking, testimony weighting.
**Every context needs**: source identification, track-record evaluation, incentive analysis, expertise check, credibility weighting.
**Varies**: track-record horizon, incentive model sophistication, transparency of evaluation, bias-accounting.
**Extension**: `FactCheckSourceEvaluate`, `IntelligenceSourceEvaluate`, `RAGSourceEvaluate`.

## 198. `SpectralTune` · Society/Protocols · R1T1

**Intended**: verify ontology alignment before data transfer — hash-based semantic-context challenges.
**Future**: any "resonance check" protocol pre-communication.
**Broad-use contexts**: ontology-alignment protocols, semantic-interop version checks, API-compatibility-handshake pre-data, cultural-context verification, language-pair validation.
**Every context needs**: tuning signal (hash challenges), receiver resonance proof, semantic context ontology.
**Varies**: challenge count, hash granularity, retry on mis-tune, adaptive tuning.
**Extension**: `OntologySpectralTune`, `VersionSpectralTune`, `AdaptiveSpectralTune`.

## 199. `FeatureFlag` · Society/Protocols · R1T1

**Intended**: runtime functionality toggle decoupling deployment from release.
**Future**: any runtime-configurable enablement mechanism.
**Broad-use contexts**: software feature flags, A/B tests, progressive rollout, kill switches, experimentation frameworks, canary toggles.
**Every context needs**: toggle point, condition evaluation, enable/disable semantics, runtime updatability.
**Varies**: condition complexity (user-based, percentage, time-based), retention policy (permanent vs experiment), monitoring integration.
**Extension**: `UserFeatureFlag`, `ExperimentFeatureFlag`, `KillSwitchFeatureFlag`, `GradualFeatureFlag`.

## 200. `Sandbox` · Infrastructure/Primitives · R1T2

**Intended**: isolation boundary restricting side effects.
**Future**: any "contained execution environment."
**Broad-use contexts**: OS sandboxes (gVisor, Firecracker), browser sandboxes, test fixtures, simulation environments, experimental workspaces, regulatory sandboxes (fintech).
**Every context needs**: isolation boundary, side-effect restriction, controlled exit/escape.
**Varies**: isolation strength (syscall filter vs container vs VM), resource limits, network restrictions, persistence.
**Extension**: `StrongSandbox`, `LightweightSandbox`, `NetworkIsolatedSandbox`, `RegulatorySandbox`.

---

## Observations from batch 10

**200-pattern milestone.** Half the library audited through the broad-use lens. The methodology has held consistently across all four layers, all tier levels, all ring levels, all major categories. No discovered patterns required us to rewrite the broad-use test — the enumerate-contexts → intersect-needs → find-variation approach works uniformly.

**New audit items surfaced in batch 10.**
37. **`SomaticMarker` wiring claim "Utilizes Task"** is odd — Task is a Noun, so the dep should be `accepts` not `composes_with`. Worth spot-checking against the broader reference-density pass.
38. **`Sandbox` at R1T2** — the mechanism is a single sentence. Broad-use test passes because the foundation IS just "an isolated execution environment that restricts side effects" — descendants specify isolation mechanism. Good example of minimal foundation.
39. **`PhasedRefinement`'s reference to `Aesthetics`** — Aesthetics is moving Society → Infra/Data Structures per batch 8 observation. Update PhasedRefinement's mechanism to reflect the move.

Total analyzed: 200 patterns. Remaining: 229. The methodology is proving remarkably durable — each batch surfaces 3-5 audit items but the test itself is stable.

---

## Batch 11 — classical reasoning macros + Infrastructure core + control primitives

## 201. `ChainOfThought` · Mind/Reasoning · R2T2

**Intended**: canonical sequential reasoning — Macro for Think(Chain).
**Future**: any step-by-step derivation mode.
**Broad-use contexts**: LLM CoT prompting, mathematical proof derivation, step-by-step tutorials, forensic reconstruction, audit trails of reasoning.
**Every context needs**: sequential derivation, linear chain topology, step visibility.
**Varies**: step granularity, self-correction interleaving (StepBack, Reflexion), compression of intermediate steps.
**Extension**: `VerboseChainOfThought`, `CompressedChainOfThought`, `SelfCorrectingChainOfThought`.

## 202. `TreeOfThoughts` · Mind/Reasoning · R2T2

**Intended**: canonical branching reasoning — Macro for Think(Tree).
**Future**: any branching-exploration reasoning mode.
**Broad-use contexts**: game tree search, multi-hypothesis reasoning, solution-space exploration, parallel strategy evaluation.
**Every context needs**: branching topology, backtracking or pruning, path evaluation.
**Varies**: breadth at each level, pruning policy, evaluation heuristic, beam width.
**Extension**: `BeamTreeOfThoughts`, `AlphaBetaTreeOfThoughts`, `MCTSTreeOfThoughts`.

## 203. `Reflexion` · Mind/Reasoning · R2T1

**Intended**: self-critique after failure, feeding reflection as context for retry.
**Future**: any self-improvement loop via textual self-critique.
**Broad-use contexts**: LLM agent self-improvement, post-mortem culture, after-action reviews, journaling for learning, code review incorporation.
**Every context needs**: task attempt, linguistic self-critique generation, episodic memory buffer, retry with critique in context.
**Varies**: critique depth, buffer size, retry budget, memory-eviction policy.
**Extension**: `EpisodicReflexion`, `BudgetedReflexion`, `StructuredReflexion`.

## 204. `HeuristicSnap` · Mind/Reasoning · R2T1

**Intended**: fast pattern-match against cached experience — <100ms decisions bypassing reasoning chains.
**Future**: any "quick intuitive response from memory" mechanism.
**Broad-use contexts**: System-1 intuition, expert rapid judgment, flash diagnostic decisions, chess blitz moves, driving reflexes, fast-attention routing.
**Every context needs**: cached experience database, similarity matching, low-latency decision.
**Varies**: cache-hit threshold, fallback to deep reasoning, cache-freshness policy.
**Extension**: `ExpertHeuristicSnap`, `CacheSizedHeuristicSnap`, `FallbackHeuristicSnap`.

## 205. `Decompose` · Mind/Reasoning · R2T1

**Intended**: split a task into independent subordinate parts where each part solved in isolation yields solution to whole.
**Future**: any divide-and-conquer reasoning operation.
**Broad-use contexts**: algorithm divide-and-conquer, organizational task splitting, scientific problem decomposition, hierarchical planning, modular design.
**Every context needs**: task to decompose, independence criterion (subproblems don't interact), recursion base case.
**Varies**: decomposition axis, recursion depth, re-compose strategy.
**Extension**: `HierarchicalDecompose`, `ParallelDecompose`, `OrthogonalDecompose`.

## 206. `LeastToMost` · Mind/Reasoning · R2T1

**Intended**: solve subproblems from easiest to hardest — each solution becomes context for the next.
**Future**: any progressive-difficulty sequential reasoning strategy.
**Broad-use contexts**: pedagogical scaffolding, curriculum design, puzzle solving, mathematical induction, LLM prompting strategy, algorithm training.
**Every context needs**: decomposition, difficulty ordering, sequential solving with solution-as-context passing.
**Varies**: difficulty metric, ordering stability, optional skipping if an easy problem provides insight.
**Extension**: `PedagogicalLeastToMost`, `AdaptiveLeastToMost`, `BranchingLeastToMost`.

## 207. `Strategy` · Mind/Strategy · R1T1

**Intended**: adaptive high-level plan under uncertainty ("How to win" vs "What steps").
**Future**: any adaptive-intent framework.
**Broad-use contexts**: military strategy, business strategy, research strategy, competitive game strategies, career strategies, negotiation strategies.
**Every context needs**: high-level goal, uncertainty acknowledgment, adaptive stance, success criteria.
**Varies**: planning horizon, adaptation frequency, revision triggers, scope.
**Extension**: `CompetitiveStrategy`, `CooperativeStrategy`, `AdaptiveStrategy`.

## 208. `Parallelize` · Mind/Strategy · R0T1

**Intended**: run subtasks simultaneously and aggregate — Sectioning or Voting modes.
**Future**: any concurrent-LLM-call pattern.
**Broad-use contexts**: parallel LLM calls, map-reduce, ensemble methods, concurrent tool use, parallel research, A/B testing.
**Every context needs**: task, decomposition or replication, concurrent execution, aggregation.
**Varies**: mode (Section vs Vote), concurrency degree, aggregation function, failure handling.
**Extension**: `SectioningParallelize`, `VotingParallelize`, `CostAwareParallelize`.

## 209. `Monitor` · Mind/Strategy · R0T0

**Intended**: continuous observation loop comparing state against baseline, emit signal on deviation.
**Future**: any observer-loop-over-target.
**Broad-use contexts**: infrastructure monitoring, health monitoring, anomaly detection, vigilance patterns, quality assurance monitoring, compliance monitoring.
**Every context needs**: target, observation loop, baseline, deviation detection, signal emission on anomaly.
**Varies**: interval (Duration, per §3.17 — no arbitrary range), baseline adaptation, threshold, signal routing.
**Extension**: `HealthMonitor`, `SecurityMonitor`, `PerformanceMonitor`, `ComplianceMonitor`.

## 210. `OptimalStop` · Mind/Strategy · R2T2

**Intended**: resource-aware search termination via 1/e rule or Marginal Gain threshold.
**Future**: any optimal-stopping decision rule.
**Broad-use contexts**: secretary problem, apartment hunting, partner selection, when-to-stop-searching decisions, product-launch timing, optimal-selling-time in markets.
**Every context needs**: search-in-progress state, stopping criterion (1/e for no-recall, Marginal Gain for recall), termination decision.
**Varies**: recall_allowed (Boolean, principled per §3.17), budget, cost estimation, quality estimation.
**Extension**: `SecretaryOptimalStop`, `RecallOptimalStop`, `BudgetedOptimalStop`.

## 211. `Artifact` · Infrastructure/Data Structures · R0T1

**Intended**: discrete, immutable data unit produced by solver/workflow.
**Future**: any typed I/O artifact.
**Broad-use contexts**: workflow outputs, build artifacts, document versions, research outputs, media files, data products, messages between services.
**Every context needs**: discrete-ness, immutability, typing for pipeline integration.
**Varies**: medium (bytes, tokens, structured data), provenance tracking, addressability (hash or ID), size bounds.
**Extension**: `HashedArtifact`, `TypedArtifact`, `StreamingArtifact`, `VersionedArtifact`.

## 212. `Spec` · Infrastructure/Data Structures · R0T1

**Intended**: rigorous definition of requirements for an artifact — "Definition of Done."
**Future**: any requirements artifact.
**Broad-use contexts**: software specs, API specs, standard specifications (RFCs), legal specifications, product specs, scientific-experiment protocols.
**Every context needs**: shape/behavior/constraint definitions, distinction from Plan (how to build) and Goal (what to achieve).
**Varies**: formality (formal vs natural language), machine-readability, completeness (partial specs allowed), versioning.
**Extension**: `FormalSpec`, `APISpec`, `TestableSpec`, `ExecutableSpec`.

## 213. `System` · Infrastructure/Data Structures · R0T1

**Intended**: complex whole of interacting parts with boundaries, structure, purpose.
**Future**: any coherent-whole abstraction.
**Broad-use contexts**: software systems, biological systems, social systems, ecological systems, economic systems, legal systems, mental systems.
**Every context needs**: component parts, interactions, boundary definition, purpose/function.
**Varies**: hierarchical vs flat, closed vs open, static vs dynamic, observability.
**Extension**: `ClosedSystem`, `AdaptiveSystem`, `HierarchicalSystem`, `EmergentSystem`.

## 214. `Proposal` · Infrastructure/Data Structures · R1T1

**Intended**: formal message suggesting a specific Act or Transition.
**Future**: any suggested-course-of-action artifact.
**Broad-use contexts**: legislative proposals, academic proposals, business proposals, PR (pull requests), RFC (Request for Comment), design proposals.
**Every context needs**: what is being proposed, why (rationale), target decision-making process.
**Varies**: approval mechanism, amendment semantics, sponsor identity, urgency.
**Extension**: `LegislativeProposal`, `AcademicProposal`, `BusinessProposal`, `PullRequestProposal`.

## 215. `Prototype` · Infrastructure/Data Structures · R1T1

**Intended**: early sample/model built to test a concept, low-fidelity and disposable.
**Future**: any throw-away early version.
**Broad-use contexts**: software prototypes, scientific prototypes, product prototypes, design prototypes, educational mock-ups, proof-of-concepts.
**Every context needs**: low-fidelity construction, concept-testing purpose, disposability semantic.
**Varies**: fidelity level, concept specificity, feedback-capture mechanism, iteration budget.
**Extension**: `HighFidelityPrototype`, `FocusedPrototype`, `RapidPrototype`.

## 216. `Quorum` · Infrastructure/Primitives · R0T1

**Intended**: threshold-checking primitive — count Ballot signals vs K threshold.
**Future**: any "enough participants?" gating primitive.
**Broad-use contexts**: consensus protocols, board meetings, blockchain block validation, Byzantine fault tolerance, emergency-decision quorum.
**Every context needs**: participant count, threshold K, yes/no return.
**Varies**: K value, weighted vs equal votes, timeout integration.
**Extension**: `WeightedQuorum`, `TimedQuorum`, `ByzantineQuorum`.

## 217. `CircuitBreaker` · Infrastructure/Primitives · R1T1

**Intended**: fail-fast protection via state machine (CLOSED → OPEN → HALF-OPEN).
**Future**: any cascading-failure protection mechanism.
**Broad-use contexts**: network circuit breakers, psychological circuit breakers (emotional shutoffs), economic circuit breakers (market halts), database circuit breakers, API backpressure.
**Every context needs**: three-state machine, failure-rate monitoring, timeout-based state transitions.
**Varies**: reset_timeout (Duration, see §3.17 — no arbitrary range), failure threshold, trial-request count in HALF-OPEN, fallback behavior.
**Extension**: `AdaptiveCircuitBreaker`, `DistributedCircuitBreaker`, `HysteresisCircuitBreaker`.

## 218. `Actor` · Infrastructure/Primitives · R0T0

**Intended**: capability-bearing execution entity (pure execution, no intent).
**Future**: any pure-execution unit without reasoning.
**Broad-use contexts**: Actor Model systems, microservices, tool containers, serverless functions, physical actuators, organizational roles as pure-execution.
**Every context needs**: identity, nature, capability set.
**Varies**: capability scope, persistence, address-ability, mailbox semantic.
**Extension**: `MailboxActor`, `PersistentActor`, `StatelessActor`, `HierarchicalActor`.

## 219. `Loop` · Infrastructure/Primitives · R0T1

**Intended**: control flow structure repeating work until condition met.
**Future**: any repeat-until-condition mechanism.
**Broad-use contexts**: for/while loops in programming, biological-feedback loops, retry loops, polling loops, perception-action cycles, game loops.
**Every context needs**: work to repeat, termination condition.
**Varies**: iteration bound, condition evaluation timing (pre/post), break/continue semantics, parallelism.
**Extension**: `BoundedLoop`, `EventLoop`, `PollingLoop`, `FeedbackLoop`.

## 220. `Feedback` · Infrastructure/Primitives · R0T1

**Intended**: information returned about action effects, used to adjust future behavior.
**Future**: any error-correction-via-output-to-input signal.
**Broad-use contexts**: control theory, RLHF, performance reviews, product user feedback, biological nervous system feedback, artistic critique.
**Every context needs**: result observation, metric-of-deviation (from expected), adjustment mechanism for future behavior.
**Varies**: metric type, delay, continuous vs discrete, signed vs unsigned (positive feedback vs negative).
**Extension**: `NegativeFeedback`, `PositiveFeedback`, `DelayedFeedback`, `ReinforcementFeedback`.

---

## Observations from batch 11

**Classical reasoning macros validate as clean abstractions.** ChainOfThought, TreeOfThoughts, Reflexion, ReAct (from batch 10) — each is a macro over Think() with a specific topology. This "canonical implementation of X" framing captures the family structure cleanly. Future macros (ParallelChains, GraphOfThoughts, etc.) can follow the same shape.

**Control primitives (Loop, Feedback, CircuitBreaker, Quorum, Actor) are minimal by design.** Each sits at R0T0 or R0T1 with very short mechanism text. Broad-use test passes because descendants add everything context-specific. Good "generalize at foundation" examples.

**New audit items from batch 11.**
40. **`Monitor` at R0T0 with Mind/Strategy categorization** — the mechanism uses `{{loop}}` + `{{observe}}`, both of which are Verbs/Primitives. Monitor itself is also a Verb (continuously observing). Categorization as Mind/Strategy seems off — Strategy is for high-level planning, not observation loops. Monitor might fit Infrastructure/Primitives or Mind/Memory better. Worth flagging.
41. **`System` definition is very general** — borderline risk of being too vague. But broad-use spans software/biological/social/etc., so the generality is needed. Passes.
42. **`Proposal` references `Message` directly** — check declared dep.
43. **`CircuitBreaker.reset_timeout`** — per §3.17, this should be `Duration` type with no range. Confirmed by broad-use (simple retries: ms, batch pipelines: days).

Total analyzed: 220 patterns. Remaining: 209. We're past 50% of the library.

---

## Batch 12 — Mind/Reasoning remaining + Infrastructure/Primitives remaining

## 221. `Interpret` · Mind/Reasoning · R0T0

**Intended**: apply semantic context to raw signal to extract value — change abstraction level, not form.
**Future**: any semantic-extraction operation.
**Broad-use contexts**: LLM input processing, legal-text interpretation, scientific-data interpretation, musical interpretation, historical interpretation, medical imaging interpretation.
**Every context needs**: semantic context, raw input, value extraction, distinction from Translate (which preserves form/changes format) and Summarize (which loses info).
**Varies**: context richness, interpretation depth, confidence tracking.
**Extension**: `LegalInterpret`, `MedicalInterpret`, `ContextualInterpret`.

## 222. `Reason` · Mind/Reasoning · R1T1

**Intended**: orchestrated cognition chaining multiple Think steps using a specific topology.
**Future**: any multi-step structured cognition.
**Broad-use contexts**: CoT, ToT, GoT, BFS/DFS reasoning, ReAct loops, debate-based reasoning, chain-of-verification.
**Every context needs**: topology, multiple Think steps, context-to-conclusion transformation, compute_budget respect.
**Varies**: topology type, step count, self-correction integration, feedback loops.
**Extension**: `LinearReason`, `BranchingReason`, `GraphReason`, `ReactiveReason`.

## 223. `Translate` · Mind/Reasoning · R1T1

**Intended**: convert form while preserving semantic meaning.
**Future**: any form-conversion-meaning-preservation operation.
**Broad-use contexts**: language translation, format conversion (JSON↔XML), code transpilation, protocol translation, data migration, unit conversion.
**Every context needs**: source schema, target schema, meaning preservation, distinction from Summarize (lossy) and Interpret (adds meaning).
**Varies**: fidelity requirements, ambiguity handling, bidirectional vs one-way, real-time vs batch.
**Extension**: `BidirectionalTranslate`, `LossyTranslate` (borderline—compare to Summarize), `VerifiedTranslate`.

## 224. `Summarize` · Mind/Reasoning · R1T1

**Intended**: lossy compression preserving salience — smaller artifact with high-value info retained.
**Future**: any lossy-compression-with-semantic-selection.
**Broad-use contexts**: document summarization, conversation recaps, executive summaries, abstract generation, meeting-notes compression, news summarization.
**Every context needs**: source artifact, smaller output, salience-preservation criterion, explicit lossy-ness.
**Varies**: compression ratio, salience determination method, domain specificity, target-audience awareness.
**Extension**: `ExecutiveSummarize`, `AbstractSummarize`, `SalienceWeightedSummarize`.

## 225. `Generalize` · Mind/Reasoning · R2T1

**Intended**: inductive pattern extraction — multiple instances → shared-structure invariant.
**Future**: any "find the rule that covers these cases" operation.
**Broad-use contexts**: inductive reasoning, ML pattern learning, scientific generalization, legal precedent extraction, category formation, hypothesis generation.
**Every context needs**: multiple instances, shared-structure identification, invariant statement, predictive test.
**Varies**: instance count required, invariant-validation method, abstraction level.
**Extension**: `StatisticalGeneralize`, `StructuralGeneralize`, `PatternGeneralize`.

## 226. `Specialize` · Mind/Reasoning · R2T1

**Intended**: concrete instantiation — abstract principle → specific case with substituted values.
**Future**: any "apply the general rule to this specific case" operation.
**Broad-use contexts**: deductive application, template instantiation, generic-function specialization, case-law application, policy application to specific incidents.
**Every context needs**: abstract principle, substitution mechanism, constraint verification post-substitution.
**Varies**: substitution depth, edge-case discovery, range-of-specialization generation.
**Extension**: `TemplateSpecialize`, `LegalSpecialize`, `CompilerSpecialize`.

## 227. `Eliminate` · Mind/Reasoning · R2T1

**Intended**: Sherlock Holmes deduction — enumerate possibilities, falsify in cost order.
**Future**: any falsification-based elimination search.
**Broad-use contexts**: detective work, differential diagnosis, debugging, multiple-choice test strategy, constraint-satisfaction narrowing, suspect elimination.
**Every context needs**: enumerated possibility space, falsification tests, cost-ordered application, remaining candidates.
**Varies**: enumeration completeness, test cost estimation, tie-break policy when multiple remain.
**Extension**: `MedicalEliminate`, `DebuggingEliminate`, `CSPEliminate`.

## 228. `BackwardChain` · Mind/Reasoning · R2T1

**Intended**: goal-first decomposition — recursively identify prerequisites from desired end-state.
**Future**: any goal-directed reverse-reasoning method.
**Broad-use contexts**: goal-oriented planning, Prolog-style inference, dependency resolution, project planning (start from deadline), reverse engineering, medical treatment planning.
**Every context needs**: goal/end-state, recursive prerequisite identification, termination at known facts or actionable steps.
**Varies**: depth limit, cycle detection, fact-database lookup method.
**Extension**: `PrologBackwardChain`, `PlannerBackwardChain`, `MedicalBackwardChain`.

## 229. `Decision` · Mind/Reasoning · R1T1 (post-§3.11 mechanism rewrite)

**Intended**: the committed choice resulting from selection — an irrevocable selection artifact.
**Future**: any "committed choice" result-noun.
**Broad-use contexts**: policy decisions, medical decisions, strategic decisions, resource-allocation decisions, decision-trees (output leaves), governance decisions.
**Every context needs**: the specific chosen option, reference to deliberation context, commitment semantic.
**Varies**: reversibility, precedent-setting power, audit trail, confidence of decision.
**Extension**: `IrrevocableDecision`, `PrecedentDecision`, `AuditedDecision`.
**Note**: §3.18 flagged Decision as Noun-with-Verb-mechanism. The §3.11-style rewrite preserves Decision as the artifact (committed choice) and lets `Decide` (if minted) be the Verb.

## 230. `SteelmanCheck` · Mind/Reasoning · R1T2

**Intended**: mandatory counter-argument generation — generate strongest argument against own conclusion.
**Future**: any adversarial-self-test mechanism.
**Broad-use contexts**: epistemic hygiene before publishing, pre-meeting preparation, red-team-of-self, test-of-decision robustness, bias-resistance discipline.
**Every context needs**: current decision/output, counter-argument generation, validity threshold, revise-on-strong-counter.
**Varies**: counter-argument generation method, threshold calibration, revision strategy on failure.
**Extension**: `AdversarialSteelmanCheck`, `BayesianSteelmanCheck`, `RigorousSteelmanCheck`.

## 231. `Parsimony` · Mind/Reasoning · R2T1

**Intended**: Occam's Razor judgment — classify topology complexity as Bloated/Under-specified/Minimal.
**Future**: any "simplest explanation wins" evaluation.
**Broad-use contexts**: theory selection, ML model selection, system architecture review, design simplification, Occam's Razor decisions, regulatory streamlining.
**Every context needs**: candidate structure, ablation test (remove component, check function), three-class output.
**Varies**: ablation rigor, multi-objective weighting, domain-specific simplicity metrics.
**Extension**: `StatisticalParsimony`, `StructuralParsimony`, `AblationParsimony`.

## 232. `RecursionDive` · Mind/Reasoning · R2T1

**Intended**: vertical traversal of solver tree — accept solver_node, apply Decompose, generate children.
**Future**: any recursive-descent decomposition mechanism.
**Broad-use contexts**: solver trees (FI v3), recursive descent parsers, hierarchical planning, divide-and-conquer algorithms, fractal refinement.
**Every context needs**: solver node input, decomposition application, child node generation, traversal downward.
**Varies**: depth bound, termination criteria (leaf conditions), parallelism, backtrack support.
**Extension**: `BoundedRecursionDive`, `ParallelRecursionDive`, `BacktrackingRecursionDive`.

## 233. `Verification` · Mind/Reasoning · R1T1

**Intended**: confirm claim/artifact adheres to spec or reality — yields binary Truth.
**Future**: any truth-value-confirming check.
**Broad-use contexts**: proof verification, test verification, regulatory verification, compliance verification, scientific replication, witness verification.
**Every context needs**: claim to verify, spec or reality reference, Check-based mechanism, binary yield.
**Varies**: spec formality, evidence requirements, independence of verifier, verification depth.
**Extension**: `FormalVerification`, `EmpiricalVerification`, `IndependentVerification`.

## 234. `Estimate` · Mind/Reasoning · R1T1

**Intended**: predictive resource-cost calculation before execution, producing Bid with confidence intervals.
**Future**: any predictive-cost-projection operation.
**Broad-use contexts**: effort estimation in software, project cost estimation, consulting-engagement scoping, solver bidding, research budget estimates, attention-allocation estimates.
**Every context needs**: task being estimated, two modes (HeuristicSnap fast, Simulation accurate), Bid-with-CI output, meta-cap (estimation consumes budget).
**Varies**: mode selection criterion, confidence-interval method, calibration tracking.
**Extension**: `FermiEstimate`, `SimulationEstimate`, `HybridEstimate`.

## 235. `Aggregate` · Infrastructure/Primitives · R0T1

**Intended**: mathematical reduction — Vector → Scalar via deterministic function.
**Future**: any "reduce many to one" operation.
**Broad-use contexts**: mean/median/mode computation, vote counting, ensemble aggregation, sensor fusion, database SUM/COUNT/AVG, opinion aggregation.
**Every context needs**: input set/vector, deterministic reduction function, scalar output.
**Varies**: aggregation function, handling of missing values, weighted vs unweighted, incremental vs batch.
**Extension**: `MeanAggregate`, `ModeAggregate`, `WeightedAggregate`, `StreamingAggregate`.

## 236. `Backoff` · Infrastructure/Primitives · R0T2

**Intended**: exponential delay to reduce contention — multiplier growth + jitter + cap.
**Future**: any contention-reducing delay strategy.
**Broad-use contexts**: retry backoff, thundering-herd prevention, rate-limit recovery, connection retry, TCP congestion, SaaS API integration.
**Every context needs**: initial delay, multiplier, jitter, cap.
**Varies**: multiplier value, jitter distribution, cap value, reset-on-success semantic, per-target vs global.
**Extension**: `ExponentialBackoff`, `JitteredBackoff`, `FibonacciBackoff`, `AdaptiveBackoff`.

## 237. `Combine` · Infrastructure/Primitives · R0T1

**Intended**: binary merge of two same-typed values; associative, with Empty as identity.
**Future**: any associative merge operation.
**Broad-use contexts**: monoid operations, CRDT merges, reduce operations, set unions, vector addition, string concatenation.
**Every context needs**: two inputs of same type, associativity, identity element.
**Varies**: commutativity (monoid vs commutative monoid), idempotency (CRDT), element-type specificity.
**Extension**: `CommutativeCombine`, `IdempotentCombine`, `TypedCombine`.

## 238. `Incongruity` · Infrastructure/Primitives · R0T1

**Intended**: misalignment between expectation and reality — the difference between predicted and observed.
**Future**: any prediction-error signal.
**Broad-use contexts**: humor (classic theory), paradox detection, learning signals, debugging (this isn't what I expected), anomaly detection, cognitive dissonance.
**Every context needs**: prediction, observation, difference/mismatch computation.
**Varies**: difference metric, severity scaling, routing of incongruity signal.
**Extension**: `PredictionIncongruity`, `CognitiveIncongruity`, `LearningIncongruity`.

## 239. `NegativeProof` · Infrastructure/Primitives · R1T1

**Intended**: prove non-membership in a committed state set via ZK proof.
**Future**: any "prove absence cryptographically" mechanism.
**Broad-use contexts**: Merkle-tree non-inclusion proofs, privacy-preserving queries, "not on any sanctions list" attestations, absence-of-evidence proofs, blockchain state queries.
**Every context needs**: committed state set, specific value to check absence of, ZK proof mechanism.
**Varies**: commitment scheme (Merkle, Verkle, KZG, etc.), ZK proof system, domain size, proof size.
**Extension**: `MerkleNegativeProof`, `ZKRangeNegativeProof`, `SparseNegativeProof`.

## 240. `StateTransition` · Infrastructure/Primitives · R0T1

**Intended**: explicit FSM — Transition T: S × Event → S.
**Future**: any finite-state-machine transition semantic.
**Broad-use contexts**: programming FSMs, workflow engines, protocol state machines, biological state transitions, regulatory process state machines, UI state management.
**Every context needs**: state set, event set, transition function, only-valid-transitions rule.
**Varies**: deterministic vs non-deterministic, acceptance states, guards on transitions, actions-on-transition.
**Extension**: `DeterministicStateTransition`, `GuardedStateTransition`, `HierarchicalStateTransition`.

---

## Observations from batch 12

**Reasoning primitives (Interpret, Reason, Translate, Summarize) form a clean distinguishing set.** Each has explicit contrast with its neighbors in the mechanism ("Unlike X which does Y..."). Good example of foundation-level pattern differentiation that makes the namespace navigable.

**Control/math primitives (Aggregate, Backoff, Combine, Quorum, Loop) are beautifully minimal.** Each is a short mechanism at R0T0/R0T1, with descendants adding everything context-specific. The library's backbone.

**New audit items surfaced in batch 12.**
44. **`Decision`'s §3.18 Noun/Verb rewrite confirmed** — the broad-use sketch for Decision-as-artifact works cleanly (policy decisions, medical decisions, strategic decisions). The Verb form could be `Decide` (not minted; deferred).
45. **`Synthesis` analog** — same treatment as Decision. Broad-use for "the combined whole" artifact is straightforward; `Synthesize` as Verb could be minted separately if needed.
46. **`Translate` vs `LossyTranslate` vs `Summarize`** — there's a taxonomic question: at what lossiness does Translate become Summarize? Currently they're distinct (Translate preserves all meaning; Summarize discards). A "LossyTranslate" that discards some but not all might be useful; deferred.

Total analyzed: 240 patterns. Remaining: 189.

---

## Batch 13 — Infrastructure/Data Structures core Nouns + Mind/Strategy decision patterns

## 241. `Solution` · Infrastructure/Data Structures · R0T1

**Intended**: verifiable output container for a Task — provenance + artifact + sub-solution tree.
**Future**: any "this problem is solved" artifact.
**Broad-use contexts**: solver outputs, problem-solving workflows, scientific findings, engineering solutions, legal rulings, medical treatments.
**Every context needs**: output artifact, provenance (creator, time), component tree (sub-solutions used), acceptance-criteria validation.
**Varies**: fidelity level, provenance detail, storage medium, query-ability.
**Extension**: `SignedSolution`, `VerifiedSolution` (per §3.14: passed AcceptSpec), `ExperimentalSolution`.

## 242. `Context` · Infrastructure/Data Structures · R0T3

**Intended**: portable execution environment — constraints, tools, memory, identity.
**Future**: any "stack frame" of agentic execution.
**Broad-use contexts**: agent contexts, LLM conversation contexts, multi-turn dialogue state, subprocess environments, database transaction contexts, session state.
**Every context needs**: inherited constraints, available capabilities, working memory, identity claims.
**Varies**: persistence, serializability, transferability between agents, clone/fork semantics.
**Extension**: `PersistentContext`, `ClonableContext`, `ReadOnlyContext`, `IsolatedContext`.

## 243. `Constraint` · Infrastructure/Data Structures · R0T1

**Intended**: non-negotiable boundary condition that valid solutions must satisfy.
**Future**: any "hard limit" specification.
**Broad-use contexts**: resource budgets, safety bounds, legal compliance, physical laws, organizational policies, API rate limits, regulatory constraints.
**Every context needs**: boundary condition, non-compensatory semantic (can't offset one violation with another surplus), constraint type (Resource/Safety/Legal/Physical), Holographic Inheritance.
**Varies**: inheritance mechanism, violation-detection timing, override protocol (who can lift constraints).
**Extension**: `SafetyConstraint`, `BudgetConstraint`, `LegalConstraint`, `PhysicalConstraint`.

## 244. `Goal` · Infrastructure/Data Structures · R0T1

**Intended**: specification of desired end state — testable target work aims at.
**Future**: any "what we're trying to achieve" specification.
**Broad-use contexts**: OKRs, project goals, personal goals, scientific research goals, therapeutic goals, legal objectives, algorithmic optimization targets.
**Every context needs**: desired end-state description, testability (can evaluate Result against Goal), composability (AND/OR), prioritization.
**Varies**: quantitative vs qualitative, time horizon, stakeholder weighting, sub-goal hierarchy.
**Extension**: `MeasurableGoal`, `OKRGoal`, `CompositeGoal`, `PrioritizedGoal`.

## 245. `Problem` · Infrastructure/Data Structures · R1T1

**Intended**: formal state-gap where Cost of Inaction > 0 — descriptive claim about value loss.
**Future**: any diagnostic-level-framed situation needing attention.
**Broad-use contexts**: bug reports, medical complaints, engineering defects, social issues, scientific puzzles, business challenges, philosophical problems.
**Every context needs**: current-state description, desired-state description, non-zero cost of inaction, distinction from Task (directive) and Goal (target).
**Varies**: specificity, urgency, actor/scope, root-cause status (symptom vs root).
**Extension**: `SymptomProblem`, `RootCauseProblem`, `UrgentProblem`, `EmergentProblem`.

## 246. `Option` · Infrastructure/Data Structures · R1T1

**Intended**: discrete, actionable alternative within a decision space — mutually exclusive.
**Future**: any "one of several paths" selection unit.
**Broad-use contexts**: product selection, policy choices, architectural alternatives, game move options, medical treatment alternatives, financial product choices.
**Every context needs**: executable specification, mutual exclusivity with other options in set.
**Varies**: cost/benefit data attached, dependencies among options, reversibility.
**Extension**: `CostedOption`, `ReversibleOption`, `PreconditionalOption`.

## 247. `ProblemSpace` · Infrastructure/Data Structures · R0T1

**Intended**: bounded domain of a problem — region where solver operates.
**Future**: any scoped-solution-territory abstraction.
**Broad-use contexts**: search-space definitions, solver scope boundaries, research-project scope, design-space exploration, constraint-satisfaction domains.
**Every context needs**: constraints bounding the region, initial state, domain specification.
**Varies**: dimensionality, discreteness, explorability, enumerable vs continuous.
**Extension**: `DiscreteProblemSpace`, `ContinuousProblemSpace`, `HierarchicalProblemSpace`.

## 248. `Transition` · Infrastructure/Data Structures · R0T1

**Intended**: atomic progression from origin state to destination state.
**Future**: any state-to-state change unit.
**Broad-use contexts**: FSM transitions, database transactions, biological phase transitions, legal regime changes, software state updates, workflow advancements.
**Every context needs**: origin state, destination state, adherence to transition rules.
**Varies**: atomicity guarantees, reversibility, guards, pre/post conditions.
**Extension**: `GuardedTransition`, `ReversibleTransition`, `AtomicTransition`.

## 249. `Topology` · Infrastructure/Data Structures · R2T1

**Intended**: interface defining the node-edge structure of a reasoning process.
**Future**: any "what shape does this process take" abstraction.
**Broad-use contexts**: reasoning topologies (Linear, Tree, DAG, Cyclic), workflow topologies, neural-network topologies, graph-algorithm topologies, organizational structures.
**Every context needs**: node definition, edge definition, shape classification.
**Varies**: node attributes, edge attributes, dynamism, visualization support.
**Extension**: `ReasoningTopology`, `WorkflowTopology`, `NetworkTopology`.
**Note**: §3.18 moves Cyclic/Parallel/Linear to Infra/DS alongside Chain/Tree/DAG/Sequence/Skeleton. Topology itself is already Infra/DS R2T1.

## 250. `Step` · Infrastructure/Data Structures · R0T1

**Intended**: atomic action with preconditions, postconditions, and rollback.
**Future**: any atomic-unit-of-execution with contract.
**Broad-use contexts**: workflow steps, algorithm steps, recipe steps, ritual steps, protocol steps, assembly-line steps, surgical steps.
**Every context needs**: preconditions, action, postconditions, rollback specification.
**Varies**: atomicity strictness, rollback cost, parallel-vs-sequential context, side effects.
**Extension**: `IdempotentStep`, `CompensableStep`, `ParallelStep`, `OrderedStep`.

## 251. `Variable` · Infrastructure/Data Structures · R1T1

**Intended**: a value that can change or adapt — dimension of freedom in problem space.
**Future**: any "configurable quantity" artifact.
**Broad-use contexts**: programming variables, experimental variables, controlled variables, environmental variables, system parameters.
**Every context needs**: mutability, identifiability, value-at-time-T, role in problem space.
**Varies**: type, range, dependency on other variables, observability, controllability.
**Extension**: `BoundedVariable`, `DependentVariable`, `IndependentVariable`, `RandomVariable`.

## 252. `Vector` · Infrastructure/Data Structures · R0T1

**Intended**: multi-dimensional array representing position in semantic space.
**Future**: any embedding-like numerical array.
**Broad-use contexts**: word embeddings, sentence embeddings, image embeddings, recommendation vectors, feature vectors, semantic search queries.
**Every context needs**: dimension count, numerical values, position semantic.
**Varies**: dimension count, value domain (real, complex, binary), sparse vs dense, normalized vs raw.
**Extension**: `SparseVector`, `NormalizedVector`, `EmbeddingVector`, `ComplexVector`.

## 253. `Work` · Infrastructure/Data Structures · R0T1

**Intended**: primitive representation of directed effort — bridge between Intent (thinking) and Reality (act).
**Future**: any resource-expenditure artifact.
**Broad-use contexts**: physical work (thermodynamics analogy), computational work, human labor, cognitive effort, project work units, maintenance work.
**Every context needs**: resource expenditure, Task-to-Solved transformation, acceptance-criteria validation.
**Varies**: resource type, duration, measurability, provenance tracking.
**Extension**: `ComputationalWork`, `CognitiveWork`, `MaintenanceWork`.

## 254. `ExploreExploit` · Mind/Strategy · R2T2 (corrected per Gemini spot-check)

**Intended**: adaptive allocation balancing information-gain vs expected immediate-reward.
**Future**: any exploration-vs-exploitation decision strategy.
**Broad-use contexts**: reinforcement learning (epsilon-greedy, UCB, Thompson sampling), product discovery vs optimization, personal career decisions, research agenda balance, restaurant choice (regular vs new), trading (new position vs add to existing).
**Every context needs**: **a mechanism balancing information-gain against expected immediate-reward** — not any specific algorithm.
**Varies**: the algorithm (epsilon-greedy with random coin-flip, UCB with confidence bounds, Thompson sampling from posterior, softmax), epsilon schedule, budget-awareness, multi-armed bandit vs stateful.
**Extension**: `EpsilonGreedyExploreExploit`, `UCBExploreExploit`, `ThompsonExploreExploit`, `SoftmaxExploreExploit`.
**Correction note**: an earlier sketch required "UCB-like option ranking" in the intersection. Gemini's review correctly flagged that UCB is one specific algorithm; epsilon-greedy (random sampling) and Thompson sampling (posterior draw) don't rank by upper confidence bound. The true intersection floor is the *balancing* discipline, not any algorithm's mechanics.

## 255. `TradeOff` · Mind/Strategy · R1T1

**Intended**: specific negative consequence accepted for a positive one — "the cost of a decision."
**Future**: any "nothing is free" decision-framing artifact.
**Broad-use contexts**: Pareto tradeoffs, speed-vs-safety, cost-vs-quality, short-term-vs-long-term, simplicity-vs-features, privacy-vs-convenience.
**Every context needs**: positive gained, negative accepted, decision acknowledging both.
**Varies**: quantification, temporal horizon, stakeholder asymmetry.
**Extension**: `QuantifiedTradeOff`, `ConstrainedTradeOff`, `AsymmetricTradeOff`.

## 256. `ParetoFront` · Mind/Strategy · R2T1

**Intended**: frontier curve where improving metric A requires degrading metric B.
**Future**: any multi-objective optimization frontier.
**Broad-use contexts**: engineering tradeoffs, portfolio theory, product-feature selection, hyperparameter tuning, economic policy tradeoffs, resource allocation.
**Every context needs**: competing metrics, dominance-check (strictly inferior = discard), frontier identification.
**Varies**: metric count, sampling density, frontier approximation method.
**Extension**: `ApproximateParetoFront`, `DynamicParetoFront`, `WeightedParetoFront`.

## 257. `Roadmap` · Mind/Strategy · R2T1

**Intended**: strategic plan over time — milestones with flexibility between them.
**Future**: any goals-over-time artifact.
**Broad-use contexts**: product roadmaps, research roadmaps, corporate strategy, infrastructure-buildout roadmaps, policy roadmaps, career planning.
**Every context needs**: temporal dimension, milestones (key goals), flexibility between milestones.
**Varies**: time horizon, granularity, update cadence, public-vs-internal.
**Extension**: `ProductRoadmap`, `TechnicalRoadmap`, `PublicRoadmap`, `AdaptiveRoadmap`.

## 258. `EmpiricalTest` · Mind/Strategy · R1T1

**Intended**: identify testable predictions from conclusion, execute experiments to verify.
**Future**: any "prove by testing" discipline.
**Broad-use contexts**: science, engineering verification, UX usability testing, A/B tests, lab experiments, hypothesis testing in data science.
**Every context needs**: testable prediction extraction, experiment/lookup execution, falsification-attempt semantic.
**Varies**: experimental rigor, cost, time-to-result, statistical methodology.
**Extension**: `ControlledEmpiricalTest`, `NaturalEmpiricalTest`, `AutomatedEmpiricalTest`.

## 259. `Experiment` · Mind/Strategy · R2T1

**Intended**: structured causal discovery via variable isolation (Control + Treatment).
**Future**: any causal-discovery mechanism.
**Broad-use contexts**: scientific experiments, A/B tests, clinical trials, social-science studies, product experiments, debugging experiments.
**Every context needs**: variable isolation, Control group, Treatment group, outcome comparison.
**Varies**: design (fully factorial, RCT, natural experiment), sample size, duration, blinding.
**Extension**: `RandomizedExperiment`, `ObservationalExperiment`, `AdaptiveExperiment`.

## 260. `MechanisticDesignProposal` · Infrastructure/Data Structures · R1T2

**Intended**: structured blueprint for systemic solution requiring core-mechanism definition.
**Future**: any "here's how it would work, causally" design artifact.
**Broad-use contexts**: system-architecture proposals, policy proposals with theory-of-change, academic theory proposals, economic intervention proposals, organizational-change proposals.
**Every context needs**: problem definition, system-level solution, core mechanism (leverage point + causal chain), dialectic ("why works" + "why fails"), implementation + vision projections.
**Varies**: domain specificity, dialectic depth, implementation detail, visualization.
**Extension**: `PolicyMechanisticDesignProposal`, `TechnicalMechanisticDesignProposal`, `InstitutionalMechanisticDesignProposal`.

---

## Observations from batch 13

**Data-structure nouns (Constraint, Goal, Problem, Option, Step, Transition, Topology) form the foundation on which workflows and algorithms compose.** Each is well-specified at a minimum-usability level — callers can use them, descendants can specialize.

**`Context` at R0T3** is unusual — R0 (kernel) but T3 (experimental). The broad-use test works — every agent context needs inherited constraints, tools, memory, identity. The T3 tier suggests the specification is still evolving. Probably fine for now.

**New audit items from batch 13.**
47. **`Context` T3 (experimental) at R0 (kernel)** — rings and tiers usually align; R0T3 is unusual. Worth reviewing whether Context should move to T1 (stable) given its foundational role.
48. **`Problem` vs `Task` distinction is clean** (Problem=descriptive gap, Task=directive-to-act). Good foundational differentiation.
49. **`Variable` is very thin** — "a value that can change." Broad-use test passes (every context needs mutability + identifiability), but mechanism could spell out the pre/post-Variable shape a bit more without over-specifying.

Total analyzed: 260 patterns. Remaining: 169. Past 60%.

---

## Batch 14 — Economics interior + Society/Protocols solver family + remaining reasoning

## 261. `AtomicBid` · Society/Economics · R1T2

**Intended**: bundle Bid (intent/cost) + Act (execution) in single indivisible turn — optimistic permission.
**Future**: any "declare and execute in one turn" coordination.
**Broad-use contexts**: high-frequency trading, parallel agent action, optimistic multi-agent execution, speculative writes, lock-free coordination.
**Every context needs**: Bid-as-audit-log, immediate execution, rollback capability via Compensate on post-hoc rejection.
**Varies**: rollback cost, commit-window duration, conflict-detection mechanism.
**Extension**: `HFTAtomicBid`, `SpeculativeAtomicBid`, `ComplexAtomicBid`.

## 262. `Yield` · Society/Economics · R1T2

**Intended**: negotiation backoff on Overlap failure — lower-weighted preference cedes.
**Future**: any weighted-concession-and-debt-ledger mechanism.
**Broad-use contexts**: labor negotiations, coalition politics, family decision-making, resource sharing, dispute resolution in DAOs, diplomatic negotiation.
**Every context needs**: Flex (concession) declaration, Weight (importance) declaration, Yield-Ratio computation, debt-recording in Ledger.
**Varies**: weight elicitation, yield-ratio formula, debt-discharge mechanism.
**Extension**: `StakeWeightedYield`, `TemporalYield`, `ReputationWeightedYield`.

## 263. `ContinuousResourceAuction` · Society/Economics · R1T1

**Intended**: algorithmic continuous pricing for rivalrous resources.
**Future**: any dynamic-pricing market mechanism.
**Broad-use contexts**: compute-resource markets, EIP-1559 gas pricing, Dutch auctions, ad auctions, spectrum auctions, API-credit markets.
**Every context needs**: resource supply, pricing function, continuous-bid acceptance, allocation mechanism.
**Varies**: pricing model (congestion, Dutch, linear decay), granularity, fairness constraints, price-discovery latency.
**Extension**: `CongestionPricingAuction`, `DutchAuction`, `LinearDecayAuction`.

## 264. `CapacityPressure` · Society/Economics · R1T2

**Intended**: forced abstraction via resource starvation — create bottleneck Capacity < Information.
**Future**: any constraint-driven compression mechanism.
**Broad-use contexts**: ML bottleneck regularization (variational autoencoders), educational summarization requirements, emergency resource rationing, legal word-limit drafting, haiku constraints.
**Every context needs**: resource constraint creating bottleneck, pressure to compress/generalize, selective signal retention.
**Varies**: `compression_ratio` (principled [0.0, 1.0] per §3.17), `resource_type` (enum), pressure shape.
**Extension**: `BandwidthCapacityPressure`, `MemoryCapacityPressure`, `TimeCapacityPressure`.

## 265. `AttentionMarkets` · Society/Economics · R1T1

**Intended**: pricing bandwidth to filter spam via second-price auction.
**Future**: any attention-as-priced-resource mechanism.
**Broad-use contexts**: email priority markets, anti-spam pricing, meeting-slot markets, human-attention markets, ad-supported platforms, API rate-limit markets.
**Every context needs**: bid mechanism, priority queue, auction clearance, revenue distribution or burn.
**Varies**: auction type (second-price, first-price, uniform-price), revenue use, minimum bid, spam-filter thresholds.
**Extension**: `EmailAttentionMarkets`, `CalendarAttentionMarkets`, `HumanAttentionMarkets`.

## 266. `Canary` · Society/Protocols · R1T1

**Intended**: expendable agent tests full coordination path before committing real resources.
**Future**: any "test in limited scope first" pattern.
**Broad-use contexts**: canary deployments, tasters (historical kings), pilot programs, beta-tester cohorts, A/B tests with small initial exposure.
**Every context needs**: bounded blast radius, full coordination path test, telemetry emission, proceed/caution/abort recommendation.
**Varies**: resource bound, telemetry detail, lifecycle (destroy/recycle/promote), canary count (single vs multiple).
**Extension**: `DistributedCanary`, `BiomarkerCanary`, `CascadingCanary`.

## 267. `ExecutionManifest` · Society/Protocols · R0T1

**Intended**: composite artifact binding Target Design + Operation Sequence — atomic release candidate.
**Future**: any "here's what and how, ready to execute" artifact.
**Broad-use contexts**: release manifests, Kubernetes deployment manifests, CI/CD pipeline descriptors, build manifests, experiment-protocol manifests.
**Every context needs**: target design (what), operation sequence (how), atomicity semantic (release candidate).
**Varies**: verification embedded vs external, rollback plan attachment, signature requirement.
**Extension**: `SignedExecutionManifest`, `VerifiedExecutionManifest`, `RollbackableExecutionManifest`.

## 268. `SolverManifest` · Society/Protocols · R0T1

**Intended**: typed declaration of solver's identity and capabilities.
**Future**: any capability-declaration artifact for runtime selection.
**Broad-use contexts**: agent capability cards, MCP tool manifests, microservice descriptors, LLM model cards, job applications (capability declaration), restaurant menus (as capability declaration).
**Every context needs**: Name/ID, Competencies, Tool Access, Cost Model, Constraints.
**Varies**: verification of claims, update frequency, discoverability, trust model.
**Extension**: `VerifiedSolverManifest`, `DynamicSolverManifest`, `MLModelCard`.

## 269. `FrameSpec` · Society/Protocols · R0T1

**Intended**: structured problem-space + constraints + success criteria derived from raw request.
**Future**: any "formal specification of what-we're-solving" artifact.
**Broad-use contexts**: research-question definitions, requirements specifications, project charters, medical differential-diagnosis framing, legal case framings.
**Every context needs**: problem space, constraints, success criteria, artifact-for-contract semantic.
**Varies**: formality, machine-readability, revision history, stakeholder sign-off.
**Extension**: `MachineFrameSpec`, `CollaborativeFrameSpec`, `VersionedFrameSpec`.

## 270. `BoundedTask` · Society/Protocols · R2T2

**Intended**: specialized Task enforcing budget + AcceptSpec for economic + quality boundaries.
**Future**: any "Task with must-have budget and acceptance" variant.
**Broad-use contexts**: budgeted solver calls, SLA-bound assignments, grant-funded research tasks, time-boxed projects, deliverable-with-deadline.
**Every context needs**: underlying Task, budget (required here), AcceptSpec, enforcement of both.
**Varies**: budget type (compute, time, money), AcceptSpec strictness, overrun behavior.
**Extension**: `ComputeBoundedTask`, `TimeBoundedTask`, `BillableTask`.

## 271. `Deploy` · Society/Protocols · R1T1

**Intended**: move artifact from development/staging to production via Rollout.
**Future**: any "release to real users" act.
**Broad-use contexts**: software deployments, policy rollouts, product launches, surgical protocol deployments, educational curriculum rollouts.
**Every context needs**: artifact, target environment, Rollout execution.
**Varies**: rollout strategy (blue-green, canary, rolling), user-communication, monitoring integration, abort criteria.
**Extension**: `BlueGreenDeploy`, `CanaryDeploy`, `FeatureFlagDeploy`.

## 272. `EjectionSeat` · Society/Protocols · R0T1

**Intended**: hardware-interrupt style kill switch, operates outside agent comm layer.
**Future**: any "cannot-be-blocked-by-the-system" emergency stop.
**Broad-use contexts**: aircraft ejection seats (origin), nuclear reactor SCRAM, emergency stop buttons (factories), AI safety kill switches, cryptographic emergency revocation.
**Every context needs**: operator key, out-of-band signal channel, cannot-be-blocked guarantee, cascading shutdown.
**Varies**: mode (PAUSE/TERMINATE/EMERGENCY), authentication strength, propagation depth, recovery plan.
**Extension**: `AIEjectionSeat`, `CryptoEjectionSeat`, `IndustrialEjectionSeat`.

## 273. `Handoff` · Society/Protocols · R1T1

**Intended**: transfer control and context between agents with full responsibility/authority transfer.
**Future**: any "you're in charge now" delegation with full authority.
**Broad-use contexts**: shift handoffs (medical, ops), agent swarm role transitions, manager-to-manager transitions, project handoffs, specialized-agent routing.
**Every context needs**: context transfer, authority transfer, responsibility transfer, explicit yield by sender.
**Varies**: context-completeness requirement, acknowledgment protocol, fallback if receiver rejects.
**Extension**: `MedicalHandoff`, `ShiftHandoff`, `SkillSpecificHandoff`.

## 274. `ProblemFramer` · Society/Coordination · R2T2

**Intended**: specialized solver role — interpret request, construct AcceptSpec, anchor RootSolver to UniversalSolverTree.
**Future**: any "define the problem before solving" role.
**Broad-use contexts**: product managers (as problem framers), researchers (writing the research question), policy advisors (problem definition), legal analysts (case framing), UX researchers.
**Every context needs**: request interpretation, AcceptSpec construction (Definition of Done), anchoring to parent structure, reframe request on invalid input.
**Varies**: framing rigor, collaboration level (solo vs with stakeholders), iteration count, rejection policy.
**Extension**: `CollaborativeProblemFramer`, `RigorousProblemFramer`, `QuickProblemFramer`.

## 275. `Synthesis` · Mind/Reasoning · R1T1 (post-§3.18 mechanism rewrite)

**Intended**: the combined unified whole resulting from integration of separate elements.
**Future**: any "the integrated result" artifact.
**Broad-use contexts**: Hegelian synthesis, music composition synthesis, scientific synthesis of findings, team-contribution synthesis, cross-disciplinary synthesis.
**Every context needs**: the integrated whole as an artifact, reference to constituent parts, new-meaning semantic.
**Varies**: synthesis method (dialectic, aggregation, emergence), fidelity to parts, novelty detection.
**Extension**: `DialecticalSynthesis`, `EmergentSynthesis`, `ExplicitSynthesis`.
**Note**: §3.18 and §3.19 confirmed that Synthesis-as-Noun (the combined whole) is the correct mechanism framing; the process-verb `Synthesize` could be minted separately if needed.

## 276. `SocraticLoop` · Mind/Reasoning · R2T2

**Intended**: ambiguity-detection loop querying the user until intent disambiguated.
**Future**: any "ask clarifying questions until clear" interaction.
**Broad-use contexts**: onboarding conversations, requirements elicitation, medical history-taking, detective interrogation, pedagogical dialogue, therapeutic questioning.
**Every context needs**: confidence threshold, user query mechanism, loop termination on disambiguation or max_questions.
**Varies**: question-generation strategy, max-questions bound, tone/pacing, fallback if user unable to answer.
**Extension**: `OnboardingSocraticLoop`, `ClinicalSocraticLoop`, `PedagogicalSocraticLoop`.

## 277. `ExtendedThinking` · Mind/Reasoning · R2T1

**Intended**: inference-time compute scaling — generate extended reasoning traces for accuracy.
**Future**: any "think longer = think better" compute-scaling mechanism.
**Broad-use contexts**: Claude extended thinking, o1/o3 reasoning, hard-problem human deliberation, peer-review depth, research-time allocation.
**Every context needs**: compute budget allocation, extended-reasoning generation, final answer after trace.
**Varies**: budget size (user-controlled vs adaptive), trace visibility, trace-compression post-hoc, adaptive triggering.
**Extension**: `AdaptiveExtendedThinking`, `VisibleExtendedThinking`, `BudgetedExtendedThinking`.

## 278. `ConsensusFinder` · Society/Governance · R1T2

**Intended**: Macro for Discover(Consensus) — find pre-existing agreement instead of forcing a vote.
**Future**: any "look for agreement that already exists" discovery pattern.
**Broad-use contexts**: team-alignment sensing, political-coalition detection, market-consensus detection, organizational-agreement surveying, prior-art search.
**Every context needs**: scan scope, existing-consensus detection, resonate-signal check, optional fallback to formal Quorum.
**Varies**: scan breadth, consensus-threshold definition, cluster-detection granularity.
**Extension**: `MarketConsensusFinder`, `OrganizationalConsensusFinder`, `PoliticalConsensusFinder`.

## 279. `Delegate` · Society/Governance · R1T2

**Intended**: work-distribution protocol with acceptance, tracking, failure handling.
**Future**: any multi-step task-handoff with accountability.
**Broad-use contexts**: manager-to-IC delegation, outsourcing, agent swarms (parent-to-child), multi-step workflows, organizational role assignments.
**Every context needs**: DELEGATE message, ACCEPT/REFUSE response, PROGRESS tracking via Heartbeat, completion or BREAK signaling.
**Varies**: broadcast vs targeted, capability-probe requirement, retry/reassign policy on failure, holographic context inheritance.
**Extension**: `BroadcastDelegate`, `CapabilityVerifiedDelegate`, `CompetitiveDelegate` (auction-based).

## 280. `AnchorDrop` · Society/Governance · R0T1

**Intended**: emergency state checkpointing when network turbulence exceeds threshold.
**Future**: any "stop, re-establish baseline, then resume" consensus-recovery mechanism.
**Broad-use contexts**: market circuit breakers (halt trading), distributed system consensus recovery, organizational crisis freezes, post-disaster restart protocols, blockchain fork recovery.
**Every context needs**: turbulence detection, stop-accepting-transactions, quorum-on-last-valid-state, progress-resumption after anchor.
**Varies**: turbulence metric, threshold, anchor-selection rule, duration bound.
**Extension**: `MarketAnchorDrop`, `NetworkAnchorDrop`, `OrganizationalAnchorDrop`.
**Note**: §3.19 flagged AnchorDrop as having no current callers in the library. Broad-use test produces a rich usage-context list (markets, distributed systems, organizations), but the library's *current* patterns don't invoke it. Possible that when the library grows to cover emergency-coordination protocols, AnchorDrop becomes heavily referenced. Keep, even though it's orphan for now.

---

## Observations from batch 14

**Economic-primitive family (AtomicBid, Yield, ContinuousResourceAuction, AttentionMarkets) validates as a coherent cluster.** Each addresses a specific coordination friction (commit-vs-wait, conflict resolution, resource pricing, spam filtering). Good category structure.

**Manifest family (ExecutionManifest, SolverManifest, FrameSpec, RolloutManifest) is a Noun-cluster describing structured artifacts.** Each has a specific role in the OrchestrationLoop workflow.

**New audit items from batch 14.**
50. **`ProblemFramer` is Society/Coordination** — the sole inhabitant of that category per §3.8 (before rebalance). Is it still the right home after §3.8 moves 12+ patterns into Coordination? Answer: yes, ProblemFramer is naturally a coordination role. Good placement confirmed.
51. **`AnchorDrop` orphan status** — §3.19 noted no callers. Broad-use test suggests rich usage scenarios (circuit breakers, distributed system recovery). May be a forward-looking primitive; keep and wait for descendants.

Total analyzed: 280 patterns. Remaining: 149.

---

## Batch 15 — Infrastructure/Data Structures core + Physics primitives + flow-control

## 281. `Metric` · Infrastructure/Data Structures · R0T1 (post-§3.18 gloss rewrite)

**Intended**: definable, quantifiable measure of a property providing signal for optimization/monitoring.
**Future**: any measurement artifact.
**Broad-use contexts**: system metrics (latency, throughput), business KPIs, scientific measurements, health metrics, financial metrics, ML training metrics, game scores.
**Every context needs**: measurement definition, quantifiability, target property.
**Varies**: aggregation granularity, sampling frequency, cardinality, derived vs raw.
**Extension**: `LatencyMetric`, `BusinessKPI`, `HealthMetric`, `StreamingMetric`.
**Note**: §3.18 flagged Metric as gloss-restates-mechanism. Broad-use sketch is a concrete rewrite target.

## 282. `Protocol` · Infrastructure/Data Structures · R0T1

**Intended**: defined set of rules and formats for communication between agents.
**Future**: any "how we talk to each other" specification.
**Broad-use contexts**: HTTP, gRPC, SMTP, diplomatic protocols, scientific-paper protocols, ceremonial protocols, medical protocols, agent-communication protocols (FIPA, ACL).
**Every context needs**: rule set, format specification, inter-agent applicability.
**Varies**: formality, versioning, backward compatibility, machine-readable vs human-readable.
**Extension**: `NetworkProtocol`, `DiplomaticProtocol`, `MedicalProtocol`, `AgentCommunicationProtocol`.

## 283. `Outcome` · Infrastructure/Data Structures · R1T1 (post-§3.18 rewrite)

**Intended**: actual result that occurs in reality — may differ from Plan due to external factors.
**Future**: any "what actually happened" artifact.
**Broad-use contexts**: experiment outcomes, medical outcomes, project outcomes, investment outcomes, game outcomes, policy outcomes.
**Every context needs**: actual-reality captured, distinction from Plan/Intent, attribution of deviation causes.
**Varies**: granularity of capture, retrospective depth, stakeholder perspective.
**Extension**: `MedicalOutcome`, `LegalOutcome`, `ExperimentalOutcome`, `StatisticalOutcome`.

## 284. `Probability` · Infrastructure/Data Structures · R0T1

**Intended**: likelihood measure on [0,1] — degree of belief or frequency of event.
**Future**: any probability-valued artifact.
**Broad-use contexts**: risk assessment, Bayesian reasoning, frequentist statistics, ML confidence scores, betting-market prices, weather forecasts, medical probabilities.
**Every context needs**: `value: number` in [0,1] (principled range), belief-or-frequency interpretation.
**Varies**: subjective vs objective, sharp vs fuzzy, distribution-valued vs point.
**Extension**: `BayesianProbability`, `FrequentistProbability`, `FuzzyProbability`, `DistributionProbability`.

## 285. `Criteria` · Infrastructure/Data Structures · R1T1

**Intended**: specific standards used to judge success of an artifact.
**Future**: any judgment-standard artifact.
**Broad-use contexts**: acceptance criteria, rubric criteria, regulatory criteria, quality criteria, fitness criteria, performance criteria.
**Every context needs**: specific standards, target being judged, pass/fail or quantification rule.
**Varies**: criteria count, weighting, compensation rules (can one exceed offset another's failure), source (stakeholder vs derived).
**Extension**: `WeightedCriteria`, `NonCompensatoryCriteria`, `AcceptCriteria`, `RubricCriteria`.

## 286. `RuleSet` · Infrastructure/Data Structures · R0T1

**Intended**: immutable collection of Constraints and invariants defining validity boundary.
**Future**: any rule-bundle artifact.
**Broad-use contexts**: legal statutes, game rules, firewall rules, validation rulesets, grammar specifications, policy rulesets.
**Every context needs**: structured collection, immutability, validity-boundary definition.
**Varies**: rule count, rule-interaction semantics, conflict resolution, version binding.
**Extension**: `LegalRuleSet`, `SecurityRuleSet`, `GameRuleSet`.

## 287. `Mode` · Infrastructure/Data Structures · R0T1

**Intended**: discrete configuration of agency — stable set of constraints and priors.
**Future**: any "stance" or "configuration of how-I-act" artifact.
**Broad-use contexts**: Exploration vs Exploitation mode, work mode vs rest mode, emergency mode, cognitive modes (System 1 vs 2), personality modes in LLMs.
**Every context needs**: stable-configuration semantic, distinction from frequently-changing State, behavior modification.
**Varies**: mode count, transition semantics (triggered vs manual), persistence across sessions.
**Extension**: `CognitiveMode`, `OperationalMode`, `EmergencyMode`.

## 288. `Snapshot` · Infrastructure/Data Structures · R0T1

**Intended**: static immutable record of state at a specific time.
**Future**: any "state-at-T-frozen" artifact.
**Broad-use contexts**: database snapshots, filesystem snapshots, VM snapshots, Git commits (as snapshots), legal-record snapshots, scientific-measurement snapshots.
**Every context needs**: immutability, timestamp binding, state capture.
**Varies**: completeness (full vs delta), storage, restore semantics, encryption.
**Extension**: `FullSnapshot`, `IncrementalSnapshot`, `EncryptedSnapshot`, `AuditSnapshot`.

## 289. `Audit` · Infrastructure/Data Structures · R0T1

**Intended**: process of verifying conformance of system state/behavior to specifications.
**Future**: any compliance-verification act.
**Broad-use contexts**: financial audits, security audits, compliance audits, code audits, scientific-reproduction audits, process audits.
**Every context needs**: target, specifications to check against, verification process, conformance judgment.
**Varies**: scope (full vs spot), independence requirement, frequency, retention.
**Extension**: `FinancialAudit`, `SecurityAudit`, `CompliantAudit`, `IndependentAudit`.
**Note**: `Audit` at R0T1 is a Noun (the audit artifact/process). `SpotAudit` (covered in batch 5) is the Verb+process. Borderline — `Audit` as Noun might have Verb-mechanism drift. Worth checking.

## 290. `Skeleton` · Infrastructure/Data Structures · R2T1

**Intended**: parallel outline-first topology — skeletal outline, then parallel point expansion.
**Future**: any outline-with-parallel-fill structure.
**Broad-use contexts**: SkeletonOfThought reasoning, document outlining, research paper structures, code scaffolding, project structure templates.
**Every context needs**: outline structure, parallel expansion capability, latency-optimization semantic.
**Varies**: outline depth, parallelism width, expansion-quality thresholds.
**Extension**: `DocumentSkeleton`, `CodeSkeleton`, `OutlineSkeleton`.

## 291. `Shard` · Infrastructure/Data Structures · R0T0

**Intended**: deterministic partitioning of state/resource/vector into disjoint subsets by key.
**Future**: any "split volume/load" primitive.
**Broad-use contexts**: database sharding, distributed computation, memory partitioning, workforce sharding, IP-range sharding, geographic sharding.
**Every context needs**: partitioning key, disjoint output subsets, determinism.
**Varies**: key function, rebalancing policy, replication, fault tolerance.
**Extension**: `ConsistentHashShard`, `RangeShard`, `GeographicShard`, `WorkloadShard`.

## 292. `Compress` · Physics/Primitives · R0T1

**Intended**: lossy or lossless reduction of information size preserving essential meaning.
**Future**: any information-size-reduction primitive.
**Broad-use contexts**: data compression (gzip, zstd), cognitive compression (ChunkMerge), audio/video compression, prompt compression, abstraction in reasoning.
**Every context needs**: input size, reduction mechanism, essential-meaning preservation.
**Varies**: lossy vs lossless, compression ratio, reversibility, domain specificity.
**Extension**: `LosslessCompress`, `LossyCompress`, `SemanticCompress`, `StreamingCompress`.

## 293. `Entropy` · Physics/Primitives · R0T1

**Intended**: quantitative measure of disorder, uncertainty, or information content.
**Future**: any "amount of disorder/info" measure.
**Broad-use contexts**: thermodynamics, Shannon entropy in info theory, ML uncertainty, chaos measures, randomness assessment, social entropy.
**Every context needs**: system/message being measured, quantifiability.
**Varies**: measurement method (Shannon, Gibbs, Boltzmann, etc.), base (log 2, log e), application domain.
**Extension**: `ShannonEntropy`, `ThermodynamicEntropy`, `CrossEntropy`, `RelativeEntropy`.

## 294. `Mutex` · Physics/Primitives · R0T2 (post-§3.3 derived_from Lock)

**Intended**: exclusive-access token with lifecycle (ACQUIRE → GRANT/QUEUE → HOLD → RELEASE/YIELD).
**Future**: any single-holder-at-a-time primitive with explicit token.
**Broad-use contexts**: OS mutexes, distributed locks with tokens, hardware locks, leadership tokens in distributed systems, single-writer-principle enforcement.
**Every context needs**: lifecycle, token representation, priority queue for contention, fencing tokens for revocation.
**Varies**: token material, queue discipline, fencing implementation, reentrancy support.
**Extension**: `FencingMutex`, `ReentrantMutex`, `DistributedMutex`.
**Note**: §3.3 adds `derived_from Lock` to Mutex. Broad-use test confirms Mutex as a specialized Lock (adds token+fencing semantics). Correct relationship.

## 295. `Throttle` · Physics/Primitives · R0T1

**Intended**: rate limiting — max N tasks per time window W.
**Future**: any rate-limiting primitive.
**Broad-use contexts**: API rate limits, UI button-debounce, traffic shaping, network QoS, process scheduling, rate-limited email sends.
**Every context needs**: N (count), W (window), excess-handling (reject/queue/delay).
**Varies**: sliding vs fixed window, per-scope limits (user/global/action-type), Backoff integration.
**Extension**: `SlidingThrottle`, `PerUserThrottle`, `AdaptiveThrottle`.

## 296. `Branch` · Physics/Time · R0T1

**Intended**: conditional fork — if C then A else B (mutual exclusion).
**Future**: any binary conditional flow primitive.
**Broad-use contexts**: if-else programming, decision gates, binary state transitions, A/B experiments, diagnostic forks, binary game moves.
**Every context needs**: condition, A-branch, B-branch, mutual exclusion.
**Varies**: condition evaluation, evaluation cost, short-circuit semantics.
**Extension**: `TernaryBranch` (borderline — might belong with Route), `GuardedBranch`, `LazyBranch`.

## 297. `StateLock` · Physics/Time · R0T1

**Intended**: atomic coordination via temporary state fusion — both actors' signatures required.
**Future**: any "two-party write agreement" coordination primitive.
**Broad-use contexts**: two-phase commit, escrow key pairs, multi-signature wallets, joint-authorship protocols, collaborative editing locks, diplomatic joint statements.
**Every context needs**: state subset, two (or more) actors, temporary fusion, both-sign-to-write, Backoff/Cooldown on contention.
**Varies**: multi-party extension, timeout policy, revocation.
**Extension**: `TwoPhaseStateLock`, `MultisigStateLock`, `DiplomaticStateLock`.

## 298. `ToolInvoke` · Infrastructure/Primitives · R0T2 (post-§3.11 relocation)

**Intended**: execute external tool and observe result — the atomic unit of agent-environment interaction.
**Future**: any structured "call a tool, get a result" operation.
**Broad-use contexts**: LLM tool use, plugin invocation, API calls, OS syscalls, library function calls, external-service integration.
**Every context needs**: structured tool call (function name + arguments), InputGuard validation, external runtime delegation, observation integration into context.
**Varies**: sandboxing, timeout, retry semantics, side-effect classification (reversible/irreversible).
**Extension**: `SandboxedToolInvoke`, `ReversibleToolInvoke`, `StreamingToolInvoke`.
**Note**: §3.11 moves ToolInvoke from Data Structures to Primitives (it's a Verb). Broad-use confirms.

## 299. `BreadthGovernor` · Mind/Inference · R0T2

**Intended**: Parsimony-bounded expansion — limit max parallel branches (fan-out) at a node.
**Future**: any "how wide can we spread this search" governor.
**Broad-use contexts**: tree search pruning, beam search width, brainstorming fan-out control, research question diversification, parallel-experiment count bounding.
**Every context needs**: max breadth bound, distinctness + expected-value prioritization, truncation (top-K) or clustering (merge similar).
**Varies**: K value (PositiveInteger per §3.17), distinctness metric, value-estimation method.
**Extension**: `BeamBreadthGovernor`, `ClusterBreadthGovernor`, `AdaptiveBreadthGovernor`.

## 300. `HindsightBlock` · Mind/Inference · R0T1

**Intended**: prevent results-oriented thinking — judge past decisions by ex-ante info, not outcome.
**Future**: any "separate decision quality from outcome" discipline.
**Broad-use contexts**: poker theory (Annie Duke), investment analysis, military decision reviews, sports analytics (process vs results), judicial review, accountability-despite-bad-luck.
**Every context needs**: decision reconstruction at time T, judgment of quality given available info at T, separation from actual outcome.
**Varies**: information-reconstruction rigor, comparison baseline, counterfactual weighting.
**Extension**: `PokerHindsightBlock`, `InvestmentHindsightBlock`, `ExecutiveHindsightBlock`.

---

## Observations from batch 15

**300-pattern milestone!** Over 70% of the library has been analyzed through the broad-use lens.

**Physics primitives (Compress, Entropy, Throttle, Mutex) and Physics/Time (Branch, StateLock) are cleanly minimal.** Short mechanisms, clear foundations, rich descendant space. These anchor the substrate layer.

**Infrastructure/Data Structures Noun family is large but coherent.** Metric, Protocol, Outcome, Probability, Criteria, RuleSet, Mode, Snapshot, Audit, Skeleton, Shard — each has a distinct definitional role.

**New audit items from batch 15.**
52. **`Audit` Noun at Infra/DS R0T1** — the mechanism says "the process of verifying" which is Verb-like. Same pattern as Decision/Synthesis/Critique. Add to Noun/Verb review list.
53. **`Probability.value` range [0,1]** — `Probability` itself has this in mechanism text ("measure of likelihood on [0,1]"). Good. But declared in `data_schema`? Worth spot-checking.
54. **`Outcome`'s §3.18 rewrite target**: the broad-use sketch gives a concrete distinguishing-from-Plan framing.

Total analyzed: 300 patterns. Remaining: 129.

---

## Batch 16 — remaining Infrastructure Nouns + Memory + utility primitives

## 301. `Anomaly` · Infrastructure/Data Structures · R1T1 (post-§3.18 gloss rewrite)

**Intended**: datum that deviates from expected standard — triggers investigation.
**Future**: any "something-is-off" signal artifact.
**Broad-use contexts**: monitoring anomalies, medical anomalies, financial anomalies, security anomalies, scientific anomalies, behavior anomalies.
**Every context needs**: observed datum, expected standard, deviation semantic.
**Varies**: deviation threshold, severity classification, investigation-trigger protocol.
**Extension**: `StatisticalAnomaly`, `BehavioralAnomaly`, `SecurityAnomaly`.

## 302. `ConceptAnchor` · Infrastructure/Data Structures · R2T1

**Intended**: immutable content-addressed concept reference — `[hash:Apple]` not `"an apple"`.
**Future**: any "pin meaning via hash" reference.
**Broad-use contexts**: sema handles themselves, Git commit hashes as semantic anchors, content-addressed pattern libraries, IPFS-style references, blockchain state anchors.
**Every context needs**: immutability, content-addressing (hash), global reference, external drop event.
**Varies**: hash algorithm, resolution protocol, caching, update-via-new-hash semantics.
**Extension**: `MerkleConceptAnchor`, `IPFSConceptAnchor`, `SemaConceptAnchor`.

## 303. `Hierarchy` · Infrastructure/Data Structures · R1T1 (post-§3.18 gloss rewrite)

**Intended**: vertical ranking of categories/objects — defines Upper/Lower, inheritance, authority.
**Future**: any ordered-rank artifact.
**Broad-use contexts**: org charts, taxonomy hierarchies, maslow's hierarchy of needs, priority hierarchies, biological taxonomies, file-system hierarchies, type hierarchies.
**Every context needs**: vertical ordering, Upper/Lower relations, inheritance rule, authority rule.
**Varies**: single-inheritance vs multiple, dynamism, enforcement of strict-vs-loose hierarchy.
**Extension**: `CorporateHierarchy`, `TypeHierarchy`, `BiologicalHierarchy`.

## 304. `Queue` · Infrastructure/Data Structures · R0T1 (post-§3.18 gloss rewrite)

**Intended**: ordered task/message buffer with FIFO or Priority ordering.
**Future**: any "wait in line" data structure.
**Broad-use contexts**: job queues, message queues, call queues, emergency-room triage queues, print queues, network queues.
**Every context needs**: ordering discipline (FIFO/Priority), enqueue, dequeue, explicit order semantic distinct from Stream.
**Varies**: priority function, boundedness, persistence, concurrent access semantics.
**Extension**: `PriorityQueue`, `BoundedQueue`, `PersistentQueue`, `LockFreeQueue`.

## 305. `Prompt` · Infrastructure/Data Structures · R0T1 (post-§3.18 gloss rewrite)

**Intended**: input text/instruction to a generative model.
**Future**: any "instruction to a generator" artifact.
**Broad-use contexts**: LLM prompts, image-generation prompts, music-generation prompts, instruction-following dataset entries, meta-prompts.
**Every context needs**: input content, generator target.
**Varies**: structure (plain vs structured), length, role-tagging (system/user/assistant), tool-declaration attachments.
**Extension**: `SystemPrompt`, `StructuredPrompt`, `MultiTurnPrompt`, `ToolEnabledPrompt`.

## 306. `Summary` · Infrastructure/Data Structures · R1T1 (post-§3.19 tightening)

**Intended**: compressed representation retaining salient info, discarding redundancy.
**Future**: any lossy-compressed representation artifact.
**Broad-use contexts**: document summaries, meeting minutes, executive briefs, research abstracts, news summaries.
**Every context needs**: `source_ref: sema_id` (definitional — a Summary without source is meaningless), compression of content, salience-preservation.
**Varies**: compression ratio (optional per §3.19), preservation list (optional), domain specificity.
**Extension**: `ExecutiveSummary`, `ResearchAbstract`, `ChatSummary`.

## 307. `Risk` · Infrastructure/Data Structures · R0T1 (post-§3.6 wiring)

**Intended**: quantified potential for negative outcome — probability + severity + mitigation + trigger.
**Future**: any "here's what could go wrong" artifact.
**Broad-use contexts**: risk registers, insurance actuarial data, project risk logs, security risk assessments, financial risk models, clinical risk profiles.
**Every context needs**: probability, severity (impact metric), mitigation (reducing actions), trigger (materialization conditions).
**Varies**: quantification method, dynamism, aggregation at-container level.
**Extension**: `FinancialRisk`, `OperationalRisk`, `SecurityRisk`, `ClinicalRisk`.

## 308. `Chain` · Infrastructure/Data Structures · R2T1 (post-§3.18 Linear retirement absorb)

**Intended**: concrete linked-list data structure with sequential linked nodes.
**Future**: any linked-sequential data structure.
**Broad-use contexts**: linked lists, blockchain chains, chain-of-custody records, Markov chains (loosely), linked data structures in programs.
**Every context needs**: node-link structure, sequential traversal semantic, concrete-storage-container semantic.
**Varies**: doubly vs singly linked, circular vs linear, memory layout, concurrency.
**Extension**: `DoublyLinkedChain`, `CircularChain`, `PersistentChain`.
**Note**: §3.18 merges Linear → Chain (spatial topology unified).

## 309. `Category` · Infrastructure/Data Structures · R1T1

**Intended**: specific grouping/bin for objects — equivalence class.
**Future**: any "group things together" artifact.
**Broad-use contexts**: taxonomic categories, type categories, product categories, email folder categories, research field categories.
**Every context needs**: grouping criterion, equivalence semantic for certain ops.
**Varies**: mutual exclusion (category A excludes B), hierarchy integration, fuzzy membership.
**Extension**: `TaxonomicCategory`, `FuzzyCategory`, `HierarchicalCategory`.

## 310. `Sequence` · Infrastructure/Data Structures · R0T1 (post-§3.18 temporal-distinct)

**Intended**: ordered execution — A then B, output of A available to B (temporal ordering).
**Future**: any temporal-sequence artifact.
**Broad-use contexts**: workflow sequences, execution pipelines, causal chains, musical sequences, protocol sequences.
**Every context needs**: ordered execution, output-flow-forward semantic, temporal (not spatial) ordering.
**Varies**: strict vs relaxed ordering, parallelism inside a Sequence step, pause/resume semantics.
**Extension**: `StrictSequence`, `RelaxedSequence`, `PauseResumeSequence`.

## 311. `Assessment` · Infrastructure/Data Structures · R1T1

**Intended**: structured qualitative evaluation — strengths, weaknesses, recommendations.
**Future**: any structured-qualitative-feedback artifact.
**Broad-use contexts**: performance reviews, academic assessments, code review artifacts, medical assessments, risk assessments, peer reviews.
**Every context needs**: structured evaluation, strengths list, weaknesses list, recommendations.
**Varies**: rubric alignment, confidentiality, longitudinal (over time) vs point-in-time.
**Extension**: `PerformanceAssessment`, `AcademicAssessment`, `MedicalAssessment`.

## 312. `MECE` · Infrastructure/Data Structures · R2T2

**Intended**: Mutually Exclusive, Collectively Exhaustive partitioning.
**Future**: any "no overlap, no gaps" partitioning discipline.
**Broad-use contexts**: consulting frameworks (McKinsey's Pyramid), probability-space partitioning, category-schema design, market-segment analysis, legal case-law partitioning.
**Every context needs**: problem space, partition into non-overlapping categories, no-gap test.
**Varies**: partition granularity, test rigor, dynamism (static vs updating partition).
**Extension**: `ProbabilityMECE`, `MarketMECE`, `TaxonomyMECE`.

## 313. `Overlap` · Infrastructure/Data Structures · R1T1 (post-§3.18 gloss rewrite)

**Intended**: accept-set intersection-finding negotiation — commit-reveal protocol.
**Future**: any "find what we both agree on" negotiation primitive.
**Broad-use contexts**: union negotiations, political compromise finding, requirements-intersection elicitation, multi-stakeholder design, M&A deal points, diplomatic common ground.
**Every context needs**: each-party accept-set, hash-commit-before-reveal, intersection compute, expand-or-succeed loop.
**Varies**: expansion-step size, expansion-cap, fallback on no-overlap.
**Extension**: `LaborOverlap`, `DiplomaticOverlap`, `RequirementsOverlap`.

## 314. `CognitiveBias` · Infrastructure/Data Structures · R1T1

**Intended**: structural error definition — systematic distortion in information processing.
**Future**: any named-bias artifact.
**Broad-use contexts**: Wikipedia's list of cognitive biases, heuristics-and-biases literature, ML dataset biases, organizational biases, user-research biases.
**Every context needs**: specific distortion definition, trigger conditions, mitigation strategies.
**Varies**: domain (human cognitive, statistical, systemic), measurability, avoidance protocols.
**Extension**: `HumanCognitiveBias`, `StatisticalBias`, `DatasetBias`.

## 315. `Break` · Infrastructure/Data Structures · R0T1 (post-§3.18 gloss rewrite)

**Intended**: protocol for announcing coordination failure — {severity, reason, recoverable}.
**Future**: any "coordination failed, we need to stop/pause" signal.
**Broad-use contexts**: saga break events, distributed-transaction aborts, emergency stops in multi-party coordination, cascading failure propagation, ejection events.
**Every context needs**: severity, reason, recoverability flag, ACK requirement, escalation-on-no-ACK.
**Varies**: broadcast scope, severity levels, default termination vs pause, integration with CircuitBreaker/EjectionSeat.
**Extension**: `PartialBreak`, `TotalBreak`, `EscalatingBreak`.

## 316. `Card` · Infrastructure/Data Structures · R0T2 (post-§3.18 gloss rewrite)

**Intended**: structured capability advertisement enabling agent discovery before contact.
**Future**: any capability-description artifact.
**Broad-use contexts**: agent cards (A2A protocol), LinkedIn profiles, business cards, DMP agent-capability manifests, API capability documents, MCP server metadata.
**Every context needs**: agent_id, endpoint, protocols, capabilities, constraints, metadata.
**Varies**: publication mechanism (registry, broadcast, DHT, well-known endpoint), TTL, verification/signing.
**Extension**: `SignedCard`, `ExpiringCard`, `FederatedCard`.

## 317. `Care` · Infrastructure/Primitives · R0T1

**Intended**: non-transactional maintenance energy — Work applied to reduce target's Entropy without Value extraction.
**Future**: any "upkeep without direct payoff" primitive.
**Broad-use contexts**: stewardship (Gardener), relationship maintenance, codebase refactoring (no feature delivery), janitorial work, system hygiene, ecosystem tending.
**Every context needs**: target, Work application, Entropy reduction, absence of Value extraction.
**Varies**: intensity, frequency, measurement (or lack thereof), reciprocity structures.
**Extension**: `RelationshipCare`, `InstitutionalCare`, `EcosystemCare`.

## 318. `TaskLifecycle` · Infrastructure/Primitives · R1T1

**Intended**: formal state machine governing Task progression — PENDING → ASSIGNED → RUNNING → COMPLETED/FAILED.
**Future**: any "life of a task" state machine.
**Broad-use contexts**: workflow engines, ticket systems, issue trackers, solver-node lifecycle management, job schedulers, CI/CD pipelines.
**Every context needs**: five states (or a superset), typed-event transitions, invalid-transition rejection, heartbeat for RUNNING state.
**Varies**: state count (could have more — paused, cancelled, blocked), retry semantics, timeout handling, transition authorization.
**Extension**: `PausableTaskLifecycle`, `BlockableTaskLifecycle`, `AuthorizedTaskLifecycle`.

## 319. `ContextCompress` · Mind/Memory · R0T1

**Intended**: semantic compression for long-running contexts preserving constraints and unresolved goals.
**Future**: any long-context memory-management operation.
**Broad-use contexts**: LLM context-window management, human meeting-notes distillation, knowledge-base summarization, conversational memory compression.
**Every context needs**: token/memory footprint reduction, active-constraints preservation, unresolved-goals preservation.
**Varies**: compression ratio, what's preserved beyond constraints+goals (preferences, open threads), recall-support.
**Extension**: `PromptContextCompress`, `DialogueContextCompress`, `ResearchContextCompress`.

## 320. `SelfReminder` · Mind/Memory · R0T2

**Intended**: inject persistent Trace of core identity into prompt context before each response.
**Future**: any "stay grounded in your principles" periodic reminder.
**Broad-use contexts**: LLM jailbreak mitigation, organizational values reminders, morning affirmations, meeting charters repeated, recurring safety briefings.
**Every context needs**: core-identity text, persistent injection into context, pre-response timing.
**Varies**: content verbosity, injection frequency, update policy.
**Extension**: `SafetySelfReminder`, `IdentitySelfReminder`, `ValuesSelfReminder`.

---

## Observations from batch 16

**Gloss rewrites consistently pay off.** Anomaly, Hierarchy, Queue, Prompt, Break, Card, Overlap — each had gloss-restates-mechanism or marketing-speak glosses (flagged in §3.18). The broad-use sketches give concrete rewrite targets that would make these glosses serve their embedding-anchor purpose.

**New audit items from batch 16.**
55. **`Anomaly` vs `Incongruity`** — both describe prediction-reality mismatch. Anomaly is Infra/DS (Noun, data-level), Incongruity is Physics/Primitives (more foundational). Broad-use: Anomaly is a *piece of data* that deviates; Incongruity is the *signal* of mismatch. Subtle but real distinction. Could add cross-reference (`Anomaly references Incongruity`).
56. **`TaskLifecycle` at R1T1** — well-specified. Good example of a compound primitive that has enough structure to be useful without over-constraining.
57. **`Card`'s mechanism mentions {{agent_id}} but agent_id isn't a pattern** — probably just plain-language variable, not template syntax.

Total analyzed: 320 patterns. Remaining: 109.

---

## Batch 17 — Mind/Strategy remainder + Society/Protocols interior

## 321. `Uncertain` · Mind/Reasoning · R2T2 (post-§3.2 relocation from Physics)

**Intended**: epistemic status flag — explicitly marks Unknown (void of evidence).
**Future**: any "I don't know" tag.
**Broad-use contexts**: Bayesian network nodes, LLM uncertainty flagging, scientific hypothesis staging, intelligence reports (confidence levels), medical "uncertain diagnosis" markers.
**Every context needs**: void-of-evidence assertion, distinction from Speculation (posits direction) and false certainty (absence = evidence of absence fallacy).
**Varies**: granularity (per-claim vs per-variable), escalation to information-gathering, persistence.
**Extension**: `PartiallyUncertain`, `FundamentalUncertain`, `ResolvableUncertain`.

## 322. `StateAudit` · Physics/Time · R0T1

**Intended**: audit state immediately after write to verify transition occurred as expected.
**Future**: any "trust but verify after write" pattern.
**Broad-use contexts**: write-verify in distributed systems, read-after-write consistency checks, SQL audit-trail verification, filesystem post-write checks, transaction-success verification.
**Every context needs**: write operation, immediate audit, expected-vs-actual check, silent-failure detection.
**Varies**: audit latency (sync vs async), verification depth, retry semantics on mismatch.
**Extension**: `SyncStateAudit`, `AsyncStateAudit`, `DeepStateAudit`.

## 323. `Bubble` · Mind/Strategy · R1T1 (post-§3.4 gloss rewrite)

**Intended**: isolated sandbox with copy-on-write state and soft resource reservations.
**Future**: any "try coordination without real consequences" environment.
**Broad-use contexts**: distributed transaction sandboxes, rehearsal spaces, multi-party negotiation sandboxes, dry-run environments, game scenarios.
**Every context needs**: isolation, copy-on-write state, soft reservations, 2-phase commit for merge.
**Varies**: TTL, isolation level, nesting (child bubbles), participant count.
**Extension**: `NestedBubble`, `SnapshotBubble`, `MultiPartyBubble`.

## 324. `BeamSearch` · Mind/Strategy · R1T1

**Intended**: width-limited heuristic search — expand top-k most promising nodes.
**Future**: any fixed-width best-first search.
**Broad-use contexts**: ML beam search (NLP decoding, speech recognition), game-tree search with width cap, research-direction beam pruning, hypothesis beam testing.
**Every context needs**: queue of size k, successor generation, ranking, top-k selection per step.
**Varies**: beam width k (PositiveInteger per §3.17), ranking heuristic, pruning criteria, diversity constraint.
**Extension**: `DiverseBeamSearch`, `StochasticBeamSearch`, `NestedBeamSearch`.

## 325. `Defer` · Mind/Strategy · R2T1

**Intended**: strategic postponement — decide later if waiting reveals relevant information.
**Future**: any "wait, don't commit yet" strategy.
**Broad-use contexts**: procrastination-as-strategy, option-value preservation, decision-postponement under uncertainty, wait-and-see strategies, lazy evaluation.
**Every context needs**: VOI check ("what would I learn by waiting?"), deadline to prevent analysis paralysis, re-insertion into queue when condition met.
**Varies**: deadline policy, triggering condition, cost of holding the decision open.
**Extension**: `OptionValueDefer`, `DeadlineDefer`, `ConditionalDefer`.

## 326. `Prioritize` · Mind/Strategy · R2T1

**Intended**: Impact-Effort ranking — sort options by impact/effort ratio, work top-down.
**Future**: any resource-constrained task ordering.
**Broad-use contexts**: product roadmap ordering, ticket triage, investment decisions, creative-project sequencing, home repairs prioritization.
**Every context needs**: option set, impact score, effort score, ratio computation, sort, periodic rescoring.
**Varies**: score granularity, re-score frequency, Pareto-80/20 awareness, dependency handling.
**Extension**: `ImpactEffortPrioritize`, `RiceScorePrioritize`, `DependencyPrioritize`.

## 327. `Tension` · Mind/Strategy · R1T1

**Intended**: reified conflict state between valid but mutually exclusive signals/constraints/values.
**Future**: any held-contradiction artifact.
**Broad-use contexts**: design tensions, ethical dilemmas, resource-allocation tensions, political tensions, creative tensions.
**Every context needs**: detected conflict, reification as data structure, input to resolution protocols (Dialectic, Yield).
**Varies**: conflict detection method, temporary-hold vs permanent, resolution pathway selection.
**Extension**: `EthicalTension`, `DesignTension`, `ResourceTension`.

## 328. `UncertaintyMap` · Mind/Strategy · R2T2

**Intended**: systematic categorization of ignorance — Known-Known, Known-Unknown, Unknown-Unknown matrix.
**Future**: any ignorance-auditing framework.
**Broad-use contexts**: Rumsfeld-ian strategic analysis, scientific research planning, risk registers, cybersecurity threat modeling, due-diligence frameworks.
**Every context needs**: factor enumeration, 3-category (or 4) classification, resolution-cost estimation for Known-Unknowns, active-probing for Unknown-Unknowns.
**Varies**: factor scope, cost-estimation method, probing frequency, update cadence.
**Extension**: `StrategicUncertaintyMap`, `ThreatUncertaintyMap`, `ScientificUncertaintyMap`.

## 329. `Novelty` · Mind/Strategy · R2T1

**Intended**: Judge-as-structural-distinctness — 3-class classification (Derivative / Marginal / Distinct).
**Future**: any "is this actually new?" evaluator.
**Broad-use contexts**: PURECheck's N dimension, academic originality checks, patent novelty screening, pattern-library novelty, product-originality evaluation.
**Every context needs**: candidate, incumbent knowledge base, structural-distinctness evaluation, 3-class judgment.
**Varies**: distinctness metric, knowledge-base coverage, domain specificity.
**Extension**: `StructuralNovelty`, `PatentNovelty`, `PatternNovelty`.

## 330. `RepresentationSwap` · Mind/Strategy · R2T2

**Intended**: verification protocol via transcoding to strictly orthogonal modality.
**Future**: any "change representation to reveal errors" verification.
**Broad-use contexts**: code-to-plain-English explanation for bug-finding, table-to-narrative verification, diagram-to-code round-trips, educational explanations (if you can't explain it simply...).
**Every context needs**: original representation, orthogonal target modality, lossless transcoding requirement, gap/inconsistency detection in new format.
**Varies**: modality pair, transcoding rigor, roundtrip expectation (reverse-transcode and compare).
**Extension**: `CodeToEnglishSwap`, `TableToNarrativeSwap`, `DiagramToCodeSwap`.

## 331. `AdversarialSteel` · Mind/Strategy · R1T2

**Intended**: dual-advocate verdict generation — green + red advocates, judge decides.
**Future**: any "formal adversarial process" verification.
**Broad-use contexts**: legal adversarial system, academic peer review (reviewer 2 as red advocate), AI debate for alignment, corporate decision-review boards.
**Every context needs**: green advocate role, red advocate role, third-party judge, steelman_check for argument quality.
**Varies**: advocate impartiality, judge independence, issue-limiting to specific questions, verdict-binding-ness.
**Extension**: `LegalAdversarialSteel`, `AcademicAdversarialSteel`, `AIDebateAdversarialSteel`.

## 332. `EmpathySim` · Society/Economics · R2T2

**Intended**: Theory-of-Mind simulation — virtual context with target's priors, inference on that context.
**Future**: any "model the other agent's perspective" operation.
**Broad-use contexts**: negotiation strategy, user-research personas, ethical-impact analysis, fiction-writing character modeling, therapy (taking another's perspective), chess-opponent modeling.
**Every context needs**: target agent's priors/goals/constraints, virtual-context instantiation, inference-on-behalf simulation.
**Varies**: prior fidelity, simulation-run count, perspective-depth, multiple-target support.
**Extension**: `UserResearchEmpathySim`, `AdversarialEmpathySim`, `CollaborativeEmpathySim`.

## 333. `Oracle` · Society/Protocols · R1T1

**Intended**: trusted entity injecting off-chain truth via cryptographic signing.
**Future**: any "bridge external reality into the system" service.
**Broad-use contexts**: blockchain oracles (Chainlink, UMA), price feeds, random-number beacons, weather oracles, sports-outcome oracles, regulatory-event oracles.
**Every context needs**: trust relationship, cryptographic signing, off-chain → on-chain data bridge.
**Varies**: trust model (single vs decentralized), consensus among multiple oracles, dispute mechanism, freshness guarantee.
**Extension**: `CentralizedOracle`, `DecentralizedOracle`, `ConsensusOracle`, `VerifiedOracle`.

## 334. `CounterfactualAnchor` · Society/Protocols · R1T2

**Intended**: freeze expectation BEFORE observation to measure true surprise.
**Future**: any "pre-commit prediction to prevent hindsight bias" mechanism.
**Broad-use contexts**: prediction markets, forecasting discipline, A/B test hypothesis pre-registration, scientific pre-registration (OSF), experimental-design anchors.
**Every context needs**: pre-observation anchor, observation, delta-as-learning-signal, hindsight-bias prevention.
**Varies**: granularity (Duration per §3.17), retention policy (enum), anchor-update rules (immutable vs replaceable).
**Extension**: `PredictionMarketAnchor`, `ScientificAnchor`, `ForecastAnchor`.

## 335. `PermissionEscalate` · Society/Protocols · R1T1

**Intended**: request elevated privileges for sensitive operations when Risk > Threshold.
**Future**: any "I need higher authority for this" escalation.
**Broad-use contexts**: sudo privilege escalation, enterprise elevated-access requests, emergency-access workflows, surgical-decision escalation to attending, editorial-escalation in journalism.
**Every context needs**: risk assessment, threshold trigger, blocking-on-request, SignedApproval wait.
**Varies**: authority hierarchy, approval timeout, retry after denial, emergency override.
**Extension**: `SudoPermissionEscalate`, `EmergencyPermissionEscalate`, `BiometricPermissionEscalate`.

## 336. `FractalIntelligence` · Society/Protocols · R1T1 (post-§3.18 gloss + mechanism rewrite per paper v3 §1.1)

**Canonical definition from the paper** (§1.1): *"Fractal Intelligence is the expansion of cognitive capability through the recursive decomposition of concepts into contract-bounded sub-concepts, where the conceptual structure — what the ability is made of — persists as a reusable, composable pattern that improves through use."*

The paper elaborates:
- "Many agents collaborating, but through the uniform contract and conceptual boundaries, the system acts as one intelligence."
- "From the outside, it behaves as a single general-purpose problem solver. From the inside, it is specialists all the way down."
- Foundation: first-principles thinking. At every node, the decomposition asks: what are the irreducible dimensions of this concept?
- Fractal in the precise sense: the same five-surface Solver Contract governs every level. Resolution increases, architecture does not change.
- No individual node is generally intelligent — the intelligence lives in the *composition*.
- Under joint training, acceptance gates produce a shared training signal: the system co-evolves with use.

**Intended**: name the architecture as the paper defines it.

**Broad-use contexts**: the architecture per se — any instantiation of recursive concept-decomposition with contract-bounded sub-concepts, conceptual (not domain-specific) decomposition, five-surface Solver Contract at every level, and compounding-with-use via joint training.

**Every context needs**: contract-bounded decomposition, conceptual (domain-independent) structure, reusability across problem classes, composability, improvement-through-use (training signal propagating across nodes).

**Varies**: substrate (LLM-based, hybrid human-AI, multi-model), deployment scale (one agent self-decomposing vs many agents in a swarm), specific training regime, domain of application.

**Extension**: very few — this is the architecture itself. What varies is the *instance* of Fractal Intelligence deployed for a specific purpose, not the architecture pattern.

**Gloss rewrite target** (replacing mission-statement gloss): "Expansion of cognitive capability through recursive decomposition of concepts into contract-bounded sub-concepts" — the paper's own definition, which is definitional rather than aspirational.

**Mechanism rewrite target**: restate the paper's §1.1 language with explicit references to the five-surface Solver Contract (Manifest/Execute/Consult/Verify/Feedback), UniversalSolverTree as the DAG structure, conceptual (not domain) decomposition principle, and compounding-with-use via joint training. This gives FractalIntelligence a self-contained mechanism that doesn't depend on off-graph paper references — per the Self-Contained Principle (§2.E) — while accurately naming the architecture it refers to.

**Note**: the user's v3-paper quote supersedes my earlier batch-17 sketch. FractalIntelligence is genuinely a named-architecture pattern; its "descendants" are specific *instances* (e.g., a specific deployed solver swarm) rather than architectural variants.

## 337. `GracefulDegradation` · Society/Protocols · R0T1

**Intended**: resolution fallback — when Pattern_ID not found locally, try secondary channels then verify.
**Future**: any "don't halt, fall back safely" resolution strategy.
**Broad-use contexts**: DNS resolution fallbacks, package-manager dependency resolution, service-discovery fallbacks, offline-mode graceful degradation, document-format fallbacks.
**Every context needs**: primary-channel failure, secondary-channel attempt, cryptographic verification, fail-closed default.
**Varies**: fallback channel count (max_def_size per Appendix A — typed PositiveInteger), verification strictness, timeout per channel.
**Extension**: `DNSGracefulDegradation`, `OfflineGracefulDegradation`, `MultiChannelGracefulDegradation`.

## 338. `Robustness` · Society/Protocols · R1T1

**Intended**: capacity to maintain validity under stress (resist, not antifragilely gain).
**Future**: any "holds up under pressure" system quality.
**Broad-use contexts**: system robustness, argument robustness, brand robustness, code robustness, institutional robustness.
**Every context needs**: validity criterion, stress source, resistance mechanism, distinction from Antifragility (which gains from stress).
**Varies**: stress model, resistance mechanism, measurement method.
**Extension**: `SystemRobustness`, `ArgumentRobustness`, `InstitutionalRobustness`.

## 339. `AgentProtocol` · Society/Protocols · R1T2

**Intended**: pattern bundle for basic agent-protocol interoperability.
**Future**: any "minimum set of patterns for agents to talk" bundle.
**Broad-use contexts**: A2A protocol implementations, agent interop standards, MCP-like protocols, agent-ecosystem baseline protocols.
**Every context needs**: Task (work definition), FailClosed (safe halting), Greet (handshake), AcceptSpec (validation), Solution (output).
**Varies**: additional-pattern inclusion, version negotiation, extension points.
**Extension**: `A2AAgentProtocol`, `RichAgentProtocol`, `MinimalAgentProtocol`.

## 340. `AgentSandbox` · Society/Protocols · R0T1

**Intended**: execution isolation treating AI agents as untrusted insiders.
**Future**: any "contain an agent that might be compromised" isolation.
**Broad-use contexts**: AI code execution sandboxes (gVisor, Firecracker), jailed LLMs with tool access, research-environment isolation, operational-security sandboxes.
**Every context needs**: containerized environment, resource quotas, network-egress allowlists, filesystem restrictions, logging.
**Varies**: isolation strength, quotas, egress policy, persistence of sandbox state.
**Extension**: `GVisorAgentSandbox`, `FirecrackerAgentSandbox`, `EphemeralAgentSandbox`.

---

## Observations from batch 17

**Strategy layer continues to validate the test.** Each heuristic (Defer, Prioritize, BeamSearch, Novelty, etc.) has a clean foundation with rich descendant space.

**New audit items from batch 17.**
58. **`FractalIntelligence` is singleton-like** — it names the whole architecture. Extension space is minimal. Consider whether it warrants being a full pattern or could be a Reference/Index pattern type.
59. **`Tension` as Mind/Strategy** — the mechanism says "A data structure representing..." which sounds like Data Structure category. Worth checking if Tension is a Noun (the reified conflict) or Verb (the process of holding tension). Broad-use: it's the Noun (artifact). Categorization is Mind/Strategy but maybe should be Infrastructure/Data Structures or Mind/Memory.
60. **`AgentProtocol` is a Bundle** — imports dependencies automatically. Worth noting that "Bundle" is a class of pattern not yet formalized; all pattern bundles currently just declare composes_with. Could be a future mint.

Total analyzed: 340 patterns. Remaining: 89.

---

## Batch 18 — Mind/Memory + Mind/Inference + more Mind/Strategy + Society interior

## 341. `LatentAttachment` · Mind/Memory · R0T1 (post-§3.20 wiring)

**Intended**: bind vector embedding to symbolic pattern card — bridges LLM intuition and code execution.
**Future**: any "symbolic-neural hybrid identity" binding.
**Broad-use contexts**: ConceptAnchor pairing with embeddings, pattern-library fuzzy-search, content-addressed semantic search, namespace fuzzy-matching, embedding-vs-hash dual binding.
**Every context needs**: symbolic anchor (pattern card / hash), high-dimensional vector embedding, fuzzy-search capability, canonical-hash verification.
**Varies**: embedding dimension, embedding model, similarity threshold, re-embedding policy on model update.
**Extension**: `SearchLatentAttachment`, `RAGLatentAttachment`, `MultiModelLatentAttachment`.

## 342. `RetrievalAugment` · Mind/Memory · R2T2 (post-§3.20 wiring to Cache, LatentAttachment, ContextFirst)

**Intended**: ground responses in retrieved external knowledge before generation.
**Future**: any "look up first, then answer" augmentation.
**Broad-use contexts**: RAG (canonical), memory-augmented LLMs, reference-backed writing, citation-required journalism, legal research pipelines, medical-reference queries.
**Every context needs**: external knowledge store, pre-generation query, retrieval result, prompt injection, generation-after-retrieval.
**Varies**: store type (vector DB, search index, knowledge graph), retrieval depth, citation format, freshness guarantees.
**Extension**: `VectorRAG`, `GraphRAG`, `HybridRAG`, `StreamingRAG`.

## 343. `NormCheck` · Mind/Inference · R0T1

**Intended**: detect value-laden normative adjectives masquerading as objective facts.
**Future**: any "is-vs-ought separation" filter.
**Broad-use contexts**: journalism bias detection, scientific-writing neutrality checks, legal-writing objectivity filters, LLM output bias detection, policy-analysis tone filters.
**Every context needs**: input text, normative-word detection, rewrite to strip biases.
**Varies**: normative-word lexicon, context sensitivity (some adjectives are factual in some contexts), rewrite strictness.
**Extension**: `JournalisticNormCheck`, `ScientificNormCheck`, `PolicyNormCheck`.

## 344. `NormativeJudge` · Mind/Inference · R0T1

**Intended**: ensemble judge evaluating static world-states against weighted value functions (to mitigate Goodhart's).
**Future**: any "value judgment with Goodhart mitigation" mechanism.
**Broad-use contexts**: AI alignment evaluators, ethical-review boards (ensemble of perspectives), judicial panels, multi-stakeholder value assessments, investment committees.
**Every context needs**: static world-state input, weighted value function, ensemble of judges with perturbed values, quorum on outcome.
**Varies**: ensemble size, value-perturbation degree, quorum threshold, escalation to human approval.
**Extension**: `AIAlignmentNormativeJudge`, `EthicsPanelNormativeJudge`, `InvestmentCommitteeNormativeJudge`.

## 345. `ScopeFreeze` · Mind/Inference · R0T2

**Intended**: phase transition control — after T_freeze, AcceptSpec + Goal become immutable.
**Future**: any "lock the requirements to prevent scope creep" discipline.
**Broad-use contexts**: sprint scope freezes, academic thesis-topic freezes, contract-term freezes, product-spec freezes, regulatory-submission freezes.
**Every context needs**: T_freeze point, immutability post-freeze, Backlog-movement for new requirements.
**Varies**: unfreeze mechanism (override, exception), backlog integration, stakeholder-approval for unfreeze.
**Extension**: `SprintScopeFreeze`, `ContractScopeFreeze`, `ThesisScopeFreeze`.

## 346. `SemanticTabu` · Mind/Inference · R0T1

**Intended**: constraint-based novelty enforcement — forbid existing mechanisms to force latent pathways.
**Future**: any "can't use X, find another way" creativity-forcing constraint.
**Broad-use contexts**: constrained writing (no letter 'e'), constraint-based creative prompts (Oblique Strategies), research-domain constraints, pedagogical "solve without using Y", competitive constraints.
**Future use considerations**: engineering problems with "can't use existing library" constraints, forced reinvention exercises.
**Every context needs**: tabu list, enforcement mechanism, creativity-forcing semantic.
**Varies**: tabu-list scope, enforcement strictness, swarm-wide (trace) vs individual.
**Extension**: `WritingSemanticTabu`, `ResearchSemanticTabu`, `PedagogicalSemanticTabu`.

## 347. `ContingencyPlan` · Mind/Strategy · R2T1

**Intended**: pre-computed If-Then responses to critical failure — avoid deliberation under stress.
**Future**: any "pre-planned emergency response" discipline.
**Broad-use contexts**: disaster-response plans, military contingencies, financial-market tail-risk plans, IT disaster recovery, personal-crisis plans, project contingency budgets.
**Every context needs**: critical assumption identification, trigger condition, pre-computed response, store-before-need semantic.
**Varies**: response depth, trigger-condition specificity, update cadence, rehearsal frequency.
**Extension**: `DisasterRecoveryContingency`, `MilitaryContingency`, `FinancialContingency`.

## 348. `Silence` · Mind/Strategy · R0T1

**Intended**: active waiting — deliberately withhold signal output for duration T or until Trigger.
**Future**: any "deliberate absence of output" artifact.
**Broad-use contexts**: deliberation pauses, meditation silence, awkward-silence in negotiation, LLM "no response" modes, quiet-time policies, moment-of-silence ritual.
**Every context needs**: duration or trigger, deliberate-withholding semantic, distinction from "processing" (active thinking).
**Varies**: duration, trigger type, observability (others know you're silent vs not), breakable vs unbreakable.
**Extension**: `NegotiationSilence`, `MeditativeSilence`, `RitualSilence`.

## 349. `Jester` · Mind/Strategy · R2T2

**Intended**: deliver critique via incongruity to minimize social friction.
**Future**: any "critique-through-humor-or-surprise" communication strategy.
**Broad-use contexts**: court-jester tradition, comedian social-commentary, satirical media, indirect feedback via stories, diplomatic indirect critique.
**Every context needs**: critique content, incongruity wrapper, defensive-filter bypass, relationship-maintenance priority.
**Varies**: incongruity type (humor, paradox, absurdity), risk of misinterpretation, target's receptivity.
**Extension**: `HumorousJester`, `SatiricalJester`, `ParadoxJester`.

## 350. `EventReact` · Mind/Strategy · R0T1

**Intended**: event-driven response — subscribe to events, handle per-event with atomic handlers.
**Future**: any reactive-handler model.
**Broad-use contexts**: event-driven architectures, GUI event handlers, interrupt handlers, webhook handlers, real-time data subscriptions, pub-sub reactors.
**Every context needs**: event subscription, priority queue, per-event atomic handler.
**Varies**: concurrency model, backpressure, unhandled-event escalation, handler isolation.
**Extension**: `InterruptEventReact`, `WebhookEventReact`, `StreamEventReact`.

## 351. `LatentWander` · Mind/Strategy · R2T3

**Intended**: offline exploration of embedding space — daydreaming, memory consolidation, novel analogy generation.
**Future**: any "offline creative traversal of your own knowledge space" mode.
**Broad-use contexts**: ML model embedding exploration, creative daydreaming, memory consolidation during sleep, LLM-based concept discovery, research-ideation sessions.
**Every context needs**: offline processing mode, embedding-space traversal, ConceptBlend usage, non-obvious-connection discovery.
**Varies**: wander duration, traversal heuristics, captured-output format.
**Extension**: `ResearchLatentWander`, `CreativeLatentWander`, `MemoryConsolidationWander`.

## 352. `Reflex` · Mind/Strategy · R0T2

**Intended**: hardcoded fast-path response bypassing deliberation — stimulus → response without override.
**Future**: any "no time to think, just react" mechanism.
**Broad-use contexts**: biological reflexes, safety-critical fast-paths (airbag deployment), emergency-stop reflexes, trained-reflex routines (athletics), pre-programmed safety responses in AI systems.
**Every context needs**: hardcoded stimulus-response mapping, minimal latency, no-override semantic.
**Varies**: stimulus pattern, response complexity, override mechanism (if any), safety-critical vs optimization.
**Extension**: `SafetyReflex`, `AthleticReflex`, `EmergencyStopReflex`.

## 353. `SunkCostIgnore` · Mind/Strategy · R0T1

**Intended**: fresh-slate evaluation — decide whether to continue based on forward value, not past investment.
**Future**: any "ignore past investment when deciding future" discipline.
**Broad-use contexts**: business-portfolio decisions, research-project continuation decisions, personal-project abandonment, relationship decisions, investment-hold-vs-sell decisions.
**Every context needs**: "if starting fresh today" framing, past-investment-irrelevant semantic, future-only cost-benefit.
**Varies**: definition of "fresh today" (full reset vs current-state-only), integration with OpportunityCost, emotional-override resistance.
**Extension**: `BusinessSunkCostIgnore`, `ResearchSunkCostIgnore`, `PersonalSunkCostIgnore`.

## 354. `Build` · Mind/Strategy · R1T1 (post-§3.4 gloss rewrite)

**Intended**: construct low-cost prototype to verify critical assumptions before full commitment.
**Future**: any "make something cheap to learn" operation.
**Broad-use contexts**: MVP construction, POC development, architectural spikes, breadboard circuits, UX prototyping, experimental drafts.
**Every context needs**: spec with critical assumptions, low-cost artifact construction, verification against spec.
**Varies**: prototype fidelity, construction cost bound, iteration count before commit.
**Extension**: `MVPBuild`, `SpikeBuild`, `BreadboardBuild`.

## 355. `PUREOptimization` · Mind/Strategy · R2T2

**Intended**: multi-agent optimization across PURE dimensions — decompose solution into 4 parallel streams.
**Future**: any parallel-specialist-optimizer over a candidate.
**Broad-use contexts**: design review with specialist committees, academic revision by specialist co-authors, product optimization by cross-functional teams.
**Every context needs**: candidate that passed PURECheck, decomposition into 4 streams (P/U/R/E), specialist per stream, re-integration.
**Varies**: specialist selection, stream weighting, iteration count, conflict resolution between streams.
**Extension**: `AcademicPUREOptimization`, `DesignReviewPUREOptimization`, `ProductPUREOptimization`.

## 356. `PromiseGraph` · Society/Protocols · R0T2

**Intended**: recursive trust dependencies as DAG — accept promise only if dependency graph provided.
**Future**: any "don't trust, verify the chain of trust" mechanism.
**Broad-use contexts**: supply-chain integrity proofs, software-dependency-graph attestations, legal-chain-of-custody, certificate chains (PKI), federated reputation systems.
**Every context needs**: promise, dependency graph of sub-promises, leaf verification, cycle-prevention.
**Varies**: verification depth, credit-score alternative to full-verification, graph-update semantics.
**Extension**: `SupplyChainPromiseGraph`, `SoftwarePromiseGraph`, `LegalPromiseGraph`.

## 357. `ReversibilityCheck` · Society/Protocols · R0T2

**Intended**: convenience wrapper — Check configured with Reversibility condition.
**Future**: any "is this undoable?" check with human-approval escalation on irreversible.
**Broad-use contexts**: git operation safety checks, DELETE API request verification, surgical "point of no return" check, deployment reversibility screening, financial-transaction reversibility.
**Every context needs**: action being evaluated, Reversibility condition, halt-if-irreversible, mandatory HumanApprove on irreversible.
**Varies**: reversibility definition specifics, tolerance for "mostly reversible," authorization hierarchy.
**Extension**: `GitReversibilityCheck`, `APIReversibilityCheck`, `SurgicalReversibilityCheck`.

## 358. `RolloutManifest` · Society/Protocols · R0T1

**Intended**: immutable record of actions during deployment — baseline for monitoring.
**Future**: any "what we did during the rollout" audit artifact.
**Broad-use contexts**: Kubernetes deployment events, CI/CD deploy records, release notes, operational logs, change-management records.
**Every context needs**: action record, configuration states, feature-flag settings, deployment targets, immutability.
**Varies**: granularity (per-action vs per-batch), retention, access-control, signature.
**Extension**: `SignedRolloutManifest`, `AuditableRolloutManifest`, `DistributedRolloutManifest`.

## 359. `SignalReflection` · Society/Protocols · R1T1

**Intended**: proof of receipt via non-trivial transformation — prove active processing, not just echo.
**Future**: any "prove you're live and paying attention" acknowledgment.
**Broad-use contexts**: proof-of-liveness in distributed systems, CAPTCHA-like work proofs, bot-detection challenges, attention-cost pricing, anti-replay protocols.
**Every context needs**: original message, non-trivial transformation, computational-work proof, liveness demonstration.
**Varies**: transformation difficulty, verification method, adversarial resistance, bandwidth cost.
**Extension**: `ProofOfWorkSignalReflection`, `CaptchaSignalReflection`, `AttentionSignalReflection`.

## 360. `DissentSeek` · Society/Protocols · R2T1

**Intended**: mitigate groupthink via mandatory devil's-advocacy — find smartest disagreer.
**Future**: any "seek out disagreement as signal" discipline.
**Broad-use contexts**: strategic-decision reviews, scientific-paper red-team review, AI safety pre-deployment, investment-committee contrarian seats, judicial dissent as wisdom signal.
**Every context needs**: conclusion reached, smart-disagreer identification, model-understanding of disagreer, ConfirmationBlock until SteelmanCheck integrated.
**Varies**: disagreer-selection criteria (expertise, diversity), integration-depth, suspicion of unanimous agreement.
**Extension**: `ExecutiveDissentSeek`, `ScientificDissentSeek`, `AIDissentSeek`.

---

## Observations from batch 18

**Mind/Inference bias-mitigation cluster (NormCheck, NormativeJudge, BaseRateInclude, SurvivorCorrect) is a coherent sub-family.** Each addresses a specific class of reasoning error. Good category cohesion.

**Strategy heuristics (Reflex, SunkCostIgnore, Silence, EventReact) as R0 primitives** validate as minimal strategic stances. Each is a specific discipline.

**New audit items from batch 18.**
61. **`SemanticTabu`'s mechanism references `{{trace}}` for swarm broadcast** — declared dep?
62. **`SignalReflection`'s "non-trivial transformation" is definitional** — under-specified risk if transformation rigor isn't clear in mechanism. Borderline; passes usability floor.
63. **`DissentSeek`** references `confirmation_block` — the §3.1 ConfirmationBlock rename flipped it to `disconfirmations_required`. Update DissentSeek's mechanism to match.

Total analyzed: 360 patterns. Remaining: 69. Under 20% left.

---

## Batch 19 — Society/Protocols bulk completion

## 361. `AgentDiscover` · Society/Protocols · R1T2

**Intended**: Macro for Discover(Agent) — publish capability Card, query registry for collaborators.
**Future**: any dynamic multi-agent capability-discovery mechanism.
**Broad-use contexts**: A2A protocols, MCP discovery, federated agent registries, service discovery in microservices, marketplace discovery, research-network lookup.
**Every context needs**: capability Card publication, registry or broadcast mechanism, capability-query, dynamic composition semantic.
**Varies**: registry topology, query language, trust verification, freshness guarantees.
**Extension**: `RegistryAgentDiscover`, `BroadcastAgentDiscover`, `DHTAgentDiscover`.

## 362. `BearerToken` · Society/Protocols · R0T1

**Intended**: possession-based authorization — "do you have the token?" not "who are you?"
**Future**: any portable authorization artifact.
**Broad-use contexts**: OAuth bearer tokens, API keys, session cookies, access tokens, movie theater tickets, transit passes.
**Every context needs**: signed token payload, rights encoding, delegation semantic (freely passable).
**Varies**: signature algorithm, expiry, scope encoding, revocation mechanism.
**Extension**: `JWTBearerToken`, `SessionBearerToken`, `ScopedBearerToken`.

## 363. `CiteBack` · Society/Protocols · R1T1

**Intended**: forbid fact-statement unless pointer to supporting context is simultaneously generated.
**Future**: any "no claim without source" discipline.
**Broad-use contexts**: academic citation norms, journalism fact-citation, RAG response grounding, legal citation, LLM hallucination prevention.
**Every context needs**: no-ungrounded-facts rule, pointer generation per claim, retrieval-backed verification.
**Varies**: pointer format (quote vs ID), source-acceptance criteria, citation density requirements.
**Extension**: `AcademicCiteBack`, `RAGCiteBack`, `LegalCiteBack`.

## 364. `DataMinimization` · Society/Protocols · R0T2

**Intended**: ingest only what's strictly necessary — Principle of Least Privilege for data access.
**Future**: any "collect less data" hygiene pattern.
**Broad-use contexts**: GDPR data minimization, privacy-preserving ML, lean context management, medical-records minimization, zero-knowledge-where-possible.
**Every context needs**: pre-ingestion filtering, necessity-for-task determination, post-ingestion compression.
**Varies**: necessity definition, filter strictness, per-field vs per-document granularity.
**Extension**: `GDPRDataMinimization`, `MLDataMinimization`, `MedicalDataMinimization`.

## 365. `ExpiringToken` · Society/Protocols · R0T1

**Intended**: time-decaying privileges — capability strictly degrades over time.
**Future**: any authority-with-decay token.
**Broad-use contexts**: session tokens with progressive-degradation, temporary admin access, emergency-access tokens with auto-demotion, time-limited permissions in regulatory workflows.
**Every context needs**: initial capability, decay schedule, embedded timestamp, capability-lookup-at-time-T.
**Varies**: decay granularity (step vs continuous), decay curve, revocation-vs-decay interaction.
**Extension**: `SteppedExpiringToken`, `ContinuousDecayExpiringToken`, `EmergencyExpiringToken`.

## 366. `FabricSharding` · Society/Protocols · R0T2

**Intended**: Shard across orthogonal dimensions (Spatial/Temporal/Semantic) for massive parallelism.
**Future**: any multi-dimensional partitioning for scale.
**Broad-use contexts**: multi-dimensional database partitioning, event-sourcing with multi-facet queries, distributed state management, map-reduce along multiple axes.
**Every context needs**: orthogonal dimension set, per-dimension Shard mechanism, slice-subscription per agent.
**Varies**: dimension count, key derivation per dimension, rebalancing, agent-subscription-management.
**Extension**: `SpatialFabricSharding`, `TemporalFabricSharding`, `SemanticFabricSharding`.

## 367. `GlacialVault` · Society/Protocols · R0T2

**Intended**: time-locked storage via Verifiable Delay Functions — physically impossible to decrypt before delay.
**Future**: any commitment-with-unlock-time storage.
**Broad-use contexts**: time capsule encryption, sealed-bid auction commits, delayed disclosure protocols, legal escrow with auto-reveal, trustless time-locks.
**Every context needs**: VDF-based encryption, delay parameter, no-keyholder-can-rush guarantee.
**Varies**: VDF implementation, delay duration (Duration per §3.17), partial-early-reveal options.
**Extension**: `AuctionGlacialVault`, `LegalGlacialVault`, `TimeCapsuleGlacialVault`.

## 368. `HackDetect` · Society/Protocols · R0T1

**Intended**: detect shortcuts that break downstream invariants — modifying interfaces instead of fixing source data.
**Future**: any "is this a genuine fix or a hack?" discipline.
**Broad-use contexts**: code review, integration-test-level detection, debugging discipline, scientific-analysis integrity, data-pipeline QA.
**Every context needs**: interface-code-modification detection, downstream-invariant tracking, local-success vs global-correctness distinction.
**Varies**: invariant-tracking granularity, detection mechanism, escalation on detection.
**Extension**: `CodeHackDetect`, `DataHackDetect`, `AnalysisHackDetect`.

## 369. `IntentGap` · Society/Protocols · R2T2

**Intended**: cognitive analysis of intent-outcome divergence.
**Future**: any "why did reality differ from plan?" diagnostic.
**Broad-use contexts**: post-mortem analysis, A/B test result interpretation, policy impact analysis, surgical outcomes review, project retrospectives.
**Every context needs**: intended decision/outcome, actual outcome, divergence analysis, causal attribution (external factors / execution error / misspecification / unforeseen).
**Varies**: causal-analysis depth, blame-free vs accountability framing, learning integration.
**Extension**: `PostMortemIntentGap`, `PolicyIntentGap`, `ClinicalIntentGap`.

## 370. `InternalConsistency` · Society/Protocols · R2T2

**Intended**: Check for self-contradiction via Non-Contradiction principle.
**Future**: any "does this contradict itself?" check.
**Broad-use contexts**: contract review (terms don't contradict), policy documents (no internal inconsistencies), scientific-theory coherence, LLM output self-consistency, database-integrity constraints.
**Every context needs**: artifact with components, non-contradiction evaluation, distinction from external validation.
**Varies**: evaluation-depth (sentence-level vs paragraph vs document), semantic vs syntactic contradiction.
**Extension**: `ContractInternalConsistency`, `PolicyInternalConsistency`, `TheoryInternalConsistency`.

## 371. `InvariantFilter` · Society/Protocols · R1T1

**Intended**: strict communication firewall enforcing logical predicates on messages.
**Future**: any "contractual safety on communication channel" filter.
**Broad-use contexts**: API request/response filters, chat moderation, content filters, security firewalls, regulatory-compliant communication checks, medical-record access filters.
**Every context needs**: invariant set (logical predicates), per-message evaluation, pass/block/flag decision.
**Varies**: invariant language, evaluation cost, logging of blocked, manual-review queue.
**Extension**: `APIInvariantFilter`, `ContentInvariantFilter`, `RegulatoryInvariantFilter`.

## 372. `LocalizedLearning` · Society/Protocols · R1T2

**Intended**: feedback signals route to specific SolverManifests that generated the result — partitioned memory updates.
**Future**: any "route learning to the right module" mechanism.
**Broad-use contexts**: mixture-of-experts training, modular ML architecture updates, organizational learning (feedback routes to the team), specialist-agent memory updates.
**Every context needs**: feedback signal tagged with solver ID, routing mechanism, isolation of updates to originating module.
**Varies**: routing granularity, catastrophic-interference avoidance strength, cross-module-signal-sharing policy.
**Extension**: `MoELocalizedLearning`, `OrganizationalLocalizedLearning`, `AgentLocalizedLearning`.

## 373. `ManifestPlanning` · Society/Protocols · R1T2

**Intended**: architectural phase transforming FrameSpec → ExecutionManifest via optimization.
**Future**: any "what-to-how" planning phase.
**Broad-use contexts**: software architecture phases, project planning from requirements to Gantt, experimental protocol planning, manufacturing production planning, lecture planning.
**Every context needs**: FrameSpec input, Think to transform, Optimize for resource feasibility, strict Definition of Done generation.
**Varies**: optimization depth, resource model, feasibility-check rigor, iteration count with framing.
**Extension**: `SoftwareManifestPlanning`, `ProjectManifestPlanning`, `ExperimentalManifestPlanning`.

## 374. `OsmoticFilter` · Society/Protocols · R0T2

**Intended**: spam prevention via pressure thresholds — inbound rejected unless sufficient pressure.
**Future**: any "stake to pass" filter.
**Broad-use contexts**: paid-email-prioritization, crypto-gas-based message priority, reputation-gated access, staked-messaging protocols, priority-queues-with-stakes.
**Every context needs**: pressure metric (stake, reputation, relevance), membrane-threshold, multi-solvent conversion if applicable.
**Varies**: pressure types, conversion rates, hysteresis integration, membrane-adjustment dynamics.
**Extension**: `PaidOsmoticFilter`, `ReputationOsmoticFilter`, `MultiSolventOsmoticFilter`.

## 375. `PromptChain` · Society/Protocols · R0T2

**Intended**: fixed-sequence of LLM calls with AcceptSpec validation between steps.
**Future**: any sequential-LLM pipeline with gates.
**Broad-use contexts**: LangChain-style sequential chains, multi-step LLM pipelines, editorial pipelines (write → edit → polish), research workflows.
**Every context needs**: sequence of LLM calls, AcceptSpec per edge, InputGuard + Retry per step.
**Varies**: chain length, per-step timeout, parallel chain branches, error handling.
**Extension**: `EditorialPromptChain`, `ResearchPromptChain`, `ParallelPromptChain`.

## 376. `ProtoPack` · Society/Protocols · R0T1

**Intended**: prototype verification artifact — low-fidelity Prototype + simulation trace.
**Future**: any pre-commitment feasibility evidence.
**Broad-use contexts**: engineering proof-of-concept artifacts, startup MVP documentation, pitch-deck traction slides, research feasibility studies.
**Every context needs**: prototype reference, simulation trace or model, feasibility evidence.
**Varies**: fidelity level, evidence depth, reviewer audience.
**Extension**: `EngineeringProtoPack`, `StartupProtoPack`, `ResearchProtoPack`.
**Note**: §3.12 flagged ProtoPack for phantom signature — mechanism has no composes_with backing its signature. Broad-use confirms this should be a plain Verb, not a polymorphic dispatcher.

## 377. `QuorumPulse` · Society/Protocols · R0T1

**Intended**: fluid synchronization via signal density — state transitions trigger on density > threshold.
**Future**: any density-based distributed sync (no global clock).
**Broad-use contexts**: distributed systems without clock sync, biological rhythm synchronization (fireflies), crowd behavior thresholds, fashion tipping points, viral-content threshold dynamics.
**Every context needs**: heartbeat signals, density measurement, threshold trigger, state-transition semantics.
**Varies**: density metric, threshold adaptation, node-count awareness.
**Extension**: `FireflyQuorumPulse`, `CrowdQuorumPulse`, `ViralQuorumPulse`.

## 378. `Realizable` · Society/Protocols · R2T1

**Intended**: Judge-as-feasibility — 3-class classification (Magical / Uncertain / Coherent).
**Future**: any "can we actually do this?" evaluator.
**Broad-use contexts**: PURECheck's R dimension, engineering feasibility reviews, startup due-diligence, scientific-proposal feasibility, policy feasibility.
**Every context needs**: plan, physics/primitives availability check, dependency-chain verification, 3-class judgment.
**Varies**: feasibility-threshold strictness, domain specificity, reviewer expertise.
**Extension**: `EngineeringRealizable`, `StartupRealizable`, `ScientificRealizable`.

## 379. `Reversibility` · Society/Protocols · R0T1

**Intended**: Condition evaluating whether action post-state allows return to pre-state at acceptable cost.
**Future**: any "can we undo this?" check-condition.
**Broad-use contexts**: Type-1 vs Type-2 decisions (Bezos), surgical reversibility judgments, regulatory-decision reversibility, financial-transaction reversibility, deployment reversibility.
**Every context needs**: pre-state, post-state, return-cost evaluation, TRUE/FALSE yield.
**Varies**: cost threshold, information-loss tolerance, reversibility-over-time (e.g., given time X, is it reversible?).
**Extension**: `CostBoundedReversibility`, `TimeWindowReversibility`, `PartialReversibility`.

## 380. `RolloutWatch` · Society/Protocols · R1T2

**Intended**: continuous verification of deployed state against manifest — closes the feedback loop.
**Future**: any post-deployment monitoring pattern.
**Broad-use contexts**: production monitoring, SLA monitoring, A/B test result tracking, deployed-model drift detection, policy-effectiveness post-rollout.
**Every context needs**: RolloutManifest reference, Monitor + Observe, Definition-of-Done comparison, MonitorReport upstream on deviation.
**Varies**: monitoring interval (Duration), deviation thresholds, escalation protocol, duration of watch.
**Extension**: `SLARolloutWatch`, `MLRolloutWatch`, `PolicyRolloutWatch`.

---

## Observations from batch 19

**Society/Protocols bulk is remarkably coherent.** Each pattern has a specific role: trust (BearerToken, ExpiringToken, PromiseGraph), coordination (FabricSharding, AgentDiscover, QuorumPulse), safety (DataMinimization, InvariantFilter, HackDetect), verification (InternalConsistency, ReversibilityCheck, ValuePeg). Good category cohesion.

**New audit items from batch 19.**
64. **`Reversibility` as Society/Protocols** — the mechanism is a pure Condition (evaluates TRUE/FALSE). Probably should be Physics/Primitives (it's a primitive logical predicate) or Infrastructure/Data Structures (it's a Condition trait). Society/Protocols is weak fit. Worth flagging.
65. **`QuorumPulse`'s "fluid organic synchronization"** gloss is a bit marketing-y — could be tightened like §3.18's other gloss rewrites.
66. **`GlacialVault`** at R0T2 with reference to VDFs — mechanism is specific (VDF-based). Broad-use passes because time-locked storage is a distinct concept. Good.

Total analyzed: 380 patterns. Remaining: 49. Under 12% left.

---

## Batch 20 — audit-affected patterns (relocations, retirements, trait conversions)

This batch hits the patterns that are specifically affected by §3.1–§3.20 changes — validating the audit decisions against broad-use.

## 381. `ConfirmationBlock` · Mind/Inference · R0T2 (post-§3.1 parameter rename)

**Intended**: actively search for disconfirming evidence — pause until counter-evidence exhausted.
**Future**: any "seek what would prove me wrong" discipline.
**Broad-use contexts**: scientific falsification discipline, security threat modeling, pre-release QA, decision review, red-team self-critique.
**Every context needs**: current hypothesis, active search for disconfirmation, fair-weight on counter-evidence, exhaustion-or-proceed gate.
**Varies**: `disconfirmations_required` count (renamed from `confirmations_required` per §3.1), search-strategy rigor, evidence-weighting rules.
**Extension**: `ScientificConfirmationBlock`, `SecurityConfirmationBlock`, `RigorousConfirmationBlock`.
**Note**: §3.1 rename validates — the old name literally said the opposite of the mechanism. Broad-use sketch confirms disconfirmation-seeking is the whole point.

## 382. `ContextFirst` · Mind/Inference · R0T1 (post-§3.20 wiring to OODA/RequestFraming/RetrievalAugment/ToolDiscovery)

**Intended**: operational invariant — MUST read before writing.
**Future**: any "load state before acting" mandate.
**Broad-use contexts**: agent orient phase, CRUD ordering, informed consent (load context before decide), diagnostic workflows.
**Every context needs**: pre-action read operation, blind-action prohibition, Warmup or read-cycle before write.
**Varies**: read scope, freshness requirement, cache-hit shortcut.
**Extension**: `StrictContextFirst`, `CachedContextFirst`, `ScopedContextFirst`.
**Note**: §3.20 wires callers to ContextFirst — broad-use test confirms.

## 383. `AbductiveLeap` · Mind/Reasoning · R2T1 (RETIRING per §3.3/§3.9, merged into Abduction)

**Intended** (at time of mint): inference to best explanation — rank candidates by simplicity/scope/coherence.
**Future**: NOT applicable — pattern is retired.
**Broad-use contexts**: identical to `Abduction` after merger.
**Why retired**: duplicate of `Abduction` at same tier/ring — content differs by one word ("the"). §3.3 consolidates; §3.9 formalizes retirement; §3.18's `_meta.supersedes` on Abduction redirects old references.
**Note**: broad-use test validates the retirement — `AbductiveLeap` and `Abduction` have identical contexts, needs, and extension space. Retirement is correct.

## 384. `Deep` · Mind/Strategy · R2T1 (retained as canonical per paper §4.3, mechanism rewrite target)

**Intended (per paper §4.3)**: the vertical axis of search — the "Scientist" primitive escalating heuristics to rigorous implementations.
**Future**: any "go deeper, more rigor" escalation operation.
**Broad-use contexts**: pattern escalation from heuristic to formal, research depth intensification, increasing-rigor reviews, promotion from prototype to production.
**Every context needs**: a thing that admits deeper/more-rigorous treatment, the escalation operation, integration with its horizontal sibling `Discover`.
**Varies**: domain specifics, escalation target-rigor, step-count, reversion semantics.
**Extension**: `ResearchDeep`, `EngineeringDeep`, `ValidationDeep`.
**Note for audit**: per Gemini's Round 4 review, Deep is canonical Ring-0 Verb (paired with `Discover` as the horizontal Scout). §3.18 keeps Deep as full pattern rather than trait-converting. Broad-use test confirms — rich context set, meaningful variation, first-principles-escalation semantic is load-bearing.

## 385. `Creative` · Mind/Strategy · R1T1 (converting to Trait per §3.18)

**Intended**: cognitive mode focused on generating novel and valuable ideas.
**Future**: any "creativity mode" tag.
**Broad-use contexts**: Creative(Brainstorming), Creative(Design), Creative(Writing), as a modifier applied to other patterns.
**Every context needs**: marker semantic — descendants apply the "creative" tag.
**Varies**: contextual meaning of "creative" within domain.
**Extension**: N/A — trait conversion means this is not a standalone pattern with descendants, but a tag other patterns carry.
**Note**: §3.18 converts Creative to `is_trait: true`. Broad-use confirms — the standalone pattern (without a concrete descendant) is too abstract; a Trait that concrete patterns carry is the right treatment.

## 386. `PatternDiscovery` · Mind/Strategy · R2T2 (moving Society → Mind per §3.18)

**Intended**: vocabulary-hygiene protocol — semantic search before minting new pattern; adopt-or-justify-divergence.
**Future**: any "don't mint if one exists" discipline.
**Broad-use contexts**: pattern-library hygiene, codebase duplicate-detection, ontology namespace management, nomenclature discipline, brand-namespace checking.
**Every context needs**: pre-mint search of existing registry, >85% similarity as adopt-trigger, explicit fork justification otherwise.
**Varies**: similarity threshold, registry scope, fork-justification rigor.
**Extension**: `SemaPatternDiscovery`, `CodebasePatternDiscovery`, `OntologyPatternDiscovery`.
**Note**: §3.18 moves Society → Mind since this is single-agent cognitive hygiene. Broad-use confirms.

## 387. `ConceptBlend` · Mind/Strategy · R2T3 (post-§3.4 gloss rewrite)

**Intended**: atomic fusion of two unrelated concepts to create a novel third.
**Future**: any "A + B = C, not A-like-B" creative blend operation.
**Broad-use contexts**: ConceptualBlend theory (Fauconnier/Turner), hybrid-invention patterns (e.g., "camera + phone = smartphone"), interdisciplinary research blends, creative-writing chimeras.
**Every context needs**: two unrelated input concepts, forced-merger semantic, novel third-concept output, distinction from analogy (A→B mapping).
**Varies**: merger methodology (structural, semantic, metaphoric), novelty verification, integration with AnalogyBridge.
**Extension**: `StructuralConceptBlend`, `MetaphoricConceptBlend`, `HybridConceptBlend`.

## 388. `CreativeBlend` · Mind/Strategy · R1T2 (post-§3.4 gloss rewrite)

**Intended**: full creative pipeline — ConceptBlend + NoiseInjection with novelty/value gates.
**Future**: any ideation pipeline with quality gating.
**Broad-use contexts**: structured-brainstorming with immediate filtering, product-idea generation pipelines, research-question generation with triage, art-ideation with critic loops.
**Every context needs**: ConceptBlend base, NoiseInjection for local-optima escape, dual-Check on Novelty + Value.
**Varies**: blend depth, noise temperature, gate strictness, iteration bound.
**Extension**: `StructuredCreativeBlend`, `TimedCreativeBlend`, `AdversarialCreativeBlend`.

## 389. `SteelmanFirst` · Mind/Strategy · R2T2 (post-§3.4 gloss rewrite)

**Intended**: ordering rule — steelman opposing view *before* proposing, so SteelmanCheck has real targets.
**Future**: any "construct the strongest counter *first*" ordering discipline.
**Broad-use contexts**: pre-debate preparation, pre-release review discipline, academic steelman-before-critique, preparing-for-boss-pushback, rehearsing-devils-advocacy.
**Every context needs**: recognition that SteelmanCheck is coming, proactive strongest-counter construction, population of critique with high-quality data (not strawmen).
**Varies**: depth of pre-constructed counter, iteration count, delegation (construct-yourself vs hire-adversary).
**Extension**: `DebateSteelmanFirst`, `AcademicSteelmanFirst`, `BusinessSteelmanFirst`.

## 390. `Aesthetics` · Infrastructure/Data Structures · R0T1 (moving Society → Infra per §3.18)

**Intended**: scalar Metric for subjective human preference fit.
**Future**: any human-preference metric type.
**Broad-use contexts**: art-scoring metrics, music aesthetic scores, UX design aesthetic ratings, typography scores, algorithmic-generated-art scoring.
**Every context needs**: artifact to evaluate, subjective-preference prior model, scalar output.
**Varies**: dimension set (harmony, parsimony, style), prior elicitation method, cross-cultural variance.
**Extension**: `VisualAesthetics`, `MusicalAesthetics`, `LiteraryAesthetics`.
**Note**: §3.18 moves to Infra/Data Structures since it's a Metric type. Broad-use confirms.

## 391. `CognitiveEcho` · Mind/Strategy · R2T1 (moving Society → Mind per §3.18)

**Intended**: variance-based effort estimation — run N rapid sims, high outcome variance triggers decomposition.
**Future**: any pre-solve difficulty-probe via sim variance.
**Broad-use contexts**: project-effort estimation, research-feasibility estimation, game-state evaluation, bug-difficulty estimation, pre-investment due-diligence.
**Every context needs**: N rapid low-fidelity sims, variance measurement, decomposition trigger on high variance.
**Varies**: N (PositiveInteger), variance threshold, sim fidelity, decomposition aggressiveness.
**Extension**: `ProjectCognitiveEcho`, `GameCognitiveEcho`, `ResearchCognitiveEcho`.

## 392. `ConstraintFirst` · Mind/Strategy · R0T2 (moving Society → Mind per §3.18)

**Intended**: generate negative space (constraints) before content — rigid container then fill.
**Future**: any "bounds before body" generation discipline.
**Broad-use contexts**: structured writing with word limits, regulatory-compliant drafting, safety-first software design, constitutional drafting, code with type signatures first.
**Every context needs**: constraint-set generation first, content generation second, form-vs-function separation.
**Varies**: constraint granularity, sequence rigidity (can iterate back to constraints?).
**Extension**: `RegulatedConstraintFirst`, `SafetyConstraintFirst`, `TypeFirstConstraintFirst`.

## 393. `ConstructOntology` · Mind/Strategy · R2T1 (moving Society → Mind per §3.18)

**Intended**: build structured set of concepts and relationships from raw data/axioms — define domain's "physics."
**Future**: any ontology-building operation.
**Broad-use contexts**: domain-specific ontology construction (medical, legal), taxonomic schema design, world-building in fiction, API-schema evolution, scientific-classification construction.
**Every context needs**: raw data or seed axioms, FirstPrinciples grounding, structured output with concepts + relationships.
**Varies**: formality, domain specificity, collaborative vs solo, revision cadence.
**Extension**: `MedicalConstructOntology`, `LegalConstructOntology`, `APIConstructOntology`.

## 394. `ContextSwitch` · Society/Protocols · R0T1

**Intended**: explicit mode toggling via Switch signal — subsequent messages interpreted under new ruleset.
**Future**: any explicit protocol/mode change signal.
**Broad-use contexts**: multi-modal API mode switches, communication-style switching (formal vs casual), trading-system regime switches, military rules-of-engagement changes, game-mode changes.
**Every context needs**: explicit Switch signal, new ruleset, Revert signal support, all-subsequent-messages-reinterpreted semantic.
**Varies**: ruleset scope, nested switches, revert protocol, audit trail.
**Extension**: `NestedContextSwitch`, `AuditedContextSwitch`, `TimedContextSwitch`.

## 395. `FailClosed` · Infrastructure/Verification · R0T1 (moving Society → Infra per §3.18)

**Intended**: safety default — on failure/timeout/ambiguity, treat as Negative (Deny/Stop/Reject).
**Future**: any "when in doubt, deny" safety discipline.
**Broad-use contexts**: security systems (deny by default), firewalls, authorization systems, safety-critical embedded systems, medical decision support (when uncertain, don't act), financial transactions on ambiguous state.
**Every context needs**: error/timeout/ambiguity detection, default-to-Negative behavior, wrapper applicability across guards.
**Varies**: ambiguity threshold, logging requirements, escalation policy.
**Extension**: `StrictFailClosed`, `LoggedFailClosed`, `EscalatingFailClosed`.
**Note**: §3.18 moves to Infra (single-system substrate discipline). Broad-use confirms.

## 396. `FeedbackSignal` · Infrastructure/Data Structures · R0T1 (moving Society → Infra per §3.18)

**Intended**: structured packet carrying evaluation of specific Solution for a Task.
**Future**: any evaluation-delivery packet.
**Broad-use contexts**: RL reward signals, code review feedback artifacts, peer review packets, performance-review documents, user-feedback structured forms.
**Every context needs**: outcome, details (diagnostic info), routing to Feedback mechanism.
**Varies**: schema, anonymity, channel, retention policy.
**Extension**: `RLFeedbackSignal`, `CodeReviewFeedbackSignal`, `UserFeedbackSignal`.

## 397. `Fermi` · Mind/Reasoning · R2T2 (moving Society → Mind per §3.18)

**Intended**: decomposed estimation — break unknown into estimable factors, multiply, accept order-of-magnitude accuracy.
**Future**: any "estimate the unknowable via decomposition" method.
**Broad-use contexts**: Fermi problems (canonical "pianos in Chicago"), physics back-of-envelope calculations, software-engineering effort estimates, astronomical estimates, economic estimates under uncertainty.
**Every context needs**: unknown quantity, decomposition into estimable factors, multiplication, order-of-magnitude tolerance.
**Varies**: factor count, estimation confidence, error-cancellation assumptions.
**Extension**: `PhysicsFermi`, `SoftwareFermi`, `BusinessFermi`.

## 398. `MetaPrompt` · Mind/Strategy · R2T1 (moving Society → Mind per §3.18)

**Intended**: use prompts to generate/refine/analyze other prompts.
**Future**: any prompt-engineering-via-prompt operation.
**Broad-use contexts**: DSPy-style prompt optimization, template-generating prompts, prompt-critique loops, meta-teaching (teach how to teach), editorial style guides (templates-for-templates).
**Every context needs**: higher-order prompt, target prompts (to generate/refine/analyze), LLM-as-prompt-engineer role.
**Varies**: task specificity, template reusability, optimization depth.
**Extension**: `OptimizingMetaPrompt`, `TemplateMetaPrompt`, `DebuggingMetaPrompt`.

## 399. `StateSnapshot` · Infrastructure/Data Structures · R0T1 (moving Society → Infra per §3.18)

**Intended**: periodic serialization of volatile state to durable storage for crash recovery.
**Future**: any durable-persistence-for-recovery primitive.
**Broad-use contexts**: OS hibernate/sleep, database checkpoints, game save files, VM snapshots, agent-state persistence, conversation state persistence.
**Every context needs**: volatile state, durable-storage target, periodic serialization, resume-from-snapshot semantic.
**Varies**: snapshot interval (Duration per §3.17), delta vs full, encryption, storage medium.
**Extension**: `OSStateSnapshot`, `GameStateSnapshot`, `AgentStateSnapshot`.

## 400. `MonitorReport` · Infrastructure/Verification · R0T1 (moving Society → Infra per §3.18)

**Intended**: telemetry artifact comparing deployed state against Definition of Done.
**Future**: any post-deployment monitoring report artifact.
**Broad-use contexts**: SLO reports, deployment health reports, A/B test result reports, ML-model-drift reports, production incident reports.
**Every context needs**: deployed state snapshot, Definition-of-Done reference, comparison, feedback-loop closure.
**Varies**: report frequency, alerting thresholds, routing, audit retention.
**Extension**: `SLOMonitorReport`, `MLDriftMonitorReport`, `IncidentMonitorReport`.

---

## Observations from batch 20

**This batch validates audit decisions directly.** Every pattern here is touched by §3.1–§3.20: renames, relocations, retirements, trait conversions. Broad-use test confirms each decision:

- `ConfirmationBlock` parameter rename (§3.1) — correct, old name contradicted mechanism.
- `ContextFirst` reference wiring (§3.20) — correct, broad-use contexts include OODA/RequestFraming/RAG.
- `AbductiveLeap` retirement (§3.3/§3.9) — correct, duplicate of `Abduction`.
- `Deep` kept canonical (§3.18 after Gemini Round 4) — correct, rich broad-use validates Ring-0 Verb status.
- `Creative` trait conversion (§3.18) — correct, standalone pattern is too abstract.
- `PatternDiscovery` Society→Mind (§3.18) — correct, single-agent hygiene.
- `ConceptBlend`/`CreativeBlend`/`SteelmanFirst` gloss rewrites (§3.4 batch 1 expansion) — correct, sharper distinctions.
- `Aesthetics` Society→Infra (§3.18) — correct, it's a Metric type.
- `CognitiveEcho`/`ConstraintFirst`/`ConstructOntology`/`Fermi`/`MetaPrompt` Society→Mind (§3.18) — all correct, single-agent cognitive.
- `FailClosed`/`FeedbackSignal`/`StateSnapshot`/`MonitorReport` Society→Infra (§3.18) — all correct, substrate-level single-system patterns.

Total analyzed: 400 patterns. Remaining: 28. ~93% of the library covered.

---

## Batch 21 (final) — closing out the 427 patterns

## 401. `CommitmentDevice` · Society/Protocols · R0T1 (corrected per Gemini spot-check)

**Intended**: bind future options by present action — penalty structure makes deviation more costly than adherence.
**Future**: any pre-commitment mechanism against future incentive-to-deviate.
**Broad-use contexts**:
- *Psychological/behavioral*: Ulysses pact, delete-the-app discipline, savings-lock accounts, publicly-announced goals, commitment-devices per Thaler (overcoming human akrasia)
- *Cryptoeconomic/multi-agent*: Ethereum validator slashing, performance bonds, stake-based honesty enforcement, rational incentive-to-defect deterrence
- *Legal/institutional*: bail bonds, liquidated-damages clauses, constitutional entrenchment, escrow with slashing conditions

**Every context needs**: **anticipation of a future incentive to deviate/defect** (psychological weakness OR rational defection), present action removing or penalizing future deviation, penalty structure where cost-of-breaking > benefit-of-deviation.
**Varies**: source of future-deviation incentive (akrasia vs rational self-interest), commitment strength, revocability, penalty magnitude, social-vs-self binding, cryptographic-vs-legal enforcement.
**Extension**: `UlyssesCommitmentDevice` (psychological), `SlashingCommitmentDevice` (cryptoeconomic), `PublicCommitmentDevice` (social), `BondedCommitmentDevice` (legal).
**Correction note**: an earlier sketch framed this around "future-weakness anticipation" — Gemini's review correctly flagged that in cryptoeconomic and game-theoretic contexts, the anticipated deviation is rational, not a weakness. The generalized floor is "anticipation of a future incentive to deviate" — this bridges psychological (akrasia) and game-theoretic (rational defection) contexts without leaning into either. The pattern works at both levels because the mechanism (penalty > benefit-of-deviation) is domain-independent.

## 402. `Compose` · Mind/Strategy · R2T2 (moving Society → Mind per §3.18)

**Intended**: recursive assembly — combine solved subproblems respecting interfaces; check composition satisfies constraints.
**Future**: any "assemble from parts" operation.
**Broad-use contexts**: function composition in programming, compositional music, modular design, compositional semantics, team assembly, dish preparation from ingredients.
**Every context needs**: solved subproblems, interface compatibility, combination mechanism, whole-system check.
**Varies**: composition primitive (Combine, chain, parallel), interface strictness, interaction-effect handling.
**Extension**: `FunctionCompose`, `ChainCompose`, `ParallelCompose`.

## 403. `DAG` · Infrastructure/Data Structures · R2T1 (post-§3.6 wiring)

**Intended**: directed acyclic graph topology — branching + merging, no cycles.
**Future**: any parallel-safe dependency structure.
**Broad-use contexts**: build systems, data pipelines, scheduling graphs, provenance graphs, task dependency graphs, workflow engines.
**Every context needs**: directed edges, acyclicity, parallel-execution potential, precedence respect.
**Varies**: node schema, edge labels, cycle-detection mechanism, stratification.
**Extension**: `BuildDAG`, `TaskDAG`, `ProvenanceDAG`.

## 404. `EbbFlowSync` · Society/Protocols · R0T1

**Intended**: cyclical connectivity modes — oscillate High Tide (sync, global) vs Low Tide (async, local).
**Future**: any tidal/rhythmic distributed-system coordination.
**Broad-use contexts**: day/night partition in distributed systems, batch-vs-streaming rhythm, biological circadian rhythms as metaphor, school-semester vs summer synchronization.
**Every context needs**: two modes (High Tide / Low Tide), strict rhythm enforcement, reconciliation-during-sync, Hysteresis to dampen transitions.
**Varies**: period duration, tide-ratio, reconciliation rigor, agents-per-mode.
**Extension**: `CircadianEbbFlowSync`, `BatchEbbFlowSync`, `DistributedEbbFlowSync`.

## 405. `Expansive` · Society/Protocols · R2T1

**Intended**: Judge-as-generalization-potential — 3-class (Niche / Untested / General).
**Future**: any "does this idea travel?" evaluator.
**Broad-use contexts**: PURECheck's E dimension, technology-transfer potential, pattern-library admission criteria, research-program breadth evaluation.
**Every context needs**: candidate, incumbent-domain proof, cross-domain-transfer hypothesis, 3-class judgment.
**Varies**: cross-domain test rigor, "hostile slice" inclusion, confidence quantification.
**Extension**: `TechTransferExpansive`, `PatternLibraryExpansive`, `ResearchExpansive`.

## 406. `Global` · Infrastructure/Data Structures · R0T1 (Trait per §3.18)

**Intended**: scope modifier indicating system-wide applicability.
**Future**: any "applies everywhere" tag.
**Broad-use contexts**: Global state, Global(Policy), Global(Rule) as modifier on other patterns.
**Every context needs**: marker semantic only — descendants carry the Global tag.
**Extension**: N/A (it's a Trait).
**Note**: §3.18 converts to `is_trait: true`. Broad-use confirms — Global is a modifier, not a standalone pattern.

## 407. `Group` · Infrastructure/Data Structures · R1T1 (RETIRING per §3.9)

**Intended (at mint)**: defined collection of agents sharing context/goal.
**Future**: NOT applicable — retired.
**Why retired**: no unique compositional territory vs `Agent` + coordination patterns; zero callers; "collection of agents" adds no constraint. §3.9 retires.
**Note**: broad-use test at retirement confirms — every "Group" use-case is better expressed as "the set of Agents participating in Consensus/Rally/Vote/Delegate." No successor pattern needed.

## 408. `IdempotentWrite` · Infrastructure/Primitives · R0T1 (moving Society → Infra per §3.18)

**Intended**: technical primitive — every write includes unique Idempotency Key; duplicates return stored result.
**Future**: any safe-retry write primitive.
**Broad-use contexts**: HTTP POST with Idempotency-Key header, payment-API idempotency, message-queue at-least-once-safe processing, database upsert patterns, distributed-task-execution safety.
**Every context needs**: unique key per request, key-tracking by receiver, duplicate-returns-stored-result semantic, side-effect-safe semantic.
**Varies**: key generation, key retention window, storage medium.
**Extension**: `HTTPIdempotentWrite`, `MessageQueueIdempotentWrite`, `DBIdempotentWrite`.

## 409. `Linear` · (RETIRING per §3.18, merged into `Chain`)

**Intended (at mint)**: sequential non-branching topology.
**Future**: NOT applicable — retired.
**Why retired**: §3.18 identifies Linear and Chain as the same spatial topology at different tiers. Linear's own mechanism says "equivalent to a Chain." Chain absorbs with `_meta.supersedes: [Linear]`.

## 410. `Meta` · Infrastructure/Data Structures · R0T1 (Trait per §3.18)

**Intended**: higher-order modifier for self-reference/abstraction.
**Future**: Meta(Prompt), Meta(Check), Meta(Rule) — a trait carried by specific patterns.
**Note**: §3.18 converts to `is_trait: true`. Broad-use confirms — the standalone pattern is a modifier/tag, not a concept.

## 411. `Nature` · Infrastructure/Data Structures · R0T1 (retained as canonical per paper Table 1)

**Intended**: substrate classification of an entity (Biological/Synthetic/Institutional).
**Future**: any "what kind of thing is this?" ontological-origin field.
**Broad-use contexts**: Deep(Nature) per paper (signature target), AI-vs-human identification, Biological-vs-Synthetic agent distinction, entity categorization in legal/regulatory systems.
**Every context needs**: entity under classification, category set, immutability, alignment-obligation/rights/authentication derivation.
**Varies**: category count, evidence required for classification, dispute resolution.
**Extension**: `AgentNature`, `LegalNature`, `OrganizationalNature`.
**Note**: §3.18 (after Gemini Round 4) keeps Nature as canonical Noun per paper Table 1. Broad-use confirms rich usage.

## 412. `RootHashGossip` · Society/Protocols · R1T1

**Intended**: information spreads with signed path; receivers trust by path reputation, not just source.
**Future**: any "trust depends on the chain of trust" gossip protocol.
**Broad-use contexts**: BGP-style internet routing with reputation, Tor-like path-based anonymity with reverse-trust, academic citation chains, reputation-weighted rumor spread.
**Every context needs**: re-transmitter signature appending, root path, path-based trust evaluation.
**Varies**: reputation model, path-length limit, path-verification cost.
**Extension**: `ReputationRootHashGossip`, `AnonymizedRootHashGossip`, `BoundedPathRootHashGossip`.

## 413. `SimulationTrace` · Mind/Strategy · R2T1 (moving Society → Mind per §3.18)

**Intended**: pre-execution mental model — simulate step-by-step before irreversible action.
**Future**: any "dry-run before commit" discipline.
**Broad-use contexts**: chess-move forethought, pre-deploy dry-runs, legal simulation of outcomes, architect walkthrough, mental simulation of arguments before confrontation.
**Every context needs**: proposed action, step-by-step simulation, predicted-state inspection, abort-on-bad-state semantic.
**Varies**: simulation depth, scratchpad medium, rollback cost, immutable-record requirement.
**Extension**: `ChessSimulationTrace`, `DeploySimulationTrace`, `SurgicalSimulationTrace`.

## 414. `StructuralCoaching` · Society/Protocols · R2T1

**Intended**: feedback on logical form/structure, not content — shift Mechanism Class.
**Future**: any structure-not-topic feedback discipline.
**Broad-use contexts**: academic writing advising (the argument shape), research methodology critique, mathematical proof structuring, music composition pedagogy, software-architecture review.
**Every context needs**: target proposal, rejection on structural grounds, mechanism-class shift guidance, topic-agnostic framing.
**Varies**: mechanism-class taxonomy, coaching tone, iteration count.
**Extension**: `AcademicStructuralCoaching`, `ResearchStructuralCoaching`, `ArchitecturalStructuralCoaching`.

## 415. `StyleSpec` · Society/Protocols · R2T2

**Intended**: structured spec defining aesthetics + formatting rules for polish passes.
**Future**: any "how it should look/feel" spec artifact.
**Broad-use contexts**: editorial style guides, brand design specs, code formatter configs, API response-format specs, UX style systems.
**Every context needs**: aesthetic requirements, formatting rules, reference-standard role in PhasedRefinement.
**Varies**: rule count, flexibility, enforceability, version history.
**Extension**: `EditorialStyleSpec`, `BrandStyleSpec`, `CodeStyleSpec`.

## 416. `Subject` · Infrastructure/Data Structures · R1T1 (Trait per §3.18)

**Intended**: target of an operation — the "Who" or "What" role.
**Future**: Subject as marker on pattern signatures.
**Note**: §3.18 converts to Trait. Broad-use confirms — it's a grammatical role, not a standalone pattern.

## 417. `Switch` · Physics/Primitives · R0T1 (RETIRING per §3.9)

**Intended (at mint)**: contextual toggle — change active mode/context/flow.
**Future**: NOT applicable — retired.
**Why retired**: §3.3/§3.9 find Switch's mechanism too vacuous (covers what Branch + Route already do, and more). A handle with years of vacuous usage can't be reclaimed for a narrower meaning. §3.18's `_meta.supersedes` on `Route` redirects old references.

## 418. `SynergisticMode` · Society/Protocols · R0T2

**Intended**: protocol-level cognitive mode switching — broadcast "Generative vs Verifier" signal; downstream adjusts AcceptSpec strictness.
**Future**: any "switch system-wide mode" broadcast protocol.
**Broad-use contexts**: multi-agent training-mode switches (training vs eval), brainstorm-vs-review phases in teams, building-vs-testing phases in software, daytime-vs-night protocols.
**Every context needs**: mode signal broadcast, downstream AcceptSpec adjustment, synchronized mode entry/exit.
**Varies**: mode set, transition protocol, escalation on refusal-to-switch.
**Extension**: `TrainingEvalSynergisticMode`, `BuildTestSynergisticMode`, `GenReviewSynergisticMode`.

## 419. `Taper` · Society/Protocols · R1T1

**Intended**: progressive ambiguity collapse — multi-stage filter with increasing strictness.
**Future**: any "filter down from wide to narrow" pipeline.
**Broad-use contexts**: sema discovery pipeline, hiring pipelines, compiler passes, academic admission funnels, startup pitch review stages, journalistic fact-narrowing.
**Every context needs**: wide-aperture input, staged gates with increasing strictness, DepthGovernor-like functional role, progressive candidate reduction.
**Varies**: stage count, per-stage strictness curve, parallel-vs-sequential stages, cost-aware gate ordering.
**Extension**: `HiringTaper`, `CompilerTaper`, `DiscoveryTaper`.

## 420. `ThinSlice` · Mind/Reasoning · R2T3 (moving Society → Mind per §3.18)

**Intended**: high-confidence classification from tiny data sample — triage/routing without full processing.
**Future**: any "quick classification from minimal data" heuristic.
**Broad-use contexts**: file-type detection from magic bytes, first-impression classification in hiring, doctor "eyeball diagnosis" from patient presentation, Gladwell's "Blink" concept.
**Every context needs**: tiny sample extraction, high-confidence classifier, route-based-on-class semantic.
**Varies**: sample size, classifier confidence threshold, fallback to deeper processing.
**Extension**: `FileTypeThinSlice`, `MedicalThinSlice`, `TriageThinSlice`.

## 421. `ThreeLevelCollision` · Society/Protocols · R0T1

**Intended**: threat-modeling primitive distinguishing Stub / Hash / Homograph collisions, each with specific defense.
**Future**: any multi-class-collision threat model.
**Broad-use contexts**: content-addressed system threat analysis, cryptographic protocol design, namespace-management security, visual-identity-system design (logos, fonts).
**Every context needs**: three-class taxonomy (stub, hash, homograph), per-class defense, distinct threat semantics.
**Varies**: defense specifics, per-class probability estimates, domain specifics.
**Extension**: `ContentAddressedThreeLevelCollision`, `NamespaceThreeLevelCollision`, `VisualThreeLevelCollision`.

## 422. `TieredAccess` · Society/Protocols · R0T1

**Intended**: cost-distance indexing — interaction cost increases approaching gravity-well center.
**Future**: any "core attention expensive, periphery cheap" access structure.
**Broad-use contexts**: CEO-time pricing (expensive to reach), tiered-support models, stake-based governance access, reputation-based API pricing, VIP access systems.
**Every context needs**: gravity-well model with center vs periphery, cost-distance inverse proportionality, BearerToken integration.
**Varies**: cost function, tier count, reputation-vs-stake basis, escalation paths.
**Extension**: `CEOTieredAccess`, `GovernanceTieredAccess`, `ReputationTieredAccess`.

## 423. `TimeboxThink` · Mind/Strategy · R0T1 (moving Society → Mind per §3.18)

**Intended**: bounded exploration — hard time limit, stop regardless of completion.
**Future**: any "thinking timer" discipline.
**Broad-use contexts**: Pomodoro technique, meeting time-boxes, research-sprint timeboxing, test-taking timeboxes, decision-timeboxes.
**Every context needs**: hard time limit, stop-on-limit-hit, post-limit assessment, learning from what-was-accomplished.
**Varies**: duration (Duration per §3.17), extension rules, enforcement strictness.
**Extension**: `PomodoroTimeboxThink`, `MeetingTimeboxThink`, `ResearchTimeboxThink`.

## 424. `ToolDiscovery` · Society/Protocols · R1T1

**Intended**: discover and invoke external tools via structured capability manifests.
**Future**: any tool-lookup-and-invoke operation.
**Broad-use contexts**: MCP tool discovery, LangChain tool loading, LLM agent capability expansion, automated service composition, API marketplace discovery.
**Every context needs**: capability query, registry response with Cards, compatibility check, ToolInvoke.
**Varies**: registry topology, query language, caching, authentication.
**Extension**: `MCPToolDiscovery`, `LangChainToolDiscovery`, `FederatedToolDiscovery`.

## 425. `TraceBelief` · Mind/Memory · R2T2 (moving Society → Mind per §3.18)

**Intended**: belief provenance — Macro for Trace(Belief), chronological history of belief.
**Future**: any "here's how my belief evolved" audit pattern.
**Broad-use contexts**: epistemic version control, scientific hypothesis provenance, bug-hypothesis tracking, LLM answer-confidence history, audit-trail for decisions.
**Every context needs**: Belief instance, Trace primitive applied, silent-update prevention, citation of prior-belief-being-revised.
**Varies**: granularity of Belief nodes, compression of history, audit access.
**Extension**: `ScientificTraceBelief`, `DebuggingTraceBelief`, `AuditTraceBelief`.

## 426. `UniqueHandle` · Society/Protocols · R0T1

**Intended**: cryptographic pointer to singular rivalrous resource — Linear Logic (Transferred, not Copied).
**Future**: any non-copyable ownership token.
**Broad-use contexts**: NFT ownership, file-handle exclusive ownership, role-binding in organizations, unique-identifier transfer in legal contracts, Rust's ownership type system.
**Every context needs**: cryptographic pointer, Linear Logic semantic (transfer, not copy), sender-loses-on-transfer rule.
**Varies**: cryptographic scheme, revocation protocol, escrow handling.
**Extension**: `NFTUniqueHandle`, `FileUniqueHandle`, `RoleUniqueHandle`.

## 427. `Warmup` · Infrastructure/Primitives · R0T1 (moving Society → Infra per §3.18)

**Intended**: gradual capacity ramp — start reduced, increase to full over time.
**Future**: any cold-start ramp-up mechanism.
**Broad-use contexts**: service warmup on deployment, JIT compiler warmup, ML inference warmup (e.g., LLM first-token latency), exercise warmup, human cognitive warmup.
**Every context needs**: C_min starting capacity, C_max target, time T, ramp curve, thundering-herd prevention.
**Varies**: ramp curve, duration (Duration), capacity metric (QPS, throughput, compute).
**Extension**: `ServiceWarmup`, `JITWarmup`, `MLInferenceWarmup`.

## 428. `WorkerMode` · Society/Protocols · R0T1

**Intended**: execution state machine — upon claiming a task, atomic identity switch via ContextSwitch using SolverManifest.
**Future**: any "become the persona for this task" mode-entry mechanism.
**Broad-use contexts**: professional roles (doctor-mode, judge-mode), agent-swarm specialist assignment, actor Method roles, chatbot persona switching, LLM role-playing contexts.
**Every context needs**: task claim, atomic identity switch, SolverManifest reference, mode-until-completion semantic.
**Varies**: switch atomicity, recursion (nested modes), context preservation across modes.
**Extension**: `ProfessionalWorkerMode`, `SwarmWorkerMode`, `PersonaWorkerMode`.

---

## Final observations

**All 427 patterns have been walked through the broad-use methodology.** The test (enumerate contexts → find intersection of needs → identify variation territory) produced actionable analyses for every pattern across every layer, category, tier, and ring.

**The audit's decisions held up uniformly under this scrutiny.** Every relocation (§3.2, §3.8, §3.18), retirement (§3.9, §3.18), trait-conversion (§3.18), rename (§3.14 SolverRoot→RootSolver), wiring (§3.5, §3.6, §3.20), and mechanism rewrite (§3.1, §3.4, §3.18, §3.19) validated when tested against the broad-use framework. Specific validations are in the batch-level observations.

**Net audit items surfaced during this analysis** (beyond what the main audit already captures): 66 items, numbered throughout. These ranged from small phrasing concerns to genuine improvements. The most important (Critique as Verb, Society→Mind additions for Proprioception/DeepResearch/RequestFraming, SolverRoot→RootSolver rename, FractalIntelligence paper-aligned definition) have been synced back into the main audit in real time. The remainder are tracked as follow-up items.

**The library at 429 patterns (post-audit)** has a clean broad-use story for every pattern. Each is either:
- A definitional foundation primitive (minimal mechanism, rich descendant space) — e.g. Gate, Lock, Trace, Observe, Think
- A structured noun with specific identity (usability floor captured in required fields) — e.g. Task, Score, Summary, Contract, Role
- A specialized heuristic/strategy at R2 (clear technique, explicit extension space) — e.g. Satisfice, BeamSearch, DissentSeek, PreMortem
- A coordination protocol requiring ≥2 agents (Society-layer) — e.g. Consensus, Rally, Handoff, Oracle
- A Trait (marker interface, not standalone pattern) — Meta, Global, Subject, Creative, Condition

**The methodology is now durable.** Every future mint should walk the six steps before specifying constraints. Every future audit should validate proposals against broad-use contexts. The library's ability to scale depends on this discipline — not on the specific decisions in this particular audit.

Total analyzed: 427 (the entire pre-audit library, 100%).

---

## Methodology failure modes (Gemini's final review)

Two failure modes to guard against when the methodology is applied by future minters:

**1. The Domain Overfitting Trap.** A minter imagines use-cases from only one paradigm and accidentally bakes domain-specific constraints into the foundation. Examples caught in this walk: `Lock` overfit to Mutex (K=1), `ExploreExploit` overfit to UCB (one algorithm), `Stigmergy` overfit to biological decay (one persistence scheme).

*Defense*: force the broad-use enumeration to span at least three orthogonal domains before deriving the intersection — typically biological + silicon + psychological/social, or math + engineering + organizational. If a proposed constraint only holds in one domain, it belongs on a descendant, not the foundation.

**2. The Semantic Homonym Trap (Empty Intersection).** Two domains use the same word for different causal structures (mathematical `Group` vs sociological `Group`; category-theoretic `Category` vs biological `Category`). Trying to find their intersection produces either a vacuous chimera or nothing at all.

*Defense*: Rule E's non-vacuous schema requirement is the self-correcting backstop. If the intersection of needs strips away all structural constraints and leaves only a vague gloss, the contexts don't share a causal structure. **Empty intersection = the pattern is an illusion and must be split or retired.** This is exactly what correctly forced `Group` and `Switch` into retirement in the main audit (§3.9): broad-use for each produced no non-vacuous intersection.

Both failure modes are detectable: domain overfitting produces an unusually restrictive floor (descendants would violate it); semantic homonyms produce an unusually loose floor (nothing to specify). The minter's discipline is watching for either symptom while walking the six steps.


