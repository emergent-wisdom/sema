# Reviewing a Pattern Card

`authoring.md` describes the **mechanics** of changing the vocabulary — staging,
apply, cascade, verify. This document describes the **judgment**: how to decide
whether a card is right, what goes wrong in practice, and what has already been
tried and failed.

It is a living document. The loop that uses it is expected to update it — see
[Maintaining this document](#maintaining-this-document).

---

## 1. Start with the scenario, not the checklist

The first question on any card is **what does a consuming agent do with this, and
where does that go wrong?** Not "which rule does this violate."

This matters because of what the card is. Every hashed field loads into the
context of every agent that depends on the pattern, so a wrong invariant is not a
documentation error — it is an instruction that will be followed. The verifier of
a Sema contract is a reasoner, not a compiler, which means defects are found by
imagining use and are missed by matching patterns.

The findings that justified this review all came from following a consequence:

- **`CiteBack`** required every assertion to link to a source ID and required the
  source to exist. Both are satisfied by attaching a *real* source ID to an
  *unrelated* claim. A pattern built to prevent hallucination permitted a
  hallucination with a footnote.
- **`HumanApprove`** required execution to halt until approval, and separately
  listed indefinite halting as a failure mode. The question nobody had asked was
  what happens when the timeout fires — and a gate that silently permits is worse
  than no gate, because it looks like a control.
- **`Compare`** asserted transitivity while its varies line permitted tolerance.
  The harm only appears downstream: under near-equality, grouping by equality
  becomes order-dependent, so the same values cluster differently depending on
  which comparison ran first.
- **`BayesUpdate`** bounded the posterior to (0,1) and the prior to [0.1, 0.9].
  Consistent until you notice that today's posterior is tomorrow's prior.

None of those are rule violations. The taxonomy in §3 is a **cross-check to run
after** the scenario, to catch what imagining use missed. Read in the other order
it will crowd out the thing that produced it.

## 2. The ordered checks

Apply these to a card you have already reasoned about.

**Read the manual section, not just the JSON.** On a large fraction of cards the
recorded `critique` or `tensions` already contained the finding. `ContextCompress`:
"that criterion is the hardest part and is under-specified." `Correlation`: "the
pattern has no structural defense against the upgrading." `Sign`: "this is
technical non-repudiation; legal non-repudiation has separate requirements." The
reviewers who wrote the commentary saw these; the contracts never absorbed it.

**Look for the honest formulation before inventing one** — on the same card, on a
neighbour, or in the sibling family. This is the highest-yield single move in the
review. Worked instances:

| Borrowed from | Fixed |
|---|---|
| `Realizable`'s "terminates in a primitive drawn from a stated set" | `FirstPrinciples`' infinite regress |
| `SolverManifest`'s "Claims, not proofs" | `ExtendedThinking`, `NegativeProof` |
| `Hypothesis`' "names an observation that would tell against it" | `ConfirmationBlock` |
| `AdversarialSteel`'s citation requirement | `SteelmanCheck` |
| `FailClosed`'s "Ambiguity == Rejection" | `HumanApprove`'s timeout default |
| `Contract`'s required-but-may-be-empty field | `MonitorReport` |
| `AtomicBid`'s "reversible or low-stakes" precondition | `LazyConsensus` |
| `Expansive`'s four-invariant shape | `Novelty` |

The reason it works is structural: the library repeatedly solved a problem
correctly in one place and restated it loosely elsewhere, because each card was
written on its own rather than against its family.

The same closeness is what makes borrowing go wrong, and the failure is silent:
**a borrowed formulation is only safe if the neighbour is estimating the same
quantity.** `MarginalValueRule` carried `Bid`'s failure-mode labels, where
"Underestimation: too optimistic, leading to overrun" is correct because a Bid
estimates *cost*. `MarginalValueRule` estimates *expected improvement*, so the sign
flips and both labels sat on the wrong bodies — an overestimate of value is what
wastes budget. Nothing in either card looks wrong in isolation. Before borrowing,
name what the neighbour measures.

**Compare `usage.every_context_needs` against `required` and against what the
parameters can express.** Empirically the most reliable field in the sidecar — the
missing contract was repeatedly already written there. It is nonetheless labelled a
*review hypothesis*, so it is a candidate to check rather than a specification to
transcribe. See §2a and Rule J clause 3.

**The override rule applies to ADDING an invariant, not only to deleting one.** This
is the mistake that produced three defects in a single pass, all caught on review.
`RecursiveRootCause` gained a provenance-citation invariant while `varies` assigns
"provenance tracking" to descendants and `extensions` names
`ProvenancedRecursiveRootCause`. `RegimeSense` gained an invariant mandating one
response while `varies` assigns "trigger action" to descendants and the mechanism
offers two. `RetrievalAugment` gained a mandatory citation while citation is absent
from `every_context_needs` and `varies` lists "citation format". Each looked like
repairing a weak contract and was in fact annexing descendant territory. Before
adding an invariant, read `varies`, `extensions` and `every_context_needs` — a
contract the family assigns downward is not a gap in the parent.

**And check the fields a new invariant can contradict, not only the mechanism.**
"Grep the mechanism" is too narrow: `SurprisalUpdate`'s clamped invariant left the
*postcondition* asserting unqualified proportionality, so the contradiction simply
moved from invariant-versus-invariant to invariant-versus-postcondition.
`Translate`'s `motivation.removability` went on citing "the Semantic Equivalence
invariant" after that invariant was deleted — and the critique note for that very
edit says removability "now rests on both halves of it", so the reasoning was written
and the field was not. `Overlap`'s `why_this_layer` still read "accept-set
intersection data structure" after the card was re-contracted as a protocol. The
sweep is: mechanism, preconditions, postconditions, failure_modes, then
`removability`, `why_this_layer`, `varies`, `extensions`, `every_context_needs`.

**Check `usage.varies` and do not override it** — but not mechanically. It has
contradicted a hashed invariant a dozen times and been right in most of them,
because it was written thinking about the whole family while the invariant was
written thinking about one card. The counter-examples matter as much as the rule:

- **`DAG`** — kept the required `root_id` and documented the restriction as an
  invariant instead of relaxing it, because its varies line says nothing about
  roots, so nothing actually conflicted.
- **`Falsification`** — declined to add a parameter for a varies-named confidence
  threshold, because no invariant referred to an undefined quantity. Nothing
  dangled, and a descendant can differ by mechanism rather than by parameter.
- **`HeldRelease`** — varies offers "partial release, streaming semantics" against
  a no-partial-states invariant. Atomicity is the point of an escrow, so this
  conflict is recorded rather than resolved.
- **`LayeredCheck`** — varies said "halt vs continue-with-warning" against
  Fail-Fast. Resolved by the **method-versus-rule split**: what varies is which
  findings count as failures; what holds is that a failure stops the sequence.

That last distinction generalises. Ask whether varies is naming *how* something is
done (descendant territory) or *whether* it holds (the contract's business).

**Check the consumers** to settle an over-narrow mechanism or an ambiguous card.
`Delegate` settled what `HolographicShard` is, when the card itself was
self-contradictory.

**Before deleting an invariant**, check whether its content already lives on the
card as a failure mode. **Before deleting an escape clause**, ask what it was
protecting — `AtomicBid`'s "(or low-stakes)" and `Abduction`'s "of similar scope"
both survived scrutiny, and without them each pattern would have forbidden
something legitimate.

**When an invariant asserts enforcement**, check that the field it enforces
against is required *and exists*. `ExchangeRate` demanded a timestamp on a card
with no `data_schema` at all.

**Before calling a quantity undefined**, check the parameters, the schema, whether
the dial is delegated to a dependency, and whether it is defined under a different
name.

**When you add a dependency by hand, copy the target's current `sema_id`.** A bare
`sema:Ledger` is rejected by Rule 2.4 at the validate step, before anything is
written. The apply chain does resolve refs to current hashes — but only after
validation has passed.

**When you replace an invariant, grep the mechanism for the claim you removed.**
Five cards in this review kept asserting in prose exactly what had just been
deleted from their contract: `Sign`'s mechanism said "non-repudiable link" after the
non-repudiation invariant was replaced for overstating what cryptography delivers,
`Step`'s said "an atomic unit of action" after Atomicity became declared
reversibility, and `WorldReversible`'s required inversion "at low cost" with no
invariant bounding cost. `LayeredCheck`'s said the hierarchy was "of abstraction" after the invariant was
changed to order by *cost* — the two orderings can diverge, which is why the
invariant was changed. And `EpistemicCalibrate`'s asserted unconditional decay after
the invariant gained a floor and a reset exemption.

All five were created *by* the fix, and all five are the mechanism-versus-invariant
class this document exists to catch. The placeholder diff does not see them, because
the wording survives without any placeholder changing.

**A term-match check for this class is a weak signal, like the others in §4.**
Comparing terms dropped from the invariants against terms surviving in the mechanism
flags 61 of 224 changed cards. A sample of 8 held **one** real contradiction
(`LayeredCheck`), one mild gap (`EpistemicCalibrate`) and six false positives —
`Decompose`'s mechanism already stated the criterion framing its new invariant
adopted, and `Induction`'s already said "disclosure rather than soundness". Roughly
12%. Worth noting that the three Codex found were found by **reading the cards**, not
by running this check, which is the same lesson §4 records five times over: run it as
a cross-check against a card you are already reading.

**After any hashed-field rewrite**, diff the placeholder set and assert no
dependency is left declared-but-unused — the validator will reject the batch
otherwise (schema §1). When a placeholder's only appearance is in a claim you are
deleting, prefer **moving** it somewhere it does work over dropping the edge.

**Always check the reverse edge before wiring.** This changed the intended action
roughly ten times. Most instructive: `Build`'s invariant referred to
`Cost(rollout)`, and `Rollout` is `Build`'s own consumer.

## 2a. What this document is subordinate to

Nothing here licenses adding fields. Three rules predate it and govern it, stated
in `authoring.md` and `AGENTS.md`:

- **Missing fields are not a coverage target.** Missing invariants or failure modes
  are not automatically defects.
- **The constraint-placement test.** A requirement belongs in a general parent only
  when omitting it would make the implementation cease to be that pattern *across
  every listed broad-use context*. Quantitative identity axes go in parameters,
  qualitatively different strategies in descendants, deployment policy in callers,
  contextual risks in the sidecar. Concrete leaf patterns may stay deliberately
  narrow.
- **A field count is not an argument.** "Only two invariants" is not actionable
  without an identity argument.

The taxonomy in §3 is compatible with all three, but only if read correctly. Every
class there is a claim about a *specific* defect — a contract that contradicts
another field, an invariant that permits a named failure, a claim the mechanism
makes and the contract omits. None is "this card has too few invariants."

The link between them is `usage.every_context_needs` — but it is a weaker link than
an earlier draft of this section claimed. The manual labels that field a **review
hypothesis**, not a specification, so a claim in it can be wrong and reclassifying
one is a legitimate outcome. What it gives you is a *candidate* answer to the
placement test, phrased in exactly the terms the test needs, from a reviewer who
was thinking about the whole family. Check the candidate; do not transcribe it.

Empirically it has been the most reliable field on the cards, which is why "the
missing contract was already in the intersection" is a legitimate finding and "zero
invariants at high fan-in" is not. But reliable is not normative. Rule J clause 3
states the obligation correctly: every claim in the intersection is traceable to
hashed semantics, explicitly delegated, or explicitly rejected. Rejection is
available. When the intersection does not survive scrutiny, the honest outcome is a
sidecar note, a descendant opportunity, or an OPEN — not a new invariant.

**Measured compliance, and a correction.** Of 107 cards where the invariant count
rose during the 2026-07 pass, 79% have an identity argument in the ledger record;
22 do not. Of 65 where failure modes were added, 75% do; 16 do not. Those ~38
records are not necessarily wrong changes — they are changes whose justification
was not written down, which makes them unverifiable, and they should be re-read
rather than trusted. The raw counts also overstate new claims: `Delegate` shows
+5 invariants where six contracts were *unpacked* from a single 476-character
string.

The pass also, for a time, operated on a self-authored rule that "zero failure
modes on a card with consumers is itself a defect." That contradicts the first rule
above and should not be reintroduced. It never reached a durable file, but it
shaped some of the 16 unargued failure-mode additions.

**Where failure modes belong**, since the documents can appear to disagree.
`authoring.md` places "contextual risks" in the sidecar, and `failure_modes` is one
of the eleven hashed fields. The reading that makes both true: a risk **intrinsic
to the mechanism** — it holds wherever the pattern is used — is card content, and a
risk that arises **only in some deployments** is sidecar content. `Probe`'s
observer effect is intrinsic. "This is expensive on our current infrastructure" is
not.

## 3. Defect taxonomy

Ordered roughly by consequence. **The counts are approximate**, reconstructed from
the session record rather than queried — see §5 for why, and for the tagging
convention that makes future counts verifiable.

### The defining property is uncontracted

The most consequential class. The claim that justifies the pattern's existence is
stated in the gloss, restated in the mechanism, named in the intersection — and
absent from the contract, because the invariants cover the mechanics and skip the
definition. `Care` (non-transactionality), `ConceptBlend` (a novel *third*
concept), `ContextSwitch` (scoped rather than ambient), `Correlation` (the absence
of a causal edge), `Creative` (novelty *and* value), `Exception`
(must-be-handled), `ExperienceSharding` (active/archival split, not forgetting),
`FabricSharding` (orthogonal dimensions).

### The invariant does what its own mechanism forbids

`Novelty`'s mechanism: "the essential move is a structural comparison against the
incumbent set **rather than a similarity score on surface tokens**." Its only
invariant was a similarity score on surface tokens.

### The contract misleads where the prose is accurate

`NegativeProof`'s mechanism ends "the guarantee is bounded — it proves
non-membership in the committed tree, not global non-possession." Its invariant
said "absence of evidence is evidence of absence," with the qualifier in a
parenthesis. A consumer reading the field that *binds* was misled.

Watch the operator especially, because a formalism reads as precision.
`OpportunityCost`'s mechanism says the cost *includes* the value of the best
forgone alternative and *deducts* it from the budget calculation; its invariant
said `Cost = {{value}} of best foregone alternative`. Read literally, the equality
discards the resources actually consumed — a 100-token action forgoing a 5-token
alternative costs 5. An `=` where the prose says "includes" is a different claim,
not a terser one.

### A parameter can express what an invariant forbids

`DeliberativeAlign` offered `strictness: {Strict, Permissive}` against "if Policy
forbids X and Goal requires X, agent must ABORT" — a Permissive setting on a
safety-abort contract. `ContinuousResourceAuction` required `HoldingCost > 0` with
`holding_cost_rate` ranged `[0.0, 1.0]`. The repair is usually to give the
parameter the axis the invariant permits rather than to delete it.

Check the other direction too — **a declared parameter value under which an
invariant cannot hold at all.** The repair depends on the shape of the conflict.
`NormCheck` was the common-property case: Flag, Rewrite, and Reject differ in what
happens after detection, so the invariant was narrowed to what all three modes
share and fact preservation was scoped to Rewrite.

`SteelmanCheck` was the two-judgment case. Its `strength_threshold` simultaneously
qualified a counter-argument as an adequate steelman and treated that same score
as the verdict that the original decision must be discarded. The repair separates
the questions: Judge scores counter-argument adequacy, then Check evaluates whether
the conclusion remains robust. One number no longer answers two different
questions.

`PromptChain` exposed a third case. Its Skip mode never defined the input to the
next step, so weakening the invariant could not create an executable continuation.
The mode was removed. Zero retries now means strict halt; a positive retry budget
means bounded recovery; exhaustion always halts before the next step.

So when a parameter value breaks an invariant, ask three questions in order. Do
all modes share a narrower property that still identifies the pattern? If one
parameter performs two judgments, should those judgments be separated? If a mode
cannot define the next state or input, remove it or fully specify that transition;
do not save it with weaker prose.

### The missing contract was already in the intersection

`AgentProtocol`'s curated bundle members, `AgentSandbox`'s quotas and logging,
`SolverManifest`'s five elements. Check `every_context_needs` before writing
anything new.

### `usage.varies` contradicts a hashed invariant

See §2. Twelve or so instances; varies usually wins.

### An invariant permits the failure mode the card names

`EpistemicCalibrate` asserted strictly decreasing confidence with no floor,
against a sole failure mode of "paralysis, confidence drops to zero too fast."
Distinguish this from two look-alikes that are **not** defects: a failure mode
naming **misuse of a precondition** (`AtomicBid`'s Permission Race) and one naming
the **detectable violation a process repairs** (`Compose`'s Interface Mismatch).

### Advisory mood where a contract belongs

`NormativeJudge`'s entire Goodhart defence was "this pattern *should* be deployed
as an ENSEMBLE," with the threshold parameter unreferenced. An ensemble that is
recommended is one that will sometimes be a single judge — precisely the
configuration Goodhart's Law exploits.

### An undefined quantity, or one defined under a different name

Undefined: `StepBack`'s max depth, `ChunkMerge`'s `ContextWindowLimit`,
`ConceptBlend`'s distance threshold, `NoiseInjection`'s reference to "parameter"
on a card with no parameters. Misnamed: `ContinuousResourceAuction`'s `T_cycle`
(the parameter is `cycle_time`), `DepthGovernor`'s `action_cost_threshold`
(`entropy_threshold`), `Hysteresis`' `T_up`/`T_down`, `MetaCheck`'s "max depth"
(`recursion_depth`). Not undefined — unfindable.

### A per-instance value in `parameters`

`Belief`'s `confidence`, `BayesUpdate`'s `prior_confidence`. See schema §1: a
value that differs per invocation is instance data. On `ExtendedThinking` the
right fix was a **mode** parameter rather than a size.

### The schema makes the pattern's purpose optional

`MonitorReport` compares deployed state against a definition of done, and
`definition_of_done` was an optional property.

### Two patterns fused in one card

`HolographicShard`: gloss, mechanism, "why it exists" and intersection all
described context propagation; the invariants, all three parameters and the
precondition all described erasure-coded storage. Resolve by weight of evidence
*including the consumer*, and flag the displaced material OPEN — it may be a
pattern the library is missing.

`Overlap` is the second instance and the more dangerous shape, because the
*contract* was the displaced half. Its gloss, mechanism, four failure modes,
why-it-exists, tensions, tradeoffs and declared intersection all describe an
accept-set negotiation protocol. Its two invariants — "Private regions respected",
"Shared region contains agreed facts" — and its precondition, "Two
ontologies/datasets", describe an ontology intersection. So the field a consumer
*binds to* contracted none of the four properties the card's own intersection
names, and contracted two belonging to something else entirely.

**How the consumer refers to a pattern tells you its category, and that is the
cheapest discriminator available.** `Yield`'s mechanism opens "Negotiation
concession. When `{{overlap}}` **fails**" — and a data structure cannot fail. One
clause in one consumer settled a question that the card's own `_meta.path`
(Infrastructure/Data Structures) answered wrongly. Before weighing prose against
contract, read how the dependents talk about it: "when X fails", "X returns", "the
X we agreed" each place X in a different category.

### Smaller classes

Decorative placeholders in invariant label prefixes (seven-plus cards; deleting
the label deletes the edge). Multiple contracts packed into one invariant string
(`Delegate` had six in 476 characters). Duplicate invariants (`HeldRelease`) and
duplicate failure modes assembled from two sources (`Crystallize` had seven
entries for four failures). Doubled words and doubled sentences (`Crystallize`,
`MentalSim`). A state list disagreeing with the mechanism's own state machine
(`HeldRelease`). An instruction to the pattern's *author* where a contract on
*instances* belongs (`HumanApprove`). A descriptive noun phrase where an invariant
belongs (`EpistemicCalibrate`, `Equilibrium`). A precondition on input
masquerading as an invariant (`FabricSharding`). The same mistake in the other
direction — a requirement sitting in `failure_modes` (`Yield`'s "Ledger requires
persistence infrastructure" is a precondition, not a way the pattern goes wrong). A handle written as prose with a
placeholder inside it (`Build`'s "the Marginal `{{value}}` Rule"), in prose
capitals with no dependency (`Delegate`'s RALLY), or as a quoted concept with no
handle at all ("Definition of Done"). A parameter description that is only a value
("Default: 1h"). A real edge existing only in a field description
(`MonitorReport`). Unmeasurable comparisons — `<<`, "proportional",
"as detailed as". Document coordinates in sidecar prose ("see Appendix A",
"§3.17") — the content usually belongs, the pointer does not.

**A lexical fix to a false citation makes it worse.** This entry is the record of
getting it wrong, because the wrong version is the tempting one.

Nine cards described themselves as "the paper's §6.N protocol". §6 of the current
`paper/sema.tex` is *Implementation*, with no subsections, so the obvious reading
was that the paper had been renumbered — and the obvious fix was to cite by title
instead: "the paper's ethical-reasoning protocol". That is what the first pass did,
and it was wrong twice over. **No commit in the entire history of `paper/sema.tex`
has ever mentioned any of those seven patterns**, and none appears in the current
text by handle or by description. The coordinates pointed at an *external*
document. In this repo "the paper" means `sema.tex`, so replacing the dead number
with a title converted a visibly broken reference into a fluent false attribution
— and the same claim sat in `removability`, the field that answers whether the
pattern should exist at all, where no coordinate detector was looking for it.

The check that would have caught it costs one grep: **before repairing a citation,
confirm the cited thing exists.** A coordinate that resolves to the wrong section
is a tripwire. Prose that names the target reads as verified and is not. Two
coordinates in the same sweep, `Judge`'s §5.2 and `Discover`'s §4.3, were reported
as "still resolving" because `sema.tex` §5.2 is *Evaluation as a Primitive: The
Judge* and §4.3 is *The Grammar of Agency* — a title coincidence mistaken for
verification, when `Discover`'s note said "FI v3" outright.

The surviving rule is narrower than "cite by title": do not attribute a design to a
document you have not read.

**The same verification can license the opposite action.** `RegimeSense`'s first
invariant triggered `OntologicalAccommodation`, which is not a pattern in this
library — and here replacing the name was right, because the referent exists under
another one. Three pieces of evidence: `OntologyAdapt` is a declared dependency of
that same card, the mechanism triggered the phantom and `{{ontology_adapt}}` in one
sentence, and two separate family discussions call the phantom "the response", which
is what `OntologyAdapt` does. So the rule is not "never repair a citation" — it is
**verify the referent first, then act**: if it exists, use its real name; if it does
not, remove the claim. Batch 8 skipped the verification and repaired anyway; that is
the only difference between the two cases.

A finding about card B, recorded on card A, stays on card A. `OntologyAdapt`'s
critique already said of this phantom "Neither exists" — and it survived in a
*hashed invariant* on `RegimeSense` plus two family discussions, because the sidecar
has no cross-reference mechanism and nothing re-reads a note from the other side.
When a note names another card, go and check that card. The seven cards' designs — five orthogonal dimensions,
Generate + Reduce, the is-ought boundary — are substantive and stand on the cards.
Attribution added nothing and asserted something false.

Separately, `§3.x` coordinates throughout the sidecar point into a *foundation
audit* document that is not in the repo at all. Twenty of those, in `usage.varies`,
`every_context_needs`, `intended`, `extensions`, `removability` and
`why_it_exists`. An earlier pass in this review had already established the fix and
applied it to one card, which is how a rule ends up half-applied: state the
substance ("Duration — no arbitrary range"), drop the pointer.

**A sweep that rewrites content must exclude `design.critique`.** Replacing the
phantom handle above corpus-wide also rewrote the two correction notes whose whole
subject was that name — "`OntologyAdapt` is not a missing sibling — it is THIS
pattern under a stale name" is nonsense. The log legitimately quotes the thing it is
correcting, which is the same reason the dated-bookkeeping sweep had to exclude it.
Third time this field has needed special handling; treat it as read-only to any
mechanical pass.

**Review narration in a field a consumer reads.** The same species as document
coordinates, and further along: an entry that is *entirely* addressed to the
reviewer. `Dialectic`'s tension read "resolved 2026-07-25. This tension was correct
and understated…", `Realizable`'s "corrected 2026-07-25. The claim that the
invariant conflicts with parallel exploration was a misreading" — an agent
hydrating from these learns about a review process, not about the pattern. Eleven
occurrences across nine cards, found by grepping for a date outside
`design.critique`, which is the review's own log and the one place a date belongs.
The date was only the marker; the whole entry was the defect. Rewrite as the
tension that now stands and move the narrative to `critique`. This is the sidecar's
version of the payload rule: the field exists to hydrate an agent, not to record
how it got that way.

Then check the field the review invented for itself. **`usage.notes` was a
changelog, not usage guidance: 62 of its 66 entries were addressed to a reviewer.**
"§3.18 moves to Infra/Data Structures since it's a Metric type. Broad-use confirms."
"Examined, unchanged." "Repointed from `Identity` to `Equivalence`." "Worth
spot-checking." Only four told a consumer anything — and two of those were
sibling *differentiations*, which belong in `family_discussion`. It exists on 66 of
455 cards, which is the tell: a field with no contract, added ad hoc, accumulates
whatever the reviewer had in hand. Unlike the 159 tensions, this needed no decision
about what the field is for, because `design.critique` already is the log — the
whole sweep was relocation. Any field the review adds for its own convenience will
do this; give it a stated contract or do not add it.

## 4. Negative results

Read this before building a tool. Each entry cost time that need not be spent
again.

**A check that silently under-selects reads as compliance.** Three instances, all
verified in code, all presenting as a green result:

- `validate_layer_direction` (Rule G) skips any dependency it cannot resolve, and
  at apply time resolves only the staged batch, so every edge into the committed
  library is skipped. Rule G reports **zero violations** and has never been
  enforced against the corpus.
- `validate_empty_fields_recursive` (Rule D) exists and is called, but only in the
  `use_pydantic=False` branch. The default path never reaches it, which is how
  three null hashed fields passed validation.
- The `extends` entailment warning keyed off the *staged* set. A parent's hash also
  moves by cascade, so an edit to `Message` moved `PolymorphicSolver` and
  re-pointed `OptimisticSolver` and `RigorousSolver`'s "is a kind of" claims with
  nothing printed. The correct criterion is *the parent's hash changed*, however it
  changed — snapshot hashes before the batch and diff after.

The shape is the same each time: the check runs, finds nothing, and the population
it was looking at was empty or partial for a structural reason. **Zero findings is
a claim about the selector until you have made it fail on purpose.** For a check
whose job is to select, one passing test is not enough — there is a population per
mechanism that can put a card in scope, and the dangerous one is always the
population no author touches. Yesterday's manual verification of the `extends`
warning confirmed the case it handled; nothing about it could reveal the case it
missed.

**This applies to verdicts, not only to code.** The earlier, pre-repair
`NormCheck` was recorded SOUND even though one invariant was false under a declared
parameter value. The verdict was sound *against what nominated the card*, which
was a circular-precondition check, and nothing about clearing that check spoke to
the rest of the card. The card was subsequently repaired; the lesson remains that
a SOUND verdict inherits the scope of whatever put the card in front of you. Record
what was examined, not just the conclusion. Where a card arrived via a targeted
sweep rather than a full read, SOUND means "this nomination was a false positive".

**A mechanical check for the misnamed-quantity class does not work.** Three
instances in one batch made it look detectable, so
`scratchpad/namedquantity.py` searched contract fields for underscore-bearing
identifiers matching no parameter or schema property. First run: 56 candidates,
dominated by false positives, because `{{placeholder}}` handle references are
snake_case too. After excluding braced tokens and formula indices: 19. Reading
those 19 shows the check conflates five unrelated things — formula and state
variables bound by the formula, names of outputs rather than inputs, protocol
message names, schema fields on cards with no schema, and the genuine mismatch.
Roughly 4 of 19 are defects and the check cannot tell which. **Keep it as a
cross-check against a card already being read, never as a work queue.**

**Detectors do not nominate work here.** The above is the concrete case. A
detector that cannot separate its class from its look-alikes will spend a
reviewer's attention on false positives and, worse, imply the unflagged cards are
clean.

**Counting a defect class by grepping prose does not work.** The counts in §3 were
reconstructed from a session record because each ledger entry phrased its finding
differently. A regex sweep recovered between 1 and 6 hits for classes with
five-to-twelve known instances. Tag the class explicitly (§5) or the count is not
recoverable.

**A change count is not a defect count, and this document has conflated them.**
"224 of 296 cards changed" appears in several commit messages and in §2a as though
it measured defects. It does not. The 224 mixes at least four kinds of edit:
provable contradictions between hashed fields, factual corrections, editorial
changes such as trimming an invariant's label prefix under the payload rule, and
preference. Some of the editorial subset repaired bloat this very review had
introduced.

The recurring *classes* in §3 are well evidenced — each names a specific structural
defect with instances. The *magnitude* is not, and needs a per-change type tag
alongside the class tag in §5 before any three-quarters claim is repeated. Until
then the defensible statement is narrower: the hard contradictions, where two
hashed fields provably disagree, are a subset of the 224 and are the part that
would survive independent adjudication.

**Fan-in stops discriminating.** Transitive fan-in was the right prioritiser while
high-fan-in patterns remained. After `Sign` (49) and `Contract` (47) the
distribution collapses: of the rest, roughly half sit at 1–5 dependents and half
at zero. Switch to fan-in-above-zero-first, alphabetical within the tier, and say
so rather than implying the order still encodes obligation.

**Do not diff a whole card against a base commit to detect content change.**
`sema_id`, `sema_ref`, `_meta.supersedes` and every dependency-embedded hash move
on any cascade rehash, so an untouched card shows as modified. Compare the
semantic fields, and compare dependencies **by handle**. `scratchpad/basediff.py`
does this.

**A hash-drift retry loop does not converge.** Drift on a large cascade is the
*correction*, not a failure. Restoring the backup discards it, and re-exporting
writes the stale hashes back — an infinite loop. `restore_plan`'s `db_valid`
parameter exists for this; the earlier retry-to-fixed-point fix was based on a
wrong theory about intra-batch hash ordering.

**A cycle will destroy the database if introduced through apply.** `--check`
passed, `rebuild --replace` failed *after* replacing the DB, and the next export
wrote zero patterns over `data/vocabulary/`. Fixed in
`src/sema/core/dependencies.py` (`validate_acyclic`, run in Phase 1) and by
timestamped backups. The reverse-edge check in §2 is the authoring-side guard.

**Put a check where the event happens, not where you are editing.** This failed twice
in one night, the same shape both times. The `extends` staleness refresh went in beside
the dependency refresh — which rewrites the *staging* file, while `data/vocabulary/` is
exported from the database, so `rebuild` round-tripped the stale value and two passes
did not converge. Then the entailment warning went in where a *child* is applied, so it
never fired for the dangerous case: a parent edited alone, with children re-pointed
later by the rebuild. Neither was a hard bug. Both were a check placed at the site of
the edit rather than the site of the risk. When a fix half-works, look for an
asymmetry — the dependency ref was correct while `extends` was stale, from the same
lookup in the same commit, which is what located the first one.

**Generalising a mechanism does not generalise its semantics.** Cascading a dependency
is safe because a dependency says *I use this*. Cascading `extends` is not, because it
says *I satisfy this*, and a changed parent may no longer be satisfied by the child.
Making `extends` cascade turned a visible staleness into an invisible falsehood:
adding "every Task declares an unbounded retry allowance" to `Task` left `BoundedTask`
— which caps total cost across retries — silently re-asserting `IS_A` against a parent
it contradicts. An outside reader caught it; the review did not. When you copy a
mechanism across fields, ask what each field *asserts*, not only what shape it has.

**Scope estimates made from a loose heuristic have been wrong every time, and the
error runs in both directions.** Five instances, which makes this the most
reliable finding in this document:

| sweep | counted | actual |
|---|---|---|
| category-label openers | 71, then 155, then 77 | 16, of which about half were defensible |
| trailing `Utilizes {{x}}.` | 31 | 26 — two of the 31 did say what the dependency was for |
| Rule I half-concepts | 55 | **0** — the rest were failure-mode *names*, not split handles |
| stale sidecar commentary | 62, reported as "a floor" | neither floor nor ceiling |
| defect-class counts | five to twelve each, from memory | 1–6 recoverable by grep |

The instinct to call an estimate "a floor" is worth distrusting specifically. It
sounds like the cautious framing and it is a claim in its own right — that the
error has a known sign. The stale-commentary sweep matched deleted invariant
*labels*, which misses every paraphrase, so it undercounts; it also produced three
false positives from causes that are worth knowing because they will recur in any
label-matching check:

- a **placeholder inside the label** — `Shard`'s `{{conservation}}:` does not match
  the string `Conservation`
- **punctuation before the colon** — `PerspectiveEnsemble`'s "Semantic Distance,
  every round:"
- a **case change alone** — `Step` and `WorldReversible` went from "Causal Closure"
  to "Causal closure" and from "Lossless Undo" to "Lossless undo", which a
  case-sensitive comparison reads as deletion plus addition

**Fixing those three causes made the queue bigger, not smaller.** Normalising the
labels — stripping placeholders, punctuation and case — took the stale-tensions
queue from 61 to **74**. It did not shrink; it traded one set of errors for a larger
candidate set, because the same normalisation that removes false negatives also
loosens the match. Do not expect a sharper detector to reduce the reading burden.

**And two more causes that no string handling can filter.** The fourth: the label is
a **common word** appearing in the prose for an unrelated, still-live reason.
`Scratchpad` matched on "bounded", and its tension — "bounded size vs complex
reasoning" — is a genuine tradeoff about an invariant that still exists. The fifth
is stranger: **the commentary cites a field that does not exist.** `Ballot`'s tension
said it "carries the rule (majority/unanimity) but doesn't enforce it", and its
schema has no `decision_rule` — the reference is to a *schema field*, so no
invariant-label check can see it, and its conclusion happened to be right for the
wrong reason. Both causes need a reader deciding whether the text is still *true*,
which is the same judgment the queue was supposed to save.

So: measure before promising a number, state the test used, and say which
direction the error runs only if you have actually established it. Where a sweep is
a work queue rather than a claim, that is fine — verify each item as you reach it,
which is what turned 55 Rule I violations into 0.

**A tension can also dissolve because the card absorbed it.** `Induction`'s
"Probabilistic vs usefulness" and "Hume's problem" stopped being tensions when the
mechanism started saying both — that the conclusion is probable rather than certain,
and that induction "has no formal justification and never acquires one, so what the
pattern requires is disclosure rather than soundness". A tension is for a live
conflict, not for a limitation the card already declares. That is distinct from
responsibility-moved: this relocates a caveat from commentary *into* the payload
rather than relocating a job to another card.

**And a tension can be orphaned by a card being split.** `HolographicShard`'s
"Information Redundancy vs storage cost" and "K-of-N reconstruction vs simpler
designs" both described the erasure-coding material removed when that fused card was
aligned to context propagation. Neither has a referent on the card any more, and
restoring them would restore the confusion. They belong with the displaced material
wherever it lands. Check for this whenever a card's scope has been narrowed.

**A tension can dissolve because a responsibility moved, not because a claim
weakened.** `ExecutionManifest`'s "budget enforcement vs exploration" closed when the
card stopped both projecting a cost and policing it — it now states the cost it
expects and says judging that against a budget is `Realizable`'s work. `Deep`'s
"functional equivalence vs emergent new questions" closed when the invariant absorbed
the objection, permitting new questions while forbidding a *different* one. Neither
was a rewording, and both are worth recognising: the tension was real while one card
was doing two jobs.

**Expect four outcomes, not two.** The fourth is **chosen, not balanced**: the
tension was accurate when written, and the review *took a side* rather than
resolving the conflict. `ConstructOntology`'s tension posed seed axioms against
emergent structure as an open question, and this review added an invariant requiring
grounding in first principles — so the card now has a position, and the cost the
tension named is inherited by everyone who uses it. Neither delete it (that hides a
cost the pattern imposes) nor leave it as open (it is not). Record it as chosen,
with the cost attached. This is the outcome most likely to be mishandled.

Two things a staleness sweep structurally cannot find. **Staleness can arrive from a
neighbour's edit** — `Contract`'s tension contrasted itself with "Constitution's
requirement" for machine-verifiable terms, and Constitution's requirement changed in
the same batch; no check keyed on one card sees that. And **a sweep is blind to text
that was never written** — `DAG`'s tensions said nothing about the `root_id`
requirement that makes it a *rooted* DAG rather than a general one. Looking for what
became wrong will not surface what was always missing.

**Expect three outcomes, not two.** A staleness sweep looks like a binary —
cosmetic rename, or resolved-and-misleading — and the commonest case is neither.
It is a claim stated in terms of a **specific value this review removed, where the
underlying tradeoff survives the value going away**. `BreadthGovernor`'s tensions
cited "7±2" and "cosine<0.8", both gone; a cap against exploration and distinctness
against exhaustiveness are properties of the pattern rather than of the numbers.
`Compose`'s said the pattern "names" a check it now requires, while the diagnosis
gap it also named is still open. Those get **reworded**, and deleting them as
resolved would discard a live tradeoff. Budget for rewording as the default.

**Most "tensions" in this library may never have been tensions.** The staleness
sweep assumes the field held something worth keeping. For a large share of the
corpus it holds a copy of a failure mode: "Clock drift (named failure) — agents
miss the High Tide window", "Cross-thread coordination latency (named failure)",
"Lossy translation (named failure)". No conflict is stated, nothing is traded
against anything, and the entry duplicates a hashed field in an unhashed one —
which is the exact mechanism that produced every stale sidecar this review has
fixed, because the copy cannot follow its original.

Measured as a queue, not a claim: **159 tensions across 107 cards** name a failure
mode and contain no comparative or conflict cue at all. The detector is loose in
one known direction — some entries state a real conflict without the word "vs"
(`Reframe`'s "reframing trades one blind spot for another" is a genuine tension) —
so verify each on arrival, as with every other queue here. An earlier, looser cut
of the same test said 191 across 121.

Five instances turned up by reading a single batch of eight: `NormCheck`,
`OntologyAdapt`, `PerspectiveEnsemble` and two on `SocraticLoop`. In every one the
live tension was recoverable and was *not* the failure mode — it was the conflict
the failure mode arises from, usually between the failure and the very invariant
meant to prevent it. `PerspectiveEnsemble` is the clearest: Strawman Waltz is what
the semantic-distance invariant exists to catch, the invariant is textual, and so
personas agreeing in substance while differing in wording satisfy it. The failure
mode survives its own mitigation, and that is the tension.

Whether the 159 should be rewritten this way or deleted as duplication is a
decision about what the sidecar is for, at a scale (107 cards) that makes it
Henrik's rather than a reviewer's. Do not sweep it silently.

**The sweep runs in both directions.** Every other entry here assumes the card
changed and the commentary went stale. `MarginalValueRule` is the reverse: its
tension stated the estimate error directions correctly — "overestimation wastes
budget, underestimation stops early" — while the card's own failure-mode labels had
them swapped. The stale-looking text was right and the hashed field was wrong. So
when a tension and a contract disagree, establish which one is true before assuming
the contract wins; a sweep for stale commentary is also a free audit of the cards.

**Pick the right unit of work.** For the tensions sweep the unit is the *tension*,
not the card: `Novelty` had three of three resolved, `Observe` and `Compare` two of
three, and four other cards one each with the rest live. Sweeping per card would
have either deleted live tensions or kept resolved ones. And when one half of a
tension is resolved, reword the retained half — `Compare`'s now says explicitly
that Arrow and Condorcet concern *aggregated* preference, so scoping the pairwise
claim to exact equality does not answer them, a distinction that was invisible
while the tension named only "transitivity".

## 5. Maintaining this document

The loop that uses this document is expected to improve it. Three rules:

**Promote a class only on the third instance.** This is the review method's
declared local sufficiency rule, not a universal `MintWhenFriction` threshold.
One sighting is an observation and belongs in the card's sidecar; two is a
coincidence; three is a class worth a reader's attention. The same discipline
that keeps the vocabulary from bloating keeps this document from becoming a
checklist nobody reads.

**Record the counter-example with the rule.** Every rule in §2 that has one is
more useful for it. A rule without its exceptions gets applied mechanically, which
is how "varies wins" would have damaged `DAG` and `HeldRelease`.

**Tag the class in the verdict.** So counts stay verifiable, ledger entries should
carry an explicit class tag — `[defining-property-uncontracted]`,
`[parameter-contradicts-invariant]`, and so on, using the §3 headings as the
vocabulary. Historical entries predate this convention and their counts are
approximate; entries from 2026-07-25 onward should be queryable.

**And add negative results.** A tool that did not work, a theory that was wrong, a
count that was overstated — those are worth more per word than another defect
class, because they stop the next reader repeating the work. §4 is the most
valuable part of this document.

## 6. A finding about the graph index, not the vocabulary

Recorded here because it was found by the review and it changes what graph queries
can be trusted for.

**The graph's contract index misattributes invariants for 24 of 455 patterns**, and
gives 6 of them the wrong invariant *count*. `find_or_create_node` auto-links a new
contract node to an existing one at cosine similarity ≥ 0.75
(`GraphStore.SIMILARITY_THRESHOLD`), which is loose enough to collapse materially
different clauses. Six patterns — `Select`, `CompatibilityCheck`, `Check`,
`ScoringFunction`, `Search`, `Aggregate` — share one `INVARIANT` node reading
"Determinism: Same input set + same criteria = same output set." Only `Select` says
that. `Check` says "Same input context yields same status", `Aggregate` says
"F(Input) always yields the same Output". Ask the graph what `Aggregate` guarantees
and it answers with `Select`'s wording.

**Identity is unaffected, and that is provable rather than assumed.** Hashes are
computed from the stored pattern dict, so if the collapsed nodes fed the hash, a
deterministic rebuild would disagree with the exports and `verify` would fail. It
passes. The exports are authoritative and correct; the damage is confined to
consumers of the index — the `pull` reconciliation queries and the node/edge totals in
`docs/information/audit.md`, which count invariant *clusters* rather than invariants.
`audit/rigor.py` is **not** affected, contrary to the first version of this entry: it
only asks whether a `HAS_INVARIANT` edge exists, never its text or count.

**The collapse is not confined to invariants, and the index is emptier than that.**
Measured per facet: **invariants 24 patterns wrong text / 6 wrong count;
preconditions 12 / 0; postconditions 1 / 0.** Those three, plus `PATTERN` and
`TAXONOMY_PATH`, are the *only* node types the database contains.

Which is the larger finding: **the corpus has 455 mechanisms, 108 parameter sets and
114 schemas, and zero graph nodes for any of them.** The field map keys on
`core_mechanism` while cards carry `mechanism`; parameters are dictionaries and the
indexer takes strings; `data_schema` is not mapped at all. So any audit that walks the
graph looking for redundant or near-duplicate *mechanisms* is not finding few — it is
looking at nothing. Distorted totals and topology also reach `sema skeleton`.

Correcting this entry twice over: `audit/rigor.py` is **not** affected, because it only
asks whether a `HAS_INVARIANT` edge exists, never its text or count. And `pull` does
not appear to reconcile on contract-node text or count either. Verify a consumer reads
what you think it reads before naming it in a blast radius — I named two that don't.

Not fixed here: whether 0.75 auto-linking is wanted at all is a design question,
and tightening it changes graph shape and the pull path.

**The method lesson is about how it surfaced.** `verify --refresh` moved one line in
a generated file: "Graph loaded with 1989 nodes and 3785 edges" became 1988 and
3784. That was fully explained by the batch — four invariants removed, one added,
net −1 — and confirming *that* explanation is what exposed the defect, because
confirming it meant learning that invariants are graph nodes at all. A delta you can
account for is still worth accounting for, when the accounting teaches you the
mechanism.
