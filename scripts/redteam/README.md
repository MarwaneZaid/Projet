# Scripts Red Team — NexaMind

Machine attaque : **VM 107** (`192.168.20.18`)

## Déploiement

```bash
SSHPASS='...' sshpass -e bash scripts/redteam/deploy-to-vm107.sh
```

## Exécution (sur VM 107)

```bash
ssh nexa@192.168.20.18
sudo bash ~/redteam/install-suricata-lab-rules.sh   # une fois — règles sid 9000001–9000003
bash ~/redteam/run-all.sh
bash ~/redteam/show-suricata-alerts.sh              # preuve alertes IDS
grep '"event_type":"alert"' /var/log/suricata/eve.json | tail -5
```

RT-01 utilise **Hydra** : `hydra -l attacker-demo -P /tmp/rt01-wordlist.txt ssh://192.168.20.20 -t 4 -f -V`

## Captures PNG

```bash
python3 scripts/redteam/generate-redteam-screenshots.py
```

Sortie : `docs/livrables/screenshots/05-red-team/`

## Documentation

- [runbook-red-team.md](../docs/livrables/redteam/runbook-red-team.md)
- [journal-exercices.md](../docs/livrables/redteam/journal-exercices.md)
