"""Tests for github-profile-builder."""

import unittest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.svg_components import (
    xml_escape,
    validate_hex_color,
    format_number,
    ColorPalette,
    get_palette,
    svg_rect,
    svg_text,
    svg_svg,
)
from scripts.svg_stats import (
    generate_stats_card,
    generate_language_stats_card,
)
from scripts.svg_snake import (
    generate_contribution_snake,
)
from scripts.svg_wrapped import (
    generate_wrapped_summary,
)
from scripts.svg_certificate import (
    generate_certificate,
)
from scripts.github_api import (
    calculate_streaks,
    parse_contribution_calendar,
    aggregate_languages,
    get_top_languages,
)


class TestSVGComponents(unittest.TestCase):
    """Test SVG component generators."""

    def test_xml_escape(self):
        """Test XML escaping."""
        self.assertEqual(xml_escape("Hello <World>"), "Hello <World>")
        self.assertEqual(xml_escape("A & B"), "A & B")
        self.assertEqual(xml_escape('Test "quotes"'), 'Test "quotes"')
        self.assertEqual(xml_escape("Test 'apostrophe'"), "Test &apos;apostrophe&apos;")

    def test_validate_hex_color(self):
        """Test hex color validation."""
        self.assertEqual(validate_hex_color("#ffffff"), "#ffffff")
        self.assertEqual(validate_hex_color("#FFFFFF"), "#ffffff")
        self.assertEqual(validate_hex_color("#abc123"), "#abc123")
        with self.assertRaises(ValueError):
            validate_hex_color("invalid")
        with self.assertRaises(ValueError):
            validate_hex_color("#gggggg")

    def test_format_number(self):
        """Test number formatting."""
        self.assertEqual(format_number(500), "500")
        self.assertEqual(format_number(1500), "1.5K")
        self.assertEqual(format_number(1000000), "1M")
        self.assertEqual(format_number(1250000), "1.3M")

    def test_color_palette(self):
        """Test color palette creation."""
        palette = ColorPalette(
            "test",
            primary="#ff0000",
            secondary="#00ff00",
            accent="#0000ff",
            background="#ffffff",
            text="#000000",
            text_muted="#888888",
            border="#cccccc",
        )
        self.assertEqual(palette.name, "test")
        self.assertEqual(palette.primary, "#ff0000")

    def test_get_palette(self):
        """Test palette retrieval."""
        palette = get_palette("midnight")
        self.assertEqual(palette.name, "Midnight")
        with self.assertRaises(ValueError):
            get_palette("nonexistent")

    def test_list_palettes(self):
        """Test listing available palettes."""
        palettes = ColorPalette
        # Just verify we get some palettes
        from scripts.svg_components import PALETTES
        self.assertGreater(len(PALETTES), 0)

    def test_svg_rect(self):
        """Test rect element generation."""
        result = svg_rect(0, 0, 100, 50, "#ff0000")
        self.assertIn('x="0"', result)
        self.assertIn('width="100"', result)
        self.assertIn('height="50"', result)
        self.assertIn('fill="#ff0000"', result)

    def test_svg_text(self):
        """Test text element generation."""
        result = svg_text(10, 20, "Hello", "#000000")
        self.assertIn('x="10"', result)
        self.assertIn('y="20"', result)
        self.assertIn(">Hello<", result)

    def test_svg_svg(self):
        """Test SVG root element generation."""
        children = [svg_text(10, 20, "Test", "#000000")]
        result = svg_svg(100, 100, children)
        self.assertIn('width="100"', result)
        self.assertIn('height="100"', result)
        self.assertIn("<svg", result)


class TestStatsGeneration(unittest.TestCase):
    """Test stats SVG generation."""

    def test_generate_stats_card(self):
        """Test stats card generation."""
        stats = {
            "repos": 10,
            "stars": 100,
            "followers": 50,
            "following": 30,
            "contributions": 500,
            "commits": 400,
        }
        result = generate_stats_card("testuser", stats, "midnight")
        self.assertIn("<svg", result)
        self.assertIn("testuser", result)

    def test_generate_individual_stat_cards(self):
        """Test individual stat cards generation."""
        stats = {
            "repos": 10,
            "stars": 100,
            "followers": 50,
            "following": 30,
            "contributions": 500,
            "commits": 400,
        }
        result = generate_individual_stat_cards("testuser", stats, "midnight")
        self.assertIsInstance(result, dict)
        self.assertIn("repos", result)
        self.assertIn("stars", result)

    def test_generate_language_stats_card(self):
        """Test language stats card generation."""
        languages = [
            {"name": "Python", "percentage": 50},
            {"name": "JavaScript", "percentage": 30},
        ]
        result = generate_language_stats_card(languages, "midnight")
        self.assertIn("<svg", result)

    def test_generate_profile_card(self):
        """Test profile card generation."""
        user_data = {
            "name": "Test User",
            "login": "testuser",
            "bio": "Test bio",
            "location": "Test Location",
            "websiteUrl": "https://example.com",
        }
        stats = {
            "repos": 10,
            "stars": 100,
            "followers": 50,
            "contributions": 500,
        }
        result = generate_profile_card(user_data, stats, "midnight")
        self.assertIn("<svg", result)
        self.assertIn("Test User", result)


class TestSnakeGenerator(unittest.TestCase):
    """Test contribution snake generation."""

    def test_generate_contribution_snake(self):
        """Test contribution snake generation."""
        days = [
            {"date": "2025-01-01", "count": 5, "color": "#ebedf0"},
            {"date": "2025-01-02", "count": 10, "color": "#9be9a8"},
            {"date": "2025-01-03", "count": 3, "color": "#40e4d6"},
        ]
        result = generate_contribution_snake(days, 2025, "midnight")
        self.assertIn("<svg", result)

    def test_generate_mini_snake(self):
        """Test mini snake generation."""
        days = [
            {"date": "2025-01-01", "count": 5, "color": "#ebedf0"},
        ]
        result = generate_mini_snake(days)
        self.assertIn("<svg", result)


class TestWrappedGeneration(unittest.TestCase):
    """Test GitHub Wrapped generation."""

    def test_generate_wrapped_summary(self):
        """Test wrapped summary generation."""
        stats = {
            "total_contributions": 1000,
            "commits": 800,
            "pull_requests": 50,
            "issues": 30,
            "reviews": 20,
            "repos_contributed_to": 10,
            "current_streak": 30,
            "longest_streak": 45,
            "followers": 100,
            "following": 50,
            "stars_received": 500,
            "stars_given": 100,
            "repos_created": 20,
            "prs_merged": 25,
            "top_languages": [
                {"name": "Python", "percentage": 50},
                {"name": "JavaScript", "percentage": 30},
            ],
            "top_repos": [
                {"name": "repo1", "description": "A repo", "stars": 100, "language": "Python", "language_color": "#3572A5"},
            ],
        }
        result = generate_wrapped_summary("testuser", 2025, stats, "midnight")
        self.assertIn("<svg", result)
        self.assertIn("GitHub Wrapped 2025", result)

    def test_generate_wrapped_card_set(self):
        """Test wrapped card set generation."""
        stats = {
            "total_contributions": 1000,
            "commits": 800,
            "pull_requests": 50,
            "issues": 30,
            "current_streak": 30,
            "longest_streak": 45,
            "followers": 100,
            "stars_received": 500,
            "repos_created": 20,
            "top_languages": [
                {"name": "Python", "percentage": 50},
            ],
        }
        result = generate_wrapped_card_set("testuser", 2025, stats, "midnight")
        self.assertIsInstance(result, dict)
        self.assertIn("contributions", result)
        self.assertIn("streaks", result)
        self.assertIn("languages", result)


class TestCertificateGeneration(unittest.TestCase):
    """Test certificate generation."""

    def test_generate_certificate(self):
        """Test certificate generation with disclaimer."""
        user_data = {
            "name": "Test User",
            "login": "testuser",
        }
        stats = {
            "total_contributions": 1000,
            "followers": 100,
            "repos": 20,
            "stars": 500,
            "current_streak": 30,
            "longest_streak": 45,
            "top_languages": [{"name": "Python", "percentage": 50}],
        }
        result = generate_certificate("testuser", user_data, stats, "midnight")
        self.assertIn("<svg", result)
        self.assertIn("Test User", result)
        self.assertIn("is not an official GitHub certification", result)

    def test_generate_compact_certificate(self):
        """Test compact certificate generation."""
        user_data = {"name": "Test User", "login": "testuser"}
        stats = {
            "total_contributions": 1000,
            "followers": 100,
            "repos": 20,
            "stars": 500,
            "current_streak": 30,
            "longest_streak": 45,
            "top_languages": [],
        }
        result = generate_compact_certificate("testuser", user_data, stats)
        self.assertIn("<svg", result)


class TestGitHubAPIHelpers(unittest.TestCase):
    """Test GitHub API helper functions."""

    def test_calculate_streaks_empty(self):
        """Test streak calculation with empty data."""
        result = calculate_streaks([])
        self.assertEqual(result["current"], 0)
        self.assertEqual(result["longest"], 0)

    def test_calculate_streaks_with_data(self):
        """Test streak calculation with contribution data."""
        days = [
            {"date": "2025-01-01", "count": 5},
            {"date": "2025-01-02", "count": 0},
            {"date": "2025-01-03", "count": 10},
        ]
        result = calculate_streaks(days)
        self.assertIn("current", result)
        self.assertIn("longest", result)

    def test_aggregate_languages(self):
        """Test language aggregation."""
        repos = [
            {"languages": {"edges": [{"node": {"name": "Python"}, "size": 1000}]}},
            {"languages": {"edges": [{"node": {"name": "Python"}, "size": 500}, {"node": {"name": "JS"}, "size": 300}]}},
        ]
        result = aggregate_languages(repos)
        self.assertEqual(result["Python"], 1500)
        self.assertEqual(result["JS"], 300)

    def test_get_top_languages(self):
        """Test getting top languages."""
        lang_totals = {"Python": 1000, "JavaScript": 800, "Java": 500}
        result = get_top_languages(lang_totals, limit=2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Python")


class TestIntegration(unittest.TestCase):
    """Integration tests for full workflow."""

    def test_full_workflow(self):
        """Test generating complete profile."""
        user_data = {
            "user": {"name": "Test User", "login": "testuser", "bio": "Test bio"},
            "contrib_data": {
                "user": {
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "totalContributions": 1000,
                            "weeks": [
                                {
                                    "contributionDays": [
                                        {"date": "2025-01-01", "contributionCount": 5, "color": "#ebedf0"},
                                        {"date": "2025-01-02", "contributionCount": 10, "color": "#9be9a8"},
                                    ]
                                }
                            ]
                        }
                    }
                }
            },
            "repos": [],
            "starred": [],
        }

        stats = {
            "total_contributions": 1000,
            "commits": 800,
            "pull_requests": 50,
            "issues": 30,
            "reviews": 20,
            "repos_contributed_to": 10,
            "repos": 15,
            "stars": 500,
            "contributions": 1000,
            "followers": 100,
            "following": 50,
            "current_streak": 30,
            "longest_streak": 45,
            "top_languages": [{"name": "Python", "percentage": 50, "color": "#3572A5"}],
            "top_repos": [],
            "stars_received": 500,
            "stars_given": 100,
        }

        # Generate all cards
        stats_card = generate_stats_card("testuser", stats, "midnight")
        self.assertIn("<svg", stats_card)

        lang_card = generate_language_stats_card(stats["top_languages"], "midnight")
        self.assertIn("<svg", lang_card)

        wrapped = generate_wrapped_summary("testuser", 2025, stats, "midnight")
        self.assertIn("<svg", wrapped)

        cert = generate_certificate("testuser", user_data["user"], stats, "midnight")
        self.assertIn("<svg", cert)
        self.assertIn("not an official GitHub certification", cert)


if __name__ == "__main__":
    unittest.main()
