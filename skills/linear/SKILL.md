---
name: linear
description: Crea, actualiza, consulta y gestiona issues en Linear.app directamente desde OpenClaw. Utiliza este skill para operaciones en el backlog de desarrollo o de clientes, gestionar estados, asignar tareas y vincular trabajo entre sesiones y Linear. Activa con frases como "crear issue en Linear", "actualizar Linear", "dame el estado de este issue".
---

# Linear Skill

Este skill permite a OpenClaw interactuar directamente con Linear.app para gestionar tu backlog de desarrollo y tareas de clientes.

## Configuración y autenticación

Para usar este skill, necesitas un token de API de Linear. Por seguridad, no lo guardes directamente en este archivo. Sigue los pasos en `references/linear_api_setup.md` para configurar tu token.

## Core Capabilities

El script principal `scripts/linear.py` se encarga de todas las interacciones con la API de Linear.

### 1. Crear un nuevo Issue

Puedes crear issues con un título, descripción, tipo (development/client), prioridad y estado inicial.

**Uso:**
```bash
python3 skills/linear/scripts/linear.py create-issue \
  --title "Implementar integración de Linear" \
  --description "Desarrollar skill de Linear para crear y gestionar issues." \
  --type "development" \
  --priority "alta" \
  --status "todo"
```

### 2. Actualizar un Issue existente

Modifica el título, descripción, tipo, prioridad o estado de un issue.

**Uso:**
```bash
python3 skills/linear/scripts/linear.py update-issue \
  --issue-id "EASY-123" \
  --status "in-progress" \
  --priority "media"
```

### 3. Consultar detalles de un Issue

Obtén toda la información de un issue específico por su ID.

**Uso:**
```bash
python3 skills/linear/scripts/linear.py get-issue \
  --issue-id "EASY-123"
```

### 4. Listar Issues

Puedes listar issues con filtros por estado, tipo, prioridad o asignado.

**Uso:**
```bash
python3 skills/linear/scripts/linear.py list-issues \
  --status "todo" \
  --type "development" \
  --assigned-to "Isaac"
```

### 5. Añadir un comentario a un Issue

Deja una nota o un seguimiento en un issue.

**Uso:**
```bash
python3 skills/linear/scripts/linear.py add-comment \
  --issue-id "EASY-123" \
  --comment "Se inició el desarrollo del script de Linear."
```

## Flujo de trabajo con easytek.md

Recuerda que `easytek.md` sigue siendo tu bitácora ejecutiva. Después de realizar cualquier operación importante en Linear (crear, actualizar), actualiza también `easytek.md` con un resumen, enlaces al issue de Linear y los próximos pasos.

## Referencias

- `references/linear_api_setup.md`: Instrucciones para la configuración del API key de Linear.
- `references/linear_models.md`: Documentación de los modelos de datos de Linear (estados, tipos, prioridades).
