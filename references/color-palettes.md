# Color Palettes Reference

This document describes all available color palettes for github-profile-builder.

## Palette Categories

### Nature Inspired
- **forest** - Greens and earth tones for nature lovers
- **ocean** - Blues and teals for water enthusiasts
- **sunset** - Warm oranges and reds

### Dark/Low Light
- **midnight** - Deep blues and purples (default)
- **monochrome** - Grays for a clean minimalist look
- **slate** - Cool grays with blue accents

### Gaming/Tech
- **dracula** - Popular dark theme for developers
- **tokyo-night** - Tokyo Night terminal theme
- **monokai** - Classic code editor theme
- **kanagawa** - Vim theme for developers

### Vibrant
- **violet** - Purple and magenta tones
- **rose** - Warm pinks and reds
- **amber** - Golden yellows

### GitHub Native
- **github** - Official GitHub dark theme colors

### Other
- **emerald** - Rich greens
- **solarized** - Solarized dark theme
- **catppuccin** - Catppuccin theme
- **gruvbox** - Gruvbox theme
- **everforest** - Everforest theme

## Usage

```bash
python scripts/generate.py --username octocat --palette ocean
```

## Adding New Palettes

Modify `scripts/svg_components.py` to add new palettes to the `PALETTES` dictionary.

## Color Philosophy

Each palette is designed to be:
1. Visually distinct from others
2. Accessible (good contrast ratios)
3. Meaningful to the intended audience
4. Compatible with SVG rendering
5. Printable-friendly (colorblind safe)