#!/usr/bin/env python

from pathlib import Path
from typing import Optional
import os
import re

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
import typer


DOCS = Path('./docs')

app = typer.Typer()


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


def main_topic(filename: str|Path) -> str:
    if not isinstance(filename, Path):
        filename = Path(filename)
    assert is_note(filename)
    name = filename.name
    return name.removeprefix("notes-on-").removesuffix('.md')


@app.command()
def topics():
    '''Muestra un listado de todos las temas disponibles.
    '''
    console = Console()
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Topic", style="dim")
    table.add_column("Title")
    for filename in DOCS.iterdir():
        if is_note(filename):
            title = get_title(filename)
            topic = main_topic(filename)
            table.add_row(topic, title)
    console.print(table)


@app.command()
def search(query: str):
    print('Search')


@app.command()
def topic(topic_name: str):
    '''Muestra un listado de .
    '''
    filename = DOCS / f'notes-on-{topic_name.lower()}.md'
    if filename.exists():
        console = Console()
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Topic", style="dim")
        table.add_column("Note")
        with open(filename, 'r', encoding='utf-8') as f_in:
            for line in f_in.readlines():
                if line.startswith('##'):
                    level, entry_name = line.strip().split(' ', 1)
                    table.add_row(topic_name, Markdown(entry_name))
        console.print(table)


if __name__ == '__main__':
    app()
