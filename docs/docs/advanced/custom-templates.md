---
title: Custom Templates
description: Use README_TEMPLATE.md and block markers to generate a branded analytics README.
---

Use README_TEMPLATE.md to design your own output and let the script render analytics into it.

Steps:

1. Create README_TEMPLATE.md with your content and insert block markers
2. Add a collapsible “Analytics Config” details block with JSON settings
3. Run .github/scripts/generate_stats_fromtemplate_withgraphs.py locally or via CI

Markers example:

```md
<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- STATS BREAKDOWN END:LANGUAGE -->
```

After generation:

- Markers and the config block are removed from the output
- Charts are saved under stats/ and linked from the README