#!/usr/bin/env python3
"""
Étape 1 de l'auth OVH : génère l'URL pour obtenir OVH_CONSUMER_KEY.

Usage:
  export OVH_APPLICATION_KEY="..."
  export OVH_APPLICATION_SECRET="..."
  python3 scripts/ovh_create_consumer_key.py

Puis ouvrir l'URL affichée, autoriser, copier le consumer key dans .env
"""

from __future__ import annotations

import os
import sys


def main() -> None:
    app_key = os.environ.get("OVH_APPLICATION_KEY", "").strip()
    app_secret = os.environ.get("OVH_APPLICATION_SECRET", "").strip()
    if not app_key or not app_secret:
        print(
            "Définir OVH_APPLICATION_KEY et OVH_APPLICATION_SECRET\n"
            "Créer l'app sur https://eu.api.ovh.com/createApp/\n"
            "Voir docs/infra/ovh-api.md",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import ovh

        client = ovh.Client(
            endpoint="ovh-eu",
            application_key=app_key,
            application_secret=app_secret,
        )
        ck = client.new_consumer_key_request()
        ck.add_recursive_rules(ovh.API_READ_ONLY)
        validation = ck.request()
    except ImportError:
        print("Installer le module ovh : pip3 install ovh", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur API OVH : {e}", file=sys.stderr)
        sys.exit(1)

    print("\n=== Autorisation OVH ===\n")
    print("1. Ouvrez cette URL dans le navigateur :\n")
    print(f"   {validation['validationUrl']}\n")
    print("2. Connectez-vous et cliquez « Autoriser »\n")
    print("3. Copiez le Consumer Key dans votre fichier .env :\n")
    print(f"   OVH_CONSUMER_KEY={validation['consumerKey']}\n")
    print("(Lecture seule GET /* — suffisant pour inventorier le serveur)\n")


if __name__ == "__main__":
    main()
