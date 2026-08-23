# Instrucciones para agentes — pdf-fotos-a-imagenes

## Propósito

Mantener una aplicación Python multiplataforma que extrae fotografías individuales de PDF
escaneados, con renderizado mediante `pypdfium2`/PDFium y detección/deskew mediante código derivado
de `msaavedra/autocrop` integrado en `src/autocrop`.

## Arquitectura obligatoria

- El PDF multipágina se abre y renderiza directamente desde Python.
- No se requieren ni deben introducirse ejecutables PDF externos salvo una decisión explícita y
  justificada del proyecto.
- No se crean PDF de una sola página como etapa intermedia.
- Las páginas renderizadas se mantienen en memoria; `--keep-pages` permite conservar PNG solo para
  revisión.
- La salida son fotografías JPEG o PNG independientes.
- Plataformas objetivo: Windows, Linux y macOS.

Consulte `docs/architecture.md`, `.github/codex/project-context.md` y `THIRD_PARTY_NOTICES.md` antes
de modificar dependencias o el motor de imagen.

## Licencia y terceros

El proyecto es `GPL-3.0-only`. `src/autocrop` deriva de `msaavedra/autocrop` GPLv3. Al modificar ese
código deben conservarse los avisos de copyright, licencia, procedencia y modificaciones locales.

## Comprobaciones

Linux/macOS:

```bash
bash scripts/check.sh
bash scripts/security.sh
```

PowerShell 7+:

```powershell
./scripts/check.ps1
./scripts/security.ps1
```

CI debe validar el código en Windows, Linux y macOS.

## Reglas de trabajo

1. Mantenga cambios pequeños, revisables y reproducibles.
2. Añada o actualice pruebas cuando cambie comportamiento.
3. No desactive controles para conseguir que una comprobación pase.
4. Cierre recursos PDF e imágenes explícitamente para evitar fugas en lotes grandes.
5. Evite pérdida de calidad y conversiones intermedias innecesarias.
6. No introduzca secretos, credenciales ni fotografías reales en pruebas.
7. Use imágenes/PDF sintéticos en el repositorio y en CI.

## Requieren aprobación humana explícita

- Fusionar en una rama protegida si la política del repositorio lo exige.
- Publicar una release o crear etiquetas.
- Cambiar secretos, permisos o reglas de protección.
- Alterar historial compartido fuera del alcance solicitado.

## Criterios de finalización

- Criterios de aceptación satisfechos.
- Ruff, mypy y pytest correctos.
- CI multiplataforma correcto.
- Controles de seguridad correctos.
- Documentación y changelog coherentes.
- Sin código, dependencias ni instrucciones obsoletas relacionadas con arquitecturas descartadas.
