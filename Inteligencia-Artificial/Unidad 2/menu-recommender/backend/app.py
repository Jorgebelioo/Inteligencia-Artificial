import sys
import os
sys.path.append(os.path.dirname(__file__))  
from recommender import recommend_example
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Evidence(BaseModel):
    IsVeganCustomer: int
    AllergicToNuts: int
    IngredientsAvailable: int
    LikesSpicy: int

@app.post("/recommend")
def recommend(evidence: Evidence):
    try:
        q = recommend_example(evidence.dict())
        probs = {state: float(prob) for state, prob in zip(q.state_names['PlatoRecomendado'], q.values)}
        return {"recommend_distribution": probs}
    except Exception as e:
        import traceback
        print("🔥 ERROR en /recommend:", traceback.format_exc())  # <- muestra el error completo en consola
        return {"error": str(e)}
