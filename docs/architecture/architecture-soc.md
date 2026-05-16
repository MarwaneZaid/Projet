# Architecture SOC

```mermaid
flowchart LR
    subgraph sources [Sources de logs]
        AD[AD / Windows]
        PF[pfSense]
        LIN[Linux / Docker]
    end

    subgraph collect [Collecte]
        WZ[Wazuh Manager]
        SUR[Suricata]
    end

    subgraph store [Stockage & analyse]
        IDX[Wazuh Indexer]
        GRA[Grafana]
    end

    subgraph ir [Réponse incident]
        TH[TheHive]
        CX[Cortex]
        N8[n8n]
    end

    AD --> WZ
    PF --> WZ
    LIN --> WZ
    SUR --> WZ
    WZ --> IDX
    IDX --> GRA
    WZ --> N8
    N8 --> TH
    TH --> CX
```

## Pipelines à implémenter

1. **Détection** : règles Wazuh + alertes Suricata
2. **Enrichissement** : Cortex analyzers sur IOC
3. **Orchestration** : n8n reçoit webhook Wazuh → case TheHive + email
4. **Visualisation** : Grafana (metrics + logs agrégés si Loki/Elastic plus tard)

## Règles d’équipe

- Toute nouvelle règle de détection : PR + test sur événement simulé
- Faux positifs documentés dans `docs/wiki/soc-regles.md` (à créer)
