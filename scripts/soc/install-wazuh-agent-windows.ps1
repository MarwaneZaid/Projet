# Install Wazuh agent 4.9.2 on Windows — run as Administrator on client-win-1.
# Manager: srv-wazuh-1 (192.168.20.22)

$ErrorActionPreference = 'Stop'
$Manager = '192.168.20.22'
$AgentName = 'client-win-1'
$MsiUrl = 'https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.2-1.msi'
$MsiPath = "$env:TEMP\wazuh-agent-4.9.2-1.msi"

Write-Host "Downloading Wazuh agent from $MsiUrl ..."
Invoke-WebRequest -Uri $MsiUrl -OutFile $MsiPath -UseBasicParsing

Write-Host "Installing (manager=$Manager, name=$AgentName) ..."
$args = @(
  '/i', $MsiPath,
  '/qn',
  "WAZUH_MANAGER=$Manager",
  "WAZUH_AGENT_NAME=$AgentName",
  'WAZUH_REGISTRATION_SERVER=',
  'WAZUH_KEEP_ALIVE_INTERVAL=60',
  'WAZUH_TIME_RECONNECT=60',
  'WAZUH_REGISTRATION_PORT=1515',
  'WAZUH_PROTOCOL=tcp',
  'WAZUH_NOTIFY_TIME=10',
  'WAZUH_ENABLE_SYSCHECK=true',
  'WAZUH_ENABLE_ROOTCHECK=true',
  'WAZUH_ENABLE_SCA=true',
  'WAZUH_ENABLE_ACTIVE_RESPONSE=true'
)
Start-Process msiexec.exe -ArgumentList $args -Wait -NoNewWindow

$svc = Get-Service -Name 'WazuhSvc' -ErrorAction SilentlyContinue
if ($svc) {
  Set-Service -Name 'WazuhSvc' -StartupType Automatic
  Restart-Service -Name 'WazuhSvc' -Force
  Write-Host "WazuhSvc status: $((Get-Service WazuhSvc).Status)"
} else {
  Write-Warning 'WazuhSvc service not found — check MSI install log'
}

Write-Host 'Done. Verify in Wazuh UI: Endpoints Summary -> client-win-1 Active'
