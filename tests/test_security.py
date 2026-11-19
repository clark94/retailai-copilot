import pytest
from app.analytics import sales_summary,low_stock

def test_invalid_group():
    with pytest.raises(ValueError):
        sales_summary("marque;DROP TABLE ventes",["France"],["Casanoov"])

def test_empty_scope():
    assert sales_summary("marque",[],["Casanoov"])==[]
    assert low_stock(brands=[])==[]
