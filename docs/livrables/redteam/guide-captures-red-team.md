# Guide captures Red Team — étape par étape

> **Dossier de sortie :** [`docs/livrables/screenshots/05-red-team/`](../screenshots/05-red-team/)  
> **Machine attaque :** VM 107 · `192.168.20.18` · user `nexa`  
> **Prérequis :** VPN OpenVPN connecté

---

## Vue d’ensemble — 10 captures à produire

| # | Fichier PNG | Méthode |
|---|-------------|---------|
| 1 | [05-red-team_terminal-run-all.png](../screenshots/05-red-team/05-red-team_terminal-run-all.png) | Auto |
| 2 | [05-red-team_scan-nmap-result.png](../screenshots/05-red-team/05-red-team_scan-nmap-result.png) | Auto |
| 3 | [05-red-team_bruteforce-ssh-done.png](../screenshots/05-red-team/05-red-team_bruteforce-ssh-done.png) | Auto |
| 4 | [05-red-team_failed-logon-ad-done.png](../screenshots/05-red-team/05-red-team_failed-logon-ad-done.png) | Auto |
| 5 | [05-red-team_suricata-eve-flows.png](../screenshots/05-red-team/05-red-team_suricata-eve-flows.png) | Auto |
| 6 | [05-red-team_suricata-eve-alerts.png](../screenshots/05-red-team/05-red-team_suricata-eve-alerts.png) | Auto |
| 7 | [05-red-team_wazuh-alerts-after-attack.png](../screenshots/05-red-team/05-red-team_wazuh-alerts-after-attack.png) | Auto |
| 8 | [05-red-team_vm107-attacker-overview.png](../screenshots/05-red-team/05-red-team_vm107-attacker-overview.png) | Auto |
| 9 | [05-rt_journal-exercice.png](../screenshots/05-red-team/05-rt_journal-exercice.png) | Auto |
| 10 | [05-rt_correlation-soc.png](../screenshots/05-red-team/05-rt_correlation-soc.png) | Auto |

**Méthode auto recommandée** : une commande génère les 10 PNG (voir § A).  
**Méthode manuelle** : commandes une par une + capture Mac (voir § B).

---

## § A — Tout regénérer en une commande (recommandé)

### Étape A.1 — Vérifier le VPN

```bash
ping -c 1 192.168.20.18
```

**Attendu :** `1 packets received`  
**Si échec :** reconnecter OpenVPN avant de continuer.

---

### Étape A.2 — (Optionnel) Sync scripts sur VM 107

```bash
cd /Users/skat/Desktop/Projet
SSHPASS='NexaMind2026!' sshpass -e bash scripts/redteam/deploy-to-vm107.sh
```

**Attendu :** `[*] OK — lancer : ssh nexa@192.168.20.18 'bash ~/redteam/run-all.sh'`

---

### Étape A.3 — (Une fois) Règles Suricata lab

> Skip si déjà fait. Nécessaire pour les alertes **NEXAMIND LAB** (sid 9000001–9000003).

```bash
SSHPASS='NexaMind2026!' sshpass -e ssh nexa@192.168.20.18 \
  'echo NexaMind2026! | sudo -S bash ~/redteam/install-suricata-lab-rules.sh'
```

**Attendu :** `active` + `sid 9000001–9000003`

---

### Étape A.4 — Générer les 10 PNG

```bash
cd /Users/skat/Desktop/Projet
python3 scripts/redteam/generate-redteam-screenshots.py
```

**Attendu :** liste des 10 fichiers + `Done — docs/livrables/screenshots/05-red-team`

**Captures produites :**

1. [05-red-team_terminal-run-all.png](../screenshots/05-red-team/05-red-team_terminal-run-all.png)
2. [05-red-team_scan-nmap-result.png](../screenshots/05-red-team/05-red-team_scan-nmap-result.png)
3. [05-red-team_bruteforce-ssh-done.png](../screenshots/05-red-team/05-red-team_bruteforce-ssh-done.png)
4. [05-red-team_failed-logon-ad-done.png](../screenshots/05-red-team/05-red-team_failed-logon-ad-done.png)
5. [05-red-team_suricata-eve-flows.png](../screenshots/05-red-team/05-red-team_suricata-eve-flows.png)
6. [05-red-team_suricata-eve-alerts.png](../screenshots/05-red-team/05-red-team_suricata-eve-alerts.png)
7. [05-red-team_wazuh-alerts-after-attack.png](../screenshots/05-red-team/05-red-team_wazuh-alerts-after-attack.png)
8. [05-red-team_vm107-attacker-overview.png](../screenshots/05-red-team/05-red-team_vm107-attacker-overview.png)
9. [05-rt_journal-exercice.png](../screenshots/05-red-team/05-rt_journal-exercice.png)
10. [05-rt_correlation-soc.png](../screenshots/05-red-team/05-rt_correlation-soc.png)

---

### Étape A.5 — Vérifier visuellement

```bash
open docs/livrables/screenshots/05-red-team/
```

**Checklist :**

- [ ] Hydra visible sur `05-red-team_bruteforce-ssh-done.png` (`[ATTEMPT]`, `Hydra v9.5`)
- [ ] Alertes `NEXAMIND LAB` sur `05-red-team_suricata-eve-alerts.png` (sid **9000001**, **9000002**, **9000003**)
- [ ] Alertes Wazuh `authentication_failed` sur `05-red-team_wazuh-alerts-after-attack.png`

---

## § B — Manuel commande par commande (démo live / Mac capture)

Utilise cette section si tu veux **capturer toi-même** avec `Cmd+Shift+4` au lieu du script Python.

**Dossier cible :** `docs/livrables/screenshots/05-red-team/`

---

### Étape B.1 — Connexion VM attaquant

```bash
ssh nexa@192.168.20.18
```

Mot de passe équipe (Passbolt / `NexaMind2026!`).

---

### Étape B.2 — RT-02 Port scan (nmap)

```bash
bash ~/redteam/scan-nmap.sh 192.168.20.20
```

**Quoi montrer :** bannière `RT-02`, ports `22/tcp open`, `80/tcp open`, `Fin RT-02`  
**Capture Mac :** `Cmd+Shift+4` sur le terminal  
**Fichier :** [05-red-team_scan-nmap-result.png](../screenshots/05-red-team/05-red-team_scan-nmap-result.png)

---

### Étape B.3 — RT-01 Brute-force SSH (Hydra)

```bash
bash ~/redteam/bruteforce-ssh.sh 192.168.20.20
```

**Quoi montrer :** commande Hydra, lignes `[ATTEMPT]`, `0 valid password found`  
**Capture Mac :** terminal Hydra  
**Fichier :** [05-red-team_bruteforce-ssh-done.png](../screenshots/05-red-team/05-red-team_bruteforce-ssh-done.png)

Commande exacte exécutée :

```bash
hydra -l attacker-demo -P /tmp/rt01-wordlist.txt ssh://192.168.20.20 -t 4 -f -V
```

---

### Étape B.4 — RT-03 Failed logon AD

```bash
bash ~/redteam/failed-logon-ad.sh 192.168.20.16
```

**Quoi montrer :** tentatives SSH vers `.16`, `Fin RT-03`  
**Capture Mac :** terminal  
**Fichier :** [05-red-team_failed-logon-ad-done.png](../screenshots/05-red-team/05-red-team_failed-logon-ad-done.png)

---

### Étape B.5 — Run-all complet (optionnel, 1 seule capture)

```bash
PAUSE=2 bash ~/redteam/run-all.sh
```

**Quoi montrer :** enchaînement RT-02 → RT-01 → RT-03  
**Fichier :** [05-red-team_terminal-run-all.png](../screenshots/05-red-team/05-red-team_terminal-run-all.png)

---

### Étape B.6 — Suricata flows (réseau)

```bash
grep '"dest_ip":"192.168.20.20"' /var/log/suricata/eve.json | \
  grep '"src_ip":"192.168.20.18"' | tail -8
```

**Quoi montrer :** lignes JSON `"event_type":"flow"`, `"app_proto":"ssh"`  
**Fichier :** [05-red-team_suricata-eve-flows.png](../screenshots/05-red-team/05-red-team_suricata-eve-flows.png)

---

### Étape B.7 — Suricata alertes IDS (signature)

```bash
grep '"event_type":"alert"' /var/log/suricata/eve.json | tail -5
```

Ou format lisible :

```bash
bash ~/redteam/show-suricata-alerts.sh
```

**Quoi montrer :** signatures **NEXAMIND LAB** :

| sid | Signature |
|-----|-----------|
| 9000001 | NEXAMIND LAB TCP Port Scan (nmap recon) |
| 9000002 | NEXAMIND LAB SSH Brute Force (Hydra) |
| 9000003 | NEXAMIND LAB SSH Login Attempts AD |

**Fichier :** [05-red-team_suricata-eve-alerts.png](../screenshots/05-red-team/05-red-team_suricata-eve-alerts.png)

---

### Étape B.8 — Wazuh alertes post-attaque

Navigateur :

```
https://192.168.20.22
```

Login : `wazuh-wui` / mot de passe Wazuh (équipe).

**Où :** Security Events → filtrer agent `srv-web-1` et `srv-ad-1`  
**Quoi montrer :** rules **5710** / **5712** (SSH failed), alertes récentes (même date que l’attaque)  
**Fichier :** [05-red-team_wazuh-alerts-after-attack.png](../screenshots/05-red-team/05-red-team_wazuh-alerts-after-attack.png)

---

### Étape B.9 — Vue VM attaquant

```bash
echo HOST=$(hostname)
echo IP=$(hostname -I)
suricata -V 2>/dev/null | head -1
systemctl is-active suricata
ls ~/redteam/*.sh
```

**Quoi montrer :** `srv-soc-1`, IP `.18`, Suricata `7.0.10`, service `active`, scripts `~/redteam/`  
**Fichier :** [05-red-team_vm107-attacker-overview.png](../screenshots/05-red-team/05-red-team_vm107-attacker-overview.png)

---

### Étape B.10 — Journal exercices

Sur ton Mac (Cursor ou navigateur fichier) :

```
docs/livrables/redteam/journal-exercices.md
```

**Quoi montrer :** tableau avec dates, MITRE T1046 / T1110.001, colonne « Alerte SOC ✅ »  
**Fichier :** [05-rt_journal-exercice.png](../screenshots/05-red-team/05-rt_journal-exercice.png)

---

### Étape B.11 — Corrélation attaque ↔ SOC

**Montage 2 fenêtres côte à côte :**

- Gauche : terminal `run-all.sh` (heure fin RT-01 / RT-02)
- Droite : Wazuh alerte même créneau horaire

**Fichier :** [05-rt_correlation-soc.png](../screenshots/05-red-team/05-rt_correlation-soc.png)

---

## § C — Dépannage

### Pas d’alertes NEXAMIND LAB dans Suricata

```bash
ssh nexa@192.168.20.18
echo NexaMind2026! | sudo -S bash ~/redteam/install-suricata-lab-rules.sh
echo NexaMind2026! | sudo -S systemctl restart suricata
PAUSE=2 bash ~/redteam/run-all.sh
grep NEXAMIND /var/log/suricata/eve.json | tail -5
```

Puis regénérer :

```bash
python3 scripts/redteam/generate-redteam-screenshots.py
```

---

### Hydra absent sur VM 107

```bash
ssh nexa@192.168.20.18
echo NexaMind2026! | sudo -S apt-get install -y hydra
hydra -V 2>&1 | head -1
```

---

### Script Python : `No module named PIL`

```bash
pip3 install pillow
```

---

### Script Python : `sshpass: command not found`

```bash
brew install sshpass
```

---

## § D — Pitch démo (30 s)

> « Depuis la VM 107 nous simulons un attaquant : **nmap** pour la reconnaissance, **Hydra** pour le brute-force SSH sur le portail, puis tentatives sur l’AD. Wazuh détecte les échecs dans les logs (rules 5710/5712). Suricata détecte le même trafic au niveau réseau — signatures NEXAMIND LAB dans eve.json. Double détection logs + réseau. »

---

## Liens utiles

| Doc | Lien |
|-----|------|
| Runbook Red Team | [runbook-red-team.md](runbook-red-team.md) |
| Journal exercices | [journal-exercices.md](journal-exercices.md) |
| Preuves / corrélation | [preuves-red-team.md](preuves-red-team.md) |
| Scripts | [`scripts/redteam/`](../../../scripts/redteam/) |
| Dossier PNG | [`screenshots/05-red-team/`](../screenshots/05-red-team/) |
