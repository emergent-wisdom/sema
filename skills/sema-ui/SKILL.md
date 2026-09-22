---
name: sema-ui
description: |
  Launch the Sema local view at localhost:3030 — pattern browser and a 3D
  graph that grows while you mint. Use when the user asks to "open the UI",
  "show the graph", or wants to watch a vocabulary being built.
user-invocable: true
allowed-tools: |
  Bash(curl -s http://localhost:3030/api/workspace*)
  Bash(sema serve *)
  Bash(uvx --from "semahash[api]" sema serve *)
---

# Sema local view

The local view runs on the user's computer. It shows the vocabulary selected
with `sema use` or `sema_use`, the same database you write to, and follows a
later switch on its own.

First check whether a Sema server is already running on the port:

```bash
curl -s http://localhost:3030/api/workspace
```

If that returns JSON, reuse the running server. Otherwise start one in the
background:

```bash
sema serve --port 3030 --open &
```

Without an installed `sema`, run `uvx --from "semahash[api]" sema serve --port 3030 --open &`.
If another program already uses port 3030, choose a free port instead. Do not
stop a process that you did not start.

Then tell the user: **Open http://localhost:3030** (the graph is at `/graph`).

## What's in the view

- **Vocabulary page** with the active vocabulary's name, whether it is
  writable, its root, and the patterns in card, list, and JSON views
- **3D graph** at `/graph`, which grows in place as you mint: new patterns
  light up, and a live panel lists them and can follow each one
- **Vocabulary switcher** when more than one database is registered
- **Publishing steps** on a writable vocabulary's page for when the user wants
  to share it on semahash.org

The view checks for new patterns every three seconds. If it shows the
read-only bootstrap, the user has no writable vocabulary selected yet: build
one with `sema build` and select it with `sema use` (or `sema_use`) before you
mint.
