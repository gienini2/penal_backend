from .extractor import extraer_vector
from .similarity import comparar_orden_publico

CATALOGO_PATH = "modules/orden_publico/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_orden_publico(vector, CATALOGO_PATH, UMBRAL)
    return ranking
