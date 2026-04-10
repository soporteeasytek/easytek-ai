#!/usr/bin/env python3
import argparse
import base64
import hashlib
import hmac
import http.cookiejar
import json
import struct
import time
import urllib.parse
import urllib.request

LOGIN_URL = "https://app.facturaprofesional.com/admin.php?action=login"


def make_totp(secret: str, digits: int = 6, period: int = 30) -> str:
    normalized = "".join(secret.strip().split()).upper()
    padded = normalized + ("=" * ((8 - len(normalized) % 8) % 8))
    key = base64.b32decode(padded)
    counter = int(time.time() // period)
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)


def post(opener, data):
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        LOGIN_URL,
        data=encoded,
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    with opener.open(req, timeout=20) as resp:
        return resp.read().decode("utf-8", "ignore")


def main():
    parser = argparse.ArgumentParser(description="Probe FacturaProfesional login flow")
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--totp-secret")
    parser.add_argument("--trust-device", action="store_true")
    args = parser.parse_args()

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    outputs = []
    outputs.append({"step": "login", "response": post(opener, {"op": "login", "usuario": args.user})})
    outputs.append({
        "step": "password",
        "response": post(opener, {"op": "login_password", "usuario": args.user, "password": args.password}),
    })

    if args.totp_secret:
        outputs.append({
            "step": "select_2fa",
            "response": post(opener, {"op": "login_2fa", "usuario": args.user, "opcion_2fa": "totp"}),
        })
        code = make_totp(args.totp_secret)
        outputs.append({
            "step": "totp",
            "code": code,
            "response": post(opener, {"op": "login_totp", "usuario": args.user, "codigo_totp": code}),
        })
        outputs.append({
            "step": "config_device",
            "response": post(
                opener,
                {"op": "config_device", "usuario": args.user, "confiar": "1" if args.trust_device else "0"},
            ),
        })

    result = {
        "cookies": [{"name": c.name, "value": c.value} for c in jar],
        "steps": outputs,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
