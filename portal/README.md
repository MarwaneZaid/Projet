# Portail Audit de Sécurité (extension)

**Responsable** : Étudiant 4 · **Support SOC/RT** : Étudiant 3

## Périmètre MVP (si le temps le permet)

### Espace client

- Authentification (email + mot de passe, ou OIDC plus tard)
- Commande / demande d’audit
- Devis simplifié (formulaire → statut « en attente »)
- Suivi statut projet
- Messagerie basique avec admin

### Espace admin

- Dashboard projets
- Validation devis
- Lien vers rapports Wazuh / exports OpenVAS (fichiers ou API read-only)

## Stack suggérée (à valider en équipe)

- **Frontend** : Next.js ou React + Vite
- **Backend** : API REST (Node ou FastAPI)
- **BDD** : PostgreSQL (Supabase ou conteneur local)
- **Auth** : sessions sécurisées ou Supabase Auth

## Statut

- [ ] Maquettes / wireframes
- [ ] Schéma BDD
- [ ] MVP auth + 1 parcours client
- [ ] Intégration rapport SOC (phase tardive)

Ne pas démarrer le portail avant validation Phase 1 infra (CHECKLIST).
