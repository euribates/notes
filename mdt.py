#!/usr/bin/env python

from pathlib import Path
from typing import Optional
import argparse
import glob
import json
import re

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from models import load_note_from_file

DOCS = Path('./source/')

OK = "[green]✓[/green]"
ERROR = "[red]✖[/red]"


def is_note(filename: str|Path) -> bool:
    filename = Path(filename)
    name = filename.name
    return name.startswith('notes-on-') and name.endswith('.md')


def get_title(filename: str) -> Optional[str]:
    pat_title = re.compile('^title: (.+)$')
    with open(filename, 'r', encoding="utf-8") as f_in:
        for line in f_in:
            if _match := pat_title.match(line):
                return _match.group(1)
    return None


def main_topic(filename: str|Path) -> str:
    if not isinstance(filename, Path):
        filename = Path(filename)
    assert is_note(filename)
    name = filename.name
    return name.removeprefix("notes-on-").removesuffix('.md')


def read_all_lines(filename: str) -> list:
    if filename.exists():
        with open(filename, 'r', encoding='utf-8') as f_in:
            return [line.strip() for line in f_in.readlines()]
    return []


class Handler:

    def __init__(self):
        self.console = Console()

    def out(self, *args, **kwargs):
        self.console.print(*args, *kwargs)

    def success(self, msg=''):
        if msg:
            self.out(f'{OK} [bold]{msg}[/]')
        else:
            self.out(OK)

    def failure(self, msg):
        self.out(f"{ERROR} [red bold]{msg}[/]")

    def get_parser(self):
        parser = argparse.ArgumentParser(
            prog='[green]✎[/green] notas.py',
            description='Gestión de notas',
            )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Muestra información del proceso',
            )
        subparsers = parser.add_subparsers(help='Ayudas de las ordenes')
        parser_ls = subparsers.add_parser('ls', help='Listar temas y notas')
        parser_ls.add_argument('topic', action='store', nargs='?')
        parser_ls.add_argument('indexes', action='store', type=int, nargs='*')
        parser_ls.set_defaults(func=self.cmd_ls)
        # Search
        parser_search = subparsers.add_parser(
            'search',
            help='Buscar en notas',
            )
        parser_search.add_argument('query', action='store')
        parser_search.add_argument('--topic', nargs='*')
        parser_search.set_defaults(func=self.cmd_search)
        # Export
        parser_export = subparsers.add_parser(
            'export',
            help='Exportar notas',
            )
        parser_export.add_argument('--topic', nargs='*')
        parser_export.set_defaults(func=self.cmd_export)
        return parser

    def cmd_ls(self, options):
        '''Muestra un listado de todos las temas disponibles.
        '''
        topic = options.topic.lower() if options.topic else ''
        if not topic:
            table = Table(title='Temas', show_header=True)
            table.add_column("Topic", style="dim")
            table.add_column("Title")
            for filename in sorted(DOCS.iterdir()):
                if is_note(filename):
                    title = get_title(filename)
                    topic = main_topic(filename)
                    table.add_row(topic, title)
            self.out(table)
            return -1
        filename = DOCS / f'notes-on-{topic}.md'
        if not filename.exists():
            self.failure(f'NO existe el tema [yellow]{topic}[/]')
            return -1
        table = Table(title=topic, show_header=True)
        table.add_column("Index", style="dim")
        table.add_column("Note")
        note = load_note_from_file(filename)
        indexes = options.indexes
        if not indexes:
            for i, point in enumerate(note.content):
                table.add_row(f'{i}', Markdown(point.title))
        else:
            for i, point in enumerate(note.content):
                if i in indexes:
                    table.add_row(f'{i}', Markdown(str(point)))
        self.out(table)
        return 0

    def cmd_search(self, options):
        '''Búsqueda de términos en un determinado tema.
        '''
        query = options.query
        topics = options.topic
        if not topics:
            filenames = DOCS.glob('notes-on-*.md')
            self.out(f"Buscando «[b][green]{query}[/green][/b]»")
        else:
            filenames = [
                DOCS / f'notes-on-{topic.lower()}.md'
                for topic in topics
                ]
            self.out(f"Buscando «[b][green]{query}[/green][/b]» en {topics!r}")
        for filename in filenames:
            if not filename.exists():
                topic = main_topic(filename)
                self.failure(f'NO existe el tema [yellow]{topic}[/]')
                continue
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
                    self.out('Encontrado!')
                    if entry_name:
                        self.out(f'[bold]{entry_name}[/b]')
                    next_line = lines.pop(0)
                    while next_line:
                        parrafo.append(next_line)
                        next_line = lines.pop(0)
                    self.out(Panel(Markdown("\n".join(parrafo))))
        return 0

    def cmd_export(self, options):
        '''Exporta un tema en formato JSON.
        '''
        outcome = []
        for topic in options.topic:
            filename = DOCS / f'notes-on-{topic.lower()}.md'
            if not filename.exists():
                self.failure(f'NO existe el tema [yellow]{topic}[/]')
                return -1
            note = load_note_from_file(filename)
            outcome.append(note)
        self.out(json.dumps(outcome))
        return 0

    def run(self):
        parser = self.get_parser()
        args = parser.parse_args()
        args.func(args)


if __name__ == '__main__':
    handler = Handler()
    handler.run()


