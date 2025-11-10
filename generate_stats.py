#!/usr/bin/env python3
import os
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

README_PATH = Path("README.md")

# ─────────────────────────────
# CONFIG DEFAULTS
# ─────────────────────────────
DEFAULT_CONFIG = {
    "show_graphs": True,
    "show_language_breakdown": True,
    "show_contributors": True,
    "show_commit_activity": True,
}

# ─────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────
def git_log(args):
    """Run a git log command and return decoded output."""
    result = subprocess.run(
        ["git"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def get_commit_stats(since=None):
    """Gather commit statistics since a given date."""
    args = ["log", "--shortstat", "--pretty=format:%H%x09%an%x09%ad", "--date=iso"]
    if since:
        args.append(f"--since={since}")
    log = git_log(args)

    commits = []
    for entry in log.split("\n"):
        parts = entry.split("\t")
        if len(parts) == 3:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
            })
    return commits


def get_diff_stats(commit_range=None):
    """Get diff statistics for a given range."""
    args = ["diff", "--numstat"]
    if commit_range:
        args.append(commit_range)
    diff = git_log(args)
    total_add, total_del = 0, 0
    language_counts = defaultdict(int)

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
            language_counts[ext] += add + delete
            total_add += add
            total_del += delete
    return total_add, total_del, language_counts


def timeframes():
    """Return the key timeframes we want to analyze."""
    now = datetime.utcnow()
    return {
        "All Time": None,
        "Last 30 Days": (now - timedelta(days=30)).isoformat(),
        "Last 7 Days": (now - timedelta(days=7)).isoformat(),
        "Last 24 Hours": (now - timedelta(hours=24)).isoformat(),
    }


# ─────────────────────────────
# MARKDOWN UPDATE LOGIC
# ─────────────────────────────
def replace_between_markers(readme_text: str, start_marker: str, end_marker: str, new_inner: str, count: int = 1) -> str:
    """Replace only content between markers, preserving markers."""
    start_re = re.escape(start_marker)
    end_re = re.escape(end_marker)
    pattern = re.compile(rf"({start_re})(.*?)(\s*{end_re})", re.DOTALL)
    replacement = rf"\1\n\n{new_inner}\n\3"
    updated, n = pattern.subn(replacement, readme_text, count=count)
    return updated if n > 0 else readme_text


def update_block(readme_text: str, block_type: str, content: str) -> str:
    """Update a single stats block, preserving markers."""
    typed_start = f"<!-- STATS BREAKDOWN START:{block_type} -->"
    typed_end   = f"<!-- STATS BREAKDOWN END:{block_type} -->"

    if typed_start in readme_text and typed_end in readme_text:
        return replace_between_markers(readme_text, typed_start, typed_end, content)

    untyped_start = "<!-- STATS BREAKDOWN START -->"
    untyped_end   = "<!-- STATS BREAKDOWN END -->"

    if untyped_start in readme_text and untyped_end in readme_text:
        return replace_between_markers(readme_text, untyped_start, untyped_end, content, count=1)

    # If no markers, append new block to end of README
    new_block = f"\n\n{typed_start}\n\n{content}\n\n{typed_end}\n"
    return readme_text + new_block


# ─────────────────────────────
# REPORT GENERATION
# ─────────────────────────────
def generate_table():
    """Generate a stats markdown table."""
    rows = []
    for label, since in timeframes().items():
        commits = get_commit_stats(since)
        add, delete, langs = get_diff_stats()
        rows.append(
            f"| {label} | {len(commits)} | +{add} / -{delete} | {add+delete} | "
            f"{', '.join(f'{k.upper()} ({v})' for k,v in langs.items())} |"
        )
    header = "| Period | Commits | Additions/Deletions | Total Lines | Languages |\n|--------|----------|--------------------|--------------|------------|"
    return f"### 📊 Repository Stats\n\n{header}\n" + "\n".join(rows)


def generate_commit_activity_graph():
    """Dummy placeholder graph example."""
    return "```\nCommits by Day:\n███████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n```\n"


def generate_language_pie():
    """Dummy text-based language pie chart."""
    return "🧠 **Language Breakdown:** JS ████ 45% | MD ██ 25% | PY ██ 20% | Other ░░ 10%\n"


def parse_config_block(readme_text: str, block_type: str) -> dict:
    """Parse JSON config block from inside a stats section."""
    start_marker = f"<!-- STATS BREAKDOWN START:{block_type} -->"
    end_marker   = f"<!-- STATS BREAKDOWN END:{block_type} -->"
    block_match = re.search(rf"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", readme_text, re.DOTALL)
    if not block_match:
        return DEFAULT_CONFIG
    inner = block_match.group(1)
    config_match = re.search(r"```json(.*?)```", inner, re.DOTALL)
    if config_match:
        try:
            cfg = json.loads(config_match.group(1))
            return {**DEFAULT_CONFIG, **cfg}
        except Exception:
            pass
    return DEFAULT_CONFIG


# ─────────────────────────────
# MAIN
# ─────────────────────────────
if __name__ == "__main__":
    readme_text = README_PATH.read_text()

    # For each desired block, generate output based on optional config
    for block in ["OVERVIEW", "LANGUAGES", "COMMITS"]:
        cfg = parse_config_block(readme_text, block)
        sections = []

        if cfg["show_contributors"] or cfg["show_commit_activity"]:
            sections.append(generate_table())

        if cfg["show_graphs"]:
            sections.append(generate_commit_activity_graph())

        if cfg["show_language_breakdown"]:
            sections.append(generate_language_pie())

        block_content = "\n".join(sections)
        readme_text = update_block(readme_text, block, block_content)

    README_PATH.write_text(readme_text)
    print("✅ README updated with stats blocks (markers preserved).")
