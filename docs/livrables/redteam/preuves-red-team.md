# Red Team NexaMind — preuves et corrélation SOC

> Complément du [journal-exercices.md](journal-exercices.md) · Captures dans `docs/livrables/screenshots/04-soc/`

## Périmètre validé (MVP)

| Critère | Statut |
|---------|--------|
| 3 scénarios d'attaque documentés | ✅ |
| TTP MITRE renseignés | ✅ |
| Alerte Wazuh correspondante | ✅ |
| Machine attaque identifiée (VM 107) | ✅ |
| Cibles = lab `192.168.20.x` uniquement | ✅ |

## Tableau de corrélation (soutenance)

| # | Attaque (Red Team) | Heure | Détection (Blue Team) | Capture |
|---|-------------------|-------|----------------------|---------|
| 1 | nmap top ports → `.20` | 15/07 00:02 | Wazuh recon + Suricata 9000001 | [scan-nmap](../screenshots/05-red-team/05-red-team_scan-nmap-result.png) |
| 2 | Hydra SSH failed → `.20` | 15/07 00:03 | Wazuh 5710/5712 + Suricata 9000002 | [bruteforce](../screenshots/05-red-team/05-red-team_bruteforce-ssh-done.png), [alertes](../screenshots/05-red-team/05-red-team_suricata-eve-alerts.png) |
| 3 | SSH failed → `.16` AD | 15/07 00:02 | Wazuh sshd 5710 + Suricata 9000003 | [failed-ad](../screenshots/05-red-team/05-red-team_failed-logon-ad-done.png) |

## Captures Red Team (`05-red-team/` — **captures manuelles 15/07/2026**)

| Fichier | Scénario | Contenu |
|---------|----------|---------|
| [05-red-team_scan-nmap-result.png](../screenshots/05-red-team/05-red-team_scan-nmap-result.png) | RT-02 | nmap ports 22, 80 |
| [05-red-team_bruteforce-ssh-done.png](../screenshots/05-red-team/05-red-team_bruteforce-ssh-done.png) | RT-01 | Hydra 10 tentatives |
| [05-red-team_hydra-commande-detail.png](../screenshots/05-red-team/05-red-team_hydra-commande-detail.png) | RT-01 | Hydra commande seule (bonus) |
| [05-red-team_failed-logon-ad-done.png](../screenshots/05-red-team/05-red-team_failed-logon-ad-done.png) | RT-03 | SSH vers AD `.16` |
| [05-red-team_terminal-run-all.png](../screenshots/05-red-team/05-red-team_terminal-run-all.png) | Tous | Enchaînement run-all |
| [05-red-team_suricata-eve-alerts.png](../screenshots/05-red-team/05-red-team_suricata-eve-alerts.png) | SOC | Alertes IDS NEXAMIND LAB |
| [05-red-team_suricata-eve-flows.png](../screenshots/05-red-team/05-red-team_suricata-eve-flows.png) | SOC | Flows TCP `.18` → `.20` |
| [05-red-team_wazuh-alerts-after-attack.png](../screenshots/05-red-team/05-red-team_wazuh-alerts-after-attack.png) | SOC | Wazuh post-attaque (auto) |
| [05-red-team_vm107-attacker-overview.png](../screenshots/05-red-team/05-red-team_vm107-attacker-overview.png) | Infra | VM 107 (auto) |
| [05-rt_journal-exercice.png](../screenshots/05-red-team/05-rt_journal-exercice.png) | Doc | Journal MITRE (auto) |
| [05-rt_correlation-soc.png](../screenshots/05-red-team/05-rt_correlation-soc.png) | Doc | Corrélation (auto) |

### Légende détaillée — ce que montre chaque capture

#### 1. `05-red-team_scan-nmap-result.png` — RT-02 Reconnaissance

**Commande :** `bash ~/redteam/scan-nmap.sh 192.168.20.20`  
**Heure :** 14/07/2026 23:59:07 CEST

| Élément visible | Signification |
|-----------------|---------------|
| Bannière `RT-02 Port scan (nmap)` | Scénario reconnaissance MITRE **T1046** |
| Source `192.168.20.18` | VM 107 = poste attaquant |
| Cible `192.168.20.20` | Portail NexaMind |
| `22/tcp open ssh` + `80/tcp open http` | Services découverts → vecteurs d'attaque |
| `Fin RT-02` + lien Suricata | Passage à la vérification SOC |

**Storytelling jury :** *« Phase reconnaissance : l'attaquant identifie SSH et HTTP avant d'exploiter. »*

---

#### 2. `05-red-team_bruteforce-ssh-done.png` — RT-01 Brute-force Hydra

**Commande :** `bash ~/redteam/bruteforce-ssh.sh 192.168.20.20`  
**Heure :** 14/07/2026 23:59:59 → 15/07 00:00:08 CEST

| Élément visible | Signification |
|-----------------|---------------|
| `MITRE : T1110.001` | Brute Force: Password Guessing |
| `hydra -l attacker-demo -P /tmp/rt01-wordlist.txt … -t 4 -f -V` | Outil pro (pas une boucle ssh artisanale) |
| 10 lignes `[ATTEMPT]` | Wordlist lab, mots de passe fictifs |
| `0 valid password found` | Attaque échouée (comportement attendu) |
| Note Wazuh 5710/5712 | Détection côté logs sur `srv-web-1` |

**Storytelling jury :** *« Hydra simule un vrai attaquant qui teste des identifiants SSH — Wazuh voit les échecs dans auth.log. »*

---

#### 3. `05-red-team_hydra-commande-detail.png` — RT-01 zoom Hydra (bonus)

**Commande :** `hydra -l attacker-demo -P /tmp/rt01-wordlist.txt ssh://192.168.20.20 -t 4 -f -V`  
**Heure :** 15/07/2026 00:01:46 → 00:01:56 CEST

Capture **focus** sur la sortie Hydra seule (sans bannière script). Utile en annexe ou slide « outil utilisé ».

---

#### 4. `05-red-team_failed-logon-ad-done.png` — RT-03 Attaque AD

**Commande :** `bash ~/redteam/failed-logon-ad.sh 192.168.20.16`  
**Heure :** 15/07/2026 00:02:24 → 00:02:37 CEST

| Élément visible | Signification |
|-----------------|---------------|
| Cible `192.168.20.16` (srv-ad-1) | Contrôleur de domaine Samba AD |
| MITRE **T1110.001** + **T1078** | Brute force + Valid Accounts |
| Utilisateurs testés | `administrator`, `fakeuser`, `attacker-demo`, `guest` |
| Note Wazuh `srv-ad-1` rule 5710 | Alerte attendue sur l'agent AD |

**Storytelling jury :** *« Après le portail, l'attaquant cible l'AD — même technique, autre machine critique. »*

---

#### 5. `05-red-team_terminal-run-all.png` — Enchaînement complet

**Commande :** `PAUSE=2 bash ~/redteam/run-all.sh`  
**Heure :** 15/07/2026 00:02:56 → 00:03:20 CEST

| Élément visible | Signification |
|-----------------|---------------|
| `RED TEAM NEXAMIND` | Orchestrateur des 3 scénarios |
| RT-02 nmap → RT-01 Hydra → RT-03 AD | Kill chain complète en ~30 s |
| Fin RT-03 + lien Wazuh `.22` | Boucle attaque → vérification SOC |
| `show-suricata-alerts.sh` en fin | Double détection réseau + logs |

**Storytelling jury :** *« Un seul script enchaîne reconnaissance, exploitation et pivot AD — démo reproductible. »*

---

#### 6. `05-red-team_suricata-eve-alerts.png` — Alertes IDS (signatures)

**Commande :** `bash ~/redteam/show-suricata-alerts.sh`

| Signature (sid) | Déclenchée par |
|-----------------|----------------|
| **NEXAMIND LAB TCP Port Scan** (9000001) | nmap RT-02 |
| **NEXAMIND LAB SSH Brute Force (Hydra)** (9000002) | Hydra RT-01 |
| **NEXAMIND LAB SSH Login Attempts AD** (9000003) | RT-03 vers `.16` |
| SURICATA SSH invalid banner | Trafic SSH anormal Hydra |

**Storytelling jury :** *« Suricata ne voit pas que des flows : de vraies signatures IDS dans eve.json, en plus de Wazuh. »*

---

#### 7. `05-red-team_suricata-eve-flows.png` — Flows réseau

**Commande :**
```bash
grep '"dest_ip":"192.168.20.20"' /var/log/suricata/eve.json | \
  grep '"src_ip":"192.168.20.18"' | tail -8
```

| Élément visible | Signification |
|-----------------|---------------|
| `"event_type":"flow"` | Connexions TCP enregistrées |
| Ports variés (9, 5000, 199…) | Traces du scan nmap |
| `"dest_port":22`, `"app_proto":"ssh"` | Sessions SSH Hydra vers le portail |
| `"state":"closed"` | Connexions terminées (échecs auth) |

**Storytelling jury :** *« Même sans signature, Suricata trace le trafic attaquant → cible dans eve.json. »*

---

#### 8–11. Captures restantes (auto — à refaire manuellement si besoin)

| Fichier | Statut | Action |
|---------|--------|--------|
| `05-red-team_wazuh-alerts-after-attack.png` | Auto (14/07) | Ouvrir `https://192.168.20.22` → capture alertes 5710 |
| `05-red-team_vm107-attacker-overview.png` | Auto (14/07) | Terminal : `hostname`, `systemctl is-active suricata` |
| `05-rt_journal-exercice.png` | Auto (14/07) | Capture `journal-exercices.md` dans Cursor |
| `05-rt_correlation-soc.png` | Auto (14/07) | Montage attaque + Wazuh même heure |

Regénérer les 4 auto : `python3 scripts/redteam/generate-redteam-screenshots.py`  
**Guide pas à pas :** [guide-captures-red-team.md](guide-captures-red-team.md)

## Chaîne démo jury (5 min)

1. Montrer VM 107 = poste attaquant (`192.168.20.18`)
2. Lancer `bash ~/redteam/run-all.sh`
3. Wazuh `.22` → nouvelles alertes
4. (Bonus) Suricata `eve.json` pendant RT-02
5. Portail `.20` → alerte remontée (Victor)

## Scripts

| Script | Rôle |
|--------|------|
| `scripts/redteam/run-all.sh` | Enchaîne les 3 scénarios |
| `scripts/redteam/bruteforce-ssh.sh` | RT-01 (Hydra) |
| `scripts/redteam/show-suricata-alerts.sh` | Démo alertes IDS |
| `scripts/redteam/install-suricata-lab-rules.sh` | Règles sid 9000001–9000003 |
| `scripts/redteam/scan-nmap.sh` | RT-02 |
| `scripts/redteam/failed-logon-ad.sh` | RT-03 |
| `scripts/redteam/deploy-to-vm107.sh` | Sync vers VM 107 |
| `scripts/redteam/generate-redteam-screenshots.py` | Génère PNG `05-red-team/` |

## Évolutions (note max)

- [ ] OpenVAS scan + rapport HTML
- [ ] BloodHound après peuplement AD
- [ ] Segment `192.168.99.0/24` dédié Red Team
