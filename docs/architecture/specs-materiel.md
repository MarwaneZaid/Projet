# Spécifications matériel & contraintes

**Hébergeur :** OVHcloud — [manager.eu.ovhcloud.com](https://manager.eu.ovhcloud.com/#/hub/)  
**Fiche complète :** [docs/infra/serveur-ovh-fiche.md](../infra/serveur-ovh-fiche.md)  
**Plan config :** [docs/infra/serveur-ovh-configuration.md](../infra/serveur-ovh-configuration.md)

## Serveur hôte OVH

| Paramètre | Valeur |
|-----------|--------|
| Fournisseur | OVHcloud |
| Type de service | **Serveur dédié** (Kimsufi KS-5) |
| Nom du serveur | `ns3138292.ip-51-77-52.eu` |
| CPU | Intel Xeon-E3 1270 v6 — 4c/8t — 3,8–4,2 GHz |
| RAM totale | **32 Go** ECC |
| Stockage | 2×2 To HDD SATA — Soft RAID |
| Datacenter | waw1 (Varsovie) |
| IPv4 publique | **51.77.52.56** |
| IPv6 | 2001:41d0:602:2638::1 |
| vRack | pn-1303451 |
| OS installé | **Proxmox VE 9** (déjà en place) |
| Accès Proxmox | https://51.77.52.56:8006 |
| Compte OVH | ul21787-ovh (Marwane Zaid) |

## Budget RAM recommandé (indicatif)

| VM / service | RAM min. | RAM conseillée |
|--------------|----------|----------------|
| Proxmox (hôte) | — | 2–4 Go réservés |
| pfSense | 512 Mo | 1 Go |
| Contrôleur AD | 2 Go | 4 Go |
| Hôte Docker (SOC) | 4 Go | 8 Go |
| VMs lab Red Team | 2 Go | 4 Go |

> 32 Go RAM : configuration confortable pour tout le projet si les VMs ne tournent pas toutes à 100 % en même temps.

## Réseau — plages internes (VMs)

| Segment | Plage | Usage |
|---------|-------|--------|
| LAN | 192.168.10.0/24 | AD, postes admin |
| DMZ | 192.168.20.0/24 | Reverse proxy |
| SOC | 192.168.30.0/24 | Wazuh, Grafana |
| LAB-RT | 192.168.99.0/24 | Red Team isolé |

Schéma : [topologie-reseau.md](topologie-reseau.md)

## Sauvegarde

- Snapshots Proxmox : quotidien sur VMs critiques
- Export config pfSense : hebdo
- Agent backup OVH : optionnel (non installé actuellement)
