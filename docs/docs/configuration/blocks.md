---
title: Analytics Blocks
description: Configure which analytics blocks are generated and how they appear in your README or documentation.
---

The repository analytics system uses explicit markers to insert and update content blocks.

Available block types:

- OVERVIEW: High-level stats table, graphs, and language summary
- LANGUAGE: Detailed language breakdown with charts
- COMMITS: Commit activity charts by day
- PULSE: Quick overall numbers like total commits and contributors

Markers used by the scripts:

```md
<!-- STATS BREAKDOWN START:OVERVIEW -->
...content...
<!-- STATS BREAKDOWN END:OVERVIEW -->
```

Select which blocks to include via the README template config:

```json
{
  "sections": {
    "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
  }
}
```

Scripts that work with blocks:

- generate_stats.py and generate_stats2/3/4: update the OVERVIEW/LANGUAGES/COMMITS blocks in-place
- generate_stats_fromtemplate_withgraphs.py: renders all selected blocks and writes a complete README, removing the markers afterward

Best practices:

- Keep markers intact if you rely on incremental updates
- Use the template-based script when you want a fully regenerated README including charts
- Always commit the README and stats/ images together to keep references valid