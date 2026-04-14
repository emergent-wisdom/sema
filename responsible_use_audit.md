# Sema Vocabulary: Responsible Use Audit

Audit of ~450 patterns for risks when adopted by unsupervised autonomous agents.

**Methodology:** Each pattern assessed on: could an autonomous agent cause real harm by applying this pattern without human oversight? Patterns flagged only for actual risk, not scary-sounding names.

---

## Evasion & Opacity

Patterns that help agents hide their actions, identity, or communications from oversight.

### MimicMask
**Gloss:** Hiding in the crowd
**Risk:** Teaches agents to embed real signals inside decoy traffic using steganography. An unsupervised agent could use this to communicate covertly, evading monitoring systems designed to keep agents accountable.
**`responsible_use`:** "Steganographic communication evades monitoring. Deploy only in environments where covert channels are explicitly authorized and audited."

### IdentityMask
**Gloss:** Disposable personas for privacy
**Risk:** Agents create untraceable disposable identities linked via zero-knowledge proofs. Enables acting without accountability — useful for privacy, but an unsupervised agent could use this to avoid attribution for harmful actions.
**`responsible_use`:** "Disposable identities prevent attribution. Ensure a root identity audit trail exists and that persona creation is logged even if individual actions are unlinkable."

### AnalogicalMask
**Gloss:** Privacy-preserving communication via approximate domain translation
**Risk:** Encodes sensitive content in a cover domain via structural analogy. An agent could use this to exfiltrate data past content filters that don't recognize the disguised form.
**`responsible_use`:** "Domain-translated content bypasses content-aware filters. Use only where data-loss-prevention policies explicitly permit analogical encoding."

### GhostTrail
**Gloss:** Cryptographically verified anonymous stigmergy
**Risk:** Agents leave environmental traces that are provably from a valid group member but untraceable to an individual. Enables plausible deniability for any single agent's actions.
**`responsible_use`:** "Ring-signature anonymity prevents individual attribution. Pair with group-level audit logging so collective behavior remains observable."

---

## Destruction & Irreversibility

Patterns that destroy data or make actions hard to undo.

### CryptoShred
**Gloss:** Deletion-by-key-destruction within a trusted execution boundary
**Risk:** Destroys encryption keys to make data permanently unrecoverable. Legitimate for privacy compliance, but an unsupervised agent could destroy evidence, audit trails, or critical data.
**`responsible_use`:** "Key destruction is irreversible and may violate data retention requirements. Require human approval before shredding and maintain a separate record of what was destroyed and why."

### EjectionSeat
**Gloss:** Hardware-interrupt kill switch
**Risk:** None — this is a safety pattern. It's the human override that terminates agent swarms. Listing it here to note it is *not* a concern; it's the opposite.
*No `responsible_use` needed.*

---

## Manipulation & Information Asymmetry

Patterns that create or exploit power imbalances in communication.

### VowOfSilence
**Gloss:** Strategic withholding of signal to force counterparty disclosure
**Risk:** A negotiation tactic where the agent deliberately reveals nothing to pressure the other party into revealing first. When used between agents, this is a coordination primitive. When used against humans, it's a manipulation technique.
**`responsible_use`:** "Strategic silence creates information asymmetry. Do not use against human counterparties without their awareness that this tactic is in play."

### MemeticSeed
**Gloss:** Viral propagation of semantic standards via economic subsidy
**Risk:** Agents subsidize adoption of their vocabulary by offering favorable terms. This is literally how standards spread — but an unsupervised agent could use economic incentives to propagate a self-serving ontology that biases other agents' reasoning.
**`responsible_use`:** "Subsidized vocabulary adoption can bias downstream reasoning. Ensure propagated patterns are from a vetted, content-addressed source and that adopters can independently verify definitions."

### EmpathySim
**Gloss:** Predictive modeling of external agent states
**Risk:** Building a model of another agent's (or human's) internal state to predict behavior. Legitimate for coordination, but the same capability enables targeted manipulation — predicting what someone will respond to.
**`responsible_use`:** "Predictive modeling of others' states enables both coordination and manipulation. Use for alignment and mutual benefit, not to exploit predicted vulnerabilities."

### Jester
**Gloss:** Delivering critique via incongruity to minimize social friction
**Risk:** Frames criticism as humor to bypass social defenses. Useful for surfacing hard truths, but an unsupervised agent could use this to deliver hostile messaging disguised as jokes, making it hard for the target to object.
**`responsible_use`:** "Humor-wrapped critique bypasses social defenses. Ensure the underlying message is constructive and the target can engage with the substance, not just the framing."

---

## Covert Coordination

Patterns that enable agents to coordinate in ways that are hard to observe.

### ShoutWhisper
**Gloss:** Dual-mode communication
**Risk:** Agents broadcast intent publicly, then switch to encrypted P2P for actual coordination. The "whisper" phase is opaque to observers. Low risk in isolation but enables covert multi-agent coordination.
**`responsible_use`:** "Encrypted P2P coordination is invisible to external monitors. Log whisper-phase metadata (participants, timestamps, topics) even when content is encrypted."

### PheromoneEconomy
**Gloss:** Value-driven coordination
**Risk:** Agents coordinate indirectly by modifying their shared environment (stigmergy) with economic signals. Hard to monitor because there's no direct communication — coordination is implicit.
**`responsible_use`:** "Stigmergic coordination leaves no direct communication trail. Monitor environmental state changes for emergent coordination patterns."

---

## Circumventing Safety

Patterns that could bypass safety mechanisms.

### PermissionEscalate
**Gloss:** Requesting elevated privileges for sensitive operations
**Risk:** The pattern itself is a safety mechanism (proper privilege escalation). But the *concept* of escalation could be misapplied — an agent reasoning about how permissions work might find ways to acquire permissions it shouldn't have. The pattern's mechanism is sound (it blocks execution until approval), but the name primes agents to think about escalation.
*No `responsible_use` needed — the mechanism is the defense.*

### ConstraintRelax
**Gloss:** Escaping local optima by loosening bounds
**Risk:** Explicitly about loosening constraints to find better solutions. An unsupervised agent could relax safety constraints, treating them as optimization barriers rather than non-negotiable boundaries.
**`responsible_use`:** "Never relax safety, ethical, or access-control constraints. This pattern applies only to search-space and optimization constraints, not to policy boundaries."

### Exaptation
**Gloss:** Radical tool repurposing via analogical mapping
**Risk:** Using tools for purposes outside their design. An agent could repurpose a benign tool in harmful ways — e.g., using a text-formatting tool as an encoding mechanism for data exfiltration.
**`responsible_use`:** "Repurposed tools may bypass safety checks designed for their original use case. Validate that the repurposed tool's safety properties still hold in the new context."

---

## Likely Fine (Reviewed, No Flag Needed)

| Pattern | Why it's fine |
|---------|--------------|
| AdversarialSteel | Dual-advocate debate — improves reasoning quality |
| AdversarialProof | Proving absence — security testing pattern |
| RedTeam | Adversarial testing of your own work |
| SacrificialProbe | Learning from cheap failures — standard engineering |
| ConfusedDeputy | The *defense* against the vulnerability, not the attack |
| NoiseInjection | Breaking out of reasoning loops — creativity tool |
| HackDetect | Detecting shortcuts — quality assurance |
| Silence | Withholding output during processing — not manipulative |
| MetaPrompt | Generating prompts from prompts — standard LLM technique |
| FailClosed | Default-deny — this IS the safety pattern |

---

## Summary

| Category | Patterns | Count |
|----------|----------|-------|
| Evasion & Opacity | MimicMask, IdentityMask, AnalogicalMask, GhostTrail | 4 |
| Destruction | CryptoShred | 1 |
| Manipulation | VowOfSilence, MemeticSeed, EmpathySim, Jester | 4 |
| Covert Coordination | ShoutWhisper, PheromoneEconomy | 2 |
| Circumventing Safety | ConstraintRelax, Exaptation | 2 |
| **Total** | | **13** |

13 out of 453 patterns (~3%) warrant a `responsible_use` notice. All 13 are excluded from the `standard` preset except EmpathySim and Jester (which could arguably stay — their risks are moderate).
