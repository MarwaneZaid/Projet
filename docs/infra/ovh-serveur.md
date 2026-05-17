# Serveur OVH — démarrage projet

**Manager :** [manager.eu.ovhcloud.com](https://manager.eu.ovhcloud.com/#/hub/)  
**API (scripts) :** [ovh-api.md](ovh-api.md) — `GET /me`, `/dedicated/server`, `/vps`

Ce serveur est votre **hôte unique** pour Proxmox et toutes les VMs du projet.

---

## Étape 1 — Identifier le type de serveur (P0)

Dans le manager OVH, ouvrez le service et notez :

| Question | Où regarder | Impact projet |
|----------|-------------|---------------|
| **Dedicated** ou **VPS** ou **Public Cloud** ? | Nom du produit | Dedicated = Proxmox direct OK ; VPS = limites (nested virt) |
| CPU / RAM / disque | Onglet « Informations » | Capacité VMs (voir specs-materiel.md) |
| **IP publique** | IP attachée | Accès SSH / Proxmox UI |
| **vRack** disponible ? | Option réseau | Utile pour VLAN avancés (optionnel) |

Remplir le tableau dans [specs-materiel.md](../architecture/specs-materiel.md).

---

## Étape 2 — Accès équipe (P0)

| # | Action | Détail |
|---|--------|--------|
| 1 | Créer un compte OVH par membre **ou** 1 compte partagé école | Éviter 4 personnes sur 1 mot de passe perso |
| 2 | Partager l’IP + accès SSH via **clés SSH** (pas mot de passe en Git) | `~/.ssh/ovh-projet` |
| 3 | Noter dans TEAM.md : qui a accès manager + qui peut reboot | |
| 4 | Activer **double auth** sur le compte OVH manager | |

---

## Étape 3 — Sécurité OVH (avant Proxmox)

| # | Action | Détail |
|---|--------|--------|
| 1 | **Firewall réseau OVH** (Edge Network Firewall) : autoriser seulement SSH (22) depuis IP école/maison | Pas `0.0.0.0/0` en permanence |
| 2 | Plus tard : Proxmox UI **8006** uniquement depuis IP admin connues | |
| 3 | Désactiver login root par mot de passe si possible ; clés SSH uniquement | |

> Le pfSense du projet filtrera **à l’intérieur** ; le firewall OVH protège le bare metal.

---

## Étape 4 — Installer Proxmox sur le serveur OVH (P1)

**Si serveur dédié (Dedicated)** — cas le plus simple :

1. Manager OVH → serveur → **Réinstaller** ou boot **IPMI/KVM**
2. Monter l’ISO **Proxmox VE** (télécharger sur [proxmox.com](https://www.proxmox.com/en/downloads))
3. Installer sur le disque principal (ZFS ou ext4 selon taille disque)
4. Hostname suggéré : `pve-projet.ovh` (ou nom école)
5. IP : utiliser l’**IP publique OVH** en premier (management) ; réseaux privés VMs ensuite via `vmbr`

**Si VPS OVH** — vérifier d’abord :

- La virtualisation imbriquée (KVM) est-elle autorisée ?
- Sinon : installer directement les services sur le VPS **sans** Proxmox (plan B : Docker + 1 VM AD allégée)

Documenter le choix dans TEAM.md « Décisions ».

---

## Étape 5 — Réseau sur OVH (schéma simple)

```
Internet
    │
    ▼
[Firewall OVH] ── IP publique
    │
    ▼
Proxmox (hôte)
    ├── vmbr0 : LAN virtuel 192.168.10.0/24 (AD, admin)
    ├── vmbr1 : DMZ 192.168.20.0/24
    ├── pfSense VM (WAN + LAN)
    ├── docker-soc01 (192.168.30.x)
    └── lab-rt (192.168.99.x, isolé)
```

**Important :** les scans Red Team (OpenVAS, Nmap) restent **entre VMs internes** — ne pas scanner le réseau OVH ni Internet sans autorisation.

---

## Étape 6 — Sauvegardes OVH

| Option | Usage |
|--------|--------|
| Snapshots Proxmox | Quotidien sur VMs critiques |
| Backup OVH (si option activée) | Sauvegarde disque hôte |
| Export XML pfSense | Hebdomadaire vers repo local (hors Git) |

---

## Checklist rapide OVH

- [ ] Type serveur noté (Dedicated / VPS / Cloud)
- [ ] CPU, RAM, disque dans specs-materiel.md
- [ ] IP publique + accès SSH testé par 2 membres
- [ ] Firewall OVH configuré (SSH restreint)
- [ ] Décision Proxmox direct vs plan B VPS documentée
- [ ] Proxmox installé → UI `:8006` accessible
- [ ] Première VM créée (test)

**Suite :** [docs/taches/01-proxmox-virtualisation.md](../taches/01-proxmox-virtualisation.md)
