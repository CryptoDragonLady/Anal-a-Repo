---
sidebar_position: 2
title: generate_stats2.py
---

# generate_stats2.py

Enhanced repository analytics with pandas and matplotlib for visual charts and comprehensive data analysis.

## Overview

`generate_stats2.py` takes repository analytics to the next level by generating visual charts (pie charts and line graphs) and providing detailed contributor analytics. This script requires external dependencies but produces professional-quality visualizations.

## Features

- **Visual Charts**: Pie charts for language breakdown, line charts for commit activity
- **PNG Output**: Saves charts to `stats/` directory
- **Pandas Integration**: Advanced data processing and time-series analysis
- **Matplotlib Graphs**: Professional, publication-quality charts
- **Contributor Analytics**: Detailed per-contributor breakdowns
- **Multiple Blocks**: OVERVIEW, LANGUAGE, COMMITS, PULSE sections
- **Automatic Chart Embedding**: Embeds chart images in README

## Installation

###Dependencies

```bash
pip install matplotlib pandas
```

Or use requirements.txt:

```txt
matplotlib>=3.3.0
pandas>=1.1.0
```

## Usage

### Basic Execution

```bash
python generate_stats2.py
```

### Output

- **README.md**: Updated with analytics and chart links
- **stats/**: Directory with generated PNG charts
  - `lang_all_time.png`
  - `lang_last_30_days.png`
  - `activity_all_time.png`
  - etc.

## Configuration

### Timeframes

```python
TIMEFRAMES = {
    "All Time": None,
    "Last 30 Days": 30,
    "Last 7 Days": 7,
    "Last 24h": 1,
}
```

**Format**: Dictionary where values are days (int) or None for all time.

### Blocks

```python
BLOCKS = ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
```

Add markers for the blocks you want in your README.

## Generated Blocks

### OVERVIEW Block

Generates contributor tables for each timeframe:

````markdown
## 📊 Repository Analytics Overview

### All Time

| Contributor | Commits | +Add | -Del | Total | Top Languages |
|-------------|----------|------|------|--------|----------------|
| Alice | 120 | 15,234 | 5,678 | 20,912 | Python (12000), JavaScript (4500) |
| Bob | 85 | 8,900 | 3,200 | 12,100 | JavaScript (7000), CSS (2100) |
```

### LANGUAGE Block

Creates pie charts and embeds them:

````markdown
## 🧠 Language Breakdown

### All Time
![All Time Language Breakdown](stats/lang_all_time.png)

### Last 30 Days
![Last 30 Days Language Breakdown](stats/lang_last_30_days.png)
```

**Chart Features**:
- Pie chart with percentages
- Color-coded segments
- Legend with language names
- 150 DPI resolution

### COMMITS Block

Generates commit activity line charts:

````markdown
## 📈 Commit Activity Trends

### All Time
![All Time Commit Activity](stats/activity_all_time.png)

### Last 30 Days
![Last 30 Days Commit Activity](stats/activity_last_30_days.png)
```

**Chart Features**:
- Daily commit counts
- Time series with date axis
- Grid lines for readability
- Smooth interpolation

### PULSE Block

Quick repository metrics:

```markdown
## ⚡ Repository Pulse

- **Total Commits:** 347
- **Contributors:** 12
- **Lines Added:** 145,234
- **Lines Deleted:** 67,890
- **First Commit Date:** 2023-01-15
- **Last Commit Date:** 2024-11-09
```

## Functions

### `git_log(since_days=None)`

Retrieves git log with numstat data.

**Parameters**:
- `since_days` (int, optional): Limit to last N days

**Returns**: List of tuples `(author, date, additions, deletions, filename)`

### `detect_language(filename)`

Maps file extensions to language names.

**Mapping**:
```python
{
    ".py": "Python",
    ".js": "JavaScript", 
    ".ts": "TypeScript",
    ".md": "Markdown",
    ".html": "HTML",
    ".css": "CSS",
    ".yml": "YAML",
    ".json": "JSON"
}
```

### `plot_language_chart(langs, label)`

Creates pie chart for language distribution.

**Parameters**:
- `langs` (dict): Language counts `{"Python": 8500, "JavaScript": 4200}`
- `label` (str): Chart title suffix

**Returns**: Path object to saved chart

**Chart Specs**:
- Figure size: 5x5 inches
- DPI: 150
- Format: PNG
- Autopct: Percentages to 1 decimal

### `plot_commit_activity(dates, label)`

Creates line chart for commit activity over time.

**Parameters**:
- `dates` (list): List of commit dates (strings)
- `label` (str): Chart title suffix

**Returns**: Path object to saved chart

**Chart Specs**:
- Figure size: 6x3 inches
- DPI: 150
- Daily frequency
- Grid: Dashed, 40% alpha

## Block Generators

### `generate_overview_block()`

Creates comprehensive contributor table with:
- Commit counts per contributor
- Additions and deletions
- Total lines changed
- Top languages per contributor

### `generate_language_block()`

Generates:
- Aggregate language statistics
- Pie chart per timeframe
- Markdown with embedded images

### `generate_commit_activity_block()`

Produces:
- Daily commit counts
- Line chart visualization
- Trend analysis

### `generate_pulse_block()`

Calculates:
- Total commits (all time)
- Unique contributors
- Total lines added/deleted
- First and last commit dates

## Example README Setup

```markdown
# Project Name

<!-- STATS BREAKDOWN START:PULSE -->
<!-- STATS BREAKDOWN END:PULSE -->

## Analytics

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- STATS BREAKDOWN END:LANGUAGE -->

<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->
```

## Advanced Usage

### Customizing Charts

Edit the plotting functions:

```python
def plot_language_chart(langs, label):
    fig, ax = plt.subplots(figsize=(7, 7))  # Larger chart
    colors = ['#ff9999', '#66b3ff', '#99ff99']  # Custom colors
    ax.pie(sizes, labels=names, autopct="%1.1f%%", 
           startangle=140, colors=colors)
    plt.savefig(chart_path, dpi=200)  # Higher resolution
```

### Adding Timeframes

```python
TIMEFRAMES = {
    "All Time": None,
    "Last Quarter": 90,
    "Last Month": 30,
    "Last Week": 7,
    "Yesterday": 1,
}
```

### Filtering Contributors

Modify `generate_overview_block()`:

```python
# Only show contributors with 10+ commits
for author, stats in sorted(contributors.items(), ...):
    if stats['commits'] >= 10:
        output += f"| {author} | ..."
```

## File Structure

```
your-repo/
├── README.md (updated)
├── generate_stats2.py
└── stats/
    ├── lang_all_time.png
    ├── lang_last_30_days.png
    ├── lang_last_7_days.png
    ├── lang_last_24h.png
    ├── activity_all_time.png
    ├── activity_last_30_days.png
    ├── activity_last_7_days.png
    └── activity_last_24h.png
```

## Troubleshooting

### Charts Not Generating

**Check**:
1. matplotlib and pandas installed
2. `stats/` directory exists (script creates it)
3. No permission errors

### Low Quality Charts

**Solution**: Increase DPI in plotting functions:
```python
plt.savefig(chart_path, dpi=300)  # Higher quality
```

### Memory Issues

**Solution**: Reduce figure size or process fewer timeframes:
```python
plt.subplots(figsize=(4, 4))  # Smaller figures
```

### Missing Contributors

**Cause**: `--no-merges` flag in git log
**Solution**: To include merge commits, remove the flag from `git_log()`

## Performance

**Typical Performance**:
- Small repo (&lt;1000 commits): &lt;5 seconds
- Medium repo (1000–10000 commits): 5–15 seconds
- Large repo (&gt;10000 commits): 15–60 seconds

**Optimization Tips**:
1. Reduce number of timeframes
2. Use `--since` to limit history
3. Cache git log results

## Limitations

- **Marker Dependency**: Requires markers in README
- **Fixed Timeframes**: Hardcoded, not configurable from README
- **Language Detection**: By extension only, no content analysis
- **No Template Support**: Directly modifies README.md

## Comparison

| Feature | stats.py | stats2.py |
|---------|----------|-----------|
| Dependencies | None | matplotlib, pandas |
| Visual Charts | Text-based | PNG images |
| Contributor Detail | Basic | Comprehensive |
| Chart Types | None | Pie, Line |
| Performance | Fast | Moderate |

## See Also

- [generate_stats.py](/docs/scripts/generate-stats): Basic version
- [generate_stats_fromtemplate_withgraphs.py](/docs/scripts/generate-stats-fromtemplate-withgraphs): Template + graphs
- [Configuration Guide](/docs/configuration)
