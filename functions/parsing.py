import re
from datetime import datetime
from pathlib import Path

import click


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
