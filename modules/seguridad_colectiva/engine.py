from .extractor import extraer_vector
from .similarity import comparar_seguridad_colectiva

CATALOGO_PATH = "modules/seguridad_colectiva/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_seguridad_colectiva(vector, CATALOGO_PATH, UMBRAL)
    return ranking
