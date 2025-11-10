---
sidebar_position: 3
title: generate_stats3.py
---

# generate_stats3.py

Config-based analytics that reads configuration from a `<details>` block in your README.

## Overview

`generate_stats3.py` introduces global configuration management by reading JSON settings from your README file. This allows you to configure timeframes, language ignore lists, and graph settings in one central location.

## Key Features

- **Global Configuration**: Single JSON config block controls all analytics
- **Customizable Timeframes**: Use `d` (days) or `h` (hours) format
- **Language Ignore Lists**: Exclude specific file extensions
- **Graph Customization**: Configure colors, sizes, and display options
- **No External Dependencies**: Uses only Python standard library

## Usage

```bash
python generate_stats3.py
```

## Configuration Format

Add this configuration block to your `README.md`:

````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last 90 Days": "90d",
    "Last 30 Days": "30d",
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
    "ignore": ["lock", "json", "min"]
  },
  "contributors": {
    "show": true,
    "max": 10
  }
}
```

</details>
````markdown

## Configuration Options

### Timeframes

Define custom time periods:

```json
"timeframes": {
  "Label": "value"
}
```

**Values**:
- `null` or `"all"`: All commits
- `"30d"`: Last 30 days
- `"24h"`: Last 24 hours
- `"90d"`, `"7d"`, etc.

### Graphs

Control graph display:

```json
"graphs": {
  "show": true,
  "width": 400,
  "height": 120,
  "color": "#4e79a7"
}
```

**Options**:
- `show` (boolean): Display graphs or not
- `width` (int): Graph width in pixels (placeholder)
- `height` (int): Graph height in pixels (placeholder)
- `color` (string): Hex color code

### Languages

Control language analytics:

```json
"languages": {
  "show_breakdown": true,
  "ignore": ["lock", "json", "min", "map"]
}
```

**Options**:
- `show_breakdown` (boolean): Show language breakdown
- `ignore` (array): File extensions to exclude (without dots)

### Contributors

Configure contributor display:

```json
"contributors": {
  "show": true,
  "max": 10
}
```

**Options**:
- `show` (boolean): Display contributors
- `max` (int): Maximum contributors to show (placeholder)

## Output Format

Similar to `generate_stats.py` but respecting configuration:

```markdown
### 📊 Repository Stats

| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 45 | +12,345 / -6,789 | 19,134 | PY(8500), JS(4200) |
| Last 90 Days | 35 | +9,800 / -4,300 | 14,100 | PY(7200), JS(3500) |
| Last 30 Days | 12 | +2,300 / -890 | 3,190 | PY(1800), JS(900) |
```

**Note**: Ignores languages specified in config (e.g., lock, json files)

## How It Works

### 1. Config Parsing

```python
def parse_global_config(readme_text: str) -> dict:
    match = re.search(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>",
        readme_text,
        re.DOTALL | re.IGNORECASE,
    )
    return json.loads(match.group(1).strip())
```

### 2. Timeframe Resolution

```python
def resolve_timeframes(cfg):
    now = datetime.utcnow()
    mapping = {}
    for label, value in cfg["timeframes"].items():
        if value.endswith("d"):
            days = int(value[:-1])
            mapping[label] = (now - timedelta(days=days)).isoformat()
        elif value.endswith("h"):
            hours = int(value[:-1])
            mapping[label] = (now - timedelta(hours=hours)).isoformat()
    return mapping
```

### 3. Language Filtering

```python
def get_diff_stats(commit_range=None, ignored_exts=None):
    ignored_exts = set(ignored_exts or [])
    for line in diff.splitlines():
        ext = Path(filename).suffix.lower().replace(".", "")
        if ext in ignored_exts:
            continue
        language_counts[ext] += add + delete
```

## Example Setup

````markdown
# My Project

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
    "ignore": ["lock", "json", "svg"]
  },
  "graphs": {
    "show": true,
    "color": "#FF6B6B"
  }
}
```

</details>

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
````markdown

## Advanced Usage

### Custom Timeframe Labels

```json
"timeframes": {
  "Project Lifetime": null,
  "Current Sprint": "14d",
  "This Week": "7d",
  "Today": "24h"
}
```

### Ignoring Build Artifacts

```json
"languages": {
  "ignore": ["lock", "min", "map", "bundle", "chunk"]
}
```

### Multiple Ignore Patterns

```json
"languages": {
  "ignore": [
    "lock", "json", "yaml",
    "min", "map",
    "svg", "png", "jpg"
  ]
}
```

## Fallback Behavior

If no config is found:

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

## Comparison with Other Scripts

| Feature | stats.py | stats3.py |
|---------|----------|-----------|
| Configuration | Per-block JSON | Global JSON |
| Timeframe Format | ISO datetime | d/h format |
| Ignore Lists | No | Yes |
| Dependencies | None | None |
| Ease of Config | Medium | Easy |

## Troubleshooting

### Config Not Found

**Symptom**: Warning "No analytics config found in README."

**Solution**: Add config block with proper formatting:
```markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{...}
```

</details>
```

### Invalid JSON

**Symptom**: Warning "Invalid JSON in analytics config"

**Solution**: Validate JSON at [jsonlint.com](https://jsonlint.com)

### Languages Still Showing

**Check**: Extension format in ignore list (no dots):
```json
"ignore": ["lock"]  // Correct
"ignore": [".lock"] // Wrong
```

## See Also

- [generate_stats4.py](/docs/scripts/generate-stats4): Enhanced version with real language data
- [Configuration Guide](/docs/configuration)
- [API Reference - Config Parsing](/docs/api/config-parsing)
