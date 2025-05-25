# ========================================
# 📦 Imports y Configuración Inicial
# ========================================
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

from utils import limpiar_formato, cargar_historial, guardar_en_historial, borrar_del_historial
from evaluador import evaluar_respuesta
from pdf_utils import exportar_pdf

# Configuración general de la app
st.set_page_config(page_title="ChatBot ISO 27001", page_icon="🛡️", layout="wide")
load_dotenv()

# ========================================
# 💾 Estado de Sesión
# ========================================
for var in ["caso", "planificacion", "sugerencias", "respuesta_usuario"]:
    st.session_state.setdefault(var, "")
st.session_state.setdefault("evaluacion", (0, ""))

# ========================================
# 🎨 Estilos CSS personalizados
# ========================================
st.markdown("""
    <style>
        .title { font-size:36px; font-weight:bold; color:#1a73e8; }
        .subtitle { font-size:24px; font-weight:bold; margin-top:10px; }
    </style>
""", unsafe_allow_html=True)

# ========================================
# 🧠 Encabezado y Descripción
# ========================================
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="https://i.pinimg.com/originals/79/04/42/7904424933cc535b666f2de669973530.gif" 
             alt="GIF" style="width: 330px; height: 250px; margin-right: 20px;">
        <div>
            <div class="title">🛡️ ChatBot ISO 27001</div>
            <div class="title">GRUPO N°4</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="padding: 15px; border-radius: 5px; color: white;">
        Esta aplicación permite simular el análisis de la norma ISO/IEC 27001. Se genera automáticamente un caso de estudio 
        sobre una problemática de seguridad de la información, permitiendo que el usuario proponga soluciones y reciba 
        una evaluación técnica.
    </p>
""", unsafe_allow_html=True)

# ========================================
# 🧩 Pestañas de la Aplicación
# ========================================
tabs = st.tabs([
    "📌 Generar Caso",
    "📝 Ingresar Respuesta",
    "📊 Evaluación",
    "📚 Historial"
])

# ========================================
# TAB 1: Generar Caso y Planificación (Vertical)
# ========================================
with tabs[0]:
    st.subheader("📌 Generar Caso de Estudio")

    # Selección de industria
    industria = st.selectbox(
        "🏭 Selecciona la industria del caso:",
        ["Salud", "Finanzas", "Ambiental", "Educación", "Tecnología", "Manufactura"]
    )

    # Botón para generar caso
    if st.button("🧠 Generar Caso"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("⚠️ Falta GOOGLE_API_KEY en el archivo .env")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Genera un caso de estudio del sector {industria.lower()} con problemas de seguridad de la información "
                "según la norma ISO 27001. Incluye tipo de organización, amenaza detectada, activos afectados y brechas."
            )
            response = model.generate_content(prompt)
            st.session_state.caso = limpiar_formato(response.text)

    # Mostrar el caso en formato plano (no editable)
    if st.session_state.caso:
        st.markdown("#### 🧠 Caso de Estudio Generado:")
        st.markdown(st.session_state.caso, unsafe_allow_html=True)
    else:
        st.info("💡 Genera el caso de estudio presionando el botón.")

    # Botón para generar planificación
    st.markdown("### 📋 Generar Planificación basada en ISO 27001")

    if st.button("📋 Generar Planificación"):
        if not st.session_state.caso:
            st.warning("⚠️ Primero genera el caso de estudio.")
        else:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"A partir del caso:\n{st.session_state.caso}\n\n"
                "Genera una planificación con controles ISO 27001 recomendados, responsables, tiempos y prioridades, "
                "preferiblemente en formato estructurado."
            )
            response = model.generate_content(prompt)
            st.session_state.planificacion = limpiar_formato(response.text)

    # Mostrar planificación
    if st.session_state.planificacion:
        st.markdown("#### 📝 Planificación Generada:")
        st.markdown(st.session_state.planificacion, unsafe_allow_html=True)

    st.markdown("---")

    # Botón para generar sugerencias
    if st.button("💡 Generar Sugerencias"):
        if not st.session_state.caso or not st.session_state.planificacion:
            st.warning("⚠️ Primero genera el caso y la planificación.")
        else:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Caso:\n{st.session_state.caso}\n\n"
                f"Planificación:\n{st.session_state.planificacion}\n\n"
                "Sugiere mejoras estratégicas adicionales según la norma ISO 27001 y buenas prácticas."
            )
            response = model.generate_content(prompt)
            st.session_state.sugerencias = limpiar_formato(response.text)

    # Mostrar sugerencias en formato plano
    if st.session_state.sugerencias:
        st.markdown("#### 💡 Sugerencias Generadas:")
        st.markdown(st.session_state.sugerencias, unsafe_allow_html=True)
    else:
        st.info("💡 Presiona el botón para generar sugerencias.")

# ========================================
# TAB 2: Ingreso de la Respuesta del Usuario
# ========================================
with tabs[1]:
    st.subheader("📝 Solución del Usuario")
    respuesta = st.text_area("✍️ Ingresa tu solución propuesta:", height=300)
    st.session_state.respuesta_usuario = limpiar_formato(respuesta)

# ========================================
# TAB 3: Evaluación de la Respuesta
# ========================================
with tabs[2]:
    st.subheader("📊 Evaluación")

    if st.button("✅ Evaluar Respuesta"):
        if len(st.session_state.respuesta_usuario.strip()) < 4:
            st.session_state.evaluacion = (0, "⚠️ Respuesta vacía o irrelevante.")
        else:
            promedio, puntuaciones, resumen = evaluar_respuesta(
                st.session_state.caso, st.session_state.respuesta_usuario
            )
            st.session_state.evaluacion = (promedio, resumen)
            st.session_state.puntuaciones = puntuaciones

    if "puntuaciones" in st.session_state:
        st.markdown(f"### ✅ Calificación General: {st.session_state.evaluacion[0]}%")
        for crit, val in st.session_state.puntuaciones.items():
            st.markdown(f"- **{crit}**: {val}%")
        st.info(st.session_state.evaluacion[1])

    # 💾 Guardar y Exportar
    if st.button("💾 Guardar y Exportar Caso"):
        guardar_en_historial(
            st.session_state.caso,
            st.session_state.planificacion,
            st.session_state.sugerencias,
            st.session_state.respuesta_usuario,
            st.session_state.evaluacion
        )
        pdf_file = exportar_pdf(
            st.session_state.caso,
            st.session_state.planificacion,
            st.session_state.sugerencias,
            st.session_state.respuesta_usuario,
            st.session_state.evaluacion
        )
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Descargar PDF",
                file_name="caso_estudio.pdf",
                mime="application/pdf",
                data=f.read()
            )

# ========================================
# TAB 4: Historial de Casos
# ========================================
with tabs[3]:
    st.subheader("📚 Historial de Casos Generados")
    historial = cargar_historial()

    if historial:
        opciones = [f"{i+1}. {h['fecha']} - {h['evaluacion']['puntaje']}%" for i, h in enumerate(historial)]
        seleccion = st.selectbox("Selecciona un caso:", opciones)
        indice = opciones.index(seleccion)
        caso_sel = historial[indice]

        if st.button("📂 Cargar Caso Seleccionado"):
            st.session_state.caso = caso_sel["caso"]
            st.session_state.planificacion = caso_sel.get("planificacion", "")
            st.session_state.sugerencias = caso_sel.get("sugerencias", "")
            st.session_state.respuesta_usuario = caso_sel["respuesta_usuario"]
            st.session_state.evaluacion = (
                caso_sel["evaluacion"]["puntaje"],
                caso_sel["evaluacion"]["justificacion"]
            )
            st.success("✅ Caso cargado correctamente.")

        if st.button("❌ Borrar Caso del Historial"):
            if borrar_del_historial(indice):
                st.success("✅ Caso borrado.")
            else:
                st.error("❌ Error al borrar el caso.")
    else:
        st.info("ℹ️ No hay historial disponible.")
