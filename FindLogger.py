from pathlib import Path
from typing import Any

import click

from functions_log.functions import (search_date, search_date_text,
                                     search_range_date, search_text,
                                     unwanted_search)
from functions_log.parsing import date_convert, full_echo, path_open


def logger_analyze(path: Path, text: str, date: str, unwanted: str, full: Any) -> Any:
    """
    Path to Logs and search text and date
    """
    lines = path_open(path)
    if not text and not date and not unwanted:
        for key, value in lines.items():
            full_echo(key, value, full)
    if text and not date and not unwanted:
        return search_text(text, lines, full)
    if not text and not unwanted and date:
        count = 0
        if date.endswith("/.."):
            date = date_convert(date[:-3])
            for key, value in lines.items():
                if key >= date:
                    count += 1
                    search_range_date(key, value, full)
            if count == 0:
                return click.secho(
                    "This date range was not detected", fg="red", bold=True
                )
        elif date[:3] == "../":
            date = date_convert(date[3:])
            for key, value in lines.items():
                if key <= date:
                    count += 1
                    search_range_date(key, value, full)
            if count == 0:
                return click.secho(
                    "This date range was not detected", fg="red", bold=True
                )
        elif len(date) > 26 and date[26] == "/":
            date_start = date_convert(date[:26])
            date_end = date_convert(date[27:])
            for key, value in lines.items():
                if date_start <= key <= date_end:
                    count += 1
                    search_range_date(key, value, full)
            if count == 0:
                return click.secho(
                    "This date range was not detected", fg="red", bold=True
                )
        else:
            return search_date(date, lines, full)
    if text and date and not unwanted:
        return search_date_text(date, text, lines, full)
    if unwanted:
        return unwanted_search(unwanted, lines, full)


@click.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, path_type=Path
    ),
    nargs=1,
    required=True,
)
@click.option("--text", "-t", "--Text", "--TEXT", help="To find the text in the Logs")
@click.option("--date", "-d", "--Date", "--DATE", help="To find the date in the Logs")
@click.option(
    "--unwanted",
    "-n",
    "--Unwanted",
    "--UNWANTED",
    "unwanted",
    help="A text to filter out logs. Logs with this text will be excluded from the results.",
)
@click.option(
    "--full",
    "--Full",
    "--FULL",
    default=None,
    show_default=True,
    help="Return full log entry unstead of default Qty",
)
def main(path, text, date, unwanted, full):
    """
    This MEGAscript find logs according to the given parametrs
    """
    logger_analyze(path, text, date, unwanted, full)


if __name__ == "__main__":
    main()
