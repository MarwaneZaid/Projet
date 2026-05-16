# Mini-Cloud SOC & Red Team — Projet équipe (4 personnes)

Plateforme de virtualisation, Active Directory, SOC, Red Team et portail d’audit de sécurité — déployée sur serveur à ressources limitées (Proxmox).

## Équipe & inversion des rôles

| Poste | Profil d’origine | Rôle dans le projet |
|-------|------------------|---------------------|
| Étudiant 1 | Cybersécurité | Infrastructure & virtualisation (Proxmox, VM, topologie) |
| Étudiant 2 | Cybersécurité | Réseau & Windows (pfSense, AD, logs) |
| Étudiant 3 | Réseau & systèmes | SOC & automatisation (Wazuh, Suricata, n8n, Grafana…) |
| Étudiant 4 | Réseau & systèmes | Red Team & portail client (CALDERA, BloodHound, site web) |

Chaque membre suit l’ensemble du projet ; les binômes valident collectivement chaque phase (voir [CHECKLIST.md](CHECKLIST.md)).

## Objectifs

- Mini-cloud **Proxmox VE**
- **Active Directory** (Samba AD ou Windows Server selon choix matériel)
- **SOC** : Wazuh, Suricata, TheHive, Cortex, Grafana
- **Red Team** : CALDERA, BloodHound, OpenVAS — scénarios simulés uniquement
- **VPN** site-to-site, **DMZ**, reverse proxy
- Extension : **portail client / admin** (branche Audit de Sécurité)

## Structure du dépôt

```
├── docs/              # Rapport, wiki, schémas, procédures
├── infra/             # Proxmox, pfSense, AD, VPN
├── soc/               # Stack Docker SOC
├── redteam/           # Stack Docker Red Team (lab isolé)
├── portal/            # Site client + admin (extension)
├── ansible/           # Automatisation & sauvegardes
├── TEAM.md            # Contacts, réunions, décisions
└── CHECKLIST.md       # Validation par phase
```

## Calendrier prévisionnel

| Période | Focus |
|---------|--------|
| Oct. – Nov. | Plan, périmètre, répartition validée |
| Déc. – Jan. | Infra : Proxmox, pfSense, AD, hôte Docker Linux |
| Fév. – Mars | SOC + Red Team en conteneurs |
| Avr. – Mai | Ansible, sauvegardes, durcissement |
| Juin | Tests intégrés (SOC, Red Team, Zero Trust) |
| Juil. | Rapport, wiki, démo orale |

## Démarrage rapide

1. Lire [docs/plan-operationnel.md](docs/plan-operationnel.md) et compléter [TEAM.md](TEAM.md) (noms, binômes).
2. Renseigner les specs serveur dans [docs/architecture/specs-materiel.md](docs/architecture/specs-materiel.md).
3. Phase infra : suivre [infra/README.md](infra/README.md).
4. Avant toute attaque simulée : isoler le lab Red Team et documenter le périmètre légal/école.

## Livrables finaux

- Rapport technique (~10 pages)
- Documentation WikiJS (client + interne)
- Schéma réseau + architecture SOC
- Pitch « entreprise IT »
- Site web (si extension réalisée)

## Règles d’équipe

- **Pas de secrets dans Git** — utiliser `.env` local (voir `.env.example` par stack).
- **Validation collective** avant passage à la phase suivante ([CHECKLIST.md](CHECKLIST.md)).
- **Red Team** : uniquement sur VMs/lab dédiés, jamais sur production ou réseau campus sans accord écrit.
