"""Development-only FastAPI app. Train the model before launching."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from engine import MODE, infer, retrieve, recommend, ART
app=FastAPI(title='Retail Demand Forecasting and Inventory Optimization',version='0.1.0')
class Features(BaseModel):
    values:list[float]=Field(min_length=1,max_length=64)
@app.get('/health')
def health():return {'status':'ok','trained':(ART/'model.joblib').exists(),'mode':MODE}
@app.post('/predict')
def predict(payload:Features):
    if MODE in ('search','recommend'):raise HTTPException(400,'Use /search or /recommend')
    if not (ART/'model.joblib').exists():raise HTTPException(503,'Train first: python engine.py train')
    try:return infer(payload.values)
    except (ValueError,IndexError) as ex:raise HTTPException(422,str(ex))
@app.get('/search')
def search(q:str,k:int=3):
    if MODE!='search':raise HTTPException(400,'Not a search project')
    if not (ART/'model.joblib').exists():raise HTTPException(503,'Train first')
    if not 1<=k<=10:raise HTTPException(422,'k must be between 1 and 10')
    return {'query':q,'citations':retrieve(q,k),'answer_policy':'Display source passages; no LLM answer is generated.'}
@app.get('/recommend')
def recommendations(user_id:int=0,k:int=5):
    if MODE!='recommend':raise HTTPException(400,'Not a recommender project')
    if not (ART/'model.joblib').exists():raise HTTPException(503,'Train first')
    if not 1<=k<=20:raise HTTPException(422,'k must be between 1 and 20')
    try:return recommend(user_id,k)
    except ValueError as ex:raise HTTPException(422,str(ex))
