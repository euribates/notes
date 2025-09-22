#!/usr/bin/env python

import sys
from pathlib import Path
from typing import Optional
import argparse
import glob
import json
import re

from fpdf import FPDF
import markdown
import markdown.extensions

from models import load_note_from_file

def main():
    topic = sys.argv[1]
    input_filename = Path(f'source/notes-on-{topic}.md')
    nota = load_note_from_file(input_filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(
        'NotoSans',
        style='',
        fname='./fonts/NotoSans-Regular.ttf',
        )
    pdf.add_font(
        'NotoSans',
        style='I',
        fname='./fonts/NotoSans-Italic.ttf',
        )
    pdf.add_font(
        'NotoSans',
        style='B',
        fname='./fonts/NotoSans-Bold.ttf',
        )
    pdf.add_font(
        'NotoSans',
        style='BI',
        fname='./fonts/NotoSans-BoldItalic.ttf',
        )
    pdf.set_font('NotoSans', size=16)
    pdf.cell(text=nota.title)
    pdf.set_font('NotoSans', size=14)
    if 'tags' in nota.metadata:
        pdf.ln(12)
        pdf.set_fill_color(255, 255, 0)
        for value in nota.metadata['tags']:
            pdf.cell(text=value, border="LRTB", fill=True)
            pdf.cell(text=' ')
    pdf.ln(12)
    pdf.set_font('NotoSans', size=16)
    pdf.cell(text='Sumario', align='C')
    pdf.ln(12)
    pdf.set_font('NotoSans', size=10)
    for part in nota.content:
        pdf.cell(text=part.title, markdown=True)
        pdf.ln()

    for part in nota.content:
        pdf.add_page()
        pdf.write_html(
            markdown.markdown(
                str(part),
                extensions=['fenced_code'],
                ),
            font_family="NotoSans",
            )


    output_filename = Path(f'notes-on-{topic}.pdf')
    print(f"Generando {output_filename}", end="...")
    pdf.output(output_filename)
    print("[OK]")


if __name__ == "__main__":
    main()
