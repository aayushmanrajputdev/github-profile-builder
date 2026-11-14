#!/usr/bin/env python3
"""Main CLI for github-profile-builder.

One-shot CLI: python scripts/generate.py --username <user> [--token <token>]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import local modules
from scripts.github_api import (
    GitHubClient,
    GitHubAPIError,
    parse_contribution_calendar,
    calculate_streaks,
    aggregate_languages,
    get_top_languages,
)
from scripts.svg_stats import (
    generate_stats_card,
    generate_individual_stat_cards,
    generate_language_stats_card,
    generate_profile_card,
)
from scripts.svg_snake import (
    generate_contribution_snake,
    generate_mini_snake,
)
from scripts.svg_wrapped import (
    generate_wrapped_summary,
    generate_wrapped_card_set,
)
from scripts.svg_certificate import (
    generate_certificate,
    generate_compact_certificate,
)
from scripts.preview import (
    generate_html_preview,
    write_preview_file,
    generate_readme_content,
)
from scripts.svg_components import list_palettes, get_palette


DEFAULT_OUTPUT_DIR = Path("github-profile-output")
DEFAULT_YEAR = 2025


def fetch_user_data(client: GitHubClient, username: str) -> Dict[str, Any]:
    """Fetch all user data from GitHub API."""
    print(f"  Fetching user profile for @{username}...")
    user_data = client.get_user(username)

    print(f"  Fetching repositories...")
    repos = client.get_user_repos(username, per_page=100, max_pages=10)

    print(f"  Fetching starred repositories...")
    starred = client.get_user_starred(username)

    print(f"  Fetching contribution calendar...")
    current_year = DEFAULT_YEAR
    contrib_data = client.get_contributions(username, current_year)

    return {
        "user": user_data,
        "repos": repos,
        "starred": starred,
        "contrib_data": contrib_data,
        "year": current_year,
    }


def build_stats(
    user_data: Dict[str, Any],
    repos: List[Dict[str, Any]],
    starred: List[Dict[str, Any]],
    contrib_data: Dict[str, Any],
    year: int,
) -> Dict[str, Any]:
    """Build comprehensive stats from raw API data."""
    user = user_data.get("user", {})
    contrib_collection = (
        contrib_data.get("user", {})
        .get("contributionsCollection", {})
    )
    calendar = contrib_collection.get("contributionCalendar", {})

    # Parse contribution days
    weeks = calendar.get("weeks", [])
    all_days = []
    for week in weeks:
        for day in week.get("contributionDays", []):
            all_days.append({
                "date": day["date"],
                "count": day["contributionCount"],
                "color": day["color"],
            })

    # Filter to year
    year_str = str(year)
    year_days = [d for d in all_days if d["date"].startswith(year_str)]

    # Calculate streaks
    streaks = calculate_streaks(year_days)

    # Total contributions
    total_contrib = sum(d["count"] for d in year_days)

    # Language stats
    lang_totals = aggregate_languages(repos)
    top_languages = get_top_languages(lang_totals, limit=10)

    # Add language colors (simplified)
    lang_colors = [
        "#f1e05a", "#3572A5", "#b07219", "#701516", "#4F5D95",
        "#89e051", "#43828c", "#b84031", "#e34c26", "#563d7c",
    ]
    for i, lang in enumerate(top_languages):
        lang["color"] = lang_colors[i % len(lang_colors)]

    # Repo highlights
    sorted_repos = sorted(
        repos,
        key=lambda r: r.get("stargazerCount", 0),
        reverse=True,
    )
    top_repos = [
        {
            "name": r.get("name", ""),
            "description": r.get("description", ""),
            "stars": r.get("stargazerCount", 0),
            "language": (r.get("primaryLanguage", {}) or {}).get("name", ""),
            "language_color": (r.get("primaryLanguage", {}) or {}).get("color", "#cccccc"),
        }
        for r in sorted_repos[:4]
    ]

    # User stats
    stats = {
        "total_contributions": total_contrib,
        "commits": contrib_collection.get("totalCommitContributions", 0),
        "pull_requests": contrib_collection.get("totalPullRequestContributions", 0),
        "issues": contrib_collection.get("totalIssueContributions", 0),
        "reviews": contrib_collection.get("totalPullRequestReviewContributions", 0),
        "repos_contributed_to": contrib_collection.get("totalRepositoryContributions", 0),
        "repos_created": user.get("public_repos", len(repos)),
        "stars_received": user.get("public_gists", 0),
        "stars_given": len(starred),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "current_streak": streaks["current"],
        "longest_streak": streaks["longest"],
        "top_languages": top_languages,
        "top_repos": top_repos,
        # Legacy keys for compatibility
        "repos": user.get("public_repos", len(repos)),
        "stars": sum(r.get("stargazerCount", 0) for r in repos),
        "contributions": total_contrib,
    }

    return stats


def generate_all_svgs(
    username: str,
    user_data: Dict[str, Any],
    stats: Dict[str, Any],
    palette_name: str,
    output_dir: Path,
    year: int,
) -> Dict[str, str]:
    """Generate all SVG assets."""
    generated = {}

    print("  Generating stats card...")
    generated["stats"] = generate_stats_card(username, stats, palette_name)

    print("  Generating individual stat cards...")
    individual = generate_individual_stat_cards(username, stats, palette_name)
    generated["individual_cards"] = individual

    print("  Generating language stats card...")
    generated["languages"] = generate_language_stats_card(
        stats.get("top_languages", []), palette_name
    )

    print("  Generating profile card...")
    generated["profile"] = generate_profile_card(user_data, stats, palette_name)

    print("  Generating contribution snake...")
    all_days = []
    contrib_collection = (
        user_data.get("contrib_data", {})
        .get("user", {})
        .get("contributionsCollection", {})
    )
    for week in contrib_collection.get("contributionCalendar", {}).get("weeks", []):
        for day in week.get("contributionDays", []):
            all_days.append({
                "date": day["date"],
                "count": day["contributionCount"],
                "color": day["color"],
            })
    generated["snake"] = generate_contribution_snake(all_days, year, palette_name)

    print("  Generating GitHub Wrapped...")
    generated["wrapped"] = generate_wrapped_summary(username, year, stats, palette_name)
    generated["wrapped_cards"] = generate_wrapped_card_set(username, year, stats, palette_name)

    print("  Generating certificate...")
    generated["certificate"] = generate_certificate(username, user_data.get("user", {}), stats, palette_name)

    # Save individual SVG files
    print(f"  Saving SVG files to {output_dir}...")
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in generated.items():
        if isinstance(content, dict):
            for subname, svg in content.items():
                filepath = output_dir / f"{subname}_{filename}.svg"
                filepath.write_text(svg, encoding="utf-8")
        else:
            filepath = output_dir / f"{filename}.svg"
            filepath.write_text(content, encoding="utf-8")

    return generated


def generate_preview(
    username: str,
    generated: Dict[str, str],
    stats: Dict[str, Any],
    user_data: Dict[str, Any],
    palette_name: str,
    output_dir: Path,
) -> Path:
    """Generate HTML preview and README content."""
    print("  Generating HTML preview...")
    html = generate_html_preview(
        username=username,
        generated_files=generated,
        stats=stats,
        user_data=user_data.get("user", {}),
        palette_name=palette_name,
    )

    preview_path = output_dir / "preview.html"
    write_preview_file(html, str(preview_path))
    print(f"  Saved preview to {preview_path}")

    # Generate README content
    readme_content = generate_readme_content(
        username=username,
        generated_files=generated,
        stats=stats,
        user_data=user_data.get("user", {}),
        palette_name=palette_name,
    )

    readme_path = output_dir / "README_GENERATED.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"  Saved README preview to {readme_path}")

    return preview_path


def main():
    parser = argparse.ArgumentParser(
        description="github-profile-builder: Generate GitHub profile SVGs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate.py --username octocat
  python scripts/generate.py --username octocat --token ghp_xxx
  python scripts/generate.py --username octocat --palette dracula
  python scripts/generate.py --username octocat --output ./my-profile
  python scripts/generate.py --username octocat --year 2024

Rate limits:
  Without token: 60 requests/hour
  With token: 5000 requests/hour
  Get a token at: https://github.com/settings/tokens
        """,
    )

    parser.add_argument("--username", "-u", required=True, help="GitHub username")
    parser.add_argument(
        "--token", "-t", default=None,
        help="GitHub API token (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--palette", "-p", default="midnight",
        choices=list_palettes(),
        help=f"Color palette (default: midnight). Available: {', '.join(list_palettes())}"
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--year", "-y", type=int, default=DEFAULT_YEAR,
        help=f"Contribution year (default: {DEFAULT_YEAR})"
    )
    parser.add_argument(
        "--no-preview", action="store_true",
        help="Skip HTML preview generation"
    )

    args = parser.parse_args()

    # Validate palette
    try:
        palette = get_palette(args.palette)
        print(f"Using palette: {palette.name}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\n=== github-profile-builder ===")
    print(f"Username: @{args.username}")
    print(f"Palette: {args.palette}")
    print(f"Output: {args.output}")
    print(f"Year: {args.year}")
    print()

    # Initialize client
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if token:
        print("Using authenticated API (5000 req/hr limit)")
    else:
        print("Using unauthenticated API (60 req/hr limit)")

    client = GitHubClient(token=token)

    try:
        # Fetch data
        print("\n--- Fetching GitHub data ---")
        data = fetch_user_data(client, args.username)

        # Build stats
        print("\n--- Building stats ---")
        stats = build_stats(
            user_data=data.get("contrib_data", {}),
            repos=data.get("repos", []),
            starred=data.get("starred", []),
            contrib_data=data.get("contrib_data", {}),
            year=args.year,
        )
        print(f"  Total contributions: {stats['total_contributions']}")
        print(f"  Current streak: {stats['current_streak']} days")
        print(f"  Longest streak: {stats['longest_streak']} days")
        print(f"  Followers: {stats['followers']}")
        print(f"  Repositories: {stats['repos']}")

        # Generate SVGs
        print("\n--- Generating SVGs ---")
        generated = generate_all_svgs(
            username=args.username,
            user_data={
                "user": data.get("user", {}),
                "contrib_data": data.get("contrib_data", {}),
            },
            stats=stats,
            palette_name=args.palette,
            output_dir=args.output,
            year=args.year,
        )

        # Generate preview
        if not args.no_preview:
            print("\n--- Generating preview ---")
            preview_path = generate_preview(
                username=args.username,
                generated=generated,
                stats=stats,
                user_data={"user": data.get("user", {})},
                palette_name=args.palette,
                output_dir=args.output,
            )

        print(f"\n=== Done! ===")
        print(f"Output directory: {args.output.absolute()}")
        print(f"Generated files:")
        for f in sorted(args.output.glob("*.svg")):
            print(f"  - {f.name}")
        if not args.no_preview:
            print(f"  - preview.html")

        # Save metadata
        meta_path = args.output / "metadata.json"
        meta_path.write_text(
            json.dumps(
                {
                    "username": args.username,
                    "palette": args.palette,
                    "year": args.year,
                    "stats": stats,
                    "user": {
                        "name": data.get("user", {}).get("name"),
                        "login": data.get("user", {}).get("login"),
                        "bio": data.get("user", {}).get("bio"),
                        "followers": data.get("user", {}).get("followers"),
                        "following": data.get("user", {}).get("following"),
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"  - metadata.json")

        print(f"\nReady to use! Copy the SVG files to your README or profile.")

    except GitHubAPIError as e:
        print(f"\nGitHub API Error: {e}")
        if e.status_code == 404:
            print(f"User not found: @{args.username}")
            print("Check the username and try again.")
        elif e.status_code == 403:
            print("Rate limit exceeded. Use --token to authenticate.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
