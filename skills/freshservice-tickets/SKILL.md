---
name: freshservice-tickets
description: Crea tickets, publica replies operativos, agrega notas privadas y cierra tickets en Freshservice por API.
---

# Freshservice Tickets Skill

Este skill recibe texto dictado o transcrito, normaliza requester y empresa contra catálogos locales, crea tickets y además permite responder tickets existentes, agregar notas privadas y cerrarlos.

## Credenciales

Usa las credenciales guardadas en `~/.openclaw/workspace/.freshservice.env`.

## Datos de apoyo

Archivos usados por el skill:

- `data/freshservice-companies.json`
- `data/freshservice-requesters.json`
- `data/manual-company-aliases.json`
- `data/manual-requester-aliases.json`

## Comandos

### 0. `chat`
Capa conversacional para que el skill decida solo si debe crear ticket, publicar reply, agregar nota privada, cerrar o consultar.

```bash
python3 scripts/freshservice-tickets.py chat \
  --text "crea ticket para isaacmb@gmail.com por configuración de mac para Isaac" \
  --email "isaacmb@gmail.com" \
  --preview
```

Ejemplos válidos:
- `crea ticket para Isaac por configuración de equipo Mac`
- `agregale reporte al INC-29748 acciones: se revisó wifi; se reinició outlook pendientes: monitorear`
- `ponle nota privada al INC-29748 cliente llamó y confirma ventana`
- `cerrá el INC-29748 porque ya quedó validado con el usuario`
- `consulta ticket INC-29748`


### 1. `voice-command`
Crea ticket nuevo desde texto dictado/transcrito.

```bash
python3 scripts/freshservice-tickets.py voice-command \
  --transcript "crea un ticket incidencia para Abraham Retana empresa ARA equipo LT-203 no funciona el correo aprobado por Isaac" \
  --email "aretana@araexportscr.com" \
  --preview
```

### 2. `reply-report`
Publica un **reply público** al ticket con el formato operativo de atención.

```bash
python3 scripts/freshservice-tickets.py reply-report \
  --ticket "INC-29748" \
  --actions "Se validó conectividad; Se reinició Outlook" \
  --pending "Monitorear comportamiento" \
  --preview
```

Formato generado:

```text
Reporte de atención de ticket #INC-29748.

Acciones:
- ...

Pendientes:
- ...
```

Si no hay contenido, deja `-` en la sección.

### 3. `add-note`
Agrega una **nota privada** al ticket.

```bash
python3 scripts/freshservice-tickets.py add-note \
  --ticket "INC-29748" \
  --note "Cliente confirmó ventana de mantenimiento para mañana." \
  --preview
```

### 4. `close-ticket`
Cierra un ticket por API.

```bash
python3 scripts/freshservice-tickets.py close-ticket \
  --ticket "INC-29748" \
  --resolution-note "Caso resuelto y validado con el usuario." \
  --preview
```

### 5. `get-ticket`
Consulta un ticket existente.

```bash
python3 scripts/freshservice-tickets.py get-ticket --ticket "INC-29748"
```

## Modo preview

Los comandos operativos principales aceptan `--preview` para ver el resultado antes de enviarlo.

## Reglas actuales

- Match de empresa por dominio y alias.
- Match de requester por correo exacto y alias.
- Warnings cuando hay ambigüedad.
- Subject dinámico para creación de tickets.
- Reply-report siempre usa formato fijo de atención.
- Add-note crea nota privada.
- Close-ticket actualiza el estado del ticket.

## Pendiente para siguientes iteraciones

- parser más fino para separar mejor empresa/reporte/acción
- confirmación interactiva cuando haya ambigüedad fuerte
- búsquedas más avanzadas por requester o empresa
