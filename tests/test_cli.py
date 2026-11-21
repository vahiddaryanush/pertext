import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

from pertext.cli import main

SRC = Path(__file__).resolve().parents[1] / "src"


def test_date_gregorian_to_jalali(capsys):
    assert main(["date", "2026-11-20"]) == 0
    assert capsys.readouterr().out.strip() == "1405/08/29"


def test_date_long_format(capsys):
    assert main(["date", "2026-11-20", "--long"]) == 0
    assert capsys.readouterr().out.strip() == "29 آبان 1405"


def test_date_jalali_to_gregorian(capsys):
    assert main(["date", "--jalali", "1405/08/29"]) == 0
    assert capsys.readouterr().out.strip() == "2026-11-20"


def test_date_accepts_persian_digits(capsys):
    assert main(["date", "--jalali", "۱۴۰۵/۰۸/۲۹"]) == 0
    assert capsys.readouterr().out.strip() == "2026-11-20"


def test_date_today_runs(capsys):
    assert main(["date", "today"]) == 0
    assert capsys.readouterr().out.count("/") == 2


def test_invalid_date_reports_error(capsys):
    assert main(["date", "2026-02-30"]) == 1
    captured = capsys.readouterr()
    assert "invalid Gregorian date" in captured.err
    assert captured.out == ""


def test_garbage_date_reports_error(capsys):
    assert main(["date", "not-a-date"]) == 1
    assert "expected a date" in capsys.readouterr().err


def test_normalize_from_file(tmp_path, capsys):
    source = tmp_path / "in.txt"
    source.write_text("می خواهم 2026", encoding="utf-8")
    assert main(["normalize", str(source), "--digits", "fa"]) == 0
    assert capsys.readouterr().out.strip() == "می‌خواهم ۲۰۲۶"


def test_normalize_from_stdin(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO("كتاب ها"))
    assert main(["normalize"]) == 0
    assert capsys.readouterr().out.strip() == "کتاب‌ها"


def test_normalize_to_output_file(tmp_path):
    source = tmp_path / "in.txt"
    target = tmp_path / "out.txt"
    source.write_text("سلام, دنیا", encoding="utf-8")
    assert main(["normalize", str(source), "-o", str(target)]) == 0
    assert target.read_text(encoding="utf-8") == "سلام، دنیا\n"


def test_missing_file_reports_error(tmp_path, capsys):
    assert main(["normalize", str(tmp_path / "missing.txt")]) == 1
    assert "pertext: error" in capsys.readouterr().err


def test_command_is_required():
    with pytest.raises(SystemExit):
        main([])


def test_module_entry_point():
    env = dict(os.environ, PYTHONPATH=str(SRC), PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "pertext", "date", "2026-03-21"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "1405/01/01"
