<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Hola, ¿Podrías decirme cómo se puede montar un sistema de sede electronica con software libre en españa

Para implementar una sede electrónica con software libre en España, se deben combinar soluciones tecnológicas abiertas con los estándares de interoperabilidad y seguridad establecidos por el marco normativo español. Aquí presentamos un enfoque estructurado:

## Componentes clave del sistema

- **Plataforma base**: Mall@, solución open source desarrollada para administraciones públicas españolas, incluye:
    - Gestor documental (Alfresco)
    - Sistema de firma electrónica (@firma v5)
    - Registro electrónico (@ries)
    - Portal ciudadano (Public@) [^1_3][^1_4]
- **Autenticación**: Integración con el sistema de certificados digitales de la FNMT-RCM, requiriendo:
    - Configurador FNMT-RCM para generación de claves [^1_1][^1_2]
    - Navegadores compatibles con certificados (Firefox, Chrome, Edge) [^1_1]


## Pasos de implementación

1. **Infraestructura tecnológica**:
    - Servidores con sistemas operativos libres (Guadalinex, Linex)
    - Middleware de interoperabilidad (Terr@ para ESB)
    - Conexión a Red SARA para comunicación interadministrativa [^1_3][^1_4]
2. **Módulos esenciales**:
```markdown
| Módulo               | Software recomendado      | Función                          |
|----------------------|---------------------------|----------------------------------|
| Gestión documental   | Alfresco/Archiv@          | Archivo electrónico de expedientes [^1_5] |
| Firma electrónica     | @firma v5                 | Validación certificados FNMT [^1_2] |
| Notificaciones        | Notific@                  | Comunicaciones oficiales [^1_2]     |
| Pagos electrónicos    | Pasarelas libres          | Integración con TPV virtual      |
```

3. **Consideraciones legales**:

- Cumplimiento del Esquema Nacional de Seguridad (ENS)
- Adhesión al Esquema Nacional de Interoperabilidad (ENI)
- Implementación de protocolos de preservación digital a largo plazo [^1_4]


## Ventajas del modelo open source

- **Reducción de costes**: Eliminación de licencias propietarias
- **Control tecnológico**: Posibilidad de adaptar el código a necesidades específicas
- **Interoperabilidad**: Uso de estándares abiertos como XML-DSig y XAdES [^1_3][^1_4]

> "La arquitectura basada en componentes libres permite escalabilidad y reutilización de desarrollos entre administraciones" [^1_3].

Para casos de éxito, destacan implementaciones como:

- **W@ndA** en Junta de Andalucía
- **PLATEA** en País Vasco
- **OpenFWPA** en Principado de Asturias [^1_3][^1_4]

La solución debe complementarse con formación a funcionarios y establecer canales de soporte técnico especializado, preferentemente a través de empresas acreditadas en administración electrónica.

<div style="text-align: center">⁂</div>

[^1_1]: https://www.sede.fnmt.gob.es/certificados/persona-fisica/obtener-certificado-software/configuracion-previa

[^1_2]: https://www.sede.fnmt.gob.es/descargas/descarga-software/instalacion-software-generacion-de-claves

[^1_3]: http://www.asiap.org/AsIAP/images/stories/JIAP/jiap2011/Presentaciones/Azul/A1717_QUANAM.pdf

[^1_4]: https://administracionelectronica.gob.es/pae_Home/dam/jcr:a9cd1fbc-0d6e-48ee-8905-5d851156f83f/Software_de_fuentes_abiertas_en_la_Administracion_electronica-Mapa_de_procesos_y_arquitectura_de_componentes_2009.pdf

[^1_5]: https://riunet.upv.es/bitstream/10251/44206/1/PFC_VMP_v1.4.pdf

[^1_6]: https://www.youtube.com/watch?v=MW9k6hdL3Ro

[^1_7]: https://sede.oepm.gob.es

[^1_8]: https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/preguntas-frecuentes/certificacion-sistemas-informaticos-declaracion-responsable.html

[^1_9]: https://sede.red.gob.es

[^1_10]: https://sede.red.gob.es/en/ayuda/requerimientos-tecnicos


---

# Cuáles son los pasos clave para montar una sede electrónica con software libre en España

Para implementar una sede electrónica con software libre en España, se deben seguir estos pasos clave respaldados por el marco normativo y las soluciones tecnológicas abiertas:

## 1. **Infraestructura tecnológica base**

- Utilizar sistemas operativos libres como **Guadalinex** o **Linex** en servidores locales o en la nube[^2_2].
- Establecer conexión a la **Red SARA** para garantizar la interoperabilidad entre administraciones públicas[^2_1].


## 2. **Selección de componentes software**

```markdown
| Función                | Herramienta recomendada      | Características                          |
|------------------------|------------------------------|------------------------------------------|
| Gestión documental     | Alfresco/Archiv@             | Archivado electrónico de expedientes[^2_3] |
| Firma electrónica       | @firma v5                    | Validación de certificados FNMT[^2_4]       |
| Portal ciudadano        | Liferay/Drupal               | CMS con accesibilidad AA del W3C[^2_3]      |
| Registro electrónico    | @ries                        | Tramitación de procedimientos[^2_2]         |
```


## 3. **Autenticación segura**

- Instalar el **Configurador FNMT-RCM** para generación de claves criptográficas[^2_3].
- Configurar navegadores compatibles (Firefox, Chrome, Edge) con certificados digitales reconocidos[^2_4][^2_3].


## 4. **Cumplimiento normativo**

- Implementar el **Esquema Nacional de Seguridad (ENS)** en todos los módulos[^2_1].
- Adherirse al **Esquema Nacional de Interoperabilidad (ENI)** para formatos de datos y protocolos[^2_1].


## 5. **Integración de servicios esenciales**

- Conectar con **Notific@** para comunicaciones oficiales[^2_1].
- Implementar pasarelas de pago libres compatibles con TPV virtuales públicos.


## 6. **Pruebas y validación**

- Realizar auditorías de accesibilidad según normativa AA del W3C[^2_2].
- Verificar la interoperabilidad con otras sedes mediante pruebas en entorno de preproducción[^2_1].

Para casos de éxito, destacan plataformas como **OpenFWPA** en Asturias y **W@ndA** en Andalucía, que utilizan arquitecturas modulares basadas en componentes libres[^2_2]. La solución debe completarse con planes de formación para funcionarios y contratación de soporte técnico especializado en administración electrónica.

<div style="text-align: center">⁂</div>

[^2_1]: https://administracionelectronica.gob.es/ctt/esede

[^2_2]: https://administracionelectronica.gob.es/pae_Home/dam/jcr:a9cd1fbc-0d6e-48ee-8905-5d851156f83f/Software_de_fuentes_abiertas_en_la_Administracion_electronica-Mapa_de_procesos_y_arquitectura_de_componentes_2009.pdf

[^2_3]: https://www.sede.fnmt.gob.es/certificados/persona-fisica/obtener-certificado-software/configuracion-previa

[^2_4]: https://sede.red.gob.es/eRegistro/pdf/RED_ES_Ayuda_requisitos.pdf

[^2_5]: https://www.dig.es/proteccion-legal-de-software-en-espana/

[^2_6]: https://administracionelectronica.gob.es/ctt/resources/Soluciones/159/Descargas/Guia-de-sedes-Electronicas.pdf?idIniciativa=159\&idElemento=79

[^2_7]: https://sede.isciii.gob.es/docs/Guia_eAdmin.pdf

[^2_8]: https://openaccess.uoc.edu/bitstream/10609/198/1/Implantación de sistemas de software libre.pdf

[^2_9]: https://core.ac.uk/download/pdf/38996549.pdf

[^2_10]: https://sede.ugr.es/requisitos_tecnicos.html


---

# Cómo integrar herramientas open source como Drupal o Liferay en mi sede electrónica

Integrar herramientas open source como **Drupal** o **Liferay** en una sede electrónica en España es totalmente viable y aporta flexibilidad, escalabilidad y cumplimiento normativo. Aquí tienes los pasos y consideraciones clave para una integración exitosa:

## 1. **Definir la arquitectura y los requisitos**

- Determina los servicios que ofrecerá la sede: trámites online, registro electrónico, consulta de expedientes, notificaciones, etc.[^3_1]
- Asegúrate de cumplir los requisitos de accesibilidad (AA del W3C), multi-idioma y seguridad conforme a la normativa española.[^3_1]


## 2. **Seleccionar la plataforma**

- **Drupal** es ideal para portales de administración pública gracias a su flexibilidad, comunidad activa y capacidad multisite, permitiendo gestionar varios portales desde una misma base común y personalizaciones independientes[^3_2][^3_3].
- **Liferay** es una plataforma de experiencia digital (DXP) robusta, orientada a la integración con sistemas existentes, gestión de identidades, analítica avanzada y personalización de la experiencia del usuario[^3_4][^3_5][^3_6][^3_7].


## 3. **Integración de sistemas esenciales**

- Integra el CMS con:
    - **Gestor de formularios** para la tramitación electrónica.
    - **Sistema de identificación y autenticación** (firma electrónica, certificados FNMT, Cl@ve) para garantizar la validez legal de los procesos[^3_1].
    - **Registro electrónico** para la entrada y salida de documentos oficiales[^3_1].
    - **Pasarela de pagos** y sistemas de notificación electrónica.
- Tanto Drupal como Liferay permiten integración mediante módulos, APIs REST, SOAP y conectores predefinidos[^3_6][^3_7].


## 4. **Desarrollo y personalización**

- En **Drupal**, utiliza módulos para formularios, gestión documental y autenticación, y adapta el diseño a los estándares de accesibilidad y usabilidad[^3_2][^3_3].
- En **Liferay**, aprovecha su marco de integración para conectar con sistemas backend (CRM, ERP, etc.), y personaliza la experiencia ciudadana con herramientas de analítica y segmentación[^3_4][^3_5][^3_6][^3_7].


## 5. **Seguridad y cumplimiento**

- Configura autenticación segura (LDAP, Kerberos, SSO) y aplica el Esquema Nacional de Seguridad (ENS)[^3_1][^3_4].
- Realiza auditorías de accesibilidad y seguridad antes del despliegue.


## 6. **Despliegue y mantenimiento**

- Utiliza infraestructuras escalables (soportadas por ambos CMS) y planifica actualizaciones centralizadas, especialmente si optas por un modelo multisite con Drupal[^3_2].
- Prepara soporte técnico y formación para usuarios y administradores.

---

### Tabla comparativa: Drupal vs Liferay para sede electrónica

| Característica | Drupal | Liferay |
| :-- | :-- | :-- |
| Lenguaje | PHP | Java |
| Multisite | Sí | Sí |
| Integración sistemas | Módulos, APIs REST/SOAP | APIs, conectores, integración avanzada |
| Accesibilidad | Adaptable, requiere configuración | Cumple AA, herramientas integradas |
| Analítica | Módulos externos | Analítica avanzada integrada |
| Escalabilidad | Alta (multisite) | Alta (clustering, multisite) |


---

**Conclusión:**
Drupal y Liferay son opciones sólidas y abiertas para montar una sede electrónica. La clave está en definir bien los requisitos, aprovechar los módulos y conectores para la integración con sistemas administrativos y cumplir con los estándares legales y de accesibilidad exigidos en España[^3_1][^3_2][^3_4][^3_6][^3_7].

<div style="text-align: center">⁂</div>

[^3_1]: https://administracionelectronica.gob.es/pae_Home/dam/jcr:a9cd1fbc-0d6e-48ee-8905-5d851156f83f/Software_de_fuentes_abiertas_en_la_Administracion_electronica-Mapa_de_procesos_y_arquitectura_de_componentes_2009.pdf

[^3_2]: https://ateneatech.com/administracion-publica-drupal

[^3_3]: https://blog.biko2.com/drupal/portales-administracion-publica-en-drupal/

[^3_4]: https://www.liferay.com/es/industries/public-sector

[^3_5]: https://www.liferay.com/es/blog/customer-experience/10-claves-para-la-digitalizacion-de-la-administracion-publica

[^3_6]: https://www.liferay.com/es/capabilities/integration

[^3_7]: https://www.hiberus.com/crecemos-contigo/por-que-tengo-que-utilizar-liferay-enterprise/

[^3_8]: https://www.laecuaciondigital.com/empresas/aplicaciones-empresariales/liferay-permite-integrar-cualquier-motor-de-ia-en-su-plataforma-digital/

[^3_9]: https://contrataciondelestado.es/wps/wcm/connect/PLACE_es/Site/area/docAccCmpnt?srv=cmpnt\&cmpntname=GetDocumentsById\&DocumentIdParam=fd8bf334-4b26-4e69-808a-ef447fd64dd7

[^3_10]: https://www.solucionex.com/blog/drupal-services

[^3_11]: https://sede.administracionespublicas.gob.es

[^3_12]: https://rednerea.juntadeandalucia.es/drupal/printpdf/142

[^3_13]: https://www.ulpgc.es/noticia/software-libre-biblioteca-ulpgc

[^3_14]: https://digitum.um.es/xmlui/bitstream/10201/27779/1/Manual_Drupal.pdf

[^3_15]: https://www.hiberus.com/crecemos-contigo/geolocalizacion-e-implementacion-en-drupal/

[^3_16]: https://www.semic.es/es/soluciones/administracion-electronica/transparencia-y-gobierno-abierto/sede-electronica

[^3_17]: https://www.liferay.com/es/

[^3_18]: https://www.arsys.es/blog/liferay-cloud-portal-empresarial

[^3_19]: https://portalerp.es/liferay-se-asocia-con-paypal-para-mejorar-el-comercio-electronico-b2b


---

# Qué aspectos técnicos debo considerar para adaptar Drupal o Liferay a los requisitos normativos españoles

Para adaptar Drupal o Liferay a los requisitos normativos españoles en el contexto de una sede electrónica, debes considerar los siguientes aspectos técnicos clave:

## **1. Cumplimiento del Esquema Nacional de Seguridad (ENS)**

- Implementa controles de acceso, autenticación y autorización robustos.
- Garantiza la confidencialidad, integridad y disponibilidad de la información crítica, utilizando medidas como cifrado, copias de seguridad y sistemas de alta disponibilidad[^4_4].
- Realiza auditorías periódicas de seguridad y aplica políticas de protección en todos los entornos.


## **2. Accesibilidad Web**

- Adapta los temas y componentes visuales para cumplir con el nivel AA de las WCAG 2.1, exigido por la legislación española para portales públicos[^4_3].
- Valida la accesibilidad mediante herramientas automáticas y revisiones manuales, asegurando que todos los usuarios, incluidos los de movilidad reducida, puedan acceder a los servicios.


## **3. Protección de Datos (RGPD y LOPDGDD)**

- Integra mecanismos para la gestión de consentimientos, derechos de los ciudadanos (acceso, rectificación, supresión, portabilidad, etc.) y registros de actividades de tratamiento[^4_5][^4_6].
- Realiza evaluaciones de impacto de protección de datos (EIPD) y aplica medidas técnicas para minimizar riesgos, como anonimización y seudonimización de datos personales[^4_6].
- Nombra un Delegado de Protección de Datos (DPD) y establece procedimientos claros para notificación de brechas de seguridad[^4_6].


## **4. Firma Electrónica y Registro**

- Integra módulos o conectores compatibles con la firma electrónica reconocida en España (FNMT, Cl@ve), asegurando la validez legal de los trámites[^4_5].
- Implementa un registro electrónico para la entrada y salida de documentos, con sellado de tiempo y trazabilidad.


## **5. Interoperabilidad y estándares**

- Utiliza formatos de datos y protocolos interoperables (XML, XAdES, PDF/A, etc.), en línea con el Esquema Nacional de Interoperabilidad.
- Asegura la integración con otras plataformas administrativas mediante APIs y servicios web estándar.


## **6. Usabilidad y formación**

- Facilita la formación de administradores y usuarios finales en el uso del CMS elegido, identificando posibles puntos de mejora y adaptando las funcionalidades a las necesidades del servicio público[^4_1].

---

**En resumen:**
La adaptación de Drupal o Liferay a la normativa española requiere una combinación de configuración técnica, integración de módulos específicos y cumplimiento estricto de los estándares legales de seguridad, protección de datos y accesibilidad, además de una gestión activa de la interoperabilidad y la formación de los usuarios[^4_1][^4_3][^4_5][^4_6].

<div style="text-align: center">⁂</div>

[^4_1]: https://www.liferay.com/es/blog/customer-experience/10-factores-que-debes-considerar-antes-de-elegir-un-cms-open-source

[^4_2]: https://rootstack.com/es/blog/drupal-vs-liferay

[^4_3]: https://openaccess.uoc.edu/bitstream/10609/116826/9/macaperezTFM0620memoria.pdf

[^4_4]: https://ast.aragon.es/sites/default/files/memoria-anual-2020.pdf

[^4_5]: https://www.adams.es/wp-content/uploads/2024/01/especialidades-formativas-1.xlsx

[^4_6]: https://ceie.online/sistemas-y-comunicaciones/

[^4_7]: https://repositorio.utn.edu.ec/bitstream/123456789/2612/1/04 ISC 286 TESIS.pdf

[^4_8]: https://dokumen.pub/humanidades-digitales-e-historiografia-lingistica-hispanica-proyectos-de-presente-y-retos-de-futuro-9783968694368.html


---

# Cómo asegurar la interoperabilidad con otros sistemas públicos españoles usando Drupal o Liferay

Para asegurar la interoperabilidad de una sede electrónica basada en **Drupal** o **Liferay** con otros sistemas públicos españoles, debes abordar varios aspectos técnicos y normativos:

## **1. Cumplimiento del Esquema Nacional de Interoperabilidad (ENI)**

- Adopta los estándares técnicos y semánticos definidos en el ENI, que garantizan la compatibilidad de los datos y documentos intercambiados entre administraciones[^5_4].
- Utiliza metadatos y formatos de archivo reconocidos (XML, PDF/A, XAdES, etc.) para documentos electrónicos.


## **2. Integración con la Red SARA**

- Publica servicios a través de la Red SARA, la infraestructura de comunicaciones de las AAPP españolas, lo que facilita el intercambio seguro y directo de información entre organismos públicos[^5_4].
- Configura los endpoints de tus servicios web para cumplir con los requisitos de seguridad y autenticación de SARA.


## **3. Uso de APIs y servicios web estándar**

- Implementa APIs REST o SOAP para exponer y consumir servicios, facilitando la integración con sistemas de terceros y plataformas estatales.
- Drupal y Liferay permiten la extensión mediante módulos o plugins para conectar con servicios externos y adaptar la lógica de negocio según las necesidades[^5_2][^5_5].


## **4. Autenticación e identificación interoperable**

- Integra mecanismos de autenticación compatibles con Cl@ve, LDAP o Kerberos, ampliamente utilizados en la administración pública española[^5_2].
- Asegura la gestión federada de identidades y la validación de usuarios con certificados digitales reconocidos.


## **5. Modularidad y extensibilidad**

- Aprovecha la arquitectura modular de ambos CMS para añadir o adaptar funcionalidades específicas mediante extensiones, sin comprometer la base del sistema[^5_5].
- Utiliza frameworks open source como OpenFWA para facilitar el desarrollo de aplicaciones interoperables en el entorno público español[^5_2].


## **6. Accesibilidad y multicanalidad**

- Garantiza que los servicios sean accesibles y funcionales en diferentes dispositivos y sistemas operativos, cumpliendo los requisitos de accesibilidad legalmente exigidos[^5_3].

---

**Resumen:**
La interoperabilidad en Drupal o Liferay se logra aplicando los estándares del ENI, integrando APIs y servicios web, utilizando la Red SARA, y asegurando autenticación federada y modularidad extensible. Esto permite que tu sede electrónica se comunique eficazmente con otros sistemas públicos españoles y cumpla con la normativa vigente[^5_2][^5_4][^5_5].

<div style="text-align: center">⁂</div>

[^5_1]: https://www.liferay.com/es/blog/customer-experience/10-factores-que-debes-considerar-antes-de-elegir-un-cms-open-source

[^5_2]: https://administracionelectronica.gob.es/pae_Home/dam/jcr:a9cd1fbc-0d6e-48ee-8905-5d851156f83f/Software_de_fuentes_abiertas_en_la_Administracion_electronica-Mapa_de_procesos_y_arquitectura_de_componentes_2009.pdf

[^5_3]: https://e-archivo.uc3m.es/rest/api/core/bitstreams/26ce8197-578e-43bb-9204-4d529390d497/content

[^5_4]: https://empleopublico.castillalamancha.es/sites/default/files/proc-selec/ficheros/cuestionario_test_es_sistemas_y_tecnologias_de_la_informacion_disc.pdf

[^5_5]: https://www.bilib.es/uploads/media/estudio_sistemas_gestion_contenidos_web_cms.pdf

[^5_6]: https://administracionelectronica.gob.es/pae_Home/dam/jcr:cd7dff7c-6e50-4b91-8e3c-05a4e914e596/Estudio_sobre_la_situacion_actual_del_Software_de_Fuentes_Abiertas_en_las_Universidades_y_Centros_de_I_D_2009.pdf

[^5_7]: https://empleopublico.castillalamancha.es/sites/default/files/proc-selec/ficheros/cuestionario_examen_1-_e._s._sist._y_tec._inf_.pdf

[^5_8]: http://femp.femp.es/files/566-2071-archivo/Student book TD 02.11.2016.pdf


---

# Cuáles son los principales desafíos técnicos al conectar Drupal o Liferay con otros sistemas públicos españoles

Los principales desafíos técnicos al conectar **Drupal** o **Liferay** con otros sistemas públicos españoles incluyen:

## **1. Integración y compatibilidad de datos**

- La administración pública española utiliza múltiples fuentes de datos heterogéneas (ERP, CRM, catálogos de datos abiertos, etc.), lo que exige que Drupal o Liferay puedan consumir y exponer información en formatos interoperables como XML, JSON o RDF, y aplicar normas técnicas como la Norma Técnica de Interoperabilidad de Reutilización de Información del Sector Público[^6_4][^6_3].
- Es necesario implementar metadatos y marcado semántico para garantizar la correcta transferencia y reutilización de información entre plataformas[^6_3][^6_4].


## **2. Cumplimiento normativo y accesibilidad**

- Los sistemas deben adaptarse a los requisitos de accesibilidad (nivel AA según WCAG 2.1) no solo en la parte pública, sino también en la administración interna, lo que implica retos en la adaptación de interfaces complejas y herramientas de gestión dentro del propio CMS o DXP[^6_1].
- La integración debe contemplar la trazabilidad y preservación digital de los documentos, asegurando el cumplimiento de la legislación sobre gestión y archivo de contenidos digitales[^6_6].


## **3. Arquitectura y extensibilidad**

- Liferay y Drupal requieren proyectos de consultoría y desarrollo para configurar integraciones robustas, especialmente cuando se conectan con microservicios, APIs REST/SOAP y sistemas legacy de la administración[^6_2].
- La arquitectura debe ser modular y flexible para facilitar futuras integraciones y adaptaciones a cambios normativos o tecnológicos[^6_2].


## **4. Seguridad y autenticación**

- Es imprescindible implementar mecanismos de autenticación federada (Cl@ve, certificados digitales, LDAP, etc.) y garantizar la seguridad en el intercambio de datos a través de la Red SARA o canales seguros equivalentes[^6_2].
- La gestión de permisos y la protección de datos personales deben estar alineadas con el RGPD y la normativa española vigente.


## **5. Mantenimiento y evolución**

- La integración con sistemas públicos suele requerir mantenimiento continuo para adaptarse a cambios en APIs, protocolos o normativas, así como la actualización de dependencias y parches de seguridad[^6_4][^6_1].

---

**En resumen:**
Los principales retos técnicos son la interoperabilidad de datos, la adaptación a la normativa de accesibilidad y seguridad, la arquitectura modular para integraciones complejas, y el mantenimiento constante para asegurar la compatibilidad y el cumplimiento legal en el entorno público español[^6_1][^6_2][^6_3][^6_4].

<div style="text-align: center">⁂</div>

[^6_1]: https://www.hiberus.com/crecemos-contigo/accesibilidad-en-todo-el-proceso-con-liferay-incluye-podcast/

[^6_2]: https://base22.com/es/blog-es/dxp-vs-cms-cual-es-mejor-para-negocio/

[^6_3]: https://digitum.um.es/xmlui/bitstream/10201/54364/1/TD_Julio-Soler_2017_.pdf

[^6_4]: https://ticjob.es/cat/treball/programador-senior-drupal-html-javascript/61175

[^6_5]: https://www.hiberus.com/crecemos-contigo/como-construir-un-chatbot-rag-serverless/

[^6_6]: https://travesia.mcu.es/bitstream/10421/5541/1/VCNBP.pdf

[^6_7]: https://dspace.ups.edu.ec/bitstream/123456789/13729/1/Tecnologia y accesibilidad Vol2.pdf

[^6_8]: https://www.congreso.es/public_oficiales/L14/CONG/BOCG/D/BOCG-14-D-373.PDF

