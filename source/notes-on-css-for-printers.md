---
title: Notas sobre CSS para impresoras
tags:
    - html
    - css
    - web
    - print
---

## Cómo definir el tamaño y la orientación del papel

Definir el tamaño físico del papel es básico. Para ello usamos
el atributo `@page`, que nos permite especificar el tamaño del papel, márgenes,
color de fondo y otras propiedades. Además, se pueden configurar páginas
individuales, como la primera, la última, páginas pares e impares, etc.

Se pueden usar diferentes medidas estandar para especificar el tamaño
del palelÑ

- `A5` (148mm x 210mm)
- `A4` (210mm x 297mm, el tamaño por defecto)
- `A3` (297mm x 420mm)
- `B3` (353mm x 500mm)
- `B4` (250mm x 353mm)
- `JIS-B4` (257mm x 364mm)
- `letter` (8.5in x 11in)
- `legal` (8.5in x 14in)
- `ledger` (11in x 17in)

O, si fuera necesario, se puede especificar un tamaño personalizado:

```
@media print {
  @page {
    size: 8.5in 11in;
  }
}
```

Para definir la orientación de la página, se usa el atributo
`orientation`, cuyos valores posibles son:

- `portrait` (Para retrato o vertical. Es el valor por defecto)
- `landscape` (Para apaisado u horizontal)

```
@media print {
  @page {
    size: A4 landscape;
  }
}
```
