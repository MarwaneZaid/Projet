# 07 — VPN, DMZ & reverse proxy

**Responsable :** Étudiant 2  
**Relecteur :** Étudiant 1  
**Priorité globale :** P3  
**Dépôt :** [infra/pfsense/](../../infra/pfsense/), extension DMZ

**Prérequis :** pfSense P1 (02), VM en DMZ si services exposés

---

## P1 — Minimum pour la démo

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 7.1 | Segment DMZ défini et **isolé du LAN** (rappel test ping) | [ ] |
| 7.2 | Schéma mis à jour : flux Internet → pfSense → DMZ | [ ] |

---

## P2 — Important

| # | Tâche exacte | Détail | Validé |
|---|--------------|--------|--------|
| 7.3 | Installer **Nginx** ou **Traefik** sur VM DMZ | 1 service backend interne (ex. Grafana en lecture seule) | [ ] |
| 7.4 | **TLS** : certificat auto-signé ou CA lab documentée | HTTPS sans erreur depuis LAN | [ ] |
| 7.5 | pfSense : NAT port 443 WAN → reverse proxy DMZ (optionnel si pas d’IP publique : doc seulement) | [ ] |
| 7.6 | Headers sécurité (HSTS, X-Frame-Options) sur proxy | [ ] |

---

## P3 — Utile

| # | Tâche exacte | Validé |
|---|--------------|--------|
| 7.7 | **VPN site-to-site** IPsec ou OpenVPN vers « site distant » simulé (2e pfSense ou cloud) | [ ] |
| 7.8 | Si impossible : document 1 page « architecture VPN prévue + blocage matériel » | [ ] |
| 7.9 | WAF basique ou rate limiting sur proxy (optionnel) | [ ] |

---

## Critères « réseau avancé validé »

- [ ] Reverse proxy fonctionnel en DMZ  
- [ ] TLS actif  
- [ ] VPN réalisé **ou** documenté proprement  

**Ensuite :** [08-livrables-rapport.md](08-livrables-rapport.md)
