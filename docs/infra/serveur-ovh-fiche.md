# Fiche serveur OVH — inventaire (mai 2026)

Source : Manager OVH + API console (session connectée).

## Compte

| Champ | Valeur |
|-------|--------|
| NIC / nichandle | `ul21787-ovh` |
| Contact | Marwane Zaid |
| Email | m.zaid@myskolae.fr |

## Serveur dédié principal

| Champ | Valeur |
|-------|--------|
| Nom OVH | `ns3138292.ip-51-77-52.eu` |
| Gamme | **KS-5** \| Intel Xeon-E3 1270 v6 |
| CPU | Intel Xeon-E3 1270 v6 — 4 cœurs / 8 threads — 3,8–4,2 GHz |
| RAM | **32 Go** ECC 2400 MHz |
| Stockage | **2×2 To** HDD SATA — **Soft RAID** (~4 To utile) |
| Datacenter | **waw1** (Varsovie, Pologne) |
| Zone | `eu-central-waw-a` |
| État | `poweron` (allumé) |
| Support | Pro |
| Renouvellement auto | Oui (échéance ~1 juin 2026) |

## Réseau

| Type | Adresse |
|------|---------|
| IPv4 principale | **51.77.52.56** |
| IPv6 | **2001:41d0:602:2638::1** |
| vRack | `pn-1303451` (service actif) |

## Système installé (déjà en place)

| Champ | Valeur |
|-------|--------|
| OS | **Proxmox Virtual Environment 9** |
| Boot | `hd` — Boot to disk |
| Monitoring OVH | Désactivé |
| Agent backup OVH | Non installé |

> **Bonne nouvelle :** Proxmox est déjà installé — pas besoin de réinstaller l’OS. Passez directement à la configuration Proxmox + création des VMs.

## Accès administration

| Service | URL / commande |
|---------|----------------|
| Proxmox UI | `https://51.77.52.56:8006` |
| SSH (root) | `ssh root@51.77.52.56` |
| Manager | [Serveur dédié](https://manager.eu.ovhcloud.com/#/dedicated/server/ns3138292.ip-51-77-52.eu) |

## Capacité VMs (estimation sur 32 Go RAM)

| VM | RAM conseillée | Rôle |
|----|----------------|------|
| pfSense | 1 Go | Firewall |
| AD | 4 Go | Contrôleur domaine |
| docker-soc01 | 8 Go | Wazuh, Grafana, SOC |
| lab-rt01 | 4 Go | Red Team isolé |
| Postes / tests | 2–4 Go | Clients Windows |
| **Total** | ~19–21 Go | Marge ~10 Go pour Proxmox |

## Services OVH liés

- Serveur dédié `ns3138292.ip-51-77-52.eu`
- vRack `pn-1303451`

---

## Configuration recommandée (à faire)

Voir [serveur-ovh-configuration.md](serveur-ovh-configuration.md).
