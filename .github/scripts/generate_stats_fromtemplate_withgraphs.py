#!/usr/bin/env python3
import subprocess
import datetime
import re
from collections import defaultdict, Counter
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import json

# ─────────────────────────────
# ─── PATHS ───────────────────
# ─────────────────────────────
TEMPLATE_PATH = Path("README_TEMPLATE.md")
OUTPUT_PATH = Path("README.md")
STATS_DIR = Path("stats")
STATS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────
# ─── DEFAULT BLOCKS ──────────
# ─────────────────────────────
DEFAULT_BLOCKS = ["OVERVIEW", "LANGUAGE", "COMMITS", "PULSE"]

# ─────────────────────────────
# ─── HELPERS ─────────────────
# ─────────────────────────────
def git_log(since_days=None):
    args = ["git", "log", "--numstat", "--pretty=format:%an|%ad", "--date=short", "--no-merges"]
    if since_days:
        since_date = (datetime.datetime.now() - datetime.timedelta(days=since_days)).strftime("%Y-%m-%d")
        args.insert(2, f"--since={since_date}")
    result = subprocess.run(args, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    data = []
    current_author, current_date = None, None
    for line in lines:
        if not line.strip():
            continue
        if "\t" not in line:
            parts = line.split("|")
            if len(parts) == 2:
                current_author, current_date = parts
        else:
            add, delete, filename = line.split("\t")
            if add == "-" or delete == "-":
                continue
            data.append((current_author, current_date, int(add), int(delete), filename))
    return data

def detect_language(filename):
    ext = Path(filename).suffix.lower()
    mapping = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".jsx": "JavaScript", ".tsx": "TypeScript", ".md": "Markdown",
        ".txt": "Text", ".html": "HTML", ".css": "CSS", ".yml": "YAML",
        ".yaml": "YAML", ".json": "JSON"
    }
    return mapping.get(ext, "Other")

def plot_language_chart(langs, label):
    if not langs:
        return None
    names, sizes = list(langs.keys()), list(langs.values())
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=names, autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    plt.title(f"Language Breakdown - {label}")
    chart_path = STATS_DIR / f"lang_{label.replace(' ', '_').lower()}.png"
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close(fig)
    return chart_path

def plot_commit_activity(dates, label):
    if not dates:
        return None
    counts = Counter(dates)
    df = pd.DataFrame(sorted(counts.items()), columns=["Date", "Commits"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df = df.asfreq("D", fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 3))
    df["Commits"].plot(ax=ax)
    plt.title(f"Commit Activity - {label}")
    plt.xlabel("Date")
    plt.ylabel("Commits per Day")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    chart_path = STATS_DIR / f"activity_{label.replace(' ', '_').lower()}.png"
    plt.savefig(chart_path, dpi=150)
    plt.close(fig)
    return chart_path

# ─────────────────────────────
# ─── CONFIG PARSING ──────────
# ─────────────────────────────
def parse_config(template_text):
    """Extract JSON config from template <details> block."""
    match = re.search(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>",
        template_text,
        re.DOTALL | re.IGNORECASE,
    )
    if not match:
        print("⚠️ No analytics config found in template, using defaults.")
        return {}
    try:
        return json.loads(match.group(1).strip())
    except json.JSONDecodeError as e:
        print(f"⚠️ Invalid JSON in analytics config: {e}")
        return {}

# ─────────────────────────────
# ─── BLOCK GENERATORS ─────────
# ─────────────────────────────
def generate_overview_block(timeframes, ignored_exts):
    output = "## 📊 Repository Analytics Overview\n\n"
    for label, days in timeframes.items():
        data = git_log(days)
        if not data:
            output += f"### {label}\n_No activity_\n\n"
            continue

        contributors = defaultdict(lambda: {"commits": 0, "additions": 0, "deletions": 0, "langs": defaultdict(int)})
        for author, date, add, delete, filename in data:
            contributors[author]["commits"] += 1
            contributors[author]["additions"] += add
            contributors[author]["deletions"] += delete
            lang = detect_language(filename)
            if lang not in ignored_exts:
                contributors[author]["langs"][lang] += add + delete

        output += f"### {label}\n\n"
        output += "| Contributor | Commits | +Add | -Del | Total | Top Languages |\n"
        output += "|-------------|----------|------|------|--------|----------------|\n"
        for author, stats in sorted(contributors.items(), key=lambda x: x[1]["commits"], reverse=True):
            total = stats["additions"] + stats["deletions"]
            langs = ", ".join(f"{k} ({v})" for k, v in sorted(stats["langs"].items(), key=lambda x: -x[1]))
            output += f"| {author} | {stats['commits']} | {stats['additions']} | {stats['deletions']} | {total} | {langs} |\n"
        output += "\n"
    return output

def generate_language_block(timeframes, ignored_exts):
    output = "## 🧠 Language Breakdown\n\n"
    for label, days in timeframes.items():
        data = git_log(days)
        all_langs = defaultdict(int)
        for _, _, add, delete, filename in data:
            lang = detect_language(filename)
            if lang not in ignored_exts:
                all_langs[lang] += add + delete
        if not all_langs:
            output += f"### {label}\n_No activity_\n\n"
            continue
        chart = plot_language_chart(all_langs, label)
        output += f"### {label}\n![{label} Language Breakdown]({chart})\n\n"
    return output

def generate_commit_activity_block(timeframes):
    output = "## 📈 Commit Activity Trends\n\n"
    for label, days in timeframes.items():
        data = git_log(days)
        dates = [d for _, d, _, _, _ in data]
        if not dates:
            output += f"### {label}\n_No commits_\n\n"
            continue
        chart = plot_commit_activity(dates, label)
        output += f"### {label}\n![{label} Commit Activity]({chart})\n\n"
    return output

def generate_pulse_block():
    output = "## ⚡ Repository Pulse\n\n"
    all_data = git_log()
    contributors = set(a for a, _, _, _, _ in all_data)
    total_commits = len(all_data)
    additions = sum(a for _, _, a, _, _ in all_data)
    deletions = sum(d for _, _, _, d, _ in all_data)
    output += f"- **Total Commits:** {total_commits}\n"
    output += f"- **Contributors:** {len(contributors)}\n"
    output += f"- **Lines Added:** {additions}\n"
    output += f"- **Lines Deleted:** {deletions}\n"
    output += f"- **First Commit Date:** {subprocess.getoutput('git log --reverse --format=%ad --date=short | head -n1')}\n"
    output += f"- **Last Commit Date:** {subprocess.getoutput('git log -1 --format=%ad --date=short')}\n"
    return output + "\n"

# ─────────────────────────────
# ─── BLOCK REPLACEMENT ───────
# ─────────────────────────────
def replace_marker_block(template_text: str, block_type: str, new_content: str) -> str:
    start_marker = f"<!-- STATS BREAKDOWN START:{block_type} -->"
    end_marker = f"<!-- STATS BREAKDOWN END:{block_type} -->"
    pattern = re.compile(
        rf"{re.escape(start_marker)}(.*?){re.escape(end_marker)}",
        re.DOTALL
    )
    if pattern.search(template_text):
        return pattern.sub(new_content, template_text)
    else:
        print(f"⚠️ No block markers found for '{block_type}', skipping.")
        return template_text

# ─────────────────────────────
# ─── MAIN ────────────────────
# ─────────────────────────────
if __name__ == "__main__":
    template_text = TEMPLATE_PATH.read_text()
    cfg = parse_config(template_text)

    # Use config or defaults
    timeframes = cfg.get("timeframes", {"All Time": None, "Last 30 Days": 30, "Last 7 Days": 7, "Last 24h": 1})
    ignored_exts = cfg.get("languages", {}).get("ignore", [])
    blocks = cfg.get("sections", {}).get("include", DEFAULT_BLOCKS)

    # Generate blocks
    section_content = {}
    if "OVERVIEW" in blocks:
        section_content["OVERVIEW"] = generate_overview_block(timeframes, ignored_exts)
    if "LANGUAGE" in blocks:
        section_content["LANGUAGE"] = generate_language_block(timeframes, ignored_exts)
    if "COMMITS" in blocks:
        section_content["COMMITS"] = generate_commit_activity_block(timeframes)
    if "PULSE" in blocks:
        section_content["PULSE"] = generate_pulse_block()

    output_text = template_text
    for section, content in section_content.items():
        output_text = replace_marker_block(output_text, section, content)

    # Remove all markers and config block
    output_text = re.sub(r"<!-- STATS BREAKDOWN (START|END).*?-->", "", output_text)
#    output_text = re.sub(
#        r"<details>\s*<summary>.*?Analytics Config.*?</summary>.*?</details>",
#        "",
#        output_text,
#        flags=re.DOTALL | re.IGNORECASE,
#    )
# Commented out so it displays in the readme. 
    OUTPUT_PATH.write_text(output_text.strip() + "\n")
    print("✅ README generated with all analytics blocks.")
