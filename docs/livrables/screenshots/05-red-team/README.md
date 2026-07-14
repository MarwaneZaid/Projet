# Captures Red Team — 15/07/2026

Captures **manuelles** terminal VM 107 (`nexa@192.168.20.18`).

| Fichier | Scénario | Explication courte |
|---------|----------|-------------------|
| [05-red-team_scan-nmap-result.png](05-red-team_scan-nmap-result.png) | RT-02 | nmap découvre ports **22** et **80** sur le portail |
| [05-red-team_bruteforce-ssh-done.png](05-red-team_bruteforce-ssh-done.png) | RT-01 | Script + **Hydra** : 10 tentatives, 0 succès |
| [05-red-team_hydra-commande-detail.png](05-red-team_hydra-commande-detail.png) | RT-01 | Zoom Hydra seul (bonus annexe) |
| [05-red-team_failed-logon-ad-done.png](05-red-team_failed-logon-ad-done.png) | RT-03 | SSH échoué vers AD `.16` |
| [05-red-team_terminal-run-all.png](05-red-team_terminal-run-all.png) | Tous | `run-all.sh` : RT-02 → RT-01 → RT-03 |
| [05-red-team_suricata-eve-alerts.png](05-red-team_suricata-eve-alerts.png) | SOC | Signatures **NEXAMIND LAB** sid 9000001–9000003 |
| [05-red-team_suricata-eve-flows.png](05-red-team_suricata-eve-flows.png) | SOC | Flows TCP scan + SSH `.18` → `.20` |
| 05-red-team_wazuh-alerts-after-attack.png | SOC | *(auto — à refaire manuellement)* |
| 05-red-team_vm107-attacker-overview.png | Infra | *(auto — à refaire manuellement)* |
| 05-rt_journal-exercice.png | Doc | *(auto — à refaire manuellement)* |
| 05-rt_correlation-soc.png | Doc | *(auto — à refaire manuellement)* |

Légende complète : [preuves-red-team.md](../../redteam/preuves-red-team.md)
