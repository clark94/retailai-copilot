import os
from fastapi.testclient import TestClient
from app.main import app
from scripts.seed import load

def test_token_and_scope(monkeypatch):
    monkeypatch.setenv('DEMO_API_TOKEN','test-only-secret')
    monkeypatch.setenv('DEMO_ALLOWED_COUNTRIES','France')
    monkeypatch.setenv('DEMO_ALLOWED_BRANDS','Casanoov')
    load()
    client=TestClient(app)
    assert client.get('/sales').status_code==401
    assert client.get('/sales',headers={'Authorization':'Bearer wrong'}).status_code==403
    r=client.get('/sales',headers={'Authorization':'Bearer test-only-secret'})
    assert r.status_code==200
    assert all(row['dimension']=='Casanoov' for row in r.json()['rows'])
    assert client.get('/stocks/movements',headers={'Authorization':'Bearer test-only-secret'}).status_code==403

def test_bad_group_by(monkeypatch):
    monkeypatch.setenv('DEMO_API_TOKEN','test-only-secret')
    r=TestClient(app).get('/sales?group_by=invalid',headers={'Authorization':'Bearer test-only-secret'})
    assert r.status_code==400
