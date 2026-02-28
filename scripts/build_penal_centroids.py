import numpy as np
from core.router.semantic_router import embedding

def construir_centroides(textos_penales, textos_no):

    emb_penal = [embedding(t) for t in textos_penales]
    emb_no = [embedding(t) for t in textos_no]

    centroide_penal = np.mean(emb_penal, axis=0)
    centroide_no = np.mean(emb_no, axis=0)

    np.save("vectores/centroide_penal.npy", centroide_penal)
    np.save("vectores/centroide_no_penal.npy", centroide_no)

if __name__ == "__main__":
    # cargar aquí tus datasets
    textos_penales = [...]
    textos_no = [...]

    construir_centroides(textos_penales, textos_no)
