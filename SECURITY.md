# Política de seguridad

## Reporte
No publique credenciales ni detalles explotables en una issue pública. Use el canal privado de seguridad del repositorio o el canal definido por la organización.

## Principios
- Mínimo privilegio.
- GitHub Actions con `permissions: contents: read` como base.
- Acciones de terceros fijadas por SHA completo y mantenidas con Dependabot.
- Ningún secreto se entrega a código no confiable.
- Gitleaks y Trivy forman parte de los controles recomendados.
- Los cambios sensibles requieren revisión humana.

## Secretos
Nunca confirme `.env`, `.env.local`, `*.pem`, `*.key`, `credentials.json` ni `service-account.json`.
