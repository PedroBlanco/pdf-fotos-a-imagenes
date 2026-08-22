# Procedimiento de rollback

Antes de publicar, identifique la versión estable anterior y la forma de restaurarla. El rollback debe ser ensayable sin destruir datos.

1. Detener el cambio si las validaciones fallan.
2. Conservar logs y evidencia.
3. Restaurar artefactos/configuración de la versión estable.
4. Restaurar datos únicamente desde backups verificados y con autorización.
5. Volver a ejecutar validación y documentar el incidente.
