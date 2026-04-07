# Naming Taxonomy

## 1. The Verification Stack (The "Check" Spectrum)

We strictly distinguish between four types of verification patterns. Choose the one that matches the *nature of the activity* and its *effect on flow*, not just the desired outcome.

| Pattern Type | Role | Output | The Question | Example |
| --- | --- | --- | --- | --- |
| **Gate** | **Enforcer (Flow Control)** | **Decision** (Open/Close/Debt) | *"Do we proceed?"* | `PUREGate`, `AuthGate` |
| **Check** | **Investigator (Fact Finding)** | **Status** (Verified/Falsified) | *"Is this true?"* | `SteelmanCheck`, `FactCheck` |
| **Judge** | **Evaluator (Valuation)** | **Score** (0.0 to 1.0) | *"Is this good?"* | `Parsimony`, `Aesthetics` |
| **Validate** | **Clerk (Compliance)** | **Boolean** (Pass/Fail) | *"Does it fit?"* | `SchemaValidate`, `InputGuard` |

### Key Distinction: Mechanisms vs. Policies

* **Cognitive Operations (Judge/Check/Validate)** generate *information*. They are the "Detectives."
* **Flow Controls (Gate)** generate *consequences*. They are the "Border Guards."

**A Gate DOES NOT think.** A Gate *wraps* a condition (which may be a complex Thinking pattern like `Parsimony`) and strictly enforces its boolean output. Ideally, Gates should accept their condition as a parameter (e.g., `Gate(Condition)`).

## 2. Naming Morphology

Pattern names must be self-documenting. Use the structure: **`[SpecificNuance][ReusableType]`**.

### A. The Control Structures (Flow)

*Use these suffixes to define "How does it run?"*

| Keyword | Definition | Examples |
| --- | --- | --- |
| **...Loop** | **Cycle.** A recurring process that runs until a condition is met. | `SocraticLoop`, `OrchestrationLoop` |
| **...Mode** | **Configuration.** A temporary state that alters behavior/permissions. | `WorkerMode`, `SynergisticMode` |
| **...Protocol** | **Interaction Standard.** A multi-step dance between agents. | `AgentProtocol`, `ForkingProtocol` |
| **...Sim** | **Virtual Execution.** Running a process in a sandbox to predict outcomes. | `MentalSim`, `EmpathySim` |
| **...Switch** | **Transition.** A mechanism to change Context or Mode. | `ContextSwitch` |

### B. The Data Containers (Nouns)

*Use these suffixes to define "What is this object?"*

| Keyword | Definition | Examples |
| --- | --- | --- |
| **...Spec** | **Requirements Contract.** A static definition of constraints or goals. "The Rules." | `AcceptSpec`, `FrameSpec` |
| **...Manifest** | **Inventory.** A complete list of contents, resources, or steps. "The Payload." | `ExecutionManifest`, `SolverManifest` |
| **...Log** | **Immutable History.** An append-only record of past events. | `TimeWarpLog`, `AuditLog` |
| **...Anchor** | **Reference Point.** A fixed, immutable state used for comparison or rollback. | `ConceptAnchor`, `CounterfactualAnchor` |
| **...Map** | **Topology.** A structured representation of a domain or space. | `UncertaintyMap`, `SafetyCartographer` |

### C. The Operators (Verbs)

*Use these suffixes to define "What actions does it perform?"*

| Keyword | Definition | Examples |
| --- | --- | --- |
| **...Search** | **Exploration.** Navigating a space to find targets. | `BeamSearch`, `DeepResearch` |
| **...Update** | **Modification.** Changing internal state based on new data. | `BayesUpdate`, `SurprisalUpdate` |
| **...Trace** | **Lineage.** Generating a path of causality or provenance. | `SimulationTrace` |

### D. The Namespace Stewardship Rule (The "Squatting" Test)

The vocabulary is a shared commons. Before claiming a short, general Handle (e.g., `Parsimony`, `Gate`, `Check`), you must apply the **Occupancy Test**:

> *"Would a future user legitimately expect this Handle to mean something broader than my specific use case?"*

* **If YES:** You are squatting. You must either:
1. **Generalize** your pattern to be that universal primitive (stripping out your specific logic).
2. **Rename** your pattern to reflect its specificity (e.g., `PUREParsimony` instead of `Parsimony`).


* **If NO:** The name is safe to claim.

**Examples:**

* ❌ **Bad:** Naming a pattern `Verify` that only checks PURE logic. (Squats on the general concept of verification).
* ✅ **Good:** Naming that pattern `PUREVerify` and leaving `Verify` free for a generic boolean check.
* ✅ **Good:** Naming a pattern `TriGate` because it handles *any* trinary signal, not just yours.

### E. The Self-Contained Principle (No Implicit Context)

Every pattern must be fully functional and meaningful **in isolation**. A pattern cannot rely on "implied" context from a specific parent protocol or framework to work correctly.

* **The Test:** "If I extract this pattern and use it in a completely different workflow, does it still make sense?"
* **Violation:** A pattern named `Parsimony` that outputs "Yellow" implying "Smallest Lift Required" (a PURE-specific concept). Outside of PURE, "Yellow" is ambiguous.
* **Fix:**
1. **Generalize:** Make the output generic (e.g., "Yellow" = "Marginal/Debt").
2. **Explicitly Import:** If the pattern relies on `SmallestLift`, it must explicitly depend on a `SmallestLift` pattern.
3. **Rename:** If the logic is inextricably tied to a parent, name it `PUREParsimony`.

**Rationale:** Dependencies must be *explicit* (in the `dependencies` block), not *implicit* (in the designer's head).

## 3. Dependency Direction (The Gravity Rule)

Dependencies MUST flow from **Specific  General** (or **High-Level  Fundamental**).

* ✅ `Toyota` depends on `Car`.
* ✅ `Society` depends on `Mind`.
* ✅ `Mind` depends on `Physics`.
* ❌ `Physics` cannot depend on `Society`. (A primitive like `Select` cannot depend on `Vote`).

**Cycle Breaking Strategy:**
If A and B are mutually dependent, identify which is the **Noun** (Object) and which is the **Verb** (Process).

* **Verb depends on Noun.** (Action requires Object).
* *Exception:* If the Noun is *defined by* the Process (e.g., `Solution` defined by `Work`), use `yields` or weak references, but ensure the *definition* doesn't cycle.
