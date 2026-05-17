# 02 — Réseau pfSense

**Responsable :** Étudiant 2 (profil cyber → rôle réseau)  
**Relecteur :** Étudiant 1  
**Priorité globale :** P1  
**Dépôt :** [infra/pfsense/](../../infra/pfsense/)

**Prérequis :** VM pfSense créée sur Proxmox (tâche 1.9)

---

## P0 — Bloquant

| # | Tâche exacte | Détail technique | Validé |
|---|--------------|------------------|--------|
| 2.1 | Installer pfSense sur la VM | ISO pfSense, assignation interfaces | [ ] |
| 2.2 | Configurer interfaces : **WAN**, **LAN** minimum | WAN = uplink école/internet ; LAN = segment admin | [ ] |
| 2.3 | Activer accès web pfSense depuis LAN | `https://IP_LAN` accessible | [ ] |

---

## P1 — Critique

| # | Tâche exacte | Détail technique | Validé |
|---|--------------|------------------|--------|
| 2.4 | **NAT** sortant LAN → WAN | Les VMs LAN accèdent à Internet pour updates | [ ] |
| 2.5 | **DHCP** sur LAN avec plage définie en cadrage | Ex. 192.168.10.100–200 | [ ] |
| 2.6 | **Réservations DHCP** : IP fixes pour AD, Docker, pfSense | Même IP après reboot | [ ] |
| 2.7 | Règles firewall : **deny by default** sur entrée WAN | Seuls services voulus ouverts | [ ] |
| 2.8 | Règle : LAN → Internet (sortant) | Test : `ping 8.8.8.8` depuis VM LAN | [ ] |
| 2.9 | Créer interface **OPT** (DMZ) si prévu au schéma | Plage DMZ séparée | [ ] |
| 2.10 | Règle : DMZ **ne joint pas** LAN directement (sauf via proxy plus tard) | Test ping LAN depuis DMZ = échec | [ ] |
| 2.11 | Activer **logs firewall** | Menu Status → System Logs → Firewall | [ ] |
| 2.12 | Export config pfSense (backup XML) | Procédure + 1 export daté dans `docs/procedures/` | [ ] |

---

## P2 — Important (préparation SOC)

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 2.13 | Préparer règle future : LAN/SOC → Wazuh (ports 1514/1515) — documenter sans ouvrir trop tôt | [ ] |
| 2.14 | Configurer **Syslog remote** vers IP future du manager Wazuh (quand SOC prêt) | [ ] |
| 2.15 | Documenter tableau des règles dans `docs/procedures/pfsense-regles.md` | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 2.16 | VPN site-to-site (IPsec ou OpenVPN) — ou documenter pourquoi impossible | [ ] |
| 2.17 | Test backup/restore config XML sur VM pfSense de lab | [ ] |

---

## Tests de validation

```text
Depuis VM LAN : ping passerelle pfSense → OK
Depuis VM LAN : ping Internet → OK
Depuis DMZ (si existant) : ping LAN → ÉCHEC attendu
```

---

## Critères « pfSense validé »

- [ ] NAT + DHCP opérationnels  
- [ ] Isolation DMZ/LAN démontrée  
- [ ] Backup config archivé  
- [ ] Relecture Étudiant 1 OK  

**Ensuite :** [03-active-directory.md](03-active-directory.md) + installation Docker sur VM dédiée
