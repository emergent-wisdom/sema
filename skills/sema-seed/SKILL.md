---
name: sema-seed
description: |
  Seed the sema vocabulary by exploring random words. Pull a word from the
  system dictionary, think about it through the sema lens without forcing
  it into a pattern, then mint only if a genuinely useful and distinct
  pattern emerges. Use when the user asks to "seed", "expand", "grow",
  or "explore new patterns for" the vocabulary.
user-invocable: true
allowed-tools: |
  Bash(shuf *)
  Bash(gshuf *)
  Bash(awk *)
  Bash(cat /usr/share/dict/words *)
  mcp__sema__sema_search
  mcp__sema__sema_resolve
  mcp__sema__sema_validate
  mcp__sema__sema_mint
  mcp__sema__sema_use
  mcp__sema__sema_stats
---

# Sema Seed Loop

Generative loop for growing the vocabulary. Pull a random word, think about it openly through the sema lens, mint only if a genuine pattern emerges.

## Preflight (once per session)

1. **Ask the user about oversight.** Default to asking confirmation before each mint:
   > "Do you want to review each pattern before I mint it, or should I mint autonomously when the four checks pass?"
   
   Set this for the session and stick with it unless told to change mode.

2. **Verify minting is enabled.** Check that `sema_mint` is available. If not, tell the user:
   > "Minting isn't enabled. Restart with `SEMA_ALLOW_MINT=true` set in your environment."

3. **Verify the active DB is writable.** Call `sema_use()` (no args) to see current. If it's the bundled DB, tell the user to `sema build my.db --preset full` and `sema_use(db_path="my.db")` first.

4. **Offer the UI.** Ask: *"Want to open the Sema UI to watch new patterns appear?"* If yes, invoke the `sema-ui` skill.

## The run

One word per run, unless the user explicitly asks for more. Most runs end with no mint — that's expected.

**Never dismiss a word before reasoning through it.** Even words that look obviously trivial, overly abstract, or already covered must go through step 2 first. The reasoning itself is the test — you cannot know whether a word names a missing pattern until you have actually tried to compose existing handles around it. Skipping the thinking and jumping straight to "no, this isn't useful" defeats the purpose of the seed loop.

### 1. Pull a random word

```bash
# macOS has shuf via coreutils; if not, use awk:
awk 'BEGIN{srand()} {print rand() "\t" $0}' /usr/share/dict/words | sort -k1,1 | head -1 | cut -f2-
```

Or with `shuf`:

```bash
shuf -n 1 /usr/share/dict/words
```

### 2. Reason about the word using sema patterns

Output **at least 3-4 paragraphs** of reasoning where sema handles are woven through the prose as the load-bearing vocabulary. Not a search summary. Not a definition. An actual chain of thought about the word, with handles doing real work in every paragraph.

Process:
1. Call `sema_search` with a phrase from the word's meaning. Read the top hits.
2. Resolve any handle whose mechanism you're unsure about (`sema_resolve`).
3. Then write the reasoning. Multiple paragraphs. Examples of the right texture:

   *"At first this looks like a `Loop#fb2e` of `Observe#xxxx` against `Decay#a1d4` — but the loop here doesn't restore state, it accumulates a `Trace#9057` that itself becomes the `Signal#f39d`. That's a different mechanism than `Heartbeat#7f88`, which just confirms presence..."*

   *"The `Tension#dd06` here is between `Care#cdfa` (non-transactional maintenance) and `OpportunityCost#xxxx` (the work foregone). Most agents collapse this to one side. The word names the holding of both — a `TensionHold#xxxx`-like posture but applied to..."*

4. Each paragraph should compose handles, compare mechanisms, surface tensions, identify what existing patterns get right and wrong about the concept.

If your output reads like a summary or a definition, you didn't reason with sema. Restart and let the handles structure the argument.

### 3. Evaluate

After the thinking, ask yourself:

- **Did a generalizable mechanism emerge?** Or was the word just an instance of something sema already covers?
- **Is the concept stable?** Does it have non-negotiable invariants?
- **Is it sufficiently distinct?** Run `sema_search` with 2-3 different phrasings of the concept. If anything scores >0.7 similarity, the pattern probably already exists in another form.
- **Does it transfer?** A useful pattern shows up in multiple domains, not just the originating word.

If any answer is "no", **don't mint.** Move to the next word. Most words won't produce patterns. That's expected.

### 4. If it passes — mint

If the user chose **review mode** (the default), present the draft pattern (handle, gloss, one-paragraph mechanism summary, layer/category/tier) and ask: *"Mint this?"* Only mint after they say yes.

If the user chose **autonomous mode**, invoke the `sema-mint` skill directly.

Either way, the mint goes through the full pipeline (validation, dependency wiring, hash) and the new handle is reported.

### 5. End the run

Stop after one word. Tell the user the outcome:
- Word explored
- If minted: the new handle and one-line gloss
- If not minted: one-line reason (already covered, doesn't transfer, no stable invariants, etc.)

If they want another, they can ask.

## Tone

This is exploration, not production. Most iterations should end in "no, this isn't a pattern" — that's a feature. The signal is the rare word that turns out to name something the vocabulary was missing.
