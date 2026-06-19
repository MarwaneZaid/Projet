# Fin de projet NexaMind — checklist équipe (juillet 2026)

> Dernière mise à jour : juin 2026 · Soutenance 35 min

## État global

| Brique | Responsable | Statut |
|--------|-------------|--------|
| Proxmox + pfSense + VPN | Abdoul | ✅ Fait |
| Portail `192.168.20.20` | Victor | ✅ Fait |
| Wazuh `192.168.20.22` | Victor | ✅ Fait (4 agents dont Windows) |
| Passbolt `192.168.20.15` | Marwane | 🟡 À remplir |
| AD `nexamind.local` `.16` | Jacques | 🟡 users vides · agent Wazuh ✅ |
| `client-win-1` `.13` | Jacques | 🟡 Agent Wazuh ✅ · domaine à faire |
| Suricata VM 107 `.18` | Marwane | ✅ Actif (`ens18`) |
| Kali Docker démo | Marwane | 🟡 Scripts dans `scripts/demo/` |
| Rapport + captures SOC | Tous | ✅ Captures `04-soc/` |

---

## Par personne — à cocher avant soutenance

### Victor
- [x] Agent Wazuh sur AD (`.16`) — `srv-ad-1` Active
- [x] Agent Wazuh **Windows** `client-win-1` (`.13`) Active
- [ ] Clé API Claude sur le portail (env, pas Git)
- [x] Captures SOC MVP dans `docs/livrables/screenshots/04-soc/` (pas vidéo)
- [ ] Merger `NexaMind-Projet-V2` sur le repo principal

### Jacques
- [ ] Users + groupes + OU sur `srv-ad-1` (`nexamind.local`)
- [ ] Joindre `client-win-1` au domaine
- [ ] Audit Samba (`auth_audit`) pour alertes AD
- [ ] Demander à Abdoul règles pfSense si agents cross-segment

### Abdoul
- [ ] Règles pfSense → `192.168.20.22` : TCP 1514, 1515, UDP 1514
- [ ] Retirer `password.txt` du repo GitHub + rotation mdp
- [ ] Merger wiki infra dans `docs/`

### Marwane
- [ ] Passbolt : inviter équipe + tous les secrets
- [ ] VM 107 : Wazuh Docker **éteint** (SOC = `.22` uniquement)
- [ ] Tester `~/demo-attaque/attaque-test.sh` depuis 107
- [x] Captures dans `docs/livrables/screenshots/04-soc/`
- [x] Remplir `docs/livrables/soc-mvp-preuves.md`

### Tous
- [ ] Call synchro 30 min : valider qui a fini quoi
- [ ] Répéter scénario 3× ([kit Victor `09-Scenario-Demo`](https://github.com/moralisateur380/projet_annuel))
- [ ] Rapport ~12 pages

---

## Scénario démo (13–22 min)

1. Montrer Wazuh + portail OK  
2. Depuis VM 107 : `~/demo-attaque/attaque-test.sh 192.168.20.20`  
3. Alerte brute-force dans Wazuh (`.22`)  
4. Alerte remontée sur portail  
5. (Bonus) Suricata `tail -f /var/log/suricata/eve.json`  
6. (Bonus) Analyse Claude  

---

## IPs réelles (référence)

| IP | VM | Rôle |
|----|-----|------|
| .1 | 100 | pfSense |
| .13 | 106 | client-win-1 |
| .15 | 103 | Passbolt |
| .16 | 104 | AD `nexamind.local` |
| .17 | 105 | win10-tempon |
| .18 | 107 | Suricata |
| .20 | 200 | Portail |
| .22 | 201 | Wazuh |
| .254 | — | Proxmox |

---

## Commandes utiles

```bash
# Attaque démo (sur 107)
ssh nexa@192.168.20.18
~/demo-attaque/attaque-test.sh

# Suricata
sudo tail -f /var/log/suricata/eve.json

# Wazuh (Victor)
https://192.168.20.22

# Portail
http://192.168.20.20
```
