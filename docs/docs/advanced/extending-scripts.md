---
title: Extending the Scripts
description: Add new timeframes, languages, or visualizations to tailor the analytics.
---

Ideas for extension:

- Add weekly or monthly aggregation helpers
- Enrich language mapping for your stack (e.g., Go, Rust, Swift)
- Include contributor graphs (top authors by timeframe)
- Generate HTML reports alongside Markdown

Where to change things:

- Timeframe parsing: resolve_timeframes in generate_stats_new*.py
- Language detection: detect_language in generate_stats_fromtemplate_withgraphs.py
- Markdown insertion: update_block and replace_between_markers helpers

Tips:

- Keep functions small and testable
- Prefer machine-friendly Git options like --numstat
- Validate README markers before writing to avoid accidental corruption