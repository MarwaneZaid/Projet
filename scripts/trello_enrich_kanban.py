#!/usr/bin/env python3
"""
Enrichit le board Kanban existant (Backlog / To Do / In Progress / …)
en ajoutant checklists, descriptions et cartes manquantes.

Cartes cibles détectées sur le board « Projet » :
  - Installation Proxmox
  - Architecture réseau & sécurité
  - Déploiement pfSense
  - Active directory
  - SOC
  - Red Team & Attaques controlées
  - Site Web Client/Admin
  - Documentation technique

Usage:
  export TRELLO_API_KEY="..."
  export TRELLO_TOKEN="..."
  python3 scripts/trello_enrich_kanban.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.trello.com/1"
BOARD_SHORT = os.environ.get("TRELLO_BOARD_ID", "uPZIvZwK")

# Checklists à fusionner (noms d'items insensibles à la casse)
CHECKLISTS: dict[str, list[str]] = {
    "Installation Proxmox": [
        "Installer Proxmox VE sur bare metal",
        "Configurer stockage ZFS/LVM + snapshots",
        "Créer vmbr0 (LAN) et vmbr1 (DMZ)",
        "Template cloud-init Debian/Ubuntu",
        "VM Linux hôte Docker (segment SOC)",
        "Inventaire VMs (IP, rôle, ressources)",
        "Politique sauvegarde snapshots",
        "Validation collective Phase 1 infra",
    ],
    "Architecture réseau & sécurité": [
        "Définir schéma réseau global",
        "Définir VLAN (LAN, DMZ, SOC, Red Team)",
        "Définir position pfSense",
        "Définir architecture VPN",
        "Valider architecture finale (schéma)",
        "Renseigner docs/architecture/topologie-reseau.md",
        "Renseigner specs matériel (docs/architecture/specs-materiel.md)",
    ],
    "Déploiement pfSense": [
        "Installer VM pfSense",
        "Configurer interfaces WAN/LAN/DMZ",
        "NAT sortant + DHCP + réservations IP",
        "Règles firewall LAN ↔ DMZ ↔ Internet",
        "Tester isolation segments",
        "Syslog remote vers Wazuh (phase SOC)",
        "Export backup config pfSense",
        "VPN site-to-site (ou documenter blocage)",
    ],
    "Active directory": [
        "Décision Samba AD vs Windows Server",
        "Installer contrôleur de domaine",
        "Créer OU, groupes, utilisateurs test",
        "GPO audit connexions + politique MDP",
        "Joindre 2 postes clients au domaine",
        "Activer forward logs sécurité → SOC",
        "Compte de service agent Wazuh",
    ],
    "SOC": [
        "Configurer soc/.env (secrets hors Git)",
        "Déployer Wazuh + Grafana (docker compose)",
        "Ouvrir ports pfSense pour agents",
        "Agent Wazuh sur AD + hôte Docker",
        "Syslog pfSense → Wazuh",
        "Déployer Suricata + règles",
        "Grafana : dashboard alertes",
        "TheHive + Cortex : incident fictif",
        "n8n : alerte → email/ticket",
        "Exercice corrélation avec Red Team",
    ],
    "Red Team & Attaques controlées": [
        "Segment LAB-RT isolé (aucune route vers LAN)",
        "Déployer OpenVAS — scan lab uniquement",
        "BloodHound : collecte sur lab AD",
        "CALDERA : déploiement + agent lab",
        "Scénario 1 : brute force honeypot (rapport)",
        "Scénario 2 : énumération AD (rapport)",
        "Documenter IOC + TTP pour le SOC",
    ],
    "Site Web Client/Admin": [
        "Maquettes wireframes client + admin",
        "Schéma BDD PostgreSQL",
        "MVP authentification sécurisée",
        "Parcours commande / demande d'audit",
        "Dashboard admin + gestion devis",
        "Lien rapports Wazuh/OpenVAS",
    ],
    "Documentation technique": [
        "Rapport technique (~10 pages)",
        "WikiJS procédures internes",
        "Schémas réseau + architecture SOC (PNG)",
        "Pitch entreprise IT (slides)",
        "Répétition démo orale équipe",
    ],
}

NEW_BACKLOG_CARDS = [
    ("Compléter TEAM.md (4 noms, contacts)", "docs/TEAM.md — échéance Phase 0"),
    ("Validation collective Phase 0 (cadrage)", "CHECKLIST.md"),
    ("Validation collective Phase 2 (SOC + RT)", "CHECKLIST.md"),
    ("Validation collective Phase 3 (Ansible)", "CHECKLIST.md"),
    ("Playbooks Ansible (inventory + agents)", "ansible/"),
    ("Test restore snapshot Proxmox", "Phase 3"),
    ("Reverse proxy DMZ + TLS lab", "Phase 3"),
]

DESCRIPTIONS: dict[str, str] = {
    "SOC": "Stack : Wazuh, Suricata, Grafana, TheHive, Cortex, n8n.\nRepo : `soc/`\nLead : Étudiant 3 (profil réseau → rôle sécurité)",
    "Active directory": "Samba AD ou Windows Server.\nRepo : `infra/active-directory/`\nLead : Étudiant 2",
    "Red Team & Attaques controlées": "CALDERA, BloodHound, OpenVAS — **lab isolé uniquement**.\nRepo : `redteam/`\nLead : Étudiant 4",
    "Site Web Client/Admin": "Extension Audit de sécurité.\nRepo : `portal/`\nLead : Étudiant 4",
    "Installation Proxmox": "Lead : Étudiant 1 (profil cyber → infra).\nRepo : `infra/proxmox/`",
    "Architecture réseau & sécurité": "Lead : Étudiant 1 + 2.\nRepo : `docs/architecture/`",
    "Déploiement pfSense": "Lead : Étudiant 2.\nRepo : `infra/pfsense/`",
    "Documentation technique": "Livrables finaux — Juin/Juillet.\nRepo : `docs/livrables/`",
}


def api(method: str, path: str, params: dict | None = None, body: dict | None = None):
    key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    if not key or not token:
        print("Définir TRELLO_API_KEY et TRELLO_TOKEN → https://trello.com/app-key", file=sys.stderr)
        sys.exit(1)
    q = {"key": key, "token": token}
    if params:
        q.update(params)
    url = f"{API}{path}?{urllib.parse.urlencode(q)}"
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = urllib.parse.urlencode(body).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode()
        return {} if not raw else json.loads(raw)


def find_card(cards: list, name: str) -> dict | None:
    name_l = name.lower()
    for c in cards:
        if c["name"].lower() == name_l or name_l in c["name"].lower():
            return c
    return None


def get_existing_items(card_id: str) -> set[str]:
    items: set[str] = set()
    checklists = api("GET", f"/cards/{card_id}/checklists")
    for cl in checklists:
        for it in cl.get("checkItems", []):
            items.add(it["name"].lower().strip())
    return items


def ensure_checklist(card_id: str, card_name: str, wanted: list[str]) -> None:
    existing = get_existing_items(card_id)
    checklists = api("GET", f"/cards/{card_id}/checklists")
    cl_id = checklists[0]["id"] if checklists else api(
        "POST", "/checklists", body={"idCard": card_id, "name": "Checklist"}
    )["id"]

    added = 0
    for item in wanted:
        if item.lower().strip() in existing:
            continue
        api(
            "POST",
            f"/checklists/{cl_id}/checkItems",
            body={"name": item, "pos": "bottom"},
        )
        added += 1
    print(f"  {card_name}: +{added} items checklist")


def ensure_description(card_id: str, card_name: str, desc: str) -> None:
    card = api("GET", f"/cards/{card_id}", {"fields": "desc"})
    if card.get("desc", "").strip():
        return
    api("PUT", f"/cards/{card_id}", body={"desc": desc})
    print(f"  {card_name}: description ajoutée")


def main() -> None:
    board = api("GET", f"/boards/{BOARD_SHORT}", {"fields": "id,name"})
    board_id = board["id"]
    print(f"Board: {board['name']}")

    cards = api("GET", f"/boards/{board_id}/cards", {"filter": "open"})
    lists = {lb["id"]: lb["name"] for lb in api("GET", f"/boards/{board_id}/lists")}
    backlog_id = next((lid for lid, n in lists.items() if n.lower() == "backlog"), None)

    print("\n— Checklists —")
    for card_name, items in CHECKLISTS.items():
        card = find_card(cards, card_name)
        if not card:
            print(f"  ⚠ Carte introuvable: {card_name}")
            continue
        ensure_checklist(card["id"], card_name, items)
        if card_name in DESCRIPTIONS:
            ensure_description(card["id"], card_name, DESCRIPTIONS[card_name])

    if backlog_id:
        print("\n— Cartes Backlog —")
        existing_names = {c["name"].lower() for c in cards}
        for title, desc in NEW_BACKLOG_CARDS:
            if title.lower() in existing_names:
                print(f"  déjà présent: {title}")
                continue
            api(
                "POST",
                "/cards",
                body={"name": title, "desc": desc, "idList": backlog_id, "pos": "bottom"},
            )
            print(f"  + {title}")

    print("\nTerminé → https://trello.com/b/uPZIvZwK/projet")


if __name__ == "__main__":
    main()
