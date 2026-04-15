---
name: sema-ui
description: |
  Launch the Sema web UI at localhost:3030 — interactive pattern browser
  with 3D graph, search, and live updates. Use when the user asks to
  "open the UI", "show the graph", or wants visual access to the vocabulary.
user-invocable: true
allowed-tools: |
  Bash(lsof -ti:3030 *)
  Bash(kill *)
  Bash(sema serve *)
  Bash(SEMA_DB_PATH=* sema serve *)
---

# Sema UI

Launch the local Sema interface at http://localhost:3030.

```bash
lsof -ti:3030 | xargs kill 2>/dev/null
sema serve --port 3030 &
```

Then tell the user: **Open http://localhost:3030**

## What's in the UI

- **Pattern browser** with semantic search, layer/category filters
- **3D graph** at `/graph` showing pattern relationships
- **Documentation** at `/docs`
- **Database switcher** in the top bar — flip between bundled vocabulary, project DBs, and any DB registered via `sema use`
- **Live refresh** every 5 seconds when running locally — new patterns appear in the graph as they're minted

## Remind the user about DB selection

After launching, remind the user: *"The active database is shown in the top bar — click it to switch between the bundled vocabulary and any project DBs you've built."*

This matters because the user might mint patterns into the wrong DB if they don't realize which one is active.
