---
title: Language Settings
description: Control language detection, mapping, and ignored extensions for analytics.
---

Language detection is based on file extensions and can be customized.

Ignore specific extensions:

```json
{
  "languages": {
    "ignore": ["lock", "map", "svg"],
    "show_breakdown": true
  }
}
```

Detection mapping (excerpt from the scripts):

```python
def detect_language(filename):
    mapping = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".jsx": "JavaScript", ".tsx": "TypeScript", ".md": "Markdown",
        ".txt": "Text", ".html": "HTML", ".css": "CSS", ".yml": "YAML",
        ".yaml": "YAML", ".json": "JSON"
    }
```

Output formats:

- Text bars in README (generate_stats_new2.py)
- Pie charts saved to stats/ (generate_stats_fromtemplate_withgraphs.py)

Tips:

- Add binary or asset extensions to the ignore list to focus on code changes
- If your project uses additional languages, extend the mapping in the scripts