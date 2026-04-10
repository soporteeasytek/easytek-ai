# FacturaProfesional Discovery

## Estado actual

Investigación inicial completada con estos resultados:

- Sitio principal: `https://app.facturaprofesional.com/admin.php`
- Login: `https://app.facturaprofesional.com/admin.php?action=login`
- API visible sin documentación pública:
  - `https://app.facturaprofesional.com/api`
  - `https://app.facturaprofesional.com/api/`
- Respuesta sin autenticación: `Authentication Required`

## Flujo de autenticación observado

### 1. Usuario
- `op=login`
- `usuario=<correo>`

### 2. Contraseña
- `op=login_password`
- `usuario=<correo>`
- `password=<clave>`

### 3. Elección de 2FA
- `op=login_2fa`
- `usuario=<correo>`
- `opcion_2fa=totp|email|sms`

### 4. TOTP
- `op=login_totp`
- `usuario=<correo>`
- `codigo_totp=<codigo>`

### 5. Configuración de dispositivo
- `op=config_device`
- `usuario=<correo>`
- `confiar=0|1`

### 6. Sesión activa previa
- `op=confirm_login`
- `usuario=<correo>`

## Hipótesis técnica

La autenticación final no depende solo de la cookie principal `FP_PROD_ADMIN`.
También parece requerir valores de dispositivo como:

- `userDevice_uid`
- `userDevice_key`
- posiblemente `userDevice_key2`

El frontend usa IndexedDB (`Dexie`, base `FPMain`) para persistir esos valores y luego los agrega a headers AJAX o al flujo posterior.

## Hallazgos concretos del HAR autenticado

La app usa principalmente endpoints internos en `admin.php?action=...`.

### Clientes

Pantalla:
- `GET admin.php?action=clientes`

Búsqueda:
- `POST admin.php?action=clientes&op=busqueda`

Autocompletado para ventas:
- `POST admin.php?action=ventas_4_4&flw&op=get_clientes_data`
- payload observado: `busqueda`, `es_compra`

Selección del cliente para el documento:
- `POST admin.php?action=cliente_carrito_4_4&flw=on`
- payload observado:
  - `id_cliente`
  - `tipo_documento`
  - `es_compra`
  - `es_anulacion_nota`
  - `es_descuento`

### Servicios / productos

Pantalla de servicios:
- `GET admin.php?action=servicios`

Búsqueda de servicios:
- `POST admin.php?action=servicios&op=busqueda`

Consulta puntual desde ventas:
- `POST admin.php?action=servicios&flw=on&op=busqueda`
- payload observado: `id_servicio`

Agregar item al carrito:
- `POST admin.php?action=agrega_carrito_4_4&flw=on`
- payload observado:
  - `item`
  - `key`
  - `cantidad`
  - `tipo_documento`
  - `es_compra`
  - `es_descuento`

### Ventas / facturas / proformas / notas crédito

Pantallas observadas:
- `GET admin.php?action=ventas_4_4`
- `GET admin.php?action=ventas_4_4&modulo=proforma`
- `POST admin.php?action=ventas_4_4&modulo=nota_credito`

Validación de notas aplicadas:
- `POST admin.php?action=ventas_4_4&op=consulta_notas_aplicada`
- payload observado:
  - `num_maestro`
  - `monto_total`

Procesamiento final confirmado:
- `POST admin.php?action=procesar_venta_4_4&flw=on`
- headers observados:
  - `X-Requested-With: XMLHttpRequest`
  - `Origin: https://app.facturaprofesional.com`
  - `Referer: https://app.facturaprofesional.com/admin.php?action=ventas_4_4`
  - `Content-Type: multipart/form-data; boundary=...`
- respuesta: `application/json`
- tamaño observado de respuesta: ~214-217 bytes

#### Payload real observado para factura (`tipoDocumento=01`)

Cabecera observada:
- `uid_form`
- `codigo_actividad_emisor=9511.0`
- `frm_tipo_cambio_global=467.55`
- `id_cliente[]=4107774`
- `fk_num_maestro=`
- `frm_prec_det=5`
- `frm_prec_otros=2`
- `tipoDocumento=01`
- `frm_plazo_credito=30`
- `lista_correos=`
- `tipo_cambio_cliente=467.55`
- `enviar_factura=1`
- `codigo_actividad_receptor=`
- `tipo_moneda=USD`
- `ver_equivalente=1`
- `input_tipo_cambio_moneda_alt=1.00`
- `input_tipo_cambio=467.55`
- `frm_tipo_doc_fact=01`
- `condicion_venta=02`
- `input_sub_total=5.00000`
- `input_monto_descuento=0.00000`
- `input_porcentaje_impuesto[]=0.65000`
- `input_monto_alt=2641.65750`
- `input_monto_total=5.65000`
- `frm_periodo_facturado=Abril 2026`
- `frm_comentario=Servicios TI al 08/04/26`
- `frm_fecha_emision_contingencia=08-04-2026`
- `last_post=1`
- `formulario_dinamico={}`

Línea observada para `detalle[3640249_1]`:
- `[data_serv]` con JSON del servicio
- `[cabys]=8313100000100`
- `[cantidad]=1`
- `[id_servicio]=3640249`
- `[precio]=5`
- `[descuentos]={}`
- `[impuesto][01][data]={"codigo":"01","codigoIVA":"08","valor":13}`

#### Payload real observado para proforma (`tipoDocumento=99`)

Cabecera observada:
- `frm_modulo=proforma`
- `tipoDocumento=99`
- `frm_tipo_doc_fact=99`
- `frm_fecha_vencimiento_proforma=16-04-2026`
- `id_cliente[]=4107774`
- `condicion_venta=02`
- `tipo_moneda=USD`
- `input_sub_total=114.00000`
- `input_monto_total=128.82000`
- `frm_comentario=Prueba`

Detalle observado:
- mismo servicio base `3640249`
- `precio=114`
- IVA 13%

#### Payload real observado para nota de crédito (`tipoDocumento=03`)

Cabecera observada:
- `frm_modulo=nota_credito`
- `tipoDocumento=03`
- `fk_num_maestro=521`
- `razon_nota=Cancelacion por solicitud del cliente`
- `frm_nc_financiera=`
- `id_cliente[]=4107774`
- `tipo_moneda=USD`
- `input_sub_total=5.00000`
- `input_monto_total=5.65000`

Detalle observado:
- mismo servicio base `3640249`
- `base_imponible=5`
- `precio=5`
- IVA 13%

### Datos reutilizables observados

Servicio observado:
- `id_servicio=3640249`
- código `00113`
- nombre `Servicios profesionales`
- `cabys=8313100000100`
- actividad `9511.0`

Cliente observado:
- `id_cliente=4107774`

### Hacienda / validaciones auxiliares

Consulta de contribuyente:
- `POST admin.php?action=api_hacienda&op=consulta_contribuyente`
- payload observado: `identificacion`
- respuesta: JSON con nombre, tipoIdentificacion, régimen, situación y actividades

Validación CABYS:
- `POST admin.php?action=util.cabys&op=valida_lista`
- payload observado: `lista[]`
- respuesta: JSON con `success`, `validos`, `medicamentos`, `invalidos`

Comprobación de correo:
- `GET admin.php?action=comprobar_correo&op=comprobarCorreo&correo=<correo>`
- también se observó `POST admin.php?action=comprobar_correo&flw=on`

## Qué ya se puede automatizar con bastante confianza

1. Búsqueda de clientes.
2. Búsqueda de servicios/productos.
3. Consulta de contribuyente en Hacienda.
4. Validación CABYS.
5. Selección de cliente e inserción de líneas al carrito.
6. Envío del submit final a `procesar_venta_4_4` para:
   - factura
   - proforma
   - nota de crédito

## Qué falta para un conector robusto

1. Confirmar la respuesta JSON exitosa completa de `procesar_venta_4_4`.
2. Confirmar el endpoint exacto de visualización/descarga de PDF que usa `ver_doc_comp(...)`.
3. Probar si el flujo puede repetirse solo con sesión + requests HTTP, sin navegador real.

## Método recomendado

Con lo ya capturado, el siguiente paso es construir un script experimental que:

1. reciba cookie/sesión válida
2. seleccione cliente
3. agregue línea
4. envíe `procesar_venta_4_4`
5. imprima la respuesta JSON y, si existe, el `doc_comp`

## Indicadores útiles

Buscar llamadas con estos patrones:
- `/api`
- `admin.php?action=`
- `procesar_venta_4_4`
- `agrega_carrito_4_4`
- `cliente_carrito_4_4`
- `get_clientes_data`
- `ver_doc_comp`
- `pdf`

## Riesgos

- La app depende mucho de estado de sesión y carrito en servidor.
- Parte del payload final se arma dinámicamente desde el DOM y `FormData`.
- La respuesta JSON del submit sigue sin venir serializada en los HAR, aunque el request quedó perfectamente capturado.
