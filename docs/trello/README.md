# Tableau Trello — Projet

**Board :** [trello.com/b/uPZIvZwK/projet](https://trello.com/b/uPZIvZwK/projet)

Le board est **privé** : l’agent ne peut pas y ajouter des cartes sans vos identifiants. Deux options ci-dessous.

## Option A — Enrichir le board actuel (recommandé)

Votre board utilise déjà le Kanban : Backlog → To Do → In Progress → Review → Done → Rapport.

1. Ouvrir [trello.com/app-key](https://trello.com/app-key) (compte **Marwane Zaid** ou celui qui possède le board)
2. Copier la **API Key** (longue chaîne alphanumérique)
3. Sur la même page, cliquer le lien **Token** → autoriser → copier le token affiché (une seule fois visible)
4. Lancer en remplaçant par vos **vraies** valeurs :

```bash
cd ~/Desktop/Projet
git pull
export TRELLO_API_KEY="abc123...votre_vraie_cle"
export TRELLO_TOKEN="ATT...votre_vrai_token"
python3 scripts/trello_enrich_kanban.py
```

> Erreur `401 Unauthorized` = clé ou token invalide, ou vous avez laissé `votre_cle` / `votre_token` (texte d'exemple).

Ce script **complète les checklists** des cartes existantes (SOC, AD, pfSense, Red Team…), ajoute des descriptions et des cartes dans le Backlog — **sans casser** votre structure.

## Option B — Board par phases (nouveau board vide)

```bash
python3 scripts/trello_import.py
```

Crée des listes par phase (Oct–Juil) avec ~70 cartes datées.

## Option B — Import manuel rapide

1. Ouvrir le board Trello connecté
2. Créer les listes dans l’ordre de [structure-board.md](structure-board.md)
3. Copier-coller les cartes depuis [cartes-par-liste.md](cartes-par-liste.md) ou importer le CSV avec un power-up « CSV Import »

## Labels à créer sur Trello

| Label | Couleur | Usage |
|-------|---------|--------|
| E1-Infra | vert | Étudiant 1 |
| E2-Réseau | bleu | Étudiant 2 |
| E3-SOC | violet | Étudiant 3 |
| E4-RedTeam | rouge | Étudiant 4 |
| Livrable | jaune | Remise rapport / démo |
| Bloquant | rouge foncé | Dépendance critique |
| Optionnel | gris | Extension portail |

## Calendrier (année scolaire)

| Phase | Période | Date limite cartes |
|-------|---------|-------------------|
| 0 Cadrage | Oct – Nov 2025 | 30/11/2025 |
| 1 Infra | Déc – Jan 2026 | 31/01/2026 |
| 2 SOC / RT | Fév – Mars 2026 | 31/03/2026 |
| 3 Auto | Avr – Mai 2026 | 31/05/2026 |
| 4 Livrables | Juin – Juil 2026 | 15/07/2026 |

> En mai 2026 : prioriser les cartes **non cochées** des phases 1–3, puis phase 4.
