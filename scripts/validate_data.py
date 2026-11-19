import csv
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with (root/'data'/'ventes_synthetiques.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
assert rows and all(r['ID_COMMANDE'] for r in rows)
assert len({r['ID_COMMANDE'] for r in rows})==len(rows)
print('Validation CSV ventes : OK',len(rows))
