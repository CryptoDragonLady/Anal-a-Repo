---
sidebar_position: 5
title: Configuration Overview
---

# Configuration Guide

Learn how to configure Repository Analytics scripts to match your project's needs.

## Configuration Methods

Different scripts use different configuration approaches:

### Method 1: Inline JSON (stats3, stats4)

Configuration embedded in README.md:

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {...},
  "languages": {...},
  "graphs": {...}
}
```

</details>
````

### Method 2: Per-Block JSON (stats)

Configuration within each stats block:

````markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
```json
{
  "show_graphs": true,
  "show_contributors": true
}
```
<!-- STATS BREAKDOWN END:OVERVIEW -->
````

### Method 3: Template Config (fromtemplate scripts)

Configuration in README_TEMPLATE.md:

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "sections": {
    "include": ["OVERVIEW", "LANGUAGE"]
  }
}
```

</details>
````

## Configuration Structure

### Complete Configuration Example

```json
{
  "timeframes": {
    "All Time": null,
    "Last Quarter": "90d",
    "Last Month": "30d",
    "Last Week": "7d",
    "Last 24 Hours": "24h"
  },
  "graphs": {
    "show": true,
    "width": 400,
    "height": 120,
    "color": "#4e79a7"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json", "min", "map"]
  },
  "contributors": {
    "show": true,
    "max": 10
  },
  "sections": {
    "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
  }
}
```

## Configuration Sections

### Timeframes

Define analysis periods:

```json
"timeframes": {
  "Label": "format"
}
```

**Formats**:
- `null` or `"all"`: All repository history
- `"30d"`: Last 30 days (d = days)
- `"24h"`: Last 24 hours (h = hours)
- `30`: Integer days (some scripts)

**Examples**:

```json
// Quarterly reporting
"timeframes": {
  "All Time": null,
  "Q4 2024": "90d",
  "This Month": "30d"
}

// Sprint-based
"timeframes": {
  "Project Lifetime": null,
  "Current Sprint": "14d",
  "This Week": "7d"
}

// Recent activity
"timeframes": {
  "Last Week": "7d",
  "Last Day": "24h",
  "Last Hour": "1h"
}
```

See [Timeframes Configuration](/docs/configuration/timeframes) for details.

### Languages

Control language analysis:

```json
"languages": {
  "show_breakdown": true,
  "ignore": ["lock", "json"]
}
```

**Options**:
- `show_breakdown` (boolean): Display language statistics
- `ignore` (array): File extensions to exclude (no dots)

**Common Ignore Lists**:

```json
// Exclude generated files
"ignore": ["lock", "min", "map", "bundle"]

// Exclude config/data
"ignore": ["json", "yaml", "yml", "xml"]

// Exclude images
"ignore": ["svg", "png", "jpg", "gif"]

// Combined
"ignore": ["lock", "json", "min", "map", "svg", "bundle"]
```

See [Languages Configuration](/docs/configuration/languages) for details.

### Graphs

Configure graph display:

```json
"graphs": {
  "show": true,
  "width": 400,
  "height": 120,
  "color": "#4e79a7"
}
```

**Options**:
- `show` (boolean): Enable/disable graphs
- `width` (int): Graph width in pixels (placeholder in basic scripts)
- `height` (int): Graph height in pixels (placeholder in basic scripts)
- `color` (string): Hex color code for styling

**Color Examples**:

```json
"color": "#FF6B6B"  // Red
"color": "#4ECDC4"  // Teal
"color": "#45B7D1"  // Blue
"color": "#96CEB4"  // Green
"color": "#FFEAA7"  // Yellow
```

See [Graphs Configuration](/docs/configuration/graphs) for details.

### Contributors

Control contributor display:

```json
"contributors": {
  "show": true,
  "max": 10
}
```

**Options**:
- `show` (boolean): Show contributor statistics
- `max` (int): Maximum contributors to display (placeholder)

### Sections

Select which analytics blocks to generate:

```json
"sections": {
  "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]
}
```

**Available Sections**:
- `OVERVIEW`: Repository statistics table
- `LANGUAGE`: Language breakdown with charts
- `COMMITS`: Commit activity trends
- `PULSE`: Quick metrics summary

See [Blocks Configuration](/docs/configuration/blocks) for details.

## Script-Specific Defaults

### generate_stats.py

```python
DEFAULT_CONFIG = {
    "show_graphs": True,
    "show_language_breakdown": True,
    "show_contributors": True,
    "show_commit_activity": True,
}
```

### generate_stats3.py / stats4.py

```python
DEFAULT_CONFIG = {
    "timeframes": {
        "All Time": None,
        "Last 30 Days": "30d",
        "Last 7 Days": "7d",
        "Last 24 Hours": "24h",
    },
    "graphs": {"show": True, "width": 400, "height": 100, "color": "#4e79a7"},
    "languages": {"show_breakdown": True, "ignore": []},
    "contributors": {"show": True, "max": 10},
}
```

### generate_stats_fromtemplate_withgraphs.py

```python
DEFAULT_BLOCKS = ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]

# Timeframes
"All Time": None,
"Last 30 Days": 30,
"Last 7 Days": 7,
"Last 24h": 1
```

## Configuration Best Practices

### 1. Start Simple

Begin with minimal config and add as needed:

```json
{
  "timeframes": {
    "All Time": null,
    "Last Month": "30d"
  }
}
```

### 2. Match Your Workflow

Align timeframes with your development cycle:

```json
// Agile teams
"timeframes": {
  "Sprint 1": "14d",
  "Sprint 2": "28d"
}

// Monthly releases
"timeframes": {
  "Current Release": "30d",
  "Previous Release": "60d"
}
```

### 3. Ignore Noise

Exclude files that skew statistics:

```json
"languages": {
  "ignore": [
    "lock",      // package-lock.json
    "min",       // minified files
    "map",       // source maps
    "json",      // config files
    "svg"        // images
  ]
}
```

### 4. Validate JSON

Always validate your JSON before committing:
- Use [jsonlint.com](https://jsonlint.com)
- Check for trailing commas
- Verify quote marks

### 5. Document Your Config

Add comments in your README:

````markdown
<details>
<summary>📈 Analytics Config</summary>

Configuration for repository analytics:
- Timeframes match our sprint cycle (2 weeks)
- Ignore lock files and minified code
- Generate all analytics blocks

```json
{...}
```

</details>
````

## Common Configurations

### Personal Project

```json
{
  "timeframes": {
    "All Time": null,
    "Last Month": "30d"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "min"]
  },
  "sections": {
    "include": ["OVERVIEW", "LANGUAGE"]
  }
}
```

### Open Source Project

```json
{
  "timeframes": {
    "All Time": null,
    "Last Quarter": "90d",
    "Last Month": "30d",
    "Last Week": "7d"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json", "md"]
  },
  "sections": {
    "include": ["PULSE", "OVERVIEW", "LANGUAGE", "COMMITS"]
  }
}
```

### Team Dashboard

```json
{
  "timeframes": {
    "All Time": null,
    "This Quarter": "90d",
    "This Month": "30d",
    "This Sprint": "14d",
    "Today": "24h"
  },
  "contributors": {
    "show": true,
    "max": 20
  },
  "sections": {
    "include": ["OVERVIEW", "COMMITS"]
  }
}
```

## Troubleshooting Configuration

### JSON Parse Error

**Error**: "Invalid JSON in analytics config"

**Solution**:
1. Validate at jsonlint.com
2. Check for:
   - Trailing commas
   - Missing quotes
   - Unescaped characters

### Config Not Applied

**Checks**:
1. Config is in correct format for your script
2. Config block is properly formatted
3. Script supports the config option

### Unexpected Behavior

**Debug**:
1. Check default values used
2. Verify config is being parsed
3. Look for error messages in output

## Next Steps

Explore specific configuration topics:

- [Timeframes Configuration](/docs/configuration/timeframes)
- [Blocks Configuration](/docs/configuration/blocks)
- [Languages Configuration](/docs/configuration/languages)
- [Graphs Configuration](/docs/configuration/graphs)
