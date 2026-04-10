# Linear Models Reference

Este documento describe los modelos de datos clave en Linear.app y cómo se mapean a los argumentos del skill `linear` de OpenClaw.

## 1. Equipos (Teams)

En Linear, los issues pertenecen a un equipo. Necesitarás el ID o el nombre/clave del equipo para crear o listar issues.

-   **ID:** Identificador único del equipo (string largo, ej. `1f2a3b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c`)
-   **Nombre (Name):** Nombre legible del equipo (ej. `EasyTEK Development`)
-   **Clave (Key):** Prefijo corto para los issues del equipo (ej. `EASY`)

**Mapeo en el skill:**
-   `--team-id`: Para especificar por ID.
-   `--team-name`: Para especificar por nombre.
-   `--team-key`: Para especificar por clave.

## 2. Estados de Workflow (Workflow States)

Cada equipo tiene un conjunto de estados para los issues (ej. `Todo`, `In Progress`, `Done`). Estos estados tienen un `name` (visible) y un `type` (categoría interna de Linear).

-   **ID:** Identificador único del estado.
-   **Nombre (Name):** Nombre del estado (ej. `Todo`, `In Progress`, `Done`, `Backlog`).
-   **Tipo (Type):** Categoría interna de Linear (ej. `unstarted`, `started`, `completed`, `canceled`). El skill `linear.py` usa el `name` para crear/actualizar y `type` para filtrar en `list-issues` si se desea.

**Mapeo en el skill:**
-   `--status`: Para crear o actualizar un issue con un estado específico por su `name`.
-   `--status` en `list-issues`: Para filtrar por `type` de estado (ej. `unstarted`).

## 3. Prioridades (Priorities)

Los issues pueden tener diferentes niveles de prioridad.

-   **Valor (Linear API):** Números flotantes (ej. `0.0` para Sin Prioridad, `1.0` para Urgente, etc.).
-   **Nombre (Skill Argumento):** Textos amigables que el skill mapea a los valores numéricos de Linear.

**Mapeo en el skill:**
-   `--priority`: Se espera uno de los siguientes valores:
    -   `sin prioridad` (se mapea a `0.0`)
    -   `urgente` (se mapea a `1.0`)
    -   `alta` (se mapea a `2.0`)
    -   `media` (se mapea a `3.0`)
    -   `baja` (se mapea a `4.0`)

## 4. Tipos de Issue (Issue Types)

Los issues pueden clasificarse en diferentes tipos (ej. `Bug`, `Feature`, `Development`, `Client`).

-   **ID:** Identificador único del tipo de issue.
-   **Nombre (Name):** Nombre legible del tipo (ej. `Bug`, `Feature`).

**Mapeo en el skill:**
-   `--issue-type`: Para especificar el tipo de issue por su `name` al crear o actualizar.

## 5. Asignados (Assignees)

Los issues se pueden asignar a usuarios de Linear.

-   **ID:** Identificador único del usuario.
-   **Nombre (Name):** Nombre del usuario (ej. `Isaac Mora`).
-   **Email (Email):** Email del usuario.

**Mapeo en el skill:**
-   `--assignee`: Se espera el `name` del usuario para asignar un issue.

---

Este documento te ayudará a entender cómo los datos de Linear se usan en el skill y cómo construir tus comandos de manera efectiva.
