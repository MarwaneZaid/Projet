# NexaMind — Projet annuel ESGI (cybersécurité)

Entreprise fictive **NexaMind SAS** : infra Proxmox, SOC Wazuh, portail client, Active Directory, démo attaque/détection.

**Serveur :** OVH `ns3138292` · `51.77.52.56` · Proxmox via VPN → `https://192.168.20.254:8006`

---

## État du projet (juin 2026)

**Document détaillé :** [docs/ETAT-PROJET.md](docs/ETAT-PROJET.md) · **Fin de projet :** [docs/livrables/FIN-PROJET-CHECKLIST.md](docs/livrables/FIN-PROJET-CHECKLIST.md)

### Équipe

| Membre | Rôle |
|--------|------|
| **Victor** | Portail web + Wazuh (`192.168.20.20` / `.22`) + IA |
| **Jacques** | AD Samba `cybernest.local` + `client-win-1` |
| **Abdoul** | pfSense + VPN + doc infra |
| **Marwane** | Passbolt + Suricata + Kali Docker |

### Résumé rapide

| Brique | État |
|--------|------|
| Proxmox, pfSense, VPN | ✅ Fait |
| Portail web + alertes | ✅ Fait (Victor) |
| Wazuh SOC + détection portail | ✅ Fait (Victor, VM 201) |
| Samba AD installé | ✅ VM up, 🟡 **vide** (Jacques) |
| Passbolt installé | ✅ 🟡 **à remplir** (Marwane) |
| Suricata + Kali Docker | 🟡 À faire (Marwane) |
| Agents Wazuh AD/Windows | 🟡 À faire (Victor) |
| Rapport + démo soutenance | 🟡 Juillet 2026 |

### VMs clés

```
192.168.20.1   pfSense          192.168.20.20  portail
192.168.20.10  AD               192.168.20.22  Wazuh (référence)
192.168.20.18  Suricata (107)   192.168.20.254 Proxmox
```

---

## Dépôts équipe

| Repo | Usage |
|------|--------|
| **Ce dépôt** | Suivi tâches, runbooks, scripts, livrables |
| [moralisateur380/projet_annuel](https://github.com/moralisateur380/projet_annuel) | Kit NexaMind V2, code portail, scénario démo |
| [Abdoulmyges/Projet-Pro_4esgi](https://github.com/Abdoulmyges/Projet-Pro_4esgi) | Wiki infra (pfSense, VPN, AD, Passbolt) |

Workflow Git : **une branche par membre → merge sur `main`**.

---

## Structure du dépôt

```
├── docs/
│   ├── ETAT-PROJET.md      ← état fait / à faire (à jour)
│   ├── taches/             ← fiches P0–P5 par partie
│   ├── wiki/               ← runbooks pas à pas
│   ├── infra/              ← OVH, Proxmox
│   └── livrables/          ← captures, preuves MVP
├── scripts/                ← OVH, Proxmox, SOC
├── soc/                    ← docker-compose Wazuh (référence)
├── portal/                 ← squelette (code principal chez Victor)
├── infra/                  ← pfSense, AD
└── _upstream/              ← clones analyse (non versionné idéalement)
```

---

## Démarrage rapide

1. Se connecter au **VPN OpenVPN** (profil `.ovpn` personnel)
2. Lire [docs/ETAT-PROJET.md](docs/ETAT-PROJET.md)
3. Aller dans **son guide** (kit Victor V2, dossier 02–05)
4. Secrets → **Passbolt** uniquement (pas Discord, pas Git)

**Infra OVH :** [docs/infra/01-firewall-ovh.md](docs/infra/01-firewall-ovh.md) · [02-premier-acces-proxmox.md](docs/infra/02-premier-acces-proxmox.md)

**Tâches détaillées :** [docs/taches/README.md](docs/taches/README.md)

---

## Règles d'équipe

- Pas de secrets dans Git (`.env` local, Passbolt pour l'équipe)
- Wazuh officiel : **Victor** / `srv-wazuh-1` / `192.168.20.22`
- Validation collective avant soutenance → [CHECKLIST.md](CHECKLIST.md)
- Red Team : lab isolé, scénarios contrôlés uniquement

---

## Livrables finaux (juillet 2026)

- Rapport technique ~12 pages
- Démo live 35 min (attaque → détection → portail) + **vidéo de secours**
- Schémas architecture + flux attaque
- Wiki / procédures à jour sur `main`
