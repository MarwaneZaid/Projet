# Proxmox — checklist installation

- [ ] ISO Proxmox VE téléchargée (version : ______)
- [ ] RAID / ZFS ou LVM-thin selon disques disponibles
- [ ] Interface web https://IP:8006 accessible depuis poste admin
- [ ] Abonnement repo : `no-subscription` si pas d’abonnement entreprise
- [ ] Mise à jour : `apt update && apt full-upgrade`
- [ ] Backup job vers stockage externe ou second disque (si possible)
- [ ] Template cloud-init Debian/Ubuntu pour VMs rapides
- [ ] Nommage VMs : `fw-pfsense`, `ad-dc01`, `docker-soc01`, `lab-rt01`

## Templates ressources par VM (ajuster selon RAM totale)

Documenter les ID VM et IPs dans `docs/architecture/inventaire-vms.md` (à créer).
