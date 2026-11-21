import datetime

import pytest

from pertext import (
    format_jalali,
    gregorian_to_jalali,
    is_jalali_leap,
    jalali_month_length,
    jalali_to_gregorian,
)

KNOWN_DATES = [
    ((2026, 11, 20), (1405, 8, 29)),
    ((2026, 3, 21), (1405, 1, 1)),
    ((2025, 3, 21), (1404, 1, 1)),
    ((2025, 3, 20), (1403, 12, 30)),  # last day of a leap year
    ((2024, 3, 20), (1403, 1, 1)),
    ((2000, 1, 1), (1378, 10, 11)),
    ((1979, 2, 11), (1357, 11, 22)),
]


@pytest.mark.parametrize("gregorian, jalali", KNOWN_DATES)
def test_known_dates_both_directions(gregorian, jalali):
    assert gregorian_to_jalali(*gregorian) == jalali
    assert jalali_to_gregorian(*jalali) == gregorian


def test_round_trip_every_day_1900_to_2100():
    day = datetime.date(1900, 1, 1)
    end = datetime.date(2100, 12, 31)
    while day <= end:
        jalali = gregorian_to_jalali(day.year, day.month, day.day)
        assert jalali_to_gregorian(*jalali) == (day.year, day.month, day.day)
        day += datetime.timedelta(days=1)


def test_consecutive_days_advance_by_one():
    day = datetime.date(1990, 1, 1)
    previous = gregorian_to_jalali(day.year, day.month, day.day)
    for _ in range(366 * 60):
        day += datetime.timedelta(days=1)
        current = gregorian_to_jalali(day.year, day.month, day.day)
        py, pm, pd = previous
        allowed = {(py, pm, pd + 1), (py, pm + 1, 1), (py + 1, 1, 1)}
        assert current in allowed
        previous = current


@pytest.mark.parametrize("year", [1399, 1403, 1408])
def test_leap_years(year):
    assert is_jalali_leap(year)
    assert jalali_month_length(year, 12) == 30


@pytest.mark.parametrize("year", [1400, 1401, 1402, 1404, 1405])
def test_common_years(year):
    assert not is_jalali_leap(year)
    assert jalali_month_length(year, 12) == 29


@pytest.mark.parametrize(
    "month, length", [(1, 31), (6, 31), (7, 30), (11, 30)]
)
def test_month_lengths(month, length):
    assert jalali_month_length(1405, month) == length


@pytest.mark.parametrize(
    "args",
    [(2025, 2, 29), (2026, 13, 1), (2026, 0, 10), (2026, 4, 31), (2026, 1, 0)],
)
def test_invalid_gregorian_dates(args):
    with pytest.raises(ValueError):
        gregorian_to_jalali(*args)


@pytest.mark.parametrize(
    "args",
    [(1405, 12, 30), (1405, 13, 1), (1405, 7, 31), (1405, 1, 32), (1405, 0, 1)],
)
def test_invalid_jalali_dates(args):
    with pytest.raises(ValueError):
        jalali_to_gregorian(*args)


def test_format():
    assert format_jalali(1405, 8, 29) == "1405/08/29"
    assert format_jalali(1405, 1, 5) == "1405/01/05"
    assert format_jalali(1405, 8, 29, long=True) == "29 آبان 1405"
