# Topologie réseau

## Schéma logique (v0)

```mermaid
flowchart TB
    Internet((Internet))
    PF[pfSense<br/>NAT · FW · VPN]
    LAN[LAN 192.168.10.0/24<br/>AD · Admin]
    DMZ[DMZ 192.168.20.0/24<br/>Reverse Proxy]
    SOC[SOC 192.168.30.0/24<br/>Wazuh · Grafana]
    LAB[LAB-RT 192.168.99.0/24<br/>Red Team isolé]

    Internet --> PF
    PF --> LAN
    PF --> DMZ
    PF --> SOC
    PF -.->|règles strictes ou aucune route| LAB
```

## Flux à documenter

1. **Logs AD / Windows** → collecteur Wazuh (ports, pare-feu)
2. **Suricata** : SPAN/miroir depuis quel segment ?
3. **VPN site-to-site** : pair distant (école, autre site simulé)
4. **Reverse proxy** : TLS termination, backends en DMZ

## Fichiers complémentaires

- Export draw.io / PNG : placer dans `docs/architecture/diagrams/`
- Table des règles pfSense : `docs/procedures/pfsense-regles.md` (à créer)

## Validation

- [ ] Schéma validé par les 4 (date : ______)
- [ ] Règles « deny by default » sur LAB-RT vers LAN
