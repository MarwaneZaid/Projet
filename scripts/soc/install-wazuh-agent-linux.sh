#!/usr/bin/env bash
# Install Wazuh agent 4.9.2 on Debian/Ubuntu — run with sudo on target VM.
set -euo pipefail

WAZUH_MANAGER="${WAZUH_MANAGER:-192.168.20.22}"
WAZUH_AGENT_NAME="${WAZUH_AGENT_NAME:-$(hostname -s)}"
WAZUH_VERSION="${WAZUH_VERSION:-4.9.2-1}"

export DEBIAN_FRONTEND=noninteractive

if dpkg -l wazuh-agent 2>/dev/null | grep -q '^ii'; then
  echo "wazuh-agent already installed"
else
  curl -fsSL https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --dearmor -o /usr/share/keyrings/wazuh.gpg
  echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" \
    > /etc/apt/sources.list.d/wazuh.list
  apt-get update -qq
  WAZUH_MANAGER="$WAZUH_MANAGER" WAZUH_AGENT_NAME="$WAZUH_AGENT_NAME" \
    apt-get install -y "wazuh-agent=${WAZUH_VERSION}"
fi

systemctl enable wazuh-agent
systemctl restart wazuh-agent
sleep 2
systemctl is-active wazuh-agent
grep -E '<address>|<port>' /var/ossec/etc/ossec.conf | head -4
