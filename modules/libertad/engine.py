from .extractor import extraer_vector
from .similarity import comparar_libertad

CATALOGO_PATH = "modules/libertad/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_libertad(vector, CATALOGO_PATH, UMBRAL)
    return ranking
