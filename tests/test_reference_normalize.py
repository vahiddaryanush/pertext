"""Reference cases for Persian normalization.

Each case is (input, expected, reason). The reason documents *why* the
transformation is correct, or why the text is deliberately left alone.
\\u200c is the zero-width non-joiner (half-space).
"""

import pytest

from pertext import normalize

Z = "‌"

CASES = [
    # --- letters ---------------------------------------------------------
    ("علي", "علی", "Arabic yeh (U+064A) becomes Persian yeh (U+06CC)"),
    ("كاركرد", "کارکرد", "Arabic kaf (U+0643) becomes Persian keheh (U+06A9)"),
    ("موسى", "موسی", "Alef maksura (U+0649) becomes Persian yeh"),
    ("سلام", "سلام", "already-normal text is unchanged"),
    # --- digits (default leaves digits alone) -----------------------------
    ("۱۴۰۵", "۱۴۰۵", "digits are not converted unless requested"),
    # --- verb prefixes ----------------------------------------------------
    ("می روم", f"می{Z}روم", "می + verb takes a half-space"),
    ("نمی روم", f"نمی{Z}روم", "نمی + verb takes a half-space"),
    ("می‌روم", f"می{Z}روم", "an existing correct half-space is preserved"),
    ("میز", "میز", "word starting with می but not a verb prefix: no space to fix"),
    ("می", "می", "bare می (wine) is left alone"),
    ("شراب می", "شراب می", "trailing می (wine) is not treated as a prefix"),
    # --- plural / comparative suffixes -------------------------------------
    ("کتاب ها", f"کتاب{Z}ها", "plural ها attaches with a half-space"),
    ("کتاب های من", f"کتاب{Z}های من", "های attaches; following word is untouched"),
    ("بزرگ تر", f"بزرگ{Z}تر", "comparative تر attaches with a half-space"),
    ("بزرگ ترین", f"بزرگ{Z}ترین", "superlative ترین attaches with a half-space"),
    ("کتابها", "کتابها", "already joined without space: left as written"),
    # --- punctuation -------------------------------------------------------
    ("سلام, دنیا", "سلام، دنیا", "comma after a Persian letter becomes ،"),
    ("چطوری?", "چطوری؟", "question mark after a Persian letter becomes ؟"),
    ("a, b", "a, b", "Latin punctuation after Latin text is unchanged"),
    ("1,000", "1,000", "thousands separator is unchanged"),
    # --- mixed scripts -----------------------------------------------------
    ("نسخه v2.0 منتشر شد", "نسخه v2.0 منتشر شد", "embedded Latin tokens are not altered"),
    ("به api.example.com برو", "به api.example.com برو", "URLs/hostnames are not altered"),
    # --- whitespace ---------------------------------------------------------
    ("سلام    دنیا", "سلام دنیا", "runs of spaces collapse to one"),
    ("  سلام  ", "سلام", "outer whitespace is trimmed"),
]


@pytest.mark.parametrize("text, expected, reason", CASES, ids=[c[2] for c in CASES])
def test_reference_case(text, expected, reason):
    assert normalize(text) == expected, reason


def test_digit_options_reference():
    assert normalize("1405 ١٤٠٥ ۱۴۰۵", digits="fa") == "۱۴۰۵ ۱۴۰۵ ۱۴۰۵"
    assert normalize("1405 ١٤٠٥ ۱۴۰۵", digits="en") == "1405 1405 1405"
