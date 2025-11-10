---
title: GitHub Actions Integration
description: Automate analytics generation and commit updates on pushes to main.
---

The repository includes a ready-to-use GitHub Actions workflow that regenerates analytics and commits updates.

Workflow summary:

```yaml
name: Repository Analytics
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  generate-stats:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install gitpython pandas matplotlib pygments
      - run: python .github/scripts/generate_stats_fromtemplate_withgraphs.py
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md stats/
          git commit -m "Update repo analytics [skip ci]" || echo "No changes"
          git push
```

Customization:

- Switch the script to one of the in-place updaters if you prefer keeping markers
- Add cron or schedule triggers for nightly analytics
- Ensure stats/ is tracked so chart images are committed