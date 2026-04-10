#!/usr/bin/env bash
# temp-check.sh
# Revisa temperatura de todos los cuartos (Sensibo + OMEGA via msmart-ng).
# Rango OK: 26-28°C. Fuera de rango → notifica a Isaac.

set -euo pipefail

source "$(dirname "$0")/../.env.iot"

API="https://home.sensibo.com/api/v2"
SENSIBO_DEVICES=("kgDm9uPz:Oficina" "hCbp45qK:Cocina")

MSMART=/Users/isaacmora/Library/Python/3.9/bin/msmart-ng
OMEGA_IP=192.168.110.231
OMEGA_ID=151732606810840
OMEGA_KEY=7833229f67a74f15864928243cd975a575cf2c5c596845db94a7351831a2d162
OMEGA_TOKEN=30ccae402e287fd0e1f5998d83f0bf0e623ccd64fcb685855af5065805ae32892ed403d5ce4884682cdb2e5400962afb8ff1c671de798b573294908bab9c1b7b

MIN_TEMP=26
MAX_TEMP=28

REPORT=""
ALERTS=""

check_temp() {
  local ROOM="$1"
  local TEMP="$2"

  if [[ "$TEMP" == ERROR* ]] || [[ -z "$TEMP" ]]; then
    ALERTS+="❌ ${ROOM}: no se pudo leer temperatura\n"
    return
  fi

  IN_RANGE=$(python3 -c "
t = float('$TEMP')
print('yes' if $MIN_TEMP <= t <= $MAX_TEMP else 'no')
")

  if [[ "$IN_RANGE" == "yes" ]]; then
    REPORT+="✅ ${ROOM}: ${TEMP}°C (OK)\n"
  else
    if python3 -c "exit(0 if float('$TEMP') < $MIN_TEMP else 1)" 2>/dev/null; then
      ALERTS+="🔽 ${ROOM}: ${TEMP}°C — ¿subimos temperatura?\n"
    else
      ALERTS+="🔼 ${ROOM}: ${TEMP}°C — ¿bajamos temperatura?\n"
    fi
  fi
}

# --- Sensibo devices ---
for entry in "${SENSIBO_DEVICES[@]}"; do
  DEVICE_ID="${entry%%:*}"
  ROOM="${entry##*:}"

  RESPONSE=$(curl --compressed --silent --max-time 10 \
    "${API}/pods/${DEVICE_ID}?fields=measurements&apiKey=${SENSIBO_API_KEY}" 2>&1) || {
    ALERTS+="❌ ${ROOM}: sin conexión (curl falló)\n"
    continue
  }

  TEMP=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['result']['measurements']['temperature'])
except Exception as e:
    print('ERROR: ' + str(e))
" 2>/dev/null)

  check_temp "$ROOM" "$TEMP"
done

# --- OMEGA Room (msmart-ng) ---
OMEGA_OUT=$($MSMART query $OMEGA_IP --id $OMEGA_ID --token $OMEGA_TOKEN --key $OMEGA_KEY 2>&1) || {
  ALERTS+="❌ Room (OMEGA): sin conexión\n"
  OMEGA_OUT=""
}

if [[ -n "$OMEGA_OUT" ]]; then
  OMEGA_TEMP=$(echo "$OMEGA_OUT" | python3 -c "
import sys, re
data = sys.stdin.read()
m = re.search(r\"'indoor_temperature': ([0-9.]+)\", data)
print(m.group(1) if m else 'ERROR: no temp')
" 2>/dev/null)
  check_temp "Room (OMEGA)" "$OMEGA_TEMP"
fi

# Output
echo "=== Temp Check $(date '+%Y-%m-%d %H:%M %Z') ==="
if [[ -n "$REPORT" ]]; then
  echo -e "$REPORT"
fi
if [[ -n "$ALERTS" ]]; then
  echo -e "$ALERTS"
fi
