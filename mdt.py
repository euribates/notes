#!/usr/bin/env python

from pathlib import Path
from typing import Optional
import os
import re

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import typer

from models import load_note_from_file

DOCS = Path('./docs')

app = typer.Typer()


def get_title(filename: str) -> Optional[str]:
    pat_title = re.compile('^title: (.+)$')
    with open(filename, 'r', encoding="utf-8") as f_in:
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


def read_all_lines(filename: str) -> list:
    if filename.exists():
        with open(filename, 'r', encoding='utf-8') as f_in:
            return [line.strip() for line in f_in.readlines()]
    return []



@app.command()
def search(topic_name:str, query: str):
    '''Búsqueda de términos en un determinado tema.
    '''
    console = Console()
    filename = DOCS / f'notes-on-{topic_name.lower()}.md'
    console.print(f"Buscando «[b][green]{query}[/green][/b]» en {filename}")
    if filename.exists():
        pat = re.compile(query, re.IGNORECASE)
        entry_name = None
        parrafo = []
        lines = read_all_lines(filename)
        while lines:
            line = lines.pop(0)
            if line.startswith('##'):
                parrafo = []
                level, entry_name = line.strip().split(' ', 1)
            else:
                if line == '':
                    parrafo = []
                else:
                    parrafo.append(line)
            if pat.search(line):
                console.print('Encontrado!')
                if entry_name:
                    console.print(entry_name, style="b")
                next_line = lines.pop(0)
                while next_line:
                    parrafo.append(next_line)
                    next_line = lines.pop(0)
                console.print(Panel(Markdown("\n".join(parrafo))))



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


@app.command()
def ls(topic_name: str, index: Optional[int] = typer.Argument(None)):
    '''Muestra un listado de notas sobre un tema.
    '''
    filename = DOCS / f'notes-on-{topic_name.lower()}.md'
    if filename.exists():
        note = load_note_from_file(filename)
        console = Console()
        if index is None:
            table = Table(show_header=True, header_style="bold green")
            table.add_column("I", style="dim")
            table.add_column("Note")
            for i, point in enumerate(note.content):
                table.add_row(f'{i}', point.title)
            console.print(table)
        else:
            for i, point in enumerate(note.content):
                if i == index:
                    console.print(Panel(Markdown(str(point))))


if __name__ == '__main__':
    app()
