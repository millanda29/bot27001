import streamlit as st
from utils import limpiar_formato, cargar_historial, guardar_en_historial, borrar_del_historial
from evaluador import evaluar_respuesta
from pdf_utils import exportar_pdf

# Configuración de la página
st.set_page_config(page_title="ChatBot ISO 27001", page_icon="🛡️", layout="wide")

# Estado de sesión
if "caso" not in st.session_state:
    st.session_state.caso = ""
if "planificacion" not in st.session_state:
    st.session_state.planificacion = ""
if "sugerencias" not in st.session_state:
    st.session_state.sugerencias = ""
if "respuesta_usuario" not in st.session_state:
    st.session_state.respuesta_usuario = ""
if "evaluacion" not in st.session_state:
    st.session_state.evaluacion = (0, "")
historial = cargar_historial()

# UI: Estilos
st.markdown("""
    <style>
        .title { font-size:36px; font-weight:bold; color:#1a73e8; }
        .subtitle { font-size:24px; font-weight:bold; margin-top:10px; }
    </style>
""", unsafe_allow_html=True)

# Cabecera
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; text-align: center;">
        <img src="https://i.pinimg.com/originals/79/04/42/7904424933cc535b666f2de669973530.gif" alt="GIF" style="width: 330px; height: 250px; margin-right: 20px;">
        <div>
            <div class="title">🛡️ ChatBot ISO 27001</div>
            <div class="title"> GRUPO N°4 </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# Descripción del proyecto
st.markdown("""
    <div style="padding: 15px; border-radius: 5px;">
        <p style="color: white;">
            Esta aplicación permite simular el análisis de la norma ISO/IEC 27001. Se genera automáticamente un caso de estudio real o ficticio con una problemática de seguridad de la información. El usuario propone una solución que se compara y evalúa con criterios técnicos como relevancia, comprensión y aplicación de la norma.
        </p>
    </div>
""", unsafe_allow_html=True)

# Tabs principales
tabs = st.tabs([
    "📌 Generar Caso",
    "📝 Ingresar Respuesta",
    "📊 Evaluación",
    "📚 Historial"
])

# Tab 1 - Generar Caso
with tabs[0]:
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os

    st.subheader("📌 Generar Caso de Estudio")

    # Selector de industria
    col1, col2 = st.columns(2)

    with col1:
        industria = st.selectbox(
            "🏭 Selecciona la industria del caso de estudio:",
            ["Salud", "Finanzas", "Ambiental", "Educación", "Tecnología", "Manufactura"]
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧠 Generar Caso"):
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                st.error("⚠️ Falta GOOGLE_API_KEY en el archivo .env")
            else:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Prompt que considera la industria seleccionada
                prompt_caso = (
                    f"Genera únicamente un caso de estudio sobre una organización del sector {industria.lower()} con problemas de seguridad de la información. "
                    "Debe estar relacionado con la norma ISO 27001 e incluir: tipo de organización, amenaza detectada, "
                    "impacto sobre los activos, y brechas identificadas."
                )
                response = model.generate_content(prompt_caso)
                st.session_state.caso = limpiar_formato(response.text)

        st.text_area("🧠 Caso de Estudio", value=st.session_state.get("caso", ""), height=300)

    with col2:
        if st.button("📋 Generar Planificación"):
            if not st.session_state.get("caso"):
                st.warning("⚠️ Primero genera el caso de estudio.")
            else:
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt_plan = (
                    f"A partir del siguiente caso de estudio:\n{st.session_state.caso}\n\n"
                    "Elabora una planificación para tratar los problemas de seguridad. Incluye controles ISO 27001 sugeridos, "
                    "responsables, tiempos y prioridades."
                )
                response = model.generate_content(prompt_plan)
                st.session_state.planificacion = limpiar_formato(response.text)

        st.text_area("📋 Planificación", value=st.session_state.get("planificacion", ""), height=300)

    st.markdown("---")
    if st.button("💡 Generar Sugerencias"):
        if not st.session_state.get("caso") or not st.session_state.get("planificacion"):
            st.warning("⚠️ Primero genera el caso y la planificación.")
        else:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt_sugerencias = (
                f"Caso:\n{st.session_state.caso}\n\n"
                f"Planificación:\n{st.session_state.planificacion}\n\n"
                "Sugiere mejoras adicionales para abordar la situación descrita, basadas en buenas prácticas, "
                "la norma ISO 27001 y un enfoque estratégico de seguridad."
            )
            response = model.generate_content(prompt_sugerencias)
            st.session_state.sugerencias = limpiar_formato(response.text)

    st.text_area("💡 Sugerencias", value=st.session_state.get("sugerencias", ""), height=200)

# Tab 2 - Ingresar Respuesta
with tabs[1]:
    st.subheader("📝 Solución del Usuario")
    respuesta = st.text_area("✍️ Ingresa tu solución propuesta:", height=300)
    st.session_state.respuesta_usuario = limpiar_formato(respuesta)

# Tab 3 - Evaluación
with tabs[2]:
    st.subheader("📊 Evaluación")
    if st.button("Evaluar"):
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

    if st.button("💾 Guardar y Exportar Caso"):
        guardar_en_historial(
            st.session_state.caso,
            st.session_state.planificacion,  # Agregar planificación
            st.session_state.sugerencias,  # Agregar sugerencias
            st.session_state.respuesta_usuario,
            st.session_state.evaluacion
        )
        pdf_file = exportar_pdf(
            st.session_state.caso,
            st.session_state.planificacion,  # Agregar planificación
            st.session_state.sugerencias,  # Agregar sugerencias
            st.session_state.respuesta_usuario,
            st.session_state.evaluacion
        )

        # Abre el archivo temporal generado en modo binario para su lectura
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Descargar PDF",
                file_name="caso_estudio.pdf",
                mime="application/pdf",
                data=f.read()  # Ahora se lee el archivo correctamente
            )

# Tab 4 - Historial
with tabs[3]:
    st.subheader("📚 Historial de Casos Generados")
    historial = cargar_historial()

    if historial:
        # Mostrar historial de manera clara
        opciones = [f"{i + 1}. {h['fecha']} - {h['evaluacion']['puntaje']}%" for i, h in enumerate(historial)]
        seleccion = st.selectbox("Selecciona un caso anterior:", opciones)
        indice = opciones.index(seleccion)
        caso_sel = historial[indice]

        # Cargar caso seleccionado
        if st.button("📂 Cargar Caso Seleccionado"):
            st.session_state.caso = caso_sel["caso"]
            st.session_state.respuesta_usuario = caso_sel["respuesta_usuario"]
            st.session_state.evaluacion = (
                caso_sel["evaluacion"]["puntaje"],
                caso_sel["evaluacion"]["justificacion"]
            )
            st.success("Caso cargado correctamente.")

        # Opción para borrar caso del historial
        if st.button("❌ Borrar Caso del Historial"):
            if borrar_del_historial(indice):
                st.success("Caso borrado del historial.")
                # Recargar historial después de borrar
                historial = cargar_historial()
            else:
                st.error("Error al borrar el caso.")
    else:
        st.info("No hay historial aún.")
