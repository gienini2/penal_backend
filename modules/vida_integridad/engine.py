from .extractor import extraer_vector
from .similarity import comparar_patrimonio

CATALOGO_PATH = "modules/vida_integridad/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_vida_integridad(vector, CATALOGO_PATH, UMBRAL)
    return ranking
