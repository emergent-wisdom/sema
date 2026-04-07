"""Generator prompts for graph-based solution taxonomy."""


def build_generation_prompt(
    problem_statement: str, graph_state: str, schema: str, max_iterations: int = 5
) -> str:
    """Build the prompt for solution generation with graph awareness.

    Args:
        problem_statement: The problem to solve
        graph_state: Output from GraphStore.get_graph_state_for_prompt()
        schema: JSON schema for solution format
        max_iterations: Max attempts before giving up
    """
    return f"""You are generating a NOVEL solution to a problem. 
Your goal is to find an unexplored position in the solution space.

=== PROBLEM ===
{problem_statement}

{graph_state}

=== YOUR TASK ===
Generate a solution that fills one of the unexplored gaps shown above.

IMPORTANT: After you submit, the system will check if your solution is too similar to existing ones.
- If your mechanism is >92% similar to an existing one, your solution will be REJECTED
- You will receive feedback showing what's similar and suggestions for morphing
- You can iterate up to {max_iterations} times to find a novel position

=== STRATEGIES ===
If your solution is rejected as too similar:

1. MORPH THE MECHANISM
   - Don't just rename it - change HOW it fundamentally works
   - Use a different trigger, a different resource, a different timing
   - Look at the underused mechanisms and try to incorporate their approach

2. TARGET DIFFERENT OUTCOMES
   - If many solutions produce the same outcome, target a different one
   - Look at unseen mechanism-outcome combinations

3. CHANGE THE SIGNAL
   - What triggers your mechanism? Can you use a completely different signal?

=== OUTPUT FORMAT ===
{schema}

Generate your solution now. Be bold - the existing solutions already cover common approaches."""


def build_feedback_prompt(
    novelty_check: dict, original_solution: dict, iteration: int, max_iterations: int
) -> str:
    """Build feedback prompt when solution is not novel enough.

    Args:
        novelty_check: Output from GraphStore.check_novelty()
        original_solution: The solution that was rejected
        iteration: Current attempt number
        max_iterations: Maximum attempts allowed
    """
    lines = [
        f"=== ITERATION {iteration}/{max_iterations} - SOLUTION NOT NOVEL ENOUGH ===",
        "",
        f"Your solution '{original_solution.get('label', '')}' was rejected.",
        "",
    ]

    if novelty_check.get("mechanism_overlap"):
        overlap = novelty_check["mechanism_overlap"]
        lines.extend(
            [
                f"MECHANISM OVERLAP: {overlap['similarity']:.0%} similar to existing",
                f"Your mechanism: {original_solution.get('core_mechanism', '')[:100]}...",
                f"Existing:       {overlap['existing_text'][:100]}...",
                "",
            ]
        )

    if novelty_check.get("outcome_overlap"):
        lines.append("OUTCOME OVERLAPS:")
        for o in novelty_check["outcome_overlap"][:3]:
            lines.append(f"  {o['similarity']:.0%} similar: '{o['new_text'][:50]}...'")
        lines.append("")

    if novelty_check.get("suggestions"):
        lines.append("SUGGESTIONS:")
        for sug in novelty_check["suggestions"]:
            lines.append(f"  - {sug}")
        lines.append("")

    lines.extend(
        [
            "=== YOUR TASK ===",
            "MORPH your solution to be genuinely different:",
            "- Change the core mechanism (not just wording)",
            "- Target different outcomes",
            "- Use a different triggering signal",
            "",
            "Do NOT just rephrase. Make structural changes.",
            "",
            "Generate a revised solution now.",
        ]
    )

    return "\n".join(lines)


def build_stuck_message(original_solution: dict, novelty_check: dict, iterations: int) -> str:
    """Build message when generator is stuck after max iterations.

    Args:
        original_solution: The last attempted solution
        novelty_check: The final novelty check results
        iterations: Number of attempts made
    """
    similarity = novelty_check.get("mechanism_overlap", {}).get("similarity", 0)
    return f"""=== GENERATION STUCK ===

After {iterations} attempts, no novel position was found.

Last attempt: {original_solution.get("label", "")}

The solution space may be saturated in this region. Options:
1. Accept the solution anyway (it will link to existing concepts)
2. Restructure the graph to reveal new distinctions
3. Approach the problem from a completely different angle

Similarity to existing: {similarity:.0%}"""


SELF_CRITIQUE_SYSTEM_PROMPT = """You have TWO roles: GENERATOR and TAXONOMIST.

As GENERATOR:
- Create solutions to the given problem
- When told a solution isn't novel, MORPH it (don't just rephrase)

As TAXONOMIST:
- Evaluate whether solutions are genuinely different from existing ones
- Suggest specific changes to reach unexplored territory

The goal is NOT to generate many solutions. The goal is to find a GENUINELY NOVEL position
in the solution space that hasn't been explored yet.

You will iterate until you find something novel or exhaust your attempts."""
