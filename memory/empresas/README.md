# Empresas

Repositorio base para expedientes de onboarding y operación por cliente.

## Estructura sugerida

- `plantilla-onboarding.yaml` → plantilla maestra
- `<slug-empresa>/perfil.yaml` → expediente principal del cliente
- `<slug-empresa>/equipos/` → inventario por equipo en JSON o YAML
- `<slug-empresa>/documentos/` → notas, resúmenes, material extraído
- `<slug-empresa>/pendientes.md` → faltantes y tareas operativas

## Flujo

1. OpenClaw captura o importa datos.
2. Se actualiza `perfil.yaml`.
3. Paperclip revisa faltantes y genera seguimiento.
4. Inventarios de Windows/macOS alimentan `equipos/`.
