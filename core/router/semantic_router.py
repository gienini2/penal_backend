import os
import math
import time
from openai import OpenAI
import os
import numpy as np

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



class ModuleRouter:

    def __init__(self, path):
        self.centroides = np.load(path, allow_pickle=True).item()

    def rank(self, emb, top_n=3):
        scores = {
            modulo: cosine(emb, vector)
            for modulo, vector in self.centroides.items()
        }

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]True)

    return ranking[:top_n]


