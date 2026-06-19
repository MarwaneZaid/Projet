#!/usr/bin/env bash
# Démo SOC NexaMind — script pour enregistrement vidéo de secours (OBS / QuickTime)
# Durée cible : ~5 min · VPN connecté · Identifiants Wazuh : wazuh-wui / MyS3cr37P450r.*-
set -euo pipefail

WAZUH_URL="${WAZUH_URL:-https://192.168.20.22}"
PORTAIL_URL="${PORTAIL_URL:-http://192.168.20.20}"
SOC_SSH="${SOC_SSH:-nexa@192.168.20.18}"
SOC_PASS="${SOC_PASS:-NexaMind2026!}"

pause() {
  local sec="${1:-5}"
  echo ""
  echo ">>> PAUSE ${sec}s — $2"
  sleep "$sec"
}

echo "=============================================="
echo " DÉMO SOC NEXAMIND — $(date '+%Y-%m-%d %H:%M')"
echo "=============================================="
pause 3 "Démarrer l'enregistrement OBS maintenant"

echo ""
echo "[1/6] Agents Wazuh actifs"
echo "  Ouvrir : ${WAZUH_URL} → Endpoints Summary"
echo "  Montrer : srv-web-1, srv-ad-1, localhost (manager)"
pause 25 "Montrer la liste des agents Active"

echo ""
echo "[2/6] Portail NexaMind — état normal"
echo "  Ouvrir : ${PORTAIL_URL}"
echo "  Login : admin / admin123 → dashboard sans alertes critiques"
pause 20 "Montrer le portail avant attaque"

echo ""
echo "[3/6] Lancer attaque brute-force SSH (depuis VM 107)"
export SSHPASS="$SOC_PASS"
sshpass -e ssh -o StrictHostKeyChecking=no "$SOC_SSH" \
  'bash ~/demo-attaque/attaque-test.sh 192.168.20.20' || true
pause 5 "Attaque lancée"

echo ""
echo "[4/6] Wazuh — Threat Hunting"
echo "  ${WAZUH_URL} → Threat Hunting → agent srv-web-1"
echo "  Filtrer : authentication / ssh"
pause 30 "Montrer les alertes brute-force"

echo ""
echo "[5/6] Portail — alertes remontées"
echo "  ${PORTAIL_URL} → dashboard admin"
echo "  Montrer : alerte critique brute-force"
pause 25 "Montrer corrélation portail ↔ Wazuh"

echo ""
echo "[6/6] Bonus — scan ports (optionnel)"
sshpass -e ssh -o StrictHostKeyChecking=no "$SOC_SSH" \
  "printf '%s\n' '$SOC_PASS' | sudo -S nmap -sT -Pn -T4 --top-ports 20 192.168.20.20 2>/dev/null | tail -8" || true
echo "  Wazuh → filtrer rule.groups:port_scan ou nmap"
pause 20 "Clôture : 3 agents, détection temps réel, chaîne attaque→SOC→portail"

echo ""
echo "=============================================="
echo " FIN DÉMO — arrêter l'enregistrement"
echo " Fichier suggéré : docs/livrables/videos/demo-soc-secours.mp4"
echo "=============================================="
