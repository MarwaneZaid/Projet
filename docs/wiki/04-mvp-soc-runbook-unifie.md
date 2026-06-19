# Leçon 4 (SOC) — Runbook unifié MVP SOC

**Périmètre strict :** ne touche qu’au **SOC** (Wazuh + agents + dashboard + 3 alertes).  
**Responsable :** Étudiant 3  
**VM cible :** `docker-soc01`

## Prérequis
- `docker-soc01` accessible en SSH
- `docker-soc01`, `ad-dc01` et **au moins 1** autre VM Linux avec réseau OK
- Wazuh/MVP dans **le périmètre SOC** (pas TheHive/Cortex/n8n tant que le MVP n’est pas validé)

## Dossiers à connaître
- Stack SOC (code à déployer) : `soc/` (dans le repo)
- Captures SOC : `docs/livrables/screenshots/04-soc/`
- Tableau final preuves : `docs/livrables/soc-mvp-preuves.md`

## Règles de captures (Mac)
- Fenêtre entière : `Cmd + Shift + 3`
- Zone choisie : `Cmd + Shift + 4`
- Fenêtre active : `Cmd + Shift + 4` puis `Espace` puis clic
- Renommer **exactement** comme demandé (ex. `04-soc_docker-ps-up.png`)
- Déplacer dans le bon dossier (jamais de `.env`, tokens, clés privées, mots de passe)

---

## Étape 4.0 — Trouver `IP_SOC`
Depuis Proxmox ou directement sur `docker-soc01` (SSH) :

```bash
hostname -I
```

Le résultat = `IP_SOC` (celle à utiliser pour ouvrir l’UI Wazuh/Grafana).

---

## Étape 4.1 — Déployer Wazuh/Grafana (docker-compose)
1. SSH sur `docker-soc01`
2. Aller dans le dossier `soc/` du repo
3. Préparer `.env` puis lancer

```bash
cd ~/Desktop/Projet/soc
cp .env.example .env
```

Éditer `~/.env` et mettre des mots de passe forts. **Ne pas committer `.env`.**

Puis :

```bash
docker compose up -d
docker compose ps
```

### Validation attendue
- `wazuh-indexer`, `wazuh-manager`, `wazuh-dashboard`, `grafana` en état **Up**

### 📸 Capture obligatoire (4.1)
- Fichier : `04-soc_docker-ps-up.png`
- Où capturer : Terminal après `docker compose ps`

---

## Étape 4.2 — Ouvrir l’UI Wazuh
1. Ouvrir le navigateur sur :
   - `https://IP_SOC` (dash Wazuh, port 443 mappé)
2. Accepter le certificat auto-signé si demandé
3. Vérifier que la page login ou le dashboard s’affiche

### 📸 Capture obligatoire (4.2)
- Fichier : `04-soc_wazuh-dashboard.png`

---

## Étape 4.3 — Enrôler 3 agents minimum
### Cibles minimales recommandées
1. `docker-soc01`
2. `ad-dc01`
3. 1 autre VM Linux

### Où
Wazuh → menu **Agents** → **Summary**

### Validation attendue
- Au moins **3 agents** en statut **Active** (verts)

### 📸 Capture obligatoire (4.3)
- Fichier : `04-soc_wazuh-agents-actifs.png`

---

## Étape 4.4 — Alerte 1 : Brute force SSH
### But
Provoquer des échecs d’auth SSH (pour générer une alerte Wazuh).

### Où lancer le test
Depuis une **VM de test** (pas le serveur OVH public).  
Cible recommandée : une VM **avec agent Wazuh actif** et **SSH**.

### Commande type
Remplacer :
- `IP_CIBLE` = IP de la VM cible SSH (celle enrôlée Wazuh)

```bash
for i in {1..8}; do
  ssh -o StrictHostKeyChecking=no fakeuser@IP_CIBLE 'exit' || true
done
```

Attendu : des tentatives échouées → alerte SSH (failed/bruteforce) dans Wazuh.

### Où vérifier l’alerte
Wazuh → **Alerts** (filtrer si nécessaire par hôte/temps)

### 📸 Capture obligatoire (4.4)
- Fichier : `04-soc_wazuh-alerte-ssh-bruteforce.png`
- Ce qu’il faut montrer : l’alerte SSH brute force/failed dans Wazuh

---

## Étape 4.5 — Alerte 2 : Échec logon AD (ex. 4625)
### But
Générer des tentatives de connexion AD invalides pour remonter des events (souvent 4625).

### Où lancer le test
Depuis un poste joint au domaine (ou via mécanisme d’auth AD du lab).

### Action
Tenter plusieurs logons invalides (mauvais mot de passe / user inconnu / échec volontaire).

### Où vérifier l’alerte
Wazuh → **Alerts**

Attendu : alerte “AD failed logon” (ex. événements 4625 remontés côté Wazuh).

### 📸 Capture obligatoire (4.5)
- Fichier : `04-soc_wazuh-alerte-ad-failed-logon.png`

---

## Étape 4.6 — Alerte 3 : Scan de ports (nmap)
### But
Provoquer une activité réseau type scan (nmap) pour remonter une alerte.

### Où lancer le test
Depuis `lab-rt01` vers une cible du lab (idéalement une VM avec agent Wazuh actif).

### Commande type
Remplacer :
- `IP_CIBLE_LAB` = IP de la cible à scanner

```bash
nmap -sS IP_CIBLE_LAB
```

### Où vérifier l’alerte
Wazuh → **Alerts**

Attendu : alerte “scan / activité suspecte”.

### 📸 Capture obligatoire (4.6)
- Fichier : `04-soc_wazuh-alerte-port-scan.png`

---

## Étape 4.7 — Dashboard exploitable
### Option recommandée (rapide)
Utiliser le dashboard Wazuh natif.

### Option Grafana
Ouvrir :
`http://IP_SOC:3000`

### Validation attendue
- Dashboard lisible
- On voit au moins : agents et/ou volume d’alertes

### 📸 Capture obligatoire (4.7)
- Fichier : `04-soc_grafana-dashboard.png`

---

## Étape 4.8 — Tableau final “preuves MVP”
Mettre un mini tableau dans `docs/livrables/soc-mvp-preuves.md` :

| Scénario | Heure action | Agent/source | Règle/ID alerte | Capture |
|---------|---------------|--------------|------------------|---------|
| SSH bruteforce | hh:mm | vm-test | rule-id | png |
| AD failed logon | hh:mm | ad-dc01 | rule-id | png |
| Port scan | hh:mm | lab-rt01 | rule-id | png |

### 📸 Capture obligatoire (4.8)
- Fichier : `04-soc_mvp-tableau-preuves.png`
- Où capturer : l’écran montrant le tableau rempli

---

## Critères Go / No-Go (MVP SOC)
- [ ] Stack Wazuh/Grafana en **Up**
- [ ] ≥ 3 agents en **Active**
- [ ] 1 dashboard lisible
- [ ] 3 alertes (SSH brute force + AD failed logon + port scan) prouvées
- [ ] Tableau final des preuves rempli

