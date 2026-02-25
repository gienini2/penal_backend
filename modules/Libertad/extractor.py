from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VARIABLES = [
    "privacion_libertad",
    "duracion_retencion",
    "traslado_forzado",
    "impedimento_salida",
    "amenaza_grave",
    "amenaza_leve",
    "coaccion_directa",
    "exigencia_condicion",
    "chantaje",
    "acoso_reiterado",
    "acceso_domicilio",
    "revelacion_informacion",
    "omision_auxilio",
    "relacion_dependencia",
    "uso_menor"
]

SYSTEM_PROMPT = """
Eres un analizador fenomenológico penal especializado en delitos contra la libertad.

Evalúa el texto y asigna un valor entre 0.0 y 1.0 a cada variable:

0.0 = ausente estructural
0.2 = circunstancial
0.4 = frecuente
0.6 = habitual
0.8 = casi definitorio
1.0 = nuclear imprescindible

Devuelve EXCLUSIVAMENTE un JSON válido con EXACTAMENTE estas 15 claves:

privacion_libertad
duracion_retencion
traslado_forzado
impedimento_salida
amenaza_grave
amenaza_leve
coaccion_directa
exigencia_condicion
chantaje
acoso_reiterado
acceso_domicilio
revelacion_informacion
omision_auxilio
relacion_dependencia
uso_menor

No añadas ninguna otra clave.
No expliques nada.
No devuelvas texto adicional.

Si el texto describe una restricción física de movimiento no consentida,
privacion_libertad no puede ser 0.0.
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
                    "name": "vector_libertad",
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
        print("Error extrayendo vector:", e)
        return vector_cero()
