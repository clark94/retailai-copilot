from app.database import connect
ALLOWED={"marque","pays","categorie","statut_commande","canal_vente"}

def sales_summary(group_by="marque",countries=None,brands=None):
    if group_by not in ALLOWED: raise ValueError("Dimension non autorisée")
    countries=countries or []
    brands=brands or []
    if not countries or not brands: return []
    country_marks=",".join("?" for _ in countries)
    brand_marks=",".join("?" for _ in brands)
    query=f"""SELECT {group_by} AS dimension,COUNT(*) AS commandes,
    ROUND(SUM(CASE WHEN statut_commande NOT IN ('Annulee','Retournee') THEN montant_total_eur ELSE 0 END),2) AS ca_eur
    FROM ventes WHERE pays IN ({country_marks}) AND marque IN ({brand_marks})
    GROUP BY {group_by} ORDER BY ca_eur DESC"""
    with connect() as con:
        return [dict(r) for r in con.execute(query,(*countries,*brands)).fetchall()]

def low_stock(threshold=15,brands=None):
    threshold=max(0,min(int(threshold),1000))
    brands=brands or []
    if not brands: return []
    marks=",".join("?" for _ in brands)
    with connect() as con:
        return [dict(r) for r in con.execute(f"""SELECT marque,id_produit,produit,MIN(stock_disponible) AS stock_observe
          FROM ventes WHERE marque IN ({marks}) GROUP BY marque,id_produit,produit
          HAVING MIN(stock_disponible) <= ? ORDER BY stock_observe LIMIT 50""",(*brands,threshold)).fetchall()]

def stock_movements():
    with connect() as con:
        return [dict(r) for r in con.execute("""SELECT code_produit,entrepot,
          ROUND(SUM(CASE WHEN type_mouvement='ENTREE' THEN quantite
                         WHEN type_mouvement='SORTIE' THEN -quantite ELSE 0 END),2) AS variation_nette,
          SUM(CASE WHEN quantite IS NULL THEN 1 ELSE 0 END) AS quantites_manquantes
          FROM mouvements GROUP BY code_produit,entrepot ORDER BY code_produit,entrepot""").fetchall()]
