# Étape 2 — Premier accès Proxmox

**Prérequis :** [01-firewall-ovh.md](01-firewall-ovh.md) terminé.

## Connexion UI

1. Ouvrir `https://51.77.52.56:8006`
2. Accepter le certificat auto-signé
3. Login : `root` + mot de passe reçu par email OVH (ou défini à l’install)

## Sécurité immédiate

```bash
# Depuis votre poste (SSH autorisé)
ssh root@51.77.52.56

# Changer le mot de passe root
passwd

# Ajouter clés SSH équipe (une ligne par personne)
mkdir -p ~/.ssh && chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

## Post-install automatique

Sur l’hôte :

```bash
# Depuis le repo cloné sur le serveur, ou en pipe depuis votre PC :
bash scripts/proxmox/01-host-postinstall.sh
```

Puis création des VMs :

```bash
bash scripts/proxmox/02-create-vms.sh
```

## Captures à prendre (Leçon 0)

Voir [../wiki/screenshots-par-etape.md](../wiki/screenshots-par-etape.md#leçon-0--accès-serveur-déjà-fait-ou-à-compléter) — déposer dans `docs/livrables/screenshots/00-acces/`.

Minimum : firewall OVH, `nc` port 22 OK, SSH connecté, UI Proxmox Datacenter.

## Cocher les tâches

- [docs/taches/01-proxmox-virtualisation.md](../taches/01-proxmox-virtualisation.md) : 1.2, 1.3, 1.9–1.11
- [inventaire-vms.md](../architecture/inventaire-vms.md) : renseigner ID et IP
