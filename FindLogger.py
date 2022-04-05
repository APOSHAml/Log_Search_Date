import re
from datetime import datetime
from pathlib import Path
from typing import Any

import click


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
        if date[-3:] == "/..":
            date = date_convert(date[:-3])
            for key, value in lines.items():
                if key >= date:
                    count += 1
                    search_range_date(key, value, lines, full)
            if count == 0:
                return click.secho(
                    "This date range was not detected", fg="red", bold=True
                )
        elif date[:3] == "../":
            date = date_convert(date[3:])
            for key, value in lines.items():
                if key <= date:
                    count += 1
                    search_range_date(key, value, lines, full)
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
                    search_range_date(key, value, lines, full)
            if count == 0:
                return click.secho(
                    "This date range was not detected", fg="red", bold=True
                )
        else:
            return search_date(date, lines, full)
    if text and date and not unwanted:
        return search_date_text(date, text, lines, full)
    if unwanted:
        return unwanted_searh(unwanted, lines, full)


def path_open(path: Path) -> dict:
    lines = {}
    try:
        if path.is_dir():
            find_log_files = path.rglob("*.log")
            for log in find_log_files:
                with log.open() as f:
                    for read_str in f:
                        stroka = read_str.strip()
                        if re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d", stroka):
                            date_time_key = date_convert(stroka[:23])
                            lines[date_time_key] = stroka[24:]
        else:
            with path.open() as f:
                for read_str in f:
                    stroka = read_str.strip()
                    if re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d", stroka):
                        date_time_key = date_convert(stroka[:23])
                        lines[date_time_key] = stroka[24:]
        return lines
    except Exception as f:
        raise f from f


def date_convert(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception as f:
        raise f from f


def full_echo(key, value, full):
    if full is None:
        if len(value) >= 300:
            click.secho(key, fg="blue", bold=True), click.echo(value[:300])
        else:
            click.secho(key, fg="blue", bold=True), click.echo(value)
    if full in ["FULL", "full", "Full"]:
        click.secho(key, fg="blue", bold=True), click.echo(value)


def search_text(text: str, lines: dict, full: Any):
    text_low = text.lower()
    count = 0
    for key, value in lines.items():
        value_low = value.lower()
        if text_low in value_low:
            count += 1
            list_index = [_.start() for _ in re.finditer(text_low, value_low)]
            for _i in list_index:
                if full is None:
                    if _i < 150:
                        click.secho(key, fg="blue", bold=True)
                        click.echo(value[:_i], nl=False), click.secho(
                            value[_i : _i + len(text)],
                            nl=False,
                            fg="green",
                            bold=True,
                        ), click.echo(value[_i + len(text) : _i + len(text) + 150])
                    elif 150 < _i < (len(value) - 150):
                        click.secho(key, fg="blue", bold=True)
                        click.echo(value[_i - 150 : _i], nl=False), click.secho(
                            value[_i : _i + len(text)],
                            nl=False,
                            fg="green",
                            bold=True,
                        ), click.echo(value[_i + len(text) : _i + len(text) + 150])
                    elif 150 < _i > (len(value) - 150):
                        click.secho(key, fg="blue", bold=True)
                        click.echo(value[_i - 150 : _i], nl=False), click.secho(
                            value[_i : _i + len(text)],
                            nl=False,
                            fg="green",
                            bold=True,
                        ), click.echo(value[_i + len(text) :])
                elif full in ["FULL", "full", "Full"]:
                    click.secho(key, fg="blue", bold=True)
                    click.echo(value[:_i]), click.secho(
                        value[_i : _i + len(text)],
                        nl=False,
                        fg="green",
                        bold=True,
                    ), click.echo(value[_i + len(text) :])
    if count == 0:
        click.secho("The text not found", fg="red", bold=True)


def search_date(date: str, lines: dict, full: Any):
    date = date_convert(date)
    value = lines.get(date, "The date not found")
    return full_echo(date, value, full)


def search_date_text(date: str, text: str, lines: dict, full: Any):
    date = date_convert(date)
    if date in lines:
        value = lines[date]
        value_low = value.lower()
        text_low = text.lower()
        if text_low in value_low:
            list_index = [_.start() for _ in re.finditer(text_low, value_low)]
            for _i in list_index:
                if full is None:
                    if _i < 150:
                        click.secho(date, fg="blue", bold=True)
                        click.echo(value[:_i], nl=False), click.secho(
                            value[_i : _i + len(text)],
                            nl=False,
                            fg="green",
                            bold=True,
                        ), click.echo(value[_i + len(text) : _i + len(text) + 150])
                    elif 150 < _i < (len(value) - 150):
                        click.secho(date, fg="blue", bold=True)
                        click.echo(value[_i - 150 : _i], nl=False), click.secho(
                            value[_i : _i + len(text)],
                            nl=False,
                            fg="green",
                            bold=True,
                        ), click.echo(value[_i + len(text) : _i + len(text) + 150])
                    elif 150 < _i > (len(value) - 150):
                        click.secho(date, fg="blue", bold=True)
                        click.echo(value[_i - 150 : _i], nl=False), click.secho(
                            value[_i : _i + len(text)],
                            nl=False,
                            fg="green",
                            bold=True,
                        ), click.echo(value[_i + len(text) :])
                elif full in ["FULL", "full", "Full"]:
                    click.secho(date, fg="blue", bold=True)
                    click.echo(value[:_i]), click.secho(
                        value[_i : _i + len(text)],
                        nl=False,
                        fg="green",
                        bold=True,
                    ), click.echo(value[_i + len(text) :])
        else:
            click.secho("This text was not found on this date", fg="red", bold=True)
    else:
        click.secho("The date not found", fg="red", bold=True)


def search_range_date(key: datetime, value: str, full: Any):
    return full_echo(key, value, full)


def unwanted_searh(unwanted: str, lines: dict, full: Any):
    count = 0
    for key, value in lines.items():
        try:
            value_split = re.split("\s+", value)
            if unwanted not in value_split:
                count += 1
                full_echo(key, value, full)
        except Exception as f:
            raise f from f
    if count == 0:
        click.secho("This text is found in all logs", fg="red", bold=True)


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
