# Structure du board Trello (ordre des listes)

```
1. 📌 Équipe & règles
2. Phase 0 — Cadrage (Oct–Nov)
3. Phase 1 — Infrastructure (Déc–Jan)
4. Phase 2 — SOC & Red Team (Fév–Mars)
5. Phase 3 — Automatisation (Avr–Mai)
6. Phase 4 — Tests & Livrables (Juin–Juil)
7. 🌐 Extension — Portail Audit (optionnel)
8. ✅ Terminé
```

## Swimlanes par membre (filtre labels)

- **E1-Infra** : Proxmox, VMs, topologie
- **E2-Réseau** : pfSense, AD, VPN, DMZ
- **E3-SOC** : Wazuh, Suricata, Grafana, TheHive, n8n
- **E4-RedTeam** : CALDERA, BloodHound, OpenVAS, portail

## Rituel hebdo (carte modèle en liste Équipe)

**Titre :** Réunion hebdo — semaine du __/__/2026

**Checklist :**
- [ ] Chaque membre : 2 min statut
- [ ] Bloquants identifiés
- [ ] 1 décision documentée dans TEAM.md
- [ ] Cartes Trello mises à jour

## Validation de phase (carte en fin de chaque liste)

**Titre :** ✅ Validation collective — Phase X

**Checklist :** reprendre [CHECKLIST.md](../../CHECKLIST.md) pour la phase concernée.
