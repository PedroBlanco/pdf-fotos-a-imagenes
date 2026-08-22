# Instrucciones para agentes — pdf-fotos-a-imagenes

## Propósito
Trabajar sobre un proyecto de tipo **software**, lenguaje **python**, manteniendo cambios pequeños, revisables, reproducibles y seguros.

## Contexto generado
Consulte `.github/codex/project-context.md`. Sus valores reflejan decisiones reales de generación; `No aplica` significa que esa opción no corresponde a este tipo de proyecto.

## Estructura
- `.github/`: CI, plantillas de colaboración y contexto/prompts de Codex.
- `docs/`: documentación mantenida junto al código o proyecto.
- `scripts/`: comandos repetibles de comprobación, seguridad y mantenimiento.
- `src/` y `tests/`: implementación y pruebas cuando correspondan.

## Comandos de trabajo
- Bash: `./scripts/check.sh` y `./scripts/security.sh`
- PowerShell: `./scripts/check.ps1` y `./scripts/security.ps1`

## Reglas de trabajo
1. Lea primero este archivo y cualquier `AGENTS.md` más cercano al archivo modificado.
2. Limite el cambio al objetivo de la tarea y evite refactorizaciones laterales no solicitadas.
3. Añada o actualice pruebas y documentación cuando cambie comportamiento.
4. Mantenga los comandos automatizables y no interactivos siempre que sea posible.
5. No desactive controles para lograr que una comprobación pase.

## Criterios de finalización
- Criterios de aceptación satisfechos.
- Comprobaciones relevantes ejecutadas y resultados comunicados.
- Riesgos, supuestos y límites documentados.
- Sin secretos, credenciales ni datos sensibles introducidos por el cambio.
- Documentación y changelog actualizados cuando corresponda.

## Requieren aprobación humana explícita
- Publicar una release o crear etiquetas.
- Hacer `push` a ramas protegidas.
- Cambiar secretos, permisos, reglas de protección o configuración de producción.
- Ejecutar migraciones destructivas o cambios irreversibles.
- Instalar software globalmente o modificar sistemas fuera del repositorio.

## Operaciones prohibidas
- Incluir claves, tokens, contraseñas, certificados privados o credenciales.
- Saltarse pruebas, análisis o revisiones ocultando errores.
- Borrar datos o archivos ajenos a la tarea.
- Ejecutar despliegues reales desde una tarea de análisis o revisión.
- Alterar historial compartido sin autorización.

## Code review
Revise corrección, alcance, pruebas, seguridad, compatibilidad, documentación, dependencias y posibilidad de rollback. Señale explícitamente lo no verificado.

## Secretos y datos
Use `.env.example` solo con nombres y valores ficticios. Los ficheros `.env`, claves privadas y credenciales están ignorados por Git. No copie secretos a worktrees.
