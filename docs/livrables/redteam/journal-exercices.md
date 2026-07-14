# Journal des exercices Red Team — NexaMind

> **Machine attaque :** VM 107 `srv-soc-1` · `192.168.20.18`  
> **Règle :** cibles **uniquement** sur `192.168.20.0/24` (lab). Jamais IP publique OVH, campus, Internet.

| Date | Scénario | Outil | Source → Cible | TTP MITRE | Alerte SOC | Auteur |
|------|----------|-------|----------------|-----------|------------|--------|
| 2026-06-19 20:09 | RT-02 Port scan | nmap | 107 → `.20` portail | T1046 | ✅ Wazuh port scan | Marwane |
| 2026-06-19 20:09 | RT-01 Brute-force SSH | ssh loop | 107 → `.20` portail | T1110.001 | ✅ Wazuh 5710/5712 | Marwane |
| 2026-06-19 20:15 | RT-03 Failed logon AD | ssh loop | 107 → `.16` AD | T1110.001, T1078 | ✅ Wazuh sshd 5710 | Marwane |
| 2026-07-10 21:51 | RT-02 Port scan | nmap 7.95 | 107 → `.20` | T1046 | ✅ (relance démo) | Marwane |
| 2026-07-10 21:51 | RT-01 Brute-force SSH | ssh x10 | 107 → `.20` | T1110.001 | ✅ (relance démo) | Marwane |
| 2026-07-10 21:52 | RT-03 Failed logon AD | ssh x12 | 107 → `.16` | T1110.001, T1078 | ✅ (relance démo) | Marwane |
| 2026-07-14 23:26 | RT-02 Port scan | nmap 7.95 | 107 → `.20` | T1046 | ✅ ports 22,80 | Marwane |
| 2026-07-14 23:26 | RT-01 Brute-force SSH | ssh x10 | 107 → `.20` | T1110.001 | ✅ à vérifier Wazuh | Marwane |
| 2026-07-14 23:26 | RT-03 Failed logon AD | ssh x12 | 107 → `.16` | T1110.001, T1078 | ✅ à vérifier Wazuh | Marwane |
| 2026-07-14 23:40 | RT-01 Brute-force SSH | **Hydra** x10 | 107 → `.20` | T1110.001 | ✅ Wazuh + Suricata | Marwane |
| 2026-07-15 00:02 | RT-01/02/03 + captures manuelles | Hydra + nmap + Suricata sid 900000x | 107 → `.20`/`.16` | T1046, T1110.001 | ✅ double détection + PNG | Marwane |

## Détail des scénarios

### RT-01 — Brute-force SSH (portail)

| Champ | Valeur |
|-------|--------|
| Objectif | Simuler un attaquant qui teste des identifiants SSH sur le portail |
| Commande | `~/redteam/bruteforce-ssh.sh 192.168.20.20` |
| Outil | **Hydra** (`-l attacker-demo -P /tmp/rt01-wordlist.txt -t 4`) |
| IOC | Multiples connexions SSH échouées depuis `.18` vers `.20` |
| Preuve SOC | `04-soc_wazuh-alerte-ssh-bruteforce.png`, `05-red-team_suricata-eve-alerts.png` (sid 9000002) |

### RT-02 — Port scan (reconnaissance)

| Champ | Valeur |
|-------|--------|
| Objectif | Phase reconnaissance MITRE avant exploitation |
| Commande | `~/redteam/scan-nmap.sh 192.168.20.20` |
| IOC | Scan TCP ports depuis `.18` |
| Preuve SOC | `04-soc_attaque-nmap-termine.png`, `04-soc_wazuh-alerte-port-scan.png` |
| Bonus IDS | `sudo tail -f /var/log/suricata/eve.json` sur VM 107 |

### RT-03 — Tentatives SSH vers AD

| Champ | Valeur |
|-------|--------|
| Objectif | Simuler attaque sur le contrôleur de domaine |
| Commande | `~/redteam/failed-logon-ad.sh 192.168.20.16` |
| IOC | SSH failed logons sur `srv-ad-1` |
| Preuve SOC | `04-soc_wazuh-alerte-ad-failed-logon.png` |

## Corrélation Red Team ↔ SOC

| Étape attaquant | Détection attendue | Outil défense |
|-----------------|-------------------|---------------|
| nmap | Alerte scan / recon | Wazuh + Suricata sid 9000001 |
| SSH brute-force (Hydra) | Règle 5710, 5712 | Wazuh agent portail + Suricata sid 9000002 |
| SSH vers AD | Règle sshd 5710 | Wazuh agent AD |
| (futur) logon AD Windows | Event 4625 | Wazuh agent Windows + audit Samba |

## Relancer les exercices

```bash
ssh nexa@192.168.20.18
bash ~/redteam/run-all.sh
```

Depuis le repo (Mac, VPN) :

```bash
bash scripts/redteam/deploy-to-vm107.sh
```

## Hors périmètre (non fait — backlog)

- Segment isolé `192.168.99.0/24` (CALDERA / OpenVAS lourd)
- BloodHound sur AD peuplé (dépend Jacques)
- OpenVAS rapport PDF
