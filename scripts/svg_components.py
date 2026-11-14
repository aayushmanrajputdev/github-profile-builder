"""Reusable SVG building blocks for original visual assets."""

import re
from typing import Dict, List, Optional, Tuple


# Color validation regex
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def validate_hex_color(color: str) -> str:
    """Validate and normalize a hex color."""
    if not HEX_COLOR_RE.match(color):
        raise ValueError(f"Invalid hex color: {color}")
    return color.lower()


def xml_escape(text: str) -> str:
    """Escape text for safe XML/SVG insertion."""
    return (
        text.replace("&", "&")
        .replace("<", "<")
        .replace(">", ">")
        .replace('"', """)
        .replace("'", "&apos;")
    )


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_number(num: int) -> str:
    """Format number with K/M suffixes."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M".replace(".0", "")
    if num >= 1_000:
        return f"{num / 1_000:.1f}K".replace(".0", "")
    return str(num)


def calculate_text_width(text: str, font_size: int, font_family: str = "system-ui") -> float:
    """Approximate text width for layout calculations."""
    # Rough approximation: average char width ~ 0.6 * font_size
    return len(text) * font_size * 0.6


class ColorPalette:
    """Color palette for SVG generation."""

    def __init__(
        self,
        name: str,
        primary: str,
        secondary: str,
        accent: str,
        background: str,
        text: str,
        text_muted: str,
        border: str,
        success: str = "#22c55e",
        warning: str = "#f59e0b",
        danger: str = "#ef4444",
    ):
        self.name = name
        self.primary = validate_hex_color(primary)
        self.secondary = validate_hex_color(secondary)
        self.accent = validate_hex_color(accent)
        self.background = validate_hex_color(background)
        self.text = validate_hex_color(text)
        self.text_muted = validate_hex_color(text_muted)
        self.border = validate_hex_color(border)
        self.success = validate_hex_color(success)
        self.warning = validate_hex_color(warning)
        self.danger = validate_hex_color(danger)

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "background": self.background,
            "text": self.text,
            "text_muted": self.text_muted,
            "border": self.border,
            "success": self.success,
            "warning": self.warning,
            "danger": self.danger,
        }


# Original color palettes - 20+ unique schemes
PALETTES: Dict[str, ColorPalette] = {
    "midnight": ColorPalette(
        "Midnight",
        primary="#6366f1",
        secondary="#8b5cf6",
        accent="#06b6d4",
        background="#0f172a",
        text="#f8fafc",
        text_muted="#94a3b8",
        border="#1e293b",
    ),
    "ocean": ColorPalette(
        "Ocean",
        primary="#0ea5e9",
        secondary="#06b6d4",
        accent="#22d3ee",
        background="#0c1e35",
        text="#f0f9ff",
        text_muted="#7dd3fc",
        border="#164e63",
    ),
    "forest": ColorPalette(
        "Forest",
        primary="#22c55e",
        secondary="#16a34a",
        accent="#84cc16",
        background="#052e16",
        text="#f0fdf4",
        text_muted="#86efac",
        border="#14532d",
    ),
    "sunset": ColorPalette(
        "Sunset",
        primary="#f97316",
        secondary="#fb923c",
        accent="#fbbf24",
        background="#431407",
        text="#fff7ed",
        text_muted="#fdba74",
        border="#9a3412",
    ),
    "rose": ColorPalette(
        "Rose",
        primary="#e11d48",
        secondary="#f43f5e",
        accent="#fb7185",
        background="#4c0519",
        text="#fff1f2",
        text_muted="#fda4af",
        border="#9f1239",
    ),
    "violet": ColorPalette(
        "Violet",
        primary="#a855f7",
        secondary="#c084fc",
        accent="#d8b4fe",
        background="#2e1065",
        text="#faf5ff",
        text_muted="#c4b5fd",
        border="#5b21b6",
    ),
    "amber": ColorPalette(
        "Amber",
        primary="#f59e0b",
        secondary="#fbbf24",
        accent="#fcd34d",
        background="#451a03",
        text="#fffbeb",
        text_muted="#fde68a",
        border="#92400e",
    ),
    "emerald": ColorPalette(
        "Emerald",
        primary="#10b981",
        secondary="#34d399",
        accent="#6ee7b7",
        background="#022c22",
        text="#ecfdf5",
        text_muted="#6ee7b7",
        border="#065f46",
    ),
    "slate": ColorPalette(
        "Slate",
        primary="#64748b",
        secondary="#94a3b8",
        accent="#cbd5e1",
        background="#0f172a",
        text="#f8fafc",
        text_muted="#94a3b8",
        border="#1e293b",
    ),
    "monochrome": ColorPalette(
        "Monochrome",
        primary="#525252",
        secondary="#737373",
        accent="#a3a3a3",
        background="#171717",
        text="#fafafa",
        text_muted="#a3a3a3",
        border="#262626",
    ),
    "dracula": ColorPalette(
        "Dracula",
        primary="#bd93f9",
        secondary="#ff79c6",
        accent="#8be9fd",
        background="#282a36",
        text="#f8f8f2",
        text_muted="#6272a4",
        border="#44475a",
    ),
    "nord": ColorPalette(
        "Nord",
        primary="#88c0d0",
        secondary="#81a1c1",
        accent="#a3be8c",
        background="#2e3440",
        text="#eceff4",
        text_muted="#d8dee9",
        border="#3b4252",
    ),
    "solarized": ColorPalette(
        "Solarized",
        primary="#268bd2",
        secondary="#859900",
        accent="#b58900",
        background="#002b36",
        text="#fdf6e3",
        text_muted="#93a1a1",
        border="#073642",
    ),
    "github": ColorPalette(
        "GitHub",
        primary="#58a6ff",
        secondary="#a371f7",
        accent="#79c0ff",
        background="#0d1117",
        text="#f0f6fc",
        text_muted="#8b949e",
        border="#30363d",
    ),
    "monokai": ColorPalette(
        "Monokai",
        primary="#a6e22e",
        secondary="#fd971f",
        accent="#f92672",
        background="#272822",
        text="#f8f8f2",
        text_muted="#75715e",
        border="#49483e",
    ),
    "tokyo-night": ColorPalette(
        "Tokyo Night",
        primary="#7aa2f7",
        secondary="#bb9af7",
        accent="#7dcfff",
        background="#1a1b26",
        text="#c0caf5",
        text_muted="#565f89",
        border="#292e42",
    ),
    "catppuccin": ColorPalette(
        "Catppuccin",
        primary="#89b4fa",
        secondary="#cba6f7",
        accent="#f5c2e7",
        background="#1e1e2e",
        text="#cdd6f4",
        text_muted="#6c7086",
        border="#313244",
    ),
    "gruvbox": ColorPalette(
        "Gruvbox",
        primary="#fabd2f",
        secondary="#fb4934",
        accent="#8ec07c",
        background="#282828",
        text="#ebdbb2",
        text_muted="#928374",
        border="#3c3836",
    ),
    "everforest": ColorPalette(
        "Everforest",
        primary="#a7c080",
        secondary="#e69875",
        accent="#d3c6aa",
        background="#2d353b",
        text="#d3c6aa",
        text_muted="#7a8478",
        border="#3d454b",
    ),
    "kanagawa": ColorPalette(
        "Kanagawa",
        primary="#7e9cd8",
        secondary="#957fb8",
        accent="#76946a",
        background="#1f1f28",
        text="#c8c093",
        text_muted="#727169",
        border="#2a2a37",
    ),
}


def get_palette(name: str) -> ColorPalette:
    """Get a color palette by name."""
    if name not in PALETTES:
        raise ValueError(f"Unknown palette: {name}. Available: {list(PALETTES.keys())}")
    return PALETTES[name]


def list_palettes() -> List[str]:
    """List all available palette names."""
    return list(PALETTES.keys())


# SVG primitive builders

def svg_rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    rx: float = 0,
    ry: float = 0,
    stroke: Optional[str] = None,
    stroke_width: float = 0,
    **attrs,
) -> str:
    """Generate a rect element."""
    parts = [
        f'x="{x}"',
        f'y="{y}"',
        f'width="{width}"',
        f'height="{height}"',
        f'fill="{fill}"',
    ]
    if rx:
        parts.append(f'rx="{rx}"')
    if ry:
        parts.append(f'ry="{ry}"')
    if stroke:
        parts.append(f'stroke="{stroke}"')
        parts.append(f'stroke-width="{stroke_width}"')
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<rect {' '.join(parts)} />"


def svg_circle(
    cx: float,
    cy: float,
    r: float,
    fill: str,
    stroke: Optional[str] = None,
    stroke_width: float = 0,
    **attrs,
) -> str:
    """Generate a circle element."""
    parts = [
        f'cx="{cx}"',
        f'cy="{cy}"',
        f'r="{r}"',
        f'fill="{fill}"',
    ]
    if stroke:
        parts.append(f'stroke="{stroke}"')
        parts.append(f'stroke-width="{stroke_width}"')
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<circle {' '.join(parts)} />"


def svg_text(
    x: float,
    y: float,
    text: str,
    fill: str,
    font_size: int = 14,
    font_family: str = "system-ui, -apple-system, sans-serif",
    font_weight: str = "normal",
    text_anchor: str = "start",
    dominant_baseline: str = "alphabetic",
    **attrs,
) -> str:
    """Generate a text element with XML-escaped content."""
    safe_text = xml_escape(text)
    parts = [
        f'x="{x}"',
        f'y="{y}"',
        f'fill="{fill}"',
        f'font-size="{font_size}"',
        f'font-family="{font_family}"',
        f'font-weight="{font_weight}"',
        f'text-anchor="{text_anchor}"',
        f'dominant-baseline="{dominant_baseline}"',
    ]
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<text {' '.join(parts)}>{safe_text}</text>"


def svg_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    stroke_width: float = 1,
    stroke_dasharray: Optional[str] = None,
    **attrs,
) -> str:
    """Generate a line element."""
    parts = [
        f'x1="{x1}"',
        f'y1="{y1}"',
        f'x2="{x2}"',
        f'y2="{y2}"',
        f'stroke="{stroke}"',
        f'stroke-width="{stroke_width}"',
    ]
    if stroke_dasharray:
        parts.append(f'stroke-dasharray="{stroke_dasharray}"')
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<line {' '.join(parts)} />"


def svg_polygon(points: List[Tuple[float, float]], fill: str, **attrs) -> str:
    """Generate a polygon element."""
    points_str = " ".join(f"{x},{y}" for x, y in points)
    parts = [f'points="{points_str}"', f'fill="{fill}"']
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<polygon {' '.join(parts)} />"


def svg_path(d: str, fill: Optional[str] = None, stroke: Optional[str] = None, stroke_width: float = 1, **attrs) -> str:
    """Generate a path element."""
    parts = [f'd="{d}"']
    if fill:
        parts.append(f'fill="{fill}"')
    else:
        parts.append('fill="none"')
    if stroke:
        parts.append(f'stroke="{stroke}"')
        parts.append(f'stroke-width="{stroke_width}"')
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<path {' '.join(parts)} />"


def svg_linear_gradient(
    id_: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stops: List[Tuple[float, str]],
) -> str:
    """Generate a linear gradient definition."""
    stop_elements = "".join(
        f'<stop offset="{offset * 100}%" stop-color="{color}" />' for offset, color in stops
    )
    return f'<linearGradient id="{id_}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">{stop_elements}</linearGradient>'


def svg_radial_gradient(
    id_: str,
    cx: float,
    cy: float,
    r: float,
    stops: List[Tuple[float, str]],
) -> str:
    """Generate a radial gradient definition."""
    stop_elements = "".join(
        f'<stop offset="{offset * 100}%" stop-color="{color}" />' for offset, color in stops
    )
    return f'<radialGradient id="{id_}" cx="{cx}%" cy="{cy}%" r="{r}%">{stop_elements}</radialGradient>'


def svg_defs(children: List[str]) -> str:
    """Generate a defs element."""
    return f"<defs>{''.join(children)}</defs>"


def svg_group(children: List[str], **attrs) -> str:
    """Generate a group element."""
    parts = []
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<g {' '.join(parts)}>{''.join(children)}</g>"


def svg_svg(
    width: int,
    height: int,
    children: List[str],
    viewBox: Optional[str] = None,
    xmlns: str = "http://www.w3.org/2000/svg",
    **attrs,
) -> str:
    """Generate the root SVG element."""
    parts = [
        f'width="{width}"',
        f'height="{height}"',
        f'xmlns="{xmlns}"',
    ]
    if viewBox:
        parts.append(f'viewBox="{viewBox}"')
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<svg {' '.join(parts)}>{''.join(children)}</svg>"


# Higher-level components

def stat_card(
    width: int,
    height: int,
    palette: ColorPalette,
    label: str,
    value: str,
    icon_path: Optional[str] = None,
    trend: Optional[str] = None,
) -> str:
    """Generate a stat card SVG."""
    padding = 16
    icon_size = 24
    label_y = padding + 16
    value_y = label_y + 24

    children = [
        svg_rect(0, 0, width, height, palette.background, rx=8, ry=8, stroke=palette.border, stroke_width=1),
    ]

    if icon_path:
        children.append(
            svg_group(
                [svg_path(icon_path, fill=palette.primary)],
                transform=f"translate({padding}, {padding}) scale(0.8)",
            )
        )
        label_x = padding + icon_size + 8
    else:
        label_x = padding

    children.extend([
        svg_text(label_x, label_y, label, palette.text_muted, font_size=11, font_weight="600"),
        svg_text(label_x, value_y, value, palette.text, font_size=20, font_weight="700"),
    ])

    if trend:
        trend_color = palette.success if trend.startswith("+") else palette.danger
        children.append(
            svg_text(width - padding, value_y, trend, trend_color, font_size=11, font_weight="600", text_anchor="end")
        )

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def progress_bar(
    x: float,
    y: float,
    width: float,
    height: float,
    progress: float,
    palette: ColorPalette,
    background_color: Optional[str] = None,
) -> List[str]:
    """Generate progress bar elements."""
    bg_color = background_color or palette.border
    progress = max(0, min(1, progress))

    return [
        svg_rect(x, y, width, height, bg_color, rx=height / 2, ry=height / 2),
        svg_rect(x, y, width * progress, height, palette.primary, rx=height / 2, ry=height / 2)
        if progress > 0
        else "",
    ]


def contribution_cell(
    x: float,
    y: float,
    size: float,
    level: int,
    palette: ColorPalette,
) -> str:
    """Generate a single contribution calendar cell."""
    # Original color scale - 5 levels
    colors = [
        palette.border,  # 0: no contributions
        "#164e29",       # 1: low
        "#1a7f37",       # 2: medium
        "#239f40",       # 3: high
        "#2ea043",       # 4: highest
    ]
    fill = colors[min(level, 4)]
    return svg_rect(x, y, size, size, fill, rx=1, ry=1)


def rounded_rect_path(x: float, y: float, width: float, height: float, radius: float) -> str:
    """Generate a rounded rectangle path."""
    r = min(radius, width / 2, height / 2)
    return (
        f"M{x + r},{y} "
        f"h{width - 2 * r} "
        f"a{r},{r} 0 0 1 {r},{r} "
        f"v{height - 2 * r} "
        f"a{r},{r} 0 0 1 -{r},{r} "
        f"h-{width - 2 * r} "
        f"a{r},{r} 0 0 1 -{r},-{r} "
        f"v-{height - 2 * r} "
        f"a{r},{r} 0 0 1 {r},-{r} "
        "Z"
    )


def badge(
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    palette: ColorPalette,
    bg_color: Optional[str] = None,
    text_color: Optional[str] = None,
) -> str:
    """Generate a badge element."""
    bg = bg_color or palette.primary
    fg = text_color or palette.background
    r = height / 2
    return svg_group([
        svg_path(rounded_rect_path(x, y, width, height, r), fill=bg),
        svg_text(x + width / 2, y + height / 2 + 3, text, fg, font_size=10, font_weight="600", text_anchor="middle"),
    ], transform=f"translate({x}, {y})")