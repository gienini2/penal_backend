from core.gate.penal_gate import PenalGate
from tqdm import tqdm

GATE = PenalGate(
    "scripts/vectores/centroide_penal.npy",
    "scripts/vectores/centroide_no_penal.npy",
    threshold=-0.01
)

def filtrar_archivo(input_path, output_path):

    with open(input_path, "r", encoding="cp1252") as f_in, \
         open(output_path, "w", encoding="cp1252") as f_out:

        for linea in tqdm(f_in, desc="Filtrando"):

            partes = linea.strip().split("@")
            if len(partes) < 3:
                continue

            texto = partes[1]

            es_penal, score = GATE.evaluar(texto)

            if es_penal:
                f_out.write(linea)

