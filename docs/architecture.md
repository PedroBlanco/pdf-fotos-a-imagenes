# Arquitectura

## Objetivo

Convertir documentos PDF de escaneos fotográficos en archivos de imagen individuales sin depender
de aplicaciones PDF externas y conservando un flujo reproducible en Windows, Linux y macOS.

## Flujo

```text
PDF multipágina
      │
      │ pypdfium2 / PDFium
      ▼
página RGB en memoria
      │
      │ autocrop
      ├─ detección de zonas no pertenecientes al fondo
      ├─ agrupación de cada fotografía
      ├─ corrección opcional de inclinación
      ▼
JPEG/PNG individuales
```

`--keep-pages` añade únicamente una salida auxiliar PNG de las páginas renderizadas. No forma parte
del flujo necesario para extraer las fotografías.

## Componentes

### `src/pdf_fotos_a_imagenes/main.py`

Interfaz CLI. Interpreta opciones, descubre documentos y presenta resultados y avisos.

### `src/pdf_fotos_a_imagenes/processing.py`

Orquesta el procesamiento: abre PDF, renderiza páginas en memoria, invoca `autocrop`, guarda
resultados, gestiona salidas y cierra recursos.

### `src/autocrop/`

Código derivado de `msaavedra/autocrop` GPLv3. Detecta fotografías sobre un fondo aproximadamente
uniforme y puede corregir su giro. La procedencia y las modificaciones locales están documentadas en
`THIRD_PARTY_NOTICES.md`.

## Dependencias de ejecución

- `pypdfium2`: acceso a PDFium y renderizado PDF.
- Pillow: representación y escritura de imágenes.
- NumPy: cálculos utilizados por `autocrop`.

No son requisitos PDFtk, Poppler, Ghostscript, ImageMagick ni PyMuPDF.

## Decisiones

### Renderizado directo

Se renderiza cada página desde el PDF original en vez de dividir previamente el documento. Esto
reduce etapas, archivos temporales y dependencias del sistema.

### Páginas en memoria

La página renderizada se pasa directamente a la detección. Solo se escribe a disco si el usuario
solicita `--keep-pages`.

### Integración de `autocrop`

El código se integra en el árbol para poder aplicar y probar adaptaciones mínimas necesarias para
Python 3 y Pillow modernos. Debido a su licencia, el proyecto completo se distribuye como
`GPL-3.0-only`.

### Calidad

El renderizado se realiza al DPI solicitado. Las páginas temporales no pasan por JPEG. En salida JPEG
se usa calidad 95 por defecto y `subsampling=0`; PNG permanece disponible cuando se desea evitar
compresión con pérdida.

## Límites conocidos

El algoritmo está orientado a fotografías separadas y con contraste suficiente frente al fondo.
Escaneos con fotografías solapadas, márgenes indistinguibles, fondos muy irregulares o elementos
ajenos pueden requerir ajustar `--precision`, `--contrast`, `--shrink` o proporcionar `--background`.
