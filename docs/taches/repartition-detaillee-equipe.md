# Répartition détaillée des tâches par membre

Guide **qui fait quoi**, **comment**, et **pourquoi**, dans l’ordre du projet.

Fiches techniques avec cases à cocher : voir les fichiers `00` à `09` dans ce dossier.

---

## Vue d’ensemble

| # | Profil d'origine | Rôle dans le projet | Fichier détaillé |
|---|------------------|---------------------|------------------|
| **Étudiant 1** | Cybersécurité | Infra, OVH, Proxmox, VMs | [01-proxmox-virtualisation.md](01-proxmox-virtualisation.md) |
| **Étudiant 2** | Cybersécurité | Réseau pfSense, AD, VPN/DMZ | [02-reseau-pfsense.md](02-reseau-pfsense.md), [03-active-directory.md](03-active-directory.md), [07-vpn-dmz-reverse-proxy.md](07-vpn-dmz-reverse-proxy.md) |
| **Étudiant 3** | Réseau & systèmes | SOC, Docker, Ansible | [04-soc.md](04-soc.md), [06-automatisation-ansible.md](06-automatisation-ansible.md) |
| **Étudiant 4** | Réseau & systèmes | Red Team, portail (option) | [05-red-team.md](05-red-team.md), [09-portail-audit.md](09-portail-audit.md) |

**Règle d'équipe :** chaque binôme **relit** le travail de l'autre avant de valider une phase ([CHECKLIST.md](../../CHECKLIST.md)).

### Binômes de relecture

| Binôme | Périmètre |
|--------|-----------|
| 1 + 2 | Infra, Proxmox, pfSense, AD, topologie LAN/DMZ |
| 3 + 4 | SOC, Red Team, portail, scénarios d'attaque |
| Tous | Validation de phase (CHECKLIST) |

---

## Phase 0 — Tous ensemble (avant toute installation)

**Pourquoi :** sans accord commun, vous installez des choses incompatibles (IP, AD, RAM).

| Tâche | Qui | Quoi faire exactement | Pourquoi |
|-------|-----|------------------------|----------|
| Compléter [TEAM.md](../../TEAM.md) | Tous | 4 noms, emails, canal Discord/Teams, jour de réunion | Savoir qui contacter |
| Lire [plan-operationnel.md](../plan-operationnel.md) | Tous | Valider objectifs et calendrier | Même vision du projet |
| Choisir **Samba AD** ou **Windows Server** | Tous → noter dans TEAM.md | Samba = moins de RAM, pas de licence ; Windows = plus réaliste entreprise | Impact VM `ad-dc01` (4 Go vs 8 Go) |
| Valider les plages IP | Tous | LAN `192.168.10.0/24`, DMZ `192.168.20.0/24`, SOC `192.168.30.0/24`, lab RT `192.168.99.0/24` | Tout le réseau s'aligne dessus |
| Schéma réseau v0 | Ét. 1 + 2 | Draw.io → PNG dans `docs/architecture/diagrams/` | Obligatoire pour le rapport |
| Accord Red Team écrit | Tous | Email/PDF encadrant : attaques **uniquement** sur lab `.99` | Légal + école |
| Accès GitHub | Responsable repo | Inviter les 3 en collaborateurs | Partager code et docs |
| Fiche serveur OVH | Ét. 1 | Remplir [serveur-ovh-fiche.md](../infra/serveur-ovh-fiche.md) | Inventaire matériel |

**Critères phase 0 validée :** TEAM.md complet, schéma IP + PNG validés, choix AD acté, tout le monde a cloné le repo.

---

## Étudiant 1 — Infra & Proxmox

**Mission :** faire tourner le mini-cloud sur le serveur OVH (`51.77.52.56`, 32 Go RAM, Proxmox VE 9).

**Dépôt :** [infra/proxmox/](../../infra/proxmox/), [infra/README.md](../../infra/README.md)

**Relecteur :** Étudiant 2

### Bloc A — Accès serveur (bloquant)

| # | Quoi faire | Comment | Pourquoi |
|---|------------|---------|----------|
| A1 | Accès **root** au serveur | Réinstall Proxmox via template OVH **ou** mode rescue + `passwd root` | Sans root, rien d'autre ne démarre |
| A2 | Firewall OVH Edge | IP équipe (ex. `46.193.6.82/32`) sur ports **22** et **8006** | SSH + UI Proxmox depuis l'extérieur |
| A3 | Tester l'accès | `nc -zv 51.77.52.56 22 8006`, puis `ssh root@51.77.52.56` | Valider avant de continuer |
| A4 | Activer SSH sur l'hôte | `systemctl enable --now ssh` (console KVM si besoin) | L'équipe se connecte à distance |

Guide : [01-firewall-ovh.md](../infra/01-firewall-ovh.md), [02-premier-acces-proxmox.md](../infra/02-premier-acces-proxmox.md)

> **Note :** le mot de passe **compte OVH Manager** ≠ mot de passe **root** du serveur.

### Bloc B — Proxmox (P1)

| # | Quoi faire | Comment | Pourquoi |
|---|------------|---------|----------|
| B1 | Mises à jour hôte | `apt update && apt full-upgrade` ou `scripts/proxmox/01-host-postinstall.sh` | Sécurité et stabilité |
| B2 | Stockage | Datacenter → Storage ; `pvesm status`, `lsblk` | Savoir où créer les disques VMs (~4 To RAID) |
| B3 | Réseau Proxmox | Bridge `vmbr0` (et `vmbr1` ou VLAN si possible) | Brancher les VMs au réseau |
| B4 | Politique snapshots | Snapshot avant chaque changement majeur ; doc 1 paragraphe | Retour arrière en cas d'erreur |
| B5 | Template cloud-init | Debian 12 ou Ubuntu 22.04 | Créer des VMs rapidement |
| B6 | Créer les VMs vides | Voir tableau ci-dessous ; script `02-create-vms.sh` | Les autres installent l'OS dedans |
| B7 | Inventaire VMs | [inventaire-vms.md](../architecture/inventaire-vms.md) : ID, IP, vCPU, RAM, rôle | Référence pour toute l'équipe |

**VMs à créer sur Proxmox :**

| VM | vCPU | RAM | Disque | Segment | Pour qui |
|----|------|-----|--------|---------|----------|
| `fw-pfsense` | 1 | 1 Go | 20 Go | WAN + LAN | Ét. 2 |
| `ad-dc01` | 2 | 4–8 Go | 60 Go | LAN (.10) | Ét. 2 |
| `docker-soc01` | 2 | 8 Go | 100 Go | SOC (.30) | Ét. 3 |
| `lab-rt01` | 2 | 4 Go | 40 Go | LAB-RT (.99) | Ét. 4 |
| `win-client01` | 2 | 4 Go | 40 Go | LAN (.10) | Ét. 2 |

**Total RAM VMs :** ~19–21 Go sur 32 Go → marge pour l'hôte Proxmox.

### Bloc C — Plus tard (P2–P3)

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| C1 | Job backup Proxmox (snapshot/backup vers 2e disque) | Récupération après panne |
| C2 | Restreindre UI Proxmox au LAN admin (pfSense ou firewall hôte) | Ne pas exposer 8006 inutilement |
| C3 | Avec Ét. 3 : inventaire Ansible, test restore snapshot | Automatisation et DR |

### Critères « Proxmox validé »

- [ ] Au moins 3 VMs créées (pfSense, AD, Docker)
- [ ] Snapshots fonctionnels
- [ ] Inventaire VMs à jour
- [ ] Relecture Étudiant 2 OK

---

## Étudiant 2 — Réseau pfSense & Active Directory

**Mission :** réseau interne + identité (comme une PME).

**Dépôt :** [infra/pfsense/](../../infra/pfsense/), [infra/active-directory/](../../infra/active-directory/)

**Relecteurs :** Ét. 1 (pfSense), Ét. 3 (logs AD pour SOC)

### Partie 1 — pfSense (dès que VM `fw-pfsense` existe)

| # | Quoi faire | Comment | Pourquoi |
|---|------------|---------|----------|
| 2.1 | Installer pfSense | ISO sur la VM ; assignation interfaces WAN + LAN | Firewall central du projet |
| 2.2 | Interface WAN | Uplink Internet (IP publique OVH / bridge Proxmox) | Updates, DNS, sortie |
| 2.3 | Interface LAN | Passerelle ex. `192.168.10.1/24` | Réseau admin + AD |
| 2.4 | DHCP sur LAN | Plage ex. `192.168.10.100–200` | IP automatiques pour les VMs |
| 2.5 | Réservations DHCP | IP fixes : AD, Docker, pfSense | IP stables après reboot |
| 2.6 | NAT sortant | LAN → Internet | `apt`, agents Wazuh, updates |
| 2.7 | Firewall WAN | Refuser tout entrant par défaut | Pas d'exposition accidentelle |
| 2.8 | Interface DMZ (OPT) | `192.168.20.0/24` | Services exposés plus tard (reverse proxy) |
| 2.9 | Isolation DMZ | DMZ **ne joint pas** le LAN (test ping = échec) | Sécurité par segments |
| 2.10 | Logs firewall | Status → System Logs → Firewall | Audit réseau |
| 2.11 | Backup config XML | Export daté dans `docs/procedures/` | Restaurer pfSense |
| 2.12 | Préparer syslog distant | Vers IP manager Wazuh (quand SOC prêt) | Centraliser logs firewall |

**Tests validation pfSense :**

```text
Depuis VM LAN : ping passerelle pfSense → OK
Depuis VM LAN : ping Internet (8.8.8.8) → OK
Depuis DMZ : ping LAN → ÉCHEC attendu
```

### Partie 2 — Active Directory (après pfSense LAN OK)

| # | Quoi faire | Samba AD | Windows Server |
|---|------------|----------|----------------|
| 3.1 | Installer contrôleur de domaine | `samba-ad-dc` / provision | Promote Server + AD DS |
| 3.2 | Créer le domaine | Ex. `lab.local` | Idem |
| 3.3 | Vérifier DNS | `nslookup lab.local` depuis client | Résolution domaine OK |

| # | Quoi faire | Détail | Pourquoi |
|---|------------|--------|----------|
| 3.4 | Structure OU | Users, Servers, Workstations, ServiceAccounts | Organisation propre |
| 3.5 | Groupes | IT-Admins, Lab-Users (pas tout le monde admin) | Bonnes pratiques |
| 3.6 | 10 utilisateurs test | CSV ou script documenté | Scénarios réalistes |
| 3.7 | GPO mots de passe | Longueur, complexité | Politique sécurité |
| 3.8 | GPO audit connexions | Event ID 4624/4625 visibles | Détection brute force AD |
| 3.9 | Joindre 2 clients Windows | `win-client01` + autre VM | Prouver que l'AD fonctionne |
| 3.10 | Compte `wazuh-agent` | Lecture logs, pas admin domaine | Agent SOC sans trop de privilèges |
| 3.11 | Forward logs AD | Syslog ou agent vers Wazuh (avec Ét. 3) | Le SOC voit les connexions AD |

### Partie 3 — VPN / DMZ (P3, plus tard)

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| 7.1 | Segment DMZ isolé (rappel test ping) | Base pour exposition contrôlée |
| 7.2 | Schéma mis à jour : Internet → pfSense → DMZ | Rapport |
| 7.3 | Nginx ou Traefik en DMZ + TLS | Reverse proxy professionnel |
| 7.4 | NAT 443 WAN → proxy (si applicable) | Accès externe documenté |
| 7.5 | VPN site-to-site (ou doc si impossible) | Extension multi-sites |

### Critères « pfSense + AD validés »

- [ ] NAT + DHCP opérationnels
- [ ] Isolation DMZ/LAN démontrée
- [ ] Login domaine sur 2 clients
- [ ] GPO audit visible dans Event Viewer
- [ ] Compte agent Wazuh créé ; Ét. 3 confirme exploitabilité des logs

---

## Étudiant 3 — SOC & automatisation

**Mission :** détecter les attaques et les visualiser (Wazuh, Grafana, Suricata, TheHive…).

**Dépôt :** [soc/](../../soc/), [docs/architecture/architecture-soc.md](../architecture/architecture-soc.md)

**Relecteur :** Étudiant 4

**Prérequis :** VM `docker-soc01`, pfSense autorise segment SOC, AD envoie des logs (tâche 3.11).

### Partie 1 — Stack SOC (P2)

| # | Quoi faire | Comment | Pourquoi |
|---|------------|---------|----------|
| 4.1 | Docker + Compose | Sur `docker-soc01` : `docker --version`, `docker compose version` | Lancer la stack |
| 4.2 | Fichier `.env` | `soc/.env.example` → `.env` sur le serveur (**jamais Git**) | Mots de passe conteneurs |
| 4.3 | Lancer la stack | `docker compose up -d` dans `soc/` | Wazuh + Grafana |
| 4.4 | Dashboard Wazuh | HTTPS port 443 mappé ; login UI OK | Vérifier que ça tourne |
| 4.5 | Règles pfSense | Ouvrir 1514/udp, 1515/tcp, 55000/tcp vers IP manager | Agents → manager |
| 4.6 | Agent sur AD | Installer sur `ad-dc01` ; statut « active » | Logs Windows/AD |
| 4.7 | Agents Linux | SOC + 1 autre VM Linux (3 sources min.) | Diversité des logs |
| 4.8 | Vérifier remontée | Login AD, SSH → visible en < 5 min | Preuve collecte |
| 4.9 | Grafana | Datasource + 1 dashboard (agents + alertes) | Livrable visuel jury |
| 4.10 | 3 règles Wazuh | Brute force SSH, logon failed AD, scan ports ; tester en déclenchant | Détection concrète |

### Partie 2 — SOC avancé (P2)

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| 4.11 | Suricata + règles Emerging Threats | IDS réseau |
| 4.12 | Documenter SPAN/miroir (quel port voit le trafic) | Architecture IDS |
| 4.13 | TheHive + Cortex : 1 incident test + 1 analyzer | Gestion d'incident |
| 4.14 | n8n : alerte Wazuh → email ou Discord/Teams | Automatisation réponse |
| 4.15 | Playbook incident 5 étapes | `docs/wiki/soc-playbook-incident.md` | Procédure SOC écrite |

### Partie 3 — Corrélation Red Team

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| 4.18 | Avec Ét. 4 : scénario RT → vérifier **alerte SOC** correspondante | Prouver détection bout en bout |

### Partie 4 — Ansible (P3, avec Ét. 1)

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| 6.1 | `ansible/inventory/hosts.yml` avec IP réelles | Cibler les VMs |
| 6.2 | Playbook install agent Wazuh (idempotent) | Reproductible |
| 6.3 | Test `--check` puis run sur 1 VM | Valider playbook |
| 6.4 | Playbook durcissement SSH | Sécurité docker-soc01 |
| 6.5 | Playbook déploiement `soc/` (secrets hors Git) | Automatisation stack |
| 6.6 | Variables via `ansible-vault` | Pas de secrets dans le repo |
| 6.7 | Test restore snapshot Proxmox | DR documenté |
| 6.8 | Procédure restore config pfSense testée | DR réseau |

### Critères « SOC validé »

- [ ] 3+ agents actifs
- [ ] 1 dashboard Grafana utile
- [ ] 1 incident TheHive traité (même fictif)
- [ ] 1 notification n8n déclenchée
- [ ] Relecture Étudiant 4 OK

---

## Étudiant 4 — Red Team & portail (optionnel)

**Mission :** simuler des attaques **uniquement** sur le lab isolé ; prouver que le SOC réagit.

**Dépôt :** [redteam/](../../redteam/), [portal/](../../portal/) (option)

**Relecteur :** Étudiant 3

> **Règle absolue :** jamais d'attaque sur réseau campus, comptes réels, ou VMs production hors lab `192.168.99.0/24`.

### Partie 1 — Préparer le lab (P0)

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| 5.1 | Segment `192.168.99.0/24` sans routage vers LAN `.10` | Isolation légale et technique |
| 5.2 | VMs cibles = lab RT + honeypots uniquement | Périmètre écrit |
| 5.3 | Journal d'exercices | [journal-exercices.md](../livrables/redteam/journal-exercices.md) : date, outil, cible, résultat | Traçabilité |

### Partie 2 — Outils & scénarios (P1–P2)

| # | Quoi faire | Comment | Pourquoi |
|---|------------|---------|----------|
| 5.4 | OpenVAS | Docker ou VM sur lab RT uniquement | Scan vulnérabilités |
| 5.5 | Rapport scan | PDF/HTML dans `docs/livrables/redteam/` | Livrable |
| 5.6 | BloodHound | Collector + import sur AD **lab** | Chemins d'attaque AD |
| 5.7 | CALDERA | 1 agent + campagne « discovery » | Attaque simulée contrôlée |
| 5.8 | Scénario 1 | Brute force honeypot SSH/RDP (pas vrai AD prod) | Déclencher alerte SOC |
| 5.9 | Scénario 2 | Énumération AD lab | TTP documentés |
| 5.10 | Tableau MITRE | IOC, heure exacte, outil par scénario | Rapport professionnel |
| 5.11 | Avec Ét. 3 | Capture alerte Wazuh correspondante | Lien RT ↔ SOC |

### Partie 3 — Portail audit (P5, **seulement si P1–P2 terminés**)

| # | Quoi faire | Pourquoi |
|---|------------|----------|
| 9.1 | Maquettes client + admin | UX validée équipe |
| 9.2 | Schéma BDD (users, projects, quotes) | Base données |
| 9.3 | Stack documentée (ex. Next.js + PostgreSQL) | Choix technique |
| 9.4 | Auth sécurisée (bcrypt, sessions) | Sécurité web |
| 9.5 | Espace client : demande d'audit + statut | MVP client |
| 9.6 | Espace admin : liste demandes + statuts | MVP admin |
| 9.7+ | Messagerie, devis, lien rapport OpenVAS | Extension |

### Critères « Red Team validé »

- [ ] 2 scénarios documentés + corrélés SOC
- [ ] OpenVAS + BloodHound livrables (sans données sensibles)
- [ ] Aucun incident réel / plainte réseau école
- [ ] Relecture Étudiant 3 OK

---

## Tous — Livrables finaux (P4)

**Fichier :** [08-livrables-rapport.md](08-livrables-rapport.md)

| Qui | Quoi | Détail |
|-----|------|--------|
| **Tous** | Date soutenance + répartition chapitres rapport | Planifié en début de phase 4 |
| **Ét. 1** | Chapitre architecture infra | Proxmox, VMs, stockage, OVH |
| **Ét. 2** | Chapitre réseau + AD | pfSense, GPO, schémas |
| **Ét. 3** | Chapitre SOC | Wazuh, Grafana, playbook, tests |
| **Ét. 4** | Chapitre Red Team | Scénarios, MITRE, corrélation SOC |
| **Tous** | Exercice intégré | 1 attaque chronométrée + réponse SOC (2 pages) |
| **Tous** | Wiki procédures | Min. 5 pages dans `docs/wiki/` |
| **Tous** | Pitch 10–15 min + script démo | `docs/livrables/script-demo.md` |
| **Tous** | FAQ jury (10 questions) | Préparation soutenance |

---

## Ordre chronologique (dépendances)

```
Phase 0  →  TOUS (cadrage, IP, schéma, TEAM.md)
    ↓
Ét. 1    →  Accès OVH + Proxmox + VMs créées + inventaire
    ↓
Ét. 2    →  pfSense → AD → clients Windows → logs AD
    ↓
Ét. 3    →  Docker SOC → agents → Grafana → règles → TheHive/n8n
    ↓
Ét. 4    →  Lab RT isolé → OpenVAS → scénarios → corrélation SOC
    ↓
Ét. 2+3  →  VPN/DMZ, Ansible, sauvegardes (P3)
    ↓
TOUS     →  Rapport, wiki, pitch, démo (P4)
    ↓
Ét. 4    →  Portail audit si temps (P5)
```

---

## État d'avancement (mai 2026)

| Personne | Statut actuel |
|----------|----------------|
| **Ét. 1** | Firewall OVH configuré (`46.193.6.82`) ; accès **root** serveur à finaliser (réinstall Proxmox ou rescue) |
| **Ét. 2** | En attente des VMs Proxmox |
| **Ét. 3** | En attente de `docker-soc01` + réseau SOC |
| **Ét. 4** | En attente du lab isolé + SOC pour corrélation |

---

## Liens utiles

| Sujet | Fichier |
|-------|---------|
| Guide priorités P0–P5 | [README.md](README.md) |
| Serveur OVH | [serveur-ovh-fiche.md](../infra/serveur-ovh-fiche.md) |
| Firewall OVH | [01-firewall-ovh.md](../infra/01-firewall-ovh.md) |
| Journal configuration | [journal-configuration.md](../infra/journal-configuration.md) |
| Validation phases | [CHECKLIST.md](../../CHECKLIST.md) |
| Contacts équipe | [TEAM.md](../../TEAM.md) |
