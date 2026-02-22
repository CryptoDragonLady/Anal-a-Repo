# Please, if you like this and you want to contribute, fork it and make a pull request. 
I'd love you see your additions. -C
---

# 📊 GitHub Repository Analytics

This repository contains a GitHub Action + Python scripts that automatically generate **repository analytics** and update your README with:

- Contributor statistics
- Commit activity trends
- Language breakdowns
- Repository pulse (total commits, lines added/deleted, contributors)
- Changelog generated from recent git history
- Graphical visualizations using matplotlib

The analytics are **template-driven** and fully configurable via JSON embedded in the template.

---

## ⚡ Features

- **Template-Based:** Keep your README clean; analytics are injected from a template with placeholders.
- **Configurable:** Control timeframes, sections, graph sizes, and ignored file types using JSON.
- **Graphical Output:** Automatically generates charts for language breakdown and commit activity.
- **Multiple Timeframes:** Supports All Time, Last 90 Days, Last 30 Days, Last 24 Hours, or custom windows.
- **Per-Section Control:** Select which analytics blocks are included in the output README.

---

## 📌 Usage

1. **Include the template placeholders** in your `README_TEMPLATE.md`:

< !-- STATS BREAKDOWN START:OVERVIEW -->
< !-- Placeholder for overview analytics -->
< !-- STATS BREAKDOWN END:OVERVIEW -->

< !-- STATS BREAKDOWN START:LANGUAGE -->
< !-- Placeholder for language analytics -->
< !-- STATS BREAKDOWN END:LANGUAGE -->

< !-- STATS BREAKDOWN START:COMMITS -->
< !-- Placeholder for commit activity analytics -->
< !-- STATS BREAKDOWN END:COMMITS -->

< !-- STATS BREAKDOWN START:PULSE -->
< !-- Placeholder for repository pulse -->
< !-- STATS BREAKDOWN END:PULSE -->

< !-- STATS BREAKDOWN START:CHANGELOG -->
< !-- Placeholder for changelog analytics -->
< !-- STATS BREAKDOWN END:CHANGELOG -->


(extra space added betweeb < and ! so that the blocks dont get replaced and the example will show)

2. **Add the configuration block** at the bottom (hidden in `<details>`):
```markdown
<details>
<summary>📈 Analytics Config</summary>

{
  "timeframes": {
    "All Time": null,
    "Last 90 Days": "90d",
    "Last 30 Days": "30d",
    "Last 24 Hours": "24h"
  },
  "graphs": {
    "show": true,
    "width": 720,
    "height": 320,
    "color": "#4e79a7"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json"]
  },
  "contributors": {
    "show": true,
    "max": 10
  },
  "changelog": {
    "show": true,
    "max_entries": 80,
    "max_days": 45,
    "max_per_day": 8,
    "include_authors": true
  },
  "sections": {
    "include": ["PULSE", "OVERVIEW", "COMMITS", "LANGUAGE", "CHANGELOG"]
  }
}

</details>
```

3. **Run the analytics script**:

```bash
python .github/scripts/generate_stats_enhanced.py
```

4. **Output:**
   The script updates `README.md` in place, refreshes all configured analytics blocks, saves charts to `stats/`, and preserves template markers for subsequent runs.

---

## 📝 Example Sections

### Overview

<!-- STATS BREAKDOWN START:OVERVIEW -->

<!-- Placeholder for overview analytics -->

<!-- STATS BREAKDOWN END:OVERVIEW -->

### Language Breakdown

<!-- STATS BREAKDOWN START:LANGUAGE -->

<!-- Placeholder for language analytics -->

<!-- STATS BREAKDOWN END:LANGUAGE -->

### Commit Activity Trends

<!-- STATS BREAKDOWN START:COMMITS -->

<!-- Placeholder for commit activity analytics -->

<!-- STATS BREAKDOWN END:COMMITS -->

### Repository Pulse

<!-- STATS BREAKDOWN START:PULSE -->

<!-- Placeholder for repository pulse -->

<!-- STATS BREAKDOWN END:PULSE -->

### Recent Updates

<!-- STATS BREAKDOWN START:CHANGELOG -->

<!-- Placeholder for changelog analytics -->

<!-- STATS BREAKDOWN END:CHANGELOG -->

---

## 🛠 Configuration Options

* **timeframes:** Define custom labels and durations (in days) or `null` for all time.
* **languages.ignore:** File extensions to ignore in language analytics.
* **graphs:** Set chart width, height, and color.
* **changelog:** Configure max entries/time window and author visibility for changelog output.
* **sections.include:** Select which analytics blocks to render in the README.

> 💡 The JSON config is parsed directly from this template; you do **not** need to edit the script.

---

## 📈 Example Graphs

All generated charts are saved in the `stats/` folder and linked automatically in the README.

* **Language Breakdown:** Pie chart per timeframe
* **Commit Activity:** Line chart showing commits per day

---

## 🏃‍♂️ Automation

Combine this with a GitHub Action to regenerate the README nightly or on-demand:

```yaml
name: Repo Analytics

on:
  schedule:
    - cron: "0 3 * * *" # every night at 3AM UTC
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Generate analytics
        run: python .github/scripts/generate_stats_enhanced.py
      - name: Commit and push updated README
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md stats/
          git diff --quiet && echo "No changes to commit." || (git commit -m "Update README analytics" && git push)
```

If you want it to regenerate it on commit and or manual execution  use this example instead: 

```yaml
name: Repo Analytics

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Generate analytics
        run: python .github/scripts/generate_stats_enhanced.py
      - name: Commit and push updated README
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md stats/
          git diff --quiet && echo "No changes to commit." || (git commit -m "Update README analytics" && git push)
```



---

## ✅ Summary

This template allows you to:

* Keep your README clean and professional
* Dynamically show contributors, commits, languages, and activity
* Generate charts automatically
* Fully customize sections and timeframes without touching the code

> Publish this repo to GitHub, enable the action, and watch your README update automatically!

```

---

This template:  

- **Documents usage** for new users  
- Shows **all blocks and charts**  
- Explains **configuration and automation**  
- Includes **foldable JSON config**  

---

```


<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null,
    "Last 90 Days": "90d",
    "Last 30 Days": "30d",
    "Last 24 Hours": "24h"
  },
  "graphs": {
    "show": true,
    "width": 720,
    "height": 320,
    "color": "#4e79a7"
  },
  "languages": {
    "show_breakdown": true,
    "ignore": ["lock", "json"]
  },
  "contributors": {
    "show": true,
    "max": 10
  },
  "changelog": {
    "show": true,
    "max_entries": 80,
    "max_days": 45,
    "max_per_day": 8,
    "include_authors": true
  },
  "sections": {
    "include": ["PULSE", "OVERVIEW", "COMMITS", "LANGUAGE", "CHANGELOG"]
  }
}
```

</details>
