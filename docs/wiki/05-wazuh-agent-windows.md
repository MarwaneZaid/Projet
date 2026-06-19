# Agent Wazuh Windows — installation manuelle (2 min)

**Manager :** `192.168.20.22` · **Version agent :** `4.9.2-1`

## Situation actuelle (18 juin 2026)

| VM | IP | RDP | Agent Wazuh |
|----|-----|-----|-------------|
| `client-win-1` (106) | 192.168.20.13 | ❌ VM éteinte / injoignable | À faire |
| `win10-tempon` (105) | 192.168.20.17 | ✅ accessible | Compte `nexa-admin` **sans droits admin** — installer en **Administrateur** |

**Linux AD (`srv-ad-1`) :** agent installé et **Active** ✅

## Option A — `win10-tempon` (105) via RDP

1. Connexion RDP : `192.168.20.17` (compte **Administrateur** local ou domaine)
2. PowerShell **en tant qu’administrateur** :

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
$Manager = '192.168.20.22'
$AgentName = 'win10-tempon'
$Msi = "$env:TEMP\wazuh-agent-4.9.2-1.msi"
Invoke-WebRequest -Uri 'https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.2-1.msi' -OutFile $Msi
msiexec /i $Msi /qn WAZUH_MANAGER=$Manager WAZUH_AGENT_NAME=$AgentName
Set-Service WazuhSvc -StartupType Automatic
Restart-Service WazuhSvc
Get-Service WazuhSvc
```

3. Vérifier : `https://192.168.20.22` → **Endpoints Summary** → `win10-tempon` **Active**

Script complet : [install-wazuh-agent-windows.ps1](../../scripts/soc/install-wazuh-agent-windows.ps1)

## Option B — `client-win-1` (106)

1. Proxmox → VM **106** → **Start**
2. Attendre IP `192.168.20.13` (console Proxmox ou `arp-scan`)
3. RDP + même script PowerShell avec `WAZUH_AGENT_NAME=client-win-1`

## Dépannage

| Symptôme | Action |
|----------|--------|
| Agent `Never connected` | `Test-NetConnection 192.168.20.22 -Port 1514` depuis Windows |
| Ports fermés | Règles pfSense 1514/1515 → `.22` ([pfsense-regles-wazuh.md](../procedures/pfsense-regles-wazuh.md)) |
| Version mismatch | Agent **4.9.2** = manager Docker **4.9.2** |

## Preuve livrable

Capture : `docs/livrables/screenshots/04-soc/04-soc_wazuh-agents-3plus.png`
