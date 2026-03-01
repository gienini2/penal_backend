import os
import math
import time
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODULOS = {
    "patrimonio": "robo, hurto, estafa, apropiación indebida, daños",
    "libertad": "detención ilegal, amenazas, coacciones, secuestro, acoso",
    "orden_publico": "resistencia a la autoridad, atentado, alteración del orden público",
    "medio_ambiente": "maltrato animal, abandono animal, caza ilegal",
    "vida_integridad": "lesiones, agresión, violencia física"
}

def cosine(v1, v2):
    dot = sum(a*b for a,b in zip(v1,v2))
    n1 = math.sqrt(sum(a*a for a in v1))
    n2 = math.sqrt(sum(b*b for b in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot/(n1*n2)

def embedding(texto):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texto
        )
        return response.data[0].embedding

    except Exception as e:
        raise RuntimeError(f"Error generando embedding: {e}")

# 🔥 PRECALCULAR EMBEDDINGS DE MÓDULOS SOLO UNA VEZ
EMB_MODULOS = None

def inicializar_modulos():
    global EMB_MODULOS
    if EMB_MODULOS is None:
        print("Inicializando embeddings de módulos...")
        EMB_MODULOS = {
            modulo: embedding(descripcion)
            for modulo, descripcion in MODULOS.items()
        }
def router_semantico_vector(emb_texto, top_n=3):

    inicializar_modulos()

    ranking = []

    for modulo, emb_mod in EMB_MODULOS.items():
        score = cosine(emb_texto, emb_mod)
        ranking.append((modulo, score))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return ranking[:top_n]

