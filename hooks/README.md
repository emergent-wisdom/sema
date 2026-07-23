# Claude Code ref gate

Enforcement hook for the sema Claude Code plugin. It scans each inbound
message for content-addressed refs (`Handle#stub`), verdicts them against the
active sema registry, and — depending on mode — annotates or refuses delivery.

Detection knowledge lives in sema (the registry holds the canonical stubs);
this hook is the enforcement point, because only the harness can actually
refuse to deliver a message. MCP tool results and skills are voluntary: the
model can ignore them. A hook that exits 2 cannot be ignored.

## What it hooks

Registered via [`hooks.json`](./hooks.json) when the plugin is installed:

| Event              | Matcher                       | Why                                        |
| ------------------ | ----------------------------- | ------------------------------------------ |
| `UserPromptSubmit` | (all prompts)                 | refs arriving from the user or an upstream agent |
| `PreToolUse`       | `Agent\|Task\|SendMessage`    | refs being relayed onward to subagents     |

## Verdicts

| Verdict   | Meaning                        | Effect (`warn`)             | Effect (`enforce`)                  |
| --------- | ------------------------------ | --------------------------- | ----------------------------------- |
| `KNOWN`   | handle exists, stub matches    | pass                        | pass                                |
| `STALE`   | handle exists, stub differs    | model-visible warning, pass | **block** (exit 2) + repair message |
| `UNKNOWN` | handle not in registry         | model-visible note, pass    | model-visible note, pass            |

`UNKNOWN` never blocks: the ref pattern can match non-sema text (`PR#12ab`).
The `STALE` repair message carries the canonical stub and tells the model to
re-verify with `sema_handshake` / `sema_resolve` before re-issuing the action.

If the registry cannot be loaded, the gate **fails open** (exit 0, with a
note on stderr) — gate infrastructure must never brick the harness.

## Configuration

Environment variables, resolved per invocation:

| Variable            | Default          | Purpose                                        |
| ------------------- | ---------------- | ---------------------------------------------- |
| `SEMA_REF_GATE`     | `warn`           | `off` \| `warn` \| `enforce`; invalid values warn |
| `SEMA_REF_GATE_DB`  | default registry | path to an alternate registry DB               |
| `SEMA_REF_GATE_LOG` | unset            | append per-invocation verdict JSON to this file |
| `SEMA_PYTHON`       | `python3`        | Python 3.10+ interpreter for the bundled hook   |

The default is `warn` so installing the plugin never surprises anyone with a
blocked action; teams that want drift stopped rather than reported opt in
with `SEMA_REF_GATE=enforce` (e.g. in a project `.claude/settings.json` `env`
block, or exported in the shell).

The hook loads the plugin's own `src/` tree and reads the active registry with
Python's standard library, so installing `sema` into the system interpreter is
not required. Warnings use Claude Code's structured `additionalContext` output
for both prompt submission and pre-tool relay events.

## Why enforce exists

In an exploratory A/B through real Claude Code sessions
([sema-evals babel-hook pilot](https://github.com/RobinOppenstam/sema-evals/tree/main/experiments/babel-hook),
haiku, 60 trials/arm, 3-boundary relay):

- no gate: 70% of drifted work shipped silently
- `warn`: the gate detected every drifted ref, and the relay still shipped
  drifted work in 5/40 trials — the model saw the warning and proceeded anyway
- `enforce`: 40/40 drifted refs blocked before the model call, zero false
  blocks on clean refs

## Implementation note

The gate scans **decoded JSON string values**, not raw payload bytes: hook
payloads are JSON, so a ref at a line start arrives as `\nHandle#stub`, and
the escaped `\n` destroys the regex word boundary (found live in the pilot).

The scan/verdict logic lives in `sema.core.check` (also exposed as the
`sema check` CLI, with a versioned verdict document and exit codes
0 clean / 3 stale / 1 error), so every harness shim — this one, and
equivalents for other harnesses — stays a thin adapter: feed the payload
to check, map the verdict to the harness's block mechanism. A shim claims
support for a harness by passing the shared conformance fixture set in
`src/sema/core/tests/fixtures/refcheck_conformance.json`.

Tests: [`tests/test_ref_gate.py`](./tests/test_ref_gate.py) (in the root
pytest run).
