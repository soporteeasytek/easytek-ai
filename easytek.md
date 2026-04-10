# easytek.md

Bitácora operativa y resumen ejecutivo compartido para todo lo relacionado con easyTEK.

Este archivo sirve para que cualquier sesión, agente o flujo tenga contexto rápido de:
- qué se está construyendo
- qué se hizo recientemente
- qué está pendiente
- qué está bloqueado
- qué decisiones ya se tomaron

## Regla de uso para todas las sesiones

Si una sesión trabaja en algo de easyTEK, al cerrar debe actualizar este archivo con:
- un resumen ejecutivo corto de lo que hizo
- pendientes o siguiente paso
- bloqueos, si existen
- referencia a Linear, si ya existe issue

Objetivo: que cualquier sesión nueva pueda ponerse en contexto en menos de 2 minutos.

---

## Resumen ejecutivo actual

Se definió que el control principal de trabajo se llevará en Linear para todo lo relacionado con desarrollo y evolución operativa.

Mientras eso se termina de ordenar, este archivo funciona como bitácora central compartida entre sesiones para conservar contexto ejecutivo, decisiones y pendientes.

También se acordó separar el trabajo en dos líneas principales:
1. easyTEK Development
2. easyTEK Operations

---

## Líneas de trabajo

### 1) easyTEK Development
Incluye:
- automatizaciones
- desarrollo de procesos
- mejoras internas
- integraciones
- skills, agentes y flujos de trabajo internos
- herramientas para soporte y operación

### 2) easyTEK Operations
Incluye:
- puesta en marcha de herramientas y automatizaciones
- operación diaria del soporte
- ejecución de procesos ya definidos
- tareas operativas internas o relacionadas con clientes
- seguimiento operativo e incidencias de ejecución

---

## Pendientes activos

### easyTEK Development

- Evaluar si algún agente existente en Paperclip puede encargarse del flujo de descargar imágenes de WhatsApp y subirlas a Google Drive. Linear: `DEV-2`
- Diseñar un skill para auditar Google Drive y proponer una estructura base de organización de archivos. Linear: `DEV-4`
- Usar ese esquema como estándar futuro para imágenes y datos entrantes desde WhatsApp. Linear: `DEV-1`
- Considerar si luego conviene crear un agente dedicado en Paperclip encima de ese skill. Linear: `DEV-3`

### easyTEK Operations

- Sin pendientes documentados todavía.

---

## Bloqueos actuales

- Existen issues históricos creados antes de la separación final de teams y conviene revisarlos para limpieza.
- Aún no existe una convención cerrada para vincular tareas de sesiones con issues de Linear.


---

## Decisiones tomadas

- Linear será la herramienta principal para llevar el control del trabajo.
- `easytek.md` será la bitácora ejecutiva compartida entre sesiones mientras consolidamos ese sistema.
- `easytek-linear.md` será la guía viva de convenciones y uso de Linear.
- Todo lo que estaba en `pendientesdev.md` se consolida aquí.
- El trabajo se separa en dos teams de Linear: `easyTEK Development` y `easyTEK Operations`.
- `easyTEK Development` será para construir herramientas, procesos, integraciones y automatizaciones.
- `easyTEK Operations` será para ejecutar, operar y dar seguimiento a lo que se pone en marcha.
- Los issues iniciales de desarrollo ya fueron recreados en `easyTEK Development`.

---

## Últimas actualizaciones

### 2026-04-09
- Se creó `easytek.md` como archivo central de contexto operativo para easyTEK.
- Se consolidaron aquí los pendientes que estaban en `pendientesdev.md`.
- Se acordó que futuras sesiones deben dejar resumen ejecutivo y pendientes al cerrar trabajo relacionado con easyTEK.
- Se conectó Linear por API usando inicialmente un team transitorio y luego se consolidó la estructura final.
- Se definió la estructura definitiva con dos teams: `easyTEK Development` (`DEV`) y `easyTEK Operations` (`OPS`).
- Se recrearon en `easyTEK Development` los primeros issues del backlog: `DEV-1`, `DEV-2`, `DEV-3` y `DEV-4`.
- Se creó la base del skill `amazon-quote-cr` con script inicial de cálculo y guía de uso.

---

## Referencias

### Archivos relacionados
- `pendientesdev.md` (origen histórico de parte de estos pendientes)
- `easytek-linear.md` (guía viva de convenciones y uso de Linear)

### Linear
- Teams activos:
  - `easyTEK Development` (`DEV`)
  - `easyTEK Operations` (`OPS`)
- Estados detectados en ambos teams: `Backlog`, `Todo`, `In Progress`, `In Review`, `Done`, `Canceled`, `Duplicate`
- Labels disponibles actualmente: `Feature`, `Bug`, `Improvement`

---

## Plantilla de actualización rápida

Usar este formato cuando una sesión cierre trabajo importante:

### YYYY-MM-DD - Nombre corto del trabajo
- Qué se hizo:
- Resultado:
- Pendiente siguiente:
- Bloqueos:
- Linear:
