from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VARIABLES = [
    "condicion_funcionario",
    "omision_deber_legal",
    "abuso_potestad",
    "detencion_privacion_libertad",
    "entrada_domicilio",
    "intercepcion_comunicaciones",
    "custodia_documental",
    "revelacion_informacion_reservada",
    "corrupcion_soborno",
    "acusacion_denuncia_falsa",
    "obstruccion_justicia",
    "quebrantamiento_condena",
    "denegacion_auxilio",
    "perjuicio_ciudadano",
    "animo_lucro",
    "reiteracion"
]

SYSTEM_PROMPT = """
Eres un analizador fenomenológico penal especializado en delitos cometidos por funcionario público o contra la administración de justicia.

Evalúa el texto y asigna un valor entre 0.0 y 1.0 a cada variable:

0.0 = ausente estructural
0.2 = circunstancial
0.4 = frecuente
0.6 = habitual
0.8 = casi definitorio
1.0 = nuclear imprescindible

Devuelve EXCLUSIVAMENTE un JSON válido con EXACTAMENTE estas 16 claves:

condicion_funcionario
omision_deber_legal
abuso_potestad
detencion_privacion_libertad
entrada_domicilio
intercepcion_comunicaciones
custodia_documental
revelacion_informacion_reservada
corrupcion_soborno
acusacion_denuncia_falsa
obstruccion_justicia
quebrantamiento_condena
denegacion_auxilio
perjuicio_ciudadano
animo_lucro
reiteracion

No añadas ninguna otra clave.
No expliques nada.
No devuelvas texto adicional.

Si el texto describe actuación de autoridad o funcionario en ejercicio de su cargo,
condicion_funcionario no puede ser 0.0.

Si el texto describe soborno o dádiva,
corrupcion_soborno no puede ser 0.0.
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
                    "name": "vector_funcion_publica",
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
        print("Error extrayendo vector funcion_publica:", e)
        return vector_cero()