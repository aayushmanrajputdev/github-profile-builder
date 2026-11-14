# SVG Components Reference

This document describes the SVG component building blocks used in github-profile-builder.

## Core Principles

1. **Self-contained** - All SVGs work without external resources
2. **Inline styles** - No external CSS dependency
3. **XML-safe** - All user content is XML-escaped
4. **Color validated** - Hex colors are regex-validated

## SVG Primitives

### Basic Elements
- `svg_rect()` - Rectangle with optional rounded corners
- `svg_circle()` - Circle element
- `svg_text()` - Text with style attributes
- `svg_line()` - Line element
- `svg_path()` - SVG path element
- `svg_polygon()` - Polygon element

### Container Elements
- `svg_svg()` - Root SVG element
- `svg_group()` - Group element for organization
- `svg_defs()` - Definitions container for gradients

### Gradient Generators
- `svg_linear_gradient()` - Linear gradient definition
- `svg_radial_gradient()` - Radial gradient definition

## Color Palettes

See `references/color-palettes.md` for available palettes.

### Color Names
- `primary` - Main accent color
- `secondary` - Secondary accent
- `accent` - Decorative accent
- `background` - Card/background color
- `text` - Primary text color
- `text_muted` - Secondary/muted text
- `border` - Border/divider color
- `success` - Positive action color (green)
- `warning` - Warning/caution color (amber)
- `danger` - Negative/error color (red)

## Utility Functions

### Text Helpers
- `xml_escape()` - Escape text for safe SVG inclusion
- `format_number()` - Format numbers with K/M suffixes
- `truncate_text()` - Truncate to max length with ellipsis

### Layout Helpers
- `rounded_rect_path()` - Generate rounded rectangle path
- `calculate_text_width()` - Approximate text dimensions

## Component Types

### Stats Cards
- Stats card - Overview with all metrics
- Individual stat cards - Separate cards per metric
- Language stats - Language usage breakdown

### Profile Cards
- Profile card - Avatar, bio, and summary stats
- Contribution snake - Interactive snake visualization
- Certificate - Achievement certificate

### Wrapped Cards
- Wrapped summary - GitHub Wrapped style
- Wrapped card set - Individual category cards

## Adding New Components

1. Create the component function in the appropriate module
2. Add proper SVG escaping for any user content
3. Use the color palette consistently
4. Test with different values including edge cases