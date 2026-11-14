"""Profile certificate SVG generator - with explicit disclaimer."""

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
    svg_radial_gradient,
    rounded_rect_path,
    xml_escape,
    format_number,
)
from typing import Dict, Any, Optional
import datetime


def generate_certificate(
    username: str,
    user_data: Dict[str, Any],
    stats: Dict[str, Any],
    palette_name: str = "midnight",
    width: int = 800,
    height: int = 600,
) -> str:
    """Generate a profile certificate SVG with explicit disclaimer.

    The certificate includes an explicit disclaimer:
    "This certificate is not an official GitHub certification."
    """
    palette = get_palette(palette_name)

    defs = _build_certificate_defs(palette, palette_name)

    current_year = datetime.datetime.now().year
    name = user_data.get("name") or username
    login = user_data.get("login", username)
    total_contributions = stats.get("total_contributions", 0)
    followers = stats.get("followers", 0)
    repos = stats.get("repos", 0)
    stars = stats.get("stars", 0)
    current_streak = stats.get("current_streak", 0)
    longest_streak = stats.get("longest_streak", 0)
    top_languages = stats.get("top_languages", [])

    children = [
        defs,
        # Border frame
        *_render_certificate_border(width, height, palette),
        # Background pattern
        *_render_background_pattern(width, height, palette),
        # Header
        *_render_certificate_header(width, palette, current_year),
        # Title
        *_render_certificate_title(width, palette),
        # Recipient
        *_render_recipient(width, palette, name, login),
        # Achievement statement
        *_render_achievement_statement(width, palette, total_contributions, current_year),
        # Stats badges
        *_render_achievement_badges(width, palette, total_contributions, followers, repos, stars, current_streak, longest_streak),
        # Top languages
        *_render_certificate_languages(width, palette, top_languages),
        # Signature area
        *_render_signature_area(width, height, palette, current_year),
        # DISCLAIMER - prominently displayed
        *_render_disclaimer(width, height, palette),
    ]

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def _build_certificate_defs(palette: ColorPalette, palette_name: str) -> str:
    """Build SVG definitions for certificate."""
    children = []

    # Main gradient
    children.append(
        svg_linear_gradient(f"cert-bg-{palette_name}", 0, 0, 100, 100, [
            (0, palette.background),
            (0.5, palette.border),
            (1, palette.background),
        ])
    )

    # Gold accent gradient
    children.append(
        svg_linear_gradient(f"gold-{palette_name}", 0, 0, 100, 0, [
            (0, "#fbbf24"),
            (0.5, "#f59e0b"),
            (1, "#d97706"),
        ])
    )

    # Seal gradient
    children.append(
        svg_radial_gradient(f"seal-{palette_name}", 50, 50, 50, [
            (0, "#fbbf24"),
            (1, "#92400e"),
        ])
    )

    # Watermark pattern
    children.append(f'''
    <pattern id="watermark-{palette.name.lower()}" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
        <text x="30" y="30" font-size="8" fill="{palette.border}" text-anchor="middle" opacity="0.1">GITHUB</text>
    </pattern>
    ''')

    return svg_defs(children)


def _render_certificate_border(width: int, height: int, palette: ColorPalette) -> list:
    """Render the decorative border frame."""
    elements = []

    # Outer border
    elements.append(
        svg_rect(10, 10, width - 20, height - 20, "none", rx=8, ry=8, stroke=palette.primary, stroke_width=3)
    )

    # Inner border
    elements.append(
        svg_rect(20, 20, width - 40, height - 40, "none", rx=6, ry=6, stroke=palette.accent, stroke_width=1, stroke_dasharray="10 5")
    )

    # Corner decorations
    corner_size = 30
    corners = [
        (25, 25), (width - 55, 25),
        (25, height - 55), (width - 55, height - 55),
    ]
    for cx, cy in corners:
        elements.append(
            svg_path(
                f"M{cx},{cy + corner_size} L{cx},{cy} L{cx + corner_size},{cy}",
                stroke=palette.primary,
                stroke_width=2,
                fill="none",
            )
        )

    return elements


def _render_background_pattern(width: int, height: int, palette: ColorPalette) -> list:
    """Render subtle background pattern."""
    elements = []

    # Watermark pattern
    elements.append(
        svg_rect(0, 0, width, height, f"url(#watermark-{palette.name.lower()})")
    )

    # Subtle diagonal lines
    for i in range(0, width + height, 80):
        elements.append(
            svg_line(i, 0, 0, i, palette.border, stroke_width=0.3, opacity="0.1")
        )

    return elements


def _render_certificate_header(width: int, palette: ColorPalette, year: int) -> list:
    """Render certificate header with year."""
    elements = []

    # Decorative line
    elements.append(
        svg_line(80, 60, width - 80, 60, palette.primary, stroke_width=2)
    )

    # Year badge
    elements.append(
        svg_group([
            svg_path(rounded_rect_path(width / 2 - 50, 40, 100, 30, 15), fill=f"url(#gold-{palette.name.lower()})"),
            svg_text(width / 2, 58, str(year), palette.background, font_size=16, font_weight="800", text_anchor="middle"),
        ])
    )

    return elements


def _render_certificate_title(width: int, palette: ColorPalette) -> list:
    """Render the main certificate title."""
    elements = []

    elements.append(
        svg_text(width / 2, 130, "CERTIFICATE OF ACHIEVEMENT", palette.text, font_size=28, font_weight="800", text_anchor="middle", letter_spacing="2px")
    )

    # Divider
    elements.append(
        svg_line(width / 2 - 100, 145, width / 2 + 100, 145, palette.accent, stroke_width=2)
    )

    return elements


def _render_recipient(width: int, palette: ColorPalette, name: str, login: str) -> list:
    """Render recipient information."""
    elements = []

    elements.append(
        svg_text(width / 2, 190, "This certifies that", palette.text_muted, font_size=16, font_weight="400", text_anchor="middle")
    )

    elements.append(
        svg_text(width / 2, 230, xml_escape(name), palette.text, font_size=32, font_weight="700", text_anchor="middle")
    )

    elements.append(
        svg_text(width / 2, 265, f"(@{xml_escape(login)})", palette.text_muted, font_size=18, font_weight="500", text_anchor="middle")
    )

    elements.append(
        svg_text(width / 2, 300, "has demonstrated exceptional dedication to open source development", palette.text_muted, font_size=14, font_weight="400", text_anchor="middle")
    )

    return elements


def _render_achievement_statement(width: int, palette: ColorPalette, total_contributions: int, year: int) -> list:
    """Render the main achievement statement."""
    elements = []

    statement = f"with {format_number(total_contributions)} contributions in {year}"

    elements.append(
        svg_text(width / 2, 340, statement, palette.primary, font_size=20, font_weight="600", text_anchor="middle")
    )

    # Decorative flourish
    elements.append(
        svg_group([
            svg_path("M-30,0 Q0,-10 30,0", stroke=palette.accent, stroke_width=2, fill="none"),
            svg_circle(-35, 0, 4, palette.accent),
            svg_circle(35, 0, 4, palette.accent),
        ], transform=f"translate({width / 2}, {360})")
    )

    return elements


def _render_achievement_badges(
    width: int,
    palette: ColorPalette,
    total_contributions: int,
    followers: int,
    repos: int,
    stars: int,
    current_streak: int,
    longest_streak: int,
) -> list:
    """Render achievement badges."""
    elements = []

    badges = [
        ("Contributions", format_number(total_contributions), palette.primary),
        ("Followers", format_number(followers), palette.secondary),
        ("Repositories", format_number(repos), palette.accent),
        ("Stars Earned", format_number(stars), palette.warning),
        ("Current Streak", f"{current_streak} days", palette.success),
        ("Longest Streak", f"{longest_streak} days", palette.danger),
    ]

    badge_width = 160
    badge_height = 70
    start_x = (width - (3 * badge_width + 2 * 20)) / 2
    start_y = 380

    for i, (label, value, color) in enumerate(badges):
        col = i % 3
        row = i // 3
        x = start_x + col * (badge_width + 20)
        y = start_y + row * (badge_height + 15)

        # Badge background
        elements.append(
            svg_rect(x, y, badge_width, badge_height, palette.background, rx=10, ry=10, stroke=color, stroke_width=2)
        )

        # Color accent bar
        elements.append(
            svg_rect(x, y, badge_width, 4, color, rx=10, ry=0)
        )

        # Value
        elements.append(
            svg_text(x + badge_width / 2, y + 30, value, palette.text, font_size=20, font_weight="800", text_anchor="middle")
        )

        # Label
        elements.append(
            svg_text(x + badge_width / 2, y + 55, label, palette.text_muted, font_size=10, font_weight="500", text_anchor="middle")
        )

    return elements


def _render_certificate_languages(width: int, palette: ColorPalette, languages: list) -> list:
    """Render top languages section."""
    if not languages:
        return []

    elements = []

    elements.append(
        svg_text(width / 2, 500, "Top Languages", palette.text_muted, font_size=14, font_weight="500", text_anchor="middle")
    )

    lang_elements = []
    for i, lang in enumerate(languages[:5]):
        name = lang.get("name", "")
        percentage = lang.get("percentage", 0)
        lang_elements.append(f"{name} {percentage}%")

    lang_text = "  •  ".join(lang_elements)
    elements.append(
        svg_text(width / 2, 525, xml_escape(lang_text), palette.text, font_size=12, font_weight="500", text_anchor="middle")
    )

    return elements


def _render_signature_area(width: int, height: int, palette: ColorPalette, year: int) -> list:
    """Render signature and date area."""
    elements = []

    sig_y = height - 140

    # Signature line
    elements.append(
        svg_line(width * 0.15, sig_y, width * 0.45, sig_y, palette.text_muted, stroke_width=1)
    )
    elements.append(
        svg_text(width * 0.3, sig_y + 20, "github-profile-builder", palette.text_muted, font_size=11, font_weight="500", text_anchor="middle")
    )
    elements.append(
        svg_text(width * 0.3, sig_y + 35, "Automated Certificate Generator", palette.text_muted, font_size=9, font_weight="400", text_anchor="middle")
    )

    # Date line
    elements.append(
        svg_line(width * 0.55, sig_y, width * 0.85, sig_y, palette.text_muted, stroke_width=1)
    )
    elements.append(
        svg_text(width * 0.7, sig_y + 20, f"Generated: {year}", palette.text_muted, font_size=11, font_weight="500", text_anchor="middle")
    )
    elements.append(
        svg_text(width * 0.7, sig_y + 35, "Based on GitHub API Data", palette.text_muted, font_size=9, font_weight="400", text_anchor="middle")
    )

    return elements


def _render_disclaimer(width: int, height: int, palette: ColorPalette) -> list:
    """Render the EXPLICIT DISCLAIMER - prominently displayed."""
    elements = []

    disclaimer_y = height - 50

    # High-visibility background
    elements.append(
        svg_rect(20, disclaimer_y - 20, width - 40, 40, palette.danger, rx=6, ry=6)
    )

    # Disclaimer text - bold and clear
    elements.append(
        svg_text(
            width / 2,
            disclaimer_y + 5,
            "❗  This certificate is not an official GitHub certification.  ❗",
            palette.background,
            font_size=12,
            font_weight="800",
            text_anchor="middle"
        )
    )

    return elements


def generate_compact_certificate(
    username: str,
    user_data: Dict[str, Any],
    stats: Dict[str, Any],
    palette_name: str = "midnight",
    width: int = 400,
    height: int = 500,
) -> str:
    """Generate a compact certificate for embedding."""
    return generate_certificate(username, user_data, stats, palette_name, width, height)
