# 06 — Automatisation & sauvegardes

**Responsable :** Étudiant 3 (Ansible) + Étudiant 1 (Proxmox backup)  
**Priorité globale :** P3  
**Dépôt :** [ansible/](../../ansible/)

**Prérequis :** Infra P1 stable, SOC agents manuels déjà OK (pour reproduire en playbook)

---

## P1 — Si le temps manque, faire au minimum

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 6.1 | Inventaire `ansible/inventory/hosts.yml` avec IP réelles des VMs | [ ] |
| 6.2 | Playbook **install agent Wazuh** sur hôte Linux (idempotent) | [ ] |
| 6.3 | Test `ansible-playbook ... --check` puis run réel sur 1 VM | [ ] |

---

## P2 — Important

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 6.4 | Playbook durcissement SSH (clés, PermitRootLogin no) sur docker-soc01 | [ ] |
| 6.5 | Playbook déploiement répertoire `soc/` + `docker compose up` (sans secrets dans repo) | [ ] |
| 6.6 | Variables sensibles via `ansible-vault` ou fichiers hors Git documentés | [ ] |
| 6.7 | **Test restore** snapshot Proxmox : créer VM test → snapshot → casser → restore | [ ] |
| 6.8 | Procédure restore config pfSense testée 1 fois | [ ] |
| 6.9 | Documenter fréquence sauvegardes (quotidien/hebdo) dans `docs/wiki/` | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 6.10 | `site.yml` orchestrant plusieurs playbooks | [ ] |
| 6.11 | Cron ou timer documenté pour backup | [ ] |

---

## Critères « automatisation validée »

- [ ] 1 playbook exécutable par un autre membre de l’équipe sans aide orale  
- [ ] 1 preuve de restore Proxmox ou pfSense  

**Ensuite :** [07-vpn-dmz-reverse-proxy.md](07-vpn-dmz-reverse-proxy.md)
