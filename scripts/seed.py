import csv, sqlite3, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.database import connect
BASE=Path(__file__).resolve().parents[1]

def load():
    with connect() as con:
        con.executescript("""CREATE TABLE IF NOT EXISTS ventes (
        id_commande TEXT PRIMARY KEY, date_commande TEXT, id_client TEXT, pays TEXT,
        marque TEXT, id_produit TEXT, categorie TEXT, produit TEXT, quantite INTEGER,
        prix_unitaire_eur REAL, remise_pct REAL, montant_total_eur REAL,
        statut_commande TEXT, stock_disponible INTEGER, canal_vente TEXT);
        CREATE TABLE IF NOT EXISTS mouvements (
        ligne_source INTEGER PRIMARY KEY, id_mouvement TEXT, date_mouvement TEXT,
        type_mouvement TEXT, code_produit TEXT, produit TEXT, categorie TEXT,
        quantite REAL, code_entrepot TEXT, entrepot TEXT, ville TEXT, region TEXT);
        """)
        with (BASE/'data'/'ventes_synthetiques.csv').open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        cols=list(rows[0])
        sql='INSERT OR REPLACE INTO ventes ('+','.join(c.lower() for c in cols)+') VALUES ('+','.join('?' for _ in cols)+')'
        con.executemany(sql,[[r[c] if r[c]!='' else None for c in cols] for r in rows])
        with (BASE/'data'/'stock_nettoye.csv').open(encoding='utf-8-sig',newline='') as f:
            stock=list(csv.DictReader(f))
        fields=['LIGNE_SOURCE','ID_MOUVEMENT','DATE_MOUVEMENT','TYPE_MOUVEMENT','CODE_PRODUIT','PRODUIT','CATEGORIE','QUANTITE','CODE_ENTREPOT','ENTREPOT','VILLE','REGION']
        con.executemany('INSERT OR REPLACE INTO mouvements VALUES ('+','.join('?' for _ in fields)+')',[[r[c] or None for c in fields] for r in stock])
    print(f'Import OK: {len(rows)} ventes, {len(stock)} mouvements')
if __name__=='__main__':load()
