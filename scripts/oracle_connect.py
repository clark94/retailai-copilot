"""Test de connexion Oracle (facultatif) : python scripts/oracle_connect.py"""
import os
from dotenv import load_dotenv
load_dotenv()
import oracledb
with oracledb.connect(user=os.environ['ORACLE_USER'],password=os.environ['ORACLE_PASSWORD'],dsn=os.environ['ORACLE_DSN']) as con:
    with con.cursor() as cur:
        cur.execute('SELECT 1 FROM DUAL')
        print('Oracle OK:',cur.fetchone())
