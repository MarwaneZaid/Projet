# Spécifications matériel & contraintes

À compléter par l’équipe avant installation Proxmox.

## Serveur hôte

| Paramètre | Valeur |
|-----------|--------|
| CPU | _modèle / cœurs / threads_ |
| RAM totale | _Go_ |
| Stockage | _SSD/HDD, capacité, RAID ?_ |
| Réseau | _1 ou 2 NIC, débit_ |
| IP management Proxmox | _ex. 10.0.0.10/24_ |

## Budget RAM recommandé (indicatif)

| VM / service | RAM min. | RAM conseillée |
|--------------|----------|----------------|
| Proxmox (hôte) | — | 2–4 Go réservés |
| pfSense | 512 Mo | 1 Go |
| Contrôleur AD | 2 Go | 4 Go |
| Hôte Docker (SOC + partiel RT) | 4 Go | 8–16 Go |
| VMs lab Red Team | 2 Go | 4 Go chacune |

> Sur serveur **très limité** : regrouper SOC sur une seule VM ; Red Team sur une autre ; pas tout en parallèle en prod démo.

## Réseau — brouillon IP (à valider)

| Segment | VLAN / interface | Plage exemple | Usage |
|---------|------------------|---------------|--------|
| LAN | vtnet0 / vmbr0 | 192.168.10.0/24 | AD, postes admin |
| DMZ | vtnet1 / vmbr1 | 192.168.20.0/24 | Reverse proxy, services exposés |
| SOC | interne | 192.168.30.0/24 | Wazuh, Grafana, TheHive |
| LAB-RT | isolé | 192.168.99.0/24 | Red Team — **sans route vers LAN** |

Schéma détaillé : [topologie-reseau.md](topologie-reseau.md)

## Sauvegarde

- Snapshots Proxmox : fréquence _à définir_
- Export config pfSense : hebdo
- Rétention : _X jours_
