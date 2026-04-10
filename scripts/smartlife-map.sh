#!/usr/bin/env bash
# smartlife-map.sh
# Mapear dispositivos Tuya/SmartLife.

set -euo pipefail

source "$(dirname "$0")/../.env.iot"

# Dispositivos detectados previamente
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
    echo "Dispositivo en $IP con producto $PRODUCT_ID"
done

# Agregar Lógica de control según sea necesario:
# Aquí podrías mapear de forma correspondiente, leer estados, etc.