# Flujo propuesto: OpenClaw + Paperclip para onboarding de clientes

## Objetivo

Usar OpenClaw como capturador e ingestor de datos operativos, y Paperclip como orquestador de completitud, seguimiento y coordinación.

## Roles

### OpenClaw

- Captura datos por chat, texto, PDFs, notas o inventarios de equipos
- Normaliza y actualiza el expediente de empresa
- Detecta campos faltantes
- Puede hacer preguntas cortas para completar secciones
- Resume estado actual del onboarding

### Paperclip

- Mantiene el checklist de onboarding
- Crea tareas por faltantes críticos e importantes
- Coordina seguimiento entre agentes
- Ejecuta rutinas periódicas de revisión de completitud
- Escala cuando faltan datos clave o hay bloqueos

## Fuente de verdad

- Archivos en `memory/empresas/<slug-empresa>/`
- `perfil.yaml` = expediente principal
- `equipos/*.json` = inventario por dispositivo
- `pendientes.md` = resumen operativo de faltantes

## Flujo operativo sugerido

1. Se crea expediente inicial desde plantilla
2. OpenClaw ingiere documentos o conversaciones
3. OpenClaw actualiza `perfil.yaml`
4. Un agente Paperclip revisa `completitud`
5. Paperclip crea tareas por faltantes, por ejemplo:
   - contacto principal faltante
   - seriales de equipos faltantes
   - MFA no verificado
   - servicios sin fecha de renovación
6. OpenClaw recibe indicación concreta de qué falta capturar
7. Al completar datos, OpenClaw actualiza expediente y Paperclip cierra/reduce pendientes

## Rutinas sugeridas en Paperclip

### Rutina 1: Revisión de completitud de onboarding

Frecuencia: diaria o 3 veces por semana

Valida:
- porcentaje de completitud
- faltantes críticos
- checklist pendiente
- equipos sin inventario

### Rutina 2: Seguimiento de vencimientos

Frecuencia: diaria

Valida:
- dominios por vencer
- licencias por vencer
- pagos mensuales/anuales próximos

### Rutina 3: Revisión de seguridad

Frecuencia: semanal o mensual

Valida:
- MFA
- antivirus
- DKIM/SPF/DMARC
- oportunidades de mejora pendientes

## Próximo paso técnico

Crear un agente o skill de onboarding que permita comandos como:

- "crear expediente para cliente X"
- "agrega contacto principal a Statera"
- "registra dominio principal"
- "importa inventario del equipo STATERA-TI003"
- "qué le falta al onboarding de Statera"

## Inventario técnico automático

### Windows
- PowerShell
- WMI/CIM
- apps instaladas
- Defender/antivirus
- BitLocker

### macOS
- system_profiler
- sw_vers
- listado de apps
- FileVault
- perfiles/configuración

Salida recomendada: JSON normalizado por equipo.
