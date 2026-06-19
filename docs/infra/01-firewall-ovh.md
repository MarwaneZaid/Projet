# Étape 1 — Firewall réseau OVH (obligatoire)

Sans cette étape, **SSH (22)** et **Proxmox (8006)** restent inaccessibles depuis l’extérieur.

## Où aller

1. [Manager OVH](https://manager.eu.ovhcloud.com/) → **Bare Metal Cloud** → **Network** → **IP**
2. Cliquer sur **51.77.52.56**
3. Onglet **Firewall réseau** (Edge Network Firewall)
4. **Activer** le firewall si désactivé

## Règles recommandées (IPv4)

Remplacer `VOTRE_IP_PUBLIQUE` par l’IP de chaque membre (trouver sur [whatismyip.com](https://www.whatismyip.com/)).

**IP détectée depuis votre connexion (mai 2026) :** `46.193.6.82` — à utiliser dans les règles si c’est bien votre box/école.

Automatisation API (si `.env` rempli) :

```bash
pip3 install ovh
python3 scripts/ovh_configure_firewall.py --allow 46.193.6.82
```


| Priorité | Action    | Protocole | Port src | Port dest | Source          | Commentaire |
| -------- | --------- | --------- | -------- | --------- | --------------- | ----------- |
| 0        | Autoriser | TCP       | *        | 22        | `IP_Membre1/32` | SSH         |
| 1        | Autoriser | TCP       | *        | 22        | `IP_Membre2/32` | SSH         |
| 2        | Autoriser | TCP       | *        | 8006      | `IP_Admin/32`   | Proxmox UI  |
| 3        | Refuser   | IPv4      | *        | *         | *               | *           |


> Ne pas ouvrir `0.0.0.0/0` sur 22 ou 8006 en production scolaire.

## Vérification

Depuis un poste autorisé :

```bash
nc -zv 51.77.52.56 22
nc -zv 51.77.52.56 8006
ssh root@51.77.52.56
```

Navigateur : `https://51.77.52.56:8006`

## Journal

Cocher dans [serveur-ovh-configuration.md](serveur-ovh-configuration.md) : A1, A2, A3.