# Changelog

Todos los cambios relevantes de este proyecto se documentarán aquí.

## [Unreleased]

### Added
- Procesamiento directo de PDF multipágina con `pypdfium2`, sin ejecutables PDF externos.
- Detección, recorte y corrección de giro mediante `msaavedra/autocrop` integrado en el proyecto.
- CLI `pdf-fotos-a-imagenes` para procesar uno o varios PDF o directorios completos.
- Ejecución alternativa mediante `python -m pdf_fotos_a_imagenes`.
- Salida JPEG o PNG, calibración opcional del fondo y conservación opcional de páginas renderizadas.
- Pruebas de integración con PDF sintético multipágina y prueba de `deskew`.
- Comprobación en CI del punto de entrada `python -m pdf_fotos_a_imagenes --help`.
- `requirements.txt` funcional que delega en `pyproject.toml` para evitar duplicar versiones de dependencias.

### Changed
- Licencia del proyecto de MIT a `GPL-3.0-only` por la integración de `msaavedra/autocrop`.
- Adaptaciones mínimas de `autocrop` para coordenadas enteras en Python 3 y Pillow moderno.
- CI valida también la instalación mediante `python -m pip install -r requirements.txt` en Linux, Windows y macOS.
- La CLI vuelve a usar importaciones relativas correctas dentro del paquete; la ejecución directa de `src/pdf_fotos_a_imagenes/main.py` no forma parte de la interfaz soportada.

### Removed
- El flujo inicial de ejemplo del esqueleto del proyecto.
- Cualquier necesidad de PDFtk, PyMuPDF u otras utilidades PDF externas.
