---
title: Report Generation
description: Build tables, language summaries, and commit graphs from Git data.
---

Tables and summaries:

```python
def generate_table(cfg):
    rows = []
    timeframes = resolve_timeframes(cfg)
    add, delete, langs = get_diff_stats(ignored_exts=cfg["languages"].get("ignore", []))
    # ...compose Markdown table rows...
```

Graphs:

- ASCII graphs for quick visualization in Markdown
- Image charts generated via matplotlib/pandas for richer visuals

Language breakdowns:

- Sum additions + deletions per language for an activity proxy
- Render as bars or pie charts depending on the script used

Outputs are inserted between markers in-place or written to a generated README, depending on which script you run.