"""pertext: zero-dependency Persian text normalization and Jalali dates."""

__version__ = "0.1.0"

from .jalali import (
    JALALI_MONTHS,
    format_jalali,
    gregorian_to_jalali,
    is_jalali_leap,
    jalali_month_length,
    jalali_to_gregorian,
)
from .normalize import (
    ZWNJ,
    normalize,
    strip_diacritics,
    to_latin_digits,
    to_persian_digits,
)

__all__ = [
    "JALALI_MONTHS",
    "ZWNJ",
    "__version__",
    "format_jalali",
    "gregorian_to_jalali",
    "is_jalali_leap",
    "jalali_month_length",
    "jalali_to_gregorian",
    "normalize",
    "strip_diacritics",
    "to_latin_digits",
    "to_persian_digits",
]
