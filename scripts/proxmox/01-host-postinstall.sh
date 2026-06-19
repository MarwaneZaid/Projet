#!/usr/bin/env bash
# Post-install Proxmox sur l'hôte OVH — à exécuter en root sur 51.77.52.56
# Usage : ssh root@51.77.52.56 'bash -s' < scripts/proxmox/01-host-postinstall.sh

set -euo pipefail

echo "=== [1/6] Versions ==="
pveversion
uname -a

echo "=== [2/6] Mise à jour système ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y full-upgrade

echo "=== [3/6] Stockage ==="
pvesm status || true
lsblk
df -h

echo "=== [4/6] Bridge vmbr0 (si absent) ==="
if ! grep -q '^auto vmbr0' /etc/network/interfaces 2>/dev/null; then
  MAIN_IF=$(ip -o link show | awk -F': ' '$2 !~ /^(lo|vmbr)/ {print $2; exit}')
  echo "Interface principale détectée : ${MAIN_IF:-non trouvée}"
  echo "Configurer vmbr0 manuellement dans /etc/network/interfaces puis : ifreload -a"
else
  echo "vmbr0 déjà présent dans /etc/network/interfaces"
fi

echo "=== [5/6] Repo no-subscription (si pas d'abonnement Proxmox) ==="
if ! grep -q pve-no-subscription /etc/apt/sources.list.d/pve-install-repo.list 2>/dev/null; then
  cat >/etc/apt/sources.list.d/pve-no-subscription.list <<'EOF'
deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription
EOF
  apt-get update
fi

echo "=== [6/6] Résumé ==="
echo "Proxmox UI : https://$(hostname -I | awk '{print $1}'):8006"
echo "Terminé. Créer les VMs via 02-create-vms.sh ou l'UI."
