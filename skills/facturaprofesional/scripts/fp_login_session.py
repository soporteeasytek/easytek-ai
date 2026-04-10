#!/usr/bin/env python3
import argparse
import base64
import hashlib
import hmac
import http.cookiejar
import json
import struct
import sys
import time
from urllib import parse, request

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
    encoded = parse.urlencode(data).encode()
    req = request.Request(
        LOGIN_URL,
        data=encoded,
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    with opener.open(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "ignore")


def main():
    p = argparse.ArgumentParser(description="Login probe for FacturaProfesional")
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--totp-secret", required=True)
    p.add_argument("--trust-device", action="store_true")
    args = p.parse_args()

    jar = http.cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(jar))

    outputs = []
    outputs.append({"step": "login", "body": post(opener, {"op": "login", "usuario": args.user})})
    outputs.append({"step": "password", "body": post(opener, {"op": "login_password", "usuario": args.user, "password": args.password})})
    outputs.append({"step": "select_2fa", "body": post(opener, {"op": "login_2fa", "usuario": args.user, "opcion_2fa": "totp"})})
    code = make_totp(args.totp_secret)
    outputs.append({"step": "totp", "code": code, "body": post(opener, {"op": "login_totp", "usuario": args.user, "codigo_totp": code})})
    outputs.append({"step": "config_device", "body": post(opener, {"op": "config_device", "usuario": args.user, "confiar": "1" if args.trust_device else "0"})})

    last = outputs[-1]["body"]
    if "confirm_login" in last:
        outputs.append({"step": "confirm_login", "body": post(opener, {"op": "confirm_login", "usuario": args.user})})

    result = {
        "cookies": [{"name": c.name, "value": c.value} for c in jar],
        "steps": outputs,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
