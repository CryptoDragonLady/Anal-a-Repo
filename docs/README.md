# Repository Analytics Documentation

Welcome to the comprehensive documentation for the **Repository Analytics** project. This documentation site provides detailed guides, API references, and practical examples for all six Python scripts in this repository.

## Quick Links

### 🚀 Getting Started
- [Installation Guide](docs/getting-started/installation) - Set up the project
- [Quick Start](docs/getting-started/quick-start) - Get running in 3 minutes
- [Basic Usage](docs/getting-started/basic-usage) - Learn the fundamentals

### 📚 Script Documentation
- [generate_stats.py](docs/scripts/generate-stats) - Basic stats with configurable blocks
- [generate_stats2.py](docs/scripts/generate-stats2) - Enhanced analytics with charts
- [generate_stats3.py](docs/scripts/generate-stats3) - Config-based analytics
- [generate_stats4.py](docs/scripts/generate-stats4) - Enhanced language breakdown
- [generate_stats_fromtemplate.py](docs/scripts/generate-stats-fromtemplate) - Template-based generation
- [generate_stats_fromtemplate_withgraphs.py](docs/scripts/generate-stats-fromtemplate-withgraphs) - Full-featured with graphs

### ⚙️ Configuration
- [Configuration Guide](docs/configuration) - Complete configuration reference
- [Timeframes](docs/configuration/timeframes) - Time period configuration
- [Languages](docs/configuration/languages) - Language filtering options
- [Graphs](docs/configuration/graphs) - Chart customization
- [Blocks](docs/configuration/blocks) - Analytics block selection

### 📖 Examples & Guides
- [Usage Examples](docs/examples) - 10+ real-world examples
- [API Reference](docs/api/overview) - Function-level documentation
- [Troubleshooting](docs/troubleshooting) - Common issues and solutions
- [Advanced Topics](docs/advanced/github-actions) - GitHub Actions, custom templates, extensions

## Building the Documentation

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation
```bash
cd docs
npm install
```

### Development Mode
```bash
npm run start
```
Starts development server at `http://localhost:3000` with live reload.

### Build for Production
```bash
npm run build
```
Generates optimized static files in `build/` directory.

### Serve Production Build
```bash
npm run serve
```
Locally test the production build at `http://localhost:3000`.

## Documentation Structure

```
📁 docs/
├── 📄 intro.md                     # Project introduction
├── 📁 getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── basic-usage.md
├── 📁 scripts/
│   ├── generate-stats.md
│   ├── generate-stats2.md
│   ├── generate-stats3.md
│   ├── generate-stats4.md
│   ├── generate-stats-fromtemplate.md
│   └── generate-stats-fromtemplate-withgraphs.md
├── 📁 configuration/
│   ├── timeframes.md
│   ├── languages.md
│   ├── graphs.md
│   └── blocks.md
├── 📁 api/
│   ├── overview.md
│   ├── git-helpers.md
│   ├── config-parsing.md
│   ├── report-generation.md
│   └── markdown-processing.md
├── 📁 advanced/
│   ├── github-actions.md
│   ├── custom-templates.md
│   └── extending-scripts.md
├── 📄 configuration.md             # Config overview
├── 📄 examples.md                  # Usage examples
└── 📄 troubleshooting.md           # Troubleshooting
```

## Key Features

### 📊 Comprehensive Documentation
- All 6 scripts fully documented
- Function-level API reference
- Complete configuration guide
- 10+ real-world examples

### 🎯 Well-Organized
- Intuitive sidebar navigation
- Clear categorization
- Cross-references between topics
- Search functionality

### 💡 Practical
- Quick start guide
- Troubleshooting section
- GitHub Actions examples
- Pre-commit hook setup

### 🎨 Professional
- Responsive design
- Dark mode support
- Syntax highlighting
- Mobile-friendly

## Documentation Statistics

- **Total Lines**: 3,332+
- **Markdown Files**: 30+
- **HTML Pages**: 37
- **Build Size**: 3.1 MB
- **Scripts Documented**: 6/6

## For Users

Start here based on your needs:

**New to the project?**
→ [Introduction](docs/intro) → [Installation](docs/getting-started/installation) → [Quick Start](docs/getting-started/quick-start)

**Want to use a specific script?**
→ [Scripts Reference](docs/category/scripts-reference)

**Need to configure scripts?**
→ [Configuration Guide](docs/configuration)

**Looking for examples?**
→ [Usage Examples](docs/examples)

**Stuck with a problem?**
→ [Troubleshooting](docs/troubleshooting)

**Want to extend functionality?**
→ [Advanced Topics](docs/advanced/extending-scripts)

## Contributing to Documentation

Found an issue in the docs? Want to improve them?

1. Edit the relevant `.md` file in `docs/docs/`
2. Test locally with `npm run start`
3. Submit a pull request

## Support

- 📖 Check [Troubleshooting](docs/troubleshooting) for common issues
- 🔍 Use the search function to find topics
- 💬 Open an issue on GitHub
- 🐛 Report documentation bugs

## Technology

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

- **Docusaurus 3.x** - Static site generator
- **TypeScript** - Configuration
- **Markdown** - Content
- **MDX** - Enhanced markdown

## License

Documentation is part of the Repository Analytics project.

---

**Last Updated**: November 9, 2025
**Status**: ✅ Complete and Built
