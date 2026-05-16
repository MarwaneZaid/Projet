# Ansible — automatisation (phase Avr. – Mai)

## Structure prévue

```
ansible/
├── inventory/
│   ├── hosts.yml          # groupes : proxmox, pfsense, ad, docker_soc
│   └── group_vars/
├── playbooks/
│   ├── site.yml           # orchestration
│   ├── docker-soc.yml
│   └── wazuh-agent.yml
└── roles/
```

## Cas d’usage

- Déploiement agents Wazuh sur VMs Linux
- Configuration de base hôte Docker (paquets, durcissement SSH)
- Sauvegarde documentée (scripts + cron, pas secrets en clair)

## Démarrage

```bash
# Depuis une machine admin avec accès SSH aux VMs
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --check
```

Inventaire : remplir après Phase 1 avec IPs réelles.
