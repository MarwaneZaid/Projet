#!/usr/bin/env python3
"""Upload and install Wazuh agent on Windows via SMB + Service Control Manager."""
from __future__ import annotations

import argparse
import os
import random
import string
import subprocess
import sys
import tempfile
import time

from impacket.dcerpc.v5 import scmr, transport
from impacket.smbconnection import SMBConnection


def rand_name(prefix: str = "WazuhInst") -> str:
    return prefix + "".join(random.choices(string.ascii_letters + string.digits, k=6))


def download_msi(url: str, dest: str) -> None:
    subprocess.check_call(["curl", "-fsSL", url, "-o", dest])


def upload_smb(host: str, user: str, password: str, local_path: str, remote_name: str) -> str:
    conn = SMBConnection(host, host)
    conn.login(user, password)
    share = "C$"
    remote_path = f"Windows\\Temp\\{remote_name}"
    with open(local_path, "rb") as fh:
        data = fh.read()
    offset = 0

    def _cb(max_size: int) -> bytes:
        nonlocal offset
        chunk = data[offset:offset + max_size]
        offset += len(chunk)
        return chunk

    conn.putFile(share, remote_path, _cb)
    return rf"C:\Windows\Temp\{remote_name}"


def run_via_service(host: str, user: str, password: str, command: str, wait: int = 120) -> None:
    string_binding = rf"ncacn_np:{host}[\pipe\svcctl]"
    rpctransport = transport.DCERPCTransportFactory(string_binding)
    rpctransport.set_credentials(user, password)
    dce = rpctransport.get_dce_rpc()
    dce.connect()
    dce.bind(scmr.MSRPC_UUID_SCMR)

    resp = scmr.hROpenSCManagerW(dce)
    scm_handle = resp["lpScHandle"]

    service_name = rand_name()
    bin_path = f'cmd.exe /c {command}'

    try:
        resp = scmr.hRCreateServiceW(
            dce,
            scm_handle,
            service_name,
            service_name,
            lpBinaryPathName=bin_path,
            dwStartType=scmr.SERVICE_DEMAND_START,
        )
        service_handle = resp["lpServiceHandle"]
        scmr.hRStartServiceW(dce, service_handle)
        print(f"[*] Service {service_name} started, waiting {wait}s...")
        time.sleep(wait)
        scmr.hRDeleteService(dce, service_handle)
        scmr.hRCloseServiceHandle(dce, service_handle)
    finally:
        scmr.hRCloseServiceHandle(dce, scm_handle)
        dce.disconnect()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="192.168.20.17")
    parser.add_argument("--user", default="nexa-admin")
    parser.add_argument("--password", default="NexaMind2026!")
    parser.add_argument("--manager", default="192.168.20.22")
    parser.add_argument("--agent-name", default="client-win-1")
    parser.add_argument("--msi-url", default="https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.2-1.msi")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        msi_local = os.path.join(tmp, "wazuh-agent.msi")
        print(f"[*] Downloading {args.msi_url}")
        download_msi(args.msi_url, msi_local)

        remote_msi = upload_smb(args.host, args.user, args.password, msi_local, "wazuh-agent-4.9.2-1.msi")
        print(f"[*] Uploaded to {remote_msi}")

        install_cmd = (
            f'msiexec /i "{remote_msi}" /qn '
            f'WAZUH_MANAGER={args.manager} WAZUH_AGENT_NAME={args.agent_name} '
            f'&& sc config WazuhSvc start= auto && net start WazuhSvc'
        )
        print(f"[*] Installing via remote service on {args.host}...")
        run_via_service(args.host, args.user, args.password, install_cmd, wait=180)
        print("[*] Done — verify agent in Wazuh UI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
