# Preparar una release

Proyecto `pdf-fotos-a-imagenes`: software Python, licencia `GPL-3.0-only`, con renderizado mediante
`pypdfium2` y código derivado de `msaavedra/autocrop` integrado en `src/autocrop`.

Revisa `VERSION`, `pyproject.toml`, `CHANGELOG.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, pruebas,
seguridad y documentación. Comprueba especialmente que no se hayan reintroducido ejecutables PDF
externos, que el flujo funcione en Windows/Linux/macOS y que cualquier modificación de `autocrop`
conserve sus avisos GPLv3 y de procedencia.

No publiques ni etiquetes automáticamente. Produce primero una propuesta de versión, lista de
cambios, riesgos, comprobaciones realizadas y procedimiento de rollback.
