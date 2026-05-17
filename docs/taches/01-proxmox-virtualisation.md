# 01 — Proxmox & virtualisation

**Responsable :** Étudiant 1 (profil cyber → rôle infra)  
**Relecteur :** Étudiant 2  
**Priorité globale :** P1  
**Dépôt :** [infra/proxmox/](../../infra/proxmox/), [infra/README.md](../../infra/README.md)

**Prérequis :** [00-cadrage-equipe.md](00-cadrage-equipe.md) validé (P0)

> **OVH :** Proxmox VE 9 est **déjà installé** sur `51.77.52.56` — voir [serveur-ovh-fiche.md](../infra/serveur-ovh-fiche.md).

---

## P0 — Bloquant

| # | Tâche exacte | Comment faire | Validé |
|---|--------------|---------------|--------|
| 1.1 | ~~Installer Proxmox~~ — **déjà fait** sur OVH | — | [x] |
| 1.2 | Accéder à l’UI `https://51.77.52.56:8006` | Certificat accepté, login root OK | [ ] |
| 1.3 | Mettre à jour l’hôte : `apt update && apt full-upgrade` | Pas d’erreur apt | [ ] |

---

## P1 — Critique (cœur infra)

| # | Tâche exacte | Comment faire | Validé |
|---|--------------|---------------|--------|
| 1.4 | Configurer stockage : LVM-thin ou ZFS (selon disques) | Voir checklist install | [ ] |
| 1.5 | Créer `vmbr0` (LAN / management) | Bridge sur NIC principale | [ ] |
| 1.6 | Créer `vmbr1` (DMZ) si 2e NIC ou VLAN documenté | Sinon noter limitation dans specs | [ ] |
| 1.7 | Activer politique **snapshots** avant chaque changement majeur | Doc procédure 1 paragraphe | [ ] |
| 1.8 | Créer template cloud-init (Debian 12 ou Ubuntu 22.04) | Template réutilisable pour VMs | [ ] |
| 1.9 | Créer VM **fw-pfsense** (ressources : 1 vCPU, 1 Go RAM min.) | VM créée, démarrable | [ ] |
| 1.10 | Créer VM **ad-dc01** (2–4 Go RAM selon choix AD) | VM créée | [ ] |
| 1.11 | Créer VM **docker-soc01** (4–8 Go RAM) | VM créée, sur segment SOC | [ ] |
| 1.12 | Rédiger **inventaire VMs** : nom, ID, IP, vCPU, RAM, rôle | `docs/architecture/inventaire-vms.md` (à créer) | [ ] |

---

## P2 — Important

| # | Tâche exacte | Comment faire | Validé |
|---|--------------|---------------|--------|
| 1.13 | Configurer sauvegarde Proxmox (backup job vers 2e disque ou NFS si dispo) | Job testé 1 fois | [ ] |
| 1.14 | Restreindre accès UI Proxmox au LAN admin uniquement | Firewall hôte ou pfSense | [ ] |
| 1.15 | VM optionnelle **lab-rt01** pour Red Team (segment isolé) | Pas de carte réseau vers LAN prod | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 1.16 | Test restore d’un snapshot sur VM jetable | [ ] |
| 1.17 | Export procédure « ajouter une VM » dans `docs/wiki/` | [ ] |

---

## Critères « Proxmox validé »

- [ ] Au moins 3 VMs créées (pfSense, AD, Docker)  
- [ ] Snapshots fonctionnels  
- [ ] Inventaire VMs à jour  
- [ ] Relecture Étudiant 2 OK  

**Ensuite :** [02-reseau-pfsense.md](02-reseau-pfsense.md) en parallèle partiel, puis [03-active-directory.md](03-active-directory.md)
