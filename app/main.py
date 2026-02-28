from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from core.gate.penal_gate import PenalGate
from core.router.semantic_router import router_semantico_vector, embedding

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
def filtrar_modulos(ranking):
    if not ranking:
        return []

    seleccion = []

    mod1, s1 = ranking[0]
    if s1 < 0.22:
        return []

    seleccion.append((mod1, s1))

    if len(ranking) > 1:
        mod2, s2 = ranking[1]
        if s2 >= 0.18 and (s1 - s2) <= 0.12:
            seleccion.append((mod2, s2))

    if len(ranking) > 2:
        mod3, s3 = ranking[2]
        if s3 >= 0.15:
            seleccion.append((mod3, s3))

    return seleccion


async def ejecutar_engine(modulo, texto):
    engine = __import__(f"modules.{modulo}.engine", fromlist=["run"])
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, engine.run, texto)


@app.post("/api/v1/penal/analyze")
async def analyze_penal(req: PenalRequest):

    # 1️⃣ embedding único
    vector = embedding(req.texto)

    # 2️⃣ gate vectorial
    is_penal, gate_score = penal_gate.evaluar_vector(vector)

    if not is_penal:
        return {
            "is_penal": False,
            "confidence_gate": gate_score
        }

    # 3️⃣ router vectorial (CORRECTO)
    ranking = router_semantico_vector(vector, top_n=3)
    print("RANKING ROUTER:", ranking)
    # 4️⃣ filtro dinámico
    modulos = filtrar_modulos(ranking)

    # 5️⃣ ejecución paralela
    tasks = [
        ejecutar_engine(modulo, req.texto)
        for modulo, _ in modulos
    ]

    resultados_modulos = await asyncio.gather(*tasks)

    ranking_global = []
    for resultados in resultados_modulos:
        ranking_global.extend(resultados)

    ranking_global = sorted(
        ranking_global,
        key=lambda x: x["score"],
        reverse=True
    )[:3]

    return {
        "is_penal": True,
        "confidence_gate": gate_score,
        "top_delitos": ranking_global
    }
    if not modulos:
        return {
            "is_penal": False,
            "confidence_gate": gate_score
    }




