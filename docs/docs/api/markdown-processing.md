---
title: Markdown Processing
description: Safe, marker-preserving replacement routines used by the analytics scripts.
---

The scripts update content between explicit markers, preserving the markers themselves.

replace_between_markers

```python
def replace_between_markers(text, start_marker, end_marker, new_inner, count=1):
    pattern = re.compile(rf"({re.escape(start_marker)})(.*?)(\s*{re.escape(end_marker)})", re.DOTALL)
    replacement = rf"\1\n\n{new_inner}\n\3"
    updated, n = pattern.subn(replacement, text, count=count)
    return updated if n > 0 else text
```

update_block

```python
def update_block(text, block_type, content):
    typed_start = f"<!-- STATS BREAKDOWN START:{block_type} -->"
    typed_end   = f"<!-- STATS BREAKDOWN END:{block_type} -->"
    # falls back to untyped markers if present
```

Tips:

- Keep the start/end markers intact if you rely on incremental updates
- If a block is missing, the updater appends a new block at the end of the file