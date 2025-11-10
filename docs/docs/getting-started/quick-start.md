---
sidebar_position: 2
title: Quick Start
---

# Quick Start Guide

Get up and running with Repository Analytics in under 5 minutes!

## Choose Your Script

Depending on your needs, choose one of these quick paths:

### Path 1: Basic Stats (Fastest)

For simple commit and language statistics without charts:

```bash
python generate_stats.py
```

**Use when**: You want quick stats without installing dependencies.

### Path 2: Enhanced Analytics

For comprehensive analytics with visual charts:

```bash
# Install dependencies first
pip install matplotlib pandas

# Run the script
python generate_stats2.py
```

**Use when**: You want beautiful charts and detailed analytics.

### Path 3: Template-Based

For clean README generation from templates:

```bash
python generate_stats_fromtemplate_withgraphs.py
```

**Use when**: You want to keep your template separate from output.

## Step-by-Step Quick Start

### 1. Set Up Your README

Add analytics markers to your `README.md`:

````markdown
# My Project

Project description here...

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- This will be replaced with analytics -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- Language breakdown will appear here -->
<!-- STATS BREAKDOWN END:LANGUAGE -->
````markdown

### 2. Run a Script

```bash
python generate_stats.py
```

### 3. Check the Results

Open `README.md` to see your updated analytics!

````markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->

### 📊 Repository Stats

| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 45 | +12,345 / -6,789 | 19,134 | PY(8500), JS(4200), MD(1200) |
| Last 30 Days | 12 | +2,300 / -890 | 3,190 | PY(1800), JS(900) |

<!-- STATS BREAKDOWN END:OVERVIEW -->
````markdown

## 5-Minute Tutorial

Let's create a complete setup from scratch:

### Step 1: Prepare Your Repository (1 min)

```bash
cd your-repository
```

### Step 2: Add Analytics Markers (2 min)

Edit your `README.md`:

```markdown
# Your Project Name

<!-- STATS BREAKDOWN START:PULSE -->
<!-- STATS BREAKDOWN END:PULSE -->

## Features
- Feature 1
- Feature 2

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

<!-- STATS BREAKDOWN START:LANGUAGE -->
<!-- STATS BREAKDOWN END:LANGUAGE -->

<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->
```

### Step 3: Copy the Script (30 sec)

```bash
# Download the script
curl -O https://raw.githubusercontent.com/your-org/analrepo/main/generate_stats.py
```

Or copy it manually from the repository.

### Step 4: Run the Script (30 sec)

```bash
python generate_stats.py
```

### Step 5: Commit Your Changes (1 min)

```bash
git add README.md
git commit -m "Add repository analytics"
git push
```

Done! Your README now has live analytics.

## Quick Configuration

Want to customize your analytics? Add a config block:

```markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last 90 Days": "90d",
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
```

## Script Comparison Quick Reference

| Feature | stats.py | stats2.py | stats3.py | stats4.py | fromtemplate.py | fromtemplate_withgraphs.py |
|---------|----------|-----------|-----------|-----------|-----------------|----------------------------|
| **No dependencies** | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Visual charts** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Config from README** | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Template-based** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Real language data** | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Multiple blocks** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Common Quick Scenarios

### Scenario 1: Personal Project
**Goal**: Simple stats, no charts

```bash
python generate_stats.py
```

### Scenario 2: Open Source Project
**Goal**: Professional analytics with charts

```bash
pip install matplotlib pandas
python generate_stats_fromtemplate_withgraphs.py
```

### Scenario 3: Team Dashboard
**Goal**: Contributor tracking and trends

```bash
pip install matplotlib pandas
python generate_stats2.py
```

### Scenario 4: Automated GitHub Action
**Goal**: Daily analytics updates

See [GitHub Actions Guide](/docs/advanced/github-actions) for details.

## Troubleshooting Quick Fixes

### No markers found
**Fix**: Add markers to your README.md

### Module not found
**Fix**: Install dependencies
```bash
pip install matplotlib pandas
```

### No git repository
**Fix**: Initialize git
```bash
git init
```

### Empty output
**Fix**: Make sure you have commits
```bash
git log  # Should show commits
```

## Next Steps

Now that you're up and running:

- **Learn More**: Read [Basic Usage](/docs/getting-started/basic-usage)
- **Customize**: Check out [Configuration](/docs/configuration)
- **Advanced**: Explore [Scripts Reference](/docs/category/scripts-reference)
- **Automate**: Set up [GitHub Actions](/docs/advanced/github-actions)

## Quick Tips

1. **Run regularly**: Set up a cron job or GitHub Action
2. **Customize timeframes**: Adjust to your release cycle
3. **Ignore files**: Exclude lock files and build artifacts
4. **Test first**: Run locally before committing
5. **Backup README**: Keep a copy before first run

## Quick Command Reference

```bash
# Basic run
python generate_stats.py

# With virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install matplotlib pandas
python generate_stats2.py

# From template
python generate_stats_fromtemplate_withgraphs.py

# Check what changed
git diff README.md

# Commit analytics
git add README.md stats/
git commit -m "Update analytics"
git push
```

That's it! You're now generating repository analytics. 🎉
