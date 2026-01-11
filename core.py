#!/usr/bin/env python

from pathlib import Path
from typing import Optional
from collections import defaultdict
import argparse
import glob
import yaml
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
    return name.startswith('notes-on-') and name.endswith('.rst')


def get_metadata(filename: str) -> dict:
    pat_tags = re.compile('^.. :tags: *(.+)$')
    result = {}
    with open(filename, 'r', encoding="utf-8") as f_in:
        for line in f_in:
            line = line.rstrip()
            if 'title' not in result:
                result['title'] = line
            if m := pat_tags.match(line):
                result['tags'] = [_.strip() for _ in m.group(1).split(',')]
    return result


def get_title(filename: str) -> Optional[str]:
    with open(filename, 'r', encoding="utf-8") as f_in:
        for line in f_in:
            line = line.rstrip()
            return line


def main_topic(filename: str|Path) -> str:
    if not isinstance(filename, Path):
        filename = Path(filename)
    assert is_note(filename)
    name = filename.name
    return name.removeprefix("notes-on-").removesuffix('.rst')


def read_all_lines(filename: str) -> list:
    if filename.exists():
        with open(filename, 'r', encoding='utf-8') as f_in:
            return [line.strip() for line in f_in.readlines()]
    return []
