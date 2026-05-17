# 04 — SOC (détection & réponse)

**Responsable :** Étudiant 3 (profil réseau → rôle sécurité)  
**Relecteur :** Étudiant 4  
**Priorité globale :** P2  
**Dépôt :** [soc/](../../soc/), [docs/architecture/architecture-soc.md](../architecture/architecture-soc.md)

**Prérequis :** VM Docker sur segment SOC (1.11), pfSense LAN→SOC autorisé, AD avec logs (3.11)

---

## P0 — Bloquant

| # | Tâche exacte | Commande / chemin | Validé |
|---|--------------|-------------------|--------|
| 4.1 | Installer Docker + Docker Compose sur `docker-soc01` | `docker --version`, `docker compose version` | [ ] |
| 4.2 | Copier `soc/.env.example` → `.env` (sur le serveur, **pas dans Git**) | Mots de passe forts uniques | [ ] |
| 4.3 | Lancer stack de base : `docker compose up -d` dans `soc/` | Conteneurs `running` | [ ] |
| 4.4 | Accéder au dashboard Wazuh (HTTPS port 443 mappé) | Login UI OK | [ ] |

---

## P1 — Critique

| # | Tâche exacte | Détail | Validé |
|---|--------------|--------|--------|
| 4.5 | Ouvrir sur pfSense : **1514/udp**, **1515/tcp**, **55000/tcp** vers IP manager | Règles documentées | [ ] |
| 4.6 | Installer **agent Wazuh** sur contrôleur AD | Agent « active » dans UI | [ ] |
| 4.7 | Installer agent sur `docker-soc01` + 1 autre VM Linux | 3 sources minimum | [ ] |
| 4.8 | Vérifier remontée d’événements dans Wazuh (login AD, ssh, etc.) | Alertes ou logs visibles < 5 min | [ ] |
| 4.9 | **Grafana** : datasource vers Wazuh/Elastic + **1 dashboard** (agents + alertes) | Capture PNG pour rapport | [ ] |
| 4.10 | Règles Wazuh : au moins 3 règles pertinentes (brute force SSH, logon failed AD, scan ports) | Tester en déclenchant l’événement | [ ] |

---

## P2 — Important

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 4.11 | Déployer **Suricata** (conteneur ou VM) + règles Emerging Threats de base | [ ] |
| 4.12 | Documenter **SPAN/miroir** : quel port voit le trafic | [ ] |
| 4.13 | **TheHive** + **Cortex** : créer 1 incident test + 1 analyzer | [ ] |
| 4.14 | **n8n** : webhook alerte Wazuh → email ou message Teams/Discord | [ ] |
| 4.15 | Playbook incident écrit (5 étapes : détection → triage → containment → analyse → clôture) | `docs/wiki/soc-playbook-incident.md` | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 4.16 | Exporter JSON dashboard Grafana dans `soc/grafana/dashboards/` | [ ] |
| 4.17 | Durcissement : Grafana/Wazuh non exposés sur WAN | [ ] |

---

## Corrélation Red Team (à faire avec partie 05)

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 4.18 | Lors d’un scénario RT : noter l’heure, TTP, et vérifier qu’une **alerte SOC** correspond | [ ] |

---

## Critères « SOC validé »

- [ ] 3+ agents actifs  
- [ ] 1 dashboard Grafana utile  
- [ ] 1 incident TheHive traité (même fictif)  
- [ ] 1 notification n8n déclenchée  
- [ ] Relecture Étudiant 4 OK  

**Ensuite :** [05-red-team.md](05-red-team.md) en parallèle contrôlé
