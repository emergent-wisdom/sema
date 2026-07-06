# Vocabulary Audit Report

Generated: 2026-07-06

All audits below are **advisory**. Heuristic audits generate false positives; use this report as a starting point for manual review, not as a correctness gate.

## Hash validity (stored sema_id matches content)

Source: `scripts/audit/audit_hash_validity.py` (ok)

```text
Checking hash validity for 452 patterns...

All 452 hashes valid.
```

## Missing or short fields

Source: `scripts/audit/audit_missing_or_short.py` (ok)

```text
Auditing 452 patterns in data/vocabulary...
⚠️  Abduction (Abduction.json)
   Missing: _meta.layer, _meta.category

⚠️  AcceptSpec (AcceptSpec.json)
   Missing: _meta.layer, _meta.category

⚠️  Act (Act.json)
   Missing: _meta.layer, _meta.category

⚠️  Actor (Actor.json)
   Missing: _meta.layer, _meta.category

⚠️  AdversarialProof (AdversarialProof.json)
   Missing: _meta.layer, _meta.category

⚠️  AdversarialSteel (AdversarialSteel.json)
   Missing: _meta.layer, _meta.category

⚠️  Aesthetics (Aesthetics.json)
   Missing: _meta.layer, _meta.category

⚠️  Agent (Agent.json)
   Missing: _meta.layer, _meta.category

⚠️  AgentDiscover (AgentDiscover.json)
   Missing: _meta.layer, _meta.category

⚠️  AgentProtocol (AgentProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  AgentSandbox (AgentSandbox.json)
   Missing: _meta.layer, _meta.category

⚠️  Aggregate (Aggregate.json)
   Missing: _meta.layer, _meta.category

⚠️  AmbiguityResolution (AmbiguityResolution.json)
   Missing: _meta.layer, _meta.category

⚠️  AnalogyBridge (AnalogyBridge.json)
   Missing: _meta.layer, _meta.category

⚠️  AnchorDrop (AnchorDrop.json)
   Missing: _meta.layer, _meta.category

⚠️  Anomaly (Anomaly.json)
   Missing: _meta.layer, _meta.category

⚠️  AntifragileInversion (AntifragileInversion.json)
   Missing: _meta.layer, _meta.category

⚠️  Artifact (Artifact.json)
   Missing: _meta.layer, _meta.category

⚠️  Assessment (Assessment.json)
   Missing: _meta.layer, _meta.category

⚠️  Assumption (Assumption.json)
   Missing: _meta.layer, _meta.category

⚠️  AtomicBid (AtomicBid.json)
   Missing: _meta.layer, _meta.category

⚠️  AttentionMarkets (AttentionMarkets.json)
   Missing: _meta.layer, _meta.category

⚠️  Attractor (Attractor.json)
   Missing: _meta.layer, _meta.category

⚠️  Audit (Audit.json)
   Missing: _meta.layer, _meta.category

⚠️  AuditTrail (AuditTrail.json)
   Missing: _meta.layer, _meta.category

⚠️  Award (Award.json)
   Missing: _meta.layer, _meta.category

⚠️  Axiom (Axiom.json)
   Missing: _meta.layer, _meta.category

⚠️  Backoff (Backoff.json)
   Missing: _meta.layer, _meta.category

⚠️  BackwardChain (BackwardChain.json)
   Missing: _meta.layer, _meta.category

⚠️  Ballot (Ballot.json)
   Missing: _meta.layer, _meta.category

⚠️  BaseRateInclude (BaseRateInclude.json)
   Missing: _meta.layer, _meta.category

⚠️  BayesUpdate (BayesUpdate.json)
   Missing: _meta.layer, _meta.category

⚠️  BeamSearch (BeamSearch.json)
   Missing: _meta.layer, _meta.category

⚠️  BearerToken (BearerToken.json)
   Missing: _meta.layer, _meta.category

⚠️  Belief (Belief.json)
   Missing: _meta.layer, _meta.category

⚠️  BeliefTracking (BeliefTracking.json)
   Missing: _meta.layer, _meta.category

⚠️  Bid (Bid.json)
   Missing: _meta.layer, _meta.category

⚠️  Bisect (Bisect.json)
   Missing: _meta.layer, _meta.category

⚠️  Boolean (Boolean.json)
   Missing: _meta.layer, _meta.category

⚠️  BoundedTask (BoundedTask.json)
   Missing: _meta.layer, _meta.category

⚠️  Branch (Branch.json)
   Missing: _meta.layer, _meta.category

⚠️  BreadthGovernor (BreadthGovernor.json)
   Missing: _meta.layer, _meta.category

⚠️  Break (Break.json)
   Missing: _meta.layer, _meta.category

⚠️  Bubble (Bubble.json)
   Missing: _meta.layer, _meta.category

⚠️  Budget (Budget.json)
   Missing: _meta.layer, _meta.category

⚠️  Build (Build.json)
   Missing: _meta.layer, _meta.category

⚠️  Cache (Cache.json)
   Missing: _meta.layer, _meta.category

⚠️  Canary (Canary.json)
   Missing: _meta.layer, _meta.category

⚠️  CapacityPressure (CapacityPressure.json)
   Missing: _meta.layer, _meta.category

⚠️  Card (Card.json)
   Missing: _meta.layer, _meta.category

⚠️  Care (Care.json)
   Missing: _meta.layer, _meta.category

⚠️  Category (Category.json)
   Missing: _meta.layer, _meta.category

⚠️  CausalBarrier (CausalBarrier.json)
   Missing: _meta.layer, _meta.category

⚠️  Causation (Causation.json)
   Missing: _meta.layer, _meta.category

⚠️  Chain (Chain.json)
   Missing: _meta.layer, _meta.category

⚠️  ChainOfThought (ChainOfThought.json)
   Missing: _meta.layer, _meta.category

⚠️  Check (Check.json)
   Missing: _meta.layer, _meta.category

⚠️  ChunkMerge (ChunkMerge.json)
   Missing: _meta.layer, _meta.category

⚠️  CircuitBreaker (CircuitBreaker.json)
   Missing: _meta.layer, _meta.category

⚠️  CiteBack (CiteBack.json)
   Missing: _meta.layer, _meta.category

⚠️  CognitiveBias (CognitiveBias.json)
   Missing: _meta.layer, _meta.category

⚠️  CognitiveEcho (CognitiveEcho.json)
   Missing: _meta.layer, _meta.category

⚠️  CollaborativeWritingProtocol (CollaborativeWritingProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  Combine (Combine.json)
   Missing: _meta.layer, _meta.category

⚠️  CommitmentDevice (CommitmentDevice.json)
   Missing: _meta.layer, _meta.category

⚠️  Compare (Compare.json)
   Missing: _meta.layer, _meta.category

⚠️  CompatibilityCheck (CompatibilityCheck.json)
   Missing: _meta.layer, _meta.category

⚠️  Compensate (Compensate.json)
   Missing: _meta.layer, _meta.category

⚠️  Compose (Compose.json)
   Missing: _meta.layer, _meta.category

⚠️  Compress (Compress.json)
   Missing: _meta.layer, _meta.category

⚠️  Compromise (Compromise.json)
   Missing: _meta.layer, _meta.category

⚠️  ComputeBudget (ComputeBudget.json)
   Missing: _meta.layer, _meta.category

⚠️  ConceptAnchor (ConceptAnchor.json)
   Missing: _meta.layer, _meta.category

⚠️  ConceptBlend (ConceptBlend.json)
   Missing: _meta.layer, _meta.category

⚠️  ConceptualDecomposition (ConceptualDecomposition.json)
   Missing: _meta.layer, _meta.category

⚠️  Condition (Condition.json)
   Missing: _meta.layer, _meta.category

⚠️  ConfidenceCalibrate (ConfidenceCalibrate.json)
   Missing: _meta.layer, _meta.category

⚠️  ConfirmationBlock (ConfirmationBlock.json)
   Missing: _meta.layer, _meta.category

⚠️  ConfusedDeputy (ConfusedDeputy.json)
   Missing: _meta.layer, _meta.category

⚠️  Consensus (Consensus.json)
   Missing: _meta.layer, _meta.category

⚠️  ConsensusFinder (ConsensusFinder.json)
   Missing: _meta.layer, _meta.category

⚠️  Conservation (Conservation.json)
   Missing: _meta.layer, _meta.category

⚠️  Constitution (Constitution.json)
   Missing: _meta.layer, _meta.category

⚠️  Constraint (Constraint.json)
   Missing: _meta.layer, _meta.category

⚠️  ConstraintFirst (ConstraintFirst.json)
   Missing: _meta.layer, _meta.category

⚠️  ConstructOntology (ConstructOntology.json)
   Missing: _meta.layer, _meta.category

⚠️  Context (Context.json)
   Missing: _meta.layer, _meta.category

⚠️  ContextCompress (ContextCompress.json)
   Missing: _meta.layer, _meta.category

⚠️  ContextFirst (ContextFirst.json)
   Missing: _meta.layer, _meta.category

⚠️  ContextSwitch (ContextSwitch.json)
   Missing: _meta.layer, _meta.category

⚠️  ContingencyPlan (ContingencyPlan.json)
   Missing: _meta.layer, _meta.category

⚠️  ContinuousResourceAuction (ContinuousResourceAuction.json)
   Missing: _meta.layer, _meta.category

⚠️  Contract (Contract.json)
   Missing: _meta.layer, _meta.category

⚠️  Cooldown (Cooldown.json)
   Missing: _meta.layer, _meta.category

⚠️  Correlation (Correlation.json)
   Missing: _meta.layer, _meta.category

⚠️  CounterfactualAnchor (CounterfactualAnchor.json)
   Missing: _meta.layer, _meta.category

⚠️  Creative (Creative.json)
   Missing: _meta.layer, _meta.category

⚠️  CreativeBlend (CreativeBlend.json)
   Missing: _meta.layer, _meta.category

⚠️  Criteria (Criteria.json)
   Missing: _meta.layer, _meta.category

⚠️  Critique (Critique.json)
   Missing: _meta.layer, _meta.category

⚠️  Crystallize (Crystallize.json)
   Missing: _meta.layer, _meta.category

⚠️  CurriculumReplay (CurriculumReplay.json)
   Missing: _meta.layer, _meta.category

⚠️  Cyclic (Cyclic.json)
   Missing: _meta.layer, _meta.category

⚠️  DAG (DAG.json)
   Missing: _meta.layer, _meta.category

⚠️  Dampen (Dampen.json)
   Missing: _meta.layer, _meta.category

⚠️  DataMinimization (DataMinimization.json)
   Missing: _meta.layer, _meta.category

⚠️  Datum (Datum.json)
   Missing: _meta.layer, _meta.category

⚠️  Decay (Decay.json)
   Missing: _meta.layer, _meta.category

⚠️  Decision (Decision.json)
   Missing: _meta.layer, _meta.category

⚠️  Decompose (Decompose.json)
   Missing: _meta.layer, _meta.category

⚠️  DecompositionGate (DecompositionGate.json)
   Missing: _meta.layer, _meta.category

⚠️  Deduction (Deduction.json)
   Missing: _meta.layer, _meta.category

⚠️  Deep (Deep.json)
   Missing: _meta.layer, _meta.category

⚠️  DeepResearch (DeepResearch.json)
   Missing: _meta.layer, _meta.category

⚠️  Defer (Defer.json)
   Missing: _meta.layer, _meta.category

⚠️  Delegate (Delegate.json)
   Missing: _meta.layer, _meta.category

⚠️  DeliberativeAlign (DeliberativeAlign.json)
   Missing: _meta.layer, _meta.category

⚠️  Deploy (Deploy.json)
   Missing: _meta.layer, _meta.category

⚠️  DepthGovernor (DepthGovernor.json)
   Missing: _meta.layer, _meta.category

⚠️  DesignArchitect (DesignArchitect.json)
   Missing: _meta.layer, _meta.category

⚠️  Dialectic (Dialectic.json)
   Missing: _meta.layer, _meta.category

⚠️  Disband (Disband.json)
   Missing: _meta.layer, _meta.category

⚠️  Discover (Discover.json)
   Missing: _meta.layer, _meta.category

⚠️  DiscoveryProtocol (DiscoveryProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  DissentSeek (DissentSeek.json)
   Missing: _meta.layer, _meta.category

⚠️  Distance (Distance.json)
   Missing: _meta.layer, _meta.category

⚠️  DocumentedOverride (DocumentedOverride.json)
   Missing: _meta.layer, _meta.category

⚠️  DogfoodFirst (DogfoodFirst.json)
   Missing: _meta.layer, _meta.category

⚠️  DriftWatch (DriftWatch.json)
   Missing: _meta.layer, _meta.category

⚠️  EbbFlowSync (EbbFlowSync.json)
   Missing: _meta.layer, _meta.category

⚠️  EjectionSeat (EjectionSeat.json)
   Missing: _meta.layer, _meta.category

⚠️  Elect (Elect.json)
   Missing: _meta.layer, _meta.category

⚠️  Eliminate (Eliminate.json)
   Missing: _meta.layer, _meta.category

⚠️  EmpathySim (EmpathySim.json)
   Missing: _meta.layer, _meta.category

⚠️  EmpiricalTest (EmpiricalTest.json)
   Missing: _meta.layer, _meta.category

⚠️  Entropy (Entropy.json)
   Missing: _meta.layer, _meta.category

⚠️  EntropyPump (EntropyPump.json)
   Missing: _meta.layer, _meta.category

⚠️  EpistemicCalibrate (EpistemicCalibrate.json)
   Missing: _meta.layer, _meta.category

⚠️  EpistemicROI (EpistemicROI.json)
   Missing: _meta.layer, _meta.category

⚠️  Equilibrium (Equilibrium.json)
   Missing: _meta.layer, _meta.category

⚠️  Estimate (Estimate.json)
   Missing: _meta.layer, _meta.category

⚠️  EthicalReasoningProtocol (EthicalReasoningProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  EvaluatorOptimizer (EvaluatorOptimizer.json)
   Missing: _meta.layer, _meta.category

⚠️  Event (Event.json)
   Missing: _meta.layer, _meta.category

⚠️  EventReact (EventReact.json)
   Missing: _meta.layer, _meta.category

⚠️  Exception (Exception.json)
   Missing: _meta.layer, _meta.category

⚠️  ExchangeRate (ExchangeRate.json)
   Missing: _meta.layer, _meta.category

⚠️  ExecutionManifest (ExecutionManifest.json)
   Missing: _meta.layer, _meta.category

⚠️  Expansive (Expansive.json)
   Missing: _meta.layer, _meta.category

⚠️  ExperienceSharding (ExperienceSharding.json)
   Missing: _meta.layer, _meta.category

⚠️  Experiment (Experiment.json)
   Missing: _meta.layer, _meta.category

⚠️  ExpiringToken (ExpiringToken.json)
   Missing: _meta.layer, _meta.category

⚠️  ExplainBeacon (ExplainBeacon.json)
   Missing: _meta.layer, _meta.category

⚠️  ExploreExploit (ExploreExploit.json)
   Missing: _meta.layer, _meta.category

⚠️  ExtendedThinking (ExtendedThinking.json)
   Missing: _meta.layer, _meta.category

⚠️  FabricSharding (FabricSharding.json)
   Missing: _meta.layer, _meta.category

⚠️  FailClosed (FailClosed.json)
   Missing: _meta.layer, _meta.category

⚠️  FailureTrace (FailureTrace.json)
   Missing: _meta.layer, _meta.category

⚠️  Falsification (Falsification.json)
   Missing: _meta.layer, _meta.category

⚠️  FeatureFlag (FeatureFlag.json)
   Missing: _meta.layer, _meta.category

⚠️  Feedback (Feedback.json)
   Missing: _meta.layer, _meta.category

⚠️  FeedbackSignal (FeedbackSignal.json)
   Missing: _meta.layer, _meta.category

⚠️  Fermi (Fermi.json)
   Missing: _meta.layer, _meta.category

⚠️  FirstPrinciples (FirstPrinciples.json)
   Missing: _meta.layer, _meta.category

⚠️  Forest (Forest.json)
   Missing: _meta.layer, _meta.category

⚠️  FractalIntelligence (FractalIntelligence.json)
   Missing: _meta.layer, _meta.category

⚠️  FrameError (FrameError.json)
   Missing: _meta.layer, _meta.category

⚠️  FrameSpec (FrameSpec.json)
   Missing: _meta.layer, _meta.category

⚠️  Gardener (Gardener.json)
   Missing: _meta.layer, _meta.category

⚠️  Gate (Gate.json)
   Missing: _meta.layer, _meta.category

⚠️  GenealogicalTrace (GenealogicalTrace.json)
   Missing: _meta.layer, _meta.category

⚠️  Generalize (Generalize.json)
   Missing: _meta.layer, _meta.category

⚠️  GlacialVault (GlacialVault.json)
   Missing: _meta.layer, _meta.category

⚠️  Global (Global.json)
   Missing: _meta.layer, _meta.category

⚠️  Goal (Goal.json)
   Missing: _meta.layer, _meta.category

⚠️  GracefulDegradation (GracefulDegradation.json)
   Missing: _meta.layer, _meta.category

⚠️  Gradient (Gradient.json)
   Missing: _meta.layer, _meta.category

⚠️  GraphOfThought (GraphOfThought.json)
   Missing: _meta.layer, _meta.category

⚠️  Greet (Greet.json)
   Missing: _meta.layer, _meta.category

⚠️  HackDetect (HackDetect.json)
   Missing: _meta.layer, _meta.category

⚠️  Handoff (Handoff.json)
   Missing: _meta.layer, _meta.category

⚠️  Heartbeat (Heartbeat.json)
   Missing: _meta.layer, _meta.category

⚠️  HeldRelease (HeldRelease.json)
   Missing: _meta.layer, _meta.category

⚠️  HeuristicSnap (HeuristicSnap.json)
   Missing: _meta.layer, _meta.category

⚠️  Hierarchy (Hierarchy.json)
   Missing: _meta.layer, _meta.category

⚠️  HindsightBlock (HindsightBlock.json)
   Missing: _meta.layer, _meta.category

⚠️  HolographicShard (HolographicShard.json)
   Missing: _meta.layer, _meta.category

⚠️  HumanApprove (HumanApprove.json)
   Missing: _meta.layer, _meta.category

⚠️  HumanEmulatorProtocol (HumanEmulatorProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  Hypothesis (Hypothesis.json)
   Missing: _meta.layer, _meta.category

⚠️  HypothesisEngine (HypothesisEngine.json)
   Missing: _meta.layer, _meta.category

⚠️  HypothesisLadder (HypothesisLadder.json)
   Missing: _meta.layer, _meta.category

⚠️  Hysteresis (Hysteresis.json)
   Missing: _meta.layer, _meta.category

⚠️  IdempotentWrite (IdempotentWrite.json)
   Missing: _meta.layer, _meta.category

⚠️  Identity (Identity.json)
   Missing: _meta.layer, _meta.category

⚠️  IdentityHandshake (IdentityHandshake.json)
   Missing: _meta.layer, _meta.category

⚠️  Incongruity (Incongruity.json)
   Missing: _meta.layer, _meta.category

⚠️  Induction (Induction.json)
   Missing: _meta.layer, _meta.category

⚠️  InputGuard (InputGuard.json)
   Missing: _meta.layer, _meta.category

⚠️  IntentGap (IntentGap.json)
   Missing: _meta.layer, _meta.category

⚠️  InternalConsistency (InternalConsistency.json)
   Missing: _meta.layer, _meta.category

⚠️  Interpret (Interpret.json)
   Missing: _meta.layer, _meta.category

⚠️  InvariantFilter (InvariantFilter.json)
   Missing: _meta.layer, _meta.category

⚠️  Invert (Invert.json)
   Missing: _meta.layer, _meta.category

⚠️  Jester (Jester.json)
   Missing: _meta.layer, _meta.category

⚠️  Judge (Judge.json)
   Missing: _meta.layer, _meta.category

⚠️  Kairos (Kairos.json)
   Missing: _meta.layer, _meta.category

⚠️  LatentAttachment (LatentAttachment.json)
   Missing: _meta.layer, _meta.category

⚠️  LatentWander (LatentWander.json)
   Missing: _meta.layer, _meta.category

⚠️  LateralOptimization (LateralOptimization.json)
   Missing: _meta.layer, _meta.category

⚠️  LatticeCommit (LatticeCommit.json)
   Missing: _meta.layer, _meta.category

⚠️  LayeredCheck (LayeredCheck.json)
   Missing: _meta.layer, _meta.category

⚠️  LazyConsensus (LazyConsensus.json)
   Missing: _meta.layer, _meta.category

⚠️  LeastToMost (LeastToMost.json)
   Missing: _meta.layer, _meta.category

⚠️  Ledger (Ledger.json)
   Missing: _meta.layer, _meta.category

⚠️  LivedProof (LivedProof.json)
   Missing: _meta.layer, _meta.category

⚠️  LocalizedLearning (LocalizedLearning.json)
   Missing: _meta.layer, _meta.category

⚠️  Lock (Lock.json)
   Missing: _meta.layer, _meta.category

⚠️  Loop (Loop.json)
   Missing: _meta.layer, _meta.category

⚠️  MECE (MECE.json)
   Missing: _meta.layer, _meta.category

⚠️  ManifestPlanning (ManifestPlanning.json)
   Missing: _meta.layer, _meta.category

⚠️  MarginalValueRule (MarginalValueRule.json)
   Missing: _meta.layer, _meta.category

⚠️  Measurement (Measurement.json)
   Missing: _meta.layer, _meta.category

⚠️  MechanisticDesignProposal (MechanisticDesignProposal.json)
   Missing: _meta.layer, _meta.category

⚠️  MemeticSeed (MemeticSeed.json)
   Missing: _meta.layer, _meta.category

⚠️  MentalSim (MentalSim.json)
   Missing: _meta.layer, _meta.category

⚠️  Message (Message.json)
   Missing: _meta.layer, _meta.category

⚠️  Meta (Meta.json)
   Missing: _meta.layer, _meta.category

⚠️  MetaCheck (MetaCheck.json)
   Missing: _meta.layer, _meta.category

⚠️  MetaPrompt (MetaPrompt.json)
   Missing: _meta.layer, _meta.category

⚠️  MetaProtocols (MetaProtocols.json)
   Missing: _meta.layer, _meta.category

⚠️  Metric (Metric.json)
   Missing: _meta.layer, _meta.category

⚠️  MintWhenFriction (MintWhenFriction.json)
   Missing: _meta.layer, _meta.category

⚠️  Mode (Mode.json)
   Missing: _meta.layer, _meta.category

⚠️  ModestClaim (ModestClaim.json)
   Missing: _meta.layer, _meta.category

⚠️  Monitor (Monitor.json)
   Missing: _meta.layer, _meta.category

⚠️  MonitorReport (MonitorReport.json)
   Missing: _meta.layer, _meta.category

⚠️  MonotonicCounter (MonotonicCounter.json)
   Missing: _meta.layer, _meta.category

⚠️  Mutex (Mutex.json)
   Missing: _meta.layer, _meta.category

⚠️  MutualInformation (MutualInformation.json)
   Missing: _meta.layer, _meta.category

⚠️  Nature (Nature.json)
   Missing: _meta.layer, _meta.category

⚠️  NegativeProof (NegativeProof.json)
   Missing: _meta.layer, _meta.category

⚠️  Noise (Noise.json)
   Missing: _meta.layer, _meta.category

⚠️  NoiseInjection (NoiseInjection.json)
   Missing: _meta.layer, _meta.category

⚠️  NormCheck (NormCheck.json)
   Missing: _meta.layer, _meta.category

⚠️  NormativeJudge (NormativeJudge.json)
   Missing: _meta.layer, _meta.category

⚠️  Novelty (Novelty.json)
   Missing: _meta.layer, _meta.category

⚠️  Nucleate (Nucleate.json)
   Missing: _meta.layer, _meta.category

⚠️  OODA (OODA.json)
   Missing: _meta.layer, _meta.category

⚠️  OathBind (OathBind.json)
   Missing: _meta.layer, _meta.category

⚠️  Observe (Observe.json)
   Missing: _meta.layer, _meta.category

⚠️  OntologyAdapt (OntologyAdapt.json)
   Missing: _meta.layer, _meta.category

⚠️  OntologyHandshake (OntologyHandshake.json)
   Missing: _meta.layer, _meta.category

⚠️  OpportunityCost (OpportunityCost.json)
   Missing: _meta.layer, _meta.category

⚠️  OptimalStop (OptimalStop.json)
   Missing: _meta.layer, _meta.category

⚠️  OptimisticSolver (OptimisticSolver.json)
   Missing: _meta.layer, _meta.category

⚠️  Optimize (Optimize.json)
   Missing: _meta.layer, _meta.category

⚠️  Option (Option.json)
   Missing: _meta.layer, _meta.category

⚠️  Oracle (Oracle.json)
   Missing: _meta.layer, _meta.category

⚠️  OrchestrationLoop (OrchestrationLoop.json)
   Missing: _meta.layer, _meta.category

⚠️  OsmoticFilter (OsmoticFilter.json)
   Missing: _meta.layer, _meta.category

⚠️  Outcome (Outcome.json)
   Missing: _meta.layer, _meta.category

⚠️  OutputGuard (OutputGuard.json)
   Missing: _meta.layer, _meta.category

⚠️  Overlap (Overlap.json)
   Missing: _meta.layer, _meta.category

⚠️  PURE (PURE.json)
   Missing: _meta.layer, _meta.category

⚠️  PUREBrainstorming (PUREBrainstorming.json)
   Missing: _meta.layer, _meta.category

⚠️  PURECheck (PURECheck.json)
   Missing: _meta.layer, _meta.category

⚠️  PUREOptimization (PUREOptimization.json)
   Missing: _meta.layer, _meta.category

⚠️  Parallel (Parallel.json)
   Missing: _meta.layer, _meta.category

⚠️  Parallelize (Parallelize.json)
   Missing: _meta.layer, _meta.category

⚠️  ParetoFront (ParetoFront.json)
   Missing: _meta.layer, _meta.category

⚠️  Parsimony (Parsimony.json)
   Missing: _meta.layer, _meta.category

⚠️  PathwayMemory (PathwayMemory.json)
   Missing: _meta.layer, _meta.category

⚠️  PatternDiscovery (PatternDiscovery.json)
   Missing: _meta.layer, _meta.category

⚠️  PatternEmergence (PatternEmergence.json)
   Missing: _meta.layer, _meta.category

⚠️  PatternSketch (PatternSketch.json)
   Missing: _meta.layer, _meta.category

⚠️  PerformanceSignal (PerformanceSignal.json)
   Missing: _meta.layer, _meta.category

⚠️  Permission (Permission.json)
   Missing: _meta.layer, _meta.category

⚠️  PermissionEscalate (PermissionEscalate.json)
   Missing: _meta.layer, _meta.category

⚠️  PerspectiveEnsemble (PerspectiveEnsemble.json)
   Missing: _meta.layer, _meta.category

⚠️  PhaseTransition (PhaseTransition.json)
   Missing: _meta.layer, _meta.category

⚠️  PhasedRefinement (PhasedRefinement.json)
   Missing: _meta.layer, _meta.category

⚠️  Plan (Plan.json)
   Missing: _meta.layer, _meta.category

⚠️  PolymorphicSolver (PolymorphicSolver.json)
   Missing: _meta.layer, _meta.category

⚠️  PreMortem (PreMortem.json)
   Missing: _meta.layer, _meta.category

⚠️  Prioritize (Prioritize.json)
   Missing: _meta.layer, _meta.category

⚠️  Probability (Probability.json)
   Missing: _meta.layer, _meta.category

⚠️  Probe (Probe.json)
   Missing: _meta.layer, _meta.category

⚠️  Problem (Problem.json)
   Missing: _meta.layer, _meta.category

⚠️  ProblemFramer (ProblemFramer.json)
   Missing: _meta.layer, _meta.category

⚠️  ProblemSpace (ProblemSpace.json)
   Missing: _meta.layer, _meta.category

⚠️  PromiseGraph (PromiseGraph.json)
   Missing: _meta.layer, _meta.category

⚠️  Prompt (Prompt.json)
   Missing: _meta.layer, _meta.category

⚠️  PromptChain (PromptChain.json)
   Missing: _meta.layer, _meta.category

⚠️  ProphetFanOut (ProphetFanOut.json)
   Missing: _meta.layer, _meta.category

⚠️  PropheticQuorum (PropheticQuorum.json)
   Missing: _meta.layer, _meta.category

⚠️  Proposal (Proposal.json)
   Missing: _meta.layer, _meta.category

⚠️  Proprioception (Proprioception.json)
   Missing: _meta.layer, _meta.category

⚠️  ProtoPack (ProtoPack.json)
   Missing: _meta.layer, _meta.category

⚠️  Protocol (Protocol.json)
   Missing: _meta.layer, _meta.category

⚠️  Prototype (Prototype.json)
   Missing: _meta.layer, _meta.category

⚠️  Queue (Queue.json)
   Missing: _meta.layer, _meta.category

⚠️  Quorum (Quorum.json)
   Missing: _meta.layer, _meta.category

⚠️  QuorumPulse (QuorumPulse.json)
   Missing: _meta.layer, _meta.category

⚠️  Rally (Rally.json)
   Missing: _meta.layer, _meta.category

⚠️  Rank (Rank.json)
   Missing: _meta.layer, _meta.category

⚠️  ReAct (ReAct.json)
   Missing: _meta.layer, _meta.category

⚠️  ReAttempt (ReAttempt.json)
   Missing: _meta.layer, _meta.category

⚠️  Realizable (Realizable.json)
   Missing: _meta.layer, _meta.category

⚠️  RealizationProtocol (RealizationProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  Reason (Reason.json)
   Missing: _meta.layer, _meta.category

⚠️  ReceptivityGate (ReceptivityGate.json)
   Missing: _meta.layer, _meta.category

⚠️  RecursionDive (RecursionDive.json)
   Missing: _meta.layer, _meta.category

⚠️  RecursiveRootCause (RecursiveRootCause.json)
   Missing: _meta.layer, _meta.category

⚠️  RedTeam (RedTeam.json)
   Missing: _meta.layer, _meta.category

⚠️  Refine (Refine.json)
   Missing: _meta.layer, _meta.category

⚠️  Reflex (Reflex.json)
   Missing: _meta.layer, _meta.category

⚠️  Reflexion (Reflexion.json)
   Missing: _meta.layer, _meta.category

⚠️  Reframe (Reframe.json)
   Missing: _meta.layer, _meta.category

⚠️  RegimeSense (RegimeSense.json)
   Missing: _meta.layer, _meta.category

⚠️  RegretMinimization (RegretMinimization.json)
   Missing: _meta.layer, _meta.category

⚠️  RepresentationSwap (RepresentationSwap.json)
   Missing: _meta.layer, _meta.category

⚠️  RequestFraming (RequestFraming.json)
   Missing: _meta.layer, _meta.category

⚠️  Resonate (Resonate.json)
   Missing: _meta.layer, _meta.category

⚠️  Resource (Resource.json)
   Missing: _meta.layer, _meta.category

⚠️  Responsibility (Responsibility.json)
   Missing: _meta.layer, _meta.category

⚠️  Result (Result.json)
   Missing: _meta.layer, _meta.category

⚠️  RetrievalAugment (RetrievalAugment.json)
   Missing: _meta.layer, _meta.category

⚠️  Retry (Retry.json)
   Missing: _meta.layer, _meta.category

⚠️  Reversibility (Reversibility.json)
   Missing: _meta.layer, _meta.category

⚠️  ReversibilityCheck (ReversibilityCheck.json)
   Missing: _meta.layer, _meta.category

⚠️  RigorousSolver (RigorousSolver.json)
   Missing: _meta.layer, _meta.category

⚠️  Risk (Risk.json)
   Missing: _meta.layer, _meta.category

⚠️  Roadmap (Roadmap.json)
   Missing: _meta.layer, _meta.category

⚠️  Robustness (Robustness.json)
   Missing: _meta.layer, _meta.category

⚠️  Role (Role.json)
   Missing: _meta.layer, _meta.category

⚠️  Rollout (Rollout.json)
   Missing: _meta.layer, _meta.category

⚠️  RolloutManifest (RolloutManifest.json)
   Missing: _meta.layer, _meta.category

⚠️  RolloutWatch (RolloutWatch.json)
   Missing: _meta.layer, _meta.category

⚠️  RootHashGossip (RootHashGossip.json)
   Missing: _meta.layer, _meta.category

⚠️  RootSolver (RootSolver.json)
   Missing: _meta.layer, _meta.category

⚠️  Route (Route.json)
   Missing: _meta.layer, _meta.category

⚠️  RuleSet (RuleSet.json)
   Missing: _meta.layer, _meta.category

⚠️  SacrificialProbe (SacrificialProbe.json)
   Missing: _meta.layer, _meta.category

⚠️  Sandbox (Sandbox.json)
   Missing: _meta.layer, _meta.category

⚠️  Satisfice (Satisfice.json)
   Missing: _meta.layer, _meta.category

⚠️  ScopeFreeze (ScopeFreeze.json)
   Missing: _meta.layer, _meta.category

⚠️  Score (Score.json)
   Missing: _meta.layer, _meta.category

⚠️  ScoringFunction (ScoringFunction.json)
   Missing: _meta.layer, _meta.category

⚠️  Scratchpad (Scratchpad.json)
   Missing: _meta.layer, _meta.category

⚠️  Search (Search.json)
   Missing: _meta.layer, _meta.category

⚠️  Select (Select.json)
   Missing: _meta.layer, _meta.category

⚠️  SelfConsistency (SelfConsistency.json)
   Missing: _meta.layer, _meta.category

⚠️  SelfReminder (SelfReminder.json)
   Missing: _meta.layer, _meta.category

⚠️  SemanticTabu (SemanticTabu.json)
   Missing: _meta.layer, _meta.category

⚠️  Sequence (Sequence.json)
   Missing: _meta.layer, _meta.category

⚠️  Shard (Shard.json)
   Missing: _meta.layer, _meta.category

⚠️  ShoutWhisper (ShoutWhisper.json)
   Missing: _meta.layer, _meta.category

⚠️  Sign (Sign.json)
   Missing: _meta.layer, _meta.category

⚠️  Signal (Signal.json)
   Missing: _meta.layer, _meta.category

⚠️  SignalReflection (SignalReflection.json)
   Missing: _meta.layer, _meta.category

⚠️  Silence (Silence.json)
   Missing: _meta.layer, _meta.category

⚠️  Simulation (Simulation.json)
   Missing: _meta.layer, _meta.category

⚠️  SimulationTrace (SimulationTrace.json)
   Missing: _meta.layer, _meta.category

⚠️  Skeleton (Skeleton.json)
   Missing: _meta.layer, _meta.category

⚠️  SkeletonOfThought (SkeletonOfThought.json)
   Missing: _meta.layer, _meta.category

⚠️  Snapshot (Snapshot.json)
   Missing: _meta.layer, _meta.category

⚠️  SocraticLoop (SocraticLoop.json)
   Missing: _meta.layer, _meta.category

⚠️  Solution (Solution.json)
   Missing: _meta.layer, _meta.category

⚠️  Solver (Solver.json)
   Missing: _meta.layer, _meta.category

⚠️  SolverManifest (SolverManifest.json)
   Missing: _meta.layer, _meta.category

⚠️  SolverNode (SolverNode.json)
   Missing: _meta.layer, _meta.category

⚠️  SolverTree (SolverTree.json)
   Missing: _meta.layer, _meta.category

⚠️  SomaticMarker (SomaticMarker.json)
   Missing: _meta.layer, _meta.category

⚠️  SourceEvaluate (SourceEvaluate.json)
   Missing: _meta.layer, _meta.category

⚠️  Spec (Spec.json)
   Missing: _meta.layer, _meta.category

⚠️  Specialize (Specialize.json)
   Missing: _meta.layer, _meta.category

⚠️  SpectralTune (SpectralTune.json)
   Missing: _meta.layer, _meta.category

⚠️  SpotAudit (SpotAudit.json)
   Missing: _meta.layer, _meta.category

⚠️  State (State.json)
   Missing: _meta.layer, _meta.category

⚠️  StateAudit (StateAudit.json)
   Missing: _meta.layer, _meta.category

⚠️  StateLock (StateLock.json)
   Missing: _meta.layer, _meta.category

⚠️  StateSnapshot (StateSnapshot.json)
   Missing: _meta.layer, _meta.category

⚠️  StateTransition (StateTransition.json)
   Missing: _meta.layer, _meta.category

⚠️  Status (Status.json)
   Missing: _meta.layer, _meta.category

⚠️  SteelmanCheck (SteelmanCheck.json)
   Missing: _meta.layer, _meta.category

⚠️  SteelmanFirst (SteelmanFirst.json)
   Missing: _meta.layer, _meta.category

⚠️  Step (Step.json)
   Missing: _meta.layer, _meta.category

⚠️  StepBack (StepBack.json)
   Missing: _meta.layer, _meta.category

⚠️  Stigmergy (Stigmergy.json)
   Missing: _meta.layer, _meta.category

⚠️  StrategicReading (StrategicReading.json)
   Missing: _meta.layer, _meta.category

⚠️  Strategy (Strategy.json)
   Missing: _meta.layer, _meta.category

⚠️  Stream (Stream.json)
   Missing: _meta.layer, _meta.category

⚠️  StructuralCoaching (StructuralCoaching.json)
   Missing: _meta.layer, _meta.category

⚠️  StyleSpec (StyleSpec.json)
   Missing: _meta.layer, _meta.category

⚠️  Subject (Subject.json)
   Missing: _meta.layer, _meta.category

⚠️  Summarize (Summarize.json)
   Missing: _meta.layer, _meta.category

⚠️  Summary (Summary.json)
   Missing: _meta.layer, _meta.category

⚠️  SunkCostIgnore (SunkCostIgnore.json)
   Missing: _meta.layer, _meta.category

⚠️  SurprisalUpdate (SurprisalUpdate.json)
   Missing: _meta.layer, _meta.category

⚠️  SurvivorCorrect (SurvivorCorrect.json)
   Missing: _meta.layer, _meta.category

⚠️  SynergisticMode (SynergisticMode.json)
   Missing: _meta.layer, _meta.category

⚠️  Synthesis (Synthesis.json)
   Missing: _meta.layer, _meta.category

⚠️  System (System.json)
   Missing: _meta.layer, _meta.category

⚠️  Taper (Taper.json)
   Missing: _meta.layer, _meta.category

⚠️  Task (Task.json)
   Missing: _meta.layer, _meta.category

⚠️  TaskLifecycle (TaskLifecycle.json)
   Missing: _meta.layer, _meta.category

⚠️  TemporalEnsembleForecasting (TemporalEnsembleForecasting.json)
   Missing: _meta.layer, _meta.category

⚠️  Tension (Tension.json)
   Missing: _meta.layer, _meta.category

⚠️  TensionHold (TensionHold.json)
   Missing: _meta.layer, _meta.category

⚠️  ThinSlice (ThinSlice.json)
   Missing: _meta.layer, _meta.category

⚠️  Think (Think.json)
   Missing: _meta.layer, _meta.category

⚠️  ThreeLevelCollision (ThreeLevelCollision.json)
   Missing: _meta.layer, _meta.category

⚠️  Throttle (Throttle.json)
   Missing: _meta.layer, _meta.category

⚠️  TieredAccess (TieredAccess.json)
   Missing: _meta.layer, _meta.category

⚠️  TimeWarpLog (TimeWarpLog.json)
   Missing: _meta.layer, _meta.category

⚠️  TimeboxThink (TimeboxThink.json)
   Missing: _meta.layer, _meta.category

⚠️  ToolDiscovery (ToolDiscovery.json)
   Missing: _meta.layer, _meta.category

⚠️  ToolInvoke (ToolInvoke.json)
   Missing: _meta.layer, _meta.category

⚠️  Topology (Topology.json)
   Missing: _meta.layer, _meta.category

⚠️  Trace (Trace.json)
   Missing: _meta.layer, _meta.category

⚠️  TraceBelief (TraceBelief.json)
   Missing: _meta.layer, _meta.category

⚠️  TradeOff (TradeOff.json)
   Missing: _meta.layer, _meta.category

⚠️  Transition (Transition.json)
   Missing: _meta.layer, _meta.category

⚠️  Translate (Translate.json)
   Missing: _meta.layer, _meta.category

⚠️  TranslationProxy (TranslationProxy.json)
   Missing: _meta.layer, _meta.category

⚠️  Tree (Tree.json)
   Missing: _meta.layer, _meta.category

⚠️  TreeOfThoughts (TreeOfThoughts.json)
   Missing: _meta.layer, _meta.category

⚠️  TriGate (TriGate.json)
   Missing: _meta.layer, _meta.category

⚠️  TruthseekingProtocol (TruthseekingProtocol.json)
   Missing: _meta.layer, _meta.category

⚠️  Uncertain (Uncertain.json)
   Missing: _meta.layer, _meta.category

⚠️  UncertaintyMap (UncertaintyMap.json)
   Missing: _meta.layer, _meta.category

⚠️  Understand (Understand.json)
   Missing: _meta.layer, _meta.category

⚠️  UniqueHandle (UniqueHandle.json)
   Missing: _meta.layer, _meta.category

⚠️  UniversalSolverTree (UniversalSolverTree.json)
   Missing: _meta.layer, _meta.category

⚠️  UptakeAsGround (UptakeAsGround.json)
   Missing: _meta.layer, _meta.category

⚠️  UptakeOverTimestamp (UptakeOverTimestamp.json)
   Missing: _meta.layer, _meta.category

⚠️  Validate (Validate.json)
   Missing: _meta.layer, _meta.category

⚠️  Value (Value.json)
   Missing: _meta.layer, _meta.category

⚠️  ValuePeg (ValuePeg.json)
   Missing: _meta.layer, _meta.category

⚠️  Variable (Variable.json)
   Missing: _meta.layer, _meta.category

⚠️  Vector (Vector.json)
   Missing: _meta.layer, _meta.category

⚠️  Verification (Verification.json)
   Missing: _meta.layer, _meta.category

⚠️  Vote (Vote.json)
   Missing: _meta.layer, _meta.category

⚠️  Warmup (Warmup.json)
   Missing: _meta.layer, _meta.category

⚠️  WhyClimb (WhyClimb.json)
   Missing: _meta.layer, _meta.category

⚠️  Work (Work.json)
   Missing: _meta.layer, _meta.category

⚠️  WorkerMode (WorkerMode.json)
   Missing: _meta.layer, _meta.category

⚠️  Workflow (Workflow.json)
   Missing: _meta.layer, _meta.category

⚠️  WorldReversible (WorldReversible.json)
   Missing: _meta.layer, _meta.category

⚠️  WorldTransparent (WorldTransparent.json)
   Missing: _meta.layer, _meta.category

⚠️  Yield (Yield.json)
   Missing: _meta.layer, _meta.category

Found issues in 452 patterns.
```

## Graph structure (orphans, duplicates, naked patterns)

Source: `scripts/audit/audit_graph.py` (ok)

```text
Loading graph...
Graph loaded with 1809 nodes and 3580 edges.
Checking for orphaned patterns...
Checking for orphaned components...
Checking for missing metadata...
Checking for hierarchy cycles...
Checking for duplicate names...
Checking rigor...

Audit Complete. Found 79 problems.

[NO_CONTRACTS] Pattern 'Axiom' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Branch' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Category' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Causation' has no Invariants, Preconditions, or Postconditions.
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
[NO_CONTRACTS] Pattern 'Nature' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Correlation' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Identity' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Entropy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Incongruity' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Metric' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Snapshot' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Transition' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Value' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Synthesis' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Event' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StateTransition' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Score' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Summary' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ContextCompress' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StateAudit' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Actor' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Refine' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Subject' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Noise' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Problem' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Queue' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Understand' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Discover' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ReversibilityCheck' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Dampen' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'EntropyPump' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StateLock' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Exception' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Belief' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Compromise' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Permission' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Outcome' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Roadmap' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Strategy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Jester' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'RuleSet' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ContextSwitch' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'IdentityHandshake' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Verification' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Experiment' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'TreeOfThoughts' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'HypothesisEngine' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'ReAttempt' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Role' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Deploy' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Aesthetics' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'TraceBelief' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'Solver' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'PURECheck' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'StyleSpec' has no Invariants, Preconditions, or Postconditions.
[NO_CONTRACTS] Pattern 'RecursionDive' has no Invariants, Preconditions, or Postconditions.
```

## Rigor coverage (invariants / pre / post)

Source: `scripts/audit/audit_rigor.py` (ok)

```text
{
  "total": 452,
  "with_invariants": 372,
  "with_preconditions": 181,
  "with_postconditions": 171,
  "fully_rigorous": 170,
  "naked": 79
}

Sample 'Naked' Patterns (No strict logic):
- Axiom
- Branch
- Category
- Causation
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
```

## Potential missing dependency links

Source: `scripts/audit/audit_missing_links.py` (ok)

```text
🔍 Scanning data/vocabulary for missing links...
Loaded 452 patterns.

Found 395 potential missing links.

🔹 AcceptSpec
   ❓ Mentions 'FrameError' but not linked.
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Score' but not linked.
   ❓ Mentions 'Solution' but not linked.
   ❓ Mentions 'Solver' but not linked.
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
🔹 Anomaly
   ❓ Mentions 'Datum' but not linked.
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
🔹 Boolean
   ❓ Mentions 'Decision' but not linked.
   ❓ Mentions 'Status' but not linked.
🔹 BoundedTask
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Gate' but not linked.
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
🔹 Check
   ❓ Mentions 'Decision' but not linked.
🔹 CognitiveEcho
   ❓ Mentions 'Feedback' but not linked.
🔹 CollaborativeWritingProtocol
   ❓ Mentions 'Decompose' but not linked.
   ❓ Mentions 'Variable' but not linked.
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
🔹 ConceptualDecomposition
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Decompose' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 Condition
   ❓ Mentions 'Boolean' but not linked.
   ❓ Mentions 'Result' but not linked.
🔹 ConfusedDeputy
   ❓ Mentions 'Prompt' but not linked.
🔹 Constraint
   ❓ Mentions 'Resource' but not linked.
🔹 Context
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Budget' but not linked.
🔹 Correlation
   ❓ Mentions 'Causation' but not linked.
🔹 CreativeBlend
   ❓ Mentions 'ConceptBlend' but not linked.
   ❓ Mentions 'NoiseInjection' but not linked.
🔹 Critique
   ❓ Mentions 'Feedback' but not linked.
🔹 Crystallize
   ❓ Mentions 'Entropy' but not linked.
🔹 Cyclic
   ❓ Mentions 'Condition' but not linked.
🔹 DataMinimization
   ❓ Mentions 'Goal' but not linked.
🔹 DecompositionGate
   ❓ Mentions 'Decision' but not linked.
   ❓ Mentions 'Gate' but not linked.
🔹 DeepResearch
   ❓ Mentions 'Plan' but not linked.
   ❓ Mentions 'Search' but not linked.
🔹 Delegate
   ❓ Mentions 'Work' but not linked.
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
🔹 DiscoveryProtocol
   ❓ Mentions 'Protocol' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 Distance
   ❓ Mentions 'Identity' but not linked.
   ❓ Mentions 'Metric' but not linked.
🔹 DriftWatch
   ❓ Mentions 'Distance' but not linked.
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
🔹 Expansive
   ❓ Mentions 'Judge' but not linked.
🔹 ExperienceSharding
   ❓ Mentions 'Agent' but not linked.
🔹 FailureTrace
   ❓ Mentions 'AcceptSpec' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Gate' but not linked.
   ❓ Mentions 'Identity' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 Falsification
   ❓ Mentions 'Hypothesis' but not linked.
🔹 Feedback
   ❓ Mentions 'Noise' but not linked.
🔹 Forest
   ❓ Mentions 'Topology' but not linked.
   ❓ Mentions 'Tree' but not linked.
🔹 FractalIntelligence
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Solver' but not linked.
   ❓ Mentions 'Value' but not linked.
🔹 FrameError
   ❓ Mentions 'Solver' but not linked.
🔹 FrameSpec
   ❓ Mentions 'Constraint' but not linked.
🔹 Gate
   ❓ Mentions 'Decision' but not linked.
🔹 Generalize
   ❓ Mentions 'Refine' but not linked.
🔹 Global
   ❓ Mentions 'System' but not linked.
🔹 Goal
   ❓ Mentions 'Result' but not linked.
🔹 GraphOfThought
   ❓ Mentions 'ChainOfThought' but not linked.
   ❓ Mentions 'DAG' but not linked.
   ❓ Mentions 'SkeletonOfThought' but not linked.
   ❓ Mentions 'Think' but not linked.
   ❓ Mentions 'TreeOfThoughts' but not linked.
🔹 Greet
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Protocol' but not linked.
🔹 HeldRelease
   ❓ Mentions 'Oracle' but not linked.
🔹 HumanEmulatorProtocol
   ❓ Mentions 'Decompose' but not linked.
   ❓ Mentions 'Solver' but not linked.
   ❓ Mentions 'Variable' but not linked.
🔹 Hypothesis
   ❓ Mentions 'Assumption' but not linked.
   ❓ Mentions 'Axiom' but not linked.
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
   ❓ Mentions 'Distance' but not linked.
   ❓ Mentions 'Search' but not linked.
🔹 LateralOptimization
   ❓ Mentions 'Optimize' but not linked.
   ❓ Mentions 'Reframe' but not linked.
   ❓ Mentions 'Translate' but not linked.
🔹 LayeredCheck
   ❓ Mentions 'Hierarchy' but not linked.
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
🔹 Measurement
   ❓ Mentions 'Observe' but not linked.
🔹 MechanisticDesignProposal
   ❓ Mentions 'Dialectic' but not linked.
   ❓ Mentions 'Novelty' but not linked.
🔹 MemeticSeed
   ❓ Mentions 'Resource' but not linked.
🔹 MetaCheck
   ❓ Mentions 'Verification' but not linked.
🔹 MetaProtocols
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Meta' but not linked.
   ❓ Mentions 'Tree' but not linked.
🔹 Mutex
   ❓ Mentions 'Resource' but not linked.
   ❓ Mentions 'Sequence' but not linked.
🔹 NegativeProof
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Search' but not linked.
   ❓ Mentions 'State' but not linked.
🔹 NormativeJudge
   ❓ Mentions 'Value' but not linked.
🔹 Novelty
   ❓ Mentions 'Judge' but not linked.
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
   ❓ Mentions 'FailureTrace' but not linked.
   ❓ Mentions 'Interpret' but not linked.
   ❓ Mentions 'Loop' but not linked.
   ❓ Mentions 'Plan' but not linked.
   ❓ Mentions 'Problem' but not linked.
   ❓ Mentions 'Rollout' but not linked.
   ❓ Mentions 'Solution' but not linked.
🔹 OsmoticFilter
   ❓ Mentions 'Queue' but not linked.
🔹 Outcome
   ❓ Mentions 'Plan' but not linked.
🔹 OutputGuard
   ❓ Mentions 'Score' but not linked.
🔹 PURE
   ❓ Mentions 'Expansive' but not linked.
   ❓ Mentions 'Novelty' but not linked.
   ❓ Mentions 'PUREBrainstorming' but not linked.
   ❓ Mentions 'PURECheck' but not linked.
   ❓ Mentions 'PUREOptimization' but not linked.
   ❓ Mentions 'Parsimony' but not linked.
   ❓ Mentions 'Realizable' but not linked.
🔹 PUREBrainstorming
   ❓ Mentions 'Check' but not linked.
   ❓ Mentions 'MechanisticDesignProposal' but not linked.
   ❓ Mentions 'Optimize' but not linked.
   ❓ Mentions 'PURE' but not linked.
   ❓ Mentions 'PURECheck' but not linked.
   ❓ Mentions 'Proposal' but not linked.
🔹 PURECheck
   ❓ Mentions 'Expansive' but not linked.
   ❓ Mentions 'PURE' but not linked.
   ❓ Mentions 'Protocol' but not linked.
   ❓ Mentions 'Realizable' but not linked.
🔹 PUREOptimization
   ❓ Mentions 'PURE' but not linked.
   ❓ Mentions 'Parsimony' but not linked.
   ❓ Mentions 'Realizable' but not linked.
   ❓ Mentions 'Synthesis' but not linked.
🔹 ParetoFront
   ❓ Mentions 'ExchangeRate' but not linked.
🔹 Parsimony
   ❓ Mentions 'Judge' but not linked.
🔹 PathwayMemory
   ❓ Mentions 'RootSolver' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 PatternDiscovery
   ❓ Mentions 'Search' but not linked.
🔹 PerformanceSignal
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Gate' but not linked.
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Solution' but not linked.
   ❓ Mentions 'Solver' but not linked.
🔹 PermissionEscalate
   ❓ Mentions 'Risk' but not linked.
🔹 PerspectiveEnsemble
   ❓ Mentions 'Distance' but not linked.
   ❓ Mentions 'Mode' but not linked.
   ❓ Mentions 'Role' but not linked.
🔹 PhasedRefinement
   ❓ Mentions 'Artifact' but not linked.
🔹 PolymorphicSolver
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Solver' but not linked.
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
🔹 Prompt
   ❓ Mentions 'Message' but not linked.
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
🔹 Rank
   ❓ Mentions 'Conservation' but not linked.
   ❓ Mentions 'Score' but not linked.
🔹 ReAct
   ❓ Mentions 'Goal' but not linked.
🔹 Realizable
   ❓ Mentions 'Judge' but not linked.
   ❓ Mentions 'Resource' but not linked.
🔹 RealizationProtocol
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'Artifact' but not linked.
   ❓ Mentions 'Interpret' but not linked.
   ❓ Mentions 'Loop' but not linked.
   ❓ Mentions 'Plan' but not linked.
   ❓ Mentions 'Realizable' but not linked.
   ❓ Mentions 'Rollout' but not linked.
🔹 ReceptivityGate
   ❓ Mentions 'AcceptSpec' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Gate' but not linked.
   ❓ Mentions 'Solver' but not linked.
   ❓ Mentions 'Verification' but not linked.
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
   ❓ Mentions 'Conservation' but not linked.
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
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Solution' but not linked.
   ❓ Mentions 'Solver' but not linked.
   ❓ Mentions 'System' but not linked.
   ❓ Mentions 'Verification' but not linked.
🔹 Risk
   ❓ Mentions 'Probability' but not linked.
🔹 Rollout
   ❓ Mentions 'Compensate' but not linked.
🔹 RolloutWatch
   ❓ Mentions 'MonitorReport' but not linked.
   ❓ Mentions 'Rollout' but not linked.
🔹 RootSolver
   ❓ Mentions 'Budget' but not linked.
   ❓ Mentions 'Problem' but not linked.
   ❓ Mentions 'Reframe' but not linked.
   ❓ Mentions 'Responsibility' but not linked.
   ❓ Mentions 'SolverTree' but not linked.
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
   ❓ Mentions 'Conservation' but not linked.
   ❓ Mentions 'Decompose' but not linked.
   ❓ Mentions 'Resource' but not linked.
🔹 Skeleton
   ❓ Mentions 'Parallel' but not linked.
🔹 SkeletonOfThought
   ❓ Mentions 'Parallel' but not linked.
   ❓ Mentions 'Skeleton' but not linked.
   ❓ Mentions 'Think' but not linked.
🔹 Solver
   ❓ Mentions 'Contract' but not linked.
   ❓ Mentions 'Feedback' but not linked.
   ❓ Mentions 'FrameError' but not linked.
   ❓ Mentions 'UniversalSolverTree' but not linked.
🔹 SolverManifest
   ❓ Mentions 'Constraint' but not linked.
   ❓ Mentions 'Identity' but not linked.
   ❓ Mentions 'Lock' but not linked.
🔹 SolverNode
   ❓ Mentions 'Budget' but not linked.
🔹 SolverTree
   ❓ Mentions 'Budget' but not linked.
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
🔹 Status
   ❓ Mentions 'Boolean' but not linked.
   ❓ Mentions 'Decision' but not linked.
🔹 SteelmanCheck
   ❓ Mentions 'Score' but not linked.
🔹 SteelmanFirst
   ❓ Mentions 'Proposal' but not linked.
   ❓ Mentions 'SteelmanCheck' but not linked.
🔹 StrategicReading
   ❓ Mentions 'Budget' but not linked.
🔹 SurvivorCorrect
   ❓ Mentions 'Estimate' but not linked.
🔹 SynergisticMode
   ❓ Mentions 'Protocol' but not linked.
🔹 TaskLifecycle
   ❓ Mentions 'Heartbeat' but not linked.
   ❓ Mentions 'State' but not linked.
🔹 TensionHold
   ❓ Mentions 'Falsification' but not linked.
   ❓ Mentions 'Tension' but not linked.
🔹 Throttle
   ❓ Mentions 'Queue' but not linked.
🔹 TieredAccess
   ❓ Mentions 'Distance' but not linked.
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
🔹 Uncertain
   ❓ Mentions 'Status' but not linked.
🔹 Understand
   ❓ Mentions 'Deep' but not linked.
🔹 UniqueHandle
   ❓ Mentions 'Resource' but not linked.
🔹 UniversalSolverTree
   ❓ Mentions 'Agent' but not linked.
   ❓ Mentions 'DAG' but not linked.
🔹 UptakeAsGround
   ❓ Mentions 'Verification' but not linked.
🔹 Validate
   ❓ Mentions 'Judge' but not linked.
   ❓ Mentions 'Result' but not linked.
   ❓ Mentions 'Score' but not linked.
   ❓ Mentions 'Status' but not linked.
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
Scanning 452 patterns for unlinked handle mentions...

⚠️  Abduction:
   • Mentions 'Anomaly' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AcceptSpec:
   • Mentions 'Compensate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'FrameError' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'PURE' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Vector' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AmbiguityResolution:
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AnalogyBridge:
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AnchorDrop:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Anomaly:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Attractor:
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Route' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Audit:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  AuditTrail:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Boolean:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Cache:
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Check:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Noise' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  CollaborativeWritingProtocol:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  ConceptualDecomposition:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decompose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Overlap' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Shard' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Condition:
   • Mentions 'Boolean' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Conservation:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Constraint' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'RuleSet' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ContingencyPlan:
   • Mentions 'Assumption' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ContinuousResourceAuction:
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  DecompositionGate:
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Prototype' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reframe' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Quorum' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vote' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Discover:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DiscoveryProtocol:
   • Mentions 'Creative' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Novelty' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DissentSeek:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Robustness' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Distance:
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vector' (unlinked). Should it be '{{{ghost}}}'?
⚠️  DocumentedOverride:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Event' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Elect:
   • Mentions 'Audit' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Cooldown' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Disband' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vote' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Eliminate:
   • Mentions 'Falsification' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EpistemicROI:
   • Mentions 'Experiment' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Equilibrium:
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Estimate:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Subject' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  EthicalReasoningProtocol:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Option' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PURE' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Think' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ExperienceSharding:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Shard' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  FailureTrace:
   • Mentions 'AcceptSpec' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Critique' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Forest:
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FractalIntelligence:
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Global' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FrameError:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Select' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
⚠️  FrameSpec:
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Gardener:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Gate:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Condition' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Route' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Gradient:
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Vector' (unlinked). Should it be '{{{ghost}}}'?
⚠️  GraphOfThought:
   • Mentions 'Branch' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'ChainOfThought' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Hypothesis' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Parallel' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'SkeletonOfThought' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'TreeOfThoughts' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Greet:
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  HumanEmulatorProtocol:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Deep' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Variable' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Hypothesis:
   • Mentions 'Assumption' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Axiom' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Falsification' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Measurement:
   • Mentions 'Act' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Observe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Variable' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  MetaProtocols:
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Meta' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  MutualInformation:
   • Mentions 'Correlation' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Entropy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Variable' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Value' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Novelty:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Creative' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Distance' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Nucleate:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Route' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'FailureTrace' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Rollout' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Sequence' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  OsmoticFilter:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  PURE:
   • Mentions 'Compose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Deep' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Deploy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Expansive' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Novelty' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PUREBrainstorming' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PURECheck' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PUREOptimization' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Parsimony' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Realizable' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Variable' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PUREBrainstorming:
   • Mentions 'PURE' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PURECheck:
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PURE' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PUREOptimization:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Metric' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PURE' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Parsimony:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Topology' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PathwayMemory:
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'RootSolver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PatternDiscovery:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Search' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PerformanceSignal:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compress' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decay' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Permission:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PermissionEscalate:
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PerspectiveEnsemble:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PhaseTransition:
   • Mentions 'Consensus' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PhasedRefinement:
   • Mentions 'Deep' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Plan:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  PolymorphicSolver:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Prompt:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Message' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  QuorumPulse:
   • Mentions 'Quorum' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Rally:
   • Mentions 'Criteria' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Rank:
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ReAct:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'PURE' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
⚠️  ReAttempt:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Build' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Realizable:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Step' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  ReceptivityGate:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Gate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Trace' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RecursionDive:
   • Mentions 'Strategy' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RecursiveRootCause:
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Validate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RedTeam:
   • Mentions 'Break' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Goal' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Mode' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solution' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Risk:
   • Mentions 'Probability' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Robustness:
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Role:
   • Mentions 'Identity' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Rollout:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compensate' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RolloutWatch:
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Plan' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Workflow' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RootHashGossip:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
⚠️  RootSolver:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reframe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Solver' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SacrificialProbe:
   • Mentions 'Probe' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Signal' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Measurement' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Feedback' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'FrameError' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'UniversalSolverTree' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
⚠️  SolverTree:
   • Mentions 'Budget' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Chain' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'DAG' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  Status:
   • Mentions 'Boolean' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Check' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decision' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Outcome' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Reason' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Queue' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Retry' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Task' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Transition' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TemporalEnsembleForecasting:
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
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
   • Mentions 'Distance' (unlinked). Should it be '{{{ghost}}}'?
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
⚠️  TriGate:
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
⚠️  TruthseekingProtocol:
   • Mentions 'Cache' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Compose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Contract' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Loop' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Protocol' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Uncertain:
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Work' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UncertaintyMap:
   • Mentions 'Estimate' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Risk' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UniqueHandle:
   • Mentions 'Resource' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Result' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Role' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Variable' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UniversalSolverTree:
   • Mentions 'Agent' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'DAG' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Decompose' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Problem' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'State' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Tree' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UptakeAsGround:
   • Mentions 'Context' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Verification' (unlinked). Should it be '{{{ghost}}}'?
⚠️  UptakeOverTimestamp:
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'System' (unlinked). Should it be '{{{ghost}}}'?
⚠️  Validate:
   • Mentions 'Artifact' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Judge' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Score' (unlinked). Should it be '{{{ghost}}}'?
   • Mentions 'Status' (unlinked). Should it be '{{{ghost}}}'?
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

Scan complete. Found unlinked handle mentions in 371 patterns.
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
