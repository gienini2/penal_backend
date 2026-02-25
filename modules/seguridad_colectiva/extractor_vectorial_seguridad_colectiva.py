from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VARIABLES = [
    "sustancia_estupefaciente",
    "trafico_sustancia",
    "posesion_para_distribucion",
    "conduccion_vehiculo",
    "conduccion_temeraria",
    "riesgo_grave_circulacion",
    "menosprecio_vida",
    "negativa_prueba_alcohol_droga",
    "abandono_lugar_accidente",
    "conduccion_sin_permiso",
    "alteracion_elementos_viales",
    "resultado_lesivo",
    "animo_lucro",
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

Devuelve EXCLUSIVAMENTE un JSON válido con EXACTAMENTE estas 14 claves:

sustancia_estupefaciente
trafico_sustancia
posesion_para_distribucion
conduccion_vehiculo
conduccion_temeraria
riesgo_grave_circulacion
menosprecio_vida
negativa_prueba_alcohol_droga
abandono_lugar_accidente
conduccion_sin_permiso
alteracion_elementos_viales
resultado_lesivo
animo_lucro
reiteracion

No añadas ninguna otra clave.
No expliques nada.
No devuelvas texto adicional.

Si el texto describe venta o distribución de droga,
trafico_sustancia no puede ser 0.0.

Si el texto describe conducción con riesgo extremo,
conduccion_temeraria no puede ser 0.0.
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
                    "name": "vector_seguridad_colectiva",
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
        print("Error extrayendo vector seguridad_colectiva:", e)
        return vector_cero()