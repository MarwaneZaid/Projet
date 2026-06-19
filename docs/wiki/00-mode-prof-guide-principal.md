# Guide pédagogique — mode « prof »

Ce dossier explique **comment faire**, **pourquoi**, et **quelle capture d'écran prendre** à chaque étape clé.

## Captures d'écran (obligatoire pour le rapport)

Pour **chaque** étape : lire dans [screenshots-par-etape.md](screenshots-par-etape.md) :

1. **Où chercher** (menu Proxmox, Manager OVH, Terminal…)
2. **Comment** prendre la capture (Mac `Cmd+Shift+3/4`)
3. **Quoi montrer** sur l'image
4. **Nom du fichier** + **dossier** (`docs/livrables/screenshots/01-proxmox/` …)


| Règle          | Détail                                                    |
| -------------- | --------------------------------------------------------- |
| **Quand**      | Juste après l'étape réussie                               |
| **Où stocker** | Sous-dossier par leçon dans `docs/livrables/screenshots/` |
| **Interdit**   | Mots de passe, clés privées, `.env`                       |


Chaque leçon du wiki indique aussi **📸** les captures minimales.

---

## Ordre des leçons


| #   | Leçon                 | Fichier                                                                      | Captures                                                                              | Quand              |
| --- | --------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------ |
| 0   | Accès serveur         | [../infra/02-premier-acces-proxmox.md](../infra/02-premier-acces-proxmox.md) | [§ Leçon 0](screenshots-par-etape.md#leçon-0--accès-serveur-déjà-fait-ou-à-compléter) | Fait / à compléter |
| 1   | Créer les VMs Proxmox | [01-proxmox-creer-vms.md](01-proxmox-creer-vms.md)                           | [§ Leçon 1](screenshots-par-etape.md#leçon-1--proxmox--créer-les-vms)                 | **Maintenant**     |
| 2   | pfSense               | [02-pfsense-installation.md](02-pfsense-installation.md)                     | [§ Leçon 2](screenshots-par-etape.md#leçon-2--pfsense-à-faire)                        | Après VMs          |
| 3   | Active Directory      | *(à rédiger)*                                                                | [§ Leçon 3](screenshots-par-etape.md#leçon-3--active-directory-à-faire)               | Après pfSense      |
| 4   | MVP SOC (seulement)   | [README-SOC-GUIDE-COMPLET.md](README-SOC-GUIDE-COMPLET.md) · [04-mvp-soc-runbook-unifie.md](04-mvp-soc-runbook-unifie.md) | [§ Leçon 4](screenshots-par-etape.md#leçon-4--mvp-soc-seulement)                       | Après AD           |
| 5   | Red Team              | *(à rédiger)*                                                                | [§ Leçon 5](screenshots-par-etape.md#leçon-5--red-team-à-faire)                       | Après SOC          |


---

## Méthode de travail (4 étapes)

1. Lire la leçon.
2. Faire l'action sur le serveur / Proxmox.
3. **📸 Prendre la capture** indiquée → enregistrer dans `docs/livrables/screenshots/`.
4. Cocher `docs/taches/` + passer à l'étape suivante.

---

## Rôle des 4 étudiants (rappel)

- **Étudiant 1** : Proxmox, VMs, stockage
- **Étudiant 2** : pfSense, AD
- **Étudiant 3** : SOC Docker
- **Étudiant 4** : Red Team (lab isolé)

Répartition : [../taches/repartition-detaillee-equipe.md](../taches/repartition-detaillee-equipe.md)