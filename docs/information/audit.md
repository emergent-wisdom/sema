# Vocabulary Audit Report

Generated: 2026-04-16

All audits below are **advisory**. Heuristic audits generate false positives; use this report as a starting point for manual review, not as a correctness gate.

## Hash validity (stored sema_id matches content)

Source: `scripts/audit/audit_hash_validity.py` (ok)

```text
Checking hash validity for 427 patterns...

All 427 hashes valid.
```

## Missing or short fields

Source: `scripts/audit/audit_missing_or_short.py` (ok)

```text
Auditing 427 patterns in data/vocabulary...
✅ No issues found.
```

## Graph structure (orphans, duplicates, naked patterns)

Source: `scripts/audit/audit_graph.py` (ok)

```text
Loading graph...
Graph loaded with 1670 nodes and 3111 edges.
Checking for orphaned patterns...
Checking for orphaned components...
Checking for missing metadata...
Checking for hierarchy cycles...
Checking for duplicate names...
Checking rigor...

Audit Complete. Found 80 problems.

[NO_CONTRACTS] Pattern 'Axiom' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Branch' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Category' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Creative' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Datum' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Global' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Hypothesis' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'InputGuard' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Meta' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'MonitorReport' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Option' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Parallel' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Prompt' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Protocol' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Prototype' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Sandbox' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Sequence' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'System' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Topology' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Variable' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Vector' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Criteria' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Hierarchy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'FeatureFlag' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Anomaly' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'CognitiveBias' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Abduction' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Nature' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Correlation' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Identity' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Entropy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Incongruity' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Metric' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Snapshot' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Transition' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Value' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Causation' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Synthesis' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Event' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StateTransition' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Score' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Summary' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Discover' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ContextCompress' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StateAudit' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Actor' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Refine' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Subject' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Noise' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Problem' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Queue' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Understand' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ReversibilityCheck' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Dampen' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StateLock' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Solver' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Exception' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Belief' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Compromise' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Permission' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Outcome' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Roadmap' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Strategy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Jester' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'RuleSet' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'IdentityHandshake' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Switch' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Verification' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ContextSwitch' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Experiment' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'TreeOfThoughts' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'HypothesisEngine' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Role' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Deploy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Group' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Aesthetics' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'PURECheck' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'TraceBelief' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'RecursionDive' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StyleSpec' has no Invariants, Preconditions, or Postconditions.
```

## Rigor coverage (invariants / pre / post)

Source: `scripts/audit/audit_rigor.py` (ok)

```text
{
  "total": 427,
  "with_invariants": 346,
  "with_preconditions": 181,
  "with_postconditions": 171,
  "fully_rigorous": 170,
  "naked": 80
}

Sample 'Naked' Patterns (No strict logic):
- Axiom
- Branch
- Category
- Creative
- Datum
- Global
- Hypothesis
- InputGuard
- Meta
- MonitorReport
- Option
- Parallel
- Prompt
- Protocol
- Prototype
```

## Potential missing dependency links

Source: `scripts/audit/audit_missing_links.py` (ok)

```text
🔍 Scanning data/vocabulary for missing links...
Loaded 427 patterns.

Found 300 potential missing links.

🔹 AcceptSpec
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Score' but not linked.
   ❓ Mentions 'Spec' but not linked.
🔹 Act
   ❓ Mentions 'Actor' but not linked.
   ❓ Mentions 'Result' but not linked.
🔹 AdversarialProof
   ❓ Mentions 'RedTeam' but not linked.
   ❓ Mentions 'Search' but not linked.
🔹 AdversarialSteel
   ❓ Mentions 'Proposal' but not linked.
🔹 Agent
   ❓ Mentions 'Goal' but not linked.
🔹 AgentSandbox
   ❓ Mentions 'Resource' but not linked.
🔹 Aggregate
   ❓ Mentions 'Mode' but not linked.
🔹 AtomicBid
   ❓ Mentions 'Bid' but not linked.
   ❓ Mentions 'Permission' but not linked.
🔹 AttentionMarkets
   ❓ Mentions 'Bid' but not linked.
   ❓ Mentions 'Queue' but not linked.
🔹 Audit
   ❓ Mentions 'Verification' but not linked.
🔹 Award
   ❓ Mentions 'Bid' but not linked.
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'HeldRelease' but not linked.
   ❓ Mentions 'Value' but not linked.
🔹 BackwardChain
   ❓ Mentions 'Goal' but not linked.
   ❓ Mentions 'Step' but not linked.
🔹 BaseRateInclude
   ❓ Mentions 'Probability' but not linked.
🔹 BeamSearch
   ❓ Mentions 'Constraint' but not linked.
🔹 BoundedTask
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Gate' but not linked.
🔹 Bubble
   ❓ Mentions 'Group' but not linked.
🔹 Budget
   ❓ Mentions 'Resource' but not linked.
🔹 Build
   ❓ Mentions 'ProtoPack' but not linked.
🔹 Cache
   ❓ Mentions 'Value' but not linked.
🔹 Care
   ❓ Mentions 'Entropy' but not linked.
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Work' but not linked.
🔹 CausalBarrier
   ❓ Mentions 'Event' but not linked.
🔹 ChainOfThought
   ❓ Mentions 'Chain' but not linked.
   ❓ Mentions 'Step' but not linked.
   ❓ Mentions 'Think' but not linked.
🔹 ChunkMerge
   ❓ Mentions 'Group' but not linked.
🔹 CognitiveEcho
   ❓ Mentions 'Feedback' but not linked.
🔹 CognitiveSolver
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 Combine
   ❓ Mentions 'Result' but not linked.
🔹 Compose
   ❓ Mentions 'DAG' but not linked.
🔹 Compromise
   ❓ Mentions 'Protocol' but not linked.
🔹 ComputeBudget
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Meta' but not linked.
   ❓ Mentions 'Risk' but not linked.
🔹 Condition
   ❓ Mentions 'Result' but not linked.
🔹 ConfusedDeputy
   ❓ Mentions 'Prompt' but not linked.
🔹 Consensus
   ❓ Mentions 'Group' but not linked.
🔹 Constraint
   ❓ Mentions 'Resource' but not linked.
🔹 Context
   ❓ Mentions 'Budget' but not linked.
🔹 Critique
   ❓ Mentions 'Feedback' but not linked.
🔹 Crystallize
   ❓ Mentions 'Entropy' but not linked.
🔹 Cyclic
   ❓ Mentions 'Condition' but not linked.
🔹 DataMinimization
   ❓ Mentions 'Goal' but not linked.
🔹 DeepResearch
   ❓ Mentions 'Plan' but not linked.
   ❓ Mentions 'Search' but not linked.
🔹 DeliberativeAlign
   ❓ Mentions 'Goal' but not linked.
🔹 DepthGovernor
   ❓ Mentions 'Entropy' but not linked.
🔹 DesignArchitect
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Dialectic' but not linked.
   ❓ Mentions 'MechanisticDesignProposal' but not linked.
   ❓ Mentions 'PreMortem' but not linked.
🔹 Dialectic
   ❓ Mentions 'Synthesis' but not linked.
🔹 Elect
   ❓ Mentions 'Result' but not linked.
🔹 Eliminate
   ❓ Mentions 'Falsification' but not linked.
   ❓ Mentions 'Search' but not linked.
🔹 EpistemicCalibrate
   ❓ Mentions 'Event' but not linked.
🔹 Estimate
   ❓ Mentions 'Meta' but not linked.
🔹 EvaluatorOptimizer
   ❓ Mentions 'Feedback' but not linked.
🔹 EventReact
   ❓ Mentions 'Event' but not linked.
🔹 ExecutionManifest
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Sequence' but not linked.
🔹 Falsification
   ❓ Mentions 'Hypothesis' but not linked.
🔹 Feedback
   ❓ Mentions 'Noise' but not linked.
🔹 FractalIntelligence
   ❓ Mentions 'Value' but not linked.
🔹 FrameSpec
   ❓ Mentions 'Constraint' but not linked.
🔹 Generalize
   ❓ Mentions 'Refine' but not linked.
🔹 Global
   ❓ Mentions 'System' but not linked.
🔹 Goal
   ❓ Mentions 'Result' but not linked.
🔹 Greet
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Protocol' but not linked.
🔹 Group
   ❓ Mentions 'Agent' but not linked.
🔹 HeldRelease
   ❓ Mentions 'Oracle' but not linked.
🔹 HypothesisEngine
   ❓ Mentions 'Result' but not linked.
🔹 Identity
   ❓ Mentions 'Role' but not linked.
🔹 Interpret
   ❓ Mentions 'Translate' but not linked.
🔹 Invert
   ❓ Mentions 'Solution' but not linked.
🔹 Judge
   ❓ Mentions 'Score' but not linked.
🔹 LatentAttachment
   ❓ Mentions 'Search' but not linked.
🔹 LateralOptimization
   ❓ Mentions 'Optimize' but not linked.
   ❓ Mentions 'Reframe' but not linked.
   ❓ Mentions 'Translate' but not linked.
🔹 LayeredCheck
   ❓ Mentions 'Hierarchy' but not linked.
🔹 Linear
   ❓ Mentions 'Chain' but not linked.
   ❓ Mentions 'Step' but not linked.
🔹 LocalizedLearning
   ❓ Mentions 'Feedback' but not linked.
🔹 Loop
   ❓ Mentions 'State' but not linked.
🔹 MECE
   ❓ Mentions 'Refine' but not linked.
🔹 ManifestPlanning
   ❓ Mentions 'Chain' but not linked.
   ❓ Mentions 'ExecutionManifest' but not linked.
   ❓ Mentions 'FrameSpec' but not linked.
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Step' but not linked.
🔹 MarginalValueRule
   ❓ Mentions 'Budget' but not linked.
🔹 MechanisticDesignProposal
   ❓ Mentions 'Dialectic' but not linked.
   ❓ Mentions 'Novelty' but not linked.
🔹 MemeticSeed
   ❓ Mentions 'Resource' but not linked.
🔹 MetaCheck
   ❓ Mentions 'Verification' but not linked.
🔹 Mutex
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Sequence' but not linked.
🔹 NegativeProof
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Search' but not linked.
   ❓ Mentions 'State' but not linked.
🔹 NormativeJudge
   ❓ Mentions 'Value' but not linked.
🔹 OODA
   ❓ Mentions 'Act' but not linked.
   ❓ Mentions 'Cyclic' but not linked.
   ❓ Mentions 'Observe' but not linked.
🔹 Observe
   ❓ Mentions 'Actor' but not linked.
   ❓ Mentions 'State' but not linked.
🔹 OpportunityCost
   ❓ Mentions 'Resource' but not linked.
🔹 OptimalStop
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Search' but not linked.
🔹 OptimisticSolver
   ❓ Mentions 'Actor' but not linked.
   ❓ Mentions 'Message' but not linked.
   ❓ Mentions 'Parallel' but not linked.
   ❓ Mentions 'Reason' but not linked.
   ❓ Mentions 'Solution' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 OrchestrationLoop
   ❓ Mentions 'AcceptSpec' but not linked.
   ❓ Mentions 'Artifact' but not linked.
   ❓ Mentions 'Interpret' but not linked.
   ❓ Mentions 'Loop' but not linked.
   ❓ Mentions 'Plan' but not linked.
   ❓ Mentions 'Problem' but not linked.
   ❓ Mentions 'Rollout' but not linked.
   ❓ Mentions 'Solution' but not linked.
🔹 OsmoticFilter
   ❓ Mentions 'Queue' but not linked.
🔹 OutputGuard
   ❓ Mentions 'Score' but not linked.
🔹 PUREBrainstorming
   ❓ Mentions 'Check' but not linked.
   ❓ Mentions 'MechanisticDesignProposal' but not linked.
   ❓ Mentions 'Optimize' but not linked.
   ❓ Mentions 'PURECheck' but not linked.
   ❓ Mentions 'Proposal' but not linked.
🔹 PURECheck
   ❓ Mentions 'Expansive' but not linked.
   ❓ Mentions 'Protocol' but not linked.
   ❓ Mentions 'Realizable' but not linked.
🔹 PUREOptimization
   ❓ Mentions 'Parsimony' but not linked.
   ❓ Mentions 'Realizable' but not linked.
   ❓ Mentions 'Synthesis' but not linked.
🔹 ParetoFront
   ❓ Mentions 'ExchangeRate' but not linked.
   ❓ Mentions 'Metric' but not linked.
🔹 PatternDiscovery
   ❓ Mentions 'Search' but not linked.
🔹 PermissionEscalate
   ❓ Mentions 'Risk' but not linked.
🔹 PerspectiveEnsemble
   ❓ Mentions 'Mode' but not linked.
   ❓ Mentions 'Role' but not linked.
🔹 PhasedRefinement
   ❓ Mentions 'Artifact' but not linked.
🔹 PreMortem
   ❓ Mentions 'Probability' but not linked.
🔹 Prioritize
   ❓ Mentions 'Score' but not linked.
🔹 Probe
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Sandbox' but not linked.
   ❓ Mentions 'Verification' but not linked.
🔹 ProblemFramer
   ❓ Mentions 'Problem' but not linked.
   ❓ Mentions 'Reframe' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 PromiseGraph
   ❓ Mentions 'DAG' but not linked.
   ❓ Mentions 'Verification' but not linked.
🔹 PromptChain
   ❓ Mentions 'Step' but not linked.
🔹 ProphetFanOut
   ❓ Mentions 'Entropy' but not linked.
🔹 ProtoPack
   ❓ Mentions 'Prototype' but not linked.
🔹 Protocol
   ❓ Mentions 'Spec' but not linked.
🔹 Quorum
   ❓ Mentions 'Proposal' but not linked.
   ❓ Mentions 'Result' but not linked.
🔹 Rally
   ❓ Mentions 'Group' but not linked.
🔹 Rank
   ❓ Mentions 'Score' but not linked.
🔹 ReAct
   ❓ Mentions 'Goal' but not linked.
🔹 Realizable
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Uncertain' but not linked.
🔹 RealizationProtocol
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Artifact' but not linked.
   ❓ Mentions 'Interpret' but not linked.
   ❓ Mentions 'Loop' but not linked.
   ❓ Mentions 'Plan' but not linked.
   ❓ Mentions 'Realizable' but not linked.
   ❓ Mentions 'Rollout' but not linked.
🔹 RecursiveRootCause
   ❓ Mentions 'Chain' but not linked.
   ❓ Mentions 'Step' but not linked.
🔹 RedTeam
   ❓ Mentions 'Goal' but not linked.
🔹 RegimeSense
   ❓ Mentions 'Score' but not linked.
🔹 RequestFraming
   ❓ Mentions 'FrameSpec' but not linked.
🔹 Resonate
   ❓ Mentions 'Feedback' but not linked.
🔹 Resource
   ❓ Mentions 'Identity' but not linked.
🔹 Result
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 Reversibility
   ❓ Mentions 'Condition' but not linked.
   ❓ Mentions 'Entropy' but not linked.
🔹 ReversibilityCheck
   ❓ Mentions 'Audit' but not linked.
   ❓ Mentions 'Check' but not linked.
   ❓ Mentions 'Reversibility' but not linked.
🔹 RigorousSolver
   ❓ Mentions 'System' but not linked.
   ❓ Mentions 'Verification' but not linked.
🔹 Risk
   ❓ Mentions 'Probability' but not linked.
🔹 Rollout
   ❓ Mentions 'Compensate' but not linked.
🔹 RolloutWatch
   ❓ Mentions 'MonitorReport' but not linked.
   ❓ Mentions 'Rollout' but not linked.
🔹 Sandbox
   ❓ Mentions 'Resource' but not linked.
🔹 ScopeFreeze
   ❓ Mentions 'Goal' but not linked.
   ❓ Mentions 'Lock' but not linked.
🔹 ScoringFunction
   ❓ Mentions 'Score' but not linked.
🔹 Select
   ❓ Mentions 'Result' but not linked.
🔹 SelfConsistency
   ❓ Mentions 'Mode' but not linked.
🔹 SemanticTabu
   ❓ Mentions 'Constraint' but not linked.
🔹 Shard
   ❓ Mentions 'Decompose' but not linked.
   ❓ Mentions 'Resource' but not linked.
🔹 Skeleton
   ❓ Mentions 'Parallel' but not linked.
🔹 SkeletonOfThought
   ❓ Mentions 'Parallel' but not linked.
   ❓ Mentions 'Skeleton' but not linked.
   ❓ Mentions 'Think' but not linked.
🔹 SolverManifest
   ❓ Mentions 'Constraint' but not linked.
   ❓ Mentions 'Identity' but not linked.
   ❓ Mentions 'Lock' but not linked.
🔹 SolverNode
   ❓ Mentions 'Budget' but not linked.
🔹 SolverRoot
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Problem' but not linked.
   ❓ Mentions 'Reframe' but not linked.
   ❓ Mentions 'Responsibility' but not linked.
🔹 SolverTree
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Chain' but not linked.
   ❓ Mentions 'DAG' but not linked.
🔹 SomaticMarker
   ❓ Mentions 'Probability' but not linked.
   ❓ Mentions 'Score' but not linked.
   ❓ Mentions 'System' but not linked.
🔹 SourceEvaluate
   ❓ Mentions 'Assessment' but not linked.
🔹 Specialize
   ❓ Mentions 'Constraint' but not linked.
🔹 State
   ❓ Mentions 'System' but not linked.
🔹 StateTransition
   ❓ Mentions 'Event' but not linked.
   ❓ Mentions 'State' but not linked.
🔹 SteelmanCheck
   ❓ Mentions 'Score' but not linked.
🔹 SteelmanFirst
   ❓ Mentions 'Proposal' but not linked.
🔹 StrategicReading
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Linear' but not linked.
🔹 SurvivorCorrect
   ❓ Mentions 'Estimate' but not linked.
🔹 SynergisticMode
   ❓ Mentions 'Protocol' but not linked.
🔹 TaskLifecycle
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Heartbeat' but not linked.
   ❓ Mentions 'State' but not linked.
🔹 TensionHold
   ❓ Mentions 'Falsification' but not linked.
   ❓ Mentions 'Tension' but not linked.
🔹 Throttle
   ❓ Mentions 'Queue' but not linked.
🔹 TieredAccess
   ❓ Mentions 'Metric' but not linked.
🔹 TimeboxThink
   ❓ Mentions 'Result' but not linked.
🔹 ToolDiscovery
   ❓ Mentions 'Discover' but not linked.
   ❓ Mentions 'Protocol' but not linked.
   ❓ Mentions 'Verification' but not linked.
🔹 ToolInvoke
   ❓ Mentions 'Actor' but not linked.
   ❓ Mentions 'Result' but not linked.
🔹 Topology
   ❓ Mentions 'Cyclic' but not linked.
   ❓ Mentions 'DAG' but not linked.
   ❓ Mentions 'Linear' but not linked.
   ❓ Mentions 'Tree' but not linked.
🔹 Trace
   ❓ Mentions 'Feedback' but not linked.
🔹 TraceBelief
   ❓ Mentions 'Belief' but not linked.
🔹 Transition
   ❓ Mentions 'State' but not linked.
🔹 Translate
   ❓ Mentions 'Summarize' but not linked.
🔹 TranslationProxy
   ❓ Mentions 'Protocol' but not linked.
🔹 TreeOfThoughts
   ❓ Mentions 'Think' but not linked.
   ❓ Mentions 'Tree' but not linked.
🔹 TriGate
   ❓ Mentions 'Ledger' but not linked.
🔹 Understand
   ❓ Mentions 'Deep' but not linked.
🔹 UniqueHandle
   ❓ Mentions 'Linear' but not linked.
   ❓ Mentions 'Resource' but not linked.
🔹 UniversalSolverTree
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Tree' but not linked.
🔹 UptakeAsGround
   ❓ Mentions 'Verification' but not linked.
🔹 Validate
   ❓ Mentions 'Gate' but not linked.
   ❓ Mentions 'Judge' but not linked.
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Verification' but not linked.
🔹 WhyClimb
   ❓ Mentions 'Entropy' but not linked.
🔹 Work
   ❓ Mentions 'Goal' but not linked.
🔹 Workflow
   ❓ Mentions 'Artifact' but not linked.
   ❓ Mentions 'Step' but not linked.
🔹 Yield
   ❓ Mentions 'Ledger' but not linked.
```

## Unlinked handle mentions

Source: `scripts/audit/audit_unlinked_mentions.py` (ok)

```text
Scanning 427 patterns for unlinked handle mentions...

⚠️  AbductiveLeap:
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AcceptSpec:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compensate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Spec' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Act:
   • Mentions 'Actor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Permission' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Actor:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AdversarialProof:
   • Mentions 'RedTeam' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AdversarialSteel:
   • Mentions 'Compromise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Aesthetics:
   • Mentions 'Optimize' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AgentDiscover:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Discover' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AgentSandbox:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Aggregate:
   • Mentions 'Compress' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AmbiguityResolution:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AnalogyBridge:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AnchorDrop:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AntifragileInversion:
   • Mentions 'Sign' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Artifact:
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Workflow' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Assessment:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Critique' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reflexion' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AtomicBid:
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Bid' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Permission' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AttentionMarkets:
   • Mentions 'Bid' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Message' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Queue' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AuditTrail:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Award:
   • Mentions 'Lock' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Axiom:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Backoff:
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BackwardChain:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Ballot:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Proposal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BaseRateInclude:
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BayesUpdate:
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BeamSearch:
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BearerToken:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Delegate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Belief:
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BeliefTracking:
   • Mentions 'Belief' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Bid:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  BreadthGovernor:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Break:
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Bubble:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sandbox' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Simulation' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Snapshot' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Build:
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Prototype' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Canary:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CapacityPressure:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compress' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Card:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Greet' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Category:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CausalBarrier:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Queue' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Causation:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Chain:
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ChainOfThought:
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Check:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ChunkMerge:
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CircuitBreaker:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CiteBack:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CognitiveEcho:
   • Mentions 'Decompose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Simulation' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CognitiveSolver:
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CommitmentDevice:
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CompatibilityCheck:
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Compensate:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Assumption' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Compose:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Compromise:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ComputeBudget:
   • Mentions 'Deep' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Estimate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Ledger' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConceptAnchor:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Condition:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConfidenceCalibrate:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConfirmationBlock:
   • Mentions 'Belief' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConfusedDeputy:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Permission' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Prompt' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Consensus:
   • Mentions 'Actor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConsensusFinder:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vote' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Constitution:
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Constraint:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Nature' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConstraintFirst:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Creative' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ConstructOntology:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Context:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ContextFirst:
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ContextSwitch:
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'RuleSet' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ContingencyPlan:
   • Mentions 'Assumption' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ContinuousResourceAuction:
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Cooldown:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Creative:
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Criteria:
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Critique:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Crystallize:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Lock' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  CurriculumReplay:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Cyclic:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Refine' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Dampen:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DataMinimization:
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Decision:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Assumption' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Decompose:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Yield' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Deep:
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DeepResearch:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decompose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Refine' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Synthesis' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Defer:
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Queue' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Delegate:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Message' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Deploy:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DepthGovernor:
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DesignArchitect:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Refine' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Dialectic:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Disband:
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Quorum' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vote' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Discover:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DissentSeek:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Robustness' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DogfoodFirst:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Workflow' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DriftWatch:
   • Mentions 'Anomaly' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EbbFlowSync:
   • Mentions 'Dampen' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Lock' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EjectionSeat:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Heartbeat' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Switch' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Elect:
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Cooldown' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Disband' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vote' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Eliminate:
   • Mentions 'Falsification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EmpathySim:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Simulation' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EntropyPump:
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EpistemicCalibrate:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EpistemicROI:
   • Mentions 'Experiment' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Estimate:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EvaluatorOptimizer:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EventReact:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Exception:
   • Mentions 'Anomaly' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ExecutionManifest:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Build' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Rollout' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Expansive:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ExperienceSharding:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Experiment:
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ExpiringToken:
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ExploreExploit:
   • Mentions 'Estimate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Option' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ExtendedThinking:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Think' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FailClosed:
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Falsification:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FeatureFlag:
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Feedback:
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FeedbackSignal:
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Fermi:
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FirstPrinciples:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FractalIntelligence:
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Optimize' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FrameSpec:
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Gardener:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Gate:
   • Mentions 'Message' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  GenealogicalTrace:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Generalize:
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Refine' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Global:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Goal:
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  GracefulDegradation:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Greet:
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Group:
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HackDetect:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Handoff:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HeldRelease:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Oracle' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HeuristicSnap:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HindsightBlock:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HolographicShard:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Shard' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HumanApprove:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Assessment' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Hypothesis:
   • Mentions 'Falsification' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HypothesisEngine:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Falsification' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
⚠️  HypothesisLadder:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Hysteresis:
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Switch' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  IdempotentWrite:
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Identity:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
⚠️  IdentityHandshake:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Switch' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  InputGuard:
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
⚠️  IntentGap:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Interpret:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Translate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Invert:
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Jester:
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Kairos:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LatentAttachment:
   • Mentions 'Card' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vector' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LatentWander:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Discover' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LateralOptimization:
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LatticeCommit:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LayeredCheck:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LazyConsensus:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LeastToMost:
   • Mentions 'Build' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Linear:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LivedProof:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  LocalizedLearning:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Lock:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Loop:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MECE:
   • Mentions 'Category' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Overlap' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Refine' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ManifestPlanning:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Workflow' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MarginalValueRule:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Deep' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MechanisticDesignProposal:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Dialectic' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Proposal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MentalSim:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Simulation' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MetaCheck:
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Critique' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MetaPrompt:
   • Mentions 'Critique' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Generalize' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Prompt' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Refine' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Metric:
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MintWhenFriction:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Mode:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Monitor:
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MonitorReport:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  MonotonicCounter:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Mutex:
   • Mentions 'Heartbeat' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Queue' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Yield' (unlinked). Should it be '{{{ghost}}}'?
⚠️  NegativeProof:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Datum' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Snapshot' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  NormativeJudge:
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Novelty:
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Nucleate:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Heartbeat' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Stigmergy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OODA:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Observe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OathBind:
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Observe:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OntologyAdapt:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OpportunityCost:
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OptimalStop:
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OptimisticSolver:
   • Mentions 'Actor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Permission' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Optimize:
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Option:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Oracle:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OrchestrationLoop:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Rollout' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OsmoticFilter:
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tension' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Outcome:
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OutputGuard:
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Overlap:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Select' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PUREBrainstorming:
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PURECheck:
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PUREOptimization:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Realizable' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Synthesis' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Parallelize:
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ParetoFront:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'TradeOff' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PatternDiscovery:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Permission:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PermissionEscalate:
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PerspectiveEnsemble:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PhasedRefinement:
   • Mentions 'Deep' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Plan:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PreMortem:
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Prioritize:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Probability:
   • Mentions 'Assessment' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Belief' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Probe:
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sandbox' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Problem:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ProblemFramer:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reframe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ProblemSpace:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PromiseGraph:
   • Mentions 'DAG' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PromptChain:
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ProphetFanOut:
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PropheticQuorum:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vote' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Proposal:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Proprioception:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ProtoPack:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Simulation' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Protocol:
   • Mentions 'Spec' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Prototype:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Queue:
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
⚠️  QuorumPulse:
   • Mentions 'Quorum' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Rally:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Rank:
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ReAct:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Realizable:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Uncertain' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RealizationProtocol:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Spec' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Reason:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RecursionDive:
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RecursiveRootCause:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RedTeam:
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Refine:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Reflexion:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Critique' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Reframe:
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Invert' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RegimeSense:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Anomaly' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RegretMinimization:
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RepresentationSwap:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RequestFraming:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Workflow' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Resonate:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Resource:
   • Mentions 'Mutex' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Responsibility:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Monitor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Result:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RetrievalAugment:
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vector' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Retry:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Backoff' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compensate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Stream' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Reversibility:
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ReversibilityCheck:
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RigorousSolver:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Risk:
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Roadmap:
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Robustness:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Role:
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Switch' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Rollout:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compensate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RolloutWatch:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Workflow' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RootHashGossip:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SacrificialProbe:
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Sandbox:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vector' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Satisfice:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Option' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ScopeFreeze:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Score:
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ScoringFunction:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Scratchpad:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Select:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SelfConsistency:
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SelfReminder:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Prompt' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SemanticTabu:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Shard:
   • Mentions 'Decompose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ShoutWhisper:
   • Mentions 'Discover' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Switch' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Sign:
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Silence:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SimulationTrace:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Scratchpad' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Skeleton:
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SkeletonOfThought:
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Snapshot:
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SocraticLoop:
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Solution:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Solver:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SolverManifest:
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SolverNode:
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SolverRoot:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reframe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SolverTree:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hierarchy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SomaticMarker:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SourceEvaluate:
   • Mentions 'Assessment' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Spec:
   • Mentions 'Build' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Specialize:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Understand' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SpectralTune:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Message' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resonate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SpotAudit:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StateAudit:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StateLock:
   • Mentions 'Lock' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StateSnapshot:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StateTransition:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SteelmanCheck:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SteelmanFirst:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Critique' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StepBack:
   • Mentions 'Category' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Stigmergy:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StrategicReading:
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Strategy:
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Stream:
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StructuralCoaching:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Proposal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  StyleSpec:
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Spec' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SunkCostIgnore:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SurprisalUpdate:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SurvivorCorrect:
   • Mentions 'Estimate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SynergisticMode:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Taper:
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Optimize' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TaskLifecycle:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Heartbeat' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Queue' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TensionHold:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tension' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Think:
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ThreeLevelCollision:
   • Mentions 'Actor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Throttle:
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TieredAccess:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TimeWarpLog:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ToolDiscovery:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ToolInvoke:
   • Mentions 'Actor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Topology:
   • Mentions 'Cyclic' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'DAG' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Trace:
   • Mentions 'Actor' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Interpret' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TraceBelief:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Belief' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Translate:
   • Mentions 'Summarize' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TranslationProxy:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TreeOfThoughts:
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Uncertain:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UncertaintyMap:
   • Mentions 'Estimate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UniqueHandle:
   • Mentions 'Linear' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Variable' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UniversalSolverTree:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UptakeAsGround:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Group' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UptakeOverTimestamp:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Validate:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Value:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ValuePeg:
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Variable:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Verification:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Spec' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Vote:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Message' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Rally' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Warmup:
   • Mentions 'Cache' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  WhyClimb:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hierarchy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Work:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  WorkerMode:
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Workflow:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
⚠️  WorldReversible:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  WorldTransparent:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Yield:
   • Mentions 'Ledger' (unlinked). Should it be '{{{ghost}}}'?

Scan complete. Found unlinked handle mentions in 343 patterns.
```

## Semantic similarity between patterns

Source: `scripts/audit/audit_similarity.py` (ok)

```text
🔍 Computing pairwise similarities to find missing SIMILAR_TO links...
Loaded 0 patterns with embeddings.

Found 0 pairs with High Similarity (> 0.75) but NO link.
```

## Scenario coverage

Source: `scripts/audit/audit_scenarios.py` (ok)

```text
Auditing 0 scenarios...
No scenarios have multiple solutions (1:1 mapping currently).
```
