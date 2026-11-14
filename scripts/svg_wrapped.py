"""GitHub Wrapped summary cards - original implementation."""

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
    format_number,
    validate_hex_color,
)
from typing import Dict, List, Any, Optional
import datetime


def generate_wrapped_summary(
    username: str,
    year: int,
    stats: Dict[str, Any],
    palette_name: str = "midnight",
    width: int = 800,
    height: int = 1000,
) -> str:
    """Generate a GitHub Wrapped style summary card.

    All metrics come from real API data for the calendar year.
    """
    palette = get_palette(palette_name)

    defs = _build_wrapped_defs(palette, palette_name)

    children = [
        defs,
        # Background
        svg_rect(0, 0, width, height, palette.background, rx=16, ry=16, stroke=palette.border, stroke_width=2),
        # Header
        *_render_wrapped_header(width, palette, username, year),
        # Stats sections
        *_render_contribution_stats(20, 160, width - 40, stats, palette, palette_name),
        *_render_streak_stats(20, 320, width - 40, stats, palette, palette_name),
        *_render_language_stats(20, 480, width - 40, stats, palette, palette_name),
        *_render_social_stats(20, 640, width - 40, stats, palette, palette_name),
        *_render_repo_highlights(20, 800, width - 40, stats, palette, palette_name),
        # Footer
        *_render_wrapped_footer(width, height, palette, year),
    ]

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def _build_wrapped_defs(palette: ColorPalette, palette_name: str) -> str:
    """Build SVG definitions for wrapped cards."""
    children = []

    # Section background gradients
    for i in range(5):
        children.append(
            svg_linear_gradient(f"section-{i}-{palette_name}", 0, 0, 100, 100, [
                (0, palette.background),
                (1, palette.border),
            ])
        )

    # Accent gradients
    children.append(
        svg_linear_gradient(f"accent-{palette_name}", 0, 0, 100, 0, [
            (0, palette.primary),
            (1, palette.secondary),
        ])
    )

    return svg_defs(children)


def _render_wrapped_header(width: int, palette: ColorPalette, username: str, year: int) -> List[str]:
    """Render the wrapped header section."""
    elements = []

    # Decorative top bar
    elements.append(
        svg_rect(0, 0, width, 8, palette.primary)
    )

    # Title
    elements.append(
        svg_text(width / 2, 70, f"GitHub Wrapped {year}", palette.text, font_size=28, font_weight="800", text_anchor="middle")
    )

    # Username
    elements.append(
        svg_text(width / 2, 100, f"@{xml_escape(username)}", palette.text_muted, font_size=16, font_weight="500", text_anchor="middle")
    )

    # Divider
    elements.append(
        svg_line(width * 0.2, 115, width * 0.8, 115, palette.accent, stroke_width=3)
    )

    return elements


def _render_contribution_stats(x: float, y: float, width: float, stats: Dict, palette: ColorPalette, palette_name: str) -> List[str]:
    """Render contribution statistics section."""
    elements = []

    # Section background
    elements.append(
        svg_rect(x, y, width, 140, f"url(#section-0-{palette_name})", rx=12, ry=12, stroke=palette.border, stroke_width=1)
    )

    # Section title
    elements.append(
        svg_text(x + 20, y + 30, "Contributions", palette.text, font_size=18, font_weight="700")
    )

    # Stats grid
    contrib_data = [
        ("Total Contributions", stats.get("total_contributions", 0)),
        ("Commits", stats.get("commits", 0)),
        ("Pull Requests", stats.get("pull_requests", 0)),
        ("Issues", stats.get("issues", 0)),
        ("Reviews", stats.get("reviews", 0)),
        ("Repositories", stats.get("repos_contributed_to", 0)),
    ]

    col_width = (width - 40) / 3
    row_height = 35
    start_x = x + 20
    start_y = y + 45

    for i, (label, value) in enumerate(contrib_data):
        col = i % 3
        row = i // 3
        item_x = start_x + col * col_width
        item_y = start_y + row * row_height

        elements.append(
            svg_text(item_x, item_y, format_number(value), palette.text, font_size=20, font_weight="700")
        )
        elements.append(
            svg_text(item_x, item_y + 20, label, palette.text_muted, font_size=9, font_weight="500")
        )

    return elements


def _render_streak_stats(x: float, y: float, width: float, stats: Dict, palette: ColorPalette, palette_name: str) -> List[str]:
    """Render streak statistics section."""
    elements = []

    elements.append(
        svg_rect(x, y, width, 140, f"url(#section-1-{palette_name})", rx=12, ry=12, stroke=palette.border, stroke_width=1)
    )

    elements.append(
        svg_text(x + 20, y + 30, "Streaks", palette.text, font_size=18, font_weight="700")
    )

    streak_data = [
        ("Current Streak", stats.get("current_streak", 0), "days"),
        ("Longest Streak", stats.get("longest_streak", 0), "days"),
        ("Longest Streak Date", stats.get("longest_streak_date", "N/A"), ""),
    ]

    col_width = (width - 40) / 3
    start_x = x + 20
    start_y = y + 50

    for i, (label, value, unit) in enumerate(streak_data):
        item_x = start_x + i * col_width

        display_value = f"{value} {unit}".strip() if unit else str(value)
        elements.append(
            svg_text(item_x + col_width / 2, start_y, display_value, palette.text, font_size=24, font_weight="800", text_anchor="middle")
        )
        elements.append(
            svg_text(item_x + col_width / 2, start_y + 30, label, palette.text_muted, font_size=11, font_weight="500", text_anchor="middle")
        )

    # Streak visualization - mini calendar
    _render_streak_mini_calendar(elements, x + 20, start_y + 50, width - 40, 60, stats, palette)

    return elements


def _render_streak_mini_calendar(
    elements: List[str],
    x: float,
    y: float,
    width: float,
    height: float,
    stats: Dict,
    palette: ColorPalette,
):
    """Render a mini calendar showing streak periods."""
    # Simplified: show current streak as a bar
    current = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    max_streak = max(current, longest, 1)

    bar_width = width - 20
    bar_height = 16
    bar_y = y + 20

    # Background
    elements.append(
        svg_rect(x + 10, bar_y, bar_width, bar_height, palette.border, rx=8, ry=8)
    )

    # Current streak
    current_width = (current / max_streak) * bar_width
    if current_width > 0:
        elements.append(
            svg_rect(x + 10, bar_y, current_width, bar_height, palette.primary, rx=8, ry=8)
        )

    # Longest streak marker
    longest_x = x + 10 + (longest / max_streak) * bar_width
    elements.append(
        svg_line(longest_x, bar_y - 4, longest_x, bar_y + bar_height + 4, palette.accent, stroke_width=2)
    )

    # Labels
    elements.append(
        svg_text(x + 10, bar_y + bar_height + 16, f"Current: {current} days", palette.text, font_size=9, font_weight="500")
    )
    elements.append(
        svg_text(x + bar_width + 10, bar_y + bar_height + 16, f"Longest: {longest} days", palette.text_muted, font_size=9, font_weight="500", text_anchor="end")
    )


def _render_language_stats(x: float, y: float, width: float, stats: Dict, palette: ColorPalette, palette_name: str) -> List[str]:
    """Render top languages section."""
    elements = []

    elements.append(
        svg_rect(x, y, width, 140, f"url(#section-2-{palette_name})", rx=12, ry=12, stroke=palette.border, stroke_width=1)
    )

    elements.append(
        svg_text(x + 20, y + 30, "Top Languages", palette.text, font_size=18, font_weight="700")
    )

    languages = stats.get("top_languages", [])
    if not languages:
        elements.append(
            svg_text(x + width / 2, y + 80, "No language data available", palette.text_muted, font_size=12, text_anchor="middle")
        )
        return elements

    # Language bars
    bar_width = width - 60
    bar_height = 12
    start_y = y + 50
    gap = 18

    for i, lang in enumerate(languages[:5]):
        lang_y = start_y + i * gap
        name = lang.get("name", "Unknown")
        percentage = lang.get("percentage", 0)
        color = lang.get("color", palette.primary)

        # Name
        elements.append(
            svg_text(x + 20, lang_y + 9, name, palette.text, font_size=11, font_weight="500")
        )

        # Percentage
        elements.append(
            svg_text(x + width - 20, lang_y + 9, f"{percentage}%", palette.text_muted, font_size=11, font_weight="500", text_anchor="end")
        )

        # Bar background
        elements.append(
            svg_rect(x + 120, lang_y + 3, bar_width - 120, bar_height, palette.border, rx=6, ry=6)
        )

        # Bar fill
        if percentage > 0:
            elements.append(
                svg_rect(x + 120, lang_y + 3, (bar_width - 120) * (percentage / 100), bar_height, color, rx=6, ry=6)
            )

    return elements


def _render_social_stats(x: float, y: float, width: float, stats: Dict, palette: ColorPalette, palette_name: str) -> List[str]:
    """Render social stats section."""
    elements = []

    elements.append(
        svg_rect(x, y, width, 140, f"url(#section-3-{palette_name})", rx=12, ry=12, stroke=palette.border, stroke_width=1)
    )

    elements.append(
        svg_text(x + 20, y + 30, "Social", palette.text, font_size=18, font_weight="700")
    )

    social_data = [
        ("Followers", stats.get("followers", 0)),
        ("Following", stats.get("following", 0)),
        ("Stars Received", stats.get("stars_received", 0)),
        ("Stars Given", stats.get("stars_given", 0)),
        ("Repos Created", stats.get("repos_created", 0)),
        ("PRs Merged", stats.get("prs_merged", 0)),
    ]

    col_width = (width - 40) / 3
    row_height = 40
    start_x = x + 20
    start_y = y + 45

    for i, (label, value) in enumerate(social_data):
        col = i % 3
        row = i // 3
        item_x = start_x + col * col_width
        item_y = start_y + row * row_height

        # Color indicator
        color = [palette.primary, palette.secondary, palette.accent, palette.warning, palette.success, palette.danger][i % 6]
        elements.append(
            svg_rect(item_x, item_y, 8, 8, color, rx=2, ry=2)
        )

        elements.append(
            svg_text(item_x + 14, item_y + 12, format_number(value), palette.text, font_size=18, font_weight="700")
        )
        elements.append(
            svg_text(item_x + 14, item_y + 28, label, palette.text_muted, font_size=9, font_weight="500")
        )

    return elements


def _render_repo_highlights(x: float, y: float, width: float, stats: Dict, palette: ColorPalette, palette_name: str) -> List[str]:
    """Render repository highlights section."""
    elements = []

    elements.append(
        svg_rect(x, y, width, 180, f"url(#section-4-{palette_name})", rx=12, ry=12, stroke=palette.border, stroke_width=1)
    )

    elements.append(
        svg_text(x + 20, y + 30, "Repository Highlights", palette.text, font_size=18, font_weight="700")
    )

    top_repos = stats.get("top_repos", [])
    if not top_repos:
        elements.append(
            svg_text(x + width / 2, y + 100, "No repository data available", palette.text_muted, font_size=12, text_anchor="middle")
        )
        return elements

    card_width = (width - 60) / 2
    card_height = 100
    start_x = x + 20
    start_y = y + 45

    for i, repo in enumerate(top_repos[:4]):
        col = i % 2
        row = i // 2
        card_x = start_x + col * (card_width + 20)
        card_y = start_y + row * (card_height + 10)

        _render_repo_card(elements, card_x, card_y, card_width, card_height, repo, palette, palette_name)

    return elements


def _render_repo_card(
    elements: List[str],
    x: float,
    y: float,
    width: float,
    height: float,
    repo: Dict,
    palette: ColorPalette,
    palette_name: str,
):
    """Render a single repository highlight card."""
    name = repo.get("name", "Unknown")
    stars = repo.get("stars", 0)
    language = repo.get("language", "")
    description = repo.get("description", "")

    # Card background
    elements.append(
        svg_rect(x, y, width, height, palette.background, rx=8, ry=8, stroke=palette.border, stroke_width=1)
    )

    # Repo name
    elements.append(
        svg_text(x + 12, y + 20, xml_escape(name), palette.text, font_size=13, font_weight="700")
    )

    # Description
    if description:
        desc_truncated = description[:80] + ("..." if len(description) > 80 else "")
        elements.append(
            svg_text(x + 12, y + 40, xml_escape(desc_truncated), palette.text_muted, font_size=9, font_weight="400")
        )

    # Language color dot
    if language:
        lang_color = repo.get("language_color", palette.primary)
        elements.append(
            svg_circle(x + 12, y + 70, 5, lang_color)
        )
        elements.append(
            svg_text(x + 22, y + 73, xml_escape(language), palette.text_muted, font_size=9, font_weight="500")
        )

    # Stars
    elements.append(
        svg_text(x + width - 12, y + 20, f"★ {format_number(stars)}", palette.warning, font_size=12, font_weight="600", text_anchor="end")
    )


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


def _render_wrapped_footer(width: int, height: int, palette: ColorPalette, year: int) -> List[str]:
    """Render the wrapped footer."""
    elements = []

    footer_y = height - 60

    # Divider
    elements.append(
        svg_line(40, footer_y - 20, width - 40, footer_y - 20, palette.border, stroke_width=1)
    )

    # Disclaimer
    elements.append(
        svg_text(width / 2, footer_y, "Generated from real GitHub API data", palette.text_muted, font_size=10, font_weight="500", text_anchor="middle")
    )
    elements.append(
        svg_text(width / 2, footer_y + 20, f"github-profile-builder • © {year}", palette.text_muted, font_size=9, font_weight="400", text_anchor="middle")
    )

    return elements


def generate_wrapped_card_set(
    username: str,
    year: int,
    stats: Dict[str, Any],
    palette_name: str = "midnight",
    card_width: int = 400,
    card_height: int = 300,
) -> Dict[str, str]:
    """Generate individual wrapped cards for each metric category."""
    palette = get_palette(palette_name)
    cards = {}

    # Card 1: Contributions
    cards["contributions"] = _generate_single_wrapped_card(
        "Contributions", [
            ("Total", stats.get("total_contributions", 0)),
            ("Commits", stats.get("commits", 0)),
            ("PRs", stats.get("pull_requests", 0)),
            ("Issues", stats.get("issues", 0)),
        ], palette, palette_name, card_width, card_height
    )

    # Card 2: Streaks
    cards["streaks"] = _generate_single_wrapped_card(
        "Streaks", [
            ("Current", stats.get("current_streak", 0)),
            ("Longest", stats.get("longest_streak", 0)),
        ], palette, palette_name, card_width, card_height
    )

    # Card 3: Languages
    languages = stats.get("top_languages", [])
    lang_items = [(lang["name"], lang.get("percentage", 0)) for lang in languages[:5]]
    cards["languages"] = _generate_single_wrapped_card(
        "Languages", lang_items, palette, palette_name, card_width, card_height
    )

    # Card 4: Social
    cards["social"] = _generate_single_wrapped_card(
        "Social", [
            ("Followers", stats.get("followers", 0)),
            ("Stars", stats.get("stars_received", 0)),
            ("Repos", stats.get("repos_created", 0)),
        ], palette, palette_name, card_width, card_height
    )

    return cards


def _generate_single_wrapped_card(
    title: str,
    items: List[tuple],
    palette: ColorPalette,
    palette_name: str,
    width: int,
    height: int,
) -> str:
    """Generate a single wrapped metric card."""
    gradient_id = f"wrapped-card-{palette_name}"
    defs = svg_defs([
        svg_linear_gradient(gradient_id, 0, 0, 100, 100, [
            (0, palette.background),
            (1, palette.border),
        ]),
    ])

    children = [
        defs,
        svg_rect(0, 0, width, height, f"url(#{gradient_id})", rx=12, ry=12, stroke=palette.border, stroke_width=1),
        svg_text(20, 30, title, palette.text, font_size=16, font_weight="700"),
        svg_line(20, 40, width - 20, 40, palette.accent, stroke_width=2),
    ]

    start_y = 60
    for i, (label, value) in enumerate(items):
        y = start_y + i * 40
        children.append(
            svg_text(20, y, format_number(value) if isinstance(value, int) else str(value), palette.text, font_size=24, font_weight="800")
        )
        children.append(
            svg_text(20, y + 24, label, palette.text_muted, font_size=10, font_weight="500")
        )

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")