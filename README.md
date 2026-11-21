# pertext

[![CI](https://github.com/vahiddaryanush/pertext/actions/workflows/ci.yml/badge.svg)](https://github.com/vahiddaryanush/pertext/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Dependencies: none](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

Zero-dependency Python library and CLI for **Persian (Farsi) text normalization** and **Jalali (Solar Hijri) ↔ Gregorian date conversion**.

Persian text found in the wild is messy: Arabic *yeh* and *kaf* mixed with the Persian forms, three different digit systems, missing or misplaced half-spaces (ZWNJ), diacritics, tatweel, and Latin punctuation inside Persian sentences. These inconsistencies silently break search, deduplication, string matching, and NLP pipelines. `pertext` fixes them with a small, predictable, well-tested API.

## Features

- Unify Arabic letter variants (ي → ی, ك → ک, ى → ی)
- Convert digits to Persian (۰-۹) or Latin (0-9), including Arabic-Indic digits
- Insert correct half-spaces (ZWNJ) after `می` / `نمی` and before `ها`, `های`, `تر`, `ترین`, …
- Clean up stray, repeated, or misplaced ZWNJ characters
- Strip diacritics and tatweel; decompose Arabic presentation forms from copied PDFs
- Use Persian punctuation (`، ؛ ؟`) only where it follows a Persian letter
- Convert between Gregorian and Jalali dates; leap years and month lengths included
- Pure standard library, fully typed, idempotent normalization

## Installation

```bash
pip install pertext
```

Requires Python 3.9 or newer. No third-party dependencies.

## Quick start

```python
from pertext import normalize, gregorian_to_jalali, jalali_to_gregorian, format_jalali

normalize("من كتاب ها را می خوانم, اما نمی دانم?")
# 'من کتاب‌ها را می‌خوانم، اما نمی‌دانم؟'

normalize("سال 2026 است", digits="fa")
# 'سال ۲۰۲۶ است'

gregorian_to_jalali(2026, 11, 20)
# (1405, 8, 29)

format_jalali(1405, 8, 29, long=True)
# '29 آبان 1405'

jalali_to_gregorian(1405, 8, 29)
# (2026, 11, 20)
```

## Command line

```bash
$ echo 'كتاب ها را می خوانم, اما نمی دانم?' | pertext normalize --digits fa
کتاب‌ها را می‌خوانم، اما نمی‌دانم؟

$ pertext date 2026-11-20 --long
29 آبان 1405

$ pertext date --jalali 1405/08/29
2026-11-20

$ pertext normalize input.txt -o output.txt
```

## API

| Function | Description |
| --- | --- |
| `normalize(text, *, digits=None, remove_diacritics=True, remove_tatweel=True, fix_spacing=True, fix_punctuation_marks=True)` | Full normalization pipeline. `digits` is `"fa"`, `"en"`, or `None`. |
| `to_persian_digits(text)` / `to_latin_digits(text)` | Digit conversion only. |
| `strip_diacritics(text)` | Remove harakat, tanwin, shadda, and dagger alef. |
| `gregorian_to_jalali(y, m, d)` | Returns `(year, month, day)`. Raises `ValueError` on invalid dates. |
| `jalali_to_gregorian(y, m, d)` | Returns `(year, month, day)`. Raises `ValueError` on invalid dates. |
| `is_jalali_leap(year)` / `jalali_month_length(year, month)` | Calendar helpers. |
| `format_jalali(y, m, d, *, long=False)` | `1405/08/29` or `29 آبان 1405`. |

### Design notes

- **Idempotent:** `normalize(normalize(x)) == normalize(x)`.
- **Conservative:** Latin text, URLs, and code-like strings are left untouched.
- **Calendar range:** the Jalali conversion uses the 33-year arithmetic rule, which matches the official calendar for the modern era (about 1178–1633 AP). It is tested by round-tripping every day from 1900 to 2100.

## Development

```bash
git clone https://github.com/vahiddaryanush/pertext
cd pertext
pip install -e ".[dev]"
pytest
```

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

To report a vulnerability, see [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
