# Revisar un cambio

Proyecto `pdf-fotos-a-imagenes`: `software` / `python` / `GPL-3.0-only`.

Arquitectura esperada: PDF multipágina renderizado directamente con `pypdfium2`; detección,
recorte y corrección de giro con el código derivado de `msaavedra/autocrop` integrado en
`src/autocrop`; sin ejecutables PDF externos.

Revisa el diff frente al objetivo, `AGENTS.md`, `.github/codex/project-context.md` y
`THIRD_PARTY_NOTICES.md`. Prioriza defectos, regresiones de calidad de imagen, pérdida de datos,
compatibilidad Windows/Linux/macOS, recursos no cerrados, licencias, dependencias, pruebas y
documentación incorrecta. Señala como regresión cualquier reintroducción innecesaria de un programa
PDF externo. Distingue hallazgos comprobados de sugerencias.
