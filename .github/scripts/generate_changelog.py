#!/usr/bin/env python3
"""Generate markdown changelog content from git history."""

from __future__ import annotations

import datetime as dt
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class CommitEntry:
    date: dt.date
    short_hash: str
    author: str
    subject: str
    category: str


def _run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def _categorize(subject: str) -> str:
    lowered = subject.strip().lower()

    if lowered.startswith(("feat:", "feature:", "add:")):
        return "feature"
    if lowered.startswith(("fix:", "bugfix:", "hotfix:")):
        return "fix"
    if "security" in lowered or lowered.startswith(("sec:", "security:")):
        return "security"
    if lowered.startswith(("perf:", "optimize:")):
        return "performance"
    if lowered.startswith(("refactor:", "cleanup:")):
        return "refactor"
    if lowered.startswith(("docs:", "doc:")):
        return "docs"
    if lowered.startswith(("test:", "tests:")):
        return "test"
    if lowered.startswith(("build:", "ci:", "chore:", "release:")):
        return "ops"
    if lowered.startswith(("revert:",)):
        return "revert"
    return "other"


def _strip_prefix(subject: str) -> str:
    return subject.split(":", 1)[1].strip() if ":" in subject else subject.strip()


def collect_commits(max_entries: int = 80, max_days: int = 45) -> list[CommitEntry]:
    since_date = (dt.datetime.utcnow() - dt.timedelta(days=max_days)).strftime("%Y-%m-%d")
    args = [
        "log",
        f"--since={since_date}",
        f"--max-count={max_entries}",
        "--date=short",
        "--pretty=format:%ad|%h|%an|%s",
        "--no-merges",
    ]
    output = _run_git(args)

    entries: list[CommitEntry] = []
    for line in output.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        date_text, short_hash, author, subject = parts
        try:
            commit_date = dt.datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            continue

        entries.append(
            CommitEntry(
                date=commit_date,
                short_hash=short_hash,
                author=author,
                subject=subject,
                category=_categorize(subject),
            )
        )

    return entries


def build_changelog_markdown(
    max_entries: int = 80,
    max_days: int = 45,
    max_per_day: int = 8,
    include_authors: bool = True,
) -> str:
    entries = collect_commits(max_entries=max_entries, max_days=max_days)
    generated = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    if not entries:
        return (
            "_No commits found in the configured changelog window._\n\n"
            f"_Generated: {generated}_"
        )

    by_date: dict[dt.date, list[CommitEntry]] = defaultdict(list)
    category_totals: Counter[str] = Counter()

    for entry in entries:
        by_date[entry.date].append(entry)
        category_totals[entry.category] += 1

    lines = [
        f"_Generated from git history: last {max_days} days / up to {max_entries} commits._",
        f"_Updated: {generated}_",
        "",
        "### Summary",
        "",
        f"- Commits analyzed: **{len(entries)}**",
        f"- Feature commits: **{category_totals.get('feature', 0)}**",
        f"- Fix commits: **{category_totals.get('fix', 0)}**",
        f"- Security commits: **{category_totals.get('security', 0)}**",
        f"- Refactor/performance commits: **{category_totals.get('refactor', 0) + category_totals.get('performance', 0)}**",
        "",
    ]

    for commit_date in sorted(by_date.keys(), reverse=True):
        lines.append(f"### {commit_date.isoformat()}")
        day_entries = by_date[commit_date][:max_per_day]

        for entry in day_entries:
            category = entry.category.upper()
            subject_text = _strip_prefix(entry.subject)
            if include_authors:
                lines.append(
                    f"- **[{category}]** {subject_text} (`{entry.short_hash}`, {entry.author})"
                )
            else:
                lines.append(f"- **[{category}]** {subject_text} (`{entry.short_hash}`)")

        hidden = len(by_date[commit_date]) - len(day_entries)
        if hidden > 0:
            lines.append(f"- _... {hidden} additional commits omitted for brevity_")

        lines.append("")

    return "\n".join(lines).strip() + "\n"


if __name__ == "__main__":
    print(build_changelog_markdown())
