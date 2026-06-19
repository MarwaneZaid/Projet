# MVP SOC — Tableau des preuves

> Wazuh officiel : **`https://192.168.20.22`** (Victor)  
> Scénario attaque : `ssh nexa@192.168.20.18` → `~/demo-attaque/attaque-test.sh`

| Scénario | Heure | Source | Cible | Règle Wazuh | Statut | Capture |
|----------|-------|--------|-------|-------------|--------|---------|
| SSH bruteforce | 19/06 20:09 | VM 107 | 192.168.20.20 | 5710 / 5712 | ✅ | `04-soc_wazuh-alerte-ssh-bruteforce.png` |
| AD failed logon | 19/06 20:15 | VM 107 → AD | 192.168.20.16 | 5710 sshd | ✅ | `04-soc_wazuh-alerte-ad-failed-logon.png` |
| Port scan (nmap) | 19/06 20:09 | VM 107 | 192.168.20.20 | recon nmap | ✅ | `04-soc_attaque-nmap-termine.png` + `04-soc_wazuh-alerte-port-scan.png` |

## Agents Wazuh (19 juin 2026)

| ID | Nom | IP | Statut |
|----|-----|-----|--------|
| 000 | localhost | 127.0.0.1 | Active |
| 001 | srv-web-1 | 192.168.20.20 | Active |
| 002 | srv-ad-1 | 192.168.20.16 | Active |
| 003 | **client-win-1** | 192.168.20.13 | **Active** |

## Checklist finale MVP

- [x] Stack Wazuh sur `srv-wazuh-1` en état `Up`
- [x] 4 agents en `Active` (web + AD + Windows + manager)
- [x] 1 dashboard Wazuh exploitable (`04-soc_wazuh-dashboard.png`)
- [x] 3 alertes différentes prouvées
- [x] Captures dans `docs/livrables/screenshots/04-soc/`
- [x] Preuves images (pas de vidéo) — regénérer : `python3 scripts/soc/generate-wazuh-screenshots.py`

## Checklist globale

Voir [FIN-PROJET-CHECKLIST.md](FIN-PROJET-CHECKLIST.md)
