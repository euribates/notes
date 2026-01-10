WSL (Windows Subsystem for Linux)
========================================================================

.. tags:: linux, os, windows
   

Qué es el :index:`WSL`
------------------------------------------------------------------------

El **Subsistema de Windows para Linux** (WSL) es una capa de
compatibilidad desarrollada por Microsoft para ejecutar binarios de
Linux (en formato ELF) a partir de Windows 10. A partir de junio de 2019
está disponible WSL versión 2, que incorpora cambios importantes, como
el uso de un núcleo Linux real.


Cómo acceder desde Windows a los ficheros dentro del WSL
------------------------------------------------------------------------

Desde la terminal de Linux se puede ejecutar ``explorer.exe .`` (Hay que
incluir la extensión) para abrir el explorador de archivos en la carpeta
actual.

También, desde el propio explorador, se puede introducir la dirección
``\\wsl$`` en la barra de direcciones para abrir la carpeta raíz del
WSL.
