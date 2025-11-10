---
sidebar_position: 1
title: Introduction
---

# Repository Analytics Documentation

Welcome to the comprehensive documentation for the **Repository Analytics** project - a powerful suite of Python scripts designed to automatically generate detailed statistics and analytics for your Git repositories.

## What is Repository Analytics?

Repository Analytics is a collection of six specialized Python scripts that analyze your Git repository and generate comprehensive statistics including:

- Commit statistics across multiple timeframes
- Contributor analytics with detailed breakdowns
- Language usage analysis with visual charts
- Commit activity trends over time
- Repository pulse metrics
- Automated README updates with generated analytics

## Key Features

### Automated Statistics Generation
- **Multiple Timeframes**: Analyze data across All Time, Last 30/7 Days, Last 24 Hours, or custom periods
- **Contributor Insights**: Track commits, additions, deletions per contributor
- **Language Breakdown**: Visual charts showing language distribution
- **Activity Trends**: Line graphs of commit activity over time

### Flexible Configuration
- **JSON-based Configuration**: Control all aspects via JSON config blocks
- **Template-Driven**: Clean separation between templates and generated output
- **Customizable Timeframes**: Support for `d` (days) and `h` (hours) formats
- **Selective Blocks**: Choose which analytics sections to include

### Visual Analytics
- **Matplotlib Charts**: Pie charts for language breakdown
- **Activity Graphs**: Line charts for commit trends
- **PNG Output**: High-quality charts saved to `stats/` directory
- **README Integration**: Automatic embedding of charts in README

### README Management
- **Marker-based Updates**: Preserve custom content while updating stats
- **Multiple Block Support**: OVERVIEW, LANGUAGE, COMMITS, PULSE sections
- **Template Processing**: Generate clean READMEs from templates
- **Config Removal**: Optionally strip config blocks from output

## The Six Scripts

This project includes six complementary scripts, each designed for specific use cases:

1. **[generate_stats.py](/docs/scripts/generate-stats)** - Basic stats with configurable blocks and markers
2. **[generate_stats2.py](/docs/scripts/generate-stats2)** - Enhanced analytics with pandas and matplotlib
3. **[generate_stats3.py](/docs/scripts/generate-stats3)** - Config-based analytics from README
4. **[generate_stats4.py](/docs/scripts/generate-stats4)** - Enhanced with real language calculations
5. **[generate_stats_fromtemplate.py](/docs/scripts/generate-stats-fromtemplate)** - Template-based generation
6. **[generate_stats_fromtemplate_withgraphs.py](/docs/scripts/generate-stats-fromtemplate-withgraphs)** - Full-featured with graphs

## Quick Start

Get started in 3 simple steps:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd analrepo

# 2. Install dependencies (for scripts with charts)
pip install matplotlib pandas

# 3. Run a script
python generate_stats.py
```

Your README will be automatically updated with comprehensive analytics!

## Use Cases

### Personal Projects
Track your coding activity and language preferences over time.

### Team Repositories
Monitor team contributions and identify trends in development activity.

### Open Source Projects
Generate transparent statistics for contributors and community insights.

### GitHub Actions
Automate analytics generation on every commit or scheduled runs.

## Documentation Structure

This documentation is organized into the following sections:

- **Getting Started**: Installation, quick start, and basic usage
- **Scripts Reference**: Detailed documentation for each script
- **Configuration**: How to configure analytics generation
- **API Reference**: Function-level documentation
- **Examples**: Real-world usage examples
- **Troubleshooting**: Common issues and solutions
- **Advanced Topics**: GitHub Actions, custom templates, extensions

## Requirements

- **Python 3.6+**: Core requirement for all scripts
- **Git**: Repository must be a Git repository
- **matplotlib** (optional): For scripts generating charts (stats2, withgraphs)
- **pandas** (optional): For enhanced data processing (stats2, withgraphs)

## Support & Contribution

- **Issues**: Report bugs or request features on GitHub
- **Pull Requests**: Contributions are welcome
- **Documentation**: Help improve these docs

## Next Steps

Ready to get started? Choose your path:

- **New Users**: Start with [Installation](/docs/getting-started/installation)
- **Quick Setup**: Jump to [Quick Start](/docs/getting-started/quick-start)
- **Explore Scripts**: Browse [Scripts Reference](/docs/category/scripts-reference)
- **See Examples**: Check out [Examples](/docs/examples)

Let's dive in and start generating powerful repository analytics!
