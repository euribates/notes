#!/usr/bin/env python3

import subprocess
from pathlib import Path
import argparse

import yaml

OK = "\u001b[32m[✓]\u001b[0m"
ERROR = "\u001b[31m[✖]\u001b[0m"

DOCS = Path('./source/')


def get_metadata(filename: str) -> dict:
    '''Devuelve los metadatos de un fichero.
    '''
    with open(filename, 'r', encoding="utf-8") as f_in:
        line = f_in.readline().strip()
        if line == '---': #  YAML header
            buff = []
            for line in f_in:
                line = line.strip()
                if line == '---':
                    break
                buff.append(line)
            else:
                raise ValueError(
                    "Encuentro la marca de inicio de metadata"
                    f" en el fichero {filename}, pero no la marca"
                    " de final."
                    )
            return yaml.safe_load('\n'.join(buff))
    return {}


def check(msg, condition: bool):
    if not condition:
        print(msg, ERROR)
        raise ValueError('No se cumple la condición: {msg}')
    print(msg, OK)


def get_options():
    parser = argparse.ArgumentParser(
        prog="md2rst.py",
        description="Pasar de markdown a restructuredText",
        )
    parser.add_argument('topic')
    return parser.parse_args()


def add_topic(topic, metadata, filename):
    with open(filename, 'r', encoding='utf-8') as f_in:
        lines = [
            line.strip()
            for line in f_in.readlines()
            ]
    with open(filename, 'w', encoding='utf-8') as f_out:
        print(topic, file=f_out)
        print('=' * 72, file=f_out)
        print('', file=f_out)
        if 'tags' in metadata:
            tags = f','.join(metadata['tags'])
            print(f'.. tags:: {tags}', file=f_out)
            print('', file=f_out)
        print('', file=f_out)
        for line in lines:
            print(line, file=f_out)


def _execute(cmd):
    print(*cmd, sep=' ', end='...')
    subprocess.run(cmd, check=True)
    print(OK)


def add_to_git(filename):
    _execute(['git', 'add', str(filename)])


def remove_from_git(filename):
    _execute(['git', 'rm', str(filename)])


def markdown_to_rst(md_filename, rst_filename):
    _execute([
        'pandoc',
        '--from=markdown',
        '--to=rst',
        f'--output={rst_filename}',
        str(md_filename),
        ])


def main():
    options = get_options()
    md_filename = DOCS / f'notes-on-{options.topic}.md'
    rst_filename = DOCS / f'notes-on-{options.topic}.rst'
    check(f'Existe {md_filename.name}', md_filename.exists())
    check(f'No existe {rst_filename.name}', not rst_filename.exists())
    metadata = get_metadata(md_filename)
    if 'tags' in metadata:
        tags = f','.join(metadata['tags'])
        print(f'tags: {tags}')
    markdown_to_rst(md_filename, rst_filename)
    check(f'Existe {rst_filename}', rst_filename.exists())
    add_topic(options.topic, metadata, rst_filename)
    add_to_git(rst_filename)
    remove_from_git(md_filename)

if __name__ == "__main__":
    main()
