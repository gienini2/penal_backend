# filtro_penal.py

from semantic_router import router_semantico
from tqdm import tqdm

UMBRAL = 0.22

def filtrar_archivo(input_path, output_path):

    with open(input_path, "r", encoding="cp1252") as f_in, \
         open(output_path, "w", encoding="cp1252") as f_out:

        for linea in tqdm(f_in, desc="Filtrando"):
            partes = linea.strip().split("@")
            if len(partes) < 3:
                continue

            texto = partes[1]

            ranking = router_semantico(texto, top_n=1)
            if not ranking:
                continue

            _, score = ranking[0]

            if score >= UMBRAL:
                f_out.write(linea)