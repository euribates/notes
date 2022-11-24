#!/usr/bin/env python

import os
import re
from typing import Optional
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table


DOCS = Path('./docs')


def get_title(filename: str) -> Optional[str]:
    pat_title = re.compile('^title: (.+)$')
    with open(filename, 'r') as f_in:
        for line in f_in:
            if _match := pat_title.match(line):
                return _match.group(1)
    return None


def is_note(filename: str|Path) -> bool:
    if not isinstance(filename, Path):
        filename = Path(filename)
    name = filename.name
    return name.startswith('notes-on-') and name.endswith('.md')


def main_topic(filename:str|Path):
    if not isinstance(filename, Path):
        filename = Path(filename)
    assert is_note(filename)
    name = filename.name
    return name.removeprefix("notes-on-").removesuffix('.md')

@click.group()
def mdt():
    pass


@click.command()
def notes():
    console = Console()
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Topic", style="dim", width=24)
    table.add_column("Title")
    for filename in DOCS.iterdir():
        if is_note(filename):
            title = get_title(filename)
            topic = main_topic(filename)
            table.add_row(topic, title)
    console.print(table)


@click.command()
def search():
    click.echo('Search')


if __name__ == '__main__':
    mdt.add_command(notes)
    mdt.add_command(search)
    mdt()
