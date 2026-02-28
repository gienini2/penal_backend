from .extractor import extraer_vector
from .similarity import comparar_medio_ambiente

CATALOGO_PATH = "modules/medio_ambient/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_medio_ambiente(vector, CATALOGO_PATH, UMBRAL)
    return ranking
