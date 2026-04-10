# easytek-linear.md

Guía viva de uso de Linear para easyTEK.

Este documento define cómo usamos Linear y debe mantenerse actualizado cada vez que cambie la estructura, convención o forma de trabajo.

## Propósito

Linear es el sistema principal para gestionar el trabajo de easyTEK.

Su objetivo es dar visibilidad clara de:
- qué se está construyendo
- qué se está operando
- cuál es la prioridad
- qué está bloqueado
- qué sigue después

`easytek.md` sigue existiendo como bitácora ejecutiva y resumen operativo entre sesiones.

---

## Estructura oficial

### Team 1: easyTEK Development
Key: `DEV`

Usar este team para:
- desarrollo de herramientas
- automatizaciones
- integraciones
- agentes y skills
- mejoras internas
- procesos nuevos
- bugs de herramientas o flujos internos

### Team 2: easyTEK Operations
Key: `OPS`

Usar este team para:
- operación diaria
- puesta en marcha de herramientas y automatizaciones
- ejecución de procesos definidos
- seguimiento operativo
- incidencias operativas
- tareas de implementación o uso real de lo construido

---

## Regla principal de clasificación

### Va en `DEV` si:
- hay que construir algo
- hay que mejorar algo técnico
- hay que automatizar un proceso
- hay que crear o ajustar una integración
- hay que corregir una herramienta

### Va en `OPS` si:
- el trabajo ya es ejecución
- se está usando una herramienta ya creada
- es seguimiento operativo
- es una tarea recurrente de operación
- es implementación o despliegue práctico

Si una tarea empieza en construcción y termina en operación, separar en dos issues si eso mejora claridad.

---

## Tipos de issue actuales

Labels disponibles actualmente:
- `Feature`
- `Improvement`
- `Bug`
- `Operation Info`

### Uso recomendado
- `Feature`: nueva capacidad o desarrollo nuevo
- `Improvement`: mejora de proceso, estructura o herramienta existente
- `Bug`: algo roto o incorrecto
- `Operation Info`: documentación operativa, guías, convenciones o referencias internas visibles en Linear

---

## Estados oficiales

Estados detectados en ambos teams:
- `Backlog`
- `Todo`
- `In Progress`
- `In Review`
- `Done`
- `Canceled`
- `Duplicate`

### Significado práctico
- `Backlog`: idea o pendiente sin arrancar
- `Todo`: listo para ejecutarse pronto
- `In Progress`: en trabajo activo
- `In Review`: pendiente de validación o revisión
- `Done`: terminado
- `Canceled`: descartado
- `Duplicate`: duplicado de otro issue

---

## Prioridades

### Uso recomendado
- `Urgente`: bloquea operación o requiere atención inmediata
- `Alta`: importante, debe entrar pronto
- `Media`: importante pero no bloqueante
- `Baja`: mejora futura o deseable

---

## Convención de trabajo

### Regla base
Todo trabajo nuevo de easyTEK debe quedar en Linear.

### Regla de sesión
Si una sesión trabajó en algo relacionado con easyTEK, al terminar debe:
1. actualizar el issue correspondiente en Linear
2. actualizar `easytek.md` con un resumen ejecutivo corto

### Qué debe quedar en `easytek.md`
- qué se hizo
- resultado
- siguiente paso
- issue de Linear relacionado
- bloqueos importantes si existen

---

## Convención de redacción de issues

### Títulos
Usar títulos claros, directos y accionables.

Ejemplos:
- `Diseñar skill para auditoría y estructura de Google Drive`
- `Evaluar agente Paperclip para flujo WhatsApp a Google Drive`
- `Implementar proceso operativo para clasificación de imágenes`

### Descripción
Debe incluir, cuando aplique:
- objetivo
- alcance
- resultado esperado
- restricciones o contexto relevante

---

## Issues iniciales creados

### easyTEK Development
- `DEV-1` Definir estándar de organización para imágenes y datos entrantes
- `DEV-2` Evaluar agente Paperclip para flujo WhatsApp a Google Drive
- `DEV-3` Evaluar agente dedicado en Paperclip para flujo de archivos
- `DEV-4` Diseñar skill para auditoría y estructura de Google Drive

### easyTEK Operations
- Sin issues iniciales documentados todavía.

---

## Relación con otros archivos

### `easytek.md`
Es la bitácora ejecutiva compartida entre sesiones.
No debe reemplazar a Linear como sistema principal de tareas.

### `easytek-linear.md`
Este archivo es la guía viva de convenciones y uso de Linear.
Cada vez que cambie la estructura o la forma de trabajo, se debe actualizar.

---

## Regla de mantenimiento

Siempre que hagamos un cambio en el uso de Linear, debemos actualizar este archivo.

Ejemplos de cambios que obligan actualización:
- creación de nuevos teams
- cambio de estados
- nueva convención de prioridades
- nuevos labels
- nueva forma de clasificar trabajo
- cambio en la relación entre Linear y otros archivos

---

## Última actualización

### 2026-04-09
- Se definió la estructura oficial con dos teams: `easyTEK Development` (`DEV`) y `easyTEK Operations` (`OPS`).
- Se estableció que Linear será el sistema principal de gestión.
- Se estableció que `easytek.md` será la bitácora ejecutiva complementaria.
- Se acordó que cualquier cambio futuro en el uso de Linear debe reflejarse aquí.
- Se creó el label `Operation Info` para issues informativos o de referencia, como la guía operativa en Linear.
