import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from utils import limpiar_formato

# Evalúa la respuesta del usuario con ayuda de Gemini y proporciona retroalimentación guiada
def evaluar_respuesta(caso, respuesta_usuario):
    respuestas_invalidas = [
        "no sé", "no se", "no sé nada", "no se nada", "no sé responder", "no se responder",
        "no sé del tema", "no se del tema", "no sé de este tema para responder",
        "no se de este tema para responder"
    ]

    respuesta_normalizada = respuesta_usuario.strip().lower()
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise Exception("GOOGLE_API_KEY no definida en .env")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Si la respuesta es inválida, generamos retroalimentación constructiva
    if not respuesta_normalizada or respuesta_normalizada in respuestas_invalidas:
        # Generar retroalimentación útil con Gemini
        prompt_feedback = (
            "El siguiente caso de estudio requiere una respuesta relacionada con ISO 27001. "
            "El usuario no proporcionó una respuesta válida. Ayúdalo con una retroalimentación constructiva "
            "sobre cómo podría comenzar a abordar este tipo de casos, qué elementos debe considerar, "
            "y cómo aplicar conceptos de la norma ISO 27001. Recuerda mencionar con detalle cada norma o anexo utilizados como referencia.\n\n"
            f"CASO:\n{caso}"
        )
        response = model.generate_content(prompt_feedback)
        texto_feedback = limpiar_formato(response.text)

        return 0, {
            "Relevancia": 0,
            "Comprensión": 0,
            "Aplicación": 0,
            "Coherencia": 0
        }, f"La respuesta proporcionada es irrelevante o vacía. Puntaje 0%.\n\n Sugerencia para mejorar:\n{texto_feedback}"

    # Evaluación normal cuando la respuesta es válida
    prompt_eval = (
        "Evalúa detalladamente la siguiente respuesta del usuario respecto al caso ISO 27001. "
        "Califica cada criterio de 0 a 100 y proporciona una breve justificación por cada uno. "
        "Criterios:\n"
        "1. Relevancia con el caso\n"
        "2. Comprensión del problema\n"
        "3. Aplicación de ISO 27001\n"
        "4. Coherencia y lógica en relación con la norma ISO 27001\n\n"
        "IMPORTANTE: Si la respuesta no tiene ninguna relación con el caso ni con la norma ISO 27001, "
        "debes asignar 0% en TODOS los criterios.\n\n"
        "Devuelve el resultado con el siguiente formato exacto:\n"
        "Relevancia: XX%\nComprensión: XX%\nAplicación ISO 27001: XX%\nCoherencia: XX%\nJustificación: ...\n\n"
        f"CASO:\n{caso}\n\nRESPUESTA:\n{respuesta_usuario}"
    )

    try:
        response = model.generate_content(prompt_eval)
        texto = limpiar_formato(response.text)
    except Exception as e:
        raise RuntimeError(f"Error al generar evaluación: {e}")

    criterios = ["Relevancia", "Comprensión", "Aplicación", "Coherencia"]
    puntuaciones = {}
    for criterio in criterios:
        match = re.search(rf"{criterio}.*?(\d{{1,3}})%", texto, re.IGNORECASE)
        puntuaciones[criterio] = int(match.group(1)) if match else 0

    justificacion = re.search(r"Justificación:(.*)", texto, re.DOTALL | re.IGNORECASE)
    resumen = justificacion.group(1).strip() if justificacion else "No se proporcionó justificación."

    promedio = round(sum(puntuaciones.values()) / len(criterios), 2)
    return promedio, puntuaciones, resumen
