#!/usr/bin/env python3
"""
Importe listes, labels et cartes sur le board Trello du projet.

Usage:
  export TRELLO_API_KEY="..."
  export TRELLO_TOKEN="..."
  python3 scripts/trello_import.py

Optionnel:
  export TRELLO_BOARD_ID="uPZIvZwK"   # shortLink par défaut
  export TRELLO_DRY_RUN=1             # affiche sans créer
"""

from __future__ import annotations

import csv
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.trello.com/1"
BOARD_SHORT = os.environ.get("TRELLO_BOARD_ID", "uPZIvZwK")
CSV_PATH = Path(__file__).resolve().parent.parent / "docs" / "trello" / "import.csv"

LABELS = {
    "E1-Infra": "green",
    "E2-Réseau": "blue",
    "E3-SOC": "purple",
    "E4-RedTeam": "red",
    "Livrable": "yellow",
    "Bloquant": "red",
    "Optionnel": "black",
}


def api(method: str, path: str, params: dict | None = None, body: dict | None = None) -> dict | list:
    key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    if not key or not token:
        print("Erreur: définir TRELLO_API_KEY et TRELLO_TOKEN", file=sys.stderr)
        print("  https://trello.com/app-key", file=sys.stderr)
        sys.exit(1)

    q = {"key": key, "token": token}
    if params:
        q.update(params)
    url = f"{API}{path}?{urllib.parse.urlencode(q)}"
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = urllib.parse.urlencode(body).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return {} if not raw else __import__("json").loads(raw)
    except urllib.error.HTTPError as e:
        print(f"API {method} {path} → {e.code}: {e.read().decode()}", file=sys.stderr)
        raise


def dry() -> bool:
    return os.environ.get("TRELLO_DRY_RUN", "").lower() in ("1", "true", "yes")


def get_board_id() -> str:
    board = api("GET", f"/boards/{BOARD_SHORT}", {"fields": "id,name"})
    print(f"Board: {board['name']} ({board['id']})")
    return board["id"]


def ensure_labels(board_id: str) -> dict[str, str]:
    existing = {lb["name"]: lb["id"] for lb in api("GET", f"/boards/{board_id}/labels")}
    ids: dict[str, str] = {}
    for name, color in LABELS.items():
        if name in existing:
            ids[name] = existing[name]
            continue
        if dry():
            print(f"[dry] label: {name}")
            ids[name] = f"dry-{name}"
            continue
        lb = api("POST", "/labels", body={"name": name, "color": color, "idBoard": board_id})
        ids[name] = lb["id"]
        print(f"Label créé: {name}")
    return ids


def get_or_create_list(board_id: str, name: str, cache: dict[str, str]) -> str:
    if name in cache:
        return cache[name]
    lists = api("GET", f"/boards/{board_id}/lists", {"filter": "open"})
    for lst in lists:
        if lst["name"] == name:
            cache[name] = lst["id"]
            return lst["id"]
    if dry():
        print(f"[dry] liste: {name}")
        cache[name] = f"dry-list-{name}"
        return cache[name]
    lst = api("POST", "/lists", body={"name": name, "idBoard": board_id})
    cache[name] = lst["id"]
    print(f"Liste créée: {name}")
    return lst["id"]


def create_card(
    list_id: str,
    title: str,
    desc: str,
    due: str,
    label_ids: list[str],
) -> None:
    body: dict[str, str] = {"name": title, "idList": list_id, "pos": "bottom"}
    if desc:
        body["desc"] = desc
    if due:
        body["due"] = f"{due}T17:00:00.000Z"
    if label_ids:
        body["idLabels"] = ",".join(label_ids)

    if dry():
        print(f"[dry] carte: {title} ({due})")
        return
    api("POST", "/cards", body=body)


def load_csv() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with CSV_PATH.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def main() -> None:
    if not CSV_PATH.exists():
        print(f"CSV introuvable: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    board_id = get_board_id()
    label_ids = ensure_labels(board_id)
    list_cache: dict[str, str] = {}
    cards = load_csv()

    print(f"Import de {len(cards)} cartes…")
    for row in cards:
        list_name = row["List"].strip()
        list_id = get_or_create_list(board_id, list_name, list_cache)
        labels_raw = row.get("Labels", "").strip()
        lids = []
        for part in labels_raw.replace(",", ";").split(";"):
            name = part.strip()
            if name and name in label_ids:
                lids.append(label_ids[name])
        create_card(
            list_id,
            row["Title"].strip(),
            row.get("Description", "").strip(),
            row.get("Due Date", "").strip(),
            lids,
        )

    print("Terminé. Ouvrez:", f"https://trello.com/b/{BOARD_SHORT}/projet")


if __name__ == "__main__":
    main()
