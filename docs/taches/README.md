# Guide des tâches — Projet Mini-Cloud SOC

Suivi **sur GitHub uniquement** (sans Trello). Chaque fichier décrit **quoi faire exactement**, dans quel ordre, et la **priorité**.

## Légende des priorités

| Niveau | Signification | Quand |
|--------|---------------|-------|
| **P0** | Bloquant — à faire en premier | Sans ça, rien d’autre ne démarre |
| **P1** | Critique — cœur du projet | Indispensable pour la démo |
| **P2** | Important — valeur ajoutée forte | Attendu pour une note complète |
| **P3** | Utile — professionnalisation | Automatisation, sauvegardes, VPN |
| **P4** | Livrables finaux | Rapport, pitch, présentation |
| **P5** | Optionnel | Extension portail audit |

## Ordre global recommandé

```
P0 Cadrage → P1 Infra (Proxmox → pfSense → AD) → P1 Docker host
         → P2 SOC → P2 Red Team (lab isolé) → P3 Ansible / sauvegardes
         → P4 Tests intégrés + rapport → P5 Portail (si temps)
```

## Répartition par membre (détaillée)

**Guide complet :** [repartition-detaillee-equipe.md](repartition-detaillee-equipe.md) — qui fait quoi, comment, pourquoi, ordre chronologique.

## Fichiers par partie

| Fichier | Périmètre | Responsable | Priorité max |
|---------|-----------|-------------|--------------|
| [00-cadrage-equipe.md](00-cadrage-equipe.md) | Plan, équipe, IP, matériel | Tous | P0 |
| [../infra/ovh-serveur.md](../infra/ovh-serveur.md) | Serveur OVH : accès, firewall, Proxmox | Étudiant 1 | P0–P1 |
| [01-proxmox-virtualisation.md](01-proxmox-virtualisation.md) | Proxmox, VMs, stockage | Étudiant 1 | P1 |
| [02-reseau-pfsense.md](02-reseau-pfsense.md) | pfSense, NAT, firewall, DHCP | Étudiant 2 | P1 |
| [03-active-directory.md](03-active-directory.md) | AD, GPO, logs | Étudiant 2 | P1 |
| [04-soc.md](04-soc.md) | Wazuh, Suricata, Grafana, TheHive | Étudiant 3 | P2 |
| [05-red-team.md](05-red-team.md) | CALDERA, BloodHound, OpenVAS | Étudiant 4 | P2 |
| [06-automatisation-ansible.md](06-automatisation-ansible.md) | Ansible, sauvegardes | Étudiant 3 + 1 | P3 |
| [07-vpn-dmz-reverse-proxy.md](07-vpn-dmz-reverse-proxy.md) | VPN, DMZ, TLS | Étudiant 2 | P3 |
| [08-livrables-rapport.md](08-livrables-rapport.md) | Rapport, wiki, pitch, démo | Tous | P4 |
| [09-portail-audit.md](09-portail-audit.md) | Site client / admin | Étudiant 4 | P5 |

## Validation collective

À la fin de chaque bloc P1 / P2 / P3 / P4 : réunion équipe + cases à cocher dans [CHECKLIST.md](../../CHECKLIST.md).

## Mise à jour

Quand une tâche est terminée : cocher dans le fichier concerné et ouvrir une PR GitHub avec preuve (capture, log, lien commit).
