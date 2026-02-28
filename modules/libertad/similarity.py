import os
import json
import math

VARIABLES = [
    "privacion_libertad",
    "duracion_retencion",
    "traslado_forzado",
    "impedimento_salida",
    "amenaza_grave",
    "amenaza_leve",
    "coaccion_directa",
    "exigencia_condicion",
    "chantaje",
    "acoso_reiterado",
    "acceso_domicilio",
    "revelacion_informacion",
    "omision_auxilio",
    "relacion_dependencia",
    "uso_menor"
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
        if file.startswith("CP-Libertad") and file.endswith(".json"):
            nombre = file.replace("CP-Libertad-","").replace(".json","")
            with open(os.path.join(path_base,file), "r", encoding="utf-8") as f:
                matriz[nombre] = vector_to_list(json.load(f))
    return matriz

def comparar_libertad(vector_texto, path_base, umbral=0.5):

    vector_texto_list = vector_to_list(vector_texto)
    matriz = cargar_catalogo(path_base)

    ranking = []

    for delito, vector_delito in matriz.items():
        score = cosine(vector_texto_list, vector_delito)
        ranking.append({
            "delito": delito,
            "score": round(score, 4)
        })

    ranking.sort(key=lambda x: x["score"], reverse=True)

    if umbral > 0:
        ranking = [r for r in ranking if r["score"] >= umbral]

    return ranking
