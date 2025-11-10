---
title: Graphs Configuration
description: Enable or disable graphs, and customize appearance for commit activity charts.
---

The analytics system can generate commit activity charts and language pie charts.

Basic graph configuration:

```json
{
  "graphs": {
    "show": true,
    "width": 400,
    "height": 100,
    "color": "#4e79a7"
  }
}
```

Two rendering modes:

1) Inline ASCII graphs

- Used by generate_stats_new.py and generate_stats_new2.py
- Quick to render and compatible anywhere Markdown is rendered

2) Image charts with matplotlib and pandas

- Used by .github/scripts/generate_stats_fromtemplate_withgraphs.py
- Saves images under stats/ and embeds them into the README
- Produces smoother trends and pie charts

Example output reference:

```md
![Last 30 Days Commit Activity](stats/activity_last_30_days.png)
```

Tip: Commit the stats/ directory along with README changes so chart links remain valid.