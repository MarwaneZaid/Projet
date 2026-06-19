# État du projet NexaMind — fait / reste à faire

> Mise à jour : **18 juin 2026** · Soutenance juillet 2026  
> Serveur : OVH `ns3138292` · Proxmox `https://192.168.20.254:8006` (VPN)

**Checklist fin de projet :** [livrables/FIN-PROJET-CHECKLIST.md](livrables/FIN-PROJET-CHECKLIST.md)

---

## Équipe et rôles

| Membre | Mission |
|--------|---------|
| **Victor** | Portail `192.168.20.20` + Wazuh `192.168.20.22` + IA Claude |
| **Jacques** | AD `nexamind.local` + `client-win-1` |
| **Abdoul** | pfSense + VPN + doc infra |
| **Marwane** | Passbolt + Suricata (107) + démo attaque |

**Décisions :** Wazuh officiel = **VM 201** (`.22`) uniquement · VM 107 = Suricata · Kali = Docker

---

## Plan d'adressage (IPs réelles mesurées)

| VM ID | Nom | IP | Rôle | État |
|-------|-----|-----|------|------|
| 100 | srv-pfsense-ro | 192.168.20.1 | Firewall + VPN | ✅ |
| 103 | srv-passbolt-1 | **192.168.20.15** | Passbolt | 🟡 vide |
| 104 | srv-ad-1 | **192.168.20.16** | Samba AD `nexamind.local` | 🟡 agent Wazuh ✅ · users vides |
| 105 | win10-tempon | 192.168.20.17 | Windows test | ✅ (RAM) |
| 106 | client-win-1 | 192.168.20.13 | Poste Windows | ✅ agent Wazuh · hors domaine |
| 107 | srv-soc-1 | **192.168.20.18** | Suricata + démo attaque | ✅ Suricata |
| 200 | srv-web-1 | 192.168.20.20 | Portail NexaMind | ✅ |
| 201 | srv-wazuh-1 | 192.168.20.22 | Wazuh SOC | ✅ |
| 101/102 | templates | — | Debian / Win10 | ✅ |
| 110 | ct-test | DHCP | LXC test | ✅ |
| — | Proxmox | 192.168.20.254 | Hyperviseur | ✅ (~94 % RAM) |

---

## Ce qui est fait

- ✅ Infra Proxmox, pfSense, VPN, templates
- ✅ Portail FastAPI + nginx + agent Wazuh
- ✅ Wazuh 4.9.2 sur `.22` — agents : web, AD, **Windows**, manager local
- ✅ Captures MVP SOC dans `docs/livrables/screenshots/04-soc/` (3 alertes + agents)
- ✅ Détection brute-force portail validée (Victor)
- ✅ Passbolt installé sur `.15`
- ✅ AD Samba DC opérationnel sur `.16` (annuaire vide)
- ✅ Suricata 7.0.10 sur `.18` (interface `ens18`)
- ✅ Scripts démo : `scripts/demo/` + copie sur `nexa@192.168.20.18:~/demo-attaque/`
- ✅ Wazuh VM 107 arrêté + cron maintenance supprimé

---

## Ce qui reste (bloquant soutenance)

| Priorité | Qui | Quoi |
|----------|-----|------|
| P0 | **Marwane** | Remplir Passbolt + inviter l'équipe |
| P0 | **Jacques** | Users/groupes AD + joindre `client-win-1` + audit |
| P0 | **Victor** | Clé API Claude · merge repo V2 |
| P1 | **Abdoul** | Règles pfSense → `.22` (1514/1515) · retirer secrets Git |
| P1 | **Tous** | Répéter démo 3× · rapport · captures `soc-mvp-preuves.md` |

---

## Accès rapides (VPN)

| Service | URL |
|---------|-----|
| Proxmox | https://192.168.20.254:8006 |
| Portail | http://192.168.20.20 |
| Wazuh | https://192.168.20.22 |
| Passbolt | https://192.168.20.15 |
| pfSense | https://192.168.20.1 |

---

## Dépôts

| Repo | Rôle |
|------|------|
| [MarwaneZaid/Projet](https://github.com/MarwaneZaid/Projet) | Repo principal (tâches, scripts, livrables) |
| [moralisateur380/projet_annuel](https://github.com/moralisateur380/projet_annuel) | Kit V2 Victor |
| [Abdoulmyges/Projet-Pro_4esgi](https://github.com/Abdoulmyges/Projet-Pro_4esgi) | Wiki infra Abdoul |

---

## Sécurité

- Secrets uniquement dans **Passbolt** (pas Discord / Git)
- `password.txt` repo Abdoul → à supprimer + rotation
