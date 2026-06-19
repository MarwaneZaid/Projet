#!/usr/bin/env bash
# Création des VMs de base sur Proxmox (IDs 100–104)
# Prérequis : ISO pfSense + template cloud-init Debian dans le stockage local
# Usage : exécuter sur l'hôte Proxmox en root

set -euo pipefail

STORAGE="${STORAGE:-local-lvm}"
BRIDGE="${BRIDGE:-vmbr0}"

create_vm() {
  local vmid=$1 name=$2 memory=$3 cores=$4 disk=$5
  if qm status "$vmid" &>/dev/null; then
    echo "VM $vmid ($name) existe déjà — ignorée"
    return
  fi
  echo "Création VM $vmid : $name (${memory}M, ${cores}c, ${disk}G)"
  qm create "$vmid" \
    --name "$name" \
    --memory "$memory" \
    --cores "$cores" \
    --net0 "virtio,bridge=${BRIDGE}" \
    --scsi0 "${STORAGE}:${disk}" \
    --ostype l26 \
    --agent 1
}

echo "=== VMs projet mini-cloud ==="
create_vm 100 fw-pfsense    1024 1 20
create_vm 101 ad-dc01       4096 2 60
create_vm 102 docker-soc01  8192 2 100
create_vm 103 lab-rt01      4096 2 40
create_vm 104 win-client01  4096 2 40

echo ""
echo "Prochaines étapes manuelles :"
echo "  100 : attacher ISO pfSense, boot, config WAN/LAN"
echo "  101–104 : cloner depuis template cloud-init ou installer OS"
echo "  Mettre à jour docs/architecture/inventaire-vms.md avec les IP"
