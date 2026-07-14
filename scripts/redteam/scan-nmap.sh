#!/usr/bin/env bash
# Scénario RT-02 — Reconnaissance / port scan (lab uniquement)
# MITRE : T1046 (Network Service Discovery)
set -euo pipefail

CIBLE="${1:-192.168.20.20}"
PORTS="${PORTS:-top-ports 100}"

echo "=============================================="
echo " RT-02 Port scan (nmap)"
echo " Heure début : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo " Source      : $(hostname) ($(hostname -I | awk '{print $1}'))"
echo " Cible       : ${CIBLE}"
echo " MITRE       : T1046"
echo "=============================================="

if ! command -v nmap >/dev/null 2>&1; then
  echo "[!] nmap absent — installer : sudo apt install nmap"
  exit 1
fi

# shellcheck disable=SC2086
sudo nmap -sT -Pn -T4 --${PORTS} "$CIBLE" -oN "/tmp/rt02-nmap-${CIBLE}.txt" 2>/dev/null || \
  nmap -sT -Pn -T4 --${PORTS} "$CIBLE" -oN "/tmp/rt02-nmap-${CIBLE}.txt"

echo ""
echo "[*] Résultat sauvegardé : /tmp/rt02-nmap-${CIBLE}.txt"
tail -15 "/tmp/rt02-nmap-${CIBLE}.txt" 2>/dev/null || true
echo "[*] Fin RT-02 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "[*] Vérifier Wazuh (port scan) + Suricata : sudo tail -f /var/log/suricata/eve.json"
