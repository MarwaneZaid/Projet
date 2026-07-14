#!/usr/bin/env python3
"""Generate Red Team proof PNGs from live lab (VPN required)."""
from __future__ import annotations

import json
import ssl
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/livrables/screenshots/05-red-team"
OUT.mkdir(parents=True, exist_ok=True)

SSH_USER = "nexa"
SSH_PASS = "NexaMind2026!"
ATTACKER = "192.168.20.18"
PORTAIL = "192.168.20.20"
AD = "192.168.20.16"

WAZUH_API = "https://192.168.20.22:55000"
WAZUH_USER = "wazuh-wui"
WAZUH_PASS = "MyS3cr37P450r.*-"
INDEXER = "https://192.168.20.22:9200"
INDEXER_USER = "admin"
INDEXER_PASS = "SecretPassword"


def ssh(host: str, cmd: str, timeout: int = 120) -> str:
    r = subprocess.run(
        [
            "sshpass", "-e", "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=8",
            f"{SSH_USER}@{host}",
            cmd,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**subprocess.os.environ, "SSHPASS": SSH_PASS},
    )
    return (r.stdout + r.stderr).strip()


def render_png(lines: list[str], path: Path, title: str, width: int = 1450) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        path.with_suffix(".txt").write_text(title + "\n\n" + "\n".join(lines), encoding="utf-8")
        print(f"  (txt fallback) {path.with_suffix('.txt')}")
        return

    h = max(380, 95 + len(lines) * 24)
    img = Image.new("RGB", (width, h), "#0f1419")
    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    except OSError:
        font_t = font = ImageFont.load_default()

    draw.text((20, 14), title, fill="#f97316", font=font_t)
    draw.text(
        (20, 44),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC · NexaMind Red Team · VM 107"),
        fill="#6b7280",
        font=font,
    )
    y = 78
    for line in lines:
        low = line.lower()
        if any(x in low for x in ("rt-0", ">>>", "====", "mitre", "nmap scan report")):
            color = "#38bdf8"
        elif any(x in low for x in ("open", "fin rt", "terminé", "ok", "active")):
            color = "#4ade80"
        elif any(x in low for x in ("tentative", "failed", "ssh")):
            color = "#fbbf24"
        else:
            color = "#e5e7eb"
        draw.text((20, y), line[:135], fill=color, font=font)
        y += 24
    img.save(path)
    print(f"  {path}")


def wazuh_token() -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(f"{WAZUH_API}/security/user/authenticate?raw=true", method="POST")
    import base64
    tok = base64.b64encode(f"{WAZUH_USER}:{WAZUH_PASS}".encode()).decode()
    req.add_header("Authorization", f"Basic {tok}")
    with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
        return r.read().decode().strip()


def search_alerts(query: dict) -> list[dict]:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    body = json.dumps(query).encode()
    import base64
    tok = base64.b64encode(f"{INDEXER_USER}:{INDEXER_PASS}".encode()).decode()
    req = urllib.request.Request(
        f"{INDEXER}/wazuh-alerts-*/_search",
        data=body,
        method="POST",
    )
    req.add_header("Authorization", f"Basic {tok}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        data = json.loads(r.read())
    return [h["_source"] for h in data.get("hits", {}).get("hits", [])]


def alert_lines(agent: str, groups: str | None = None, limit: int = 8) -> list[str]:
    must = [{"match": {"agent.name": agent}}]
    if groups:
        must.append({"match": {"rule.groups": groups}})
    q = {"size": limit, "query": {"bool": {"must": must}}, "sort": [{"@timestamp": "desc"}]}
    hits = search_alerts(q)
    if not hits:
        hits = search_alerts({"size": limit, "query": {"match": {"agent.name": agent}}, "sort": [{"@timestamp": "desc"}]})
    lines = [f"{'Time':<20} {'Rule':<8} Description", "-" * 85]
    for s in hits:
        ts = (s.get("timestamp") or s.get("@timestamp", ""))[:19]
        ru = s.get("rule", {})
        lines.append(f"{ts:<20} {str(ru.get('id', '?')):<8} {(ru.get('description') or '')[:55]}")
    return lines


def main() -> None:
    print("[*] Running Red Team on VM 107…")
    run_out = ssh(ATTACKER, "PAUSE=2 bash ~/redteam/run-all.sh 2>&1", timeout=180)

    run_lines = run_out.splitlines()
    render_png(
        run_lines[:45] if len(run_lines) > 45 else run_lines,
        OUT / "05-red-team_terminal-run-all.png",
        "Red Team — run-all.sh (VM 107 → portail + AD)",
    )

    # Extract RT-02 nmap block
    nmap_block: list[str] = []
    capture = False
    for line in run_lines:
        if "RT-02" in line:
            capture = True
        if capture:
            nmap_block.append(line)
        if capture and "Fin RT-02" in line:
            break
    render_png(
        nmap_block or ["(nmap output missing)"],
        OUT / "05-red-team_scan-nmap-result.png",
        "RT-02 — Port scan nmap → 192.168.20.20",
    )

    # RT-01 brute force block
    bf_block: list[str] = []
    capture = False
    for line in run_lines:
        if "RT-01" in line:
            capture = True
        if capture:
            bf_block.append(line)
        if capture and "Fin RT-01" in line:
            break
    render_png(
        bf_block or ["(bruteforce output missing)"],
        OUT / "05-red-team_bruteforce-ssh-done.png",
        "RT-01 — SSH brute force → portail",
    )

    # RT-03 AD block
    ad_block: list[str] = []
    capture = False
    for line in run_lines:
        if "RT-03" in line:
            capture = True
        if capture:
            ad_block.append(line)
        if capture and "Fin RT-03" in line:
            break
    render_png(
        ad_block or ["(AD output missing)"],
        OUT / "05-red-team_failed-logon-ad-done.png",
        "RT-03 — Failed SSH logon → AD (.16)",
    )

    print("[*] Suricata eve.json (flows .18 → .20)…")
    suri_raw = ssh(
        ATTACKER,
        f"grep '\"dest_ip\":\"{PORTAIL}\"' /var/log/suricata/eve.json 2>/dev/null | "
        f"grep '\"src_ip\":\"{ATTACKER}\"' | tail -8",
        timeout=30,
    )
    suri_lines = ["Suricata eve.json — flows attaquant → portail", ""]
    for raw in suri_raw.splitlines()[:8]:
        try:
            ev = json.loads(raw)
            et = ev.get("event_type", "?")
            ts = ev.get("timestamp", "")[:19]
            if et == "flow":
                fc = ev.get("flow", {})
                suri_lines.append(
                    f"{ts}  flow  {ev.get('src_ip')}:{ev.get('src_port')} → "
                    f"{ev.get('dest_ip')}:{ev.get('dest_port')}  pkts={fc.get('pkts_toserver', '?')}"
                )
            elif et == "alert":
                sig = ev.get("alert", {}).get("signature", "alert")
                suri_lines.append(f"{ts}  ALERT  {sig[:70]}")
            else:
                suri_lines.append(f"{ts}  {et}")
        except json.JSONDecodeError:
            suri_lines.append(raw[:120])
    if len(suri_lines) < 3:
        suri_lines.append("(no recent flows — run-all may need rerun)")
    render_png(suri_lines, OUT / "05-red-team_suricata-eve-flows.png", "Suricata — détection réseau (VM 107)")

    print("[*] Suricata alerts (signatures IDS)…")
    alert_raw = ssh(
        ATTACKER,
        "bash ~/redteam/show-suricata-alerts.sh 2>&1; "
        "echo '---RAW---'; "
        "grep '\"event_type\":\"alert\"' /var/log/suricata/eve.json 2>/dev/null | tail -5",
        timeout=30,
    )
    alert_lines_suri = [
        "Suricata eve.json — event_type: alert (signatures IDS)",
        f"Lab : {ATTACKER} → {PORTAIL} · règles NEXAMIND LAB sid 9000001–9000003",
        "",
    ]
    lab_alerts = 0
    in_raw = False
    for line in alert_raw.splitlines():
        if line == "---RAW---":
            in_raw = True
            alert_lines_suri.append("")
            alert_lines_suri.append("--- grep tail -5 (brut) ---")
            continue
        if not in_raw:
            if line.startswith("★"):
                lab_alerts += 1
            if line.strip() and not line.startswith("[*]") and "====" not in line:
                alert_lines_suri.append(line[:120])
            continue
        raw = line.strip()
        if not raw:
            continue
        try:
            ev = json.loads(raw)
            al = ev.get("alert", {})
            sig = al.get("signature", "?")
            sid = al.get("signature_id", "?")
            ts = ev.get("timestamp", "")[:19]
            src = ev.get("src_ip", "?")
            dst = ev.get("dest_ip", "?")
            alert_lines_suri.append(f"{ts}  [{sid}]  {src} → {dst}  {sig[:50]}")
        except json.JSONDecodeError:
            alert_lines_suri.append(raw[:120])
    if lab_alerts == 0 and "--- grep" not in "\n".join(alert_lines_suri):
        alert_lines_suri.append("(aucune alerte lab — sudo bash ~/redteam/install-suricata-lab-rules.sh)")
    else:
        alert_lines_suri.append("")
        alert_lines_suri.append(f"Alertes lab marquées ★ : {lab_alerts}")
        alert_lines_suri.append(
            "Commande : grep '\"event_type\":\"alert\"' /var/log/suricata/eve.json | tail -5"
        )
    render_png(
        alert_lines_suri,
        OUT / "05-red-team_suricata-eve-alerts.png",
        "Suricata — alertes IDS (double détection réseau)",
    )

    print("[*] Wazuh correlation…")
    try:
        wazuh_token()
        w_lines = ["=== Wazuh alerts (post Red Team) ===", ""] + alert_lines("srv-web-1", "authentication_failed", 6)
        w_lines += ["", "=== srv-ad-1 ===", ""] + alert_lines("srv-ad-1", "authentication_failed", 6)
    except Exception as exc:
        w_lines = [f"Wazuh API error: {exc}", "Open https://192.168.20.22 manually"]
    render_png(w_lines, OUT / "05-red-team_wazuh-alerts-after-attack.png", "Wazuh — alertes après attaque")

    # Journal excerpt
    journal = (ROOT / "docs/livrables/redteam/journal-exercices.md").read_text(encoding="utf-8")
    j_lines = ["Journal exercices Red Team — extrait", ""]
    for line in journal.splitlines():
        if line.startswith("| 2026-"):
            j_lines.append(line)
    render_png(j_lines, OUT / "05-rt_journal-exercice.png", "Journal Red Team (dates / MITRE / SOC)")

    # Correlation side-by-side text
    corr: list[str] = [
        "CORRÉLATION RED TEAM ↔ SOC (NexaMind)",
        "",
        "--- Attaque (VM 107) ---",
    ]
    for line in run_lines:
        if "RT-0" in line and "====" not in line:
            corr.append(line.strip())
        if "Fin RT-" in line:
            corr.append(line.strip())
    corr += ["", "--- Détection Wazuh ---"]
    corr.extend(w_lines[2:12] if len(w_lines) > 2 else w_lines)
    render_png(corr, OUT / "05-rt_correlation-soc.png", "Corrélation attaque + alertes SOC")

    # Machine attaquant overview
    info = ssh(
        ATTACKER,
        "echo HOST=$(hostname); echo IP=$(hostname -I); suricata -V 2>/dev/null | head -1; "
        "systemctl is-active suricata; ls ~/redteam/*.sh 2>/dev/null",
        timeout=20,
    ).splitlines()
    render_png(
        info,
        OUT / "05-red-team_vm107-attacker-overview.png",
        "VM 107 — poste attaquant (Suricata + scripts)",
    )

    print(f"\nDone — {OUT}")


if __name__ == "__main__":
    main()
