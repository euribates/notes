---
title: Notas sobre Fpdf2
tags:
    - python
    - pdf
---

## Qué es FPDF2

**Fpdf2** es una librería de creación de documentos PDF
escrita en Python.

## Cómo haer un ejemplo básico con FPDF2

Empecemos con el ejemplo clásico:

```python
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", style="B", size=16)
pdf.cell(40, 10, "Hello World!")
pdf.output("tuto1.pdf")
```

Primero creamos un objeto `FPDF`. El constructor FPDF es usado aquí con
los valores predeterminados: Las páginas en A4 vertical y la
unidad de medida en milímetros. Podría haberse especificado
explícitamente con:

```python
pdf = FPDF(orientation="P", unit="mm", format="A4")
```

Es posible configurar el PDF en modo horizontal (`L`) o usar otros
formatos de página como carta (`Letter`) y oficio (`Legal`) y unidades de
medida (`pt`, `cm`, `in`).

Tenemos que agregar una página con `add_page`. El origen es la esquina
superior izquierda y la posición actual está ubicada por defecto a 1 cm
de los bordes; los márgenes pueden ser cambiados con `set_margins`.

Antes de que podamos imprimir texto, es obligatorio seleccionar una
fuente con set_font, de lo contrario, el documento sería inválido.
Elegimos helvetica en negrita 16:

pdf.set_font('Helvetica', style='B', size=16)

Podríamos haber especificado cursiva con `I`, subrayado con `U` o fuente
regular con una cadena de texto vacía (o cualquier combinación). Nota
que el tamaño de la fuente es dado en puntos, no en milímetros (u otra
unidad de medida del usuario); ésta es la única excepción. Las otras
fuentes estándar son **Times**, **Courier**, **Symbol** y
**ZapfDingbats**.


