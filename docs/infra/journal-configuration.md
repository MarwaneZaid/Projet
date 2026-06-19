# Journal de configuration — en direct

**Serveur :** `ns3138292.ip-51-77-52.eu` — **51.77.52.56** — Proxmox VE 9  
**Compte OVH :** `ul21787-ovh` (Marwane Zaid)

---

## Étapes réalisées (session agent)

| # | Date | Action | Résultat |
|---|------|--------|----------|
| 1 | 2026-05-19 | Test connectivité ICMP vers 51.77.52.56 | Ping bloqué (normal OVH) |
| 2 | 2026-05-19 | Test TCP port 22 (SSH) | **Timeout** — firewall OVH ou filtrage réseau |
| 3 | 2026-05-19 | Test UI Proxmox `https://51.77.52.56:8006` | **Inaccessible** depuis l’environnement agent |
| 4 | 2026-05-19 | SSH batch `root@51.77.52.56` | **Timeout** — pas d’accès sans ouverture firewall |
| 5 | 2026-05-19 | Manager OVH (navigateur) | **Connecté** — serveur `ns3138292` + vRack `pn-1303451` visibles |
| 6 | 2026-05-19 | Scripts post-install Proxmox | Créés : `scripts/proxmox/01-host-postinstall.sh`, `02-create-vms.sh` |
| 7 | 2026-05-19 | Guides pas à pas | `docs/infra/01-firewall-ovh.md`, `02-premier-acces-proxmox.md` |
| 8 | 2026-05-19 | Retest port 22 | **Timeout** (inchangé) |
| 9 | 2026-05-19 | IP publique détectée (curl) | `46.193.6.82` |
| 10 | 2026-05-19 | Scripts bootstrap | `bootstrap-serveur.sh`, `ovh_configure_firewall.py` |

---

## Blocage actuel

**Le pare-feu réseau OVH n’autorise pas encore SSH ni Proxmox depuis l’extérieur.**

→ Action humaine requise : suivre [01-firewall-ovh.md](01-firewall-ovh.md) avec **votre IP publique**.

---

## Prochaines étapes (ordre)

1. [ ] Firewall OVH — IP équipe sur 22 et 8006
2. [ ] SSH + `01-host-postinstall.sh`
3. [ ] VMs : pfSense, AD, docker-soc, lab-rt
4. [ ] pfSense → AD → SOC Docker

Voir [serveur-ovh-configuration.md](serveur-ovh-configuration.md).
