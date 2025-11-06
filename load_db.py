#!/usr/bin/env python

from pathlib import Path
from typing import Optional
import sqlite3
import re

from models import load_note_from_file

DOCS = Path('./source/')

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


def save_note_to_database(db, pk, topic, title, body):
    cur = db.cursor()
    sql = (
        "INSERT INTO note ("
        "    id_note,"
        "    topic,"
        "    title,"
        "    body) VALUES ("
        "    :id_note,"
        "    :topic,"
        "    :title,"
        "    :body)"
        )
    cur.execute(sql, {
        'id_note': pk,
        'topic': topic,
        'title': title,
        'body': body,
        })



def main():
    pk = 1
    db = sqlite3.connect("notes.db")
    for filename in sorted(DOCS.iterdir()):
        if is_note(filename):
            # title = get_title(filename)
            topic = main_topic(filename)
            filename = DOCS / f'notes-on-{topic}.md'
            note = load_note_from_file(filename)
            for i, point in enumerate(note.content):
                print(f'{topic} {i} {point.title}', end=' ')
                save_note_to_database(
                    db, 
                    pk,
                    topic,
                    point.title,
                    point.body(),
                    )
                pk += 1
                print(f"[{pk}]")
    db.commit()


if __name__ == '__main__':
    main()


