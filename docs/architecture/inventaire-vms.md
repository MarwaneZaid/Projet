# Inventaire des machines virtuelles

À maintenir par l’Étudiant 1 après chaque création/modification de VM.

Hôte Proxmox : **51.77.52.56** — `ns3138292.ip-51-77-52.eu`

| Nom VM | ID Proxmox | vCPU | RAM | Disque | IP | Segment | Rôle | Responsable |
|--------|------------|------|-----|--------|-----|---------|------|---------------|
| fw-pfsense | | 1 | 1 Go | 20 Go | TBD | WAN + LAN | Firewall | Ét. 2 |
| ad-dc01 | | 2 | 4 Go | 60 Go | 192.168.10.x | LAN | Contrôleur AD | Ét. 2 |
| docker-soc01 | | 2 | 8 Go | 100 Go | 192.168.30.x | SOC | Wazuh, Grafana | Ét. 3 |
| lab-rt01 | | 2 | 4 Go | 40 Go | 192.168.99.x | LAB-RT | Red Team | Ét. 4 |
| win-client01 | | 2 | 4 Go | 40 Go | 192.168.10.x | LAN | Client AD | Ét. 2 |

## Snapshots nommés

| VM | Nom snapshot | Date | Commentaire |
|----|--------------|------|-------------|
| | | | |
