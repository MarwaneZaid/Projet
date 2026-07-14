# Runbook Red Team — NexaMind (lab contrôlé)

**Responsable :** Marwane · **Relecteur SOC :** Victor  
**Machine attaque :** VM 107 `192.168.20.18` (Suricata + scripts)

---

## 0. Règles de sécurité (obligatoire)

1. Attaques **uniquement** vers les IP du tableau ci-dessous.
2. **Jamais** : IP publique `51.77.52.56`, réseau campus, Internet, comptes réels.
3. Noter chaque exercice dans [journal-exercices.md](journal-exercices.md).
4. Prévenir l'équipe avant un `run-all.sh` en production démo.

### Cibles autorisées

| IP | VM | Rôle | Scénarios |
|----|-----|------|-----------|
| 192.168.20.20 | 200 | Portail | RT-01, RT-02 |
| 192.168.20.16 | 104 | AD Samba | RT-03 |
| 192.168.20.13 | 106 | Windows | (futur, après domaine) |

---

## 1. Prérequis

- VPN OpenVPN connecté
- Accès SSH : `ssh nexa@192.168.20.18` (mot de passe équipe / Passbolt)
- Wazuh accessible : `https://192.168.20.22`

---

## 2. Installation des scripts sur VM 107

Depuis ton Mac (repo cloné) :

```bash
cd /chemin/vers/Projet
chmod +x scripts/redteam/*.sh
SSHPASS='...' sshpass -e bash scripts/redteam/deploy-to-vm107.sh
```

Ou copie manuelle :

```bash
scp scripts/redteam/*.sh nexa@192.168.20.18:~/redteam/
ssh nexa@192.168.20.18 'chmod +x ~/redteam/*.sh'
```

---

## 3. Scénarios

### RT-01 — Brute-force SSH (Hydra)

```bash
bash ~/redteam/bruteforce-ssh.sh 192.168.20.20
```

- **MITRE :** T1110.001  
- **Outil :** `hydra -l attacker-demo -P /tmp/rt01-wordlist.txt ssh://192.168.20.20 -t 4 -f -V`  
- **Détection :** Wazuh rules 5710, 5712 sur agent `srv-web-1` + Suricata sid **9000002** (NEXAMIND LAB SSH Brute Force)

### RT-02 — Port scan

```bash
bash ~/redteam/scan-nmap.sh 192.168.20.20
```

- **MITRE :** T1046  
- **Détection :** Wazuh + Suricata (`eve.json`)

### RT-03 — Attaque SSH vers AD

```bash
bash ~/redteam/failed-logon-ad.sh 192.168.20.16
```

- **MITRE :** T1110.001, T1078  
- **Détection :** Wazuh agent `srv-ad-1`

### Tout enchaîner

```bash
bash ~/redteam/run-all.sh
```

Variable `PAUSE=5` pour réduire les pauses entre scénarios.

### Suricata — alertes IDS (preuve double détection)

```bash
grep '"event_type":"alert"' /var/log/suricata/eve.json | tail -5
bash ~/redteam/show-suricata-alerts.sh
```

Règles lab internes (une fois, sudo) :

```bash
sudo bash ~/redteam/install-suricata-lab-rules.sh
```

---

## 4. Vérification SOC (Victor / Marwane)

1. Wazuh → **Threat Hunting** ou **Security Events**
2. Filtrer par agent : `srv-web-1`, `srv-ad-1`
3. Noter rule.id et timestamp → compléter le journal
4. Portail `http://192.168.20.20` → dashboard alertes

---

## 5. Livrables

| Fichier | Contenu |
|---------|---------|
| [journal-exercices.md](journal-exercices.md) | Tableau date / outil / MITRE |
| [preuves-red-team.md](preuves-red-team.md) | Corrélation avec captures SOC |
| `screenshots/04-soc/` | Preuves images |
| `screenshots/05-red-team/` | Captures Red Team (9 PNG) |

---

## 6. Pitch jury (30 s)

> « Depuis la VM 107 nous simulons un attaquant : reconnaissance nmap, brute-force SSH avec Hydra sur le portail, et tentatives sur l'AD. Chaque action est mappée MITRE ATT&CK et déclenche une alerte Wazuh **et** une signature Suricata dans eve.json — double détection logs + réseau. »
