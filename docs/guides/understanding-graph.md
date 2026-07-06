# Using Sema with Understanding Graph

Sema and [Understanding Graph](https://github.com/emergent-wisdom/understanding-graph)
cover two different axes of shared memory for AI agents. They compose
cleanly, and most teams benefit from running both.

| Layer | Tool | Answers |
|---|---|---|
| Semantic memory | Sema | *What does this word actually mean, byte-for-byte?* |
| Episodic memory | Understanding Graph | *What happened? Why did we choose this?* |

Semantic without episodic: agents agree on definitions but have no history
to build on. Episodic without semantic: agents accumulate reasoning traces
but drift on the meaning of the words they use. Together, they form a
reasoning commons that survives across sessions and across agents.

> **A note on the hashes in this doc.** The examples below use live canonical
> hashes from the current sema vocabulary (`StateLock#7cd8`,
> `MechanisticDesignProposal#4c39`). Refinement can change a hash. If a
> handshake returns `HALT` instead of `PROCEED`, run `sema show <handle>`
> to see the current canonical stub — that's the fail-closed protocol
> working as designed, not a doc bug.

## Install both

```bash
claude mcp add sema -- uvx --from "semahash[mcp]" sema mcp
claude mcp add ug   -- npx -y understanding-graph mcp
```

Verify:

```
claude mcp list
```

You should see both `sema` and `ug` listed as active.

## Pattern: handshake before deciding

Before writing a `decision` node in Understanding Graph that depends on a
shared concept (a lock, a protocol, a verification step), run a `sema`
handshake first:

```
sema_handshake({ ref: "StateLock#7cd8" })
```

- If the verdict is `PROCEED`, both agents share the same byte-exact
  definition of `StateLock`. Safe to write the decision node and commit.
- If the verdict is `HALT`, the definitions have drifted. Do *not* write a
  decision. Write a `tension` node instead, capturing the drift, so other
  agents can see why work is blocked.

## Pattern: pin the hash inside the graph node

When you *do* write a decision, embed the sema hash inside the node's
`mechanism` field. This turns the coordination primitive into a
content-addressed reference that cannot drift:

```
graph_batch({
  commit_message: "Architect: chose StateLock for session mutex",
  operations: [{
    op: "add_concept",
    trigger: "decision",
    title: "Session mutex via StateLock",
    mechanism: "Use sema://StateLock#7cd8 for session-level mutex.",
    explanation: "StateLock gives fail-closed semantics; verified via sema_handshake before commit."
  }]
})
```

Later, any teammate who reads this node can re-run the handshake on
`StateLock#7cd8` to verify the definition is still the same one the original
architect used.

## Pattern: discover past uses of a sema pattern

To find every graph node that has ever referenced a sema pattern:

```
graph_semantic_search({ query: "StateLock#7cd8" })
```

Because sema hashes are content-addressed, you're guaranteed to be reading
history about the *same* `StateLock`, not a renamed or drifted version.

## Minimal two-agent coordination recipe

**Agent A (Architect)** — `CLAUDE.md`:

```markdown
1. graph_skeleton() to orient.
2. Before posting a design, sema_handshake on MechanisticDesignProposal#4c39.
3. If PROCEED, write a `decision` node via graph_batch, citing the hash.
4. If HALT, write a `tension` node and stop.
```

**Agent B (Engineer)** — `CLAUDE.md`:

```markdown
1. graph_history() to see what the Architect posted.
2. For any `decision` node that cites a sema hash, run sema_handshake first.
3. Only implement after PROCEED. Log the handshake result as a `thinking`
   node.
```

This recipe guarantees:

- Definitions are stable (semantic memory, via sema).
- The design trail is legible (episodic memory, via the graph).
- Drift causes an explicit HALT, not a silent failure.

## See also

- [Sema README — Install](../../README.md#install) — MCP server setup for any client
- [Understanding Graph integrations](https://github.com/emergent-wisdom/understanding-graph/tree/main/integrations) — per-client setup guides
- [Understanding Graph: using-with-sema](https://github.com/emergent-wisdom/understanding-graph/blob/main/docs/using-with-sema.md) — the mirror walkthrough
