{{ config(materialized='table') }}
select marque, count(*) as nb_commandes,
round(sum(case when statut_commande not in ('Annulee','Retournee') then montant_total_eur else 0 end),2) as ca_eur
from {{ source('retailai_raw','ventes_raw') }}
group by marque
