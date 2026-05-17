# Cartes Trello — copier-coller par liste

## 📌 Équipe & règles

| Carte | Labels | Échéance |
|-------|--------|----------|
| Lire README GitHub + cloner le dépôt | | 20/10/2025 |
| Compléter TEAM.md (4 noms, contacts, binômes) | Livrable | 15/11/2025 |
| Définir jour/heure réunion hebdo + canal Discord/Teams | | 15/11/2025 |
| Règles : pas de secrets dans Git, lab RT isolé | Bloquant | 15/11/2025 |
| Inviter les 3 coéquipiers sur GitHub (collaborators) | | 20/11/2025 |

---

## Phase 0 — Cadrage (Oct–Nov)

| Carte | Labels | Échéance |
|-------|--------|----------|
| Réunion kickoff — valider périmètre projet | Livrable | 31/10/2025 |
| Valider plan opérationnel (docs/plan-operationnel.md) | Livrable | 15/11/2025 |
| Remplir specs matériel serveur | E1-Infra | 20/11/2025 |
| Décision : Samba AD **ou** Windows Server | E2-Réseau | 25/11/2025 |
| Plan IP : LAN / DMZ / SOC / LAB-RT | E1-Infra, E2-Réseau | 25/11/2025 |
| Schéma réseau v0 (draw.io + topologie-reseau.md) | E1-Infra | 30/11/2025 |
| Configurer labels + listes Trello | | 30/11/2025 |
| ✅ Validation collective — Phase 0 | Livrable | 30/11/2025 |

---

## Phase 1 — Infrastructure (Déc–Jan)

| Carte | Labels | Échéance |
|-------|--------|----------|
| Installer Proxmox VE sur bare metal | E1-Infra | 15/12/2025 |
| Configurer stockage (ZFS/LVM) + politique snapshots | E1-Infra | 20/12/2025 |
| Créer vmbr0 (LAN) et vmbr1 (DMZ) | E1-Infra | 22/12/2025 |
| Template cloud-init Debian/Ubuntu | E1-Infra | 05/01/2026 |
| VM pfSense — installation | E2-Réseau | 10/01/2026 |
| pfSense : NAT sortant + DHCP + réservations | E2-Réseau | 12/01/2026 |
| pfSense : règles firewall LAN/DMZ (deny by default) | E2-Réseau | 15/01/2026 |
| Tester isolation segments (ping + blocage) | E2-Réseau | 18/01/2026 |
| VM contrôleur AD (Samba ou Windows) | E2-Réseau | 20/01/2026 |
| AD : OU, groupes, utilisateurs de test | E2-Réseau | 22/01/2026 |
| AD : GPO audit connexions + politique MDP | E2-Réseau | 24/01/2026 |
| Joindre 2 postes clients au domaine | E2-Réseau | 26/01/2026 |
| Activer / forward logs sécurité AD | E2-Réseau, E3-SOC | 28/01/2026 |
| VM Linux hôte Docker (réseau SOC) | E1-Infra | 28/01/2026 |
| Rédiger inventaire VMs (IP, rôle, ressources) | E1-Infra, Livrable | 30/01/2026 |
| Export backup config pfSense (procédure) | E2-Réseau | 31/01/2026 |
| ✅ Validation collective — Phase 1 | Livrable | 31/01/2026 |

---

## Phase 2 — SOC & Red Team (Fév–Mars)

| Carte | Labels | Échéance |
|-------|--------|----------|
| Copier soc/.env.example → .env (mots de passe forts) | E3-SOC | 10/02/2026 |
| Déployer stack SOC (Wazuh + Grafana) docker compose | E3-SOC | 15/02/2026 |
| Ouvrir ports pfSense → agents Wazuh (1514/1515) | E2-Réseau, E3-SOC | 15/02/2026 |
| Agent Wazuh sur contrôleur AD | E3-SOC | 20/02/2026 |
| Agent Wazuh sur hôte Docker + 1 VM lab | E3-SOC | 22/02/2026 |
| Syslog pfSense → Wazuh | E2-Réseau, E3-SOC | 25/02/2026 |
| Déployer Suricata + règles de base | E3-SOC | 28/02/2026 |
| Documenter SPAN / miroir trafic | E3-SOC | 28/02/2026 |
| Grafana : dashboard alertes / agents | E3-SOC | 05/03/2026 |
| TheHive + Cortex : incident fictif bout en bout | E3-SOC | 10/03/2026 |
| n8n : alerte Wazuh → email ou ticket | E3-SOC | 15/03/2026 |
| Segment LAB-RT isolé (sans route vers LAN) | E4-RedTeam, Bloquant | 10/03/2026 |
| Déployer OpenVAS — scan cible lab uniquement | E4-RedTeam | 15/03/2026 |
| BloodHound : collecte SharpHound sur lab AD | E4-RedTeam | 20/03/2026 |
| CALDERA : déploiement + agent lab | E4-RedTeam | 22/03/2026 |
| Scénario 1 : brute force honeypot (rapport) | E4-RedTeam, Livrable | 25/03/2026 |
| Scénario 2 : énumération AD (rapport) | E4-RedTeam, Livrable | 28/03/2026 |
| Vérifier corrélation alerte SOC ↔ scénario RT | E3-SOC, E4-RedTeam | 30/03/2026 |
| ✅ Validation collective — Phase 2 | Livrable | 31/03/2026 |

---

## Phase 3 — Automatisation (Avr–Mai)

| Carte | Labels | Échéance |
|-------|--------|----------|
| Créer inventaire Ansible (hosts.yml) | E3-SOC | 15/04/2026 |
| Playbook : installation agent Wazuh | E3-SOC | 20/04/2026 |
| Playbook : déploiement hôte Docker SOC | E3-SOC | 25/04/2026 |
| Test restore snapshot Proxmox (VM test) | E1-Infra | 30/04/2026 |
| Procédure sauvegarde pfSense + test restore | E2-Réseau | 05/05/2026 |
| VPN site-to-site pfSense (ou doc si matériel manquant) | E2-Réseau | 15/05/2026 |
| Reverse proxy DMZ (Nginx/Traefik) | E2-Réseau | 20/05/2026 |
| Certificats TLS lab (CA interne ou Let's Encrypt) | E2-Réseau | 22/05/2026 |
| Durcissement SSH hôte Docker | E1-Infra | 25/05/2026 |
| ✅ Validation collective — Phase 3 | Livrable | 31/05/2026 |

---

## Phase 4 — Tests & Livrables (Juin–Juil)

| Carte | Labels | Échéance |
|-------|--------|----------|
| Exercice SOC : détection + réponse (scénario documenté) | E3-SOC, Livrable | 15/06/2026 |
| Exercice Red Team + rapport corrélation logs | E4-RedTeam, Livrable | 20/06/2026 |
| Rapport technique (~10 pages) | Livrable | 30/06/2026 |
| WikiJS : doc interne + procédures | Livrable | 05/07/2026 |
| Schémas réseau + architecture SOC (PNG/draw.io) | Livrable | 05/07/2026 |
| Pitch « entreprise IT » (slides 10–15 min) | Livrable | 10/07/2026 |
| Répétition démo orale (toute l’équipe) | Livrable | 12/07/2026 |
| Présentation finale + Q&A | Livrable | 15/07/2026 |
| ✅ Validation collective — Phase 4 | Livrable | 15/07/2026 |

---

## 🌐 Extension — Portail Audit (optionnel)

| Carte | Labels | Échéance |
|-------|--------|----------|
| Maquettes wireframes client + admin | E4-RedTeam, Optionnel | 30/04/2026 |
| Schéma BDD PostgreSQL | E4-RedTeam, Optionnel | 05/05/2026 |
| MVP authentification client | E4-RedTeam, Optionnel | 20/05/2026 |
| Parcours commande / demande d’audit | E4-RedTeam, Optionnel | 31/05/2026 |
| Dashboard admin + gestion devis | E4-RedTeam, Optionnel | 15/06/2026 |
| Lien rapport Wazuh/OpenVAS dans portail | E3-SOC, E4-RedTeam, Optionnel | 30/06/2026 |
