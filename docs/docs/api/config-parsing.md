---
title: Config Parsing
description: Read analytics configuration from README template or README using a JSON block.
---

The scripts can read a JSON configuration embedded inside a collapsible details block.

Example block in README_TEMPLATE.md:

````md
<details>
  <summary>Analytics Config</summary>

  ```json
  {
    "timeframes": {
      "All Time": "all",
      "Last 30 Days": "30d",
      "Last 7 Days": "7d",
      "Last 24 Hours": "24h"
    },
    "sections": { "include": ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"] },
    "languages": { "ignore": ["lock", "map"], "show_breakdown": true },
    "graphs": { "show": true, "color": "#4e79a7" }
  }
  ```

</details>
````

Parsing helpers:

```python
def parse_global_config(readme_text: str) -> dict:
    match = re.search(r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>", readme_text, re.DOTALL | re.IGNORECASE)
    if not match:
        return DEFAULT_CONFIG
    return json.loads(match.group(1).strip())
```

Notes:

- If JSON parsing fails, defaults are used
- Template-based generator removes the config block from output after rendering