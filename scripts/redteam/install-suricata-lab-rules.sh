#!/usr/bin/env bash
# Installe les règles Suricata NexaMind (lab interne) sur VM 107
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_SRC="${DIR}/suricata-nexamind-lab.rules"
RULES_DEST="/var/lib/suricata/rules/nexamind-lab.rules"
YAML="/etc/suricata/suricata.yaml"

if [[ ! -f "${RULES_SRC}" ]]; then
  echo "[!] Fichier absent : ${RULES_SRC}"
  exit 1
fi

if [[ "$(id -u)" -ne 0 ]]; then
  echo "[!] Exécuter en root : sudo bash install-suricata-lab-rules.sh"
  exit 1
fi

echo "[*] Copie ${RULES_SRC} → ${RULES_DEST}"
install -m 644 "${RULES_SRC}" "${RULES_DEST}"

if ! grep -q "nexamind-lab.rules" "${YAML}"; then
  echo "[*] Ajout nexamind-lab.rules dans ${YAML}"
  sed -i '/^rule-files:/a\  - nexamind-lab.rules' "${YAML}"
fi

echo "[*] Validation config Suricata…"
suricata -T -c "${YAML}" --init-errors-fatal

echo "[*] Reload Suricata…"
systemctl reload suricata || systemctl restart suricata
systemctl is-active suricata
echo "[*] OK — règles lab actives (sid 9000001–9000003)"
