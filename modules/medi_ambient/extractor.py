from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VARIABLES = [
    "dano_fauna",
    "dano_flora",
    "maltrato_animal",
    "abandono_animal",
    "riesgo_muerte_animal",
    "uso_metodos_prohibidos",
    "caza_pesca_ilegal",
    "dano_habitat_protegido",
    "animo_lucro",
    "reiteracion"
]

SYSTEM_PROMPT = """
Eres un analizador fenomenológico penal especializado en delitos contra el medio ambiente y los animales.

Evalúa el texto y asigna un valor entre 0.0 y 1.0 a cada variable:

0.0 = ausente estructural
0.2 = circunstancial
0.4 = frecuente
0.6 = habitual
0.8 = casi definitorio
1.0 = nuclear imprescindible

Devuelve EXCLUSIVAMENTE un JSON válido con EXACTAMENTE estas 10 claves:

dano_fauna
dano_flora
maltrato_animal
abandono_animal
riesgo_muerte_animal
uso_metodos_prohibidos
caza_pesca_ilegal
dano_habitat_protegido
animo_lucro
reiteracion

No añadas ninguna otra clave.
No expliques nada.
No devuelvas texto adicional.

Si el texto describe abandono de un animal doméstico en condiciones de riesgo,
abandono_animal no puede ser 0.0.
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
                    "name": "vector_medio_ambiente",
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
