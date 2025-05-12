import os
import json
import re
from datetime import datetime

HISTORIAL_PATH = "historial.json"

# Limpia formato Markdown o caracteres especiales
def limpiar_formato(texto):
    texto = re.sub(r"\*{1,2}", "", texto)
    texto = re.sub(r"#{1,6}\s*", "", texto)
    texto = re.sub(r"`+", "", texto)
    texto = re.sub(r"_+", "", texto)
    texto = re.sub(r"^\s*>+", "", texto, flags=re.M)
    return texto.strip()

# Carga historial desde el archivo JSON
def cargar_historial():
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guarda una nueva entrada en el historial
def guardar_en_historial(caso, planificacion, sugerencias, respuesta, evaluacion):
    historial = cargar_historial()  # Se asegura que el historial se cargue correctamente
    historial.append({
        "caso": caso,
        "planificacion": planificacion,
        "sugerencias": sugerencias,
        "respuesta_usuario": respuesta,
        "evaluacion": {
            "puntaje": evaluacion[0],
            "justificacion": evaluacion[1]
        },
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    # Guardamos el historial actualizado en el archivo
    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

# Elimina un caso específico del historial por su índice
def borrar_del_historial(indice):
    historial = cargar_historial()
    if 0 <= indice < len(historial):
        historial.pop(indice)
        with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)
        return True
    return False