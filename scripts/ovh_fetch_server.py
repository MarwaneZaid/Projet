#!/usr/bin/env python3
"""
Lit les infos serveur OVH via l'API et affiche un résumé pour specs-materiel.md.

Prérequis : pip3 install ovh
Fichier .env à la racine du projet (voir ovh.env.example)

Usage:
  python3 scripts/ovh_fetch_server.py
"""

from __future__ import annotations

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


def get_client():
    try:
        import ovh
    except ImportError:
        print("pip3 install ovh", file=sys.stderr)
        sys.exit(1)

    load_dotenv()
    endpoint = os.environ.get("OVH_ENDPOINT", "ovh-eu")
    key = os.environ.get("OVH_APPLICATION_KEY", "").strip()
    secret = os.environ.get("OVH_APPLICATION_SECRET", "").strip()
    consumer = os.environ.get("OVH_CONSUMER_KEY", "").strip()
    if not all([key, secret, consumer]):
        print(
            "Remplir .env (voir ovh.env.example) ou exporter les 3 variables OVH_*\n"
            "Guide : docs/infra/ovh-api.md",
            file=sys.stderr,
        )
        sys.exit(1)
    return ovh.Client(
        endpoint=endpoint,
        application_key=key,
        application_secret=secret,
        consumer_key=consumer,
    )


def main() -> None:
    client = get_client()

    print("=== GET /me ===")
    me = client.get("/me")
    print(f"  Compte : {me.get('nichandle')} — {me.get('firstname')} {me.get('name')}")

    print("\n=== Serveurs dédiés GET /dedicated/server ===")
    try:
        dedicated = client.get("/dedicated/server")
        if dedicated:
            for name in dedicated:
                info = client.get(f"/dedicated/server/{name}")
                ips = client.get(f"/dedicated/server/{name}/ips")
                print(f"\n  [{name}]")
                print(f"    Commercial : {info.get('commercialRange')} — {info.get('datacenter')}")
                print(f"    OS : {info.get('os')}")
                print(f"    IP : {', '.join(ips[:3])}{'...' if len(ips) > 3 else ''}")
        else:
            print("  (aucun)")
    except Exception as e:
        print(f"  — {e}")

    print("\n=== VPS GET /vps ===")
    try:
        vps_list = client.get("/vps")
        if vps_list:
            for name in vps_list:
                info = client.get(f"/vps/{name}")
                print(f"\n  [{name}]")
                print(f"    Modèle : {info.get('model', {}).get('name')}")
                print(f"    Datacenter : {info.get('datacenter')}")
                print(f"    IP : {info.get('ips')}")
        else:
            print("  (aucun)")
    except Exception as e:
        print(f"  — {e}")

    print("\n--- Copier ces valeurs dans docs/architecture/specs-materiel.md ---\n")


if __name__ == "__main__":
    main()
