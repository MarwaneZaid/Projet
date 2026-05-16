# Red Team — laboratoire isolé

**Responsable lead** : Étudiant 4 · **Relecteur** : Étudiant 3

## Règles impératives

- Segment **192.168.99.0/24** (ou équivalent) **sans accès routé vers LAN prod**
- Scénarios **uniquement** sur VMs et comptes de lab
- Accord écrit établissement / encadrant avant toute simulation
- Journaliser chaque exercice : date, outil, cible, résultat, preuves SOC

## Outils

| Outil | Rôle | Déploiement |
|-------|------|-------------|
| OpenVAS | Scan vulnérabilités | Docker ou VM dédiée |
| BloodHound | Chemins AD | poste analyste + collecte SharpHound sur lab |
| CALDERA | Adversary emulation | `docker-compose.yml` (à compléter) |

## Scénarios prévus (exemples)

1. Brute force SSH / RDP sur honeypot lab
2. Énumération AD → chemins BloodHound
3. Campagne CALDERA « discovery » sans exfil réelle

## Livrable

Rapport par scénario dans `docs/livrables/redteam/` : TTP, IOC, corrélation avec alertes Wazuh.
