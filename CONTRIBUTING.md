# Contributing

Thanks for your interest in improving github-profile-builder!

## Development Setup

```bash
git clone https://github.com/aayushmanrajputdev/github-profile-builder
cd github-profile-builder
python -m venv .venv
source .venv/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests are mock-based. They verify:

- GitHub API response parsing
- SVG structure and self-containment
- XML escaping of user-provided text
- Hex color validation
- CLI argument handling

## Live API Testing

End-to-end testing against the live GitHub API requires network access and is not available in all environments. To run live tests:

```bash
export GITHUB_TOKEN=ghp_xxxx
python scripts/generate.py --username aayushmanrajputdev --format all --output ./out
```

## Code Style

- Python 3.11+ features only
- Standard library only for core output paths
- Functions under 60 lines
- Docstrings on all public functions
- Type hints on all public signatures

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Add tests for any new behavior
4. Ensure all tests pass
5. Open a PR describing the change

## Reporting Issues

Include:

- Python version
- Command run
- Expected vs actual output
- Any error messages

## License

By contributing, you agree that your contributions are licensed under the MIT License.