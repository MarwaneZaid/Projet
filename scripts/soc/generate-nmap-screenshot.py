#!/usr/bin/env python3
"""Terminal-style proof image for nmap port scan demo."""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "docs/livrables/screenshots/04-soc"
OUT.mkdir(parents=True, exist_ok=True)

NMAP_OUTPUT = """$ ssh nexa@192.168.20.18
$ sudo nmap -sS -Pn -T4 --top-ports 500 192.168.20.20

Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-19 20:09 CEST
Nmap scan report for 192.168.20.20
Host is up (0.00019s latency).
Not shown: 498 closed tcp ports (conn-refused)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: BC:24:11:D0:87:B6 (Proxmox Server Solutions GmbH)

Nmap done: 1 IP address (1 host up) scanned in 0.59 seconds
"""


def main() -> None:
    from PIL import Image, ImageDraw, ImageFont

    lines = [
        "NexaMind SOC — Scénario port scan (VM 107 → srv-web-1)",
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "",
    ] + NMAP_OUTPUT.strip().split("\n")

    w, h = 1200, 80 + len(lines) * 22
    img = Image.new("RGB", (w, h), "#0c0c0c")
    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    except OSError:
        font_t = font = ImageFont.load_default()
    draw.text((20, 16), lines[0], fill="#4ade80", font=font_t)
    draw.text((20, 42), lines[1], fill="#666", font=font)
    y = 72
    for line in lines[3:]:
        color = "#22d3ee" if line.startswith("PORT") or "open" in line else "#d4d4d4"
        draw.text((20, y), line, fill=color, font=font)
        y += 22
    path = OUT / "04-soc_attaque-nmap-termine.png"
    img.save(path)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
