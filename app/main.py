from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from core.gate.penal_gate import PenalGate
from core.router.semantic_router import ModuleRouter, embedding

class PenalRequest(BaseModel):
    texto: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gienini2.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

THRESHOLD_GATE     = -0.01
THRESHOLD_MOD1     = 0.22
THRESHOLD_MOD2     = 0.18
THRESHOLD_MOD2_GAP = 0.12
THRESHOLD_MOD3     = 0.15

@app.on_event("startup")
async def startup_event():
    app.state.gate = PenalGate(
        "scripts/vectores/centroide_penal.npy",
        "scripts/vectores/centroide_no_penal.npy",
        threshold=THRESHOLD_GATE
    )
    app.state.router = ModuleRouter("scripts/vectores/centroides_modulos.npy")
    print("✅ Gate y Router cargados correctamente")


def filtrar_modulos(ranking):
    if not ranking:
        return []

    seleccion = []
    mod1, s1 = ranking[0]

    if s1 < THRESHOLD_MOD1:
        return []

    seleccion.append((mod1, s1))

    if len(ranking) > 1:
        mod2, s2 = ranking[1]
        if s2 >= THRESHOLD_MOD2 and (s1 - s2) <= THRESHOLD_MOD2_GAP:
            seleccion.append((mod2, s2))

    if len(ranking) > 2:
        mod3, s3 = ranking[2]
        if s3 >= THRESHOLD_MOD3:
            seleccion.append((mod3, s3))

    return seleccion


async def ejecutar_engine(modulo, texto):
    try:
        engine = __import__(f"modules.{modulo}.engine", fromlist=["run"])
        loop = asyncio.get_event_loop()
        resultado = await loop.run_in_executor(None, engine.run, texto)
        return resultado
    except Exception as e:
        print(f"❌ Error ejecutando engine {modulo}: {e}")
        return []


@app.post("/api/v1/penal/analyze")
async def analyze_penal(req: PenalRequest):
    texto = req.texto.strip()

    if not texto:
        return {"is_penal": False, "motivo": "texto_vacio"}

    es_penal, score_gate = app.state.gate.evaluar(texto)

    if not es_penal:
        return {
            "is_penal": False,
            "score_gate": round(float(score_gate), 4)
        }

    emb = embedding(texto)
    ranking_completo = app.state.router.rank(emb, top_n=3)
    modulos_activos = filtrar_modulos(ranking_completo)

    if not modulos_activos:
        return {
            "is_penal": True,
            "score_gate": round(float(score_gate), 4),
            "modulo": "desconocido",
            "confidence_router": 0.0,
            "resultados": []
        }

    modulo_principal, confidence = modulos_activos[0]
    resultados = await ejecutar_engine(modulo_principal, texto)

    return {
        "is_penal": True,
        "score_gate": round(float(score_gate), 4),
        "modulo": modulo_principal,
        "confidence_router": round(float(confidence), 4),
        "resultados": resultados,
        "modulos_evaluados": [
            {"modulo": m, "confidence": round(float(s), 4)}
            for m, s in modulos_activos
        ]
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
