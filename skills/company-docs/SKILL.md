---
name: company-docs
description: Documenta y gestiona información estructurada o de texto libre sobre empresas en el workspace. Utiliza esta skill para guardar datos de campo, contactos, o resúmenes que luego serán procesados o referenciados por otros agentes o sistemas (como Paperclip).
---

# Company Docs

Esta skill permite a OpenClaw crear y gestionar documentación sobre empresas en una estructura organizada.

## Estructura de Almacenamiento

La información se guarda en:
`/Users/isaacmora/.openclaw/workspace/memory/empresas/<nombre_empresa>/<timestamp_o_id>.md`

-   Cada empresa tendrá su propia carpeta.
-   Los documentos pueden ser en formato Markdown o JSON, dependiendo del contenido.

## Comandos

### `document-company-info`

Documenta información de una empresa en un nuevo archivo.

```bash
python3 skills/company-docs/scripts/docs.py document-company-info \
  --company-name "Nombre Empresa" \
  --info "Contenido del documento (texto libre o JSON)" \
  [--format "json"|"markdown"]
```

## Workflow de Integración (Documentar → Procesar con Paperclip)

1.  **OpenClaw recibe información** de una empresa (de ti o de alguna fuente).
2.  **OpenClaw usa `company-docs/scripts/docs.py document-company-info`** para guardar esta información en el formato y ruta definidos.
3.  **OpenClaw usa `paperclip-connector/scripts/paperclip.py create-issue`** para crear una tarea en Paperclip, referenciando el documento de empresa recién creado y enviando un resumen o los campos clave para su procesamiento.
    *   El `metadata` del issue en Paperclip incluirá la ruta al documento en el workspace.

## Futuras mejoras

-   Añadir funciones para buscar, listar o actualizar documentos de empresas.
-   Integrar con una base de datos si la cantidad de documentos crece.
