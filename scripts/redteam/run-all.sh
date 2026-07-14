#!/usr/bin/env bash
# Orchestrateur Red Team NexaMind — 3 scénarios + corrélation SOC
# À lancer depuis VM 107 : bash ~/redteam/run-all.sh
# Ou en local : scripts/redteam/deploy-to-vm107.sh puis ssh nexa@192.168.20.18
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORTAIL="${PORTAIL:-192.168.20.20}"
AD="${AD:-192.168.20.16}"
PAUSE="${PAUSE:-15}"

log() { echo ""; echo ">>> $*"; echo ""; }

log "RED TEAM NEXAMIND — $(date '+%Y-%m-%d %H:%M:%S')"
log "Cibles lab uniquement : portail ${PORTAIL}, AD ${AD}"
log "Pause ${PAUSE}s entre scénarios (export PAUSE=5 pour accélérer)"

bash "${DIR}/scan-nmap.sh" "$PORTAIL"
sleep "$PAUSE"

bash "${DIR}/bruteforce-ssh.sh" "$PORTAIL"
sleep "$PAUSE"

bash "${DIR}/failed-logon-ad.sh" "$AD"

log "Suricata — alertes IDS (double détection réseau + logs Wazuh)"
bash "${DIR}/show-suricata-alerts.sh" || true

log "Terminé. Ouvrir Wazuh https://192.168.20.22 → Threat Hunting"
log "Journal : docs/livrables/redteam/journal-exercices.md"
