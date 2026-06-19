# Guide complet — MVP SOC (Étudiant 3)

Document de référence pour comprendre, préparer et livrer la partie **SOC** du projet mini-cloud NexaMind / 4eSGI.

**Public :** Marwane Zaid (responsable SOC) et relecteurs.  
**Périmètre :** Wazuh + agents + dashboard + 3 alertes démontrées.  
**Runbook opérationnel (actions rapides) :** [04-mvp-soc-runbook-unifie.md](04-mvp-soc-runbook-unifie.md)

---

## Table des matières

1. [Résumé exécutif](#1-résumé-exécutif)
2. [Ton rôle dans le projet](#2-ton-rôle-dans-le-projet)
3. [Architecture globale](#3-architecture-globale)
4. [Glossaire — toutes les notions à connaître](#4-glossaire--toutes-les-notions-à-connaître)
5. [Compétences à maîtriser](#5-compétences-à-maîtriser)
6. [Accès à l'infrastructure](#6-accès-à-linfrastructure)
7. [La stack SOC expliquée](#7-la-stack-soc-expliquée)
8. [Ports, protocoles et flux réseau](#8-ports-protocoles-et-flux-réseau)
9. [Procédure MVP — étape par étape](#9-procédure-mvp--étape-par-étape)
10. [Les 3 scénarios d'alerte (détail + exemples)](#10-les-3-scénarios-dalerte-détail--exemples)
11. [Captures d'écran et livrables](#11-captures-décran-et-livrables)
12. [Critères de validation (Go / No-Go)](#12-critères-de-validation-go--no-go)
13. [Ressources d'apprentissage (filtrées pour ton projet)](#13-ressources-dapprentissage-filtrées-pour-ton-projet)
14. [Coordination avec l'équipe](#14-coordination-avec-léquipe)
15. [Dépannage fréquent](#15-dépannage-fréquent)
16. [Sécurité et bonnes pratiques](#16-sécurité-et-bonnes-pratiques)
17. [FAQ](#17-faq)
18. [Annexes — chemins du dépôt](#18-annexes--chemins-du-dépôt)

---

## 1. Résumé exécutif

### Qu'est-ce que tu construis ?

Un **SOC minimal** (Security Operations Center) : un poste de surveillance qui **collecte les logs**, **détecte des comportements suspects** et **affiche des alertes** sur un dashboard.

### Objectif MVP (non négociable)

| # | Livrable | Preuve |
|---|----------|--------|
| 1 | Stack Wazuh + Grafana déployée sur `docker-soc01` | `docker compose ps` → tout en `Up` |
| 2 | ≥ 3 agents Wazuh actifs | Capture liste agents `Active` |
| 3 | 1 dashboard exploitable | Wazuh natif ou Grafana |
| 4 | 3 alertes différentes simulées | SSH bruteforce, AD 4625, scan nmap |
| 5 | Tableau de preuves rempli | `docs/livrables/soc-mvp-preuves.md` |

### Ce que le SOC **fait** vs **ne fait pas**

| Le SOC fait | Le SOC ne fait pas (dans le MVP) |
|-------------|----------------------------------|
| Observer et alerter | Bloquer automatiquement les attaques (ce n'est pas un firewall) |
| Centraliser les logs | Remplacer pfSense ou l'AD |
| Corréler des événements | Gérer des tickets d'incident (TheHive = phase 2) |
| Documenter des preuves pour le rapport | Attaquer des systèmes réels (uniquement lab simulé) |

---

## 2. Ton rôle dans le projet

### Équipe (inversion des rôles)

| Étudiant | Rôle projet | Lien avec le SOC |
|----------|-------------|------------------|
| Étudiant 1 | Proxmox, VMs, stockage | Doit fournir la VM `docker-soc01` |
| Étudiant 2 | pfSense, Active Directory | Doit ouvrir les flux réseau + agent sur AD |
| **Étudiant 3 (toi)** | **SOC Wazuh/Grafana** | Déploie, enrôle agents, démontre alertes |
| Étudiant 4 | Red Team (lab isolé) | Simule attaques → ton SOC doit les voir |

### Ton périmètre strict

**Tu fais :**
- Déploiement Docker de la stack dans `soc/`
- Installation / validation des agents Wazuh
- Configuration d'un dashboard
- Simulation des 3 scénarios d'alerte
- Captures + tableau de preuves

**Tu ne fais pas (sauf blocage total) :**
- Création des VMs Proxmox
- Configuration pfSense complète
- Déploiement AD
- Red Team / portail web
- TheHive, Cortex, n8n, Suricata (phase 2)

---

## 3. Architecture globale

### Vue d'ensemble

```
                    Internet
                        │
                        ▼
              ┌─────────────────┐
              │  Serveur OVH    │
              │  51.77.52.56    │
              │  Proxmox VE 9   │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐   ┌──────────┐   ┌──────────┐
    │ pfSense │   │ ad-dc01  │   │docker-   │
    │ (FW/VPN)│   │ (AD)     │   │soc01     │
    └─────────┘   └──────────┘   │ Wazuh    │
         │             │         │ Grafana  │
         │             │         └────┬─────┘
         │             │              │
         └─────────────┴──────────────┘
                    LAN interne
              (accessible via VPN)
```

### Segments réseau (référence équipe Abdoul)

| Réseau | Rôle | Exemples d'IP |
|--------|------|---------------|
| `192.168.10.0/24` | WAN intermédiaire (pfSense ↔ Proxmox) | pfSense WAN : `192.168.10.1` |
| `192.168.20.0/24` | LAN principal | pfSense LAN : `192.168.20.1`, Proxmox UI : `192.168.20.254:8006` |
| `10.10.10.0/24` | Tunnel VPN OpenVPN | Client VPN : `10.10.10.x` |
| Segment SOC (cible projet) | VMs SOC | `docker-soc01` : ex. `192.168.30.x` |

> **Important :** l'accès **normal** à Proxmox se fait via **VPN** → `https://192.168.20.254:8006`, pas via l'IP publique `51.77.52.56` (réservée à l'admin infra avec règles iptables spécifiques).

### Pipeline SOC (flux de données)

```
[Machine surveillée]          [Stack SOC]
     │                              │
     │  logs / events               │
     ▼                              ▼
 Agent Wazuh  ──1514/udp──►  Wazuh Manager
                                   │
                                   ▼
                            Wazuh Indexer
                            (stockage / recherche)
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
            Wazuh Dashboard   Grafana      Règles d'alerte
            (visualisation)  (métriques)   (détection)
```

---

## 4. Glossaire — toutes les notions à connaître

### Infrastructure

| Terme | Définition | Exemple dans le projet |
|-------|------------|------------------------|
| **Hyperviseur** | Logiciel qui héberge des machines virtuelles | Proxmox VE sur le serveur OVH |
| **VM (Machine virtuelle)** | Serveur simulé sur l'hyperviseur | `docker-soc01`, `ad-dc01`, `lab-rt01` |
| **Proxmox VE** | Plateforme de virtualisation open source | UI web sur port `8006` |
| **Bridge réseau (vmbr)** | Interface réseau virtuelle Proxmox | `vmbr0` (WAN), `vmbr1`, `vmbr2` (LAN) |
| **OVH Dedicated** | Serveur physique loué chez OVH | `ns3138292` — IP `51.77.52.56` |
| **Edge Network Firewall** | Pare-feu réseau OVH (avant le serveur) | Autorise ports 22, 8006 depuis IP équipe |
| **KVM / IPMI** | Console distante (écran/clavier du serveur) | Accès quand SSH ne répond pas |

### Réseau

| Terme | Définition | Exemple |
|-------|------------|---------|
| **IP publique** | Adresse visible sur Internet | `51.77.52.56` |
| **IP privée** | Adresse interne au lab | `192.168.20.x`, `192.168.30.x` |
| **Port** | Numéro identifiant un service | `22` = SSH, `8006` = Proxmox, `443` = HTTPS |
| **TCP / UDP** | Protocoles de transport | Agent Wazuh : UDP `1514`, enrôlement TCP `1515` |
| **VPN** | Tunnel chiffré pour accéder au réseau interne | OpenVPN → réseau `10.10.10.0/24` |
| **NAT** | Traduction d'adresses | pfSense fait du NAT WAN ↔ LAN |
| **Firewall** | Filtre le trafic réseau | pfSense + iptables hôte + firewall OVH |
| **Timeout vs Refused** | Timeout = pas de réponse (filtrage/down) ; Refused = service absent mais machine joignable | Ton cas actuel = **timeout** |

### Sécurité / SOC

| Terme | Définition | Exemple |
|-------|------------|---------|
| **SOC** | Centre opérationnel de sécurité — équipe/outil qui surveille | Ta VM `docker-soc01` + Wazuh |
| **SIEM** | Security Information and Event Management — collecte + corrélation + alertes | Wazuh est un SIEM |
| **Log** | Enregistrement d'un événement système | Tentative SSH échouée, login AD refusé |
| **Agent** | Petit programme installé sur une machine surveillée | Agent Wazuh sur AD, Linux, SOC |
| **Alerte** | Notification qu'une règle de détection a matché | Brute force SSH détectée |
| **Règle (rule)** | Condition qui déclenche une alerte | Ex. « >5 échecs SSH en 2 min » |
| **False positive** | Alerte incorrecte (comportement normal) | À documenter si ça arrive |
| **IDS / IPS** | Détection / prévention d'intrusion réseau | Suricata (phase 2, pas MVP) |
| **Brute force** | Tentatives répétées de deviner un mot de passe | 8× `ssh fakeuser@IP` |
| **Port scan** | Exploration des ports ouverts d'une cible | `nmap -sS IP_CIBLE` |
| **Event ID 4625** | Événement Windows « échec de connexion » | Alerte AD failed logon |

### Outils du projet

| Terme | Définition | Rôle |
|-------|------------|------|
| **Wazuh Manager** | Cerveau du SIEM — reçoit logs, applique règles | Conteneur `wazuh-manager` |
| **Wazuh Indexer** | Base de recherche/stockage (OpenSearch) | Conteneur `wazuh-indexer` |
| **Wazuh Dashboard** | Interface web de visualisation | Conteneur `wazuh-dashboard`, port `443` |
| **Grafana** | Outil de dashboards et graphiques | Conteneur `grafana`, port `3000` |
| **Docker Compose** | Orchestration multi-conteneurs | Fichier `soc/docker-compose.yml` |
| **pfSense** | Firewall/router open source | Gère VPN, NAT, règles LAN |
| **Active Directory (AD)** | Annuaire Microsoft (identités, domaine) | VM `ad-dc01`, domaine `nexamind.local` |
| **OpenVPN** | VPN pour accéder au lab depuis l'extérieur | Profil `.ovpn` personnel `m.zaid` |

---

## 5. Compétences à maîtriser

### Niveau minimum pour livrer le MVP

| Domaine | Ce que tu dois savoir faire | Où t'entraîner |
|---------|----------------------------|----------------|
| **Linux** | SSH, `cd`, `ls`, éditer un fichier, `systemctl`, `docker compose` | [linuxjourney.com](https://linuxjourney.com/) |
| **Réseau** | IP, masque, port, ping, nc, VPN | Docs équipe + Network+ (résumé) |
| **Docker** | `docker compose up -d`, `docker compose ps`, logs | `soc/README.md` |
| **Git** | clone, add, commit, push (sans secrets) | [gitimmersion.com](http://gitimmersion.com) |
| **Wazuh** | UI Agents, Alerts, Dashboard | Runbook + [doc Wazuh](https://documentation.wazuh.com/) |
| **Sécurité** | Comprendre logs, alertes, simulation d'attaque **en lab** | Runbook scénarios 4.4–4.6 |

### Ce que tu n'as pas besoin de maîtriser pour le MVP

- Python avancé
- Cloud AWS/GCP/Azure
- ELK stack complet (Wazuh intègre déjà l'indexation)
- Exploitation offensive avancée (Metasploit, etc.)
- Ansible, Kubernetes

### Plan 90DaysOfCyberSecurity — ce qui t'intéresse

Repo : [farhanashrafdev/90DaysOfCyberSecurity](https://github.com/farhanashrafdev/90DaysOfCyberSecurity)

| Jours | Sujet | Utilité pour ton projet |
|-------|-------|-------------------------|
| 1–7 | Network+ | Comprendre IP, ports, VPN |
| 8–14 | Security+ | Logs, détection, bonnes pratiques |
| 15–28 | Linux | **Essentiel** — commandes sur les VMs |
| 57–63 | Git | **Essentiel** — livrables sur GitHub |
| 43–56 | Traffic Analysis | Optionnel — comprendre nmap / Wireshark |
| 85–90 | Hacking (HTB) | Optionnel — culture Red Team |
| 29–42 Python, 64–70 ELK, 71–77 Cloud | | **Pas prioritaire** pour le MVP |

---

## 6. Accès à l'infrastructure

### Méthode officielle (équipe) — via VPN

1. Installer **OpenVPN Connect** : [openvpn.net/client](https://openvpn.net/client/)
2. Importer ton profil `.ovpn` (user `m.zaid`) — reçu sur Discord
3. Se connecter au VPN
4. Vérifier :

```bash
ping -c 3 192.168.20.254
```

5. Ouvrir Proxmox :

```
https://192.168.20.254:8006
```

6. Login :
   - `m.zaid@pve` (compte projet)
   - ou `root@pam` (admin complet)

Mot de passe : Passbolt ou MP Discord (jamais dans Git).

### Comptes Proxmox (équipe)

| Utilisateur | Royaume | Usage |
|-------------|---------|-------|
| `root` | `pam` | Admin système OVH |
| `m.zaid` | `pve` | **Ton compte projet** |
| `j.evaldo` | `pve` | Jacques |
| `v.tassart` | `pve` | Victor |

### Accès IP publique (cas exceptionnel)

```
https://51.77.52.56:8006
ssh root@51.77.52.56
```

Fonctionne seulement si ton IP est autorisée dans **firewall OVH** et **iptables hôte**. L'équipe a configuré l'accès standard via VPN.

### Serveur OVH — fiche rapide

| Élément | Valeur |
|---------|--------|
| Nom | `ns3138292.ip-51-77-52.eu` |
| IP publique | `51.77.52.56` |
| OS | Proxmox VE 9.1.9 |
| RAM | 32 Go |
| Compte OVH | Marwane Zaid (`ul21787-ovh`) |

---

## 7. La stack SOC expliquée

### Fichier principal

`soc/docker-compose.yml` — définit 4 conteneurs :

| Conteneur | Image | Rôle | Port exposé |
|-----------|-------|------|-------------|
| `wazuh-indexer` | `wazuh/wazuh-indexer:4.9.0` | Stockage et recherche des événements | Interne |
| `wazuh-manager` | `wazuh/wazuh-manager:4.9.0` | Collecte, règles, corrélation | `1514`, `1515`, `55000` |
| `wazuh-dashboard` | `wazuh/wazuh-dashboard:4.9.0` | Interface web SIEM | `443` → UI Wazuh |
| `grafana` | `grafana/grafana:latest` | Dashboards graphiques | `3000` |

### Variables d'environnement (`.env`)

Copier `soc/.env.example` → `soc/.env` (sur le serveur, **jamais dans Git) :

| Variable | Usage |
|----------|-------|
| `WAZUH_VERSION` | Version des images Wazuh |
| `WAZUH_INDEXER_PASSWORD` | Mot de passe indexeur / admin dashboard |
| `WAZUH_API_PASSWORD` | Mot de passe API Wazuh |
| `GF_ADMIN_USER` / `GF_ADMIN_PASSWORD` | Login Grafana |

### Agent Wazuh — comment ça marche

1. Tu installes l'agent sur une VM (Linux ou Windows)
2. L'agent lit les logs locaux (`/var/log/auth.log`, Event Viewer Windows, etc.)
3. Il envoie les événements au **Manager** (IP de `docker-soc01`, port `1514`)
4. Le Manager applique des **règles** → génère des **alertes**
5. Les alertes sont visibles dans le **Dashboard**

### Exemple concret de chaîne complète

```
1. Attaquant (lab) : ssh fakeuser@192.168.20.50 (×8 échecs)
2. VM cible : /var/log/auth.log enregistre "Failed password"
3. Agent Wazuh sur la VM : lit auth.log → envoie au Manager
4. Wazuh Manager : règle "SSH brute force" match
5. Wazuh Dashboard : alerte visible dans Alerts
6. Toi : capture d'écran + ligne dans soc-mvp-preuves.md
```

---

## 8. Ports, protocoles et flux réseau

### Ports à connaître

| Port | Protocole | Service | Direction |
|------|-----------|---------|-----------|
| 22 | TCP | SSH | Admin → serveurs |
| 443 | TCP | Wazuh Dashboard (HTTPS) | Navigateur → docker-soc01 |
| 3000 | TCP | Grafana | Navigateur → docker-soc01 |
| 8006 | TCP | Proxmox UI | Navigateur → Proxmox |
| 1514 | UDP | Agent Wazuh → Manager | VMs → docker-soc01 |
| 1515 | TCP | Enrôlement agent Wazuh | VMs → docker-soc01 |
| 55000 | TCP | API Wazuh | Interne / admin |
| 1194 | UDP | OpenVPN | Client → pfSense |

### Flux à demander à l'équipe réseau (pfSense)

L'étudiant 2 doit autoriser depuis le LAN/SOC vers `docker-soc01` :

- **1514/udp** — logs agents
- **1515/tcp** — enrôlement
- **443/tcp** — dashboard (si accès depuis postes admin)

Documenter dans le rapport qui a ouvert quoi.

---

## 9. Procédure MVP — étape par étape

### Phase 0 — Prérequis (sans serveur)

- [ ] Lire ce guide
- [ ] Lire [04-mvp-soc-runbook-unifie.md](04-mvp-soc-runbook-unifie.md)
- [ ] Préparer le dossier captures : `docs/livrables/screenshots/04-soc/`
- [ ] Préparer le tableau : `docs/livrables/soc-mvp-preuves.md`
- [ ] Récupérer profil VPN `.ovpn` + mots de passe (Discord / Passbolt)

### Phase 1 — Accès

- [ ] Connecter OpenVPN (`m.zaid`)
- [ ] `ping 192.168.20.254` OK
- [ ] Ouvrir `https://192.168.20.254:8006` → login OK
- [ ] Repérer VM `docker-soc01` dans Proxmox

### Phase 2 — Déploiement stack

```bash
# SSH sur docker-soc01 (remplacer IP)
ssh nexa@IP_DOCKER_SOC

# Cloner ou copier le repo si nécessaire
cd ~/Projet/soc   # adapter le chemin

cp .env.example .env
nano .env         # mots de passe forts

docker compose up -d
docker compose ps
```

**Validation :** 4 conteneurs `Up`  
**Capture :** `04-soc_docker-ps-up.png`

### Phase 3 — UI Wazuh

- Navigateur : `https://IP_SOC`
- Login : `admin` + mot de passe indexeur (`.env`)
- **Capture :** `04-soc_wazuh-dashboard.png`

### Phase 4 — Agents (minimum 3)

| # | Machine | Type | Comment |
|---|---------|------|---------|
| 1 | `docker-soc01` | Linux | Agent local sur le manager SOC |
| 2 | `ad-dc01` | Windows | Agent AD — remonte Event 4625 |
| 3 | 1 VM Linux | Linux | ex. client ou serveur Debian |

Wazuh UI → **Agents** → vérifier statut **Active**  
**Capture :** `04-soc_wazuh-agents-actifs.png`

### Phase 5 — Dashboard

- Option A : dashboard Wazuh natif (recommandé MVP)
- Option B : Grafana `http://IP_SOC:3000`

**Capture :** `04-soc_grafana-dashboard.png`

### Phase 6 — 3 alertes + preuves

Voir section 10 ci-dessous.

### Phase 7 — Clôture

- [ ] Remplir `soc-mvp-preuves.md`
- [ ] Toutes les captures dans `04-soc/`
- [ ] Cocher `docs/taches/04-soc.md`

---

## 10. Les 3 scénarios d'alerte (détail + exemples)

### Scénario 1 — Brute force SSH

**Objectif pédagogique :** montrer que le SOC détecte des tentatives de connexion SSH répétées.

**Prérequis :** VM cible avec SSH actif + agent Wazuh `Active`.

**Commande (depuis une VM de test du lab, pas depuis Internet) :**

```bash
for i in {1..8}; do
  ssh -o StrictHostKeyChecking=no fakeuser@IP_CIBLE 'exit' || true
done
```

**Où vérifier :** Wazuh → **Security Events** ou **Alerts** → filtrer par agent / règle SSH.

**Exemple de log attendu :** `Failed password for invalid user fakeuser from X.X.X.X port XXXXX ssh2`

**Capture :** `04-soc_wazuh-alerte-ssh-bruteforce.png`

---

### Scénario 2 — Échec logon Active Directory (Event 4625)

**Objectif pédagogique :** montrer que les événements Windows AD remontent au SIEM.

**Prérequis :** Agent Wazuh sur `ad-dc01` + audit logon activé (GPO équipe).

**Action :** depuis un poste joint au domaine `nexamind.local`, tenter plusieurs connexions avec un mauvais mot de passe.

**Event Windows clé :**

| Event ID | Signification |
|----------|---------------|
| 4625 | Échec de connexion (bad password, user inconnu) |
| 4624 | Connexion réussie (ne pas confondre) |

**Où vérifier :** Wazuh → Alerts → filtrer `4625` ou "logon failure".

**Capture :** `04-soc_wazuh-alerte-ad-failed-logon.png`

---

### Scénario 3 — Scan de ports (nmap)

**Objectif pédagogique :** détecter une reconnaissance réseau (phase pré-attaque).

**Prérequis :** VM `lab-rt01` (Red Team) avec accès réseau vers une cible lab.

**Commande :**

```bash
nmap -sS IP_CIBLE_LAB
```

**Exemple :**

```bash
# Depuis lab-rt01 vers une VM Linux du LAN
nmap -sS 192.168.20.50
```

**Où vérifier :** Wazuh → Alerts → règle scan / suspicious network activity.

**Capture :** `04-soc_wazuh-alerte-port-scan.png`

---

## 11. Captures d'écran et livrables

### Dossier de dépôt

`docs/livrables/screenshots/04-soc/`

### Liste complète des captures MVP

| # | Fichier | Quand | Quoi montrer |
|---|---------|-------|--------------|
| 4.1 | `04-soc_docker-ps-up.png` | Après `docker compose ps` | 4 conteneurs Up |
| 4.2 | `04-soc_wazuh-dashboard.png` | UI Wazuh ouverte | Login ou dashboard |
| 4.3 | `04-soc_wazuh-agents-actifs.png` | ≥3 agents | Statut Active (vert) |
| 4.4 | `04-soc_wazuh-alerte-ssh-bruteforce.png` | Après test SSH | Alerte brute force |
| 4.5 | `04-soc_wazuh-alerte-ad-failed-logon.png` | Après test AD | Alerte 4625 / failed logon |
| 4.6 | `04-soc_wazuh-alerte-port-scan.png` | Après nmap | Alerte scan |
| 4.7 | `04-soc_grafana-dashboard.png` | Dashboard prêt | Agents / alertes visibles |
| 4.8 | `04-soc_mvp-tableau-preuves.png` | Fin MVP | Tableau rempli |

### Raccourcis Mac

| Action | Touche |
|--------|--------|
| Écran entier | `Cmd + Shift + 3` |
| Zone | `Cmd + Shift + 4` |
| Fenêtre | `Cmd + Shift + 4` → `Espace` → clic |

### Interdit sur les captures

- Mots de passe (champs ou terminal)
- Clés SSH privées
- Contenu de `.env`
- Tokens API / profils `.ovpn` complets

---

## 12. Critères de validation (Go / No-Go)

### Go — MVP validé ✅

- [ ] Stack Docker `Up` (4 services)
- [ ] ≥ 3 agents `Active`
- [ ] 1 dashboard exploitable
- [ ] 3 alertes **différentes** avec heure + rule ID notés
- [ ] 8 captures nommées correctement
- [ ] `soc-mvp-preuves.md` rempli
- [ ] Aucun secret committé sur GitHub

### No-Go — à corriger ❌

- Agents en `Disconnected` → vérifier firewall 1514/1515
- Pas d'alerte après test → vérifier agent sur la bonne machine, règles Wazuh
- Dashboard vide → indexer pas prêt, attendre 2–5 min après deploy
- Timeout Proxmox → VPN non connecté ou routes OpenVPN incorrectes

---

## 13. Ressources d'apprentissage (filtrées pour ton projet)

### Docs projet (priorité 1)

| Ressource | Chemin |
|-----------|--------|
| Runbook opérationnel | [04-mvp-soc-runbook-unifie.md](04-mvp-soc-runbook-unifie.md) |
| Captures détaillées | [screenshots-par-etape.md](screenshots-par-etape.md) § Leçon 4 |
| Architecture SOC | [../architecture/architecture-soc.md](../architecture/architecture-soc.md) |
| Tâches SOC | [../taches/04-soc.md](../taches/04-soc.md) |
| Repo équipe (accès VPN) | [Projet-Pro_4esgi](https://github.com/Abdoulmyges/Projet-Pro_4esgi) |

### Docs officielles (priorité 2)

| Sujet | Lien |
|-------|------|
| Wazuh Docker | [documentation.wazuh.com — Docker](https://documentation.wazuh.com/current/deployment-options/docker/) |
| Agent Linux | [Agent Linux](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html) |
| Agent Windows | [Agent Windows](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html) |
| Proxmox | [pve.proxmox.com/pve-docs](https://pve.proxmox.com/pve-docs/) |
| Grafana | [grafana.com/docs](https://grafana.com/docs/grafana/latest/) |

### Formation générale (priorité 3 — si tu manques de bases)

| Sujet | Ressource |
|-------|-----------|
| Linux | [linuxjourney.com](https://linuxjourney.com/) |
| Git | [gitimmersion.com](http://gitimmersion.com) |
| Réseau (bases) | Professor Messer Network+ (YouTube) — chapitres IP/subnetting/ports |
| Sécurité (bases) | Professor Messer Security+ — chapitres logs, SIEM, incident response |
| Plan 90 jours (filtré) | [90DaysOfCyberSecurity](https://github.com/farhanashrafdev/90DaysOfCyberSecurity) — jours 1–28, 57–63, 43–56 optionnel |

---

## 14. Coordination avec l'équipe

### Ce dont tu as besoin des autres

| De qui | Quoi | Pourquoi |
|--------|------|----------|
| Abdoul / Jacques | Profil `.ovpn` + mdp VPN | Accéder au lab |
| Jacques | Compte `m.zaid@pve` + mdp | Proxmox |
| Étudiant 1 | VM `docker-soc01` running, 8 Go RAM | Héberger Wazuh |
| Étudiant 2 | Flux 1514/1515 ouverts sur pfSense | Agents joignables |
| Étudiant 2 | Agent Wazuh sur `ad-dc01` | Alerte AD |
| Étudiant 4 | Accès `lab-rt01` pour nmap | Alerte scan |

### Message type pour l'équipe

> « SOC prêt côté docs et compose. J'ai besoin de : (1) VPN actif, (2) VM docker-soc01 up, (3) ports 1514/1515 ouverts vers IP_SOC, (4) agent sur ad-dc01. Je déploie dès que c'est OK. »

---

## 15. Dépannage fréquent

| Symptôme | Cause probable | Action |
|----------|----------------|--------|
| Timeout `51.77.52.56:8006` | Accès public bloqué par iptables | Utiliser VPN → `192.168.20.254:8006` |
| VPN connecté mais ping LAN fail | Routes OpenVPN non poussées | pfSense : IPv4 Local Network = `192.168.20.0/24` |
| Agent `Disconnected` | Firewall bloque 1514/1515 | Ouvrir ports sur pfSense vers IP_SOC |
| `docker compose` fail mémoire | RAM insuffisante | VM ≥ 8 Go RAM, vérifier `free -h` |
| Pas d'alerte après test | Agent pas sur la bonne VM | Vérifier agent sur **cible**, pas seulement sur SOC |
| Dashboard Wazuh 502 | Indexer pas prêt | Attendre 2–5 min, `docker compose logs wazuh-indexer` |
| Certificat HTTPS refusé | Normal (auto-signé) | Accepter exception navigateur |

---

## 16. Sécurité et bonnes pratiques

1. **Ne jamais** committer `.env`, mots de passe, clés privées, `.ovpn`
2. Simuler les attaques **uniquement** dans le lab (VMs internes)
3. Ne pas scanner / attaquer l'IP publique OVH ni des systèmes hors projet
4. Restreindre l'accès Wazuh/Grafana au LAN/VPN (pas exposer sur Internet)
5. Mots de passe forts uniques dans `.env`
6. Credentials équipe via **Passbolt** ou MP Discord — pas dans Git

---

## 17. FAQ

**Q : Je dois faire tout le plan 90DaysOfCyberSecurity ?**  
R : Non. Linux + Git + bases réseau/sécu suffisent. Le reste est bonus.

**Q : Pourquoi je n'accède pas à Proxmox en IP publique ?**  
R : L'équipe a configuré l'accès via VPN. C'est normal.

**Q : C'est quoi IP_SOC ?**  
R : L'IP de la VM `docker-soc01` sur le réseau interne. Trouve-la avec `hostname -I` en SSH.

**Q : Wazuh ou ELK ?**  
R : Wazuh pour le MVP. ELK est un autre stack SIEM (phase avancée).

**Q : Je peux déployer TheHive maintenant ?**  
R : Non. Valide d'abord le MVP (Wazuh + 3 agents + 3 alertes).

**Q : Qui installe l'agent sur AD ?**  
R : Toi ou l'étudiant AD — mais **tu** valides qu'il remonte dans Wazuh.

**Q : Que mettre dans le rapport ?**  
R : Schéma SOC, captures, tableau preuves, explication des 3 scénarios, limites du MVP.

---

## 18. Annexes — chemins du dépôt

```
Projet/
├── soc/
│   ├── docker-compose.yml      # Stack Wazuh + Grafana
│   ├── .env.example            # Modèle variables (copier → .env)
│   └── README.md               # Installation rapide
├── docs/
│   ├── wiki/
│   │   ├── README-SOC-GUIDE-COMPLET.md   # ← CE FICHIER
│   │   ├── 04-mvp-soc-runbook-unifie.md  # Runbook actions
│   │   └── screenshots-par-etape.md      # Guide captures
│   ├── livrables/
│   │   ├── soc-mvp-preuves.md            # Tableau preuves
│   │   └── screenshots/04-soc/           # Tes PNG
│   ├── architecture/
│   │   ├── architecture-soc.md
│   │   └── inventaire-vms.md
│   └── taches/
│       └── 04-soc.md                     # Checklist tâches
```

### Repo équipe (accès, VPN, infra)

[https://github.com/Abdoulmyges/Projet-Pro_4esgi](https://github.com/Abdoulmyges/Projet-Pro_4esgi)

Fichiers clés :
- `4-projet-annuel/ACCES/Accès et identifiants.md`
- `4-projet-annuel/Tutorials/Guide de connexion VPN.md`
- `4-projet-annuel/Infra/Réservation Adresse IP.md`

---

*Document maintenu par l'équipe SOC — projet 4eSGI / NexaMind. Dernière mise à jour : juin 2026.*
