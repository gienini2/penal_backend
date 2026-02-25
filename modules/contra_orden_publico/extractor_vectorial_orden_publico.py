from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VARIABLES = [
    "violencia_autoridad",
    "intimidacion_autoridad",
    "resistencia_activa",
    "resistencia_pasiva",
    "desobediencia",
    "uso_arma",
    "tenencia_arma",
    "deposito_armas",
    "arma_prohibida",
    "alteracion_paz_publica",
    "interrupcion_servicio_publico",
    "motin_colectivo",
    "discurso_odio",
    "motivacion_discriminatoria",
    "danos_bienes_publicos",
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

Devuelve EXCLUSIVAMENTE un JSON válido con EXACTAMENTE estas 16 claves:

violencia_autoridad
intimidacion_autoridad
resistencia_activa
resistencia_pasiva
desobediencia
uso_arma
tenencia_arma
deposito_armas
arma_prohibida
alteracion_paz_publica
interrupcion_servicio_publico
motin_colectivo
discurso_odio
motivacion_discriminatoria
danos_bienes_publicos
reiteracion

No añadas ninguna otra clave.
No expliques nada.
No devuelvas texto adicional.

Si el texto describe agresión física a agente de autoridad,
violencia_autoridad no puede ser 0.0.

Si el texto describe alteración colectiva grave del orden,
alteracion_paz_publica no puede ser 0.0.
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
                    "name": "vector_orden_publico",
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
        print("Error extrayendo vector orden_publico:", e)
        return vector_cero()