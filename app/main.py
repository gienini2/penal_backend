from fastapi import FastAPI
from pydantic import BaseModel
from core.router.semantic_router import router_semantico

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
is_penal, gate_score = penal_gate.evaluar(req.texto)

if not is_penal:
    return {"is_penal": False, "confidence_gate": gate_score}
class PenalRequest(BaseModel):
    texto: str

@app.post("/api/v1/penal/analyze")
def analyze_penal(req: PenalRequest):

    modulos = router_semantico(req.texto, top_n=3)
    
    ranking_global = []
    
    for modulo, _ in modulos:
        engine = __import__(f"modules.{modulo}.engine", fromlist=["run"])
        resultados = engine.run(req.texto)
        ranking_global.extend(resultados)
    
    ranking_global = sorted(
        ranking_global,
        key=lambda x: x.score,
        reverse=True
    )[:3]
    
    return {
        "is_penal": True,
        "confidence_gate": gate_score,
        "top_delitos": ranking_global
    }
    
    


