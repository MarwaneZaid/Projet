# Checklist de validation par phase

Cocher et dater quand **toute l’équipe** a validé.

## Phase 0 — Cadrage (Oct. – Nov.)

- [ ] Plan opérationnel relu et accepté par les 4
- [ ] TEAM.md complété (noms, contacts, binômes)
- [ ] Specs matériel serveur documentées
- [ ] Plages IP et schéma réseau v0 validés
- [ ] Choix Samba AD vs Windows Server acté

## Phase 1 — Infrastructure (Déc. – Jan.)

- [ ] Proxmox installé, stockage et snapshots configurés
- [ ] VM pfSense : NAT, DHCP, règles firewall de base
- [ ] Segments LAN / DMZ définis et testés (ping, isolation)
- [ ] AD opérationnel (utilisateurs, OU, au moins 1 GPO test)
- [ ] Logs sécurité AD / Windows orientés vers le futur collecteur SOC
- [ ] VM Linux hôte Docker prête (réseau + accès admin équipe)
- [ ] Documentation procédure dans `docs/procedures/`

## Phase 2 — SOC & Red Team (Fév. – Mars)

- [ ] Stack SOC `soc/docker-compose` déployée sur segment dédié
- [ ] Agents Wazuh sur au moins 2 systèmes pilotes
- [ ] Suricata : trafic miroir ou span documenté
- [ ] Grafana : au moins 1 dashboard utile
- [ ] TheHive + Cortex : test d’un incident fictif
- [ ] Stack Red Team isolée (pas de routage vers prod)
- [ ] 1 scénario simulé documenté (ex. brute force lab)
- [ ] n8n : au moins 1 alerte → notification

## Phase 3 — Automatisation (Avr. – Mai)

- [ ] Playbooks Ansible pour déploiement reproductible
- [ ] Sauvegardes Proxmox + configs pfSense testées (restore)
- [ ] VPN site-to-site testé (ou documenté si matériel manquant)
- [ ] Reverse proxy DMZ documenté

## Phase 4 — Tests & livrables (Juin – Juil.)

- [ ] Exercice SOC : détection + réponse sur scénario connu
- [ ] Exercice Red Team : rapport aligné avec logs SOC
- [ ] Rapport technique (~10 pages)
- [ ] WikiJS à jour (client + interne)
- [ ] Schémas architecture à jour
- [ ] Pitch + démo orale répétée
- [ ] Portail client/admin (si extension) : auth + 1 parcours complet
