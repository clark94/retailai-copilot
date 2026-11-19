from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from app.analytics import sales_summary,low_stock,stock_movements
from app.security import current_user, Principal
from app.rag import answer as lexical_answer
import os
from time import perf_counter
from app.business_ai import query_business
from app.forecast import monthly_forecast
from app.observability import record, summary

app=FastAPI(title="RetailAI Copilot — Secure Demo",version="0.2.0")
class Question(BaseModel):
    question: str=Field(min_length=2,max_length=1500)

@app.get("/health")
def health(): return {"status":"ok","demo":True}

@app.get("/me")
def me(user:Principal=Depends(current_user)): return user

@app.get("/sales")
def sales(group_by:str="marque",user:Principal=Depends(current_user)):
    try: return {"rows":sales_summary(group_by, countries=user.countries,brands=user.brands),"source":"synthetic","scope":user.model_dump()}
    except ValueError as exc: raise HTTPException(400,str(exc))

@app.get("/stocks/low")
def stocks_low(threshold:int=15,user:Principal=Depends(current_user)):
    return {"rows":low_stock(threshold,brands=user.brands),"note":"stock observé dans CSV, pas stock actuel"}

@app.get("/stocks/movements")
def movements(user:Principal=Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(403,"Mouvements de stock réservés au rôle admin dans cette démonstration")
    return {"rows":stock_movements(),"note":"variation nette sans stock initial"}

@app.post("/ask")
def ask(q:Question,user:Principal=Depends(current_user)):
    started=perf_counter()
    business=query_business(q.question,user)
    if business is not None:
        record("/ask", (perf_counter()-started)*1000,200,"business-sql")
        return business
    if os.getenv("RAG_BACKEND","tfidf")=="vector":
        try:
            from app.vector_rag import answer
            result=answer(q.question,user)
            record("/ask",(perf_counter()-started)*1000,200,result.get("mode"))
            return result
        except ImportError:
            raise HTTPException(503,"Installer requirements-vector.txt")
    result=lexical_answer(q.question)
    record("/ask",(perf_counter()-started)*1000,200,result.get("mode"))
    return result

@app.get("/forecast")
def forecast(brand:str|None=None,horizon:int=3,user:Principal=Depends(current_user)):
    if brand and brand not in user.brands:
        raise HTTPException(403,"Marque non autorisée")
    try:return monthly_forecast(user,brand,horizon)
    except ValueError as exc:raise HTTPException(400,str(exc))

@app.get("/observability")
def observability(user:Principal=Depends(current_user)):
    if user.role!="admin":raise HTTPException(403,"Accès administrateur requis")
    return summary()

