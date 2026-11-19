from types import SimpleNamespace
from scripts.seed import load
from app.business_ai import query_business
from app.forecast import monthly_forecast
from app.observability import record,summary

def principal(brands=None,countries=None):
    return SimpleNamespace(brands=brands if brands is not None else ["Casanoov"],countries=countries if countries is not None else ["France"])

def test_business_query_scoped():
    load()
    result=query_business("Quel est le chiffre d'affaires de Casanoov ?",principal())
    assert result["mode"]=="business-sql"
    assert result["scope"]["brands"]==["Casanoov"]
    assert "Cazeboo:" not in result["answer"]

def test_business_empty_scope():
    assert "Aucune donnée" in query_business("ventes",principal(brands=[]))["answer"]

def test_forecast():
    load()
    result=monthly_forecast(principal(),horizon=3)
    assert len(result["forecast"])==3
    assert result["evaluation"]["walk_forward_mae_eur"]>=0

def test_forecast_no_scope():
    assert monthly_forecast(principal(countries=[]))["forecast"]==[]

def test_observability():
    before=summary()["count"]
    record("/ask",12.5,200,"business-sql")
    assert summary()["count"]>=before
