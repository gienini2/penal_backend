from core.gate.penal_gate import PenalGate
from core.router.semantic_router import router_semantico

penal_gate = PenalGate(
    "vectores/centroide_penal.npy",
    "vectores/centroide_no_penal.npy",
    threshold=0.02
)

@app.post("/api/v1/penal/analyze")
def analyze_penal(req: PenalRequest):

    is_penal, gate_score = penal_gate.evaluar(req.texto)

    if not is_penal:
        return {
            "is_penal": False,
            "confidence_gate": gate_score
        }

    # 🔥 Solo si es penal activas router
    modulos = router_semantico(req.texto, top_n=3)

    ranking_global = []

    for modulo, _ in modulos:
        engine = __import__(f"modules.{modulo}.engine", fromlist=["run"])
        resultados = engine.run(req.texto)
        ranking_global.extend(resultados)

    ranking_global = sorted(
        ranking_global,
        key=lambda x: x.score,
        reverse=True
    )[:3]

    return {
        "is_penal": True,
        "confidence_gate": gate_score,
        "top_delitos": ranking_global
    }
