"""Reference dates for the Jalali conversion.

These are well-known calendar facts (Nowruz dates and officially observed leap
years), written down independently of the algorithm. They are not a substitute
for checking against an astronomical calendar, but they catch systematic errors
that a round-trip test cannot.
"""

import pytest

from pertext import gregorian_to_jalali, is_jalali_leap, jalali_to_gregorian

# (Jalali year, Gregorian date of 1 Farvardin)
NOWRUZ = [
    (1300, (1921, 3, 21)),
    (1394, (2015, 3, 21)),
    (1395, (2016, 3, 20)),
    (1398, (2019, 3, 21)),
    (1399, (2020, 3, 20)),
    (1400, (2021, 3, 21)),
    (1401, (2022, 3, 21)),
    (1402, (2023, 3, 21)),
    (1403, (2024, 3, 20)),
    (1404, (2025, 3, 21)),
    (1405, (2026, 3, 21)),
]

LEAP_YEARS = [1375, 1379, 1383, 1387, 1391, 1395, 1399, 1403, 1408]
COMMON_YEARS = [1376, 1377, 1378, 1380, 1396, 1397, 1398, 1400, 1401, 1402, 1404, 1405, 1406, 1407]


@pytest.mark.parametrize("jyear, gdate", NOWRUZ)
def test_nowruz_dates(jyear, gdate):
    assert jalali_to_gregorian(jyear, 1, 1) == gdate
    assert gregorian_to_jalali(*gdate) == (jyear, 1, 1)


@pytest.mark.parametrize("year", LEAP_YEARS)
def test_known_leap_years(year):
    assert is_jalali_leap(year)


@pytest.mark.parametrize("year", COMMON_YEARS)
def test_known_common_years(year):
    assert not is_jalali_leap(year)
