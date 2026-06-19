# SOC — déploiement

**Responsable lead** : Étudiant 3 · **Relecteur** : Étudiant 4

**Guide complet (définitions, architecture, compétences, procédure) :** [docs/wiki/README-SOC-GUIDE-COMPLET.md](../docs/wiki/README-SOC-GUIDE-COMPLET.md)  
**Runbook actions rapides :** [docs/wiki/04-mvp-soc-runbook-unifie.md](../docs/wiki/04-mvp-soc-runbook-unifie.md)

## Prérequis

- VM Linux avec Docker (≥ 8 Go RAM pour Wazuh + Grafana)
- Segment réseau SOC (voir [docs/architecture/topologie-reseau.md](../docs/architecture/topologie-reseau.md))
- pfSense : autoriser agents → `1514/udp`, `1515/tcp`, dashboard `443`

## Installation

```bash
cp .env.example .env
# Éditer .env avec mots de passe forts
docker compose up -d
```

## Composants par vague

| Vague | Outil | Statut |
|-------|-------|--------|
| 1 | Wazuh + Grafana | `docker-compose.yml` |
| 2 | Suricata | VM ou conteneur + règles |
| 3 | TheHive + Cortex | compose séparé recommandé |
| 4 | n8n | alertes webhook → email / ticket |

## Agents

Installer l’agent Wazuh sur : contrôleur AD, pfSense (si plugin), poste Linux lab.

## Dashboards

Exporter JSON Grafana dans `soc/grafana/dashboards/`.

Architecture détaillée : [docs/architecture/architecture-soc.md](../docs/architecture/architecture-soc.md)
