# 09 — Portail Audit de sécurité (extension)

**Responsable :** Étudiant 4  
**Support :** Étudiant 3 (intégration rapports SOC)  
**Priorité globale :** P5 — **optionnel** (seulement si P1–P2 terminés)  
**Dépôt :** [portal/](../../portal/)

**Prérequis :** SOC opérationnel, maquettes validées par l’équipe

---

## P1 — MVP minimum (si vous tentez l’extension)

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 9.1 | Maquettes Figma ou wireframes (client + admin) | [ ] |
| 9.2 | Schéma BDD : users, projects, quotes, messages | [ ] |
| 9.3 | Stack choisie et documentée (ex. Next.js + PostgreSQL) | [ ] |
| 9.4 | **Auth** : inscription/login sécurisé (hash bcrypt, sessions) | [ ] |
| 9.5 | Espace **client** : formulaire demande d’audit + statut « en attente » | [ ] |
| 9.6 | Espace **admin** : liste des demandes + changement de statut | [ ] |

---

## P2 — Important

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 9.7 | Messagerie simple client ↔ admin | [ ] |
| 9.8 | Devis automatisé (calcul simplifié ou PDF généré) | [ ] |
| 9.9 | Lien téléchargement rapport scan OpenVAS (fichier statique lab) | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 9.10 | Dashboard admin avec métriques SOC (iframe Grafana ou capture) | [ ] |
| 9.11 | Déploiement conteneurisé du portail en DMZ derrière reverse proxy | [ ] |

---

## Critères « portail validé » (extension)

- [ ] 1 parcours client complet démontré en soutenance  
- [ ] Pas de faille évidente (SQLi, mots de passe clairs)  
- [ ] Code dans `portal/` avec README install  

> Si le temps manque : mentionner le portail comme **perspective** dans le rapport sans l’implémenter.
