"""Original SVG stats card generator."""

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
)
from typing import Dict, List, Optional


# Original SVG icons as path data
ICONS = {
    "user": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
    "repo": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z",
    "star": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
    "fork": "M6 2a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8.83a2 2 0 0 0-.59-1.41L15.17 2H6zm0 2h9.17l4 4H6V4zm0 16V8h12v10H6z",
    "follower": "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm12-9a4 4 0 1 1-8 0 4 4 0 0 1 8 0z",
    "following": "M18 19a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-3a6 6 0 0 1 12 0v3z",
    "commit": "M7 22L4 19l6-6 6 6-3 3zm13 0l3-3 6 6-6 6-3-3zm-26-6v-3a6 6 0 0 1 12 0v3M9 5a2 2 0 1 1 0-4 2 2 0 0 1 0 4z",
    "issue": "M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z",
    "pr": "M6 4a3 3 0 0 1 3-3h4a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3h-4a3 3 0 0 1-3-3V4zm3 2a1 1 0 0 0-1 1v6a1 1 0 0 0 2 0V7a1 1 0 0 0-1-1zM6 10h8",
    "review": "M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z",
    "contrib": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm0-4h-2V7h2v8z",
}


def render_icon(name: str, size: int = 16) -> str:
    """Render an icon as an SVG group."""
    if name not in ICONS:
        return ""
    return f'<g transform="scale({size / 24})"><path d="{ICONS[name]}" fill="currentColor"/></g>'


def generate_stats_card(
    username: str,
    stats: Dict[str, int],
    palette_name: str = "midnight",
    width: int = 495,
    height: int = 195,
) -> str:
    """Generate a comprehensive stats card SVG."""
    palette = get_palette(palette_name)

    # Card background with subtle gradient
    gradient_id = f"bg-{palette_name}"
    defs = svg_defs([
        svg_linear_gradient(gradient_id, 0, 0, 0, 100, [
            (0, palette.background),
            (1, palette.border),
        ]),
    ])

    children = [
        defs,
        svg_rect(0, 0, width, height, f"url(#{gradient_id})", rx=12, ry=12, stroke=palette.border, stroke_width=1),
    ]

    # Header
    header_y = 28
    children.append(svg_text(24, header_y, xml_escape(username), palette.text, font_size=18, font_weight="700"))
    children.append(svg_text(width - 24, header_y, "Stats", palette.text_muted, font_size=12, font_weight="500", text_anchor="end"))

    # Divider
    children.append(svg_line(24, header_y + 8, width - 24, header_y + 8, palette.border, stroke_width=1))

    # Stats grid - 3 columns, 2 rows
    stat_items = [
        ("Repositories", stats.get("repos", 0), "repo"),
        ("Stars", stats.get("stars", 0), "star"),
        ("Followers", stats.get("followers", 0), "follower"),
        ("Following", stats.get("following", 0), "following"),
        ("Contributions", stats.get("contributions", 0), "contrib"),
        ("Total Commits", stats.get("commits", 0), "commit"),
    ]

    col_width = (width - 48) / 3
    row_height = 50
    start_y = header_y + 24

    for i, (label, value, icon_name) in enumerate(stat_items):
        col = i % 3
        row = i // 3
        x = 24 + col * col_width
        y = start_y + row * row_height

        # Icon
        icon_color = palette.primary if col == 0 else (palette.secondary if col == 1 else palette.accent)
        children.append(
            svg_group(
                [svg_path(ICONS.get(icon_name, ""), fill=icon_color)],
                transform=f"translate({x}, {y - 4}) scale(0.7)",
            )
        )

        # Value
        children.append(
            svg_text(x + 20, y + 12, format_number(value), palette.text, font_size=20, font_weight="700")
        )

        # Label
        children.append(
            svg_text(x + 20, y + 34, label, palette.text_muted, font_size=10, font_weight="500")
        )

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def generate_individual_stat_cards(
    username: str,
    stats: Dict[str, int],
    palette_name: str = "midnight",
    card_width: int = 240,
    card_height: int = 100,
) -> Dict[str, str]:
    """Generate individual stat cards for each metric."""
    palette = get_palette(palette_name)
    cards = {}

    stat_configs = [
        ("repos", "Repositories", "repo", palette.primary),
        ("stars", "Stars Earned", "star", palette.secondary),
        ("followers", "Followers", "follower", palette.accent),
        ("following", "Following", "following", palette.warning),
        ("contributions", "Total Contributions", "contrib", palette.success),
        ("commits", "Total Commits", "commit", palette.danger),
    ]

    for key, label, icon, color in stat_configs:
        value = stats.get(key, 0)

        # Card background gradient
        gradient_id = f"card-{key}-{palette_name}"
        defs = svg_defs([
            svg_linear_gradient(gradient_id, 0, 0, 100, 100, [
                (0, palette.background),
                (0.5, palette.border),
                (1, palette.background),
            ]),
        ])

        children = [
            defs,
            svg_rect(0, 0, card_width, card_height, f"url(#{gradient_id})", rx=8, ry=8, stroke=palette.border, stroke_width=1),
        ]

        # Icon
        children.append(
            svg_group(
                [svg_path(ICONS[icon], fill=color)],
                transform=f"translate(16, 18) scale(0.9)",
            )
        )

        # Value
        children.append(
            svg_text(52, 32, format_number(value), palette.text, font_size=24, font_weight="800")
        )

        # Label
        children.append(
            svg_text(52, 58, label, palette.text_muted, font_size=11, font_weight="500")
        )

        # Decorative accent line
        children.append(
            svg_line(16, card_height - 16, 16 + 40, card_height - 16, color, stroke_width=3)
        )

        cards[key] = svg_svg(card_width, card_height, children, viewBox=f"0 0 {card_width} {card_height}")

    return cards


def generate_language_stats_card(
    languages: List[Dict[str, Any]],
    palette_name: str = "midnight",
    width: int = 495,
    height: int = 195,
) -> str:
    """Generate a language breakdown card."""
    palette = get_palette(palette_name)

    gradient_id = f"lang-bg-{palette_name}"
    defs = svg_defs([
        svg_linear_gradient(gradient_id, 0, 0, 0, 100, [
            (0, palette.background),
            (1, palette.border),
        ]),
    ])

    children = [
        defs,
        svg_rect(0, 0, width, height, f"url(#{gradient_id})", rx=12, ry=12, stroke=palette.border, stroke_width=1),
    ]

    # Header
    children.append(svg_text(24, 28, "Top Languages", palette.text, font_size=18, font_weight="700"))
    children.append(svg_line(24, 36, width - 24, 36, palette.border, stroke_width=1))

    if not languages:
        children.append(svg_text(width / 2, height / 2 + 10, "No language data available", palette.text_muted, font_size=14, text_anchor="middle"))
        return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")

    # Language bars
    bar_width = width - 160
    bar_height = 10
    start_y = 56
    gap = 20

    for i, lang in enumerate(languages[:6]):
        y = start_y + i * gap
        name = lang.get("name", "Unknown")
        percentage = lang.get("percentage", 0)
        color = lang.get("color", palette.primary)

        # Language name
        children.append(svg_text(24, y + 8, name, palette.text, font_size=11, font_weight="500"))

        # Percentage
        children.append(svg_text(width - 24, y + 8, f"{percentage}%", palette.text_muted, font_size=11, font_weight="500", text_anchor="end"))

        # Progress bar background
        children.append(svg_rect(24, y + 14, bar_width, bar_height, palette.border, rx=5, ry=5))

        # Progress bar fill
        if percentage > 0:
            gradient_id = f"lang-{i}-{palette_name}"
            defs_children = [
                svg_linear_gradient(gradient_id, 0, 0, 100, 0, [
                    (0, color),
                    (1, palette.primary),
                ]),
            ]
            # Add to existing defs
            children[0] = children[0].replace("</defs>", f"{svg_linear_gradient(gradient_id, 0, 0, 100, 0, [(0, color), (1, palette.primary)])}</defs>")

            children.append(
                svg_rect(24, y + 14, bar_width * (percentage / 100), bar_height, f"url(#{gradient_id})", rx=5, ry=5)
            )

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


def generate_profile_card(
    user_data: Dict[str, Any],
    stats: Dict[str, int],
    palette_name: str = "midnight",
    width: int = 495,
    height: int = 280,
) -> str:
    """Generate a profile summary card with avatar and bio."""
    palette = get_palette(palette_name)

    gradient_id = f"profile-bg-{palette_name}"
    defs = svg_defs([
        svg_linear_gradient(gradient_id, 0, 0, 0, 100, [
            (0, palette.background),
            (1, palette.border),
        ]),
    ])

    children = [
        defs,
        svg_rect(0, 0, width, height, f"url(#{gradient_id})", rx=12, ry=12, stroke=palette.border, stroke_width=1),
    ]

    # Avatar area
    avatar_size = 80
    avatar_x = 24
    avatar_y = 24

    # Avatar placeholder (circle with gradient)
    avatar_gradient = f"avatar-{palette_name}"
    children[0] = children[0].replace("</defs>", f'{svg_linear_gradient(avatar_gradient, 0, 0, 100, 100, [(0, palette.primary), (1, palette.secondary)])}</defs>')
    children.append(svg_circle(avatar_x + avatar_size / 2, avatar_y + avatar_size / 2, avatar_size / 2, f"url(#{avatar_gradient})"))

    # Username
    name = user_data.get("name") or user_data.get("login", "Unknown")
    children.append(svg_text(avatar_x + avatar_size + 20, avatar_y + 22, xml_escape(name), palette.text, font_size=20, font_weight="700"))

    # Handle
    login = user_data.get("login", "")
    children.append(svg_text(avatar_x + avatar_size + 20, avatar_y + 46, f"@{xml_escape(login)}", palette.text_muted, font_size=13, font_weight="400"))

    # Bio
    bio = user_data.get("bio", "")
    if bio:
        bio_truncated = bio[:120] + ("..." if len(bio) > 120 else "")
        children.append(svg_text(avatar_x + avatar_size + 20, avatar_y + 70, xml_escape(bio_truncated), palette.text, font_size=12, font_weight="400"))

    # Location & website
    meta_y = avatar_y + avatar_size + 16
    if user_data.get("location"):
        children.append(svg_text(avatar_x, meta_y, f"📍 {xml_escape(user_data['location'])}", palette.text_muted, font_size=11))

    if user_data.get("websiteUrl"):
        children.append(svg_text(avatar_x, meta_y + 20, f"🌐 {xml_escape(user_data['websiteUrl'])}", palette.text_muted, font_size=11))

    # Stats row
    stats_y = meta_y + 40
    stat_items = [
        (format_number(stats.get("repos", 0)), "Repos"),
        (format_number(stats.get("stars", 0)), "Stars"),
        (format_number(stats.get("followers", 0)), "Followers"),
        (format_number(stats.get("contributions", 0)), "Contributions"),
    ]

    item_width = (width - 48) / 4
    for i, (value, label) in enumerate(stat_items):
        x = 24 + i * item_width
        children.append(svg_text(x + item_width / 2, stats_y, value, palette.text, font_size=18, font_weight="700", text_anchor="middle"))
        children.append(svg_text(x + item_width / 2, stats_y + 20, label, palette.text_muted, font_size=10, font_weight="500", text_anchor="middle"))

    return svg_svg(width, height, children, viewBox=f"0 0 {width} {height}")


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