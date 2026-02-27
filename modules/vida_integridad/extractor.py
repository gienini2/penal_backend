from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VARIABLES = [
    "resultado_muerte",
    "riesgo_muerte",
    "intervencion_gestacional",
    "resultado_lesion",
    "gravedad_lesion",
    "perdida_funcional",
    "violencia_fisica",
    "imprudencia",
    "uso_arma",
    "participacion_grupal",
    "maltrato_sin_lesion",
    "reiteracion"
]

SYSTEM_PROMPT = """
Eres un analizador fenomenológico penal.

Evalúa el texto y asigna un valor entre 0.0 y 1.0 a cada variable:

0.0 = ausente estructural
0.2 = circunstancial
0.4 = frecuente
0.6 = habitual
0.8 = casi definitorio
1.0 = nuclear imprescindible

Devuelve EXCLUSIVAMENTE un JSON válido con EXACTAMENTE estas 12 claves:

resultado_muerte
riesgo_muerte
intervencion_gestacional
resultado_lesion
gravedad_lesion
perdida_funcional
violencia_fisica
imprudencia
uso_arma
participacion_grupal
maltrato_sin_lesion
reiteracion

No añadas ninguna otra clave.
No expliques nada.
No devuelvas texto adicional.

Si el texto describe una muerte directa causada por una persona,
resultado_muerte no puede ser 0.0.

Si el texto describe penetración o intervención sobre embarazo,
intervencion_gestacional no puede ser 0.0.
"""


def vector_cero():
    return {var: 0.0 for var in VARIABLES}


def extraer_vector(texto):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "vector_vida_integridad",
                    "schema": {
                        "type": "object",
                        "properties": {
                            var: {"type": "number"} for var in VARIABLES
                        },
                        "required": VARIABLES,
                        "additionalProperties": False
                    }
                }
            },
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": texto}
            ]
        )

        content = response.choices[0].message.content
        vector = json.loads(content)

        return vector

    except Exception as e:
        print("Error extrayendo vector vida_integridad:", e)
        return vector_cero()
