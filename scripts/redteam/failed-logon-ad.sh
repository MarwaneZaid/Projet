#!/usr/bin/env bash
# Scénario RT-03 — Tentatives SSH échouées vers le contrôleur AD (lab)
# Simule une attaque sur l'annuaire avant énumération AD complète.
# MITRE : T1110.001 + T1078 (Valid Accounts — abuse attempt)
set -euo pipefail

CIBLE="${1:-192.168.20.16}"
USERS=(administrator fakeuser attacker-demo guest)

echo "=============================================="
echo " RT-03 Failed logon / SSH vers AD"
echo " Heure début : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo " Source      : $(hostname) ($(hostname -I | awk '{print $1}'))"
echo " Cible       : ${CIBLE} (srv-ad-1 / nexamind.local)"
echo " MITRE       : T1110.001, T1078"
echo "=============================================="

for u in "${USERS[@]}"; do
  echo "[*] Tentatives SSH : ${u}@${CIBLE}"
  for _ in 1 2 3; do
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 -o BatchMode=yes \
      "${u}@${CIBLE}" exit 2>/dev/null || true
    sleep 1
  done
done

echo "[*] Fin RT-03 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "[*] Vérifier Wazuh agent srv-ad-1 + règles sshd 5710"
