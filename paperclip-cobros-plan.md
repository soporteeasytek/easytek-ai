# Plan operativo Paperclip, cobros y contabilidad diaria

## Objetivo

Tener un agente que una vez al día revise la información contable base y mantenga control de:

- cuentas por cobrar
- facturas pendientes
- reembolsos por incluir
- suscripciones por renovar o cobrar
- seguimientos vencidos o próximos a vencer

## Fuente principal

- `/Users/isaacmora/.openclaw/workspace/contabilidad.md`

## Acciones diarias del agente

1. Leer `contabilidad.md`.
2. Identificar facturas con estado `pendiente`, `preparada` o `enviada`.
3. Detectar cuentas por cobrar vencidas o cercanas al vencimiento según crédito.
4. Detectar suscripciones cobrables pendientes.
5. Detectar reembolsos pendientes de incluir.
6. Crear o actualizar issues en Paperclip por cliente y periodo.
7. Entregar un resumen diario con pendientes importantes.

## Convención de issues en Paperclip

### Cuentas por cobrar
- `Cobro pendiente - <Cliente> - <Periodo>`

Metadata sugerida:
- cliente
- periodo
- monto
- moneda
- credito_dias
- estado_factura
- estado_cobro
- ruta_fuente

### Suscripciones
- `Suscripción por cobrar - <Cliente> - <Concepto> - <Periodo>`

Metadata sugerida:
- cliente
- concepto
- monto
- periodicidad
- estado
- ruta_fuente

### Reembolsos
- `Reembolso pendiente - <Cliente> - <Concepto> - <Periodo>`

Metadata sugerida:
- cliente
- concepto
- monto
- estado
- ruta_fuente

## Reglas iniciales

- Si una cuenta está `pendiente`, crear issue si no existe.
- Si está `seguimiento`, mantener issue en `in_progress`.
- Si está `pagado`, mover issue a `done`.
- Si pasó la fecha esperada de pago, marcar como `blocked` o `in_progress` con alerta.

## Resumen diario esperado

Formato breve:

- Cuentas por cobrar pendientes
- Cobros vencidos o próximos a vencer
- Suscripciones pendientes
- Reembolsos pendientes
- Próximo corte mensual

## Siguiente paso técnico

Conviene luego pasar `contabilidad.md` a una estructura más parseable, por ejemplo `contabilidad.json` o archivos por cliente, para automatizar mejor la lectura y actualización.

## Notas operativas

- El script actual de `paperclip-connector` funciona para crear issues, pero hay que escapar bien los signos `$` cuando se invoca desde shell para no perder montos en la descripción.
- El agente por defecto guardado en `.paperclip.env` está terminado, por eso para crear issues hubo que asignarlos explícitamente a un agente activo.
- Agente usado para esta fase inicial: `Sales Manager` (`efa0046a-f0cd-4381-8a0f-5603535743e9`).
