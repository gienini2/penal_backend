import numpy as np
from core.router.semantic_router import embedding, cosine

class PenalGate:

    def __init__(self, centroide_penal, centroide_no_penal, threshold=0.0):
        self.c_penal = np.load(centroide_penal)
        self.c_no = np.load(centroide_no_penal)
        self.threshold = threshold

    def evaluar(self, texto):

        emb = embedding(texto)

        sim_penal = cosine(emb, self.c_penal)
        sim_no = cosine(emb, self.c_no)

        score = sim_penal - sim_no

        return score > self.threshold, score
  
    def evaluar_vector(self, emb):
        sim_penal = cosine(emb, self.c_penal)
        sim_no = cosine(emb, self.c_no)
        score = sim_penal - sim_no
        return score > self.threshold, score
