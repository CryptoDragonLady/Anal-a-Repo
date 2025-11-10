---
sidebar_position: 1
title: generate_stats.py
---

# generate_stats.py

Basic repository statistics generator with configurable blocks and marker-based README updates.

## Overview

`generate_stats.py` is the foundational script that provides essential repository analytics without requiring external dependencies. It's perfect for quick statistics generation using only Python's standard library.

## Features

- **Zero Dependencies**: Uses only Python standard library (subprocess, pathlib, collections, datetime, json, re)
- **Multiple Timeframes**: Analyze All Time, Last 30 Days, Last 7 Days, Last 24 Hours
- **Configurable Blocks**: Generate OVERVIEW, LANGUAGES, COMMITS sections independently
- **Marker Preservation**: Updates content between markers without removing them
- **JSON Configuration**: Optional per-block configuration support
- **Language Detection**: Automatic language identification by file extension

## Usage

### Basic Execution

```bash
python generate_stats.py
```

This will:
1. Read your `README.md` file
2. Find analytics markers (`<!-- STATS BREAKDOWN START/END -->`)
3. Generate statistics for each marked block
4. Update README with new content, preserving markers

### Prerequisites

- Python 3.6+
- Git repository with commit history
- README.md with analytics markers

## Markers and Blocks

### Supported Block Types

The script supports three block types:

1. **OVERVIEW**: General repository statistics
2. **LANGUAGES**: Language breakdown  
3. **COMMITS**: Commit activity information

### Marker Syntax

#### Typed Markers (Recommended)

```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
Content will be replaced here
<!-- STATS BREAKDOWN END:OVERVIEW -->
```

#### Untyped Markers (Legacy)

```markdown
<!-- STATS BREAKDOWN START -->
Content will be replaced here
<!-- STATS BREAKDOWN END -->
```

**Note**: Typed markers are preferred as they allow multiple blocks in one README.

## Configuration

### Per-Block Configuration

You can configure each block individually by including a JSON config within the markers:

```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
```json
{
  "show_graphs": true,
  "show_language_breakdown": true,
  "show_contributors": true,
  "show_commit_activity": true
}
```
<!-- STATS BREAKDOWN END:OVERVIEW -->
```

### Default Configuration

```python
DEFAULT_CONFIG = {
    "show_graphs": True,
    "show_language_breakdown": True,
    "show_contributors": True,
    "show_commit_activity": True,
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_graphs` | boolean | `true` | Display commit activity graph |
| `show_language_breakdown` | boolean | `true` | Show language distribution |
| `show_contributors` | boolean | `true` | Include contributor statistics |
| `show_commit_activity` | boolean | `true` | Show commit counts |

## Output Format

### Statistics Table

```markdown
### 📊 Repository Stats

| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 45 | +12,345 / -6,789 | 19,134 | PY(8500), JS(4200), MD(1200) |
| Last 30 Days | 12 | +2,300 / -890 | 3,190 | PY(1800), JS(900) |
| Last 7 Days | 3 | +450 / -120 | 570 | PY(300), JS(150) |
| Last 24 Hours | 1 | +50 / -10 | 60 | PY(40), MD(20) |
```

### Commit Activity Graph (Placeholder)

```
Commits by Day:
███████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
```

### Language Breakdown (Placeholder)

```
🧠 **Language Breakdown:** JS ████ 45% | MD ██ 25% | PY ██ 20% | Other ░░ 10%
```

**Note**: This script generates placeholder visualizations. For actual charts, use `generate_stats2.py`.

## How It Works

### Workflow

1. **Read README**: Load existing README.md content
2. **Parse Config**: Extract JSON configuration from each block
3. **Generate Stats**: 
   - Query git log for commit data
   - Calculate diff statistics
   - Aggregate by timeframe and language
4. **Create Sections**: Build markdown content based on config
5. **Update Blocks**: Replace content between markers
6. **Write README**: Save updated README.md

### Timeframe Processing

```python
def timeframes():
    now = datetime.utcnow()
    return {
        "All Time": None,
        "Last 30 Days": (now - timedelta(days=30)).isoformat(),
        "Last 7 Days": (now - timedelta(days=7)).isoformat(),
        "Last 24 Hours": (now - timedelta(hours=24)).isoformat(),
    }
```

### Git Command Execution

```python
def git_log(args):
    result = subprocess.run(
        ["git"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()
```

## Key Functions

### `get_commit_stats(since=None)`

Retrieves commit metadata (hash, author, date) for a given timeframe.

**Parameters**:
- `since` (str, optional): ISO format date to limit commits

**Returns**: List of commit dictionaries

**Example**:
```python
commits = get_commit_stats("2024-01-01")
# Returns: [{"hash": "abc123", "author": "John", "date": "2024-01-15"}, ...]
```

### `get_diff_stats(commit_range=None)`

Computes additions, deletions, and language statistics.

**Parameters**:
- `commit_range` (str, optional): Git commit range

**Returns**: Tuple of (additions, deletions, language_counts)

**Example**:
```python
add, delete, langs = get_diff_stats()
# Returns: (12345, 6789, {"py": 8500, "js": 4200})
```

### `replace_between_markers(readme_text, start_marker, end_marker, new_inner, count=1)`

Replaces content between markers while preserving the markers themselves.

**Parameters**:
- `readme_text` (str): Full README content
- `start_marker` (str): Opening marker
- `end_marker` (str): Closing marker
- `new_inner` (str): New content to insert
- `count` (int): Number of replacements (default: 1)

**Returns**: Updated README text

### `update_block(readme_text, block_type, content)`

Updates a specific analytics block in the README.

**Parameters**:
- `readme_text` (str): Current README content
- `block_type` (str): Type of block (OVERVIEW, LANGUAGES, etc.)
- `content` (str): New content to insert

**Returns**: Updated README text

## Example Setup

### Complete README Template

```markdown
# My Awesome Project

Description of your project...

## Repository Analytics

<!-- STATS BREAKDOWN START:OVERVIEW -->
```json
{
  "show_graphs": true,
  "show_language_breakdown": true,
  "show_contributors": true,
  "show_commit_activity": true
}
```
<!-- STATS BREAKDOWN END:OVERVIEW -->

## Language Analysis

<!-- STATS BREAKDOWN START:LANGUAGES -->
```json
{
  "show_language_breakdown": true
}
```
<!-- STATS BREAKDOWN END:LANGUAGES -->

## Commit Activity

<!-- STATS BREAKDOWN START:COMMITS -->
```json
{
  "show_graphs": true,
  "show_commit_activity": true
}
```
<!-- STATS BREAKDOWN END:COMMITS -->
```

## Advanced Usage

### Multiple Blocks in One README

```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

<!-- STATS BREAKDOWN START:LANGUAGES -->
<!-- STATS BREAKDOWN END:LANGUAGES -->

<!-- STATS BREAKDOWN START:COMMITS -->
<!-- STATS BREAKDOWN END:COMMITS -->
```

Each block will be processed independently with its own configuration.

### Selective Block Generation

Only blocks with markers will be generated. Remove markers for blocks you don't want.

### Configuration Priority

1. Inline JSON config (within markers)
2. Default configuration (in script)

## Limitations

- **Placeholder Visualizations**: Graphs and charts are text-based
- **Basic Language Detection**: By file extension only
- **No Chart Output**: Doesn't generate PNG/SVG files
- **Single README**: Only updates README.md (not README_TEMPLATE.md)

## Upgrade Path

For more advanced features:

- **Visual Charts**: Use `generate_stats2.py`
- **Template Mode**: Use `generate_stats_fromtemplate.py`
- **Combined Features**: Use `generate_stats_fromtemplate_withgraphs.py`

## Troubleshooting

### No Updates Appearing

**Check**:
1. Markers are present in README.md
2. Markers have correct syntax
3. Script completed without errors

### Wrong Block Updated

**Solution**: Use typed markers instead of untyped

### Configuration Not Applied

**Check**:
1. JSON is valid (use a JSON validator)
2. Config is inside markers
3. Proper formatting with triple backticks

### Git Errors

**Solution**: Ensure you're in a Git repository
```bash
git status  # Should not error
```

## Source Code Structure

```python
#!/usr/bin/env python3
import os
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

README_PATH = Path("README.md")
DEFAULT_CONFIG = {...}

# Git utilities
def git_log(args): ...
def get_commit_stats(since=None): ...
def get_diff_stats(commit_range=None): ...
def timeframes(): ...

# Markdown processing
def replace_between_markers(...): ...
def update_block(...): ...

# Report generation
def generate_table(): ...
def generate_commit_activity_graph(): ...
def generate_language_pie(): ...
def parse_config_block(...): ...

# Main execution
if __name__ == "__main__":
    readme_text = README_PATH.read_text()
    for block in ["OVERVIEW", "LANGUAGES", "COMMITS"]:
        cfg = parse_config_block(readme_text, block)
        sections = [...]
        readme_text = update_block(readme_text, block, "\n".join(sections))
    README_PATH.write_text(readme_text)
```

## Related Scripts

- [generate_stats3.py](/docs/scripts/generate-stats3): Config from README
- [generate_stats4.py](/docs/scripts/generate-stats4): Real language calculations
- [generate_stats2.py](/docs/scripts/generate-stats2): Enhanced with charts

## See Also

- [Configuration Guide](/docs/configuration)
- [API Reference - Git Helpers](/docs/api/git-helpers)
- [API Reference - Markdown Processing](/docs/api/markdown-processing)
