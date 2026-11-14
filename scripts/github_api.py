"""GitHub API client with rate limit handling."""

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


GITHUB_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


@dataclass
class RateLimitInfo:
    """Rate limit information from GitHub API headers."""
    limit: int
    remaining: int
    reset: int
    used: int


class GitHubAPIError(Exception):
    """Raised when GitHub API returns an error."""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class GitHubClient:
    """Client for GitHub REST and GraphQL APIs with rate limit handling."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.session_headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-profile-builder/1.0",
        }
        if self.token:
            self.session_headers["Authorization"] = f"Bearer {self.token}"

    def _request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> tuple[Dict[str, Any], RateLimitInfo]:
        """Make an HTTP request to GitHub API."""
        req_headers = {**self.session_headers, **(headers or {})}
        body = json.dumps(data).encode() if data else None

        req = urllib.request.Request(url, data=body, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req) as resp:
                response_data = json.loads(resp.read().decode())
                rate_limit = self._parse_rate_limit(resp.headers)
                return response_data, rate_limit
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise GitHubAPIError(
                f"GitHub API error ({e.code}): {error_body}",
                status_code=e.code,
            )
        except urllib.error.URLError as e:
            raise GitHubAPIError(f"Network error: {e}")

    def _parse_rate_limit(self, headers) -> RateLimitInfo:
        """Parse rate limit info from response headers."""
        def get_header(name: str) -> int:
            val = headers.get(name, headers.get(name.title(), "0"))
            try:
                return int(val)
            except ValueError:
                return 0

        return RateLimitInfo(
            limit=get_header("X-RateLimit-Limit"),
            remaining=get_header("X-RateLimit-Remaining"),
            reset=get_header("X-RateLimit-Reset"),
            used=get_header("X-RateLimit-Used"),
        )

    def _wait_for_rate_limit(self, rate_limit: RateLimitInfo) -> None:
        """Wait if rate limit is exhausted."""
        if rate_limit.remaining == 0:
            wait_time = max(rate_limit.reset - int(time.time()), 0) + 1
            if wait_time > 0:
                time.sleep(wait_time)

    # --- REST API methods ---

    def get_user(self, username: str) -> Dict[str, Any]:
        """Get user profile information."""
        url = f"{GITHUB_API_BASE}/users/{username}"
        data, rate_limit = self._request(url)
        self._wait_for_rate_limit(rate_limit)
        return data

    def get_user_repos(
        self,
        username: str,
        per_page: int = 100,
        max_pages: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get user's public repositories."""
        repos = []
        page = 1
        while page <= max_pages:
            url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page={per_page}&page={page}&sort=updated"
            data, rate_limit = self._request(url)
            self._wait_for_rate_limit(rate_limit)
            if not data:
                break
            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return repos

    def get_user_starred(
        self,
        username: str,
        per_page: int = 100,
        max_pages: int = 5,
    ) -> List[Dict[str, Any]]:
        """Get repositories starred by the user."""
        starred = []
        page = 1
        while page <= max_pages:
            url = f"{GITHUB_API_BASE}/users/{username}/starred?per_page={per_page}&page={page}"
            data, rate_limit = self._request(url)
            self._wait_for_rate_limit(rate_limit)
            if not data:
                break
            starred.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return starred

    def get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get language breakdown for a repository."""
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/languages"
        data, rate_limit = self._request(url)
        self._wait_for_rate_limit(rate_limit)
        return data

    # --- GraphQL API methods ---

    def graphql(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a GraphQL query."""
        data, rate_limit = self._request(
            GITHUB_GRAPHQL_URL,
            method="POST",
            data={"query": query, "variables": variables or {}},
            headers={"Content-Type": "application/json"},
        )
        self._wait_for_rate_limit(rate_limit)

        if "errors" in data:
            error_msgs = [e.get("message", "Unknown error") for e in data["errors"]]
            raise GitHubAPIError(f"GraphQL errors: {', '.join(error_msgs)}")

        return data.get("data", {})

    def get_contributions(
        self,
        username: str,
        year: int,
    ) -> Dict[str, Any]:
        """Get contribution calendar data for a user in a given year."""
        query = """
        query($username: String!, $from: DateTime!, $to: DateTime!) {
            user(login: $username) {
                contributionsCollection(from: $from, to: $to) {
                    contributionCalendar {
                        totalContributions
                        weeks {
                            contributionDays {
                                date
                                contributionCount
                                color
                            }
                        }
                    }
                }
            }
        }
        """
        from_date = f"{year}-01-01T00:00:00Z"
        to_date = f"{year}-12-31T23:59:59Z"
        variables = {"username": username, "from": from_date, "to": to_date}
        return self.graphql(query, variables)

    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get comprehensive user stats via GraphQL."""
        query = """
        query($username: String!) {
            user(login: $username) {
                login
                name
                bio
                avatarUrl
                location
                websiteUrl
                twitterUsername
                createdAt
                repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER) {
                    totalCount
                    nodes {
                        name
                        stargazerCount
                        forkCount
                        primaryLanguage {
                            name
                            color
                        }
                        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                            edges {
                                size
                                node {
                                    name
                                }
                            }
                        }
                    }
                }
                followers {
                    totalCount
                }
                following {
                    totalCount
                }
                starredRepositories {
                    totalCount
                }
                contributionsCollection {
                    totalCommitContributions
                    totalIssueContributions
                    totalPullRequestContributions
                    totalPullRequestReviewContributions
                    totalRepositoryContributions
                }
            }
        }
        """
        return self.graphql(query, {"username": username})

    def get_recent_contributions(self, username: str, days: int = 365) -> Dict[str, Any]:
        """Get recent contribution data."""
        # Use REST API for contributions summary
        url = f"{GITHUB_API_BASE}/users/{username}/events/public?per_page=100"
        data, rate_limit = self._request(url)
        self._wait_for_rate_limit(rate_limit)
        return {"events": data}


def parse_contribution_calendar(calendar_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse GraphQL contribution calendar into a flat list of days."""
    days = []
    for week in calendar_data.get("weeks", []):
        for day in week.get("contributionDays", []):
            days.append({
                "date": day["date"],
                "count": day["contributionCount"],
                "color": day["color"],
            })
    return days


def calculate_streaks(days: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate current and longest contribution streaks."""
    if not days:
        return {"current": 0, "longest": 0}

    # Sort by date
    sorted_days = sorted(days, key=lambda d: d["date"])

    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    for i, day in enumerate(sorted_days):
        if day["count"] > 0:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0

    # Calculate current streak (from most recent date backwards)
    for day in reversed(sorted_days):
        if day["count"] > 0:
            current_streak += 1
        else:
            break

    return {"current": current_streak, "longest": longest_streak}


def aggregate_languages(repos: List[Dict[str, Any]]) -> Dict[str, int]:
    """Aggregate language bytes across all repositories."""
    lang_totals: Dict[str, int] = {}
    for repo in repos:
        for edge in repo.get("languages", {}).get("edges", []):
            name = edge["node"]["name"]
            size = edge["size"]
            lang_totals[name] = lang_totals.get(name, 0) + size
    return lang_totals


def get_top_languages(lang_totals: Dict[str, int], limit: int = 5) -> List[Dict[str, Any]]:
    """Get top languages by bytes."""
    sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)
    total = sum(lang_totals.values())
    return [
        {"name": name, "bytes": bytes_, "percentage": round(bytes_ / total * 100, 1) if total > 0 else 0}
        for name, bytes_ in sorted_langs[:limit]
    ]