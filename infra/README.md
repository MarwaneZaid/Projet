# Infrastructure — guide de déploiement

Ordre recommandé sur Proxmox.

## 1. Proxmox VE

Voir [proxmox/checklist-install.md](proxmox/checklist-install.md).

- Installation sur bare metal
- `vmbr0` : management + LAN
- `vmbr1` : DMZ (si 2 NIC ou VLAN sur switch)
- Politique snapshots avant chaque grosse modification

## 2. pfSense

Voir [pfsense/README.md](pfsense/README.md).

- WAN / LAN / OPT (DMZ, SOC)
- DHCP réservé pour AD et serveurs fixes
- Logs firewall activés

## 3. Active Directory

Voir [active-directory/README.md](active-directory/README.md).

- Samba AD (léger) **ou** Windows Server (si licences)
- OU, groupes, GPO audit / logs
- Comptes de service pour agents (pas de mots de passe en Git)

## 4. Hôte Docker (Linux)

- VM Debian/Ubuntu dédiée, 2 vCPU / 4–8 Go RAM
- Docker + Docker Compose
- Réseau : interface sur segment SOC
- Déploiement stacks : `../soc/`, `../redteam/` (lab isolé)

## 5. VPN & DMZ

- VPN : IPsec ou OpenVPN sur pfSense (doc dans `docs/procedures/`)
- DMZ : Nginx/Traefik + certificats (Let's Encrypt interne ou CA lab)

## Responsables suggérés

| Lot | Lead | Relecteur |
|-----|------|-----------|
| Proxmox + VM | Étudiant 1 | Étudiant 2 |
| pfSense + VPN | Étudiant 2 | Étudiant 1 |
| AD + logs | Étudiant 2 | Étudiant 3 |
