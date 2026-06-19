# Captures d'écran — où chercher, comment faire, quoi montrer

Pour **chaque** étape clé : aller au bon endroit → faire la capture → enregistrer au bon chemin.

**Dépôt des images :** `docs/livrables/screenshots/NN-dossier/` (voir [README](../livrables/screenshots/README.md))

---

## Comment prendre une capture (Mac)


| Méthode             | Raccourci                                                | Quand l'utiliser                    |
| ------------------- | -------------------------------------------------------- | ----------------------------------- |
| **Fenêtre entière** | `Cmd + Shift + 3`                                        | Terminal, Proxmox plein écran       |
| **Zone choisie**    | `Cmd + Shift + 4` puis glisser                           | Une zone précise (tableau firewall) |
| **Fenêtre active**  | `Cmd + Shift + 4` puis `Espace` puis clic sur la fenêtre | Navigateur Safari, Terminal         |


**Ensuite :**

1. Le fichier est sur le **Bureau** (`Capture d'écran … .png`).
2. **Renommer** exactement comme indiqué (ex. `01-proxmox_storage-zfs.png`).
3. **Déplacer** dans le dossier indiqué (ex. `docs/livrables/screenshots/01-proxmox/`).
4. Dans le rapport : *Figure X — [légende]* + chemin du fichier.

**À flouter ou éviter :** champs mot de passe, clés SSH privées, tokens API, contenu de `.env`.

---

## Leçon 0 — Accès serveur

**Dossier :** `docs/livrables/screenshots/00-acces/`

### 0.1 — Firewall OVH actif


|                  |                                                                                                                                                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Où chercher**  | Navigateur → [manager.eu.ovhcloud.com](https://manager.eu.ovhcloud.com/) → menu **Bare Metal Cloud** → **Network** → **IP** → clic sur **51.77.52.56** → onglet **Edge Network Firewall** (ou URL `…/edge-network-firewall`) |
| **Comment**      | `Cmd+Shift+4` sur le **tableau des règles** + le toggle **Enabled** visible en haut                                                                                                                                          |
| **Quoi montrer** | Règle 0 : TCP 22 depuis ton IP ; règle 1 : TCP 8006 ; règle 19 : Refuse IPv4 ; statut **Activé**                                                                                                                             |
| **Fichier**      | `00-ovh_firewall-regles-actives.png`                                                                                                                                                                                         |


### 0.2 — Ton IP publique


|                  |                                                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Où chercher**  | Safari → [https://www.whatismyip.com](https://www.whatismyip.com) **ou** Terminal Mac                               |
| **Comment**      | Terminal : taper `curl -s https://ifconfig.me` puis `Cmd+Shift+4` sur la ligne qui affiche l’IP (ex. `46.193.6.82`) |
| **Quoi montrer** | L’IP affichée (pour prouver qu’elle correspond aux règles firewall)                                                 |
| **Fichier**      | `00-acces_mon-ip-publique.png`                                                                                      |


### 0.3 — Port 22 ouvert


|                  |                                                                              |
| ---------------- | ---------------------------------------------------------------------------- |
| **Où chercher**  | **Terminal** sur ton Mac (pas sur le serveur)                                |
| **Comment**      | Taper `nc -zv 51.77.52.56 22` → attendre **succeeded** → capture du terminal |
| **Quoi montrer** | La ligne `Connection to 51.77.52.56 port 22 [tcp/ssh] succeeded!`            |
| **Fichier**      | `00-acces_nc-port-22-ok.png`                                                 |


### 0.4 — SSH connecté


|                  |                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------- |
| **Où chercher**  | Terminal Mac après `ssh -i ~/.ssh/id_ed25519_ovh root@51.77.52.56`                    |
| **Comment**      | Une fois le prompt visible, `Cmd+Shift+4` sur le terminal                             |
| **Quoi montrer** | `root@ns3138292:~#` (ou hostname Proxmox) — **pas** la commande `ssh` avec clé privée |
| **Fichier**      | `00-acces_ssh-root-connecte.png`                                                      |


### 0.5 — Interface Proxmox


|                  |                                                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Où chercher**  | Safari → `https://51.77.52.56:8006` → accepter l’avertissement certificat → login `root`                                                             |
| **Comment**      | Après connexion : vue **Datacenter** (panneau gauche) → `Cmd+Shift+3` ou capture fenêtre Safari                                                      |
| **Quoi montrer** | Titre **Proxmox Virtual Environment**, nœud **ns3138292**, utilisateur **root@pam** en haut à droite, URL `51.77.52.56:8006` dans la barre d’adresse |
| **Fichier**      | `00-proxmox_ui-datacenter.png`                                                                                                                       |


### 0.6 — Fiche serveur OVH


|                  |                                                                                                                 |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| **Où chercher**  | Manager → **Bare Metal Cloud** → **Dedicated servers** → **ns3138292.ip-51-77-52.eu** → **General information** |
| **Comment**      | Capture de la zone **Operating system** (Proxmox 9), **Network** (51.77.52.56), **Commercial name** (KS-5)      |
| **Quoi montrer** | Nom serveur, IP, OS Proxmox, RAM 32 Go                                                                          |
| **Fichier**      | `00-ovh_fiche-serveur.png`                                                                                      |


---

## Leçon 1 — Proxmox : créer les VMs

**Dossier :** `docs/livrables/screenshots/01-proxmox/`  
**Où commencer :** `https://51.77.52.56:8006` connecté en `root@pam`

### 1.1 — Stockage ZFS


|                  |                                                                                                                   |
| ---------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Où chercher**  | Proxmox UI → panneau gauche **Datacenter** (clic) → menu du milieu **Storage**                                    |
| **Comment**      | Clic **Storage** → attendre le tableau → capture où on voit une ligne **local-zfs** ou **data** avec ~**3.6 TiB** |
| **Quoi montrer** | Colonnes **Type**, **Avail** / **Total**, nom du stockage ZFS                                                     |
| **Fichier**      | `01-proxmox_storage-zfs.png`                                                                                      |


### 1.2 — Assistant Create VM — General (pfSense)


|                  |                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| **Où chercher**  | Bouton bleu **Create VM** (barre du haut, à droite) → fenêtre assistant → onglet **General** (premier) |
| **Comment**      | Remplir VM ID **100**, Name **fw-pfsense** → **ne pas cliquer Next** tout de suite → capture           |
| **Quoi montrer** | Champs **VM ID: 100**, **Name: fw-pfsense**, **Node: ns3138292**                                       |
| **Fichier**      | `01-proxmox_vm100-general.png`                                                                         |


### 1.3 — Ressources VM 100 (RAM, disque, CPU)


|                  |                                                                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Où chercher**  | Même assistant **Create VM** → onglets **Disks**, **CPU**, **Memory** (un par un ou un récap avant Finish)                                                                         |
| **Comment**      | Capturer l’onglet **Memory** avec **1024** MiB, ou faire une capture avec plusieurs onglets visités ; idéal : 1 image par onglet ou 1 image **Summary** avant Finish si disponible |
| **Quoi montrer** | Memory **1024**, Disk **20 GiB**, CPU **1** core                                                                                                                                   |
| **Fichier**      | `01-proxmox_vm100-ressources.png`                                                                                                                                                  |


### 1.4 — VM fw-pfsense dans l’arbre


|                  |                                                                              |
| ---------------- | ---------------------------------------------------------------------------- |
| **Où chercher**  | Panneau gauche : **Datacenter** → déplier **ns3138292** → liste des VMs      |
| **Comment**      | Après **Finish** de Create VM → capture de l’arbre avec **100 (fw-pfsense)** |
| **Quoi montrer** | Ligne **fw-pfsense** avec ID **100**                                         |
| **Fichier**      | `01-proxmox_vm100-liste.png`                                                 |


### 1.5 — Deux cartes réseau pfSense (plus tard)


|                  |                                                                            |
| ---------------- | -------------------------------------------------------------------------- |
| **Où chercher**  | Clic VM **fw-pfsense (100)** → menu **Hardware** (centre)                  |
| **Comment**      | **Add** → **Network Device** pour la 2e carte → capture liste **Hardware** |
| **Quoi montrer** | **2 lignes** « Network Device » (net0, net1)                               |
| **Fichier**      | `01-proxmox_vm100-2-nics.png`                                              |


### 1.6 — VM ad-dc01 (101)


|                  |                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------ |
| **Où chercher**  | **Create VM** ID **101** name **ad-dc01** **ou** VM 101 → **Summary** / **Hardware** |
| **Comment**      | Capture montrant nom + RAM **4096** (ou 8192 si Windows)                             |
| **Quoi montrer** | **ad-dc01 (101)** et mémoire allouée                                                 |
| **Fichier**      | `01-proxmox_vm101-ad-dc01.png`                                                       |


### 1.7 — VM docker-soc01 (102)


|                  |                                                  |
| ---------------- | ------------------------------------------------ |
| **Où chercher**  | VM **102** → **Hardware** ou **Summary**         |
| **Comment**      | Capture où **Memory** = **8192** MiB est lisible |
| **Quoi montrer** | **docker-soc01** + **8 Go** RAM                  |
| **Fichier**      | `01-proxmox_vm102-docker-soc.png`                |


### 1.8 — VM lab-rt01 (103)


|                 |                                   |
| --------------- | --------------------------------- |
| **Où chercher** | Arbre gauche : **lab-rt01 (103)** |
| **Comment**     | Capture de la ligne VM 103        |
| **Fichier**     | `01-proxmox_vm103-lab-rt.png`     |


### 1.9 — Les 4 VMs ensemble (capture la plus importante)


|                  |                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------- |
| **Où chercher**  | **Datacenter** → clic nœud **ns3138292** → vue **Server View** (liste VMs)            |
| **Comment**      | Agrandir le panneau gauche pour voir **100, 101, 102, 103** sur **une seule** capture |
| **Quoi montrer** | Les 4 noms : fw-pfsense, ad-dc01, docker-soc01, lab-rt01                              |
| **Fichier**      | `01-proxmox_toutes-vms.png`                                                           |


### 1.10 — Snapshot


|                  |                                                                                                |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| **Où chercher**  | Clic une VM (ex. 100) → menu **Snapshots** (pas Hardware)                                      |
| **Comment**      | **Take Snapshot** → Name `pre-os-install` → **OK** → capture du tableau avec la nouvelle ligne |
| **Quoi montrer** | Nom snapshot + **Date** / statut                                                               |
| **Fichier**      | `01-proxmox_snapshot-pre-os.png`                                                               |


### 1.11 — Inventaire GitHub


|                  |                                                                                |
| ---------------- | ------------------------------------------------------------------------------ |
| **Où chercher**  | Sur ton Mac : Cursor / VS Code → fichier `docs/architecture/inventaire-vms.md` |
| **Comment**      | Remplir le tableau → capture de l’éditeur (pas le terminal)                    |
| **Quoi montrer** | IDs 100–103, RAM, rôles — **sans** mots de passe                               |
| **Fichier**      | `01-proxmox_inventaire-vms.png`                                                |


### 1.12 — ISO uploadées (optionnel)


|                 |                                                                       |
| --------------- | --------------------------------------------------------------------- |
| **Où chercher** | **Datacenter** → **ns3138292** → **local** (storage) → **ISO Images** |
| **Comment**     | Après upload ISO pfSense ou Debian → capture de la liste des `.iso`   |
| **Fichier**     | `01-proxmox_iso-upload.png`                                           |


---

## Leçon 2 — pfSense

**Dossier :** `docs/livrables/screenshots/02-pfsense/`  
**Où chercher :** Console VM pfSense ou navigateur `https://IP_LAN` (après install)


| #   | Où chercher                                              | Comment capturer                        | Fichier                             |
| --- | -------------------------------------------------------- | --------------------------------------- | ----------------------------------- |
| 2.1 | Console Proxmox : VM 100 → **Console** → install pfSense | Fin d’install « completed »             | `02-pfsense_install-termine.png`    |
| 2.2 | pfSense UI → **Interfaces** → **Assignments**            | WAN + LAN assignées                     | `02-pfsense_interfaces-wan-lan.png` |
| 2.3 | **Interfaces** → **LAN**                                 | IP **192.168.10.1/24** visible          | `02-pfsense_lan-ip-10.1.png`        |
| 2.4 | **Services** → **DHCP Server** → onglet LAN              | Plage enable + range .100–.200          | `02-pfsense_dhcp-plage.png`         |
| 2.5 | **Firewall** → **Rules** → **WAN**                       | Règle block par défaut en bas           | `02-pfsense_firewall-wan-deny.png`  |
| 2.6 | **Diagnostics** → **Ping** ou terminal VM LAN            | Ping **8.8.8.8** = success              | `02-pfsense_ping-internet-ok.png`   |
| 2.7 | VM DMZ ou pfSense ping                                   | Ping IP LAN depuis DMZ = **fail**       | `02-pfsense_dmz-pas-lan.png`        |
| 2.8 | **Diagnostics** → **Backup & Restore**                   | Message export OK ou fichier téléchargé | `02-pfsense_backup-xml.png`         |


---

## Leçon 3 — Active Directory

**Dossier :** `docs/livrables/screenshots/03-active-directory/`


| #   | Où chercher                                         | Comment capturer                                  | Fichier                          |
| --- | --------------------------------------------------- | ------------------------------------------------- | -------------------------------- |
| 3.1 | **ADUC** (Windows) ou terminal Samba sur `ad-dc01`  | Nom de domaine **lab.local**                      | `03-ad_domaine-cree.png`         |
| 3.2 | ADUC → arborescence **OU**                          | Dossiers Users, Servers…                          | `03-ad_structure-ou.png`         |
| 3.3 | ADUC → **Users**                                    | ≥ 10 comptes listés                               | `03-ad_utilisateurs-test.png`    |
| 3.4 | **GPMC** → GPO mot de passe → **Edit**              | Paramètres complexité activés                     | `03-ad_gpo-mot-de-passe.png`     |
| 3.5 | GPMC → GPO audit → **Advanced Audit Policy**        | Logon success/failure                             | `03-ad_gpo-audit-logon.png`      |
| 3.6 | VM client → **Paramètres** → **À propos** → Domaine | `lab.local` affiché                               | `03-ad_client-joint-domaine.png` |
| 3.7 | **Event Viewer** → Security                         | Event **4624** ou **4625**                        | `03-ad_event-logon.png`          |
| 3.8 | ADUC → utilisateur **wazuh-agent**                  | Propriétés compte (**pas** l’onglet mot de passe) | `03-ad_compte-wazuh.png`         |


---

## Leçon 4 — MVP SOC seulement

**Dossier :** `docs/livrables/screenshots/04-soc/`  
**Où chercher :** SSH sur `docker-soc01` ou navigateur vers IP SOC

| #   | Où chercher                                               | Comment capturer                                                | Fichier                                  |
| --- | --------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------- |
| 4.1 | SSH `docker-soc01` → dossier `soc/` → `docker compose ps` | Tous services Wazuh/Grafana en **Up**                          | `04-soc_docker-ps-up.png`                |
| 4.2 | Navigateur → `https://IP_SOC` (Wazuh)                     | Login ou vue dashboard Wazuh                                   | `04-soc_wazuh-dashboard.png`             |
| 4.3 | Wazuh → menu **Agents** → **Summary**                     | Au moins 3 agents **Active** (vert)                            | `04-soc_wazuh-agents-actifs.png`         |
| 4.4 | Wazuh → **Alerts** (après test brute force SSH)           | Alerte brute force / failed SSH visible                        | `04-soc_wazuh-alerte-ssh-bruteforce.png` |
| 4.5 | Wazuh → **Alerts** (après échecs logon AD)                | Alerte AD failed logon (ex. events 4625 remontés)              | `04-soc_wazuh-alerte-ad-failed-logon.png`|
| 4.6 | Wazuh → **Alerts** (après scan nmap en lab)               | Alerte scan de ports / activité suspecte                       | `04-soc_wazuh-alerte-port-scan.png`      |
| 4.7 | Grafana `http://IP_SOC:3000` (ou dashboard Wazuh natif)   | Dashboard lisible : agents + alertes                           | `04-soc_grafana-dashboard.png`           |
| 4.8 | Fichier de preuves `docs/livrables/soc-mvp-preuves.md`    | Tableau final scénarios ↔ alertes ↔ heures rempli             | `04-soc_mvp-tableau-preuves.png`         |


---

## Leçon 5 — Red Team

**Dossier :** `docs/livrables/screenshots/05-red-team/`


| #   | Où chercher                                                       | Comment capturer                      | Fichier                       |
| --- | ----------------------------------------------------------------- | ------------------------------------- | ----------------------------- |
| 5.1 | Terminal lab-rt01 : `ip route` / `ping 192.168.10.1`              | Échec ou pas de route vers LAN        | `05-rt_isolation-lab.png`     |
| 5.2 | OpenVAS → **Scans** → rapport PDF/HTML                            | Page résumé vulnérabilités            | `05-rt_openvas-rapport.png`   |
| 5.3 | BloodHound → vue **Graph**                                        | Chemins d’attaque visibles            | `05-rt_bloodhound-graphe.png` |
| 5.4 | Cursor → `docs/livrables/redteam/journal-exercices.md`            | Lignes remplies date/heure/outil      | `05-rt_journal-exercice.png`  |
| 5.5 | 2 fenêtres côte à côte : journal RT + alerte Wazuh **même heure** | Montage ou 2 captures dans le rapport | `05-rt_correlation-soc.png`   |


---

## Leçon 6–8 — Plus tard

**Dossiers :** `06-ansible/`, `07-dmz/`, `08-rapport/` (à créer au besoin)


| #   | Où chercher                                       | Fichier                          |
| --- | ------------------------------------------------- | -------------------------------- |
| 6.1 | Terminal : `ansible-playbook …` fin **failed=0**  | `06-ansible_playbook-ok.png`     |
| 7.1 | Safari → URL HTTPS reverse proxy DMZ              | `07-dmz_reverse-proxy-https.png` |
| 8.1 | Fichier `docs/architecture/diagrams/*.png` ouvert | `08-rapport_schema-reseau.png`   |


---

## Checklist rapide (leçon en cours)

Avant de passer à la leçon suivante :

- Chaque étape du guide a son **fichier .png** dans le bon dossier
- Nom de fichier = celui du tableau (pas `Capture d'écran 2026…`)
- Aucun secret visible
- Au moins une capture « vue d’ensemble » (ex. `01-proxmox_toutes-vms.png`)

**Guide pas à pas Proxmox :** [01-proxmox-creer-vms.md](01-proxmox-creer-vms.md)