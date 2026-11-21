# Contributing

Thanks for helping improve `pertext`.

## Setup

```bash
pip install -e ".[dev]"
pytest
```

## Guidelines

- Keep the library dependency-free (standard library only).
- Every behavior change needs a test. Normalization must stay idempotent.
- Prefer conservative rules: when unsure, leave the text unchanged.
- Add a line to `CHANGELOG.md` for user-visible changes.
- Open an issue first for large changes or new normalization rules, with real
  Persian examples (before and after).

## Pull requests

Keep PRs small and focused, and make sure CI passes.
