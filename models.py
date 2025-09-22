#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def __str__(self):
        text = '\n'.join(self.lines)
        return f'## {self.title}\n\n{text}'


def load_lines(filename):
    with open(filename, 'r', encoding='utf/8') as f_input:
        for line in f_input:
            line = line.rstrip()
            yield line
    return


def load_note_from_file(filename):
    note = Note(filename)
    in_header = False
    header_lines = []
    point = Point(filename)
    for line in load_lines(filename):
        if line == '---' and not header_lines:
            in_header = True
            continue
        if line == '---' and header_lines:
            in_header = False
            note.metadata = yaml.safe_load('\n'.join(header_lines))
            if 'title' in note.metadata:
                note.title = note.metadata['title']
            continue
        if in_header:
            header_lines.append(line)
        else:
            if line.startswith('## '):
                point = Point(line[3:])
                note.content.append(point)
            else:
                point.add_line(line)
    return note
