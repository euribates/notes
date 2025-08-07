---
title: Notas sobre Chart.js
---

## Sobre Chart.js

**[Chart.js](https://www.chartjs.org/docs/latest/)** es una biblioteca
JavaScript gratuita de código abierto para la visualización de datos, que
admite 8 tipos de gráficos:

1. barra
2. línea
3. área
4. circular
5. burbuja
6. radar
7. polar
8. dispersión.

Ee representa en HTML5 Canvas y está ampliamente considerado como una de las
mejores bibliotecas de visualización de datos. Está disponible bajo la licencia
MIT. 

## Ejemplo de gráfica de barras con Chartjs

Necesitaremos un canvas en nuestra página HTML:

```html
<div>
  <canvas id="myChart"></canvas>
</div>
```

Enlazamos con la libreria Chart.js:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Y finalmente generamos el código con javascript

```js
const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
```
