# 03 — Active Directory

**Responsable :** Étudiant 2  
**Relecteur :** Étudiant 3 (pour partie logs SOC)  
**Priorité globale :** P1  
**Dépôt :** [infra/active-directory/](../../infra/active-directory/)

**Prérequis :** pfSense LAN opérationnel (P1), décision Samba vs Windows (tâche 0.5)

---

## P0 — Bloquant

| # | Tâche exacte | Samba AD | Windows Server |
|---|--------------|----------|----------------|
| 3.1 | Installer le rôle contrôleur de domaine | `samba-ad-dc` ou équivalent | Promote Server + AD DS |
| 3.2 | Créer le domaine (ex. `lab.local` ou nom validé école) | `realm` / provision | Configure AD |
| 3.3 | Vérifier résolution DNS du domaine depuis une VM cliente | `nslookup lab.local` OK | Idem |

---

## P1 — Critique

| # | Tâche exacte | Détail | Validé |
|---|--------------|--------|--------|
| 3.4 | Créer OU : `Users`, `Servers`, `Workstations`, `ServiceAccounts` | Structure claire dans ADUC / samba-tool | [ ] |
| 3.5 | Créer groupes : `Domain Admins` (restreint), `IT-Admins`, `Lab-Users` | Pas tout le monde admin | [ ] |
| 3.6 | Créer **10 utilisateurs de test** minimum (noms réalistes) | CSV ou script documenté | [ ] |
| 3.7 | GPO : **politique mots de passe** (longueur, complexité) | 1 GPO liée au domaine | [ ] |
| 3.8 | GPO : **audit connexions** (succès/échec logon) | Event ID 4624/4625 visibles | [ ] |
| 3.9 | Joindre **2 postes clients** (VM Windows) au domaine | Login domaine OK | [ ] |
| 3.10 | Compte de service **wazuh-agent** (lecture logs, pas admin domaine) | Mot de passe dans coffre local, pas Git | [ ] |
| 3.11 | Configurer forward des **logs sécurité** vers collecteur (IP Wazuh quand prêt) | Syslog ou agent ; doc dans `docs/procedures/ad-logs-soc.md` | [ ] |

---

## P2 — Important

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 3.12 | 1 GPO test supplémentaire (ex. fond d’écran, verrouillage session) | [ ] |
| 3.13 | Export procédure « créer utilisateur + ajouter au groupe » | [ ] |
| 3.14 | Capture d’écran OU + GPO pour le rapport | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 3.15 | Intégration BloodHound plus tard : note sur compte collecte (lecture seule) | [ ] |

---

## Critères « AD validé »

- [ ] Login domaine sur 2 clients  
- [ ] GPO audit visible dans Event Viewer  
- [ ] Compte agent Wazuh créé  
- [ ] Étudiant 3 confirme que les logs sont exploitables pour Wazuh  

**Ensuite :** [04-soc.md](04-soc.md) — agents sur le DC
