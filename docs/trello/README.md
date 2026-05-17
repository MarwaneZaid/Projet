# Tableau Trello — Projet

**Board :** [trello.com/b/uPZIvZwK/projet](https://trello.com/b/uPZIvZwK/projet)

Le board est **privé** : l’agent ne peut pas y ajouter des cartes sans vos identifiants. Deux options ci-dessous.

## Option A — Import automatique (recommandé)

1. Créer une clé API : [trello.com/app-key](https://trello.com/app-key)
2. Générer un **token** (lien sur la même page, droits `read,write`)
3. Exporter les variables et lancer le script :

```bash
cd /Users/skat/Desktop/Projet
export TRELLO_API_KEY="votre_cle"
export TRELLO_TOKEN="votre_token"
python3 scripts/trello_import.py
```

Le script crée les **listes**, **labels** et **cartes** (avec dates d’échéance et descriptions).

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
