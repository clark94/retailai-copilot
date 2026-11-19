from app.analytics import sales_summary
from app.rag import answer
from scripts.seed import load

def test_sales():
    load()
    rows=sales_summary('marque',countries=['France'],brands=['Casanoov','Cazeboo','Sicaan'])
    assert rows and all('ca_eur' in r for r in rows)

def test_rag_unknown():
    result=answer('xyzxyzxyz totalement introuvable')
    assert result['sources']==[]
