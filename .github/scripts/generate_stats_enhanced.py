#!/usr/bin/env python3
"""Generate README analytics blocks with charts while preserving template markers.

This script updates existing README block markers in-place:
- <!-- STATS BREAKDOWN START:PULSE --> ... <!-- STATS BREAKDOWN END:PULSE -->
- <!-- STATS BREAKDOWN START:OVERVIEW --> ... <!-- STATS BREAKDOWN END:OVERVIEW -->
- <!-- STATS BREAKDOWN START:COMMITS --> ... <!-- STATS BREAKDOWN END:COMMITS -->
- <!-- STATS BREAKDOWN START:LANGUAGE --> ... <!-- STATS BREAKDOWN END:LANGUAGE -->
- <!-- STATS BREAKDOWN START:CHANGELOG --> ... <!-- STATS BREAKDOWN END:CHANGELOG -->

It intentionally does NOT remove markers or the Analytics Config block so future runs
remain template-compatible.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from generate_changelog import build_changelog_markdown

README_PATH = Path("README.md")
STATS_DIR = Path("stats")

DEFAULT_BLOCKS = ["PULSE", "OVERVIEW", "COMMITS", "LANGUAGE", "CHANGELOG"]
DEFAULT_CONFIG: dict[str, Any] = {
    "timeframes": {
        "All Time": None,
        "Last 90 Days": "90d",
        "Last 30 Days": "30d",
        "Last 24 Hours": "24h",
    },
    "graphs": {
        "show": True,
        "width": 720,
        "height": 320,
        "color": "#4e79a7",
    },
    "languages": {
        "show_breakdown": True,
        "ignore": ["lock", "json"],
    },
    "contributors": {
        "show": True,
        "max": 10,
    },
    "changelog": {
        "show": True,
        "max_entries": 80,
        "max_days": 45,
        "max_per_day": 8,
        "include_authors": True,
    },
    "sections": {
        "include": DEFAULT_BLOCKS,
    },
}

_PLOT_MODULES: tuple[Any, Any] | None = None
_PLOT_IMPORT_ATTEMPTED = False


def get_plot_modules() -> tuple[Any, Any] | None:
    global _PLOT_MODULES, _PLOT_IMPORT_ATTEMPTED
    if _PLOT_MODULES is not None:
        return _PLOT_MODULES
    if _PLOT_IMPORT_ATTEMPTED:
        return None

    _PLOT_IMPORT_ATTEMPTED = True
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt

        _PLOT_MODULES = (mdates, plt)
    except Exception as exc:
        print(f"WARNING: matplotlib unavailable ({exc}). Graph generation disabled.")
        _PLOT_MODULES = None

    return _PLOT_MODULES


@dataclass
class CommitMeta:
    commit: str
    author: str
    date: dt.date


@dataclass
class FileChange:
    commit: str
    author: str
    date: dt.date
    filename: str
    additions: int
    deletions: int


@dataclass
class Summary:
    commits: int
    contributors: int
    additions: int
    deletions: int
    churn: int
    files_changed: int
    contributor_commits: Counter[str]
    contributor_churn: Counter[str]
    language_churn: Counter[str]
    file_churn: Counter[str]
    daily_commits: Counter[dt.date]


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"WARNING: git command failed ({result.returncode}): {' '.join(args)}")
        if result.stderr:
            print(result.stderr.strip())
        return ""
    return result.stdout


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}

    # Preserve key order from base config, then append override-only keys in override order.
    for key, base_value in base.items():
        if key in override:
            override_value = override[key]
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                merged[key] = deep_merge(base_value, override_value)
            else:
                merged[key] = override_value
        else:
            merged[key] = base_value

    for key, override_value in override.items():
        if key not in base:
            merged[key] = override_value

    return merged


def parse_analytics_config(readme_text: str) -> dict[str, Any]:
    pattern = re.compile(
        r"<details>\s*<summary>.*?Analytics Config.*?</summary>\s*```json(.*?)```.*?</details>",
        re.DOTALL | re.IGNORECASE,
    )
    match = pattern.search(readme_text)
    if not match:
        print("INFO: No Analytics Config block found. Using defaults.")
        return DEFAULT_CONFIG

    try:
        user_cfg = json.loads(match.group(1).strip())
    except json.JSONDecodeError as exc:
        print(f"WARNING: Invalid Analytics Config JSON ({exc}). Using defaults.")
        return DEFAULT_CONFIG

    return deep_merge(DEFAULT_CONFIG, user_cfg)


def normalize_since_value(value: Any) -> str | None:
    """Normalize time window values into a git-compatible --since value."""
    now = dt.datetime.now()
    if value is None:
        return None

    if isinstance(value, (int, float)):
        since = now - dt.timedelta(days=float(value))
        return since.strftime("%Y-%m-%d")

    if not isinstance(value, str):
        raise TypeError(f"Unsupported timeframe type: {type(value).__name__}")

    raw = value.strip().lower()
    if not raw or raw in {"all", "none"}:
        return None

    if raw.isdigit():
        since = now - dt.timedelta(days=int(raw))
        return since.strftime("%Y-%m-%d")

    unit_match = re.fullmatch(r"(\d+)\s*([hdwmy])", raw)
    if unit_match:
        amount = int(unit_match.group(1))
        unit = unit_match.group(2)
        if unit == "h":
            delta = dt.timedelta(hours=amount)
            return (now - delta).strftime("%Y-%m-%d %H:%M")
        if unit == "d":
            return (now - dt.timedelta(days=amount)).strftime("%Y-%m-%d")
        if unit == "w":
            return (now - dt.timedelta(weeks=amount)).strftime("%Y-%m-%d")
        if unit == "m":
            return (now - dt.timedelta(days=amount * 30)).strftime("%Y-%m-%d")
        return (now - dt.timedelta(days=amount * 365)).strftime("%Y-%m-%d")

    long_unit = re.fullmatch(r"(\d+)\s*(hours?|days?|weeks?|months?|years?)", raw)
    if long_unit:
        amount = int(long_unit.group(1))
        word = long_unit.group(2)
        if word.startswith("hour"):
            return (now - dt.timedelta(hours=amount)).strftime("%Y-%m-%d %H:%M")
        if word.startswith("day"):
            return (now - dt.timedelta(days=amount)).strftime("%Y-%m-%d")
        if word.startswith("week"):
            return (now - dt.timedelta(weeks=amount)).strftime("%Y-%m-%d")
        if word.startswith("month"):
            return (now - dt.timedelta(days=amount * 30)).strftime("%Y-%m-%d")
        return (now - dt.timedelta(days=amount * 365)).strftime("%Y-%m-%d")

    # Let git parse relative language expressions if provided.
    return raw


def parse_history(since_value: Any = None) -> tuple[list[CommitMeta], list[FileChange]]:
    try:
        since = normalize_since_value(since_value)
    except TypeError as exc:
        print(f"WARNING: Invalid timeframe {since_value!r}: {exc}. Using full history.")
        since = None

    args = [
        "log",
        "--numstat",
        "--date=short",
        "--pretty=format:__COMMIT__|%H|%an|%ad",
        "--no-merges",
    ]
    if since:
        args.insert(1, f"--since={since}")

    stdout = run_git(args)
    commits: list[CommitMeta] = []
    changes: list[FileChange] = []

    current_commit = ""
    current_author = ""
    current_date: dt.date | None = None

    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("__COMMIT__|"):
            _, commit_hash, author, date_text = line.split("|", 3)
            try:
                commit_date = dt.datetime.strptime(date_text, "%Y-%m-%d").date()
            except ValueError:
                continue
            commits.append(CommitMeta(commit_hash, author, commit_date))
            current_commit = commit_hash
            current_author = author
            current_date = commit_date
            continue

        if "\t" not in line or current_date is None:
            continue

        added_raw, deleted_raw, filename = line.split("\t", 2)
        if added_raw == "-" or deleted_raw == "-":
            # Binary files have '-' placeholders.
            continue

        try:
            additions = int(added_raw)
            deletions = int(deleted_raw)
        except ValueError:
            continue

        changes.append(
            FileChange(
                commit=current_commit,
                author=current_author,
                date=current_date,
                filename=filename,
                additions=additions,
                deletions=deletions,
            )
        )

    return commits, changes


def detect_language(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    mapping = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".go": "Go",
        ".rb": "Ruby",
        ".php": "PHP",
        ".cs": "C#",
        ".cpp": "C++",
        ".c": "C",
        ".rs": "Rust",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".scala": "Scala",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".less": "LESS",
        ".md": "Markdown",
        ".json": "JSON",
        ".yml": "YAML",
        ".yaml": "YAML",
        ".xml": "XML",
        ".sql": "SQL",
        ".sh": "Shell",
        ".dockerfile": "Dockerfile",
    }
    return mapping.get(ext, ext.lstrip(".").upper() if ext else "Other")


def normalize_ignore_values(values: list[Any]) -> set[str]:
    normalized = set()
    for value in values:
        text = str(value).strip().lower()
        if text:
            normalized.add(text.lstrip("."))
    return normalized


def should_ignore(filename: str, language: str, ignored_values: set[str]) -> bool:
    ext = Path(filename).suffix.lower().lstrip(".")
    return language.lower() in ignored_values or ext in ignored_values


def summarize(commits: list[CommitMeta], changes: list[FileChange], ignored_values: set[str]) -> Summary:
    contributor_commits = Counter(commit.author for commit in commits)
    contributor_churn: Counter[str] = Counter()
    language_churn: Counter[str] = Counter()
    file_churn: Counter[str] = Counter()
    daily_commits = Counter(commit.date for commit in commits)

    additions = 0
    deletions = 0

    for change in changes:
        churn = change.additions + change.deletions
        additions += change.additions
        deletions += change.deletions
        contributor_churn[change.author] += churn
        file_churn[change.filename] += churn

        language = detect_language(change.filename)
        if not should_ignore(change.filename, language, ignored_values):
            language_churn[language] += churn

    changed_files = {change.filename for change in changes}

    return Summary(
        commits=len(commits),
        contributors=len(contributor_commits),
        additions=additions,
        deletions=deletions,
        churn=additions + deletions,
        files_changed=len(changed_files),
        contributor_commits=contributor_commits,
        contributor_churn=contributor_churn,
        language_churn=language_churn,
        file_churn=file_churn,
        daily_commits=daily_commits,
    )


def slugify(label: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", label.strip().lower())
    return slug.strip("_") or "window"


def compute_rolling(values: list[int], window: int) -> list[float]:
    out: list[float] = []
    for idx in range(len(values)):
        start = max(0, idx - window + 1)
        segment = values[start : idx + 1]
        out.append(sum(segment) / len(segment))
    return out


def figure_size(graph_cfg: dict[str, Any], default_width: float, default_height: float) -> tuple[float, float]:
    width = graph_cfg.get("width", default_width)
    height = graph_cfg.get("height", default_height)

    try:
        width_value = float(width)
    except (TypeError, ValueError):
        width_value = default_width

    try:
        height_value = float(height)
    except (TypeError, ValueError):
        height_value = default_height

    # If values look like pixels, normalize to inches for matplotlib.
    if width_value > 50:
        width_value = width_value / 100
    if height_value > 50:
        height_value = height_value / 100

    return max(width_value, 5.5), max(height_value, 2.6)


def build_daily_series(daily_counter: Counter[dt.date]) -> tuple[list[dt.date], list[int]]:
    if not daily_counter:
        return [], []

    start_date = min(daily_counter)
    end_date = max(daily_counter)
    days = []
    counts = []

    cursor = start_date
    while cursor <= end_date:
        days.append(cursor)
        counts.append(daily_counter.get(cursor, 0))
        cursor += dt.timedelta(days=1)

    return days, counts


def plot_commit_activity(label: str, summary: Summary, graph_cfg: dict[str, Any]) -> Path | None:
    if not summary.daily_commits:
        return None

    modules = get_plot_modules()
    if modules is None:
        return None
    mdates, plt = modules

    days, counts = build_daily_series(summary.daily_commits)
    rolling = compute_rolling(counts, window=7)

    fig_w, fig_h = figure_size(graph_cfg, default_width=8.2, default_height=3.2)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    base_color = graph_cfg.get("color", "#4e79a7")
    ax.bar(days, counts, color=base_color, alpha=0.35, label="Daily commits")
    ax.plot(days, rolling, color="#e15759", linewidth=2.0, label="7-day rolling avg")

    ax.set_title(f"Commit Activity - {label}")
    ax.set_ylabel("Commits")
    ax.grid(True, axis="y", linestyle="--", alpha=0.25)
    ax.legend(loc="upper right")

    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    fig.tight_layout()
    output = STATS_DIR / f"commits_{slugify(label)}.png"
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def plot_language_breakdown(label: str, summary: Summary) -> Path | None:
    if not summary.language_churn:
        return None

    modules = get_plot_modules()
    if modules is None:
        return None
    _, plt = modules

    ranked = summary.language_churn.most_common(8)
    remainder = sum(summary.language_churn.values()) - sum(v for _, v in ranked)
    if remainder > 0:
        ranked.append(("Other", remainder))

    labels = [name for name, _ in ranked]
    values = [value for _, value in ranked]

    fig, ax = plt.subplots(figsize=(6.4, 5.1))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        startangle=120,
        autopct=lambda pct: f"{pct:.1f}%" if pct >= 3 else "",
        wedgeprops={"width": 0.42},
        pctdistance=0.8,
        labeldistance=1.06,
    )

    for text in texts:
        text.set_fontsize(8)
    for auto in autotexts:
        auto.set_fontsize(8)

    ax.set_title(f"Language Churn Breakdown - {label}")
    ax.axis("equal")

    fig.tight_layout()
    output = STATS_DIR / f"language_{slugify(label)}.png"
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def plot_contributor_churn(label: str, summary: Summary, max_contributors: int) -> Path | None:
    if not summary.contributor_churn:
        return None

    modules = get_plot_modules()
    if modules is None:
        return None
    _, plt = modules

    ranked = summary.contributor_churn.most_common(max_contributors)
    names = [name for name, _ in reversed(ranked)]
    values = [value for _, value in reversed(ranked)]

    fig, ax = plt.subplots(figsize=(8.0, 4.2))
    ax.barh(names, values, color="#76b7b2")
    ax.set_title(f"Top Contributors by Churn - {label}")
    ax.set_xlabel("Lines changed (+/-)")
    ax.grid(True, axis="x", linestyle="--", alpha=0.25)

    fig.tight_layout()
    output = STATS_DIR / f"contributors_{slugify(label)}.png"
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def build_overview_block(
    ordered_labels: list[str],
    summaries: dict[str, Summary],
    primary_label: str,
    max_contributors: int,
) -> str:
    lines = ["## Repository Analytics Overview", ""]
    lines.append("| Window | Commits | Contributors | +Add | -Del | Churn | Files | Avg Churn/Commit |")
    lines.append("|--------|---------|--------------|------|------|-------|-------|------------------|")

    for label in ordered_labels:
        summary = summaries[label]
        avg_churn = (summary.churn / summary.commits) if summary.commits else 0.0
        lines.append(
            f"| {label} | {summary.commits} | {summary.contributors} | {summary.additions} | {summary.deletions} | "
            f"{summary.churn} | {summary.files_changed} | {avg_churn:.1f} |"
        )

    primary = summaries[primary_label]
    lines.extend([
        "",
        f"### Top Contributors ({primary_label})",
        "",
        "| Contributor | Commits | Churn | Share of Churn |",
        "|-------------|---------|-------|----------------|",
    ])

    total_churn = max(primary.churn, 1)
    for author, churn in primary.contributor_churn.most_common(max_contributors):
        share = (churn / total_churn) * 100
        lines.append(
            f"| {author} | {primary.contributor_commits.get(author, 0)} | {churn} | {share:.1f}% |"
        )

    if not primary.contributor_churn:
        lines.append("| _No contributor activity_ | 0 | 0 | 0.0% |")

    lines.extend([
        "",
        f"### Most Changed Files ({primary_label})",
        "",
        "| File | Churn |",
        "|------|-------|",
    ])

    for filename, churn in primary.file_churn.most_common(10):
        safe_name = filename.replace("|", "\\|")
        lines.append(f"| `{safe_name}` | {churn} |")

    if not primary.file_churn:
        lines.append("| _No file-level changes_ | 0 |")

    return "\n".join(lines)


def build_commits_block(
    ordered_labels: list[str],
    summaries: dict[str, Summary],
    commit_charts: dict[str, Path | None],
) -> str:
    lines = ["## Commit Activity Trends", ""]

    for label in ordered_labels:
        summary = summaries[label]
        chart = commit_charts.get(label)

        active_days = sum(1 for count in summary.daily_commits.values() if count > 0)
        if summary.daily_commits:
            peak_day, peak_count = max(summary.daily_commits.items(), key=lambda item: item[1])
            peak_text = f"{peak_day.isoformat()} ({peak_count})"
        else:
            peak_text = "n/a"

        lines.append(f"### {label}")
        lines.append(
            f"- Commits: **{summary.commits}** | Active days: **{active_days}** | Peak day: **{peak_text}**"
        )
        lines.append(
            f"- Additions: **{summary.additions}** | Deletions: **{summary.deletions}** | Churn: **{summary.churn}**"
        )
        if chart:
            lines.append(f"![{label} Commit Activity]({chart.as_posix()})")
        else:
            lines.append("_No commit activity in this window._")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_language_block(
    ordered_labels: list[str],
    summaries: dict[str, Summary],
    language_charts: dict[str, Path | None],
) -> str:
    lines = ["## Language Breakdown", ""]

    for label in ordered_labels:
        summary = summaries[label]
        total = sum(summary.language_churn.values())
        lines.append(f"### {label}")

        if total == 0:
            lines.append("_No language churn data in this window._")
            lines.append("")
            continue

        lines.append("| Language | Churn | Share |")
        lines.append("|----------|-------|-------|")
        for language, churn in summary.language_churn.most_common(8):
            share = (churn / total) * 100
            lines.append(f"| {language} | {churn} | {share:.1f}% |")

        chart = language_charts.get(label)
        if chart:
            lines.append("")
            lines.append(f"![{label} Language Breakdown]({chart.as_posix()})")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_pulse_block(
    generated_at: dt.datetime,
    all_time_label: str,
    all_time_summary: Summary,
    pulse_contributor_chart: Path | None,
    all_time_commit_chart: Path | None,
) -> str:
    first_commit = run_git(["log", "--reverse", "--format=%ad", "--date=short", "-1"]).strip() or "n/a"
    last_commit = run_git(["log", "-1", "--format=%ad", "--date=short"]).strip() or "n/a"

    lines = [
        "## Repository Pulse",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Commits ({all_time_label}) | {all_time_summary.commits} |",
        f"| Contributors ({all_time_label}) | {all_time_summary.contributors} |",
        f"| Lines Added ({all_time_label}) | {all_time_summary.additions} |",
        f"| Lines Deleted ({all_time_label}) | {all_time_summary.deletions} |",
        f"| Churn ({all_time_label}) | {all_time_summary.churn} |",
        f"| Files Changed ({all_time_label}) | {all_time_summary.files_changed} |",
        f"| First Commit Date | {first_commit} |",
        f"| Last Commit Date | {last_commit} |",
        "",
        f"_Generated: {generated_at.strftime('%Y-%m-%d %H:%M UTC')}_",
    ]

    if pulse_contributor_chart:
        lines.extend(["", f"![Top Contributor Churn]({pulse_contributor_chart.as_posix()})"])

    if all_time_commit_chart:
        lines.extend(["", f"![All Time Commit Activity]({all_time_commit_chart.as_posix()})"])

    return "\n".join(lines)


def replace_block(text: str, block_type: str, inner_markdown: str) -> str:
    typed_start = f"<!-- STATS BREAKDOWN START:{block_type} -->"
    typed_end = f"<!-- STATS BREAKDOWN END:{block_type} -->"

    pattern = re.compile(
        rf"({re.escape(typed_start)})(.*?)({re.escape(typed_end)})",
        re.DOTALL,
    )

    def replacement(match: re.Match[str]) -> str:
        return f"{match.group(1)}\n\n{inner_markdown.strip()}\n\n{match.group(3)}"

    updated, count = pattern.subn(replacement, text, count=1)
    if count > 0:
        return updated

    # Fallback for untyped marker style.
    untyped_start = "<!-- STATS BREAKDOWN START -->"
    untyped_end = "<!-- STATS BREAKDOWN END -->"
    fallback = re.compile(
        rf"({re.escape(untyped_start)})(.*?)({re.escape(untyped_end)})",
        re.DOTALL,
    )

    updated, count = fallback.subn(replacement, text, count=1)
    if count > 0:
        return updated

    # Marker missing: append typed block at end to avoid silent data loss.
    return text.rstrip() + f"\n\n{typed_start}\n\n{inner_markdown.strip()}\n\n{typed_end}\n"


def choose_primary_window(ordered_labels: list[str], raw_timeframes: dict[str, Any]) -> str:
    for label in ordered_labels:
        value = raw_timeframes.get(label)
        if value not in (None, "all", "ALL", ""):
            return label
    return ordered_labels[0]


def choose_all_time_window(ordered_labels: list[str], raw_timeframes: dict[str, Any]) -> str:
    for label in ordered_labels:
        value = raw_timeframes.get(label)
        if value is None or (isinstance(value, str) and value.strip().lower() in {"", "all"}):
            return label
    return ordered_labels[0]


def main() -> None:
    STATS_DIR.mkdir(exist_ok=True)

    readme_text = README_PATH.read_text(encoding="utf-8")
    config = parse_analytics_config(readme_text)

    raw_timeframes = config.get("timeframes", {})
    if not raw_timeframes:
        raw_timeframes = DEFAULT_CONFIG["timeframes"]

    ordered_labels = list(raw_timeframes.keys())
    ignored_values = normalize_ignore_values(config.get("languages", {}).get("ignore", []))
    graph_cfg = config.get("graphs", {})
    show_graphs = bool(graph_cfg.get("show", True))
    if show_graphs and get_plot_modules() is None:
        show_graphs = False
    max_contributors = int(config.get("contributors", {}).get("max", 10))

    summaries: dict[str, Summary] = {}
    commit_charts: dict[str, Path | None] = {}
    language_charts: dict[str, Path | None] = {}

    for label, timeframe_value in raw_timeframes.items():
        commits, changes = parse_history(timeframe_value)
        summary = summarize(commits, changes, ignored_values)
        summaries[label] = summary

        if show_graphs:
            commit_charts[label] = plot_commit_activity(label, summary, graph_cfg)
            language_charts[label] = plot_language_breakdown(label, summary)
        else:
            commit_charts[label] = None
            language_charts[label] = None

    primary_label = choose_primary_window(ordered_labels, raw_timeframes)
    all_time_label = choose_all_time_window(ordered_labels, raw_timeframes)

    overview_block = build_overview_block(
        ordered_labels=ordered_labels,
        summaries=summaries,
        primary_label=primary_label,
        max_contributors=max_contributors,
    )

    commits_block = build_commits_block(
        ordered_labels=ordered_labels,
        summaries=summaries,
        commit_charts=commit_charts,
    )

    language_block = build_language_block(
        ordered_labels=ordered_labels,
        summaries=summaries,
        language_charts=language_charts,
    )

    pulse_chart = (
        plot_contributor_churn(all_time_label, summaries[all_time_label], max_contributors)
        if show_graphs
        else None
    )
    pulse_block = build_pulse_block(
        generated_at=dt.datetime.utcnow(),
        all_time_label=all_time_label,
        all_time_summary=summaries[all_time_label],
        pulse_contributor_chart=pulse_chart,
        all_time_commit_chart=commit_charts.get(all_time_label),
    )

    changelog_cfg = config.get("changelog", {})
    changelog_block = build_changelog_markdown(
        max_entries=int(changelog_cfg.get("max_entries", 80)),
        max_days=int(changelog_cfg.get("max_days", 45)),
        max_per_day=int(changelog_cfg.get("max_per_day", 8)),
        include_authors=bool(changelog_cfg.get("include_authors", True)),
    )

    include_blocks = [
        str(name).upper()
        for name in config.get("sections", {}).get("include", DEFAULT_BLOCKS)
    ]

    if "PULSE" in include_blocks:
        readme_text = replace_block(readme_text, "PULSE", pulse_block)
    if "OVERVIEW" in include_blocks:
        readme_text = replace_block(readme_text, "OVERVIEW", overview_block)
    if "COMMITS" in include_blocks:
        readme_text = replace_block(readme_text, "COMMITS", commits_block)
    if "LANGUAGE" in include_blocks and config.get("languages", {}).get("show_breakdown", True):
        readme_text = replace_block(readme_text, "LANGUAGE", language_block)
    if "CHANGELOG" in include_blocks and changelog_cfg.get("show", True):
        readme_text = replace_block(readme_text, "CHANGELOG", changelog_block)

    README_PATH.write_text(readme_text, encoding="utf-8")
    print("OK: README analytics + changelog blocks updated (markers/config preserved).")


if __name__ == "__main__":
    main()
