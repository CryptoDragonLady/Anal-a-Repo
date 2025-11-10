---
title: Timeframes Configuration
description: Configure analysis windows like All Time, Last 30 Days, 7 Days, and 24 Hours used by the analytics scripts.
---

The analytics scripts support flexible time windows so you can view trends over different periods.

Supported formats:

- all or null: analyzes the entire repository history
- Nd: last N days (for example, 30d, 7d)
- Nh: last N hours (for example, 24h)

Example configuration used by the scripts that read from the README:

```json
{
  "timeframes": {
    "All Time": "all",
    "Last 30 Days": "30d",
    "Last 7 Days": "7d",
    "Last 24 Hours": "24h"
  }
}
``

How it works:

- The Python helpers resolve these values to actual dates using UTC time.
- In generate_stats_new.py and generate_stats_new2.py, the timeframes are parsed and mapped to ISO-8601 timestamps.

Code reference (simplified):

```python
from datetime import datetime, timedelta

def resolve_timeframes(cfg):
  now = datetime.utcnow()
  mapping = {}
  for label, value in cfg["timeframes"].items():
      if not value or value == "all":
          mapping[label] = None
      elif value.endswith("d"):
          days = int(value[:-1])
          mapping[label] = (now - timedelta(days=days)).isoformat()
      elif value.endswith("h"):
          hours = int(value[:-1])
          mapping[label] = (now - timedelta(hours=hours)).isoformat()
      else:
          mapping[label] = None
  return mapping
```

Tips:

- Use shorter windows (like 7d or 24h) to spot recent activity spikes.
- Keep “All Time” available to provide a comprehensive baseline.