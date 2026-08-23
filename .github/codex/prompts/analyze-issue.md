# Analizar una issue

Proyecto `pdf-fotos-a-imagenes`: software Python, licencia `GPL-3.0-only`.

Arquitectura actual:
- `pypdfium2`/PDFium abre y renderiza directamente PDF multipágina.
- `src/autocrop` contiene código derivado de `msaavedra/autocrop` GPLv3.
- No hay ejecutables PDF externos ni etapas con PDF intermedios.
- Plataformas objetivo: Windows, Linux y macOS.

Lee `AGENTS.md`, `.github/codex/project-context.md` y `THIRD_PARTY_NOTICES.md`. Analiza la issue
sin modificar archivos. Identifica objetivo, alcance, archivos probables, compatibilidad
multiplataforma, impacto en licencias, riesgos de pérdida/calidad de imagen, pruebas y criterios de
aceptación. Marca como **no verificado** cualquier supuesto que no puedas comprobar.
