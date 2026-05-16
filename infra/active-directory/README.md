# Active Directory

## Choix à acter (Phase 0)

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **Samba AD** | Léger, gratuit, suffisant pour GPO de base | Moins « entreprise » qu’un vrai Windows |
| **Windows Server** | GPO complètes, outils Microsoft | RAM + licence |

## Contenu minimum

- [ ] Domaine : `lab.local` ou nom validé par l’école
- [ ] OU : Users, Servers, Workstations, ServiceAccounts
- [ ] Groupes : Domain Admins (restreint), SOC-Readers, Lab-Users
- [ ] GPO : audit connexions, politique mots de passe
- [ ] Compte dédié agent Wazuh (lecture logs)
- [ ] Au moins 2 postes clients joint au domaine (VM)

## Intégration SOC

- Forward Windows Event Log / Samba logs vers collecteur
- Documenter ports et comptes dans `docs/procedures/ad-logs-soc.md` (à créer)
