---
sidebar_position: 4
title: generate_stats4.py
---

# generate_stats4.py

Enhanced version of stats3 with real language breakdown calculations and visual progress bars.

## Overview

`generate_stats4.py` builds on the configuration-based approach of stats3 by adding actual language percentage calculations and visual representations. Instead of placeholder language data, this script computes real statistics from your repository.

## Key Features

- **Real Language Calculations**: Actual percentages based on git diff stats
- **Visual Progress Bars**: ASCII bars showing language distribution
- **Config from README**: Reads global JSON configuration
- **Language Filtering**: Respects ignore lists from config
- **Better Error Handling**: Improved error messages and reporting
- **No Dependencies**: Python standard library only

## Usage

```bash
python generate_stats4.py
```

## Output Comparison

### stats3.py (Placeholder)

```markdown
🧠 **Language Breakdown:** JS ████ 45% | MD ██ 25% | PY ██ 20% | Other ░░ 10%
```

### stats4.py (Real Data)

```markdown
🧠 **Language Breakdown (All Time)**
```
PYTHON     ████████████████████ 45.5%
JAVASCRIPT █████████            22.3%
TYPESCRIPT ████                 12.1%
MARKDOWN   ███                   8.7%
CSS        ██                    6.4%
HTML       █                     3.2%
OTHER      ░                     1.8%
```
```

## How It Works

### Language Calculation

```python
def generate_language_breakdown(cfg):
    _, _, langs = get_diff_stats(ignored_exts=lang_cfg.get("ignore", []))
    
    total = sum(langs.values())
    sorted_langs = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    
    for lang, count in sorted_langs:
        pct = (count / total) * 100
        filled = "█" * int(pct / 5)  # Each block = 5%
        bars.append(f"{lang.upper():<10} {filled:<20} {pct:>5.1f}%")
```

### Visual Bar Generation

Each `█` represents 5% of total lines:
- 20 blocks = 100%
- `int(percentage / 5)` blocks filled
- Remaining space padded with whitespace

## Configuration

Same as stats3.py:

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
    "ignore": ["lock", "json", "min"]
  },
  "graphs": {
    "show": true,
    "color": "#4e79a7"
  }
}
```

</details>
````

## Generated Output

### Statistics Table

Same as stats3, but with filtered languages:

```markdown
### 📊 Repository Stats

| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 45 | +12,345 / -6,789 | 19,134 | PY(8500), JS(4200), MD(1200) |
```

### Language Breakdown

Real data with visual bars:

```
🧠 **Language Breakdown (All Time)**
```
PYTHON     ████████████████████ 45.5%
JAVASCRIPT ████████             19.2%
MARKDOWN   ████                  9.8%
CSS        ███                   7.3%
HTML       ██                    5.1%
YAML       ██                    4.2%
JSON       █                     3.5%
OTHER      ██                    5.4%
```
```

### Commit Graph

Placeholder (same as stats3):

```
Commits per Day (Color #4e79a7):
███████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
```

## Key Improvements Over stats3

### 1. Real Language Data

**stats3**:
```python
return "🧠 **Language Breakdown:** JS ████ 45% | MD ██ 25% | PY ██ 20% | Other ░░ 10%\n"
```

**stats4**:
```python
_, _, langs = get_diff_stats(ignored_exts=lang_cfg.get("ignore", []))
total = sum(langs.values())
for lang, count in sorted_langs:
    pct = (count / total) * 100
```

### 2. Better Formatting

- Left-aligned language names (10 chars)
- Fixed-width bar area (20 chars)
- Right-aligned percentages (5.1f format)

### 3. Error Handling

```python
if not langs:
    return "🧠 **Language Breakdown:** No language data available.\n"

if total == 0:
    return "🧠 **Language Breakdown:** No changes recorded.\n"
```

## Example Output

### Python-Heavy Repository

```
PYTHON     ████████████████████ 78.3%
MARKDOWN   ███                   8.2%
YAML       ██                    5.1%
JSON       █                     3.9%
TXT        █                     2.8%
OTHER      ░                     1.7%
```

### JavaScript Project

```
JAVASCRIPT ████████████████     55.2%
TYPESCRIPT ████████             28.7%
CSS        ██                    7.4%
HTML       █                     4.3%
JSON       █                     2.9%
MARKDOWN   ░                     1.5%
```

### Mixed Repository

```
PYTHON     ██████████           35.4%
JAVASCRIPT ████████             28.1%
MARKDOWN   ████                 14.2%
CSS        ██                    8.3%
HTML       ██                    6.7%
YAML       █                     4.2%
OTHER      ░                     3.1%
```

## Advanced Usage

### Custom Bar Characters

Modify the bar generation:

```python
# Use different characters
filled = "▓" * int(pct / 5)     # Darker blocks
filled = "■" * int(pct / 5)     # Squares
filled = "●" * int(pct / 5)     # Circles
```

### Adjust Bar Scale

```python
# Finer granularity (each block = 2.5%)
filled = "█" * int(pct / 2.5)
bars.append(f"{lang.upper():<10} {filled:<40} {pct:>5.1f}%")
```

### Filter Small Languages

```python
# Only show languages >1%
for lang, count in sorted_langs:
    pct = (count / total) * 100
    if pct > 1.0:
        filled = "█" * int(pct / 5)
        bars.append(f"{lang.upper():<10} {filled:<20} {pct:>5.1f}%")
```

## Language Detection

Same as other scripts - by file extension:

```python
ext = Path(filename).suffix.lower().replace(".", "")
language_counts[ext] += add + delete
```

**Detected Extensions**:
- `py` → PYTHON
- `js` → JAVASCRIPT  
- `ts` → TYPESCRIPT
- `md` → MARKDOWN
- `css` → CSS
- `html` → HTML
- `json` → JSON
- `yml`/`yaml` → YAML
- Others → OTHER

## Ignore List Usage

```json
{
  "languages": {
    "ignore": ["lock", "json", "min", "map"]
  }
}
```

**Effect**:
- `package-lock.json` → Ignored
- `config.json` → Ignored
- `script.min.js` → Ignored
- `bundle.js.map` → Ignored
- `README.md` → Counted

## Performance

- **Typical**:
- Small repo: &lt;1 second
- Medium repo: 1-5 seconds
- Large repo: 5-15 seconds

**Optimization**: Same as stats3 - uses efficient git commands.

## Troubleshooting

### All Languages Showing 0%

**Cause**: No changes in repository
**Solution**: Make commits with file changes

### Wrong Percentages

**Cause**: Ignored extensions not configured
**Solution**: Check ignore list matches your extensions

### Bars Not Aligned

**Cause**: Terminal not using fixed-width font
**Solution**: Use monospace font for proper alignment

## Comparison Table

| Feature | stats3.py | stats4.py |
|---------|-----------|-----------|
| Language Data | Placeholder | Real calculations |
| Visual Bars | Generic | Percentage-based |
| Sorting | N/A | By usage |
| Empty Check | No | Yes |
| Formatting | Simple | Aligned columns |

## See Also

- [generate_stats3.py](/docs/scripts/generate-stats3): Basis for this script
- [generate_stats_fromtemplate.py](/docs/scripts/generate-stats-fromtemplate): Template version
- [Configuration - Languages](/docs/configuration/languages)
