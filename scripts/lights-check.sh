#!/usr/bin/env bash
# lights-check.sh
# Revisa el estado y consumo de dispositivos IoT (Govee y Tuya).

set -uo pipefail

source "$(dirname "$0")/../.env.iot"
GOVEE_KEY="${GOVEE_API_KEY:-}"
REPORT=""
WARNINGS=""

# --- Govee ---
if [[ -n "$GOVEE_KEY" ]]; then
  echo "📡 Consultando Govee..."
  GOVEE_DEVICES=(
    "80:12:A4:C1:38:FB:0E:E5|H6160|Cocina"
    "B1:C1:A4:C1:38:70:37:A1|H6160|Luces exteriores"
    "05:C3:A4:C1:38:F8:7C:83|H6109|Pared-Cuarto"
    "4B:60:A4:C1:38:2B:E9:E6|H6109|Gym"
    "B5:71:D1:C7:C0:C6:60:1F|H6076|Floor Lamp"
  )
  for entry in "${GOVEE_DEVICES[@]}"; do
    IFS='|' read -r DEVICE_ID MODEL ROOM <<< "$entry"

    ENCODED_ID=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${DEVICE_ID}'))")
    RESP=$(curl --silent --max-time 8 \
      -H "Govee-API-Key: $GOVEE_KEY" \
      "https://developer-api.govee.com/v1/devices/state?device=${ENCODED_ID}&model=${MODEL}" 2>/dev/null) || {
      WARNINGS+="❌ Govee ${ROOM}: sin respuesta\n"
      continue
    }

    STATE=$(echo "$RESP" | python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    props = data["data"]["properties"]
    power = next((p["powerState"] for p in props if "powerState" in p), "?")
    brightness = next((p["brightness"] for p in props if "brightness" in p), "?")
    print(f"power={power} brightness={brightness}")
except Exception as e:
    print(f"ERROR: {e}")
')

    if [[ "$STATE" == ERROR* ]]; then
      WARNINGS+="⚠️ Govee ${ROOM}: no se pudo leer estado ($STATE)\n"
    else
      REPORT+="💡 ${ROOM}: ${STATE}\n"
    fi
  done
else
  echo "⚠️  GOVEE_API_KEY no configurada — saltando dispositivos Govee"
  WARNINGS+="⚠️ GOVEE_API_KEY no configurada\n"
fi

# --- TUYA (pendiente de vincular, solo registro interno) ---
# Los dispositivos Tuya están pendientes de vinculación con cuenta SmartLife.
# Se omiten del check activo hasta completar la configuración OAuth.
TUYA_IPS=(
  "192.168.110.175" "192.168.110.61" "192.168.110.96"
  "192.168.110.190" "192.168.110.80" "192.168.110.224"
  "192.168.110.242" "192.168.110.205" "192.168.110.124"
  "192.168.110.37"  "192.168.110.107"
)
echo "ℹ️  Tuya: ${#TUYA_IPS[@]} dispositivos pendientes de vincular — se omite check activo"

# --- Resumen ---
echo ""
echo "=== REPORTE GOVEE ==="
echo -e "$REPORT"
if [[ -n "$WARNINGS" ]]; then
  echo "=== ALERTAS ==="
  echo -e "$WARNINGS"
fi
echo "=== Fin del check ==="
