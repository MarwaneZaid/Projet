#!/usr/bin/env bash
# Copie les scripts Red Team sur VM 107 (srv-soc-1)
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_HOST="${DEST_HOST:-nexa@192.168.20.18}"
DEST_DIR="${DEST_DIR:-~/redteam}"
SSH_OPTS=(-o StrictHostKeyChecking=no)

run_ssh() {
  if [[ -n "${SSHPASS:-}" ]] && command -v sshpass >/dev/null; then
    sshpass -e ssh "${SSH_OPTS[@]}" "$@"
  else
    ssh "${SSH_OPTS[@]}" "$@"
  fi
}

run_scp() {
  if [[ -n "${SSHPASS:-}" ]] && command -v sshpass >/dev/null; then
    sshpass -e scp "${SSH_OPTS[@]}" "$@"
  else
    scp "${SSH_OPTS[@]}" "$@"
  fi
}

echo "[*] Déploiement Red Team → ${DEST_HOST}:${DEST_DIR}"
run_ssh "$DEST_HOST" "mkdir -p ${DEST_DIR}"
run_scp "${SRC}/"*.sh "${SRC}/suricata-nexamind-lab.rules" "${DEST_HOST}:${DEST_DIR}/"
run_ssh "$DEST_HOST" "chmod +x ${DEST_DIR}/*.sh"
echo "[*] Vérification dépendances (hydra, nmap, jq)…"
run_ssh "$DEST_HOST" "bash ${DEST_DIR}/ensure-deps.sh" || echo "[!] ensure-deps : installer hydra manuellement si besoin"
echo "[*] OK — lancer : ssh ${DEST_HOST} 'bash ${DEST_DIR}/run-all.sh'"
