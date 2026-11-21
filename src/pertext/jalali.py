"""Gregorian <-> Jalali (Solar Hijri) date conversion using pure arithmetic.

The conversion uses the 33-year arithmetic rule for the Jalali calendar.
The official Iranian calendar is defined astronomically, so an arithmetic
rule can differ from it in some years. This module has not been verified
against an independent astronomical reference; it is checked against known
dates (Nowruz and leap years) and by round-trip tests. Years must be in
1-9999; accuracy outside the modern era is not guaranteed.
"""

from __future__ import annotations

from typing import Tuple

DateTuple = Tuple[int, int, int]

_G_DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)

JALALI_MONTHS = (
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
)


def is_gregorian_leap(year: int) -> bool:
    """Return True if ``year`` is a Gregorian leap year."""
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def gregorian_to_jalali(gy: int, gm: int, gd: int) -> DateTuple:
    """Convert a Gregorian date to a Jalali ``(year, month, day)`` tuple."""
    _validate_gregorian(gy, gm, gd)
    gy2 = gy + 1 if gm > 2 else gy
    days = (
        355666
        + 365 * gy
        + (gy2 + 3) // 4
        - (gy2 + 99) // 100
        + (gy2 + 399) // 400
        + gd
        + _G_DAYS_BEFORE_MONTH[gm - 1]
    )
    jy = -1595 + 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + days % 31
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + (days - 186) % 30
    return jy, jm, jd


def jalali_to_gregorian(jy: int, jm: int, jd: int) -> DateTuple:
    """Convert a Jalali date to a Gregorian ``(year, month, day)`` tuple."""
    _validate_jalali(jy, jm, jd)
    return _jalali_to_gregorian_unchecked(jy, jm, jd)


def _jalali_to_gregorian_unchecked(jy: int, jm: int, jd: int) -> DateTuple:
    jy += 1595
    days = -355668 + 365 * jy + (jy // 33) * 8 + ((jy % 33) + 3) // 4 + jd
    days += (jm - 1) * 31 if jm < 7 else (jm - 7) * 30 + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += (days - 1) // 365
        days = (days - 1) % 365
    gd = days + 1
    month_lengths = (
        0, 31, 29 if is_gregorian_leap(gy) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31,
    )
    gm = 0
    while gm < 12 and gd > month_lengths[gm]:
        gd -= month_lengths[gm]
        gm += 1
    return gy, gm, gd


def is_jalali_leap(jy: int) -> bool:
    """Return True if Jalali year ``jy`` has 366 days (Esfand has 30 days)."""
    gy, gm, gd = _jalali_to_gregorian_unchecked(jy, 12, 30)
    return gregorian_to_jalali(gy, gm, gd) == (jy, 12, 30)


def jalali_month_length(jy: int, jm: int) -> int:
    """Return the number of days in a Jalali month."""
    if not 1 <= jm <= 12:
        raise ValueError(f"invalid Jalali month: {jm}")
    if jm <= 6:
        return 31
    if jm <= 11:
        return 30
    return 30 if is_jalali_leap(jy) else 29


def format_jalali(jy: int, jm: int, jd: int, *, long: bool = False) -> str:
    """Format as ``1405/08/29`` or, with ``long=True``, ``29 آبان 1405``.

    Raises ``ValueError`` for an invalid Jalali date.
    """
    _validate_jalali(jy, jm, jd)
    if long:
        return f"{jd} {JALALI_MONTHS[jm - 1]} {jy}"
    return f"{jy:04d}/{jm:02d}/{jd:02d}"


def parse_date(text: str) -> DateTuple:
    """Parse ``YYYY-MM-DD`` or ``YYYY/MM/DD`` into an integer tuple."""
    parts = text.strip().replace("/", "-").split("-")
    if len(parts) != 3 or not all(p.isascii() and p.isdigit() for p in parts):
        raise ValueError(f"expected a date like YYYY-MM-DD or YYYY/MM/DD, got: {text!r}")
    y, m, d = (int(p) for p in parts)
    return y, m, d


MIN_YEAR = 1
MAX_YEAR = 9999


def _validate_gregorian(y: int, m: int, d: int) -> None:
    if not MIN_YEAR <= y <= MAX_YEAR:
        raise ValueError(f"year out of supported range ({MIN_YEAR}-{MAX_YEAR}): {y}")
    if not 1 <= m <= 12:
        raise ValueError(f"invalid Gregorian month: {m}")
    lengths = (31, 29 if is_gregorian_leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not 1 <= d <= lengths[m - 1]:
        raise ValueError(f"invalid Gregorian date: {y}-{m:02d}-{d:02d}")


def _validate_jalali(y: int, m: int, d: int) -> None:
    if not MIN_YEAR <= y <= MAX_YEAR:
        raise ValueError(f"year out of supported range ({MIN_YEAR}-{MAX_YEAR}): {y}")
    if not 1 <= m <= 12:
        raise ValueError(f"invalid Jalali month: {m}")
    if not 1 <= d <= jalali_month_length(y, m):
        raise ValueError(f"invalid Jalali date: {y}/{m:02d}/{d:02d}")
