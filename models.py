#!/usr/bin/env python3

import re
import yaml


class Note:

    def __init__(self, filename, title=''):
        self.filename = filename
        self.title = title or filename
        self.metadata = {}
        self.content = []


class Point:

    def __init__(self, title):
        self.title = title
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def pop(self):
        return self.lines.pop()

    def body(self):
        return '\n'.join(self.lines)

    def __str__(self):
        return f'## {self.title}\n\n{self.body()}'


def load_lines(filename):
    with open(filename, 'r', encoding='utf/8') as f_input:
        for line in f_input:
            line = line.rstrip()
            yield line
    return


def load_note_from_file(filename):
    pat_point = re.compile('^----+$')
    note = Note(filename)
    point = Point(filename)
    prev_line = None
    for line in load_lines(filename):
        line = line.rstrip()
        if pat_point.match(line):
            assert prev_line == point.pop()
            point = Point(prev_line)
            note.content.append(point)
        else:
            point.add_line(line)
        prev_line = line
    return note
