# github-profile-builder

Generate original GitHub profile READMEs, stats cards, contribution snakes, wrapped summaries, and certificates from real GitHub API data. Zero third-party dependencies for core output.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-green.svg)](https://pypi.org/project/github-profile-builder/)

## Overview

github-profile-builder is an open-source AI-agent skill and CLI that transforms live GitHub API data into original, self-contained visual assets for your profile. Unlike template-based generators that reuse the same icons and layouts, every SVG produced here is generated from scratch with original code, palettes, and layouts.

### What It Does

- Fetches real data from the GitHub REST and GraphQL APIs
- Generates original SVG stats cards, contribution snakes, wrapped summaries, and certificates
- Produces ready-to-use README.md files for GitHub profiles
- Creates HTML preview pages so you can see results before publishing
- Runs with zero third-party dependencies for core output
- Supports unauthenticated (60 req/hr) and authenticated (5,000 req/hr) API access

### Why It's Different

| Feature | github-profile-builder | Template Generators |
|---------|----------------------|---------------------|
| SVG generation | Original code, from scratch | Reuses external icons/templates |
| Data source | Live GitHub API | Manual input or static data |
| Dependencies | Zero for core output | Often requires Node.js, npm packages |
| Wrapped metrics | Real API data, calendar year | Fabricated or template-based |
| Certificate | Includes explicit disclaimer | May omit disclaimer |
| Safety | XML-escaped, color-validated | May inject raw HTML |

## Quick Start

```bash
# Install
pip install -e .

# Generate everything for a user (unauthenticated, 60 req/hr)
python scripts/generate.py --username aayushmanrajputdev

# Use with a token for higher rate limits (5,000 req/hr)
python scripts/generate.py --username aayushmanrajputdev --token ghp_xxxx

# Generate to a specific directory
python scripts/generate.py --username aayushmanrajputdev --format all --output ./out
```

## Output Formats

### Stats Cards

Original SVG cards showing followers, following, repos, stars, contributions, and more. Each card is self-contained with no external requests at render time.

### Contribution Snake

An original SVG visualization of your contribution grid for the calendar year. Data sourced from the GitHub GraphQL API contributions collection.

### Wrapped Summary

GitHub Wrapped-style cards showing your year-in-review metrics: total contributions, current streak, longest streak, top languages, total stars, and follower count. All numbers come from real API responses.

### Certificate

A shareable SVG certificate acknowledging your contributions, with an explicit disclaimer: _"This certificate is not an official GitHub certification."_

### HTML Preview

A local HTML page displaying all generated assets together. Opens in any browser with no server required.

## Archetypes

Choose a profile style from nine archetypes in references/archetypes.md:

- **Developer** — technical, data-forward, dark theme
- **Creator** — colorful, bold, creator-focused
- **Minimal** — clean, lots of whitespace, restrained palette
- **Researcher** — academic, citation-heavy, serif typography
- **Open Source** — community-focused, badge-heavy
- **Designer** — visual-first, layout-driven
- **Data** — stats-dense, chart-forward
- **Gaming** — high-energy, neon accents
- **Executive** — professional, restrained, leadership metrics

## Color Palettes

Twenty-plus original color schemes in references/color-palettes.md. Each palette is defined by primary, secondary, accent, background, and text colors with accessibility considerations.

## SEO Targeting

This repository targets the following search terms:

- github profile builder
- github profile readme generator
- github profile readme skill
- github wrapped generator
- contribution snake generator
- github stats generator
- profile readme generator

See references/seo-keywords.md for the full keyword map and meta description strategy.

## Safety & Security

- All user-provided text is XML-escaped before insertion into SVG or HTML
- Hex colors are regex-validated (^#[0-9a-fA-F]{6}$)
- No raw HTML injection in generated output
- Tokens are passed via CLI argument or environment variable, never hardcoded
- No external network requests during SVG or HTML rendering

## Limitations

- Unauthenticated requests are limited to 60 req/hr; use --token for higher limits
- GraphQL contributions data requires authentication for detailed breakdowns
- End-to-end testing against the live API requires network access
- Some profile fields (e.g., custom social icons) require manual configuration

## License

MIT License — see LICENSE for details.

## Contributing

See CONTRIBUTING.md for development setup, testing, and PR guidelines.