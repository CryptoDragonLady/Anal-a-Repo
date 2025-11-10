---
sidebar_position: 7
title: Troubleshooting
---

# Troubleshooting Guide

Common issues and their solutions when using Repository Analytics scripts.

## Installation Issues

### Python Not Found

**Error**: `python: command not found`

**Solutions**:
```bash
# Try python3
python3 generate_stats.py

# Or install Python
# Ubuntu/Debian:
sudo apt-get install python3

# macOS:
brew install python3

# Windows: Download from python.org
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'matplotlib'`

**Solution**:
```bash
pip install matplotlib pandas

# If pip not found:
python -m pip install matplotlib pandas

# Or with pip3:
pip3 install matplotlib pandas
```

### Permission Denied

**Error**: `Permission denied` when installing packages

**Solutions**:
```bash
# Option 1: User install
pip install --user matplotlib pandas

# Option 2: Virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
pip install matplotlib pandas
```

## Script Execution Issues

### No Markers Found

**Error**: Script runs but README unchanged

**Cause**: Missing or incorrect markers

**Solution**: Add markers to README.md
```markdown
<!-- STATS BREAKDOWN START:OVERVIEW -->
<!-- Content will be replaced -->
<!-- STATS BREAKDOWN END:OVERVIEW -->
```

**Check**:
- Markers exactly match format (case-sensitive)
- Markers are in pairs (START and END)
- Block type is correct (OVERVIEW, LANGUAGE, etc.)

### Git Repository Not Found

**Error**: `fatal: not a git repository`

**Solution**:
```bash
# Check if you're in a git repo
git status

# If not, initialize:
git init
git add .
git commit -m "Initial commit"
```

### No Commits Found

**Error**: Stats show zero commits or "No activity"

**Causes**:
1. Repository has no commits
2. Timeframe excludes all commits
3. Git log command failing

**Solutions**:
```bash
# Check commit history
git log

# Make a commit if none exist
echo "test" > test.txt
git add test.txt
git commit -m "Test commit"

# Try with broader timeframe
# Change "7d" to "365d" in config
```

## Configuration Issues

### JSON Parse Error

**Error**: `Invalid JSON in analytics config`

**Solution**:
1. Validate JSON at [jsonlint.com](https://jsonlint.com)
2. Common mistakes:
   ```json
   // Wrong: Trailing comma
   {
     "timeframes": {...},  ← Remove this comma
   }
   
   // Wrong: Single quotes
   {'timeframes': {...}}  ← Use double quotes
   "timeframes": {...}
   
   // Wrong: Unquoted keys
   {timeframes: {...}}    ← Quote keys
   {"timeframes": {...}}
   ```

### Config Not Applied

**Symptom**: Changes to config don't affect output

**Checks**:
1. Config in correct location (inside `<details>` block)
2. Using script that reads config (stats3, stats4, fromtemplate)
3. Proper JSON formatting
4. Config block properly closed

**Example**:
````markdown
<details>
<summary>📈 Analytics Config</summary>

```json
{
  "timeframes": {
    "All Time": null
  }
}
```

</details>
````

### Timeframe Not Working

**Symptom**: Timeframe shows wrong data or errors

**Solutions**:
```json
// Correct formats:
"All Time": null
"Last 30 Days": "30d"    // For stats3/stats4
"Last 30 Days": 30       // For stats2/fromtemplate_withgraphs
"Last 24 Hours": "24h"

// Wrong:
"Last 30 Days": "30"     // Missing 'd'
"Last 30 Days": "30 days"  // No spaces
```

## Output Issues

### Empty Statistics

**Symptom**: Tables show 0 commits, no data

**Debug Steps**:
```bash
# 1. Check git log works
git log --oneline

# 2. Check diff works
git diff --numstat

# 3. Try basic timeframe
# Use "All Time": null

# 4. Check for errors
python generate_stats.py 2>&1 | grep -i error
```

### Wrong Language Percentages

**Symptom**: Language breakdown doesn't match repository

**Causes**:
1. Ignore list too broad
2. File extensions not detected
3. Recent changes not committed

**Solutions**:
```json
// Check ignore list
"languages": {
  "ignore": ["lock"]  // Are you ignoring too much?
}

// Commit recent changes
git add .
git commit -m "Update files"
python generate_stats.py
```

### Charts Not Generating

**Symptom**: No PNG files in `stats/` directory

**Checks**:
1. Dependencies installed:
   ```bash
   python -c "import matplotlib; import pandas"
   ```

2. Directory writable:
   ```bash
   ls -ld stats/
   ```

3. Using correct script:
   ```bash
   # These generate charts:
   python generate_stats2.py
   python generate_stats_fromtemplate_withgraphs.py
   
   # These don't:
   python generate_stats.py
   python generate_stats3.py
   python generate_stats4.py
   python generate_stats_fromtemplate.py
   ```

### Charts Low Quality

**Symptom**: Blurry or pixelated charts

**Solution**: Increase DPI in script
```python
# In plotting function, change:
plt.savefig(chart_path, dpi=150)  # Default
# To:
plt.savefig(chart_path, dpi=300)  # Higher quality
```

## Template Issues

### Template Not Found

**Error**: `FileNotFoundError: README_TEMPLATE.md`

**Solution**:
```bash
# Create template from existing README
cp README.md README_TEMPLATE.md

# Or create new template
echo "# Project" > README_TEMPLATE.md
```

### Markers Not Removed

**Symptom**: Output README still has markers

**Cause**: Using wrong script

**Solution**:
```bash
# These remove markers:
python generate_stats_fromtemplate.py
python generate_stats_fromtemplate_withgraphs.py

# These keep markers:
python generate_stats.py
python generate_stats2.py
python generate_stats3.py
python generate_stats4.py
```

## Performance Issues

### Script Runs Slowly

**Symptoms**: Takes minutes to complete

**Solutions**:

1. **Reduce timeframes**:
   ```json
   // Instead of 6 timeframes:
   "timeframes": {
     "All Time": null,
     "Last Month": "30d"  // Just 2
   }
   ```

2. **Limit git history**:
   ```bash
   # Add shallow clone option
   git clone --depth=1000 repo.git
   ```

3. **Use simpler script**:
   ```bash
   # Faster:
   python generate_stats.py
   
   # Slower (but more features):
   python generate_stats2.py
   ```

### High Memory Usage

**Symptom**: Script uses lots of RAM

**Solutions**:
1. Close other applications
2. Reduce figure sizes in chart scripts:
   ```python
   plt.subplots(figsize=(4, 4))  # Smaller
   ```

## GitHub Actions Issues

### Action Fails to Install Dependencies

**Error**: `pip install matplotlib` fails in workflow

**Solution**:
```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.x"
    cache: 'pip'  # Add caching

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install matplotlib pandas
```

### Commits Not Pushing

**Symptom**: Action runs but changes don't appear

**Checks**:
1. Permissions set:
   ```yaml
   permissions:
     contents: write
   ```

2. Git config set:
   ```yaml
   - name: Configure git
     run: |
       git config user.name "github-actions[bot]"
       git config user.email "actions@github.com"
   ```

3. Actually has changes to commit:
   ```yaml
   - name: Commit changes
     run: |
       git add README.md stats/
       git diff --quiet && echo "No changes" || \
         (git commit -m "Update analytics" && git push)
   ```

## Font/Display Issues

### Font Warnings with Matplotlib

**Warning**: `findfont: Font family [...] not found`

**Solution**:
```python
# Add to script before plotting
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'

# Or install fonts:
# Ubuntu/Debian:
sudo apt-get install fonts-dejavu

# macOS:
# Fonts usually pre-installed
```

### Bars Not Aligned in Terminal

**Symptom**: Language breakdown bars misaligned

**Cause**: Non-monospace font

**Solution**: Use monospace terminal font:
- Terminal: Set font to "Monospace" or "Courier New"
- VS Code: Set `"terminal.integrated.fontFamily": "monospace"`

## Debug Mode

### Enable Verbose Output

Add debug prints to troubleshoot:

```python
# At top of script
import sys

# Before problematic section
print(f"DEBUG: Config = {cfg}", file=sys.stderr)
print(f"DEBUG: Timeframes = {timeframes}", file=sys.stderr)

# Run script and check stderr
python generate_stats.py 2> debug.log
```

### Check Git Commands

Test git commands manually:

```bash
# Test log command
git log --shortstat --pretty=format:%H%x09%an%x09%ad --date=iso

# Test diff command
git diff --numstat

# Test with timeframe
git log --since="2024-01-01" --oneline
```

## Getting Help

If you're still stuck:

1. **Check Script Output**: Look for error messages
2. **Verify Requirements**: Python 3.6+, Git, dependencies
3. **Test Minimal Example**: Try with simple README
4. **Check GitHub Issues**: Search for similar problems
5. **Create Issue**: Include:
   - Script name and version
   - Error message (full output)
   - Your configuration
   - Steps to reproduce

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing dependency | Install with pip |
| `FileNotFoundError` | Missing file | Check file exists |
| `JSONDecodeError` | Invalid JSON | Validate JSON syntax |
| `git: command not found` | Git not installed | Install Git |
| `Permission denied` | No write access | Check permissions |
| `UnicodeDecodeError` | Encoding issue | Use UTF-8 encoding |

## Quick Fixes

```bash
# Reset to clean state
git checkout README.md

# Remove generated files
rm -rf stats/

# Reinstall dependencies
pip uninstall matplotlib pandas
pip install matplotlib pandas

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Test minimal setup
echo "<!-- STATS BREAKDOWN START:OVERVIEW -->" >> test.md
echo "<!-- STATS BREAKDOWN END:OVERVIEW -->" >> test.md
python generate_stats.py
```
