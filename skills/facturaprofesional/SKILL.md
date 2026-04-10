---
name: facturaprofesional
description: Descubrir y automatizar FacturaProfesional para creación de facturas, búsqueda de clientes, consulta de productos, descarga de PDF y tareas relacionadas. Usar cuando se necesite investigar la API o el flujo web autenticado de https://app.facturaprofesional.com, mapear endpoints internos, o ejecutar operaciones repetibles de facturación desde OpenClaw.
---

# FacturaProfesional

## Overview

Usar esta skill para trabajar con FacturaProfesional de forma segura y repetible.

Primero priorizar API autenticada. Si la API pública o privada no alcanza, usar descubrimiento del flujo web autenticado y solo después considerar automatización de UI.

## Workflow

1. Confirmar acceso válido.
2. Reproducir el login completo sin marcar dispositivos como confiables salvo instrucción explícita.
3. Identificar cómo queda autenticada la sesión: cookies, headers, tokens o claves de dispositivo.
4. Mapear endpoints útiles para clientes, productos, facturas y PDFs.
5. Probar lecturas antes de escrituras.
6. Solo automatizar creación de facturas cuando el payload y la respuesta estén claros.

## Current findings

Hallazgos ya confirmados durante la investigación inicial:

- El login vive en `admin.php?action=login`.
- El flujo de acceso es por etapas:
  - `op=login` con usuario
  - `op=login_password` con contraseña
  - `op=login_2fa` para escoger método 2FA
  - `op=login_totp` para validar TOTP
  - `op=config_device` para decidir si confiar o no en el dispositivo
- Existe `https://app.facturaprofesional.com/api` y responde `Authentication Required` sin sesión válida.
- La sesión final parece depender de cookies y estado de dispositivo que el navegador consolida después del paso `config_device`.

## Operating rules

- No guardar credenciales en el SKILL.md, scripts versionados, ni respuestas de chat.
- Guardar secretos solo en 1Password o archivos locales no versionados.
- Preferir `confiar=0` en pruebas para no dejar el host marcado como confiable.
- Antes de crear una factura real, validar el payload con una operación de lectura o en ambiente de prueba si existe.
- Si el sitio cambia el flujo de login, actualizar `references/discovery.md` y los scripts.

## References

- Leer `references/discovery.md` para el flujo observado, endpoints candidatos y notas de sesión.

## Scripts

- Usar `scripts/fp_login_probe.py` para repetir el flujo de login y diagnosticar en cuál paso falla.
- Extender el script para listar endpoints autenticados o probar operaciones concretas cuando ya se entienda la sesión.
