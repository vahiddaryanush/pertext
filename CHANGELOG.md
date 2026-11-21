# Changelog

## Unreleased

- `format_jalali` now validates its input and raises `ValueError`.
- Supported year range (1-9999) is enforced and documented.
- Letter set used by spacing/punctuation rules is now explicit (excludes tatweel).
- README: install instructions no longer claim a PyPI release; Latin-text and
  calendar-accuracy statements corrected.
- Reference test suites for Persian normalization (each case documents its reason) and for known Jalali dates; 134 tests total.

## 0.1.0

- Initial release: Persian text normalization, digit conversion, half-space
  fixing, Gregorian ↔ Jalali conversion, and the `pertext` CLI.
