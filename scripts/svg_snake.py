"""Contribution snake SVG generator - original implementation."""

from scripts.svg_components import (
    ColorPalette,
    PALETTES,
    get_palette,
    svg_svg,
    svg_rect,
    svg_text,
    svg_line,
    svg_group,
    svg_path,
    svg_defs,
    svg_linear_gradient,
    rounded_rect_path,
    xml_escape,
    validate_hex_color,
)
from typing import Dict, List, Optional, Tuple
import math


def generate_contribution_snake(
    contribution_days: List[Dict[str, Any]],
    year: int,
    palette_name: str = "midnight",
    width: int = 800,
    height: int = 200,
    animation_duration: float = 10.0,
) -> str:
    """Generate an original contribution snake SVG.

    The snake follows the contribution calendar path, with segment colors
    based on contribution intensity. No external dependencies, fully self-contained.
    """
    palette = get_palette(palette_name)

    if not contribution_days:
        return _empty_snake_svg(width, height, palette, year)

    # Sort days by date
    sorted_days = sorted(contribution_days, key=lambda d: d["date"])

    # Filter to the target year
    year_str = str(year)
    year_days = [d for d in sorted_days if d["date"].startswith(year_str)]

    if not year_days:
        return _empty_snake_svg(width, height, palette, year)

    # Calculate grid layout (53 weeks x 7 days)
    cell_size = 12
    cell_gap = 2
    grid_start_x = 60
    grid_start_y = 40

    # Map each day to grid position
    day_positions = _calculate_grid_positions(year_days, grid_start_x, grid_start_y, cell_size, cell_gap)

    # Build snake path through active days
    snake_segments = _build_snake_segments(day_positions, cell_size)

    # Generate SVG
    defs = _build_snake_defs(palette, palette_name, animation_duration)

    children = [
        defs,
        # Background
        svg_rect(0, 0, width, height, palette.background, rx=8, ry=8, stroke=palette.border, stroke_width=1),
        # Title
        svg_text(20, 24, f"Contribution Snake {year}", palette.text, font_size=16, font_weight="700"),
        # Grid cells (background)
        *_render_grid_cells(year_days, day_positions, cell_size, palette),
        # Snake body
        *_render_snake_body(snake_segments, cell_size, palette, palette_name, animation_duration),
        # Snake head
        *_render_snake_head(snake_segments, cell_size, palette),
        # Legend
        *_render_legend(width, height, palette),
    ]

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def _calculate_grid_positions(
    days: List[Dict[str, Any]],
    start_x: float,
    start_y: float,
    cell_size: float,
    cell_gap: float,
) -> Dict[str, Tuple[float, float]]:
    """Calculate grid positions for each day."""
    positions = {}
    for day in days:
        date_str = day["date"]
        # Parse year, month, day
        try:
            year, month, day_num = map(int, date_str.split("-"))
        except ValueError:
            continue

        # Calculate week of year (approximate)
        import datetime
        try:
            dt = datetime.date(year, month, day_num)
            week_num = dt.isocalendar()[1] - 1  # 0-indexed
            weekday = dt.weekday()  # Monday=0
        except ValueError:
            continue

        # GitHub weeks start on Sunday, adjust
        weekday = (weekday + 1) % 7  # Sunday=0

        x = start_x + week_num * (cell_size + cell_gap)
        y = start_y + weekday * (cell_size + cell_gap)

        positions[date_str] = (x, y)

    return positions


def _build_snake_segments(
    positions: Dict[str, Tuple[float, float]],
    cell_size: float,
) -> List[Dict[str, Any]]:
    """Build snake segments from day positions."""
    # Sort by date
    sorted_dates = sorted(positions.keys())

    segments = []
    for date_str in sorted_dates:
        x, y = positions[date_str]
        # Center of cell
        cx = x + cell_size / 2
        cy = y + cell_size / 2
        segments.append({
            "date": date_str,
            "x": cx,
            "y": cy,
            "cell_x": x,
            "cell_y": y,
        })

    return segments


def _render_grid_cells(
    days: List[Dict[str, Any]],
    positions: Dict[str, Tuple[float, float]],
    cell_size: float,
    palette: ColorPalette,
) -> List[str]:
    """Render the contribution grid cells as background."""
    elements = []

    # Color scale matching GitHub
    intensity_colors = [
        palette.border,      # 0
        "#0e4429",           # 1
        "#006d32",           # 2
        "#26a641",           # 3
        "#39d353",           # 4
    ]

    day_map = {d["date"]: d for d in days}

    for date_str, (x, y) in positions.items():
        day_data = day_map.get(date_str, {})
        count = day_data.get("count", 0)
        level = min(count, 4) if count > 0 else 0
        fill = intensity_colors[level]

        elements.append(
            svg_rect(x, y, cell_size, cell_size, fill, rx=2, ry=2, stroke=palette.background, stroke_width=0.5)
        )

    return elements


def _build_snake_defs(palette: ColorPalette, palette_name: str, duration: float) -> str:
    """Build SVG defs for snake gradients and animations."""
    defs_children = []

    # Snake body gradient
    defs_children.append(
        svg_linear_gradient(f"snake-body-{palette_name}", 0, 0, 100, 0, [
            (0, palette.primary),
            (0.5, palette.secondary),
            (1, palette.accent),
        ])
    )

    # Snake head gradient
    defs_children.append(
        svg_radial_gradient(f"snake-head-{palette_name}", 50, 50, 50, [
            (0, palette.accent),
            (1, palette.primary),
        ])
    )

    # Glow filter
    defs_children.append(f'''
    <filter id="snake-glow-{palette_name}" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
        <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    ''')

    return svg_defs(defs_children)


def _render_snake_body(
    segments: List[Dict[str, Any]],
    cell_size: float,
    palette: ColorPalette,
    palette_name: str,
    duration: float,
) -> List[str]:
    """Render the snake body as a curved path through segments."""
    if len(segments) < 2:
        return []

    elements = []

    # Build smooth path through segment centers
    path_data = _build_smooth_path(segments)

    # Snake body stroke width
    stroke_width = cell_size * 0.7

    # Main snake path with gradient
    elements.append(
        svg_path(
            path_data,
            stroke=f"url(#snake-body-{palette_name})",
            stroke_width=stroke_width,
            stroke_linecap="round",
            stroke_linejoin="round",
            fill="none",
            filter=f"url(#snake-glow-{palette_name})",
        )
    )

    # Animated dash for "movement" effect
    dash_array = stroke_width * 4
    elements.append(
        svg_path(
            path_data,
            stroke=f"url(#snake-body-{palette_name})",
            stroke_width=stroke_width * 0.3,
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_dasharray=f"{dash_array} {dash_array * 2}",
            fill="none",
            style=f"animation: snake-dash {duration}s linear infinite;",
        )
    )

    # Add CSS animation
    elements.append(f'''
    <style>
        @keyframes snake-dash {{
            to {{ stroke-dashoffset: -{dash_array * 3}; }}
        }}
    </style>
    ''')

    return elements


def _build_smooth_path(segments: List[Dict[str, Any]]) -> str:
    """Build a smooth Catmull-Rom spline through segment centers."""
    if len(segments) < 2:
        return ""

    points = [(s["x"], s["y"]) for s in segments]

    # Catmull-Rom spline
    path_parts = [f"M{points[0][0]},{points[0][1]}"]

    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]

        # Catmull-Rom to Bezier conversion
        cp1x = p1[0] + (p2[0] - p0[0]) / 6
        cp1y = p1[1] + (p2[1] - p0[1]) / 6
        cp2x = p2[0] - (p3[0] - p1[0]) / 6
        cp2y = p2[1] - (p3[1] - p1[1]) / 6

        path_parts.append(f"C{cp1x},{cp1y} {cp2x},{cp2y} {p2[0]},{p2[1]}")

    return " ".join(path_parts)


def _render_snake_head(segments: List[Dict[str, Any]], cell_size: float, palette: ColorPalette) -> List[str]:
    """Render the snake head at the most recent contribution."""
    if not segments:
        return []

    # Head is at the last segment (most recent date)
    head = segments[-1]
    head_radius = cell_size * 0.5

    elements = []

    # Head circle
    elements.append(
        svg_circle(head["x"], head["y"], head_radius, f"url(#snake-head-{palette.name.lower()})")
    )

    # Eyes
    eye_offset = head_radius * 0.3
    eye_radius = head_radius * 0.15
    elements.append(svg_circle(head["x"] - eye_offset, head["y"] - eye_offset, eye_radius, "#fff"))
    elements.append(svg_circle(head["x"] + eye_offset, head["y"] - eye_offset, eye_radius, "#fff"))

    return elements


def _render_legend(width: int, height: int, palette: ColorPalette) -> List[str]:
    """Render the contribution legend."""
    elements = []

    legend_y = height - 30
    legend_x = 20
    box_size = 10
    gap = 4
    labels = ["Less", "More"]

    # Legend background
    elements.append(
        svg_rect(legend_x - 8, legend_y - 12, 140, 24, palette.background, rx=4, ry=4, stroke=palette.border, stroke_width=0.5)
    )

    # Color boxes
    colors = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    for i, color in enumerate(colors):
        x = legend_x + i * (box_size + gap)
        elements.append(svg_rect(x, legend_y, box_size, box_size, color, rx=1, ry=1))

    # Labels
    elements.append(svg_text(legend_x, legend_y + 22, labels[0], palette.text_muted, font_size=8))
    elements.append(svg_text(legend_x + 120, legend_y + 22, labels[1], palette.text_muted, font_size=8, text_anchor="end"))

    return elements


def _empty_snake_svg(width: int, height: int, palette: ColorPalette, year: int) -> str:
    """Generate an empty state snake SVG."""
    children = [
        svg_rect(0, 0, width, height, palette.background, rx=8, ry=8, stroke=palette.border, stroke_width=1),
        svg_text(width / 2, height / 2 - 10, f"No contribution data for {year}", palette.text, font_size=14, text_anchor="middle"),
        svg_text(width / 2, height / 2 + 16, "Make some commits to see your snake!", palette.text_muted, font_size=11, text_anchor="middle"),
    ]
    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def generate_mini_snake(
    contribution_days: List[Dict[str, Any]],
    year: int,
    palette_name: str = "midnight",
    width: int = 400,
    height: int = 100,
) -> str:
    """Generate a compact snake for embedding in README."""
    return generate_contribution_snake(contribution_days, year, palette_name, width, height)


def svg_radial_gradient(id_: str, cx: float, cy: float, r: float, stops: List[Tuple[float, str]]) -> str:
    """Generate a radial gradient definition."""
    stop_elements = "".join(
        f'<stop offset="{offset * 100}%" stop-color="{color}" />' for offset, color in stops
    )
    return f'<radialGradient id="{id_}" cx="{cx}%" cy="{cy}%" r="{r}%">{stop_elements}</radialGradient>'


def svg_circle(cx: float, cy: float, r: float, fill: str, **attrs) -> str:
    """Generate a circle element."""
    parts = [
        f'cx="{cx}"',
        f'cy="{cy}"',
        f'r="{r}"',
        f'fill="{fill}"',
    ]
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return f"<circle {' '.join(parts)} />"