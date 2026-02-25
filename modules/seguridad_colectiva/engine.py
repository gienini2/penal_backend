from .extractor import extraer_vector
from .similarity import comparar_patrimonio

CATALOGO_PATH = "modules/seguridad_colectiva/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_patrimonio(vector, CATALOGO_PATH, UMBRAL)
    return ranking
