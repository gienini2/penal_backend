from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from core.gate.penal_gate import PenalGate
from core.router.semantic_router import router_semantico_vector, embedding

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

@app.on_event("startup")
async def startup_event():
    app.state.router = ModuleRouter("scripts/vectores/centroides_modulos.npy")

import os
print("CWD:", os.getcwd())
print("FILES:", os.listdir())


@app.post("/api/v1/penal/analyze")
async def analyze_penal(req: PenalRequest, request: Request):
    return {"debug": "entra correctamente", "texto": req.texto}







