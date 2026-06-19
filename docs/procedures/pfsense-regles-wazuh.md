# pfSense — règles firewall vers Wazuh (192.168.20.18)

**Responsable :** Étudiant 2 (Jacques)  
**Manager Wazuh :** `192.168.20.22` (VM 201 `srv-wazuh-1`)  
**UI pfSense :** `https://192.168.20.1`

## Ports à autoriser

| Protocole | Port | Usage |
|-----------|------|--------|
| TCP | 1514 | Données agent Wazuh |
| TCP | 1515 | Enrôlement agent |
| UDP | 1514 | Syslog (optionnel) |

## Procédure UI (3 règles)

1. Connexion : `https://192.168.20.1` → compte admin pfSense.
2. Menu **Firewall → Rules** → onglet de l’interface source des agents (souvent **LAN** ou segment `192.168.20.0/24`).
3. **Add** (flèche vers le haut) — répéter pour chaque ligne du tableau :

| Champ | Valeur |
|-------|--------|
| Action | Pass |
| Interface | LAN (ou interface source des VMs) |
| Address Family | IPv4 |
| Protocol | TCP ou UDP selon la ligne |
| Source | Any (ou alias `VMs_LAB` : AD, web, etc.) |
| Destination | Single host → `192.168.20.22` |
| Destination port | Custom → `1514` ou `1515` |
| Description | `Wazuh agent 1514 TCP` / `Wazuh enroll 1515` / `Wazuh syslog 1514 UDP` |
| Log | Cocher si vous voulez tracer les flux agents |

4. **Save** puis **Apply Changes**.

## Ordre recommandé des règles

Placer les règles Wazuh **au-dessus** d’une éventuelle règle « block LAN » générique, mais **sous** les règles anti-spoofing si présentes.

## Test après application

Depuis une VM agent (ex. `srv-web-1`, `srv-ad-1`) :

```bash
nc -zv 192.168.20.22 1514
nc -zv 192.168.20.22 1515
```

Windows (PowerShell) :

```powershell
Test-NetConnection 192.168.20.18 -Port 1514
Test-NetConnection 192.168.20.18 -Port 1515
```

Dans Wazuh : **Endpoints Summary** → agent **Active** sous 2 minutes.

## Note topologie actuelle

Si toutes les VMs sont sur le même segment L2 (`vmbr2`, `192.168.20.0/24`), le trafic est-à-est peut passer **sans** traverser pfSense. Les règles restent nécessaires dès qu’un agent est sur un autre segment (DMZ, autre VLAN) ou pour la traçabilité / conformité au cahier des charges (tâche 4.5).

## Capture livrable

📸 `02-pfsense_regles-wazuh.png` — écran **Firewall → Rules** montrant les 3 règles vers `192.168.20.18`.
