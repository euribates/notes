Sede electrónica
========================================================================

.. tags:: opendata,sistemas,administración


Sobre la sede
------------------------------------------------------------------------

Notas sobre creación de sedes electrónicas.

Cómo montar una Sede Electronica con software libre en España
------------------------------------------------------------------------

- **Plataforma base**: ``Mall@``, solución *open source* desarrollada
  para administraciones públicas españolas, incluye:

- Gestor documental (Alfresco)

- Sistema de firma electrónica (@firma v5)

- Registro electrónico (@ries)

- Portal ciudadano

- **Autenticación**: Integración con el sistema de certificados
  digitales de la FNMT-RCM, requiriendo:

- Configurador FNMT-RCM para generación de claves

- Navegadores compatibles con certificados (Firefox, Chrome, Edge)

Pasos de implementación de una sede tipo
------------------------------------------------------------------------

Infraestructura tecnológica
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Servidores con sistemas operativos libres (Guadalinex, Linex)

- ``Middleware`` de interoperabilidad (Terr@ para ESB)

- Conexión a Red SARA para comunicación interadministrativa

Módulos esenciales
~~~~~~~~~~~~~~~~~~

+------------------+--------------------+------------------------------+
| Módulo           | Software           | Función                      |
|                  | recomendado        |                              |
+==================+====================+==============================+
| Gestión          | ``                 | Archivo electrónico de       |
| documental       | Alfresco/Archiv@`` | expedientes                  |
+------------------+--------------------+------------------------------+
| Firma            | ``@firma v5``      | Validación certificados FNMT |
| electrónica      |                    |                              |
+------------------+--------------------+------------------------------+
| Notificaciones   | ``Notific@``       | Comunicaciones oficiales     |
+------------------+--------------------+------------------------------+
| Pagos            | Pasarelas libres   | Integración con TPV virtual  |
| electrónicos     |                    |                              |
+------------------+--------------------+------------------------------+
| Portal ciudadano | ``Liferay/Drupal`` | CMS con accesibilidad AA del |
|                  |                    | W3C                          |
+------------------+--------------------+------------------------------+
| Registro         | ``@ries``          | Tramitación de               |
| electrónico      |                    | procedimientos               |
+------------------+--------------------+------------------------------+

Consideraciones legales
~~~~~~~~~~~~~~~~~~~~~~~

- Cumplimiento del Esquema Nacional de Seguridad (ENS)

- Adhesión al Esquema Nacional de Interoperabilidad (ENI)

- Implementación de protocolos de preservación digital a largo plazo

Para casos de éxito, destacan implementaciones como:

- **W@ndA** en Junta de Andalucía

- **PLATEA** en País Vasco

- **OpenFWPA** en Principado de Asturias

La solución debe complementarse con formación a funcionarios y
establecer canales de soporte técnico especializado, preferentemente a
través de empresas acreditadas en administración electrónica.

Integración de servicios esenciales
------------------------------------------------------------------------

- Conectar con **Notific@** para comunicaciones oficiales

- Implementar pasarelas de pago libres compatibles con TPV virtuales
  públicos

- **Drupal** ofrece flexibilidad, comunidad activa y capacidad
  multisite, permitiendo gestionar varios portales desde una misma base
  común y personalizaciones independientes.

- **Liferay** es una plataforma de experiencia digital (DXP) robusta,
  orientada a la integración con sistemas existentes, gestión de
  identidades, analítica avanzada y personalización de la experiencia
  del usuario.

Integración de sistemas esenciales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El CMS debe integrarse con, al menos:

- **Gestor de formularios** para la tramitación electrónica.

- **Sistema de identificación y autenticación** (firma electrónica,
  certificados FNMT, Cl@ve) para garantizar la validez legal de los
  procesos.

- **Registro electrónico** para la entrada y salida de documentos
  oficiales.

- **Pasarela de pagos** y sistemas de notificación electrónica.

- Configura autenticación segura (LDAP, Kerberos, SSO)

Tanto Drupal como Liferay permiten integración mediante módulos, APIs
REST, SOAP y conectores predefinidos.

Despliegue y mantenimiento
------------------------------------------------------------------------

- Utiliza infraestructuras escalables (soportadas por ambos CMS) y
  planifica actualizaciones centralizadas, especialmente si optas por un
  modelo multisite con Drupal.

- Prepara soporte técnico y formación para usuarios y administradores.

Cumplimiento del Esquema Nacional de Seguridad (ENS)
------------------------------------------------------------------------

- Implementa controles de acceso, autenticación y autorización robustos

- Garantiza la confidencialidad, integridad y disponibilidad de la
  información crítica, utilizando medidas como cifrado, copias de
  seguridad y sistemas de alta disponibilidad

- Realiza auditorías periódicas de seguridad y aplica políticas de
  protección en todos los entornos

Accesibilidad Web
-----------------

- Adapta los temas y componentes visuales para cumplir con el nivel AA
  de las WCAG 2.1, exigido por la legislación española para portales
  públicos.

- Valida la accesibilidad mediante herramientas automáticas y revisiones
  manuales, asegurando que todos los usuarios, incluidos los de
  movilidad reducida, puedan acceder a los servicios.

Protección de Datos (RGPD y LOPDGDD)
------------------------------------

- Integra mecanismos para la gestión de consentimientos, derechos de los
  ciudadanos (acceso, rectificación, supresión, portabilidad, etc.) y
  registros de actividades de tratamiento.

- Realiza evaluaciones de impacto de protección de datos (EIPD) y aplica
  medidas técnicas para minimizar riesgos, como anonimización y
  seudonimización de datos personales.

- Nombra un Delegado de Protección de Datos (DPD) y establece
  procedimientos claros para notificación de brechas de seguridad.

Firma Electrónica y Registro
----------------------------

- Integra módulos o conectores compatibles con la firma electrónica
  reconocida en España (FNMT, Cl@ve), asegurando la validez legal de los
  trámites.

- Implementa un registro electrónico para la entrada y salida de
  documentos, con sellado de tiempo y trazabilidad.

Interoperabilidad y estándares
------------------------------

- Utiliza formatos de datos y protocolos interoperables (XML, XAdES,
  PDF/A, etc.), en línea con el Esquema Nacional de Interoperabilidad.

- Asegura la integración con otras plataformas administrativas mediante
  APIs y servicios web estándar.

Cómo asegurar la interoperabilidad con otros sistemas públicos
------------------------------------------------------------------------

Para asegurar la interoperabilidad de una sede electrónica basada en
**Drupal** o **Liferay** con otros sistemas públicos españoles, debes
abordar varios aspectos técnicos y normativos:

Cumplimiento del Esquema Nacional de Interoperabilidad (ENI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Adopta los estándares técnicos y semánticos definidos en el ENI, que
  garantizan la compatibilidad de los datos y documentos intercambiados
  entre administraciones

- Utiliza metadatos y formatos de archivo reconocidos (XML, PDF/A,
  XAdES, etc.) para documentos electrónicos

Integración con la Red SARA
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Publica servicios a través de la Red SARA, la infraestructura de
  comunicaciones de las AAPP españolas, lo que facilita el intercambio
  seguro y directo de información entre organismos públicos.

- Configura los endpoints de tus servicios web para cumplir con los
  requisitos de seguridad y autenticación de SARA.

Uso de APIs y servicios web estándar
------------------------------------

- Implementa APIs REST o SOAP para exponer y consumir servicios,
  facilitando la integración con sistemas de terceros y plataformas
  estatales.

- Drupal y Liferay permiten la extensión mediante módulos o plugins para
  conectar con servicios externos y adaptar la lógica de negocio según
  las necesidades.

Autenticación e identificación interoperable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Integra mecanismos de autenticación compatibles con Cl@ve, LDAP o
  Kerberos, ampliamente utilizados en la administración pública
  española.

- Asegura la gestión federada de identidades y la validación de usuarios
  con certificados digitales reconocidos.

Modularidad y extensibilidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Aprovecha la arquitectura modular de ambos CMS para añadir o adaptar
  funcionalidades específicas mediante extensiones, sin comprometer la
  base del sistema.

- Utiliza frameworks open source como OpenFWA para facilitar el
  desarrollo de aplicaciones interoperables en el entorno público
  español.

Accesibilidad y multicanalidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Garantiza que los servicios sean accesibles y funcionales en
  diferentes dispositivos y sistemas operativos, cumpliendo los
  requisitos de accesibilidad legalmente exigidos.

Fuentes
------------------------------------------------------------------------

-  http://femp.femp.es/files/566-2071-archivo/Student+book+TD+02.11.2016.pdf
-  http://www.asiap.org/AsIAP/images/stories/JIAP/jiap2011/Presentaciones/Azul/A1717_QUANAM.pdf
-  https://administracionelectronica.gob.es/ctt/esede
-  https://administracionelectronica.gob.es/ctt/resources/Soluciones/159/Descargas/Guia-de-sedes-Electronicas.pdf?idIniciativa=159&idElemento=79
-  https://administracionelectronica.gob.es/pae_Home/dam/jcr:a9cd1fbc-0d6e-48ee-8905-5d851156f83f/Software_de_fuentes_abiertas_en_la_Administracion_electronica-Mapa_de_procesos_y_arquitectura_de_componentes_2009.pdf
-  https://administracionelectronica.gob.es/pae_Home/dam/jcr:cd7dff7c-6e50-4b91-8e3c-05a4e914e596/Estudio_sobre_la_situacion_actual_del_Software_de_Fuentes_Abiertas_en_las_Universidades_y_Centros_de_I_D_2009.pdf
-  https://ast.aragon.es/sites/default/files/memoria-anual-2020.pdf
-  https://ateneatech.com/administracion-publica-drupal
-  https://blog.biko2.com/drupal/portales-administracion-publica-en-drupal/
-  https://ceie.online/sistemas-y-comunicaciones/
-  https://core.ac.uk/download/pdf/38996549.pdf
-  https://digitum.um.es/xmlui/bitstream/10201/54364/1/TD_Julio-Soler_2017\_.pdf
-  https://dokumen.pub/humanidades-digitales-e-historiografia-lingistica-hispanica-proyectos-de-presente-y-retos-de-futuro-9783968694368.html
-  https://dspace.ups.edu.ec/bitstream/123456789/13729/1/Tecnologia y
accesibilidad Vol2.pdf
-  https://e-archivo.uc3m.es/rest/api/core/bitstreams/26ce8197-578e-43bb-9204-4d529390d497/content
-  https://empleopublico.castillalamancha.es/sites/default/files/proc-selec/ficheros/cuestionario_examen_1-*e._s._sist._y_tec._inf*.pdf
-  https://empleopublico.castillalamancha.es/sites/default/files/proc-selec/ficheros/cuestionario_test_es_sistemas_y_tecnologias_de_la_informacion_disc.pdf
-  https://openaccess.uoc.edu/bitstream/10609/116826/9/macaperezTFM0620memoria.pdf
-  https://openaccess.uoc.edu/bitstream/10609/198/1/Implantación de
sistemas de software libre.pdf
-  https://repositorio.utn.edu.ec/bitstream/123456789/2612/1/04 ISC 286
TESIS.pdf
-  https://riunet.upv.es/bitstream/10251/44206/1/PFC_VMP_v1.4.pdf
-  https://rootstack.com/es/blog/drupal-vs-liferay
-  https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/preguntas-frecuentes/certificacion-sistemas-informaticos-declaracion-responsable.html
-  https://sede.isciii.gob.es/docs/Guia_eAdmin.pdf
-  https://sede.oepm.gob.es
-  https://sede.red.gob.es
-  https://sede.red.gob.es/en/ayuda/requerimientos-tecnicos
-  https://sede.red.gob.es/eRegistro/pdf/RED_ES_Ayuda_requisitos.pdf
-  https://sede.ugr.es/requisitos_tecnicos.html
-  https://ticjob.es/cat/treball/programador-senior-drupal-html-javascript/61175
-  https://travesia.mcu.es/bitstream/10421/5541/1/VCNBP.pdf
-  https://www.adams.es/wp-content/uploads/2024/01/especialidades-formativas-1.xlsx
-  https://www.bilib.es/uploads/media/estudio_sistemas_gestion_contenidos_web_cms.pdf
-  https://www.congreso.es/public_oficiales/L14/CONG/BOCG/D/BOCG-14-D-373.PDF
-  https://www.dig.es/proteccion-legal-de-software-en-espana/
-  https://www.hiberus.com/crecemos-contigo/como-construir-un-chatbot-rag-serverless/
-  https://www.liferay.com/es/blog/customer-experience/10-factores-que-debes-considerar-antes-de-elegir-un-cms-open-source
-  https://www.sede.fnmt.gob.es/certificados/persona-fisica/obtener-certificado-software/configuracion-previa
-  https://www.sede.fnmt.gob.es/descargas/descarga-software/instalacion-software-generacion-de-claves
-  https://www.youtube.com/watch?v=MW9k6hdL3Ro
