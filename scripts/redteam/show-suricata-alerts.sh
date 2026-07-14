#!/usr/bin/env bash
# Affiche les alertes Suricata (event_type: alert) — démo jury / preuves PNG
set -euo pipefail

EVE="${EVE:-/var/log/suricata/eve.json}"
ATTACKER="${ATTACKER:-192.168.20.18}"
PORTAIL="${PORTAIL:-192.168.20.20}"
AD="${AD:-192.168.20.16}"
TAIL="${TAIL:-5}"
FILTER_LAB="${FILTER_LAB:-1}"

if [[ ! -r "${EVE}" ]]; then
  echo "[!] ${EVE} illisible"
  exit 1
fi

echo "=============================================="
echo " Suricata — alertes IDS (event_type: alert)"
echo " Fichier  : ${EVE}"
echo " Attaquant: ${ATTACKER} · Portail: ${PORTAIL} · AD: ${AD}"
echo " Commande : grep '\"event_type\":\"alert\"' ${EVE} | tail -${TAIL}"
echo "=============================================="
echo ""

filter_line() {
  local raw="$1"
  if [[ "${FILTER_LAB}" == "1" ]]; then
    echo "${raw}" | grep -E "NEXAMIND LAB|${ATTACKER}.*${PORTAIL}|${ATTACKER}.*${AD}" || return 1
  fi
  echo "${raw}"
}

show_alert() {
  local raw="$1"
  if command -v jq >/dev/null 2>&1; then
    echo "${raw}" | jq -c '{
      timestamp: .timestamp,
      event_type: .event_type,
      src: .src_ip,
      dst: .dest_ip,
      port: .dest_port,
      signature: .alert.signature,
      sid: .alert.signature_id,
      severity: .alert.severity
    }' 2>/dev/null || echo "${raw:0:200}"
  else
    python3 -c "
import json, sys
j=json.loads(sys.argv[1])
a=j.get('alert',{})
print(f\"{j.get('timestamp','')[:19]}  [{a.get('signature_id','?')}]  \"
      f\"{j.get('src_ip','?')} → {j.get('dest_ip','?')}:{j.get('dest_port','?')}  \"
      f\"{a.get('signature','?')[:70]}\")
" "${raw}" 2>/dev/null || echo "${raw:0:200}"
  fi
}

lab_count=0
nexamind_count=0
total=0

while IFS= read -r raw; do
  [[ -z "${raw}" ]] && continue
  total=$((total + 1))
  is_nexamind=0
  echo "${raw}" | grep -q "NEXAMIND LAB" && is_nexamind=1
  if [[ "${is_nexamind}" -eq 1 ]] || echo "${raw}" | grep -qE "${ATTACKER}.*(${PORTAIL}|${AD})"; then
    prefix="★ "
    lab_count=$((lab_count + 1))
    [[ "${is_nexamind}" -eq 1 ]] && nexamind_count=$((nexamind_count + 1))
    echo "${prefix}$(show_alert "${raw}")"
  elif [[ "${FILTER_LAB}" != "1" ]]; then
    show_alert "${raw}"
  fi
done < <(grep '"event_type":"alert"' "${EVE}" | tail -200 | grep -E "NEXAMIND LAB|${ATTACKER}.*(${PORTAIL}|${AD})" || grep '"event_type":"alert"' "${EVE}" | tail -"${TAIL}")

echo ""
echo "[*] Signatures NEXAMIND LAB : ${nexamind_count} · Alertes lab (.18→.20/.16) : ${lab_count}"

if [[ "${lab_count}" -eq 0 ]]; then
  echo "[*] Aucune alerte lab récente — relancer : bash ~/redteam/run-all.sh"
  echo "[*] Vérifier règles : sudo bash ~/redteam/install-suricata-lab-rules.sh"
  echo ""
  echo "--- Dernières alertes brutes (tail -${TAIL}) ---"
  grep '"event_type":"alert"' "${EVE}" | tail -"${TAIL}" | while IFS= read -r raw; do
    show_alert "${raw}"
  done
fi
