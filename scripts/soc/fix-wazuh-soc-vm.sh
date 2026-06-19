#!/usr/bin/env bash
# Fix Wazuh single-node on srv-soc-1 (192.168.20.18)
# Run ON THE VM as nexa: bash fix-wazuh-soc-vm.sh
#
# Handles: disk full (wazuh_queue), ordered startup on low RAM, dashboard 503.
# Optional: EXPAND_ROOT=1 extends /dev/sda1 when Proxmox disk is 80G but root is ~19G.

set -euo pipefail

WAZUH_DIR="${WAZUH_DIR:-$HOME/wazuh-docker/single-node}"
QUEUE_VOL="single-node_wazuh_queue"
QUEUE_PURGE_MB="${QUEUE_PURGE_MB:-3000}"

expand_root_if_needed() {
  local root_gb
  root_gb=$(df -BG / | tail -1 | awk '{print $2}' | tr -d G)
  if [[ "${EXPAND_ROOT:-0}" == "1" ]] && [[ "${root_gb}" -lt 50 ]]; then
    echo "=== Expanding root partition (EXPAND_ROOT=1) ==="
    sudo apt-get install -y -qq parted cloud-guest-utils 2>/dev/null || true
    sudo swapoff /dev/sda5 2>/dev/null || sudo swapoff -a 2>/dev/null || true
    sudo parted /dev/sda --script rm 5 2>/dev/null || true
    sudo parted /dev/sda --script rm 2 2>/dev/null || true
    sudo growpart /dev/sda 1
    sudo resize2fs /dev/sda1
    if [[ ! -f /swapfile ]]; then
      sudo fallocate -l 2G /swapfile
      sudo chmod 600 /swapfile
      sudo mkswap /swapfile
    fi
    sudo swapon /swapfile 2>/dev/null || true
    sudo sed -i '/sda5/d' /etc/fstab
    grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    df -h /
  fi
}

echo "=== Memory / disk ==="
free -h
df -h /
expand_root_if_needed

cd "$WAZUH_DIR"

queue_mb=0
if [[ -d /var/lib/docker/volumes/${QUEUE_VOL}/_data ]]; then
  queue_mb=$(sudo du -sm "/var/lib/docker/volumes/${QUEUE_VOL}/_data" 2>/dev/null | cut -f1 || echo 0)
fi
echo "wazuh_queue: ${queue_mb} MB"

disk_pct=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
need_purge=0
[[ "${queue_mb}" -gt "${QUEUE_PURGE_MB}" ]] && need_purge=1
[[ "${disk_pct}" -ge 85 ]] && need_purge=1

if [[ "${need_purge}" -eq 1 ]]; then
  echo "=== Purge queue + ordered restart (disk ${disk_pct}%, queue ${queue_mb}MB) ==="
  sudo systemctl stop wazuh-agent 2>/dev/null || true
  docker compose down
  sudo docker volume rm "${QUEUE_VOL}" 2>/dev/null || true
  df -h /

  echo "Starting indexer..."
  docker compose up -d wazuh.indexer
  for i in {1..40}; do
    status=$(curl -sk -u admin:SecretPassword https://127.0.0.1:9200/_cluster/health 2>/dev/null | grep -o '"status":"[^"]*"' || true)
    echo "  indexer [$i]: ${status:-waiting}"
    [[ "${status}" == *"green"* || "${status}" == *"yellow"* ]] && break
    sleep 10
  done

  echo "Starting manager..."
  docker compose up -d wazuh.manager
  sleep 60

  echo "Starting dashboard..."
  docker compose up -d wazuh.dashboard
else
  echo "=== Standard restart ==="
  docker compose up -d
fi

echo "Waiting for dashboard (low RAM: up to 5 min)..."
for i in {1..30}; do
  code=$(curl -sk -o /dev/null -w '%{http_code}' --connect-timeout 5 https://127.0.0.1/ 2>/dev/null || echo "000")
  echo "  attempt $i: HTTP $code | disk $(df -h / | tail -1 | awk '{print $5}')"
  [[ "$code" == "200" || "$code" == "302" ]] && break
  sleep 10
done

echo "=== docker compose ps ==="
docker compose ps

echo "=== Cluster + dashboard ==="
curl -sk -u admin:SecretPassword https://127.0.0.1:9200/_cluster/health?pretty 2>/dev/null | grep -E '"status"|"number_of_nodes"' || true
curl -sk -I https://127.0.0.1/ 2>/dev/null | head -3 || true

echo "=== Agents ==="
docker compose exec -T wazuh.manager /var/ossec/bin/agent_control -l 2>/dev/null || true

echo "=== Restart local agent ==="
sudo systemctl restart wazuh-agent 2>/dev/null || true
sleep 15
sudo systemctl is-active wazuh-agent 2>/dev/null || true
docker compose exec -T wazuh.manager /var/ossec/bin/agent_control -l 2>/dev/null || true

echo ""
echo "UI: https://192.168.20.18  |  admin / SecretPassword"
echo "If agent shows Unknown after queue purge: sudo systemctl restart wazuh-agent"
