# Vidéo de secours — démo SOC

Si la démo live échoue en soutenance, utiliser une **vidéo enregistrée** de la chaîne complète :

**Attaque (VM 107) → Wazuh (`.22`) → Portail (`.20`)**

## Enregistrer la vidéo

1. Connecter le **VPN** pfSense
2. Lancer **OBS** ou **QuickTime** (enregistrement écran)
3. Exécuter le script guidé :

```bash
cd ~/Desktop/Projet
bash scripts/demo/demo-soc-video.sh
```

Le script affiche les **pauses** et les URLs à montrer à l’écran (~5 min).

4. Exporter en **`demo-soc-secours.mp4`** dans ce dossier

## Contenu minimum de la vidéo

| Minute | Écran | Preuve |
|--------|-------|--------|
| 0:00 | Wazuh → Endpoints Summary | 3 agents `Active` (web, AD, manager) |
| 1:00 | Portail login `admin/admin123` | État normal |
| 2:00 | Terminal VM 107 : `attaque-test.sh` | Brute-force SSH |
| 3:00 | Wazuh Threat Hunting `srv-web-1` | Alertes auth |
| 4:00 | Portail dashboard | Alerte critique remontée |

## Captures de secours (si pas de vidéo)

Déposer dans `docs/livrables/screenshots/04-soc/` :

- `04-soc_wazuh-agents-active.png`
- `04-soc_attaque-bruteforce-termine.png`
- `04-soc_wazuh-threat-hunting-srv-web-1.png`
- `04-soc_portail-dashboard-alertes.png`

## Scripts associés

- [scripts/demo/demo-soc-video.sh](../../scripts/demo/demo-soc-video.sh)
- [scripts/demo/attaque-test.sh](../../scripts/demo/attaque-test.sh)
- [scripts/soc/install-wazuh-agent-linux.sh](../../scripts/soc/install-wazuh-agent-linux.sh) (déjà exécuté sur AD)
