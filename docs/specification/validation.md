# Validation Rules

## 1. The "Text is Code" Invariants

In Sema, the text fields (`mechanism`, `invariants`, `failure_modes`) are treated as compiled code. The linter enforces strict referential integrity between the text and the dependency map.

### Rule A: The Explicit Dependency Standard

This is the most common validation error. It ensures that the definition's Identity Hash accurately reflects its logic.

1. **Forward Rule (No Magic Globals):** Every `{{key}}` placeholder used in the text MUST have a corresponding entry in the `dependencies` object. You cannot reference a concept you haven't imported.
2. **Inverse Rule (No Silent Imports):** Every key declared in `dependencies` MUST be used at least once in the text fields.
  * *Rationale:* Unused dependencies create "False Fragility"—changing the hash of a pattern without changing its actual logic.

### Rule B: Complete Categorization

Every dependency must belong to **exactly one** category. A pattern cannot simultaneously `yield` and `compose_with` the same object.

| Category | Logical Role | Runtime Implication |
| --- | --- | --- |
| **`accepts`** | **Passive Input** | The pattern reads this data. |
| **`yields`** | **Passive Output** | The pattern creates/modifies this data. |
| **`composes_with`** | **Active Tool** | The pattern executes this logic. |
| **`references`** | **Metadata** | The pattern cites this concept (no runtime effect). |

## 2. Structural Integrity Rules

### Rule C: The Gravity Rule — consolidated into Rule G

**Rule G is normative for dependency direction.** This entry is kept because the
letter is cited elsewhere, including in `src/sema/cli/tests/`, and because its
cycle-breaking heuristic is worth keeping.

C previously stated the direction rule loosely and **contradicted G**. It forbade
"`Physics` primitive referencing `Society` pattern", while G exempts `references`
and `yields` and says cross-layer references *belong* in `references`. The corpus
sides with G: it holds **79 upward `references`/`yields` edges** — `RuleSet`
(Infrastructure) references `Constitution` (Society), and so on — and **zero**
upward edges in `accepts`/`composes_with`. C as written was violated 79 times by a
corpus that satisfies G perfectly.

**Cycle Breaking (retained):** if A and B form a cycle, identify the **Noun** and
the **Verb**. The Verb usually depends on the Noun — action requires object. Where
the reverse edge already exists, the relationship is in the graph from the side
that does not cycle, so name the other pattern in prose rather than adding an edge.

### Rule D: The Empty Field Rule

Never use empty arrays `[]`, empty objects `{}`, or `null` values. If a field has no content, **omit it entirely**.

* *Why?* Canonicalization, and the reason is stronger than it first appears. The
  hash root is built as `{k: pattern[k] for k in SEMANTIC_FIELDS if k in pattern}`
  (`src/sema/core/hashing.py`), so an omitted field is **absent from the hashed
  dict** while a null field is **present with value `None`**. Those are different
  dicts and they hash differently. An empty field therefore forks the pattern's
  identity while changing nothing about its meaning — the "False Fragility" that
  Rule A's inverse clause also guards against.
* **Scope: the eleven hashed fields (schema §5), at the top level.** The rule exists
  to stop identity forking, so it has nothing to say about `_meta`, which is
  unhashed, and it must not recurse into `data_schema`, where an empty construct can
  be legitimate JSON Schema — `"required": []` means "nothing is required" and is
  valid.
* **Enforcement today is unreachable, not absent.**
  `validate_empty_fields_recursive` in `src/sema/core/validator.py` implements the
  check, but it sits in the legacy branch that runs only when `use_pydantic=False`;
  the default path validates through Pydantic and never calls it. That is how a
  2026-07 review pass introduced three violations, setting `parameters` and
  `preconditions` to `None` to remove them rather than deleting the keys.
  Correcting those three cascaded to 56 files, which is the identity fork this rule
  is about.
* Run over the corpus, the legacy check rejects exactly one pattern:
  `TaskLifecycle`'s `_meta.related: []` — outside the scope defined above, and a
  one-line fix. So enabling a correctly scoped check is close to free today, while
  enabling the recursive one as written would eventually reject a valid schema.
* `scripts/audit/rule_adherence.py` reports violations in the meantime.
* Removing a field that genuinely has no content is the right edit. Do it by
  deleting the key.

### Rule E: The Noun Schema Requirement

Absorbs the former Rule K, which stated the same requirement with a different and
less checkable population ("Data Structure **or State-Bearing Primitive**").

**The population, defined mechanically.** A pattern is a Noun for this rule if
either holds:

1. its `_meta.path` ends in `Data Structures`, or
2. it is the target of some pattern's `accepts` or `yields`.

Both are decidable from the corpus without judgment, which "state-bearing
primitive" was not. Every Noun MUST define a `data_schema`. This prevents "Schema
Drift", where agents agree on the name `Task` and disagree on its required fields.

**The "Non-Vacuous" Clause:** the schema must define at least one specific
property. `{"type": "object"}` alone does not satisfy this. If the shape is truly
arbitrary, use `{"type": "object", "additionalProperties": true}` and document
*why* in the mechanism.

The non-vacuous clause previously said "strictly forbidden for **Ring 0** Nouns",
which mixed two populations: ring and category do not coincide — of 455 patterns,
158 are ring 0 and 94 end in `Data Structures`, overlapping on 55. The clause
applies to Nouns as defined above, whatever their ring.

**Enforcement covers clause 1 only.** The validator checks the taxonomy path.
Clause 2 is unenforced, and `scripts/audit/rule_adherence.py` currently reports
four patterns that are targets of `accepts`/`yields` with no schema properties:
`AnalogyBridge`, `HolographicShard`, `Responsibility`, `UniqueHandle`.

## 3. The "Deep Fix" Protocol

When the linter reports an **Unused Dependency** (Inverse Rule Violation), do NOT blindly delete it. The dependency represents a semantic signal from a previous author. You must triage the fix:

1. **Keep & Explain (Missing Text):** The relationship is real (e.g., `Task` yields `Solution`), but the text failed to describe it.
   * *Action:* Update `mechanism` to explicitly reference `{{solution}}`.
2. **Refine Link (Wrong Target):** The relationship is real, but the target pattern is imprecise.
   * *Action:* Swap dependency for a better existing pattern.
3. **Mint New (Missing Concept):** The relationship implies a concept that doesn't exist yet.
   * *Action:* Create a new pattern.
4. **Remove (Hallucination):** The relationship is truly irrelevant or legacy.
   * *Action:* Delete the dependency key.

## 4. Signature & Naming Rules

### Rule F: Signature Syntax (`signature`)

**Rule F1 — Syntax (machine-enforced):** the `signature` field declares the **Type
Constructor** or **Functional Interface** of the pattern. Every entry MUST have at
least one argument.

**Valid Syntax Forms:**

1. **Single Argument:** `Intent(Target)` (e.g., `Check(Nature)`)
2. **Nested Arguments:** `Intent(Target(Subtarget))` (e.g., `Deep(Check(Proof))`)
3. **Multiple Arguments:** `Intent(Target, Modifier)` (e.g., `Transform(Input, Output)`)

**Forbidden:**

* `"signature": ["Check"]` — Bare name, no argument
* `"signature": ["Trace", "Validate"]` — Two bare names
* `"signature": ["Deep"]` — Even abstract intents need targets

**Rationale:** A bare signature like `["Check"]` is ambiguous—*what* does it check? The argument specifies the domain or target of the polymorphic behavior, enabling the compiler to resolve abstract intents to concrete patterns at runtime.

These syntax requirements are **machine-enforced**, and the corpus has zero
violations.

**Rule F2 — The "Truth in Advertising" Invariant (reviewer-assessed):**
If a pattern claims a `signature`, it MUST fulfil that contract entirely. Do not
claim `Act(Deploy)` if the pattern only writes a file without executing the
deployment. Concretely, a claimed intent must be backed by the dependencies that
carry it out — usually an entry in `composes_with`.

F1 and F2 are separated because nothing checks F2, and "Rule F passes" was
therefore ambiguous: it meant the syntax parsed, never that the claim was true.
Cite F1 for a lint result and F2 for a review judgment.

### Rule G: The Dependency Direction Rule

**The Fundamental Principle:** Structural dependencies flow from specific to general. The more fundamental (more general, less specific) pattern is always upstream.

**The Rule:** A pattern's **hard dependencies** (`accepts` and `composes_with`) must reference patterns at the same or more fundamental layer. Two buckets are exempt:

- **`yields`** — outputs produced. Emergence flows upward (a Mind pattern can yield a Society artifact).
- **`references`** — soft citations and comparisons, not structural dependencies. Cross-layer references belong here or in `_meta.related` (see paper §5.2, Soft-Linking strategy).

| Pattern | Depends On | Rationale |
| --- | --- | --- |
| `Toyota` | `Car` | Toyota is a specific instance; Car is the general concept |
| `Car` | `Wheel` | Car is an assembly; Wheel is a component |
| `Wheel` | `Circle` | Wheel is a physical object; Circle is a geometric primitive |

**Violations (in `accepts` / `composes_with` only):**

* **Bad:** `Car` composes_with `Toyota`. (General cannot structurally depend on specific)
* **Bad:** `Physics` pattern accepts `Society` input. (Lower layers are more fundamental)

**Allowed cross-layer patterns:**

* **OK:** `Mind` pattern yields `Society` artifact. (Emergence)
* **OK:** `Infrastructure` pattern references `Society` concept. (Soft citation)

### Rule H: The Concept Suspicion Rule

Any **Capitalized Concept** (e.g., "Creation Protocol", "FrameSpec", "MonitorReport") appearing in the text fields MUST be a linked dependency `{{key}}`.

* **Suspicious:** "Executes the Creation Protocol." (Unlinked Proper Noun).
* **Action:**

1. **Mint it:** If it's a real pattern, create it and link it: "Executes the {{creation_protocol}}."
2. **Lowercase it:** If it's just a description, lowercase it: "Executes the creation protocol."

### Rule I: The Half-Concept Ban

It is strictly forbidden to reference "half concepts" by splitting a compound term
into separate parts.

* **Bad:** "The {{problem}} Statement..."
* **Good:** "The {{problem_statement}}..." (referencing `sema:ProblemStatement#...`)

**The test is handle resolution, not capitalisation.** A violation exists when the
placeholder plus the adjacent word, concatenated, names a pattern that already
exists and should have been referenced directly. A capitalised word after a
placeholder is otherwise ordinary: `{{sandbox}} Escape` is the *name of a failure
mode*, and there is no `SandboxEscape` pattern being split. Applying the
capitalisation reading to the corpus returns 55 candidates and 0 violations;
applying the resolution test returns 0 candidates.

Those 55 are still worth a reviewer's eye for a different reason. A placeholder
sitting in an invariant's label prefix is the sole wiring for that dependency, so
rewriting the label deletes the edge (Rule A's inverse clause). That is a hazard,
not a violation of this rule.

### Rule J: Cross-Field Semantic Coherence

Rules A through I check **referential and structural integrity**: that placeholders
resolve, that layers order, that a schema is present, that a signature parses.
Rule J is the only rule about whether the hashed fields **agree with each other**,
and that is where defects actually accumulate. A 2026-07 review pass changed 224 of
296 patterns it read while the corpus registered zero violations of the
**machine-checkable structural subset** — A, B, F1 and I. That subset was satisfied
by a library whose mechanisms, invariants, parameters, schemas and failure modes
routinely contradicted one another. The claim is deliberately narrower than "A–K
were satisfied": F2 and H are reviewer judgments that nothing scores, and G was not
enforced through the normal apply path at all, so none of the three had a pass to
give.

J formerly read "no tautologies, no vague corporate speak". That is prose-quality
guidance and it caught none of the above. What follows replaces it.

None of these clauses is machine-checkable. All five are checkable by a reader,
which is the relevant standard here: the verifier of a Sema contract is a reasoner,
not a compiler.

1. **No hashed field may contradict another.** An invariant that forbids what the
   mechanism describes is a defect in one of the two, and the mechanism usually
   wins. Observed: `Probe` forbade production effects while its mechanism said a
   Probe "interacts with its target"; `Novelty` required low embedding similarity
   while its mechanism said the essential move is structural comparison "rather than
   a similarity score on surface tokens".

2. **A parameter's range may not admit a value that violates an invariant.** The
   repair is usually to give the parameter the axis the invariant permits, not to
   delete it. Observed: `DeliberativeAlign` offered `strictness: {Strict,
   Permissive}` against an invariant requiring an abort on policy violation;
   `ContinuousResourceAuction` required `HoldingCost > 0` with a range including
   zero.

3. **Every claim in `usage.every_context_needs` is traceable to hashed semantics,
   explicitly delegated, or explicitly rejected.** That field is labelled a *review
   hypothesis*, so it is not a specification to be transcribed — a claim in it may
   be wrong, and reclassifying it is a legitimate outcome. What is not legitimate is
   leaving it unaddressed, because an unaddressed intersection claim is a contract
   the reviewer believed necessary and nobody wrote down. Observed: `AgentSandbox`
   named five elements and contracted two.

4. **An invariant asserting enforcement must have an observable witness.** Not
   necessarily a schema field — `Sign`'s "verifiable by a third party without the
   signer's cooperation" is witnessed by the verification itself. But where the
   claim names a field, that field must exist and be required wherever the claim is
   universal. Observed: `ExchangeRate` demanded a validity timestamp with no
   `data_schema` at all; `MonitorReport` compared against a `definition_of_done`
   that was optional.

5. **Every hashed failure mode must be causally traceable to the mechanism or to a
   declared boundary, and the review record must state its disposition** —
   prevented, detected, bounded, delegated, or accepted. Only *universal*
   mitigations belong on the card; delegation must name the responsible dependency,
   caller or descendant, and acceptance must state the intrinsic tradeoff. The
   disposition lives in the sidecar, not as a mitigation sentence per failure mode —
   that reading is how this clause would recreate coverage-target thinking.
   Five dispositions, not one, and *accepted* is a real answer: `CiteBack` cannot
   answer common-sense questions and that cost is the discipline rather than a flaw.
   *Delegated* is equally real: `SteelmanFirst` leaves counter-argument quality to
   `SteelmanCheck`. This clause is emphatically **not** "one invariant per failure
   mode" — that would recreate the coverage-target thinking that
   `docs/guides/authoring.md` forbids. Observed: `EpistemicCalibrate` asserted
   strictly decreasing confidence with no floor against a sole failure mode of
   "confidence drops to zero too fast", disposition neither stated nor implied.

**Rule J is not a licence to add fields.** It is subordinate to the
constraint-placement test in `docs/guides/authoring.md`: a requirement belongs in a
general parent only when omitting it would make the implementation cease to be that
pattern across every listed broad-use context. J identifies *incoherence*, and the
resolution is as often to weaken or delete a claim as to add one.

### Rule K: The Schema Requirement — consolidated into Rule E

**Rule E is normative for schema requirements.** K stated the same rule with a
population that could not be decided mechanically: "Data Structure or
**State-Bearing Primitive**". E now defines the population as the taxonomy path
plus the targets of `accepts`/`yields`.

Two clauses of K are retained and belong with E:

* **Rationale:** `data_schema` defines the "Shape of the Noun", not the "Signature
  of the Verb".
* **Do Not** define `input_schema` here. Inputs are declared by `accepts`; a verb
  inherits the shape from the Noun it accepts.

---

## 5. A caution on the rule letters

The letters are not stable identifiers across documents.
`docs/specification/validation-matrix.md` uses its own lettering, in which "Rule B"
is Text-Code Consistency and "Rule C" is Parameter Validators — neither matching
this file, where B is Complete Categorization and C is the Gravity Rule. Two test
files cite "Rule C" meaning the matrix's sense.

So cite the rule by name as well as letter, and when reading a citation elsewhere,
check which document it came from.
