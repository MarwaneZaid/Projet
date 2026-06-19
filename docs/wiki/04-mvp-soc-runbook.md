# Leçon 4 — MVP SOC (Wazuh + agents + dashboard + 3 alertes)

**Périmètre strict :** cette leçon ne touche **que** au SOC.  
**Responsable :** Étudiant 3  
**Prérequis :** VM `docker-soc01` accessible en SSH, réseau OK vers AD et 1 VM Linux

**Objectif MVP :**

- [ ] Wazuh déployé sur `docker-soc01`
- [ ] 3 agents actifs minimum
- [ ] 1 dashboard exploitable
- [ ] 3 alertes démontrées avec preuve

**Captures détaillées :** [screenshots-par-etape.md § Leçon 4](screenshots-par-etape.md#leçon-4--mvp-soc-seulement)  
**Dossier captures :** `docs/livrables/screenshots/04-soc/`

---

## Étape 4.1 — Déployer la stack Wazuh/Grafana

### Où

SSH vers `docker-soc01`, puis dossier du repo `soc/`.

### Commandes

```bash
cd ~/Desktop/Projet/soc
cp .env.example .env
```

Éditer `.env` avec des mots de passe forts (ne pas commiter `.env`), puis :

```bash
docker compose up -d
docker compose ps
```

### Validation

- `wazuh-indexer`, `wazuh-manager`, `wazuh-dashboard`, `grafana` en état `Up`.

### 📸 Capture obligatoire

- Fichier : `04-soc_docker-ps-up.png`

---

## Étape 4.2 — Ouvrir et valider l’UI Wazuh

### Où

Navigateur : `https://IP_SOC` (port 443 mappé sur `wazuh-dashboard`).

### Validation

- La page login ou dashboard s’affiche.

### 📸 Capture obligatoire

- Fichier : `04-soc_wazuh-dashboard.png`

---

## Étape 4.3 — Enrôler 3 agents minimum

### Cibles minimales recommandées

1. `srv-wazuh-1` (agent local manager) ✅
2. `srv-web-1` (portail) ✅
3. `srv-ad-1` (Samba AD) ✅
4. `client-win-1` ou `win10-tempon` (Windows) — [guide Windows](05-wazuh-agent-windows.md)

### Installation Linux (manager `192.168.20.22`)

```bash
# Sur la VM cible (ex. srv-ad-1)
sudo bash scripts/soc/install-wazuh-agent-linux.sh
```

### Où

Dans Wazuh : menu **Endpoints Summary**.

### Validation

- Au moins 3 agents en statut `Active` (Linux OK) + Windows si possible.

### 📸 Capture obligatoire

- Fichier : `04-soc_wazuh-agents-actifs.png`

---

## Étape 4.4 — Créer 1 dashboard utile

### Option A (recommandée pour MVP rapide)

Utiliser le dashboard Wazuh natif.

### Option B

Grafana `http://IP_SOC:3000` avec un dashboard :

- nombre d’agents actifs,
- volume d’alertes,
- top règles.

### 📸 Capture obligatoire

- Fichier : `04-soc_grafana-dashboard.png` (ou dashboard Wazuh si vous restez natif)

---

## Étape 4.5 — Démontrer 3 alertes (preuve obligatoire)

Tu dois faire **3 scénarios** et vérifier l’alerte correspondante dans Wazuh.

### Alerte 1 — Brute force SSH

Depuis une VM de test (pas le serveur OVH public) :

```bash
for i in {1..8}; do ssh fakeuser@IP_CIBLE; done
```

Attendu : alertes SSH failed/bruteforce.

### Alerte 2 — Échec logon AD

Sur poste joint au domaine, faire plusieurs connexions AD invalides.

Attendu : événements AD (ex. 4625) visibles côté Wazuh.

### Alerte 3 — Scan de ports

Depuis `lab-rt01` vers une cible de lab :

```bash
nmap -sS IP_CIBLE_LAB
```

Attendu : alerte scan/activité réseau suspecte côté Wazuh.

### 📸 Captures obligatoires

- `04-soc_wazuh-alerte-ssh-bruteforce.png`
- `04-soc_wazuh-alerte-ad-failed-logon.png`
- `04-soc_wazuh-alerte-port-scan.png`

---

## Étape 4.6 — Tableau de preuve final MVP

Créer un mini tableau dans un fichier de notes (`docs/livrables/soc-mvp-preuves.md`) :

| Scénario | Heure action | Agent/source | Règle/ID alerte | Capture |
|---------|---------------|--------------|------------------|---------|
| SSH bruteforce | hh:mm | vm-test | rule-id | png |
| AD failed logon | hh:mm | ad-dc01 | rule-id | png |
| Port scan | hh:mm | lab-rt01 | rule-id | png |

### 📸 Capture obligatoire

- Fichier : `04-soc_mvp-tableau-preuves.png`

---

## Critères de fin (Go / No-Go)

Le MVP SOC est validé uniquement si :

- [ ] Stack Wazuh/Grafana en `Up`
- [ ] 3 agents `Active`
- [ ] Dashboard lisible
- [ ] 3 alertes différentes prouvées
- [ ] Tableau final des preuves rempli

---

## Ce que tu ne dois pas faire dans ce MVP

- Ne pas déployer TheHive/Cortex/n8n si le MVP de base n’est pas validé.
- Ne pas modifier AD, Red Team, portail hors besoin strict d’enrôlement agent/test.
- Ne pas commiter `.env` ni secrets.
