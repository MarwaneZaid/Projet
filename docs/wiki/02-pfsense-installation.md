# Leçon 2 — Installer et configurer pfSense

**Responsable :** Étudiant 2  
**Prérequis :** VM `fw-pfsense` (ID 100), ISO pfSense sur Proxmox

**Captures :** [screenshots-par-etape.md § Leçon 2](screenshots-par-etape.md#leçon-2--pfsense-à-faire)  
**Dépôt :** `docs/livrables/screenshots/02-pfsense/`

> Leçon détaillée pas à pas : à compléter quand la Leçon 1 est validée.  
> Tâches techniques : [../taches/02-reseau-pfsense.md](../taches/02-reseau-pfsense.md)

## Résumé des captures obligatoires

| Après quoi | 📸 Quoi photographier |
|------------|-------------------------|
| Install terminée | Écran install pfSense OK |
| WAN + LAN | Assignments des 2 interfaces |
| IP LAN | `192.168.10.1/24` |
| DHCP | Plage activée |
| Firewall WAN | Règle deny par défaut |
| Test | Ping Internet OK depuis LAN |
| Isolation | Ping LAN depuis DMZ = échec |
| Backup | Export XML réussi |
