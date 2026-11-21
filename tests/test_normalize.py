import pytest

from pertext import ZWNJ, normalize, strip_diacritics, to_latin_digits, to_persian_digits


def test_arabic_letters_become_persian():
    assert normalize("كتاب") == "کتاب"
    assert normalize("عربي") == "عربی"
    assert normalize("مصطفى") == "مصطفی"


def test_digit_conversion():
    assert to_persian_digits("2026 ٢٠٢٦") == "۲۰۲۶ ۲۰۲۶"
    assert to_latin_digits("۱۴۰۵ ١٤٠٥") == "1405 1405"
    assert normalize("سال 1405", digits="fa") == "سال ۱۴۰۵"
    assert normalize("سال ۱۴۰۵", digits="en") == "سال 1405"
    assert normalize("سال 1405") == "سال 1405"


def test_invalid_digits_option():
    with pytest.raises(ValueError):
        normalize("متن", digits="ar")  # type: ignore[arg-type]


def test_diacritics_and_tatweel():
    assert strip_diacritics("مُحَمَّد") == "محمد"
    assert normalize("مُحَمَّد") == "محمد"
    assert normalize("سلاـــم") == "سلام"
    assert normalize("مُحَمَّد", remove_diacritics=False) == "مُحَمَّد"


def test_half_space_after_verb_prefix():
    assert normalize("می خواهم") == "می" + ZWNJ + "خواهم"
    assert normalize("نمی دانم") == "نمی" + ZWNJ + "دانم"


def test_half_space_before_suffixes():
    assert normalize("کتاب ها") == "کتاب" + ZWNJ + "ها"
    assert normalize("بزرگ ترین") == "بزرگ" + ZWNJ + "ترین"
    assert normalize("خانه های قدیمی") == "خانه" + ZWNJ + "های قدیمی"


def test_half_space_leaves_unrelated_words_alone():
    assert normalize("او می") == "او می"
    assert normalize("تماشا کردم") == "تماشا کردم"
    assert normalize("کتاب های") == "کتاب" + ZWNJ + "های"
    assert normalize("کتابها") == "کتابها"


def test_spacing_can_be_disabled():
    assert normalize("می خواهم", fix_spacing=False) == "می خواهم"


def test_persian_punctuation():
    assert normalize("سلام, چطوری?") == "سلام، چطوری؟"
    assert normalize("بله; خوب") == "بله؛ خوب"


def test_latin_punctuation_is_untouched():
    assert normalize("what? yes, ok;") == "what? yes, ok;"
    assert normalize("example.com/?q=1") == "example.com/?q=1"


def test_punctuation_can_be_disabled():
    assert normalize("سلام, چطوری?", fix_punctuation_marks=False) == "سلام, چطوری?"


def test_zwnj_cleanup():
    assert normalize("کتاب" + ZWNJ * 3 + "ها") == "کتاب" + ZWNJ + "ها"
    assert normalize(ZWNJ + "کتاب" + ZWNJ) == "کتاب"
    # A stray ZWNJ before a space is dropped, then the suffix rule restores it.
    assert normalize("کتاب" + ZWNJ + " ها") == "کتاب" + ZWNJ + "ها"


def test_arabic_presentation_forms():
    assert normalize("ﻛﺘﺎﺏ") == "کتاب"


def test_whitespace_collapsing():
    assert normalize("  سلام   دنیا ! ") == "سلام دنیا !"
    assert normalize("خط اول \n خط دوم") == "خط اول\nخط دوم"


def test_empty_string():
    assert normalize("") == ""


@pytest.mark.parametrize(
    "sample",
    [
        "من كتاب ها را می خوانم, اما نمی دانم?",
        "مُحَمَّد  بزرگ ترین  بود",
        "سال 2026 ٢٠٢٦",
        "plain ASCII text, nothing to do?",
    ],
)
def test_normalize_is_idempotent(sample):
    once = normalize(sample, digits="fa")
    assert normalize(once, digits="fa") == once


def test_latin_letters_and_urls_are_not_rewritten():
    assert normalize("see https://example.com/a?b=1, ok") == "see https://example.com/a?b=1, ok"
    assert normalize("Hello,   World;") == "Hello, World;"  # whitespace still collapsed


def test_tatweel_kept_when_requested_does_not_break_spacing():
    assert normalize("کتــاب ها", remove_tatweel=False) == "کتــاب" + ZWNJ + "ها"


def test_words_that_only_look_like_verb_prefixes_are_untouched():
    assert normalize("میز بزرگ") == "میز بزرگ"
    assert normalize("نمیر") == "نمیر"
