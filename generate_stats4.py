#!/usr/bin/env python3
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

README_PATH = Path("README.md")


# ─────────────────────────────
# ─── GIT HELPERS ─────────────
# ─────────────────────────────
def git_log(args):
    """Run git command and return output."""
    result = subprocess.run(
        ["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.stdout.strip()


def get_commit_stats(since=None):
    """Gather commit metadata since a given date."""
    args = ["log", "--shortstat", "--pretty=format:%H%x09%an%x09%ad", "--date=iso"]
    if since:
        args.append(f"--since={since}")
    log = git_log(args)

    commits = []
    for entry in log.split("\n"):
        parts = entry.split("\t")
        if len(parts) == 3:
            commits.append(
                {"hash": parts[0], "author": parts[1], "date": parts[2]}
            )
    return commits


def get_diff_stats(commit_range=None, ignored_exts=None):
    """Compute additions, deletions, and per-language totals."""
    args = ["diff", "--numstat"]
    if commit_range:
        args.append(commit_range)
    diff = git_log(args)
    total_add, total_del = 0, 0
    language_counts = defaultdict(int)
    ignored_exts = set(ignored_exts or [])

    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            try:
                add = int(parts[0])
                delete = int(parts[1])
            except ValueError:
                continue
            filename = parts[2]
            ext = Path(filename).suffix.lower().replace(".", "")
            if ext in ignored_exts:
                continue
            language_counts[ext] += add + delete
            total_add += add
            total_del += delete
    return total_add, total_del, language_counts


# ─────────────────────────────
# ─── CONFIG PARSING ──────────
# ─────────────────────────────
def parse_global_config(readme_text: str) -> dict:
    """Read the <details><summary>Analytics Config</summary> block."""
    match = re.search(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>",
        readme_text,
        re.DOTALL | re.IGNORECASE,
    )
    if not match:
        print("⚠️ No analytics config found in README.")
        return {}

    json_text = match.group(1).strip()
    try:
        parsed = json.loads(json_text)
        return parsed
    except json.JSONDecodeError as e:
        print(f"⚠️ Invalid JSON in analytics config: {e}")
        return {}


# ─────────────────────────────
# ─── MARKDOWN BLOCK MGMT ─────
# ─────────────────────────────
def replace_between_markers(readme_text: str, start_marker: str, end_marker: str, new_inner: str, count: int = 1) -> str:
    start_re = re.escape(start_marker)
    end_re = re.escape(end_marker)
    pattern = re.compile(rf"({start_re})(.*?)(\s*{end_re})", re.DOTALL)
    replacement = rf"\1\n\n{new_inner}\n\3"
    updated, n = pattern.subn(replacement, readme_text, count=count)
    return updated if n > 0 else readme_text


def update_block(readme_text: str, block_type: str, content: str) -> str:
    typed_start = f"<!-- STATS BREAKDOWN START:{block_type} -->"
    typed_end = f"<!-- STATS BREAKDOWN END:{block_type} -->"

    if typed_start in readme_text and typed_end in readme_text:
        return replace_between_markers(readme_text, typed_start, typed_end, content)

    untyped_start = "<!-- STATS BREAKDOWN START -->"
    untyped_end = "<!-- STATS BREAKDOWN END -->"

    if untyped_start in readme_text and untyped_end in readme_text:
        return replace_between_markers(readme_text, untyped_start, untyped_end, content, count=1)

    # Append new block if none found
    return readme_text + f"\n\n{typed_start}\n\n{content}\n\n{typed_end}\n"


# ─────────────────────────────
# ─── REPORT GENERATION ───────
# ─────────────────────────────
def resolve_timeframes(cfg):
    now = datetime.utcnow()
    tf_cfg = cfg.get("timeframes", {})
    mapping = {}
    for label, value in tf_cfg.items():
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


def generate_table(cfg):
    rows = []
    timeframes = resolve_timeframes(cfg)
    ignored = cfg.get("languages", {}).get("ignore", [])
    for label, since in timeframes.items():
        commits = get_commit_stats(since)
        add, delete, langs = get_diff_stats(ignored_exts=ignored)
        langs_str = ", ".join(f"{k.upper()}({v})" for k, v in langs.items()) or "—"
        rows.append(
            f"| {label} | {len(commits)} | +{add} / -{delete} | {add + delete} | {langs_str} |"
        )

    header = "| Period | Commits | Additions/Deletions | Total Lines | Languages |\n|--------|----------|--------------------|--------------|------------|"
    return f"### 📊 Repository Stats\n\n{header}\n" + "\n".join(rows)


def generate_commit_graph(cfg):
    graph_cfg = cfg.get("graphs", {})
    if not graph_cfg.get("show", True):
        return ""
    color = graph_cfg.get("color", "#4e79a7")
    return f"```\nCommits per Day (Color {color}):\n███████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n```\n"


def generate_language_breakdown(cfg):
    lang_cfg = cfg.get("languages", {})
    if not lang_cfg.get("show_breakdown", True):
        return ""

    _, _, langs = get_diff_stats(ignored_exts=lang_cfg.get("ignore", []))
    if not langs:
        return "🧠 **Language Breakdown:** No language data available.\n"

    total = sum(langs.values())
    if total == 0:
        return "🧠 **Language Breakdown:** No changes recorded.\n"

    sorted_langs = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    bars = []
    for lang, count in sorted_langs:
        pct = (count / total) * 100
        filled = "█" * int(pct / 5)
        bars.append(f"{lang.upper():<10} {filled:<20} {pct:>5.1f}%")

    output = "\n".join(bars)
    return f"🧠 **Language Breakdown (All Time)**\n```\n{output}\n```\n"


# ─────────────────────────────
# ─── MAIN ────────────────────
# ─────────────────────────────
if __name__ == "__main__":
    readme_text = README_PATH.read_text()
    cfg = parse_global_config(readme_text)

    sections = [
        generate_table(cfg),
        generate_commit_graph(cfg),
        generate_language_breakdown(cfg),
    ]

    readme_text = update_block(readme_text, "OVERVIEW", "\n".join(sections))
    README_PATH.write_text(readme_text)
    print("✅ README updated with analytics (config preserved).")
