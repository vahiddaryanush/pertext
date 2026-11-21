"""Persian text normalization utilities.

Everything here is pure Python and relies only on the standard library.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Optional

try:  # Python 3.8+
    from typing import Literal

    Digits = Optional[Literal["fa", "en"]]
except ImportError:  # pragma: no cover
    Digits = Optional[str]  # type: ignore[misc]

ZWNJ = "‌"  # zero-width non-joiner ("نیم‌فاصله")

# Arabic letters plus the Persian-only letters (پ چ ژ ک گ ی ۀ).
_L = "\u0621-\u063f\u0641-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc\u06c0"

_LATIN_DIGITS = "0123456789"
_ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"

_TO_PERSIAN = str.maketrans(_LATIN_DIGITS + _ARABIC_DIGITS, _PERSIAN_DIGITS * 2)
_TO_LATIN = str.maketrans(_PERSIAN_DIGITS + _ARABIC_DIGITS, _LATIN_DIGITS * 2)

# Arabic letter forms that should become their Persian counterparts.
_CHAR_TABLE = str.maketrans(
    {
        "ي": "ی",  # ARABIC YEH -> FARSI YEH
        "ى": "ی",  # ALEF MAKSURA -> FARSI YEH
        "ك": "ک",  # ARABIC KAF -> KEHEH
    }
)

_PRESENTATION_FORMS = re.compile("[ﭐ-﷿ﹰ-ﻼ]")
_DIACRITICS = re.compile("[ً-ٰٟ]")

_ZWNJ_RUN = re.compile(ZWNJ + "{2,}")
_ZWNJ_NEXT_TO_SPACE = re.compile(ZWNJ + "+(?=[ \t\r\n])|(?<=[ \t\r\n])" + ZWNJ + "+")
_ZWNJ_AT_EDGE = re.compile("\\A" + ZWNJ + "+|" + ZWNJ + "+\\Z")

_VERB_PREFIX = re.compile("(?<![" + _L + "])(ن?می)[ \t]+(?=[" + _L + "])")
_SUFFIX = re.compile(
    "(?<=[" + _L + "])[ \t]+(ترین|تری|تر|هایی|های|ها)(?![" + _L + "])"
)

_PUNCTUATION = {",": "،", ";": "؛", "?": "؟"}
_PUNCTUATION_RE = re.compile("(?<=[" + _L + "])([,;?])")


def to_persian_digits(text: str) -> str:
    """Convert Latin and Arabic-Indic digits to Persian digits (۰-۹)."""
    return text.translate(_TO_PERSIAN)


def to_latin_digits(text: str) -> str:
    """Convert Persian and Arabic-Indic digits to Latin digits (0-9)."""
    return text.translate(_TO_LATIN)


def strip_diacritics(text: str) -> str:
    """Remove Arabic diacritics (harakat, tanwin, shadda, dagger alef)."""
    return _DIACRITICS.sub("", text)


def clean_zwnj(text: str) -> str:
    """Collapse repeated ZWNJ and drop ones next to spaces or at the edges."""
    text = _ZWNJ_RUN.sub(ZWNJ, text)
    text = _ZWNJ_NEXT_TO_SPACE.sub("", text)
    return _ZWNJ_AT_EDGE.sub("", text)


def fix_half_spaces(text: str) -> str:
    """Insert ZWNJ where Persian orthography expects it.

    Covers the verb prefixes ``می`` / ``نمی`` and the common suffixes
    ``ها``, ``های``, ``هایی``, ``تر``, ``تری`` and ``ترین``.
    """
    text = _VERB_PREFIX.sub("\\1" + ZWNJ, text)
    return _SUFFIX.sub(ZWNJ + "\\1", text)


def fix_punctuation(text: str) -> str:
    """Use Persian ``، ؛ ؟`` when ``, ; ?`` directly follow a Persian letter."""
    return _PUNCTUATION_RE.sub(lambda m: _PUNCTUATION[m.group(1)], text)


def collapse_whitespace(text: str) -> str:
    """Collapse runs of spaces/tabs/NBSP, trim line edges and the text."""
    text = re.sub("[ \t ]+", " ", text)
    text = re.sub(" ?\n ?", "\n", text)
    return text.strip()


def normalize(
    text: str,
    *,
    digits: Digits = None,
    remove_diacritics: bool = True,
    remove_tatweel: bool = True,
    fix_spacing: bool = True,
    fix_punctuation_marks: bool = True,
) -> str:
    """Normalize Persian text.

    Args:
        text: The input string.
        digits: ``"fa"`` for Persian digits, ``"en"`` for Latin digits, or
            ``None`` (default) to leave digits untouched.
        remove_diacritics: Strip harakat and similar marks.
        remove_tatweel: Strip the elongation character (ـ).
        fix_spacing: Insert half-spaces after ``می``/``نمی`` and before
            common suffixes such as ``ها`` and ``تر``.
        fix_punctuation_marks: Convert ``, ; ?`` after Persian letters to
            ``، ؛ ؟``.

    Arabic yeh/kaf are always unified to their Persian forms, and Arabic
    presentation forms (as found in text copied from PDFs) are decomposed.
    """
    if digits not in (None, "fa", "en"):
        raise ValueError(f"digits must be 'fa', 'en' or None, got {digits!r}")

    text = _PRESENTATION_FORMS.sub(
        lambda m: unicodedata.normalize("NFKC", m.group()), text
    )
    text = text.translate(_CHAR_TABLE)
    if remove_tatweel:
        text = text.replace("ـ", "")
    if remove_diacritics:
        text = strip_diacritics(text)
    if digits == "fa":
        text = to_persian_digits(text)
    elif digits == "en":
        text = to_latin_digits(text)
    text = clean_zwnj(text)
    if fix_spacing:
        text = fix_half_spaces(text)
    if fix_punctuation_marks:
        text = fix_punctuation(text)
    return collapse_whitespace(text)
