---
sidebar_position: 6
title: generate_stats_fromtemplate_withgraphs.py
---

# generate_stats_fromtemplate_withgraphs.py

The ultimate analytics script combining template-based generation with visual charts.

## Overview

This script combines the best features of all previous scripts:
- Template-based generation (clean output)
- Visual charts (matplotlib/pandas)
- Multiple analytics blocks
- Comprehensive configuration

## Features

- **Template Mode**: Reads from README_TEMPLATE.md
- **Visual Charts**: Pie charts and line graphs
- **All Blocks**: OVERVIEW, LANGUAGE, COMMITS, PULSE
- **Clean Output**: No markers or config in final README
- **Chart Export**: Saves PNG files to stats/
- **Full Configuration**: Control all aspects via JSON

## Installation

```bash
pip install matplotlib pandas
```

## Usage

```bash
python generate_stats_fromtemplate_withgraphs.py
```

## Complete Example

### README_TEMPLATE.md

````markdown
# Awesome Project

![Banner](banner.png)

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
    "ignore": ["lock", "json", "min"]
  },
  "sections": {
    "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
  }
}
```

</details>

## Project Stats

<!-- STATS BREAKDOWN START:PULSE -->
<!-- STATS BREAKDOWN END:PULSE -->

## Detailed Analytics

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

## Language Distribution

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- STATS BREAKDOWN END:LANGUAGE -->

## Commit Trends

<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->

## Features

- Feature 1
- Feature 2
````markdown

### Generated README.md

```markdown
# Awesome Project

![Banner](banner.png)

## Project Stats

## ⚡ Repository Pulse

- **Total Commits:** 347
- **Contributors:** 12
- **Lines Added:** 145,234
- **Lines Deleted:** 67,890
- **First Commit Date:** 2023-01-15
- **Last Commit Date:** 2024-11-09

## Detailed Analytics

## 📊 Repository Analytics Overview

### All Time

| Contributor | Commits | +Add | -Del | Total | Top Languages |
|-------------|----------|------|------|--------|----------------|
| Alice | 120 | 15,234 | 5,678 | 20,912 | Python (12000), JavaScript (4500) |
| Bob | 85 | 8,900 | 3,200 | 12,100 | JavaScript (7000), CSS (2100) |

### Last Quarter

...

## Language Distribution

## 🧠 Language Breakdown

### All Time
![All Time Language Breakdown](stats/lang_all_time.png)

### Last Quarter
![Last Quarter Language Breakdown](stats/lang_last_quarter.png)

## Commit Trends

## 📈 Commit Activity Trends

### All Time
![All Time Commit Activity](stats/activity_all_time.png)

### Last Quarter
![Last Quarter Commit Activity](stats/activity_last_quarter.png)

## Features

- Feature 1
- Feature 2
```

**Note**: All markers and config removed, charts embedded!

## Generated Files

```
your-repo/
├── README_TEMPLATE.md (source)
├── README.md (generated)
├── generate_stats_fromtemplate_withgraphs.py
└── stats/
    ├── lang_all_time.png
    ├── lang_last_quarter.png
    ├── lang_last_month.png
    ├── lang_last_week.png
    ├── activity_all_time.png
    ├── activity_last_quarter.png
    ├── activity_last_month.png
    └── activity_last_week.png
```

## Configuration

### Timeframes

```json
"timeframes": {
  "All Time": null,
  "Last Quarter": 90,
  "Last Month": 30,
  "Last Week": 7,
  "Last 24h": 1
}
```

**Format**: Days as integers or null for all time

### Languages

```json
"languages": {
  "ignore": ["lock", "json", "min", "map"]
}
```

**Effect**: Excludes matching extensions from analysis

### Sections

```json
"sections": {
  "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
}
```

**Options**:
- `OVERVIEW`: Contributor tables
- `LANGUAGE`: Language pie charts
- `COMMITS`: Activity line charts
- `PULSE`: Quick metrics

## Block Generators

### OVERVIEW

```python
def generate_overview_block(timeframes, ignored_exts):
    # Per-contributor stats for each timeframe
    # Commits, additions, deletions, top languages
    return markdown_tables
```

### LANGUAGE

```python
def generate_language_block(timeframes, ignored_exts):
    # Language aggregation
    # Pie chart generation
    # Image embedding
    return markdown_with_images
```

### COMMITS

```python
def generate_commit_activity_block(timeframes):
    # Daily commit counts
    # Time series charts
    # Trend visualization
    return markdown_with_charts
```

### PULSE

```python
def generate_pulse_block():
    # Total commits, contributors
    # Lines added/deleted
    # First/last commit dates
    return markdown_stats
```

## Chart Specifications

### Language Pie Charts

- **Size**: 5x5 inches
- **DPI**: 150
- **Format**: PNG
- **Features**: Percentages, legends, color-coded

### Commit Activity Charts

- **Size**: 6x3 inches
- **DPI**: 150
- **Format**: PNG
- **Features**: Daily frequency, grid lines, smooth curves

## Advanced Configuration

### Full Config Example

```json
{
  "timeframes": {
    "All Time": null,
    "Last Year": 365,
    "Last Quarter": 90,
    "Last Month": 30,
    "Last Week": 7,
    "Yesterday": 1
  },
  "languages": {
    "ignore": ["lock", "json", "svg", "min", "map", "bundle"]
  },
  "sections": {
    "include": ["PULSE", "OVERVIEW", "LANGUAGE", "COMMITS"]
  }
}
```

### Minimal Config

```json
{
  "timeframes": {
    "All Time": null,
    "Last Month": 30
  },
  "sections": {
    "include": ["OVERVIEW"]
  }
}
```

## Workflow Integration

### Daily Updates

```bash
#!/bin/bash
cd /path/to/repo
python generate_stats_fromtemplate_withgraphs.py
git add README.md stats/
git commit -m "Update analytics [skip ci]"
git push
```

### GitHub Actions

```yaml
name: Update Analytics

on:
  schedule:
    - cron: "0 0 * * *"  # Daily
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: pip install matplotlib pandas
      - name: Generate analytics
        run: python generate_stats_fromtemplate_withgraphs.py
      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "actions@github.com"
          git add README.md stats/
          git diff --quiet || git commit -m "Update analytics"
          git push
```

## Performance

**Typical Execution Times**:
- Small repo (&lt;1K commits): 5-10 seconds
- Medium repo (1K–10K commits): 10-30 seconds
- Large repo (&gt;10K commits): 30-60 seconds

**Bottlenecks**:
- Git operations: 40%
- Chart generation: 40%
- Data processing: 20%

## Troubleshooting

### Charts Not Generating

**Check**:
1. matplotlib and pandas installed
2. Write permissions for stats/ directory
3. No font errors in matplotlib

### Large File Sizes

**Solution**: Reduce DPI or figure sizes:
```python
plt.savefig(chart_path, dpi=100)  # Lower DPI
plt.subplots(figsize=(4, 4))      # Smaller size
```

### Memory Issues

**Solution**: Process timeframes individually or reduce data points

## Best Practices

1. **Commit Both Files**: Template and generated README
2. **Version Control Charts**: Include stats/ in repo
3. **Ignore Temp Files**: Add .gitignore for temporary data
4. **Test Locally**: Verify before automating
5. **Document Setup**: Note dependencies in README

## Comparison

| Feature | Basic Scripts | Template Scripts | This Script |
|---------|---------------|------------------|-------------|
| Template Mode | ❌ | ✅ | ✅ |
| Visual Charts | ❌/✅ | ❌ | ✅ |
| All Blocks | ❌ | ❌ | ✅ |
| Clean Output | ❌ | ✅ | ✅ |
| Dependencies | None/Some | None | Required |

## See Also

- [Examples](/docs/examples): Real-world usage
- [GitHub Actions](/docs/advanced/github-actions): Automation setup
- [Configuration Guide](/docs/configuration): Full config reference
