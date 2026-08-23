# Avisos de software de terceros

## msaavedra/autocrop

Este repositorio incorpora código derivado de **msaavedra/autocrop**:

- Proyecto original: https://github.com/msaavedra/autocrop
- Commit de referencia: `87992d775133109ad57c01d31e417df539e04dd8`
- Autor indicado en el código original: Michael Saavedra
- Licencia original: GNU General Public License version 3
- Código integrado: `src/autocrop/`

### Modificaciones locales

Modificado en 2026 para este proyecto:

1. Se añaden identificadores SPDX y se deja constancia del commit de procedencia.
2. Se normalizan a enteros las coordenadas y pasos de muestreo utilizados con Pillow bajo Python 3.
3. Se usa `Image.Resampling.BICUBIC` para compatibilidad con Pillow moderno.
4. Se elimina el dibujo de rectángulos de depuración sobre la imagen fuente durante la iteración.
5. Se realizan ajustes menores de legibilidad sin cambiar el propósito del algoritmo: detectar,
   recortar y, opcionalmente, enderezar fotografías independientes de un escaneo.

Estas modificaciones se distribuyen bajo `GPL-3.0-only` junto con el resto del proyecto.

## pypdfium2 / PDFium

El proyecto depende de `pypdfium2` para renderizar las páginas PDF. `pypdfium2` se distribuye bajo
Apache-2.0 / BSD-3-Clause y las compilaciones de PDFium pueden incorporar licencias adicionales de
sus dependencias. Los paquetes instalados de `pypdfium2` incluyen sus avisos de licencia.

No se copia ni se modifica código de `pypdfium2` dentro de este repositorio.
