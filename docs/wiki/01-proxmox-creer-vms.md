# Leçon 1 — Créer les VMs dans Proxmox (pas à pas)

**Niveau :** débutant infra  
**Durée :** ~1 h pour les 4 VMs principales  
**Prérequis :** accès `https://51.77.52.56:8006` + SSH root OK

**Captures (où + comment + nom fichier) :** [screenshots-par-etape.md § Leçon 1](screenshots-par-etape.md#leçon-1--proxmox--créer-les-vms)  
**Dépôt fichiers :** `docs/livrables/screenshots/01-proxmox/`  
**Raccourci Mac :** `Cmd+Shift+3` (écran entier) ou `Cmd+Shift+4` (zone)

---

## Objectif pédagogique

À la fin, tu sauras :

- ce qu'est une **VM** et pourquoi on en crée plusieurs ;
- comment allouer **CPU / RAM / disque** sans saturer le serveur ;
- comment nommer et documenter pour que l'équipe travaille dessus.

---

## Pourquoi plusieurs VMs ?


| VM             | Rôle métier          | Pourquoi séparée                                     |
| -------------- | -------------------- | ---------------------------------------------------- |
| `fw-pfsense`   | Firewall             | Point unique entre Internet et vos réseaux internes  |
| `ad-dc01`      | Active Directory     | Identités, groupes, GPO — cœur « entreprise »        |
| `docker-soc01` | SOC (Wazuh, Grafana) | Beaucoup de RAM ; isoler la charge                   |
| `lab-rt01`     | Red Team             | **Isolée** pour ne pas attaquer l'AD « prod » du lab |


**Principe pro :** un service = une VM (ou un conteneur), pas tout sur l'hôte Proxmox.

---

## Ressources à ne pas dépasser

Serveur : **32 Go RAM**, **4 cœurs / 8 threads**.


| VM                    | vCPU | RAM     | Disque | Total RAM |
| --------------------- | ---- | ------- | ------ | --------- |
| fw-pfsense            | 1    | 1 Go    | 20 Go  | 1 Go      |
| ad-dc01               | 2    | 4 Go    | 60 Go  | 5 Go      |
| docker-soc01          | 2    | 8 Go    | 100 Go | 13 Go     |
| lab-rt01              | 2    | 4 Go    | 40 Go  | 17 Go     |
| win-client01 (option) | 2    | 4 Go    | 40 Go  | 21 Go     |
| **Proxmox (hôte)**    | —    | ~4–8 Go | —      | marge     |


Ne pas dépasser **~24 Go** alloués aux VMs pour garder de la marge.

---

## Étape A — Vérifier le stockage (5 min)

**Où :** Proxmox UI → **Datacenter** → **Storage**

**Quoi chercher :** un stockage type **ZFS** ou **local-zfs** / `data` avec ~**3,6 To** libres (`/var/lib/vz`).

**Pourquoi :** les disques des VMs sont créés ici. Sans espace, la création échoue.

**Critère OK :** tu vois le stockage et **Available** > 200 Go.


| 📸 Capture                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Où :** Datacenter → **Storage** — **Comment :** [§ 1.1](screenshots-par-etape.md#11--stockage-zfs) — **Fichier :** `01-proxmox_storage-zfs.png` dans `docs/livrables/screenshots/01-proxmox/` |


---

## Étape B — Créer la première VM : `fw-pfsense` (15 min)

**Où :** bouton **Create VM** (en haut à droite)

### B.1 General


| Champ | Valeur                 | Pourquoi                              |
| ----- | ---------------------- | ------------------------------------- |
| Node  | `ns3138292` (ton nœud) | Seul serveur du cluster               |
| VM ID | `100`                  | ID fixe — référence dans l'inventaire |
| Name  | `fw-pfsense`           | Nom lisible pour toute l'équipe       |



| 📸 Capture                                                                                             |
| ------------------------------------------------------------------------------------------------------ |
| Onglet **General** : VM ID **100**, Name **fw-pfsense**, Node visible → `01-proxmox_vm100-general.png` |


**Next**

### B.2 OS


| Champ | Valeur                                                  | Pourquoi                                                 |
| ----- | ------------------------------------------------------- | -------------------------------------------------------- |
| ISO   | *Aucune pour l'instant* ou ISO pfSense si déjà uploadée | On crée la coque ; l'Étudiant 2 installera pfSense après |
| Type  | Linux / Other                                           | pfSense est FreeBSD — souvent « Other »                  |


Si tu n'as pas l'ISO pfSense :

1. **Datacenter** → **local** (storage) → **ISO Images** → **Upload**
2. Télécharger pfSense depuis [pfsense.org](https://www.pfsense.org/download/) (AMD64, ISO)
3. Revenir à Create VM → choisir cette ISO


| 📸 Capture (si upload ISO)                                                |
| ------------------------------------------------------------------------- |
| Liste **ISO Images** avec pfSense ou Debian → `01-proxmox_iso-upload.png` |


**Next**

### B.3 System → B.7 Network

(Voir tableau ressources dans la leçon complète — Disks 20G, CPU 1, RAM 1024, Bridge vmbr0)


| 📸 Capture                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------ |
| Un écran montrant **Memory 1024**, **Disk 20**, **CPU 1** (récap avant Finish) → `01-proxmox_vm100-ressources.png` |


**Next** → **Finish**


| 📸 Capture                                                                             |
| -------------------------------------------------------------------------------------- |
| Arborescence gauche : **fw-pfsense (100)** sous le nœud → `01-proxmox_vm100-liste.png` |


**Note prof :** pfSense aura besoin de **2 interfaces** (WAN + LAN). Après création :

1. VM `fw-pfsense` → **Hardware** → **Add** → **Network Device**


| 📸 Capture (après 2e NIC)                                              |
| ---------------------------------------------------------------------- |
| **Hardware** : 2 lignes Network Device → `01-proxmox_vm100-2-nics.png` |


---

## Étape C — Créer `ad-dc01` (VM ID 101)


| Onglet  | Valeur                                           |
| ------- | ------------------------------------------------ |
| General | ID **101**, Name **ad-dc01**                     |
| OS      | ISO Windows Server ou Debian 12 (Samba AD)       |
| Disks   | **60** GiB                                       |
| CPU     | **2** cores                                      |
| Memory  | **4096** MiB (4 Go) — **8192** si Windows Server |
| Network | `vmbr0`, VirtIO                                  |



| 📸 Capture                                                                                   |
| -------------------------------------------------------------------------------------------- |
| Liste VMs avec **ad-dc01 (101)** + résumé Hardware (RAM 4G) → `01-proxmox_vm101-ad-dc01.png` |


---

## Étape D — Créer `docker-soc01` (VM ID 102)


| Onglet  | Valeur                            |
| ------- | --------------------------------- |
| General | ID **102**, Name **docker-soc01** |
| Disks   | **100** GiB                       |
| Memory  | **8192** MiB (8 Go)               |



| 📸 Capture                                                                                      |
| ----------------------------------------------------------------------------------------------- |
| VM 102 avec **8192 MiB** visible (onglet Memory ou Summary) → `01-proxmox_vm102-docker-soc.png` |


---

## Étape E — Créer `lab-rt01` (VM ID 103)


| Onglet  | Valeur                        |
| ------- | ----------------------------- |
| General | ID **103**, Name **lab-rt01** |
| Memory  | **4096** MiB                  |



| 📸 Capture                                                          |
| ------------------------------------------------------------------- |
| VM **lab-rt01 (103)** dans la liste → `01-proxmox_vm103-lab-rt.png` |



| 📸 Capture finale leçon 1                                                      |
| ------------------------------------------------------------------------------ |
| **Une seule image** : les 4 VMs 100–103 visibles → `01-proxmox_toutes-vms.png` |


---

## Étape F — Documenter (10 min)

**Où :** [../architecture/inventaire-vms.md](../architecture/inventaire-vms.md)


| 📸 Capture                                                                                        |
| ------------------------------------------------------------------------------------------------- |
| Fichier inventaire rempli (IDs, RAM — **pas** de mots de passe) → `01-proxmox_inventaire-vms.png` |


---

## Étape G — Snapshot « avant install OS »

1. VM → **Snapshots** → **Take Snapshot**
2. Nom : `pre-os-install`


| 📸 Capture                                                                             |
| -------------------------------------------------------------------------------------- |
| Onglet Snapshots avec ligne `pre-os-install` + date → `01-proxmox_snapshot-pre-os.png` |


---

## Critères « Leçon 1 terminée »

- 4 VMs visibles dans Proxmox (100–103)
- RAM totale allouée < 24 Go
- `inventaire-vms.md` rempli
- 1 snapshot par VM
- **📸 Toutes les captures 1.1 à 1.11** (ou minimum 1.1, 1.9, 1.10, 1.11)

---

## Erreurs fréquentes


| Problème                | Cause               | Solution                        |
| ----------------------- | ------------------- | ------------------------------- |
| VM ne démarre pas       | Pas d'ISO attachée  | Hardware → CD/DVD → choisir ISO |
| « out of memory »       | Trop de RAM allouée | Réduire RAM ou arrêter une VM   |
| UI Proxmox inaccessible | Port 8006 fermé     | Firewall OVH : autoriser 8006   |


---

## Leçon suivante

→ [02-pfsense-installation.md](02-pfsense-installation.md)