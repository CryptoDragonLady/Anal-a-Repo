---
title: API Overview
description: High-level overview of the repository analytics scripts and their responsibilities.
---

The analytics system is implemented with small Python utilities that read Git history and write Markdown.

Key scripts:

- generate_stats.py: Basic block updater that writes stats tables and simple graphs
- generate_stats2.py/3.py/4.py: Variants exploring different output styles and config handling
- .github/scripts/generate_stats_fromtemplate_withgraphs.py: Full README generator from a template, producing image charts
- .github/scripts/generate_stats_new.py and generate_stats_new2.py: Enhanced in-place block updates with configurable timeframes and language breakdowns

Common responsibilities:

- Query Git commits and diffs over configurable timeframes
- Aggregate additions, deletions, and per-language totals
- Render tables, ASCII charts, or image charts
- Update content between explicit Markdown markers

Related CI integration is documented in Advanced → GitHub Actions.