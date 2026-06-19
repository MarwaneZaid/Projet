#!/usr/bin/env python3
"""
Active le firewall Edge OVH sur 51.77.52.56 et autorise SSH + Proxmox pour une IP.

Usage:
  cp ovh.env.example .env   # remplir clés API
  pip3 install ovh
  python3 scripts/ovh_configure_firewall.py --allow 46.193.6.82

Variables .env optionnelles:
  OVH_SERVER_IP=51.77.52.56
  TEAM_ALLOW_IP=46.193.6.82
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def client():
    try:
        import ovh
    except ImportError:
        print("pip3 install ovh", file=sys.stderr)
        sys.exit(1)
    load_dotenv()
    key = os.environ.get("OVH_APPLICATION_KEY", "").strip()
    secret = os.environ.get("OVH_APPLICATION_SECRET", "").strip()
    consumer = os.environ.get("OVH_CONSUMER_KEY", "").strip()
    if not all([key, secret, consumer]):
        print("Configurer .env (voir ovh.env.example)", file=sys.stderr)
        sys.exit(1)
    return ovh.Client(
        endpoint=os.environ.get("OVH_ENDPOINT", "ovh-eu"),
        application_key=key,
        application_secret=secret,
        consumer_key=consumer,
    )


def add_rule(c, ip: str, seq: int, action: str, proto: str, dest_port: int | None, src: str) -> None:
    body: dict = {
        "action": action,
        "protocol": proto,
        "sequence": seq,
        "source": src,
    }
    if dest_port is not None:
        if proto == "tcp":
            body["destinationPort"] = dest_port
        else:
            body["destinationPort"] = dest_port
    c.post(f"/ip/{ip}/firewall/{ip}/rule", **body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow",
        default=os.environ.get("TEAM_ALLOW_IP", ""),
        help="IP publique à autoriser (ex: 46.193.6.82)",
    )
    parser.add_argument(
        "--ip",
        default=os.environ.get("OVH_SERVER_IP", "51.77.52.56"),
        help="IP serveur OVH",
    )
    args = parser.parse_args()
    if not args.allow:
        print("Indiquer --allow VOTRE_IP", file=sys.stderr)
        sys.exit(1)

    allow = args.allow if "/" in args.allow else f"{args.allow}/32"
    ip = args.ip
    c = client()

    print(f"Activation firewall sur {ip}...")
    try:
        c.post(f"/ip/{ip}/firewall/{ip}/enable")
    except Exception as e:
        if "already" not in str(e).lower():
            print(f"  enable: {e}")

    print(f"Règles pour {allow}...")
    add_rule(c, ip, 0, "permit", "tcp", 22, allow)
    add_rule(c, ip, 1, "permit", "tcp", 8006, allow)
    add_rule(c, ip, 2, "deny", "ipv4", None, "0.0.0.0/0")
    print("OK — attendre 1–2 min puis : nc -zv", ip, "22 8006")


if __name__ == "__main__":
    main()
