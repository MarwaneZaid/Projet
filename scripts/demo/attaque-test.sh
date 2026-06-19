#!/usr/bin/env bash
# Scénario démo NexaMind — brute-force SSH vers le portail / cible lab
# Usage : ./attaque-test.sh [IP_CIBLE]
# Défaut : 192.168.20.20 (srv-web-1)
set -euo pipefail

CIBLE="${1:-192.168.20.20}"
USER_FAKE="attacker-demo"
TRIES="${TRIES:-8}"

echo "[*] Cible : $CIBLE — $TRIES tentatives SSH (démo contrôlée)"
for i in $(seq 1 "$TRIES"); do
  echo "  tentative $i/$TRIES..."
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 -o BatchMode=yes \
    "${USER_FAKE}@${CIBLE}" exit 2>/dev/null || true
  sleep 1
done
echo "[*] Terminé. Vérifier Wazuh https://192.168.20.22 et portail http://192.168.20.20"
