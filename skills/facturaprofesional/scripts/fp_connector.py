#!/usr/bin/env python3
import argparse
import json
import sys
from urllib import parse, request

BASE = "https://app.facturaprofesional.com/"


class FPClient:
    def __init__(self, cookie: str, user_device_uid: str = "", user_device_key: str = "", user_device_key2: str = "", app_version: str = "", sess_empresa: str = "", sess_sucursal: str = "", sess_terminal: str = "", sess_usuario: str = "", admin_sess_update: str = "1", time_init: str = "0", time_sess: str = "0"):
        self.cookie = cookie
        self.user_device_uid = user_device_uid
        self.user_device_key = user_device_key
        self.user_device_key2 = user_device_key2
        self.app_version = app_version
        self.sess_empresa = sess_empresa
        self.sess_sucursal = sess_sucursal
        self.sess_terminal = sess_terminal
        self.sess_usuario = sess_usuario
        self.admin_sess_update = admin_sess_update
        self.time_init = time_init
        self.time_sess = time_sess

    def _req(self, url: str, data=None, multipart=False):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": BASE.rstrip('/'),
            "Referer": BASE + "admin.php?action=ventas_4_4",
            "Cookie": self.cookie,
        }
        if self.user_device_uid:
            headers["userDevice-uid"] = self.user_device_uid
        if self.user_device_key:
            headers["userDevice-key"] = self.user_device_key
        if self.user_device_key2:
            headers["userDevice-key2"] = self.user_device_key2
        if self.app_version:
            headers["App-Version"] = self.app_version
        if self.sess_empresa:
            headers["Sess-Empresa"] = self.sess_empresa
        if self.sess_sucursal:
            headers["Sess-Sucursal"] = self.sess_sucursal
        if self.sess_terminal:
            headers["Sess-Terminal"] = self.sess_terminal
        if self.sess_usuario:
            headers["Sess-Usuario"] = self.sess_usuario
        if self.admin_sess_update:
            headers["admin-sess-update"] = self.admin_sess_update
        if self.time_init:
            headers["time_init"] = self.time_init
        if self.time_sess:
            headers["time_sess"] = self.time_sess
        body = None
        if data is not None and not multipart:
            body = parse.urlencode(data, doseq=True).encode()
        elif data is not None and multipart:
            boundary = "----OpenClawFacturaProfesionalBoundary"
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
            chunks = []
            for key, value in data:
                chunks.append(f"--{boundary}\r\n".encode())
                chunks.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
                chunks.append(str(value).encode())
                chunks.append(b"\r\n")
            chunks.append(f"--{boundary}--\r\n".encode())
            body = b"".join(chunks)
        req = request.Request(url, data=body, headers=headers)
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            return resp.status, ctype, raw

    def get_version(self):
        return self._req(BASE + "admin.php?action=version")

    def ack_version(self):
        return self._req(BASE + "admin.php?action=version&op=dont_show_again&flw=on")

    def search_clients(self, query: str, es_compra: int = 0):
        return self._req(
            BASE + "admin.php?action=ventas_4_4&flw&op=get_clientes_data",
            {"busqueda": query, "es_compra": es_compra},
        )

    def select_client(self, client_id: int, tipo_documento: str, es_compra: int = 0, es_anulacion_nota: int = 0, es_descuento: int = 0):
        return self._req(
            BASE + "admin.php?action=cliente_carrito_4_4&flw=on",
            {
                "id_cliente": client_id,
                "tipo_documento": tipo_documento,
                "es_compra": es_compra,
                "es_anulacion_nota": es_anulacion_nota,
                "es_descuento": es_descuento,
            },
        )

    def add_item(self, item_id: int, tipo_documento: str, cantidad: int = 1, key: int = 1, es_compra: int = 0, es_descuento: int = 0):
        return self._req(
            BASE + "admin.php?action=agrega_carrito_4_4&flw=on",
            {
                "item": item_id,
                "key": key,
                "cantidad": cantidad,
                "tipo_documento": tipo_documento,
                "es_compra": es_compra,
                "es_descuento": es_descuento,
            },
        )

    def process_document(self, fields):
        return self._req(
            BASE + "admin.php?action=procesar_venta_4_4&flw=on",
            fields,
            multipart=True,
        )


def build_proforma_payload(args):
    return [
        ("uid_form", args.uid_form),
        ("codigo_actividad_emisor", args.codigo_actividad_emisor),
        ("frm_tipo_cambio_global", args.tipo_cambio),
        ("id_cliente[]", args.client_id),
        ("fk_num_maestro", ""),
        ("frm_prec_det", args.precio),
        ("frm_prec_otros", "2"),
        ("frm_modulo", "proforma"),
        ("tipoDocumento", "99"),
        ("form-field-select-3", ""),
        ("frm_plazo_credito", args.plazo_credito),
        ("lista_correos", ""),
        ("tipo_cambio_cliente", args.tipo_cambio),
        ("enviar_factura", "1"),
        ("tipo_moneda", args.moneda),
        ("ver_equivalente", "1"),
        ("input_tipo_cambio_moneda_alt", "1.00"),
        ("input_tipo_cambio", args.tipo_cambio),
        ("frm_tipo_doc_fact", "99"),
        ("condicion_venta", args.condicion_venta),
        ("form-field-select-4", ""),
        (f"detalle[{args.item_id}_1][data_serv]", args.data_serv_json),
        (f"detalle[{args.item_id}_1][linea_opciones]", ""),
        (f"detalle[{args.item_id}_1][base_imponible]", ""),
        (f"detalle[{args.item_id}_1][cabys]", args.cabys),
        (f"detalle[{args.item_id}_1][tipo_transaccion]", ""),
        (f"detalle[{args.item_id}_1][cantidad]", args.cantidad),
        (f"detalle[{args.item_id}_1][id_servicio]", args.item_id),
        (f"detalle[{args.item_id}_1][descripcion]", ""),
        (f"detalle[{args.item_id}_1][precio]", args.precio),
        (f"detalle[{args.item_id}_1][descuentos]", "{}"),
        (f"detalle[{args.item_id}_1][impuesto][01][data]", args.impuesto_json),
        (f"detalle[{args.item_id}_1][impuesto][01][exon]", ""),
        ("input_sub_total", args.sub_total),
        ("input_monto_descuento", "0.00000"),
        ("input_porcentaje_impuesto[]", args.monto_impuesto),
        ("input_monto_alt", args.monto_alt),
        ("input_monto_total", args.total),
        ("frm_fecha_vencimiento_proforma", args.fecha_vencimiento),
        ("frm_grupo_comercial", ""),
        ("frm_periodo_facturado", ""),
        ("frm_comentario", args.comentario),
        ("estado_factura", ""),
        ("nombre_comercial", ""),
        ("last_post", "1"),
        ("formulario_dinamico", "{}"),
    ]


def main():
    p = argparse.ArgumentParser(description="FacturaProfesional experimental connector")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("search-clients")
    s1.add_argument("--cookie", required=True)
    s1.add_argument("--user-device-uid", default="")
    s1.add_argument("--user-device-key", default="")
    s1.add_argument("--user-device-key2", default="")
    s1.add_argument("--app-version", default="")
    s1.add_argument("--sess-empresa", default="")
    s1.add_argument("--sess-sucursal", default="")
    s1.add_argument("--sess-terminal", default="")
    s1.add_argument("--sess-usuario", default="")
    s1.add_argument("--admin-sess-update", default="1")
    s1.add_argument("--time-init", default="0")
    s1.add_argument("--time-sess", default="0")
    s1.add_argument("--query", required=True)

    s2 = sub.add_parser("create-proforma")
    s2.add_argument("--cookie", required=True)
    s2.add_argument("--user-device-uid", default="")
    s2.add_argument("--user-device-key", default="")
    s2.add_argument("--user-device-key2", default="")
    s2.add_argument("--app-version", default="")
    s2.add_argument("--sess-empresa", default="")
    s2.add_argument("--sess-sucursal", default="")
    s2.add_argument("--sess-terminal", default="")
    s2.add_argument("--sess-usuario", default="")
    s2.add_argument("--admin-sess-update", default="1")
    s2.add_argument("--time-init", default="0")
    s2.add_argument("--time-sess", default="0")
    s2.add_argument("--uid-form", required=True)
    s2.add_argument("--client-id", required=True)
    s2.add_argument("--item-id", required=True)
    s2.add_argument("--data-serv-json", required=True)
    s2.add_argument("--cabys", required=True)
    s2.add_argument("--precio", required=True)
    s2.add_argument("--cantidad", default="1")
    s2.add_argument("--tipo-cambio", default="467.55")
    s2.add_argument("--codigo-actividad-emisor", default="9511.0")
    s2.add_argument("--moneda", default="USD")
    s2.add_argument("--condicion-venta", default="02")
    s2.add_argument("--plazo-credito", default="30")
    s2.add_argument("--sub-total", required=True)
    s2.add_argument("--monto-impuesto", required=True)
    s2.add_argument("--monto-alt", required=True)
    s2.add_argument("--total", required=True)
    s2.add_argument("--fecha-vencimiento", required=True)
    s2.add_argument("--comentario", default="")
    s2.add_argument("--impuesto-json", default='{"codigo":"01","codigoIVA":"08","valor":13}')

    args = p.parse_args()
    client = FPClient(
        args.cookie,
        args.user_device_uid,
        args.user_device_key,
        args.user_device_key2,
        args.app_version,
        args.sess_empresa,
        args.sess_sucursal,
        args.sess_terminal,
        args.sess_usuario,
        args.admin_sess_update,
        args.time_init,
        args.time_sess,
    )

    if args.cmd == "search-clients":
        status, ctype, raw = client.search_clients(args.query)
        print(json.dumps({"status": status, "contentType": ctype, "body": raw.decode("utf-8", "ignore")}, ensure_ascii=False, indent=2))
        return

    if args.cmd == "create-proforma":
        status, ctype, raw = client.get_version()
        sys.stderr.write(f"get_version status={status} contentType={ctype} body={raw.decode('utf-8', 'ignore')[:300]}\n")
        status, ctype, raw = client.ack_version()
        sys.stderr.write(f"ack_version status={status} contentType={ctype} body={raw.decode('utf-8', 'ignore')[:300]}\n")
        status, ctype, raw = client.select_client(args.client_id, "99")
        sys.stderr.write(f"select_client status={status} contentType={ctype}\n")
        status, ctype, raw = client.add_item(args.item_id, "99", cantidad=args.cantidad)
        sys.stderr.write(f"add_item status={status} contentType={ctype}\n")
        payload = build_proforma_payload(args)
        status, ctype, raw = client.process_document(payload)
        print(json.dumps({"status": status, "contentType": ctype, "body": raw.decode("utf-8", "ignore")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
