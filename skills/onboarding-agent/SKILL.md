---
name: onboarding-agent
description: Captura, estructura y revisa información de onboarding para clientes de soporte TI. Úsalo para crear expedientes, registrar datos de empresa, contactos, plataformas, seguridad, inventario de equipos y detectar faltantes operativos para seguimiento con Paperclip.
---

# Onboarding Agent

Este skill vive en OpenClaw y funciona como capturador principal de datos para onboarding de clientes.

## Objetivo

- Crear expedientes por empresa
- Registrar información estructurada en `memory/empresas/`
- Detectar faltantes críticos e importantes
- Preparar información para seguimiento con Paperclip
- Ingerir inventarios técnicos de equipos en el futuro

## Archivos principales

- `memory/empresas/plantilla-onboarding.yaml`
- `memory/empresas/<slug-empresa>/perfil.yaml`
- `memory/empresas/<slug-empresa>/pendientes.md`
- `memory/empresas/flujo-openclaw-paperclip.md`

## Casos de uso

### 1. Crear expediente nuevo

Ejemplos:
- "crea expediente de onboarding para Empresa X"
- "inicializa onboarding para Statera"

### 2. Registrar datos de empresa

Ejemplos:
- "agrega como dominio principal stateracr.com"
- "el contacto principal es Ana Gómez, gerente, ana@empresa.com"
- "el servicio de Microsoft 365 se paga el 15 de cada mes"

### 3. Registrar infraestructura

Ejemplos:
- "agrega servidor AWS t3a.xlarge con cuenta aws@empresa.com"
- "registra equipo STATERA-TI003 para Lilliana"

### 4. Revisar faltantes

Ejemplos:
- "qué le falta al onboarding de Statera"
- "muéstrame faltantes críticos de Empresa X"

### 5. Preparar seguimiento para Paperclip

Ejemplos:
- "genera tareas de faltantes para Paperclip"
- "resume pendientes del onboarding"

## Reglas operativas

- La fuente de verdad es `memory/empresas/<slug>/perfil.yaml`
- `pendientes.md` es resumen operativo, no reemplaza el YAML
- Paperclip orquesta seguimiento, pero OpenClaw captura y actualiza datos
- Para datos ambiguos o incompletos, hacer preguntas cortas
- Mantener estructura estable para facilitar automatización futura

## Próxima integración

- ingestión de JSON de inventario para Windows/macOS
- generación automática de tareas en Paperclip por faltantes
- comandos más finos para actualizar secciones específicas
