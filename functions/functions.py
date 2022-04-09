import re
from datetime import datetime
from typing import Any

import click

from functions.parsing import date_convert, full_echo


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


def unwanted_search(unwanted: str, lines: dict, full: Any):
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
