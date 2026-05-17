# API OVH — authentification (pour scripts du projet)

L’API permet de **lire** les infos du serveur (IP, modèle, RAM…) et de les mettre dans `specs-materiel.md`.  
Elle **n’installe pas** Proxmox à votre place : l’install reste via KVM / ISO.

**Endpoint Europe :** `https://eu.api.ovh.com/1.0`

---

## Ce que vous faites (une fois, ~5 min)

### Étape A — Créer une application API

1. Allez sur **[https://eu.api.ovh.com/createApp/](https://eu.api.ovh.com/createApp/)** (connecté avec le compte OVH du serveur).
2. Remplissez :
   - **Application name :** `projet-soc-lab`
   - **Description :** Projet école mini-cloud
   - **Application URL :** `https://github.com/MarwaneZaid/Projet`
3. Validez → vous recevez :
   - **Application Key** (`AK_...`)
   - **Application Secret** (`...` longue chaîne)

Gardez-les : ce sont `OVH_APPLICATION_KEY` et `OVH_APPLICATION_SECRET`.

### Étape B — Générer le Consumer Key (autorisation)

Dans le terminal, à la racine du projet :

```bash
cd ~/Desktop/Projet
pip3 install ovh    # une seule fois

export OVH_APPLICATION_KEY="votre_application_key"
export OVH_APPLICATION_SECRET="votre_application_secret"

python3 scripts/ovh_create_consumer_key.py
```

Le script affiche une **URL**. Ouvrez-la dans le navigateur → connectez-vous OVH → **Autoriser** → copiez le **Consumer Key** affiché.

### Étape C — Fichier `.env` local (jamais sur GitHub)

```bash
cp ovh.env.example .env
# Éditer .env avec les 3 valeurs + endpoint
```

Contenu type :

```env
OVH_ENDPOINT=ovh-eu
OVH_APPLICATION_KEY=xxxxx
OVH_APPLICATION_SECRET=xxxxx
OVH_CONSUMER_KEY=xxxxx
```

`.env` est déjà dans `.gitignore`.

### Étape D — Tester

```bash
python3 scripts/ovh_fetch_server.py
```

Vous devez voir : compte `/me`, liste VPS ou serveurs dédiés, IP, etc.

---

## Ce que l’agent (Cursor) peut faire ensuite

Si les variables sont dans **votre** `.env` local et que vous lancez les scripts (ou me donnez accès terminal avec `.env` chargé), je peux :

- Remplir automatiquement les champs de [specs-materiel.md](../architecture/specs-materiel.md)
- Lister `/dedicated/server` ou `/vps`
- Vérifier `/me/api/credential`

**Ne collez pas** Application Secret ni Consumer Key dans le chat Cursor.

---

## Droits API recommandés (sécurité)

Pour le projet, **lecture seule** suffit au début :

| Méthode | Chemin | Usage |
|---------|--------|--------|
| GET | `/*` | Infos serveur, IP, état |

Le script `ovh_create_consumer_key.py` demande seulement **GET** par défaut.  
Pour reboot / réinstall via API plus tard : droits élargis (à discuter en équipe).

---

## Routes utiles (celles que vous avez vues)

| Route | Contenu |
|-------|---------|
| `GET /me` | Compte OVH |
| `GET /me/api/credential` | Apps API liées |
| `GET /dedicated/server` | Liste serveurs dédiés |
| `GET /vps` | Liste VPS |
| `GET /hosting/web` | Hébergements web (hors scope si pas utilisé) |

---

## Dépannage

| Erreur | Cause | Solution |
|--------|-------|----------|
| `401` | Consumer key invalide ou expiré | Refaire étape B |
| `403` | Droits insuffisants | Regénérer consumer key avec bonnes `accessRules` |
| `404` sur `/dedicated/server` | Vous avez un VPS, pas un dédié | Le script essaie aussi `/vps` |
| `ModuleNotFoundError: ovh` | Paquet absent | `pip3 install ovh` |

---

## Liens officiels

- [Créer une application (EU)](https://eu.api.ovh.com/createApp/)
- [Documentation API OVH](https://eu.api.ovh.com/console/?section=%2Fme&branch=v1)
