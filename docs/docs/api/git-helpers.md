---
title: Git Helpers
description: Functions that query commit history and diffs to produce analytics.
---

The helpers wrap Git commands for consistent, parseable output.

git_log

```python
def git_log(args):
    result = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()
```

get_commit_stats

```python
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
```

get_diff_stats

```python
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
                add = int(parts[0]); delete = int(parts[1])
            except ValueError:
                continue
            ext = Path(parts[2]).suffix.lower().replace(".", "")
            if ext in ignored_exts:
                continue
            language_counts[ext] += add + delete
            total_add += add; total_del += delete
    return total_add, total_del, language_counts
```

Notes:

- get_diff_stats uses “numstat” for machine-friendly counts
- Binary changes may appear as “-” and are skipped