---
sidebar_position: 3
title: Basic Usage
---

# Basic Usage

Learn the fundamentals of using Repository Analytics scripts to generate comprehensive repository statistics.

## Understanding the Workflow

All scripts follow a similar workflow:

1. **Read** repository data using Git commands
2. **Parse** configuration (if applicable)
3. **Process** commit, diff, and language data
4. **Generate** analytics content
5. **Update** README.md with new statistics

## Script Execution Basics

### Running a Script

The simplest form:

```bash
python generate_stats.py
```

### With Python 3 Explicitly

```bash
python3 generate_stats.py
```

### Make Script Executable (Linux/macOS)

```bash
chmod +x generate_stats.py
./generate_stats.py
```

## Understanding Markers

Markers define where analytics should be inserted in your README.

### Basic Marker Syntax

```markdown
<!-- STATS BREAKDOWN START:BLOCK_TYPE -->
Content will be replaced here
<!-- STATS BREAKDOWN END:BLOCK_TYPE -->
```

### Supported Block Types

- `OVERVIEW`: Repository stats table and summaries
- `LANGUAGE`: Language breakdown with optional charts
- `COMMITS`: Commit activity trends
- `PULSE`: Quick stats (total commits, contributors, etc.)

### Example Setup

```markdown
# My Project

## Analytics

<!-- STATS BREAKDOWN START:PULSE -->
<!-- STATS BREAKDOWN END:PULSE -->

## Detailed Statistics

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

## Language Analysis

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- STATS BREAKDOWN END:LANGUAGE -->

## Activity Trends

<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->
```

## Script-Specific Usage

### generate_stats.py - Basic Stats

Best for: Quick stats without dependencies

```bash
python generate_stats.py
```

**Features**:
- No external dependencies
- Multiple timeframes
- Language detection by file extension
- Marker-based updates

**Output**:
- Stats table with commits, additions, deletions
- Language counts by extension
- Multiple timeframe analysis

### generate_stats2.py - Enhanced Analytics

Best for: Visual analytics with charts

```bash
pip install matplotlib pandas
python generate_stats2.py
```

**Features**:
- Pie charts for language breakdown
- Line charts for commit activity
- Contributor detailed analytics
- Saves charts to `stats/` directory

**Output**:
- Contributor tables with language breakdown
- PNG charts embedded in README
- Pulse metrics

### generate_stats3.py - Config-Based

Best for: Customized analytics from README config

```bash
python generate_stats3.py
```

**Features**:
- Reads JSON config from README
- Customizable timeframes (d/h format)
- Ignore specific file types
- Graph customization

**Output**:
- Configured analytics blocks
- Respects ignore lists
- Custom time periods

### generate_stats4.py - Real Language Data

Best for: Accurate language statistics

```bash
python generate_stats4.py
```

**Features**:
- Real language calculations (not placeholders)
- Visual progress bars for languages
- Better error handling
- Percentage breakdowns

**Output**:
- Accurate language percentages
- Visual representation with bars
- Sorted by usage

### generate_stats_fromtemplate.py - Template Mode

Best for: Clean README generation

```bash
python generate_stats_fromtemplate.py
```

**Features**:
- Reads from `README_TEMPLATE.md`
- Generates clean `README.md`
- Removes config blocks from output
- Removes all markers

**Workflow**:
1. Edit `README_TEMPLATE.md` with your content
2. Add analytics markers
3. Add config in `<details>` block
4. Run script
5. Get clean `README.md` without markers

### generate_stats_fromtemplate_withgraphs.py - Full Featured

Best for: Complete analytics with all features

```bash
pip install matplotlib pandas
python generate_stats_fromtemplate_withgraphs.py
```

**Features**:
- Template-based generation
- All analytics blocks (OVERVIEW, LANGUAGE, COMMITS, PULSE)
- Visual charts saved to `stats/`
- Comprehensive contributor data

**Output**:
- Clean README with all analytics
- Multiple PNG charts
- Complete statistics

## Working with Timeframes

### Default Timeframes

Most scripts support these timeframes:

```python
{
  "All Time": None,
  "Last 30 Days": 30,    # or "30d"
  "Last 7 Days": 7,      # or "7d"
  "Last 24 Hours": 1     # or "24h"
}
```

### Custom Timeframes

Edit configuration to customize:

```json
{
  "timeframes": {
    "All Time": null,
    "Last Quarter": "90d",
    "Last Month": "30d",
    "Last Week": "7d",
    "Last Day": "24h",
    "Last Hour": "1h"
  }
}
```

### Timeframe Formats

- `null` or `"all"`: All commits in repository
- `"30d"`: Last 30 days
- `"24h"`: Last 24 hours
- Number: Days (for scripts using numeric format)

## Configuration Methods

### Method 1: Inline JSON Config (stats3, stats4)

Add to your README.md:

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last 30 Days": "30d"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json"]
  },
  "graphs": {
    "show": true,
    "color": "#4e79a7"
  }
}
```

</details>
````

### Method 2: Template-Based (fromtemplate scripts)

Add to `README_TEMPLATE.md`:

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "sections": {
    "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
  }
}
```

</details>
````

### Method 3: Defaults (all scripts)

If no config is provided, scripts use sensible defaults.

## Common Workflows

### Workflow 1: Daily Updates

```bash
#!/bin/bash
cd /path/to/repo
python generate_stats2.py
git add README.md stats/
git commit -m "Update analytics [skip ci]"
git push
```

### Workflow 2: Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python generate_stats.py
git add README.md
```

### Workflow 3: Manual Review

```bash
# Generate stats
python generate_stats.py

# Review changes
git diff README.md

# Commit if satisfied
git add README.md
git commit -m "Update repository analytics"
```

### Workflow 4: Multi-Repo

```bash
#!/bin/bash
for repo in repo1 repo2 repo3; do
  cd /path/to/$repo
  python ../analrepo/generate_stats.py
  git add README.md
  git commit -m "Update analytics"
  git push
done
```

## Best Practices

### 1. Version Control

Always commit the scripts to your repository:

```bash
cp /path/to/analrepo/*.py scripts/
git add scripts/
git commit -m "Add analytics scripts"
```

### 2. Ignore Generated Files

Add to `.gitignore` if you don't want to commit charts:

```
stats/*.png
stats/*.jpg
```

### 3. Test Before Commit

```bash
# Dry run - check diff before committing
python generate_stats.py
git diff README.md

# Revert if needed
git checkout README.md
```

### 4. Document Your Setup

Add a note to your README:

```markdown
## Analytics

Repository analytics are automatically generated using [Repository Analytics](https://github.com/your-org/analrepo).

To update: `python generate_stats.py`
```

### 5. Schedule Regular Updates

Use cron, GitHub Actions, or CI/CD to run regularly.

## Reading the Output

### Stats Table

```markdown
| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 45 | +12,345 / -6,789 | 19,134 | PY(8500), JS(4200) |
```

**Columns**:
- **Period**: Timeframe being analyzed
- **Commits**: Number of commits in period
- **Additions/Deletions**: Lines added and removed
- **Total Lines**: Sum of additions and deletions
- **Languages**: File types with line counts

### Language Breakdown

```
PYTHON     ████████████████████ 45.5%
JAVASCRIPT █████████            22.3%
MARKDOWN   ████                 12.1%
OTHER      ████                 20.1%
```

**Format**:
- Language name (left-aligned)
- Visual bar (filled blocks)
- Percentage of total lines

### Contributor Table

```markdown
| Contributor | Commits | +Add | -Del | Total | Top Languages |
|-------------|----------|------|------|-------|----------------|
| John Doe | 25 | 5,234 | 1,890 | 7,124 | Python (4500), JS (1200) |
```

**Columns**:
- **Contributor**: Git author name
- **Commits**: Number of commits
- **+Add**: Lines added
- **-Del**: Lines deleted
- **Total**: Add + Del
- **Top Languages**: Most-used languages with line counts

## Troubleshooting Common Issues

### Issue: "No markers found"

**Solution**: Add markers to README.md
```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
```

### Issue: "No analytics config found"

**Solution**: Either add config or script will use defaults

### Issue: Empty statistics

**Cause**: No commits in repository
**Solution**: Make some commits first

### Issue: Old data showing

**Cause**: Git cache or script not running
**Solution**: 
```bash
git pull  # Get latest commits
python generate_stats.py  # Regenerate
```

## Next Steps

- **Customize**: Learn about [Configuration](/docs/configuration)
- **Explore**: Read detailed [Scripts Reference](/docs/category/scripts-reference)
- **Automate**: Set up [GitHub Actions](/docs/advanced/github-actions)
- **Examples**: See real-world [Examples](/docs/examples)
