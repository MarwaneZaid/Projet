# 05 — Red Team (attaques simulées)

**Responsable :** Étudiant 4 (profil réseau → rôle sécurité)  
**Relecteur :** Étudiant 3  
**Priorité globale :** P2  
**Dépôt :** [redteam/](../../redteam/)

**Prérequis :** Segment **LAB-RT isolé** (aucune route vers LAN prod), accord encadrant (0.12), AD lab ou honeypots dédiés

> **Règle absolue :** jamais d’attaque sur le réseau campus, comptes réels, ou VMs production hors lab.

---

## P0 — Bloquant (sécurité)

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 5.1 | Segment réseau **192.168.99.0/24** (ou plage validée) sans routage vers LAN | Test routage documenté | [ ] |
| 5.2 | VMs cibles = **uniquement** lab RT + honeypots | Liste VMs dans rapport | [ ] |
| 5.3 | Journal d’exercice : modèle date / outil / cible / résultat | `docs/livrables/redteam/journal-exercices.md` | [ ] |

---

## P1 — Critique

| # | Tâche exacte | Détail | Validé |
|---|--------------|--------|--------|
| 5.4 | Déployer **OpenVAS** (Docker ou VM lab) | Scan uniquement IP lab | [ ] |
| 5.5 | Scan OpenVAS cible lab → rapport export PDF/HTML | Stocké dans `docs/livrables/redteam/` | [ ] |
| 5.6 | **BloodHound** : install collector + import sur AD **lab** | Capture chemins d’attaque | [ ] |
| 5.7 | **CALDERA** : déploiement + 1 agent sur VM lab | Campagne « discovery » sans exfil réelle | [ ] |
| 5.8 | **Scénario 1** : brute force sur **honeypot** SSH/RDP (pas vrai AD prod) | Rapport 1–2 pages | [ ] |
| 5.9 | **Scénario 2** : énumération AD lab (sans modification GPO prod) | Rapport 1–2 pages | [ ] |
| 5.10 | Pour chaque scénario : lister **IOC, TTP (MITRE)** et heure exacte | Tableau dans rapport | [ ] |
| 5.11 | Vérifier avec Étudiant 3 : **alerte Wazuh** correspondante | Capture alerte + lien scénario | [ ] |

---

## P2 — Important

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 5.12 | Scénario 3 optionnel : scan Nmap + corrélation Suricata | [ ] |
| 5.13 | Recommandations de remédiation par finding OpenVAS | [ ] |

---

## P3 — Utile (backlog avancé)

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 5.14 | Zero Trust avancé (micro-segmentation) — étude documentaire | [ ] |
| 5.15 | Campagne CALDERA plus complexe (lateral movement simulé en lab) | [ ] |

---

## Critères « Red Team validé »

- [ ] 2 scénarios documentés + corrélés SOC  
- [ ] OpenVAS + BloodHound livrables dans le repo (sans données sensibles)  
- [ ] Aucun incident réel / plainte réseau école  
- [ ] Relecture Étudiant 3 OK  

**Ensuite :** [06-automatisation-ansible.md](06-automatisation-ansible.md), [08-livrables-rapport.md](08-livrables-rapport.md)
