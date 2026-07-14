#!/usr/bin/env bash
# Dépendances Red Team sur VM 107 (srv-soc-1)
set -euo pipefail

PACKAGES=(hydra nmap jq)

missing=()
for pkg in "${PACKAGES[@]}"; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    missing+=("$pkg")
  fi
done

if [[ ${#missing[@]} -eq 0 ]]; then
  echo "[*] Dépendances OK : ${PACKAGES[*]}"
  exit 0
fi

echo "[*] Installation : ${missing[*]}"
if command -v sudo >/dev/null && sudo -n true 2>/dev/null; then
  sudo apt-get update -qq
  sudo apt-get install -y "${missing[@]}"
elif command -v sudo >/dev/null; then
  echo "[!] sudo requis — lancer : sudo apt-get install -y ${missing[*]}"
  exit 1
else
  echo "[!] root requis pour installer ${missing[*]}"
  exit 1
fi

echo "[*] OK"
