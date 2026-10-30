Reglamento General de Protección de Datos (RGPD / DPGR)
========================================================================


Antes de la implementación del Reglamento General de Protección de
Datos, los ciudadanos europeos tenían poco control sobre su información
personal. Las empresas podían recolectar, almacenar y procesar datos sin
una base legal clara ni el consentimiento de los usuarios.

Con la llegada del RGPD, este panorama cambió drásticamente. Ahora, las
personas cuentan con derechos fundamentales sobre sus datos, como:

- **Acceso a la información**: los usuarios pueden conocer qué datos
  poseen las empresas sobre ellos.

- **Rectificación de datos**: posibilidad de corregir información
  inexacta.

- **Derecho al olvido**: eliminación de registros personales bajo
  ciertas condiciones.

- **Portabilidad de datos**: opción de transferir información a otra
  plataforma.

Riesgos específicos de publicar un DNI/NIF
------------------------------------------------------------------------

La difusión del DNI completo aumenta los riesgos respecto de la
publicación del nombre por sí solo:

- **Suplantación de identidad y fraude**

  El DNI/NIF puede combinarse con otros datos disponibles para facilitar
  fraudes, intentos de suplantación o ataques de ingeniería social.

- **Agregación y perfilado masivo**

  El *dataset* podría cruzarse con registros mercantiles, directorios
  comerciales, información territorial y otras fuentes para construir
  perfiles detallados.


= **Pérdida de control sobre la difusión**

  Los datos pueden descargarse, replicarse, indexarse por buscadores y
  permanecer disponibles en copias incluso después de retirar el *dataset*
  original.


- **Incumplimiento de la normativa**

  Si la difusión carece de base jurídica o incluye campos innecesarios,
  podría infringir los principios de licitud, limitación de la finalidad y
  minimización del RGPD, con posibles reclamaciones y actuaciones de la
  autoridad de control.

El DNI/NIF no es, por sí mismo, una categoría especial de datos del
artículo 9 del RGPD. Sin embargo, eso no significa que sea un
identificador de libre publicación: sigue siendo un dato personal sujeto a
las garantías generales del Reglamento.


Recomendaciones para publicar un *dataset* con un DNI
------------------------------------------------------------------------

1. **Si es posible, eliminar el DNI/NIF completo** del fichero abierto. Si
   el objetivo es ofrecer un **directorio de autónomos**, normalmente
   puede bastar con el nombre, la actividad económica, la ubicación
   general y otros datos estrictamente necesarios.

2. Usar un **identificador alternativo**. Si es necesario distinguir
   registros, puede emplearse un identificador interno aleatorio que no
   revele el DNI ni permita reconstruirlo. Si el registro debe poder
   vincularse con fuentes externas, hay que evaluar también ese riesgo.

3. **Diferenciar el fichero público del registro interno**. La Administración
   puede necesitar el DNI para gestionar sus expedientes sin que eso
   implique publicarlo en el *dataset*.

4. **Documentar la base jurídica campo por campo**. Debe indicarse qué
   norma y qué finalidad justifican la publicación de cada dato, con
   especial atención al identificador nacional.

5. Realizar una evaluación de riesgos y consultar al delegado de
   protección de datos (DPD). Deben analizarse la escala de difusión, la
   posibilidad de cruces de información y los riesgos para los afectados.
   Si es probable que el tratamiento entrañe un alto riesgo, habrá que
   valorar una evaluación de impacto conforme al artículo 35 del RGPD.

6. Comprobar la información facilitada a los interesados. La transparencia
   informativa debe cubrir la finalidad, la base jurídica, los
   destinatarios y, cuando corresponda, la publicación y reutilización
   previstas.

7. Establecer medidas de gobernanza. Deben definirse condiciones de
   reutilización, procedimientos para rectificar datos incorrectos,
   mecanismos de revisión periódica y medidas de seguridad apropiadas.

  La **publicación parcial** es una alternativa expresamente contemplada
  en el artículo 16 de la Ley 19/2013: si el límite de protección de datos
  solo afecta a una parte de la información, debe valorarse omitir esa
  parte y facilitar el resto, siempre que el resultado conserve sentido.

Según el Tipo de *dataset*:

- Directorio de autónomos: Publicar los campos profesionales necesarios y
  excluir el DNI completo, a no ser que esté expresamente autorizado.

- *Dataset* estadístico: Publicar datos agregados o anonimizados, siempre
  que no se pueda identificar a las personas razonablemente.

- Relación de beneficiarios de subvenciones: Aplicar la normativa
  específica de publicidad de subvenciones y determinar qué identificador
  debe publicarse según el régimen vigente.

- Adjudicatarios de contratos públicos: Publicar los datos exigidos por la
  normativa de contratación; no añadir el DNI si no es necesario.

- Registro público regulado por una ley sectorial: Comprobar qué datos
  permite o exige difundir la norma reguladora y con qué finalidad.

En relación con la contratación pública, la AEPD ha señalado que, para
identificar a los adjudicatarios cuando se trata de empresarios
individuales, normalmente basta con el nombre y los apellidos, y que
añadir el DNI/NIF resulta innecesario a efectos de transparencia. Es un
criterio especialmente útil por analogía, aunque su aplicación definitiva
depende de la finalidad y la norma que regule el dataset concreto.


