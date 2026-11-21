"""Command-line interface: ``pertext normalize`` and ``pertext date``."""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List, Optional

from . import __version__
from .jalali import (
    format_jalali,
    gregorian_to_jalali,
    jalali_to_gregorian,
    parse_date,
)
from .normalize import normalize, to_latin_digits


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pertext",
        description="Persian text normalization and Jalali date conversion.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    norm = sub.add_parser("normalize", help="normalize Persian text from a file or stdin")
    norm.add_argument("file", nargs="?", default="-", help="input file (default: stdin)")
    norm.add_argument("--digits", choices=["fa", "en"], help="convert digits to Persian or Latin")
    norm.add_argument("--keep-diacritics", action="store_true", help="do not strip diacritics")
    norm.add_argument("--no-spacing", action="store_true", help="do not insert half-spaces")
    norm.add_argument("--no-punctuation", action="store_true", help="keep , ; ? as they are")
    norm.add_argument("-o", "--output", help="write the result to a file instead of stdout")

    date = sub.add_parser("date", help="convert between Gregorian and Jalali dates")
    date.add_argument("value", help="a date such as 2026-11-20, 1405/08/29, or 'today'")
    date.add_argument("--jalali", action="store_true", help="treat the input as a Jalali date")
    date.add_argument("--long", action="store_true", help="print the Jalali month name")
    return parser


def _read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def _run_normalize(args: argparse.Namespace) -> int:
    result = normalize(
        _read_input(args.file),
        digits=args.digits,
        remove_diacritics=not args.keep_diacritics,
        fix_spacing=not args.no_spacing,
        fix_punctuation_marks=not args.no_punctuation,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(result + "\n")
    else:
        print(result)
    return 0


def _run_date(args: argparse.Namespace) -> int:
    value = to_latin_digits(args.value).strip()
    if args.jalali:
        jy, jm, jd = parse_date(value)
        gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
        print(f"{gy:04d}-{gm:02d}-{gd:02d}")
        return 0
    if value.lower() == "today":
        today = datetime.date.today()
        y, m, d = today.year, today.month, today.day
    else:
        y, m, d = parse_date(value)
    print(format_jalali(*gregorian_to_jalali(y, m, d), long=args.long))
    return 0


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    _configure_stdio()
    args = build_parser().parse_args(argv)
    try:
        if args.command == "normalize":
            return _run_normalize(args)
        return _run_date(args)
    except (OSError, ValueError) as exc:
        print(f"pertext: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
