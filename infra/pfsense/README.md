# pfSense

## Configuration minimale

1. Interfaces : WAN, LAN, OPT1 (DMZ), OPT2 (SOC) si besoin
2. NAT sortant LAN → WAN
3. Règles : LAN → Internet ; LAN → SOC (ports agents) ; DMZ ≠ LAN sans proxy
4. DHCP + réservations pour AD et Docker host
5. Export config régulier : **Diagnostics → Backup & Restore**

## VPN site-to-site

- Documenter IP publique / pré-partagée dans coffre local (pas Git)
- Tester ping vers sous-réseau distant après tunnel UP

## Logs pour SOC

- Activer logs firewall
- Syslog remote vers IP Wazuh (phase 2)

## Fichiers équipe

- Captures ou tableaux de règles : `docs/procedures/pfsense-regles.md`
