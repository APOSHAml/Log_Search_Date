import pytest

from ..FindLogger import (date_convert, path_open, search_date,
                                      search_date_text, search_text)
from .data_test.data_testing import *


@pytest.mark.parametrize(
    "path_log,expected",
    [
        [Path("./data_test/happy.log"), lines_dict],
        [Path("../tests"), lines_dict],
        [Path("./data_test/unhappy_invalid.log"), {}],
    ],
)
def test_open_path(path_log: Path, expected: dict[datetime, str]) -> None:
    assert path_open(path_log) == expected


def test_empty_dir(tmpdir: str) -> None:
    assert path_open(Path(tmpdir)) == {}


def test_invalid_path():
    with pytest.raises(UnicodeDecodeError):
        path_open(unhappy_log)


def test_happy_convert() -> None:
    assert date_convert("2022-02-03 00:01:13.623000") == datetime(
        2022, 2, 3, 0, 1, 13, 623000
    )


def test_unhappy_convert() -> None:
    with pytest.raises(ValueError):
        date_convert("2022-02-03")


@pytest.mark.parametrize(
    "text, lines, expected",
    [
        ["Error", lines_dict, search_happy],
        ["olololo", lines_dict, "The text not found\n"],
    ],
)
def test_search_text(capfd, text: str, lines: dict, expected: str) -> None:
    search_text(text, lines, None)
    captured = capfd.readouterr()
    assert captured.out == expected


@pytest.mark.parametrize(
    "dates, lines, expected",
    [
        ["2022-02-03 00:01:13.623000", lines_dict, search_happy[:56]],
        ["2999-02-03 00:01:13.623000", lines_dict, date_no_found],
    ],
)
def test_search_date(capfd, dates: str, lines: dict, expected: str) -> None:
    search_date(dates, lines, None)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_unhappy_serch_date() -> None:
    with pytest.raises(ValueError):
        search_date("2022-02-03 00:0113.623000", lines_dict, None)


@pytest.mark.parametrize(
    "dates, text, lines, expected",
    [
        ["2022-04-07 00:08:13.922000", "Error", lines_dict, search_happy[56:]],
        ["2999-02-03 00:01:13.623000", "Error", lines_dict, "The date not found\n"],
    ],
)
def test_search_date_text(
    capfd, dates: str, text: str, lines: dict, expected: str
) -> None:
    search_date_text(dates, text, lines, None)
    captured = capfd.readouterr()
    assert captured.out == expected
