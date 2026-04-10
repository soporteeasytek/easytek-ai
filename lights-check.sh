#!/usr/bin/env bash
# lights-check.sh
# Revisa el estado y consumo de dispositivos IoT (Govee y Tuya).
# Corre 5pm-12am hora Costa Rica.

set -euo pipefail

source "$(dirname "$0")/../.env.iot"
GOVEE_KEY="${GOVEE_API_KEY:-}"
REPORT=""
WARNINGS=""

# --- Govee ---
if [[ -n "$GOVEE_KEY" ]]; then
  echo "📡 Consultando Govee..."
  GOVEE_DEVICES=(
    "80:12:A4:C1:38:FB:0E:E5:H6160:Cocina"
    "B1:C1:A4:C1:38:70:37:A1:H6160:Luces exteriores"
    "05:C3:A4:C1:38:F8:7C:83:H6109:Pared-Cuarto"
    "4B:60:A4:C1:38:2B:E9:E6:H6109:Gym"
    "B5:71:D1:C7:C0:C6:60:1F:H6076:Floor Lamp"
  )
  for entry in "${GOVEE_DEVICES[@]}"; do
    IFS=':' read -r -a parts <<< "$entry"
    DEVICE_ID="${parts[0]}:${parts[1]}:${parts[2]}:${parts[3]}:${parts[4]}:${parts[5]}:${parts[6]}:${parts[7]}"
    MODEL="${parts[8]}"
    ROOM="${parts[9]}"

    RESP=$(curl --silent --max-time 8 \
      -H "Govee-API-Key: $GOVEE_KEY" \
      "https://developer-api.govee.com/v1/devices/state?device=$(python3 -c 'import urllib.parse; print(urllib.parse.quote("$DEVICE_ID"))')&model=$MODEL" 2>/dev/null) || {
      WARNINGS+="❌ Govee ${ROOM}: sin respuesta\n"
      continue
    }

    STATE=$(echo "$RESP" | python3 -c "import sys, json
try:
    data = json.load(sys.stdin)
    props = data['data']['properties']
    state = props[0]['powerState']
    brightness = props[0]['brightness']
    print(f'Estado: {{state}}, Brillo: {{brightness}}');
except Exception as e:
    print(f'ERROR: {{e}}')
")

    if [[ "$STATE" == ERROR* ]]; then
      WARNINGS+="⚠️ Govee ${ROOM}: no se pudo leer estado\n"
    else
      REPORT+= "💡 ${ROOM}: estado - $STATE \n"
    fi
  done
else
  echo "⚠️  GOVEE_API_KEY no configurada — saltando dispositivos Govee"
fi

# --- TUYA ---
# Dispositivos Tuya conectados a la red local
DEVICES=(
    "192.168.110.175:niibwa9h8haikh8y"
    "192.168.110.61:key7qn3agvymujfp"
    "192.168.110.96:keygg897krt5kk4t"
    "192.168.110.190:niibwa9h8haikh8y"
    "192.168.110.80:key7qn3agvymujfp"
    "192.168.110.224:key7qn3agvymujfp"
    "192.168.110.242:key7qn3agvymujfp"
    "192.168.110.205:keygg897krt5kk4t"
    "192.168.110.124:0g1fmqh6d5io7lcn"
    "192.168.110.37:key7qn3agvymujfp"
    "192.168.110.107:0g1fmqh6d5io7lcn"
)

for entry in "${DEVICES[@]}"; do
    IFS=':' read -r IP PRODUCT_ID <<< "$entry"
    echo "Consultando estado de dispositivo Tuya en $IP con producto $PRODUCT_ID"
    d=tinytuya.Device('$PRODUCT_ID', '$IP', '')  # Instancia del dispositivo Tuya
    d.set_version(3)
    STATE=$(d.status())  # Obtener estado actual del dispositivo

    # Revisar conexiones
    if [[ $? -ne 0 ]]; then
        WARNINGS+="❌ Tuya ${ROOM}: sin respuesta\n"
    else
        REPORT+= "💡 ${ROOM}: estado recibido: $STATE \n"
    fi
done

# Resumen final
echo "=== Fin del check ==="