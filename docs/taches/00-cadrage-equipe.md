# 00 — Cadrage & équipe

**Responsable :** toute l’équipe (4)  
**Priorité globale :** P0 (à terminer avant toute installation)  
**Dépôt :** [TEAM.md](../../TEAM.md), [docs/architecture/](../architecture/)

---

## P0 — Bloquant (semaine 1)

| # | Tâche exacte | Livrable | Validé |
|---|--------------|----------|--------|
| 0.1 | Compléter [TEAM.md](../../TEAM.md) : 4 noms, emails, binômes | Fichier à jour | [ ] |
| 0.2 | Choisir jour/heure **réunion hebdo** + canal (Discord/Teams) | Noté dans TEAM.md | [ ] |
| 0.3 | Lire et valider [plan-operationnel.md](../plan-operationnel.md) | 4 signatures orales + date en TEAM.md | [ ] |
| 0.4 | Renseigner [specs-materiel.md](../architecture/specs-materiel.md) + [ovh-serveur.md](../infra/ovh-serveur.md) : type OVH, CPU, RAM, IP | Tableau rempli | [ ] |
| 0.5 | **Décision écrite** : Samba AD **ou** Windows Server (RAM/licence) | Ligne dans TEAM.md « Décisions » | [ ] |
| 0.6 | Définir plages IP : LAN, DMZ, SOC, LAB-RT (Red Team isolé) | [topologie-reseau.md](../architecture/topologie-reseau.md) | [ ] |
| 0.7 | Schéma réseau v0 (draw.io ou équivalent) export PNG dans `docs/architecture/diagrams/` | Fichier PNG + lien dans markdown | [ ] |
| 0.8 | Règles d’équipe : pas de secrets dans Git ; lab RT sans route vers LAN | README + oral encadrant | [ ] |
| 0.9 | Inviter les 3 coéquipiers sur le dépôt GitHub (collaborators) | Tous ont accès push/PR | [ ] |

---

## P1 — Important (avant Proxmox)

| # | Tâche exacte | Livrable | Validé |
|---|--------------|----------|--------|
| 0.10 | Inventaire matériel : 1 serveur bare metal confirmé disponible | Photo ou fiche technique | [ ] |
| 0.11 | Liste des VMs prévues + RAM allouée par VM (ne pas dépasser la RAM totale) | Table dans specs-materiel.md | [ ] |
| 0.12 | Accord écrit école/encadrant pour simulations Red Team | Email ou PDF archivé | [ ] |

---

## Critères « phase 0 validée »

- [ ] TEAM.md complet  
- [ ] Schéma IP + PNG validés par les 4  
- [ ] Choix AD acté  
- [ ] Toute l’équipe a cloné le repo et lu `docs/taches/README.md`

**Ensuite :** passer à [01-proxmox-virtualisation.md](01-proxmox-virtualisation.md)
