import os, sqlite3
from pathlib import Path

def connect():
    db=Path(os.getenv('DATABASE_PATH',str(Path(__file__).resolve().parents[1]/'runtime'/'retailai.db')))
    db.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(db)
    con.row_factory=sqlite3.Row
    return con
