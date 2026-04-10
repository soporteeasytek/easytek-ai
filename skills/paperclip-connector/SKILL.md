---
name: paperclip-connector
description: Interact with the Paperclip API to create tasks, issues, and manage agent workflows. Use when OpenClaw needs to delegate work to Paperclip agents, create new issues for processing by Paperclip, or check on Paperclip task status.
---

# Paperclip Connector

This skill provides helper functions to interact with your local Paperclip instance.

## Configuration

API Key and URL are read from `/Users/isaacmora/.openclaw/workspace/.paperclip.env`.

Example `.paperclip.env`:

```bash
PAPERCLIP_API_URL=http://127.0.0.1:3100
PAPERCLIP_AGENT_API_KEY=pcp_...
PAPERCLIP_COMPANY_ID=51d99c93-d37d-4c3f-ba7e-9805666591aa
PAPERCLIP_AGENT_ID=50260ba5-d37d-4c3f-ba7e-9805666591aa
```

**Do not commit `.paperclip.env` to version control.**

## Workflow

1.  **OpenClaw crea un ticket en Freshservice**. (Ya implementado en `freshservice.py`)
2.  **OpenClaw delega una tarea a Paperclip** usando `paperclip-connector`. Este script creará un `issue` en Paperclip. Este `issue` puede contener la información de la empresa o detalles del ticket de Freshservice para que los agentes de Paperclip lo procesen.
3.  **Paperclip procesa la tarea**. (Gestionado por los agentes de Paperclip)
4.  **Paperclip envía un mensaje a OpenClaw** (o a un webhook de OpenClaw) para que OpenClaw realice acciones en Freshservice (añadir notas, cerrar ticket, añadir timesheets). Esto requiere que Paperclip esté configurado para llamar a OpenClaw.

## Comandos

### `create-issue`

Crea una nueva tarea (issue) en Paperclip para que los agentes la procesen.

```bash
python3 skills/paperclip-connector/scripts/paperclip.py create-issue \
  --company-id "51d99c93-d37d-4c3f-ba7e-9805666591aa" \
  --subject "Procesar informe de empresa X desde Freshservice Ticket 12345" \
  --description "Detalles del informe..."
  --metadata '{"freshservice_ticket_id": 12345, "source_message": "..."}'
```

### `add-private-note`

Permite a Paperclip (vía OpenClaw) agregar una nota privada a un ticket de Freshservice.

```bash
python3 skills/freshservice/scripts/freshservice.py add-note \
  --ticket-id 12345 \
  --body "Informe procesado por Paperclip: [Resumen de lo hecho]" \
  --private
```

### `add-timesheet-and-close`

Permite a Paperclip (vía OpenClaw) agregar un timesheet y cerrar un ticket en Freshservice.

```bash
python3 skills/freshservice/scripts/freshservice.py create-ticket \
  --add-timesheet-and-close \
  --time-spent-on-close "00:30" \
  --close-note "Tarea de Paperclip completada y ticket cerrado."
```

## Futuras mejoras

-   Implementar `GET /api/companies/:companyId/issues` para que OpenClaw pueda monitorear el estado de las tareas en Paperclip.
-   Configurar un webhook en Paperclip para que notifique a OpenClaw directamente cuando una tarea se complete, en lugar de que OpenClaw tenga que hacer polling.
