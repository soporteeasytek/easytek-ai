# Agente de Billing, especificación inicial

## Objetivo

Crear un agente en Paperclip especializado en billing y cuentas por cobrar.

## Responsabilidades iniciales

1. Leer `contabilidad.md` diariamente.
2. Consultar Freshservice para clientes configurados.
3. Detectar tickets nuevos desde el último corte o último ticket facturado.
4. Consolidar tiempos reales registrados en Freshservice.
5. Redondear el total al cuarto de hora más cercano.
6. Preparar borradores de facturación por cliente.
7. Identificar tickets de clientes fuera de contrato.
8. Crear o actualizar issues de seguimiento en Paperclip.
9. Preparar recordatorios de cuentas por cobrar.

## Clientes iniciales

- Shortcuts
- Statera Outsourcing
- Trapp Hotel Monteverde

## Rutinas sugeridas

### Rutina diaria ligera
- Leer `contabilidad.md`
- Revisar tickets nuevos por cliente
- Actualizar borradores y observaciones
- Detectar anomalías o tickets sin clasificar

### Rutina fuerte del día 15
- Consolidar el periodo mensual
- Generar resumen de facturación por cliente
- Separar clientes con contrato y fuera de contrato
- Generar seguimiento de cobros
- Preparar resumen para WhatsApp o revisión manual

## Regla de redondeo

- Tomar el tiempo real de Freshservice
- Redondear solo el total final al múltiplo de 15 minutos más cercano

## Clasificación contractual requerida

Cada cliente debe tener uno de estos estados:
- con contrato
- fuera de contrato
- mixto

## Integraciones futuras

- WhatsApp para avisos y seguimiento
- FacturaProfesional para facturas emitidas y pendientes
- Paperclip para issues y workflow interno

## Nota importante sobre dinero

Para evitar problemas con `$` al crear texto vía shell o automatizaciones:
- guardar montos numéricos en metadata cuando sea posible
- renderizar el símbolo `$` solo en la presentación final
