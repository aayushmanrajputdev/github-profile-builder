# github-profile-builder

Generate original GitHub profile READMEs, stats cards, contribution snakes, wrapped summaries, and certificates from real GitHub API data. Zero third-party dependencies for core output.

## When to Use This Skill

Use this skill when someone wants to:

- Build or refresh a GitHub profile README
- Generate original SVG stats cards (followers, repos, stars, contributions)
- Create a contribution snake animation for the current year
- Produce a "GitHub Wrapped" style summary from real API data
- Generate a profile certificate with an explicit disclaimer
- Get shareable snippets for other platforms (LinkedIn, Twitter/X, dev.to)

## Quick Start

```bash
python scripts/generate.py --username aayushmanrajputdev
python scripts/generate.py --username aayushmanrajputdev --token ghp_xxxx
python scripts/generate.py --username aayushmanrajputdev --format all --output ./out
```

## Workflow

### 1. Collect Data

Fetch real data from the GitHub REST and GraphQL APIs. Use unauthenticated requests (60 req/hr) by default; pass --token for authenticated requests (5,000 req/hr). Never hardcode tokens.

### 2. Choose Archetype

Select a profile archetype from references/archetypes.md. Each archetype defines a layout, tone, and recommended color palette.

### 3. Generate Artifacts

Produce one or more of: README.md, stats SVG cards, contribution snake SVG, wrapped summary cards, certificate SVG, HTML preview.

### 4. Validate

- All user-provided text is XML-escaped before insertion into SVG/HTML
- Hex colors are regex-validated (^#[0-9a-fA-F]{6}$)
- Output files are written to the target directory
- No external network requests are made during SVG/HTML rendering

## Principles

- **Real data only.** Wrapped metrics come from live API responses for the calendar year. No fabricated numbers.
- **Original visuals.** All SVG is self-contained and generated from scratch. No copied icons, templates, or code from other tools.
- **Zero dependencies.** The core output path uses only the Python standard library.
- **Safe output.** XML-escape all text. Validate all colors. Never inject raw HTML.
- **Explicit disclaimers.** The certificate states it is not an official GitHub certification.

## Output Formats

| Format | Flag | Description |
|--------|------|-------------|
| README | --format readme | Profile README with embedded SVGs |
| Stats | --format stats | Individual SVG stat cards |
| Snake | --format snake | Contribution snake SVG |
| Wrapped | --format wrapped | Wrapped summary cards |
| Certificate | --format certificate | Profile certificate SVG |
| Preview | --format preview | HTML preview page |
| All | --format all | Every format above |

## Configuration

See references/github-api.md for endpoints, rate limits, and authentication details.
See references/color-palettes.md for original color schemes.
See references/seo-keywords.md for SEO targeting.

## Testing

Tests are mock-based and live in tests/test_generate.py. They verify data parsing, SVG structure, XML escaping, color validation, and CLI argument handling. End-to-end testing against the live GitHub API requires network access and is documented in CONTRIBUTING.md.