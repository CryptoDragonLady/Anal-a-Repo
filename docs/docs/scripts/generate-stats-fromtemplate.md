---
sidebar_position: 5
title: generate_stats_fromtemplate.py
---

# generate_stats_fromtemplate.py

Template-based README generation that separates your template from the final output.

## Overview

This script reads from `README_TEMPLATE.md` and generates a clean `README.md` file. It removes all markers and config blocks, producing a professional output file.

## Key Concept

**Separation of Concerns**:
- `README_TEMPLATE.md`: Your working file with markers and config
- `README.md`: Clean generated output for users

## Features

- **Template Processing**: Reads from README_TEMPLATE.md
- **Clean Output**: Removes markers and config from generated README
- **Config Extraction**: Parses JSON from template
- **No Dependencies**: Python standard library only

## Usage

```bash
python generate_stats_fromtemplate.py
```

**Process**:
1. Reads `README_TEMPLATE.md`
2. Extracts configuration
3. Generates analytics
4. Writes clean `README.md` (no markers, no config)

## File Structure

```
your-repo/
├── README_TEMPLATE.md  (you edit this)
├── README.md           (generated, clean)
└── generate_stats_fromtemplate.py
```

## README_TEMPLATE.md Example

````markdown
# My Project

Description...

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
    "ignore": ["lock"]
  }
}
```

</details>

## Statistics

<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->

## Features

- Feature 1
- Feature 2
````markdown

## Generated README.md

After running the script:

```markdown
# My Project

Description...

## Statistics

### 📊 Repository Stats

| Period | Commits | Additions/Deletions | Total Lines | Languages |
|--------|----------|---------------------|--------------|-----------|
| All Time | 45 | +12,345 / -6,789 | 19,134 | PY(8500), JS(4200) |
| Last 30 Days | 12 | +2,300 / -890 | 3,190 | PY(1800), JS(900) |

🧠 **Language Breakdown (All Time)**
```
PYTHON     ████████████████████ 45.5%
JAVASCRIPT █████████            22.3%
MARKDOWN   ████                 12.1%
```

## Features

- Feature 1
- Feature 2
```

**Note**: All markers and config removed!

## How It Works

### 1. Read Template

```python
TEMPLATE_PATH = Path("README_TEMPLATE.md")
template_text = TEMPLATE_PATH.read_text()
```

### 2. Parse Config

```python
def parse_config(template_text: str) -> dict:
    match = re.search(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>",
        template_text,
        re.DOTALL | re.IGNORECASE,
    )
    return json.loads(match.group(1).strip())
```

### 3. Generate Analytics

```python
sections = {
    "OVERVIEW": "\n".join([
        generate_table(cfg),
        generate_language_breakdown(cfg)
    ])
}
```

### 4. Replace Markers

```python
output_text = template_text
for section, content in sections.items():
    output_text = replace_marker_block(output_text, section, content)
```

### 5. Clean Output

```python
# Remove all markers
output_text = re.sub(r"<!-- STATS BREAKDOWN (START|END).*?-->", "", output_text)

# Remove config block
output_text = re.sub(
    r"<details>\s*<summary>.*?Analytics Config.*?</summary>.*?</details>",
    "",
    output_text,
    flags=re.DOTALL | re.IGNORECASE,
)
```

### 6. Write Clean README

```python
OUTPUT_PATH = Path("README.md")
OUTPUT_PATH.write_text(output_text.strip() + "\n")
```

## Workflow

### Recommended Workflow

1. **Edit Template**: Make changes to `README_TEMPLATE.md`
2. **Run Script**: `python generate_stats_fromtemplate.py`
3. **Review Output**: Check `README.md`
4. **Commit Both**: 
   ```bash
   git add README_TEMPLATE.md README.md
   git commit -m "Update README"
   ```

### Git Integration

Add to `.gitignore` to auto-generate:
```
# README.md will be generated
README.md
```

Or commit both for transparency.

## Configuration

Same format as stats3/stats4:

````markdown
<details>
<summary>📈 Analytics Config</summary>

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
    "ignore": ["lock", "json", "svg"]
  }
}
```

</details>
````

## Supported Sections

Currently supports:
- `OVERVIEW`: Stats table + language breakdown

To add more sections, modify:

```python
sections = {
    "OVERVIEW": generate_overview(cfg),
    "COMMITS": generate_commits(cfg),
    "PULSE": generate_pulse(cfg)
}
```

## Advantages

### Clean Output
Users see polished README without technical markers.

### Editable Template
You can update template without worrying about markers being removed.

### Version Control
Both template and output can be committed for full history.

### Automation Friendly
Easy to integrate into build pipelines.

## Limitations

- **Single Section**: Only OVERVIEW block by default
- **No Charts**: Text-based output only
- **Manual Config**: No default fallback

## Comparison

| Aspect | Regular Scripts | fromtemplate.py |
|--------|-----------------|-----------------|
| Input File | README.md | README_TEMPLATE.md |
| Output File | README.md | README.md |
| Markers in Output | Yes | No |
| Config in Output | Yes | No |
| Separation | No | Yes |

## Use Cases

### Professional Projects
Hide implementation details from users.

### Automated Builds
Generate README as part of CI/CD.

### Template Management
Maintain separate template for editing.

### Multi-Language READMEs
Generate different READMEs from one template.

## Troubleshooting

### Template Not Found

**Error**: `FileNotFoundError: README_TEMPLATE.md`

**Solution**: Create README_TEMPLATE.md in repo root

### Output Not Clean

**Check**: Marker syntax is exact:
```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
```

### Config Not Removed

**Check**: Config block format matches regex pattern

## See Also

- [generate_stats_fromtemplate_withgraphs.py](/docs/scripts/generate-stats-fromtemplate-withgraphs): With charts
- [Advanced - Custom Templates](/docs/advanced/custom-templates)
