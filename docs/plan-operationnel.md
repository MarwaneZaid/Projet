# Rapport de Projet — Mise en Route & Plan Opérationnel

## Introduction

Ce projet démontre la mise en place d’une infrastructure complète de **virtualisation** et de **cybersécurité** sur un serveur limité en ressources : mini-cloud, SOC, Active Directory, simulations d’attaque automatisées, avec livrables professionnels.

## 1. Contexte

Équipe de **4 étudiants** :

- 2 spécialisés **sécurité informatique** (dont Abdoul Hamani Bachir Seydou)
- 2 spécialisés **systèmes et réseaux**

**Challenge** : inversion des rôles — les profils réseau pilotent le SOC / Red Team ; les profils cyber pilotent l’infra / réseau. Travail en binômes avec validation collective à chaque étape.

## 2. Objectif global

| Composant | Technologies cibles |
|-----------|---------------------|
| Mini-cloud | Proxmox VE |
| Annuaire | Active Directory (Samba AD ou Windows) |
| SOC | Wazuh, Suricata, TheHive, Cortex, Grafana |
| Red Team | CALDERA, BloodHound, OpenVAS |
| Réseau | pfSense, VPN site-to-site, DMZ, reverse proxy |
| Extension | Portail client + admin (Audit de Sécurité) |

**Finalité** : présenter une solution type entreprise IT (doc technique, démo, pitch).

## 3. Organisation temporelle

Voir [CHECKLIST.md](../CHECKLIST.md) pour les critères de validation.

- **Oct. – Nov.** : cadrage et plan
- **Déc. – Jan.** : infra (Proxmox, pfSense, AD, Docker host)
- **Fév. – Mars** : SOC + Red Team (Docker)
- **Avr. – Mai** : Ansible, sauvegardes
- **Juin** : tests intégrés
- **Juil.** : rapport, wiki, présentation

## 4. Répartition des rôles

### Étudiant 1 — Infrastructure & virtualisation

- Proxmox VE, stockage, snapshots
- VM : pfSense, AD, Linux
- Topologie LAN / DMZ

### Étudiant 2 — Réseau & services Windows

- pfSense : NAT, DHCP, firewall, VPN
- AD : users, groupes, OU, GPO
- Logs sécurité pour le SOC

### Étudiant 3 — SOC & automatisation

- Stack SOC Docker
- Pipelines CI/CD conteneurs (si applicable)
- n8n : alertes → tickets / emails
- Playbooks d’incident, dashboards

### Étudiant 4 — Red Team & portail

- CALDERA, BloodHound, OpenVAS
- Scénarios simulés (lab uniquement)
- Site client + admin
- Intégration résultats SOC / Red Team

## 5. Extension — Audit de sécurité

**Espace client** : auth, commandes, devis, suivi, messagerie.

**Espace admin** : dashboard, devis/projets, lien vers outils SOC / Red Team.

## 6. Livrables

1. Rapport technique (~10 pages) → `docs/livrables/rapport/`
2. WikiJS → procédures dans `docs/wiki/`
3. Schémas réseau & SOC → `docs/architecture/`
4. Pitch final
5. Site web (extension)

## 7. Conclusion projet

Objectifs pédagogiques : compétences croisées, infra réaliste à budget limité, scénarios attaque/défense, livrables pro, travail d’équipe validé collectivement.
