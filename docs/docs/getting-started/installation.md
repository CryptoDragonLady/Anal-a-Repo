---
sidebar_position: 1
title: Installation
---

# Installation Guide

This guide will walk you through installing the Repository Analytics scripts and their dependencies.

## Prerequisites

Before installing, ensure you have the following:

### Required
- **Python 3.6 or higher**
  ```bash
  python --version  # Should show 3.6+
  ```

- **Git**
  ```bash
  git --version  # Any modern version
  ```

- **A Git Repository**
  The scripts must be run within a Git repository to analyze commits.

### Optional Dependencies
Some scripts require additional Python packages for advanced features:

- **matplotlib**: For generating charts and graphs
- **pandas**: For enhanced data processing

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd analrepo
```

### 2. Install Python Dependencies

#### For Basic Scripts (stats, stats3, stats4, fromtemplate)

No additional dependencies required! These scripts use only Python standard library.

```bash
# Test if basic scripts work
python generate_stats.py --help
```

#### For Advanced Scripts (stats2, fromtemplate_withgraphs)

Install matplotlib and pandas:

```bash
# Using pip
pip install matplotlib pandas

# Or using pip3
pip3 install matplotlib pandas

# Or with a requirements file
pip install -r requirements.txt
```

Create a `requirements.txt` file if needed:

```text
matplotlib>=3.3.0
pandas>=1.1.0
```

### 3. Verify Installation

Test that all dependencies are installed correctly:

```bash
python -c "import matplotlib; import pandas; print('All dependencies installed!')"
```

Expected output:
```
All dependencies installed!
```

## Platform-Specific Notes

### Linux/macOS

Installation is straightforward:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip
pip3 install matplotlib pandas

# macOS (with Homebrew)
brew install python
pip3 install matplotlib pandas
```

### Windows

1. **Install Python**: Download from [python.org](https://python.org)
2. **Add Python to PATH**: Check the option during installation
3. **Install packages**:
   ```cmd
   python -m pip install matplotlib pandas
   ```

### Virtual Environments (Recommended)

Using a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install matplotlib pandas

# When done, deactivate
deactivate
```

## Troubleshooting Installation

### Common Issues

#### ImportError: No module named 'matplotlib'

**Solution**: Install matplotlib
```bash
pip install matplotlib
```

#### Permission Denied

**Solution**: Use user install or virtual environment
```bash
pip install --user matplotlib pandas
```

#### Python version too old

**Solution**: Upgrade Python
```bash
# Ubuntu/Debian
sudo apt-get install python3.9

# macOS
brew upgrade python3
```

#### pip not found

**Solution**: Install pip
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# macOS (should come with Python)
python3 -m ensurepip
```

## Verifying Your Installation

Run the verification script:

```python
#!/usr/bin/env python3
import sys
print(f"Python version: {sys.version}")

try:
    import matplotlib
    print(f"✓ matplotlib {matplotlib.__version__}")
except ImportError:
    print("✗ matplotlib not installed")

try:
    import pandas
    print(f"✓ pandas {pandas.__version__}")
except ImportError:
    print("✗ pandas not installed")

try:
    import subprocess
    result = subprocess.run(['git', '--version'], capture_output=True, text=True)
    print(f"✓ {result.stdout.strip()}")
except Exception:
    print("✗ git not found")
```

Save as `verify.py` and run:
```bash
python verify.py
```

## Next Steps

Now that you have everything installed:

1. **Quick Start**: Follow the [Quick Start Guide](/docs/getting-started/quick-start)
2. **Basic Usage**: Learn [Basic Usage](/docs/getting-started/basic-usage)
3. **Explore Scripts**: Check out [Scripts Reference](/docs/category/scripts-reference)

## Update Instructions

To update to the latest version:

```bash
cd analrepo
git pull origin main

# Update dependencies if needed
pip install --upgrade matplotlib pandas
```

## Uninstallation

To remove the scripts:

```bash
# Remove the repository
rm -rf analrepo

# Optionally remove Python packages
pip uninstall matplotlib pandas
```

## Getting Help

If you encounter installation issues:

1. Check the [Troubleshooting Guide](/docs/troubleshooting)
2. Verify Python and Git versions meet requirements
3. Try using a virtual environment
4. Check GitHub issues for similar problems
5. Create a new issue with your error message
