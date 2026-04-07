# Staging Directory

Place new pattern JSON files here before applying them to the vocabulary.

## Workflow

```bash
# 1. Create your pattern
vim data/staging/MyPattern.json

# 2. Validate (dry run)
sema apply --check --add data/staging/MyPattern.json

# 3. Apply to database
sema apply --add data/staging/MyPattern.json

# 4. Export updated vocabulary
PYTHONPATH=src python3 scripts/export/export_sema.py

# 5. Delete the staging file (it's now in data/vocabulary/)
rm data/staging/MyPattern.json
```

See [Pattern Authoring Guide](../../docs/specification/authoring.md) for the full schema and rules.
