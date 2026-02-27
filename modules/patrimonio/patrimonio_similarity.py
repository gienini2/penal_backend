# patrimonio_similarity.py

import os
import json
import math

VARIABLES = [
    "animo_lucro",
    "apoderamiento",
    "fuerza_en_cosas",
    "violencia_persona",
    "intimidacion",
    "uso_arma",
    "cuantia_economica",
    "acceso_no_autorizado",
    "especial_valor_bien",
    "engaño",
    "abuso_confianza",
    "uso_indebido_bien",
    "deterioro_bien",
    "ocupacion_inmueble",
    "falsificacion_medio_pago"
]

def vector_to_list(vector):
    return [float(vector.get(v, 0.0)) for v in VARIABLES]

def cosine(v1, v2):
    dot = sum(a*b for a,b in zip(v1,v2))
    n1 = math.sqrt(sum(a*a for a in v1))
    n2 = math.sqrt(sum(b*b for b in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1*n2)

def cargar_catalogo(path_base):
    matriz = {}
    for file in os.listdir(path_base):
        if file.startswith("CP-Patrimonio") and file.endswith(".json"):
            nombre = file.replace("CP-Patrimonio-","").replace(".json","")
            with open(os.path.join(path_base,file), "r", encoding="utf-8") as f:
                matriz[nombre] = vector_to_list(json.load(f))
    return matriz

def comparar_patrimonio(vector_texto, path_base, umbral=0.5):

    vector_texto_list = vector_to_list(vector_texto)
    matriz = cargar_catalogo(path_base)

    ranking = []

    for delito, vector_delito in matriz.items():
        score = cosine(vector_texto_list, vector_delito)
        if score >= umbral:
            ranking.append({
                "delito": delito,
                "score": round(score, 4)
            })

    ranking.sort(key=lambda x: x["score"], reverse=True)

    return ranking