# GitHub API Integration

This document describes how github-profile-builder fetches data from the GitHub API.

## API Endpoints Used

### REST API
- `GET /users/{username}` - User profile data
- `GET /users/{username}/repos` - List repositories
- `GET /users/{username}/starred` - Starred repositories

### GraphQL API
- `contributionsCollection` - Contribution calendar and stats
- `user` query - Comprehensive user data

## Rate Limits

| Authentication | Rate Limit |
|----------------|------------|
| Unauthenticated | 60 requests/hour |
| Authenticated | 5,000 requests/hour |

## Getting a Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. No scopes required (public data only)
4. Copy the token for use with the tool

## Data Flow

```
User Input (username)
    ↓
GitHub API Client
    ↓
Fetch user profile → repos → starred → contributions
    ↓
Build stats from raw API data
    ↓
Generate SVG assets
```

## API Response Handling

- All API responses are cached internally during execution
- Missing data is handled gracefully (None/empty defaults)
- Color data is preserved for contribution heatmap styling

## Error Handling

- 404: User not found
- 403: Rate limit exceeded
- 500: Server error (retry with exponential backoff)

## Year-Wrapped Data

All metrics in Wrapped summaries are wrapped for the calendar year specified by `--year` parameter. Default is 2025.

## Security Notes

- Tokens are never stored
- Tokens are only used for the current execution
- Always use environment variables or CLI args for tokens