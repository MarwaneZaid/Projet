#!/usr/bin/env bash
# Bootstrap complet depuis le Mac de l'équipe (après firewall OVH)
set -euo pipefail

HOST="${HOST:-51.77.52.56}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Test ports ==="
nc -zv -w 8 "$HOST" 22 8006 || true

echo "=== SSH post-install Proxmox ==="
ssh -o StrictHostKeyChecking=accept-new "root@${HOST}" bash -s < "${ROOT}/scripts/proxmox/01-host-postinstall.sh"

echo "=== Création VMs ==="
ssh "root@${HOST}" bash -s < "${ROOT}/scripts/proxmox/02-create-vms.sh"

echo "=== Terminé ==="
echo "Proxmox : https://${HOST}:8006"
