"""Deterministic, auditable business assistant. No model-generated SQL."""
import re
from app.database import connect

def query_business(question, user):
    q=question.casefold()
    if not any(word in q for word in ("chiffre", "ventes", "commandes", "stock", "ca ", "revenu")):
        return None
    brands=[b for b in user.brands if b.casefold() in q]
    brands=brands or user.brands
    if not brands or not user.countries:
        return {"answer":"Aucune donnée autorisée pour ce périmètre.","sources":[],"mode":"business-sql"}
    filters="pays IN ("+",".join("?" for _ in user.countries)+") AND marque IN ("+",".join("?" for _ in brands)+")"
    params=(*user.countries,*brands)
    with connect() as con:
        if "stock" in q:
            rows=con.execute(f"""SELECT marque,produit,MIN(stock_disponible) AS stock_observe
                FROM ventes WHERE {filters} GROUP BY marque,produit
                ORDER BY stock_observe ASC LIMIT 5""",params).fetchall()
            lines=[f"{r['marque']} — {r['produit']}: {r['stock_observe']}" for r in rows]
            answer="Stocks observés les plus faibles (données fictives, non inventaire réel) : "+("; ".join(lines) if lines else "aucun résultat")
        else:
            rows=con.execute(f"""SELECT marque,COUNT(*) AS commandes,
                ROUND(SUM(CASE WHEN statut_commande NOT IN ('Annulee','Retournee') THEN montant_total_eur ELSE 0 END),2) AS ca
                FROM ventes WHERE {filters} GROUP BY marque ORDER BY ca DESC""",params).fetchall()
            lines=[f"{r['marque']}: {r['commandes']} commandes, {r['ca']:.2f} € de CA" for r in rows]
            answer="Résultats des ventes synthétiques : "+("; ".join(lines) if lines else "aucun résultat")
    return {"answer":answer,"sources":[{"source":"SQLite / ventes synthétiques"}],"mode":"business-sql","scope":{"brands":brands,"countries":user.countries}}
