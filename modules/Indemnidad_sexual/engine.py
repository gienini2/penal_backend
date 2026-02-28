from .extractor import extraer_vector
from .similarity import comparar_sexual

CATALOGO_PATH = "modules/Indemnidad_sexual/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_sexual(vector, CATALOGO_PATH, UMBRAL)
    return ranking
