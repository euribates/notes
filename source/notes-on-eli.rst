ELI (Identificador Europeo de Legislación)
========================================================================

.. tags:: europa,administracion,normativa


Qué es ELI
----------

El **Identificador Europeo de Legislación** (ELI) es un estándar europeo
de identificación y descripción de la normativa publicada en los diarios
oficiales y las bases de datos oficiales, que permiten acceder *online*
a la legislación en un formato normalizado, de manera que pueda
localizarse, intercambiarse y reutilizarse por encima de las fronteras.

Aunque hay mucha información legislativa disponible digitalmente a
Internet, la accesibilidad y la interoperabilidad de los sistemas de
información de las instituciones nacionales y europeas se ven
obstaculizadas por las diferencias de los varios ordenamientos jurídicos
nacionales, así como por las diferencias que hay en los sistemas
técnicos utilizados para almacenar y presentar la legislación en los
sitios web nacionales.

En este contexto, el Identificador Europeo de Legislación (ELI) tiene
por objeto facilitar el acceso, el intercambio y la interconexión de la
información jurídica publicada en los sistemas de información jurídica
nacionales, europeos y mundiales, para poner en marcha una red de
información legal, disponible como conjunto de datos abiertos y
susceptibles de reutilización.

El estándar ELI incluye especificaciones técnicas sobre tres aspectos,
que la documentación oficial define como **pilares**:

-  Identificadores web (URI) de la información jurídica para identificar
la legislación europea, nacional y regional (pilar 1 del proyecto)

-  Metadatos que especifican la manera de describir la información
jurídica (pilar 2)

-  Un lenguaje específico para intercambiar legislación entre portales
legislativos (pilar 3).

La implementación de este identificador en España se está abordando de
forma coordinada, a través de la Comisión Sectorial de Administración
electrónica, que es un órgano técnico de cooperación del Estado, las
Comunidades Autónomas y las Administraciones Locales.

España se suma a la lista de países europeos que ya aplican el estándar
ELI (Dinamarca, Finlandia, Francia, Irlanda, Italia, Luxemburgo,
Noruega, Portugal, el Reino Unido), además de la propia Unión Europea.

Cómo se identifican las normas con ELI
--------------------------------------

Cada recurso legal tiene un URI (*Uniform Resource Identifier*) que lo
identifica de manera **unívoca** y **permanente** a Internet.

Los URI se construyen en conformidad con la plantilla definida por la
especificación técnica para las normas estatales y autonómicas, que se
muestra a continuación:

::

/eli/{jurisdiction}/{type}/{year}/{month}/{day}/{number}/{version}/{version_date}/{language}/{formato}

Sobre el campo ``jurisdiction``
-------------------------------

En nuestro caso, el campo jurisdicción debe ser ``es-cn`` para la
normativa autonómica. Los valores aceptados para España se muestran en
la siguiente tabla:

========= =========================================
Valor     Nivel territorial
========= =========================================
``es``    Estado
``es-an`` Comunidad Autónoma de Andalucía
``es-ar`` Comunidad Autónoma de Aragón
``es-cn`` Comunidad Autónoma de Canarias
``es-cb`` Comunidad Autónoma de Cantabria
``es-cl`` Comunidad de Castilla y León
``es-cm`` Comunidad Autónoma de Castilla-La Mancha
``es-ct`` Comunidad Autónoma de Cataluña
``es-ex`` Comunidad Autónoma de Extremadura
``es-ga`` Comunidad Autónoma de Galicia
``es-ib`` Comunidad Autónoma de las Illes Balears
``es-ri`` Comunidad Autónoma de la Rioja
``es-md`` Comunidad de Madrid
``es-mc`` Comunidad Autónoma de la Región de Murcia
``es-nc`` Comunidad Foral de Navarra
``es-pv`` Comunidad Autónoma del País Vasco
``es-vc`` Comunitat Valenciana
``es-ce`` Ciudad Autónoma de Ceuta
``es-ml`` Ciudad Autónoma de Melilla
========= =========================================

Fuente: `ELIdata.es - MDR - Authorities - Jurisdiction -
1 <https://www.elidata.es/mdr/authority/jurisdiction/1/>`_

Para cada ayuntamiento se establece un código de jurisdicción propio,
correspondiendo a Canarias los siguientes:

+--------------------+-------------------------------------------------+
| Valor              | Entidad local                                   |
+====================+=================================================+
| ``es-cn-01350017`` | Agaete                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350022`` | Agüimes                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01350038`` | Antigua                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01350043`` | Arrecife                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01350056`` | Artenara                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01350069`` | Arucas                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350075`` | Betancuria                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01350081`` | Firgas                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350094`` | Gáldar                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350108`` | Haría                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01350115`` | Ingenio                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01350120`` | Mogán                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01350136`` | Moya                                            |
+--------------------+-------------------------------------------------+
| ``es-cn-01350141`` | Oliva, La                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-01350154`` | Pájara                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350167`` | Palmas de Gran Canaria, Las                     |
+--------------------+-------------------------------------------------+
| ``es-cn-01350173`` | Puerto del Rosario                              |
+--------------------+-------------------------------------------------+
| ``es-cn-01350189`` | San Bartolomé                                   |
+--------------------+-------------------------------------------------+
| ``es-cn-01350192`` | San Bartolomé de Tirajana                       |
+--------------------+-------------------------------------------------+
| ``es-cn-01350206`` | Aldea de San Nicolás, La                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01350213`` | Santa Brígida                                   |
+--------------------+-------------------------------------------------+
| ``es-cn-01350228`` | Santa Lucía de Tirajana                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01350234`` | Santa María de Guía de Gran Canaria             |
+--------------------+-------------------------------------------------+
| ``es-cn-01350249`` | Teguise                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01350252`` | Tejeda                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350265`` | Telde                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01350271`` | Teror                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01350287`` | Tías                                            |
+--------------------+-------------------------------------------------+
| ``es-cn-01350290`` | Tinajo                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01350304`` | Tuineje                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01350311`` | Valsequillo de Gran Canaria                     |
+--------------------+-------------------------------------------------+
| ``es-cn-01350326`` | Valleseco                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-01350332`` | Vega de San Mateo                               |
+--------------------+-------------------------------------------------+
| ``es-cn-01350347`` | Yaiza                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380012`` | Adeje                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380027`` | Agulo                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380033`` | Alajeró                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01380048`` | Arafo                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380051`` | Arico                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380064`` | Arona                                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380070`` | Barlovento                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380086`` | Breña Alta                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380099`` | Breña Baja                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380103`` | Buenavista del Norte                            |
+--------------------+-------------------------------------------------+
| ``es-cn-01380110`` | Candelaria                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380125`` | Fasnia                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01380131`` | Frontera                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380146`` | Fuencaliente de la Palma                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380159`` | Garachico                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-01380162`` | Garafía                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01380178`` | Granadilla de Abona                             |
+--------------------+-------------------------------------------------+
| ``es-cn-01380184`` | Guancha, La                                     |
+--------------------+-------------------------------------------------+
| ``es-cn-01380197`` | Guía de Isora                                   |
+--------------------+-------------------------------------------------+
| ``es-cn-01380201`` | Güímar                                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01380218`` | Hermigua                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380223`` | Icod de los Vinos                               |
+--------------------+-------------------------------------------------+
| ``es-cn-01380239`` | San Cristóbal de La Laguna                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380244`` | Llanos de Aridane, Los                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01380257`` | Matanza de Acentejo, La                         |
+--------------------+-------------------------------------------------+
| ``es-cn-01380260`` | Orotava, La                                     |
+--------------------+-------------------------------------------------+
| ``es-cn-01380276`` | Paso, El                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380282`` | Puerto de la Cruz                               |
+--------------------+-------------------------------------------------+
| ``es-cn-01380295`` | Puntagorda                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380309`` | Puntallana                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380316`` | Realejos, Los                                   |
+--------------------+-------------------------------------------------+
| ``es-cn-01380321`` | Rosario, El                                     |
+--------------------+-------------------------------------------------+
| ``es-cn-01380337`` | San Andrés y Sauces                             |
+--------------------+-------------------------------------------------+
| ``es-cn-01380342`` | San Juan de la Rambla                           |
+--------------------+-------------------------------------------------+
| ``es-cn-01380355`` | San Miguel de Abona                             |
+--------------------+-------------------------------------------------+
| ``es-cn-01380368`` | San Sebastián de la Gomera                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380374`` | Santa Cruz de la Palma                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01380380`` | Santa Cruz de Tenerife                          |
+--------------------+-------------------------------------------------+
| ``es-cn-01380393`` | Santa Úrsula                                    |
+--------------------+-------------------------------------------------+
| ``es-cn-01380407`` | Santiago del Teide                              |
+--------------------+-------------------------------------------------+
| ``es-cn-01380414`` | Sauzal, El                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380429`` | Silos, Los                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380435`` | Tacoronte                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-01380440`` | Tanque, El                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-01380453`` | Tazacorte                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-01380466`` | Tegueste                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380472`` | Tijarafe                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380488`` | Valverde                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380491`` | Valle Gran Rey                                  |
+--------------------+-------------------------------------------------+
| ``es-cn-01380504`` | Vallehermoso                                    |
+--------------------+-------------------------------------------------+
| ``es-cn-01380511`` | Victoria de Acentejo, La                        |
+--------------------+-------------------------------------------------+
| ``es-cn-01380526`` | Vilaflor de Chasna                              |
+--------------------+-------------------------------------------------+
| ``es-cn-01380532`` | Villa de Mazo                                   |
+--------------------+-------------------------------------------------+
| ``es-cn-01389013`` | Pinar de El Hierro, El                          |
+--------------------+-------------------------------------------------+
| ``es-cn-03350020`` | Fuerteventura                                   |
+--------------------+-------------------------------------------------+
| ``es-cn-03350040`` | Gran Canaria                                    |
+--------------------+-------------------------------------------------+
| ``es-cn-03350070`` | Lanzarote                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-03380030`` | Gomera, La                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-03380050`` | Hierro, El                                      |
+--------------------+-------------------------------------------------+
| ``es-cn-03380100`` | Palma, La                                       |
+--------------------+-------------------------------------------------+
| ``es-cn-03380110`` | Tenerife                                        |
+--------------------+-------------------------------------------------+
| ``es-cn-05350010`` | Mancomunidad de Municipios de la isla de        |
|                    | Lanzarote para la prestación de los servicios   |
|                    | regulados en el Reglamento Nacional de los      |
|                    | Servicios Urbanos e Interurbanos de Transportes |
|                    | en Automóviles Ligeros                          |
+--------------------+-------------------------------------------------+
| ``es-cn-05350020`` | Mancomunidad Intermunicipal del Sureste de Gran |
|                    | Canaria                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-05350030`` | Mancomunidad de Servicios Sociales Mogán-La     |
|                    | Aldea de San Nicolás                            |
+--------------------+-------------------------------------------------+
| ``es-cn-05350040`` | Mancomunidad de Municipios de las Medianías de  |
|                    | Gran Canaria                                    |
+--------------------+-------------------------------------------------+
|                    |                                                 |
+--------------------+-------------------------------------------------+
| ``es-cn-05350050`` | Mancomunidad de Ayuntamientos del Norte de Gran |
|                    | Canaria                                         |
+--------------------+-------------------------------------------------+
| ``es-cn-05350060`` | Mancomunidad Intermunicipal del Sur-Oeste de    |
|                    | Gran Canaria                                    |
+--------------------+-------------------------------------------------+
| ``es-cn-05350070`` | Mancomunidad “Costa Lairaga”                    |
+--------------------+-------------------------------------------------+
| ``es-cn-05350080`` | Mancomunidad de Municipios del Centro-Sur de    |
|                    | Fuerteventura                                   |
+--------------------+-------------------------------------------------+
|                    |                                                 |
+--------------------+-------------------------------------------------+
| ``es-cn-05350100`` | Mancomunidad del Sur de Lanzarote Yaiza-Tías    |
+--------------------+-------------------------------------------------+
| ``es-cn-05350110`` | Mancomunidad de Municipios de Montaña No        |
|                    | Costeros de Canarias                            |
+--------------------+-------------------------------------------------+
| ``es-cn-05380020`` | Mancomunidad del Norte de Tenerife              |
+--------------------+-------------------------------------------------+
| ``es-cn-05380040`` | Mancomunidad del Nordeste de Tenerife           |
+--------------------+-------------------------------------------------+
| ``es-cn-05380050`` | Mancomunidad de Municipios “San Juan de la      |
|                    | Rambla-La Guancha”                              |
+--------------------+-------------------------------------------------+
| ``es-cn-05380070`` | Mancomunidad de Servicios Garachico-El Tanque   |
+--------------------+-------------------------------------------------+
| ``es-cn-08350010`` | Consorcio de Seguridad, Emergencia, Salvamento, |
|                    | Prevención y Extinción de Incendios de la Isla  |
|                    | de Lanzarote                                    |
+--------------------+-------------------------------------------------+
| ``es-cn-08350020`` | Consorcio para el Abastecimiento de Agua a la   |
|                    | Isla de Lanzarote                               |
+--------------------+-------------------------------------------------+
| ``es-cn-08350030`` | Consorcio para la defensa y promoción del       |
|                    | espacio de La Geria                             |
+--------------------+-------------------------------------------------+
| ``es-cn-08380010`` | Consorcio de Tributos de la Isla de Tenerife    |
+--------------------+-------------------------------------------------+

Fuente:

-  `ELIdata.es - MDR - Authorities - Jurisdiction -
2 <https://www.elidata.es/mdr/authority/jurisdiction/2/>`_

Sobre el campo ``type``
------------------------------------------------------------------------

El campo ``type`` define el Rango de la norma. Se define como un código
alfabéticos de 1 a 4 letras (por ejemplo, ``lo`` para *Ley Orgánica*).
Los valores actuales definidos para la legislación nacional y autonómica
son los siguientes (Se han eliminado los tipos aplicables a la normativa
foral, es decir, las normas dictadas por las autoridades de los
territorios forales de España: Navarra y las provincias vascas de Álava,
Bizkaia y Gipuzkoa).

======== ======================== =====
Tipo     Descripción              Rango
======== ======================== =====
``c``    Constitución             1000
``ref``  Reforma (constitucional) 1000
``ai``   Acuerdos internacionales 800
``lo``   Ley Orgánica             500
``l``    Ley                      400
``rdl``  Real Decreto-ley         500
``rdlg`` Real Decreto Legislativo 500
``dl``   Decreto-ley              300
``dlg``  Decreto-Legislativo      300
``reg``  Reglamento               200
``rd``   Real Decreto             500
``d``    Decreto                  100
``o``    Orden                    100
``a``    Acuerdo                  50
``res``  Resolución               50
``ins``  Instrucción              50
``cir``  Circular                 50
======== ======================== =====

Fuente: `ELIdata.es - MDR - Authorities - Type -
1 <https://www.elidata.es/mdr/authority/resource-type/1/>`_.

El campo rango se ha añadido, para reflejar la jerarquía normativa en
España, que, ordenada de mayor a menor, es:

1. **La Constitución**: La norma suprema del ordenamiento jurídico
español, con validez sobre cualquier otra.

2. **Tratados Internacionales**: Normas que deben respetar la supremacía
de la Constitución y que se sitúan por debajo de ella.

3. **Leyes**: Promulgadas por las Cortes Generales. Pueden ser Leyes
Orgánicas (Requieren mayoría absoluta para su aprobación y regulan
materias fundamentales) o leyes Ordinarias (Requieren mayoría simple
y regulan el resto de materias). La diferencia es únicamente a
efectos de su procedimiento de aprobación, y el rango jurídico de los
dos tipos es equivalente.

4. **Normas con rango de Ley**: Normas del Gobierno que tienen fuerza de
ley, aunque no sean promulgadas por el Parlamento. Pueden ser
Decretos-Leyes, esto es, normas dictadas por el Gobierno en casos de
extraordinaria y urgente necesidad, o Decretos Legislativos: Normas
dictadas por el Gobierno en virtud de una delegación de las Cortes.
De igual manera que en el caso anterior, la diferencia radica en el
procedimiento de aprobación, siendo el mismo el rango de los
decretos-ley y los decretos legislativos.

5. **Reglamentos**: Normas de rango inferior dictadas por el Gobierno u
otras autoridades administrativas, como Reales Decretos y Órdenes
Ministeriales.

6. **Leyes del Parlamento de Canarias**: Son aprobadas por el órgano
legislativo de la Comunidad Autónoma y deben respetar lo establecido
en el Estatuto de Autonomía y la Constitución.

7. **Normas de desarrollo**: Serian por un lado los **Decretos del
Gobierno de Canarias**: normas reglamentarias dictadas por el
Gobierno de Canarias para desarrollar las leyes, y los **Reglamentos
de los diferentes Consejos de Gobierno (Consejerías)**: Son normas de
rango inferior, que complementan la legislación y desarrollan las
competencias de cada departamento

Sobre los campos ``year``, ``month`` y ``day``
------------------------------------------------------------------------

Sobre los campos ``year``, ``month`` y ``day``, son auto-explicativos,
solo hay que aclarar que se refieren siempre a la fecha de firma del
texto, **nunca a la fecha de publicación**.

Sobre el campo ``number``
------------------------------------------------------------------------

A pesar de su nombre, puede contener en algunos casos valores
alfanuméricos. En el caso de las normas sin número oficial, se adjudica
un número (1), (2), (3). En el caso de las normas con rango, fecha y
número idéntico, se genera un sufijo (b), (c), (d) para evitar la
duplicidad de URI

Sobre el campo ``version``
------------------------------------------------------------------------

Identifica si el recurso legal es el inicial, el consolidado o el
corregido. Consiste en un código limitado de valores alfabéticos, de
hasta tres caracteres, según la siguiente table:

=================== =======
Versión             Valor
=================== =======
Versión inicial     ``dof``
Versión consolidada ``con``
Versión corregida   ``cer``
=================== =======

Fuente:

-  `ELIdata.es - MDR - Authorities -
Version <https://www.elidata.es/mdr/authority/version/>`__

Sobre el campo ``version_date``
------------------------------------------------------------------------

El campo ``version_date`` (*point in time*) indica la fecha de
actualización que corresponde al texto consolidado. Es una cadena de
texto de 8 caracteres numéricos que indica una fecha usando el formato
``AAAAMMDD``. Debe corresponder con la fecha de entrada en vigor de la
versión consolidada.

Sobre el campo ``language``
------------------------------------------------------------------------

Este codifica el idioma de la disposición. Hay una lista limitada de
valores alfabéticos, pero en nuestro caso, solo necesitamos el código
``spa``.

=================== ===========
Idioma              Valor
=================== ===========
español             ``spa``
catalán             ``cat``
euskera             ``eus``
gallego             ``glg``
occitano            ``oci``
valenciano          ``vci``
Textos multilingües ``mul``
catalán+español     ``cat-spa``
euskera+español     ``eus-spa``
gallego+español     ``glg-spa``
occitano+español    ``oci-spa``
occitano+catalán    ``oci-cat``
valenciano+español  ``vci-spa``
=================== ===========

Fuente:

-  `ELIdata.es - MDR - Authorities -
Language <https://www.elidata.es/mdr/authority/language/>`__

Enlaces
------------------------------------------------------------------------

-  `DOCM. Diario Oficial Castilla - La
Mancha <https://docm.jccm.es/docm/goToEliHelp.do>`__
