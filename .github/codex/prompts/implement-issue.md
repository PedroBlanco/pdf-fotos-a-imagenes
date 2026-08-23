# Implementar una issue

Trabaja en `pdf-fotos-a-imagenes` (`software`, `python`, `GPL-3.0-only`). Antes de editar, lee
`AGENTS.md`, `.github/codex/project-context.md` y `THIRD_PARTY_NOTICES.md`.

Mantén la arquitectura actual salvo que la issue exija expresamente cambiarla: renderizado directo
de PDF con `pypdfium2` y detección/deskew con el código derivado de `msaavedra/autocrop` integrado en
`src/autocrop`. No introduzcas dependencias en ejecutables PDF externos por conveniencia.

Implementa únicamente el alcance acordado. Conserva compatibilidad con Windows, Linux y macOS,
añade o actualiza pruebas, ejecuta `scripts/check.*` y los controles de seguridad aplicables. Si
modificas código derivado de `autocrop`, conserva avisos de copyright, GPLv3 y la indicación de las
modificaciones. No publiques, no despliegues ni alteres secretos.
