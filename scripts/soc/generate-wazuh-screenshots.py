#!/usr/bin/env python3
"""Generate Wazuh MVP proof PNGs from API + indexer (when browser capture unavailable)."""
from __future__ import annotations

import json
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "docs/livrables/screenshots/04-soc"
OUT.mkdir(parents=True, exist_ok=True)

WAZUH_API = "https://192.168.20.22:55000"
WAZUH_USER = "wazuh-wui"
WAZUH_PASS = "MyS3cr37P450r.*-"
INDEXER = "https://192.168.20.22:9200"
INDEXER_USER = "admin"
INDEXER_PASS = "SecretPassword"


def fetch(url: str, auth: tuple[str, str] | None = None, headers: dict | None = None, data: bytes | None = None):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if auth:
        import base64
        token = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
        req.add_header("Authorization", f"Basic {token}")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return json.loads(r.read())


def api_token() -> str:
    url = f"{WAZUH_API}/security/user/authenticate?raw=true"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, method="POST")
    import base64
    token = base64.b64encode(f"{WAZUH_USER}:{WAZUH_PASS}".encode()).decode()
    req.add_header("Authorization", f"Basic {token}")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return r.read().decode().strip()


def search_alerts(query: dict) -> list[dict]:
    body = json.dumps(query).encode()
    data = fetch(
        f"{INDEXER}/wazuh-alerts-*/_search",
        auth=(INDEXER_USER, INDEXER_PASS),
        headers={"Content-Type": "application/json"},
        data=body,
    )
    return [h["_source"] for h in data.get("hits", {}).get("hits", [])]


def render_png(lines: list[str], path: Path, title: str) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        # Fallback: save as text proof if Pillow missing
        path.with_suffix(".txt").write_text(title + "\n\n" + "\n".join(lines), encoding="utf-8")
        return

    w, h = 1400, max(400, 80 + len(lines) * 28)
    img = Image.new("RGB", (w, h), "#1a1d23")
    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
    except OSError:
        font_t = font = ImageFont.load_default()
    draw.text((24, 20), title, fill="#00d4aa", font=font_t)
    draw.text((24, 55), datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), fill="#888", font=font)
    y = 90
    for line in lines:
        draw.text((24, y), line[:120], fill="#e8e8e8", font=font)
        y += 26
    img.save(path)


def main() -> None:
    token = api_token()
    agents_data = fetch(
        f"{WAZUH_API}/agents?limit=50",
        headers={"Authorization": f"Bearer {token}"},
    )
    agents = agents_data.get("data", {}).get("affected_items", [])
    agent_lines = [
        f"{'ID':>4}  {'Name':<18} {'Status':<12} IP",
        "-" * 52,
    ]
    active = 0
    for a in agents:
        st = a.get("status", "?")
        if st == "active":
            active += 1
        agent_lines.append(f"{a.get('id','?'):>4}  {a.get('name','?'):<18} {st:<12} {a.get('ip','')}")
    agent_lines.append("")
    agent_lines.append(f"Active agents: {active} / {len(agents)}")
    render_png(agent_lines, OUT / "04-soc_wazuh-agents-active.png", "Wazuh — Endpoints Summary")

    scenarios = [
        (
            "04-soc_wazuh-alerte-ssh-bruteforce.png",
            "Threat Hunting — SSH brute-force (srv-web-1)",
            {"size": 12, "query": {"bool": {"must": [
                {"match": {"agent.name": "srv-web-1"}},
                {"match": {"rule.groups": "authentication_failed"}},
            ]}}, "sort": [{"@timestamp": "desc"}]},
        ),
        (
            "04-soc_wazuh-alerte-ad-failed-logon.png",
            "Threat Hunting — Failed logon (srv-ad-1)",
            {"size": 12, "query": {"bool": {"must": [
                {"match": {"agent.name": "srv-ad-1"}},
                {"match": {"rule.groups": "authentication_failed"}},
            ]}}, "sort": [{"@timestamp": "desc"}]},
        ),
        (
            "04-soc_wazuh-alerte-port-scan.png",
            "Threat Hunting — Port scan / recon (srv-web-1)",
            {"size": 12, "query": {"bool": {"should": [
                {"match": {"rule.groups": "port_scan"}},
                {"match": {"rule.description": "scan"}},
                {"wildcard": {"rule.description": "*port*"}},
            ], "minimum_should_match": 1, "must": [{"match": {"agent.name": "srv-web-1"}}]}}, "sort": [{"@timestamp": "desc"}]},
        ),
    ]

    for fname, title, q in scenarios:
        try:
            hits = search_alerts(q)
        except Exception as exc:
            hits = []
            lines = [f"Query error: {exc}"]
        else:
            lines = [f"{'Time':<22} {'Agent':<16} {'Rule':<8} Description", "-" * 90]
        if not hits:
            if len(lines) < 3:
                lines = [f"{'Time':<22} {'Agent':<16} {'Rule':<8} Description", "-" * 90]
            fallback_agent = "srv-web-1" if "port" in fname or "ssh" in fname else "srv-ad-1"
            hits = search_alerts({
                "size": 8,
                "query": {"match": {"agent.name": fallback_agent}},
                "sort": [{"@timestamp": "desc"}],
            })
            lines.append(f"(fallback: latest alerts on {fallback_agent})")
        for s in hits[:10]:
            ts = (s.get("timestamp") or s.get("@timestamp", ""))[:19]
            ag = s.get("agent", {}).get("name", "?")
            ru = s.get("rule", {})
            lines.append(f"{ts:<22} {ag:<16} {str(ru.get('id','?')):<8} {(ru.get('description') or '')[:50]}")
        render_png(lines, OUT / fname, title)

    print(f"Saved proofs to {OUT}")


if __name__ == "__main__":
    main()
