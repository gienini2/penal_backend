from .extractor import extraer_vector
from .similarity import comparar_funcion_publica

CATALOGO_PATH = "modules/delitos_funcionarios/catalogo"
UMBRAL = 0.50

def run(texto):
    vector = extraer_vector(texto)
    ranking = comparar_funcion_publica(vector, CATALOGO_PATH, UMBRAL)
    return ranking
