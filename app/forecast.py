"""Transparent historical monthly baseline and holdout evaluation; not a trained ML model."""
from app.database import connect

def monthly_forecast(user, brand=None, horizon=3):
    if horizon<1 or horizon>6: raise ValueError("Horizon entre 1 et 6 mois")
    brands=[b for b in user.brands if brand is None or b==brand]
    if not brands or not user.countries:return {"history":[],"forecast":[],"evaluation":None}
    marks_b=",".join("?" for _ in brands)
    marks_c=",".join("?" for _ in user.countries)
    with connect() as con:
        rows=con.execute(f"""SELECT substr(date_commande,1,7) AS mois,
            ROUND(SUM(CASE WHEN statut_commande NOT IN ('Annulee','Retournee')
            THEN montant_total_eur ELSE 0 END),2) AS ca
            FROM ventes WHERE marque IN ({marks_b}) AND pays IN ({marks_c})
            GROUP BY substr(date_commande,1,7) ORDER BY mois""",(*brands,*user.countries)).fetchall()
    history=[{"month":r["mois"],"revenue":float(r["ca"] or 0)} for r in rows]
    if len(history)<4:return {"history":history,"forecast":[],"evaluation":None,"warning":"Historique insuffisant"}
    values=[r["revenue"] for r in history]
    errors=[abs(values[i]-sum(values[i-3:i])/3) for i in range(3,len(values))]
    mae=round(sum(errors)/len(errors),2)
    baseline=round(sum(values[-3:])/3,2)
    year,month=map(int,history[-1]["month"].split("-"))
    forecast=[]
    for offset in range(1,horizon+1):
        idx=year*12+month-1+offset
        forecast.append({"month":f"{idx//12:04d}-{idx%12+1:02d}","predicted_revenue":baseline})
    return {"history":history,"forecast":forecast,"evaluation":{"walk_forward_mae_eur":mae,"evaluation_months":len(errors)},"method":"moyenne mobile 3 mois, prévision constante","warning":"Baseline descriptive sur données synthétiques, pas un modèle ML validé"}
