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

    ranking = router_semantico(req.texto, top_n=1)

    if not ranking:
        return {"is_penal": False}

    modulo, score = ranking[0]

    if score < 0.22:
        return {"is_penal": False}

    # dispatch dinámico
    engine = __import__(f"modules.{modulo}.engine", fromlist=["run"])
    resultados = engine.run(req.texto)

    return {
        "is_penal": True,
        "modulo": modulo,
        "confidence_router": score,
        "resultados": resultados

    }




