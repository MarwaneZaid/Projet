# Équipe — contacts & coordination

## Membres

| # | Nom | Profil | Rôle projet | Contact |
|---|-----|--------|-------------|---------|
| 1 | _À compléter_ | Cybersécurité | Infra & Proxmox | |
| 2 | Abdoul Hamani Bachir Seydou | Cybersécurité | Réseau & AD | |
| 3 | _À compléter_ | Réseau & systèmes | SOC & automatisation | |
| 4 | _À compléter_ | Réseau & systèmes | Red Team & portail | |

## Binômes de relecture

| Binôme | Périmètre |
|--------|-----------|
| 1 + 2 | Infra, Proxmox, pfSense, AD, topologie LAN/DMZ |
| 3 + 4 | SOC, Red Team, portail, scénarios d’attaque |
| Tous | Validation de phase (CHECKLIST.md) |

## Réunions

- **Hebdo** : _jour / heure_ — point d’avancement + blocages
- **Fin de phase** : démo + case à cocher CHECKLIST
- **Canal** : _Discord / Teams / Matrix — à définir_
- **Dépôt** : branches par membre ou par lot (`infra/pfsense`, `soc/wazuh`, etc.)

## Décisions à tracer ici

| Date | Sujet | Décision | Validé par |
|------|-------|----------|------------|
| 2026-05 | Serveur OVH | Dédié KS-5 `ns3138292` — IP 51.77.52.56 — Proxmox 9 préinstallé | Marwane |
| | Samba AD vs Windows Server | | |
| 2026-05 | Plages IP internes | LAN .10 / DMZ .20 / SOC .30 / LAB-RT .99 | À valider équipe |
| | Hôte Docker | VM dédiée docker-soc01 | |
