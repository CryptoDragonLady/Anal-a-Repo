#!/usr/bin/env python3
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

TEMPLATE_PATH = Path("README_TEMPLATE.md")
OUTPUT_PATH = Path("README.md")

# ─────────────────────────────
# ─── GIT HELPERS ─────────────
# ─────────────────────────────
def git_log(args):
    result = subprocess.run(["git"] + args, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def get_commit_stats(since=None):
    args = ["log", "--shortstat", "--pretty=format:%H%x09%an%x09%ad", "--date=iso"]
    if since:
        args.append(f"--since={since}")
    log = git_log(args)
    commits = []
    for entry in log.split("\n"):
        parts = entry.split("\t")
        if len(parts) == 3:
            commits.append({"hash": parts[0], "author": parts[1], "date": parts[2]})
    return commits

def get_diff_stats(commit_range=None, ignored_exts=None):
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
def parse_config(template_text: str) -> dict:
    """Extract the JSON config from the <details> block in the template."""
    match = re.search(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>",
        template_text,
        re.DOTALL | re.IGNORECASE,
    )
    if not match:
        print("⚠️ No analytics config found in template.")
        return {}
    try:
        return json.loads(match.group(1).strip())
    except json.JSONDecodeError as e:
        print(f"⚠️ Invalid JSON in analytics config: {e}")
        return {}


# ─────────────────────────────
# ─── MARKER HANDLING ─────────
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
        print(f"⚠️ No block markers found for type '{block_type}', skipping.")
        return template_text


# ─────────────────────────────
# ─── REPORTS ─────────────────
# ─────────────────────────────
def resolve_timeframes(cfg):
    now = datetime.utcnow()
    tf_cfg = cfg.get("timeframes", {})
    mapping = {}
    for label, value in tf_cfg.items():
        if not value or value == "all":
            mapping[label] = None
        elif value.endswith("d"):
            mapping[label] = (now - timedelta(days=int(value[:-1]))).isoformat()
        elif value.endswith("h"):
            mapping[label] = (now - timedelta(hours=int(value[:-1]))).isoformat()
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


def generate_language_breakdown(cfg):
    lang_cfg = cfg.get("languages", {})
    if not lang_cfg.get("show_breakdown", True):
        return ""
    _, _, langs = get_diff_stats(ignored_exts=lang_cfg.get("ignore", []))
    if not langs:
        return "🧠 **Language Breakdown:** No data.\n"
    total = sum(langs.values())
    sorted_langs = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    bars = []
    for lang, count in sorted_langs:
        pct = (count / total) * 100
        filled = "█" * int(pct / 5)
        bars.append(f"{lang.upper():<10} {filled:<20} {pct:>5.1f}%")
    return f"🧠 **Language Breakdown (All Time)**\n```\n" + "\n".join(bars) + "\n```\n"


# ─────────────────────────────
# ─── MAIN ────────────────────
# ─────────────────────────────
if __name__ == "__main__":
    template_text = TEMPLATE_PATH.read_text()
    cfg = parse_config(template_text)

    sections = {
        "OVERVIEW": "\n".join([
            generate_table(cfg),
            generate_language_breakdown(cfg)
        ])
    }

    output_text = template_text
    for section, content in sections.items():
        output_text = replace_marker_block(output_text, section, content)

    # Remove config block and all markers
    output_text = re.sub(r"<!-- STATS BREAKDOWN (START|END).*?-->", "", output_text)
    output_text = re.sub(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>.*?</details>",
        "",
        output_text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    OUTPUT_PATH.write_text(output_text.strip() + "\n")
    print(f"✅ Generated clean README at {OUTPUT_PATH}")
