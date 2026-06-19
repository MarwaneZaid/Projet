# Configuration OVH + Proxmox — plan d’action

Serveur : `ns3138292.ip-51-77-52.eu` — IP **51.77.52.56** — Proxmox 9 déjà installé.

---

## Phase A — Sécurité OVH (P0)

**Guide détaillé :** [01-firewall-ovh.md](01-firewall-ovh.md)

| # | Action | Où | Statut |
|---|--------|-----|--------|
| A1 | Firewall réseau OVH : autoriser **22/tcp** (SSH) uniquement depuis IP équipe/école | Manager → IP → Firewall | [ ] **bloquant** |
| A2 | Autoriser **8006/tcp** (Proxmox) uniquement depuis IP admin | Idem | [ ] **bloquant** |
| A3 | Bloquer le reste en entrée sur IPv4 publique | Idem | [ ] |
| A4 | Activer **monitoring OVH** sur le serveur (optionnel mais utile) | Fiche serveur → Service status | [ ] |
| A5 | Clés SSH pour les 4 membres (pas mot de passe root partagé) | `~/.ssh/authorized_keys` | [ ] |

---

## Phase B — Proxmox (P1) — déjà installé

| # | Action | Statut |
|---|--------|--------|
| B1 | Connexion UI `https://51.77.52.56:8006` | [ ] |
| B2 | Changer mot de passe root si mot de passe OVH par défaut | [ ] |
| B3 | `apt update && apt full-upgrade` sur l’hôte | [ ] |
| B4 | Vérifier stockage Soft RAID (~4 To) dans Datacenter → Disks | [ ] |
| B5 | Créer `vmbr0` bridge pour VMs (si pas déjà fait) | [ ] |
| B6 | Politique snapshots avant chaque VM | [ ] |
| B7 | Créer VMs : pfSense, ad-dc01, docker-soc01 (voir inventaire-vms.md) | [ ] |

---

## Phase C — Réseau projet (P1)

Plages IP internes (VMs) — à utiliser derrière pfSense :

| Segment | Plage | Usage |
|---------|-------|--------|
| LAN | 192.168.10.0/24 | AD, admin |
| DMZ | 192.168.20.0/24 | Reverse proxy |
| SOC | 192.168.30.0/24 | Docker SOC |
| LAB-RT | 192.168.99.0/24 | Red Team **isolé** |

| # | Action | Statut |
|---|--------|--------|
| C1 | VM pfSense : WAN = bridge vers IP publique ou route OVH | [ ] |
| C2 | pfSense LAN = 192.168.10.1 | [ ] |
| C3 | Documenter dans topologie-reseau.md | [ ] |
| C4 | vRack `pn-1303451` : utiliser seulement si besoin réseau étendu (optionnel) | [ ] |

---

## Phase D — Suite projet

Enchaîner les guides :

1. [docs/taches/02-reseau-pfsense.md](../taches/02-reseau-pfsense.md)
2. [docs/taches/03-active-directory.md](../taches/03-active-directory.md)
3. [docs/taches/04-soc.md](../taches/04-soc.md)

---

## Ce qu’on ne fait pas sur le réseau OVH

- Pas de scan OpenVAS vers Internet ou IP OVH voisins
- Pas d’ouverture large `0.0.0.0/0` sur Proxmox ou SSH
- Red Team uniquement sur VMs lab internes
