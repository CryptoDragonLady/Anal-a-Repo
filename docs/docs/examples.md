---
sidebar_position: 6
title: Examples
---

# Usage Examples

Real-world examples demonstrating different use cases and configurations.

## Example 1: Personal Blog Repository

### Scenario
Personal project with minimal commits, want simple stats without charts.

### Setup

**README.md**:
````markdown
# My Blog

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
````markdown

**Command**:
```bash
python generate_stats.py
````markdown

### Output

```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->

### 📊 Repository Stats

| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 23 | +3,456 / -1,234 | 4,690 | MD(2500), CSS(800), HTML(600) |
| Last 30 Days | 5 | +245 / -89 | 334 | MD(200), CSS(100) |
| Last 7 Days | 2 | +45 / -12 | 57 | MD(50) |
| Last 24 Hours | 0 | +0 / -0 | 0 | — |

<!-- STATS BREAKDOWN END:OVERVIEW -->
````markdown

## Example 2: Open Source Project with Charts

### Scenario
Active open source project, want professional analytics with visual charts.

### Setup

**README_TEMPLATE.md**:
````markdown
# Awesome Library

![Logo](logo.png)

<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last Quarter": 90,
    "Last Month": 30,
    "Last Week": 7
  },
  "languages": {
    "ignore": ["lock", "min", "map"]
  },
  "sections": {
    "include": ["PULSE", "OVERVIEW", "LANGUAGE", "COMMITS"]
  }
}
```

</details>

## Project Metrics

<!-- STATS BREAKDOWN START:PULSE -->
<!-- STATS BREAKDOWN END:PULSE -->

## Contributors

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

## Languages

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- STATS BREAKDOWN END:LANGUAGE -->

## Activity

<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->
````markdown

**Command**:
```bash
pip install matplotlib pandas
python generate_stats_fromtemplate_withgraphs.py
```

### Output

Clean README.md with:
- Pulse metrics (total commits, contributors, etc.)
- Contributor tables for each timeframe
- Language pie charts saved as PNG
- Commit activity line graphs

## Example 3: Team Sprint Dashboard

### Scenario
Agile team tracking 2-week sprints, need detailed contributor analytics.

### Setup

**README.md with config**:
````markdown
# Project Dashboard

<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "Project Total": null,
    "Current Sprint": "14d",
    "Last Sprint": "28d",
    "This Week": "7d"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json", "yaml"]
  },
  "contributors": {
    "show": true,
    "max": 20
  }
}
```

</details>

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
````

**Command**:
```bash
python generate_stats4.py
```

### Output

Stats table with current sprint data and language breakdown with visual bars.

## Example 4: Multilingual Project

### Scenario
Project with Python backend, JavaScript frontend, want to track both separately.

### Setup

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last Month": "30d"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json", "css", "svg"]
  }
}
```

</details>

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
````

**Command**:
```bash
python generate_stats4.py
```

### Output

```
🧠 **Language Breakdown (All Time)**
```
PYTHON     ████████████         52.3%
JAVASCRIPT ██████████           48.7%
```
```

Focuses on main languages, excludes config/style files.

## Example 5: Documentation Repository

### Scenario
Documentation-heavy repo, mostly Markdown files.

### Setup

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last Quarter": "90d",
    "Last Month": "30d"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": []
  }
}
```

</details>

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
````

### Output

```
🧠 **Language Breakdown (All Time)**
```
MARKDOWN   ████████████████████ 87.3%
YAML       ██                    8.2%
JSON       █                     3.1%
OTHER      ░                     1.4%
```
```

## Example 6: Automated Daily Updates

### Scenario
Automatically update README every day with latest stats.

### Setup

**GitHub Actions** (`.github/workflows/analytics.yml`):

```yaml
name: Update Analytics

on:
  schedule:
    - cron: "0 0 * * *"  # Daily at midnight UTC
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      
      - name: Install dependencies
        run: pip install matplotlib pandas
      
      - name: Generate analytics
        run: python generate_stats_fromtemplate_withgraphs.py
      
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "actions@github.com"
          git add README.md stats/
          git diff --quiet && git diff --staged --quiet || \
            (git commit -m "Update analytics [skip ci]" && git push)
```

**Result**: README automatically updates daily.

## Example 7: Pre-Commit Hook

### Scenario
Update stats automatically before every commit.

### Setup

**.git/hooks/pre-commit**:

```bash
#!/bin/bash

echo "Updating repository analytics..."
python generate_stats.py

if [ -f README.md ]; then
  git add README.md
  echo "✓ Analytics updated"
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

**Result**: Stats update on every commit.

## Example 8: Multi-Repository Dashboard

### Scenario
Track analytics across multiple repositories.

### Setup

**update_all.sh**:

```bash
#!/bin/bash

repos=(
  "/path/to/repo1"
  "/path/to/repo2"
  "/path/to/repo3"
)

for repo in "${repos[@]}"; do
  echo "Updating $repo..."
  cd "$repo"
  python generate_stats2.py
  git add README.md stats/
  git commit -m "Update analytics" || true
  git push
done

echo "All repositories updated!"
```

**Cron job**:
```bash
0 2 * * * /path/to/update_all.sh
```

## Example 9: Custom Timeframes for Releases

### Scenario
Track stats aligned with release cycles.

### Setup

```json
{
  "timeframes": {
    "All Releases": null,
    "v2.0 Cycle": "120d",
    "v1.9 Cycle": "240d",
    "Current Month": "30d"
  }
}
```

**Output**: Analytics aligned with release history.

## Example 10: Minimal Configuration

### Scenario
Use defaults, minimal setup.

### Setup

**README.md**:
````markdown
# Simple Project

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
````

**Command**:
```bash
python generate_stats.py
```

**Result**: Works with all defaults, no config needed.

## Tips and Tricks

### Tip 1: Hide Config from Users

Use template mode to keep config out of final README:

```bash
# Edit README_TEMPLATE.md with config
python generate_stats_fromtemplate.py
# README.md is clean
```

### Tip 2: Focus on Recent Activity

```json
"timeframes": {
  "Last Week": "7d",
  "Last Day": "24h"
}
```

### Tip 3: Exclude Test Commits

Add `[skip analytics]` to commit messages and filter in custom script.

### Tip 4: Multiple Sections

```markdown
## Backend Stats
<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

## Frontend Activity
<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->
```

### Tip 5: Version Control Charts

Commit `stats/` directory:
```bash
git add stats/*.png
git commit -m "Update analytics charts"
```

## Common Patterns

### Pattern 1: Weekly Review

```bash
# Every Monday morning
0 9 * * 1 cd /repo && python generate_stats.py && git push
```

### Pattern 2: Release Notes

```bash
# Generate stats before release
python generate_stats2.py
git add README.md stats/
git commit -m "Update stats for v1.2.0"
git tag v1.2.0
git push --tags
```

### Pattern 3: Pull Request Stats

Include stats in PR description:
```bash
python generate_stats.py
# Copy output to PR
```

## See Also

- [GitHub Actions Guide](/docs/advanced/github-actions)
- [Custom Templates](/docs/advanced/custom-templates)
- [Troubleshooting](/docs/troubleshooting)
