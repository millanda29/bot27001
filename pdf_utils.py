from fpdf import FPDF
import tempfile

def limpiar_unicode(texto):
    """Reemplaza caracteres Unicode problemáticos con equivalentes ASCII."""
    reemplazos = {
        "\u2013": "-",   # guion largo
        "\u2014": "-",   # guion EM
        "\u2018": "'",   # comilla simple izquierda
        "\u2019": "'",   # comilla simple derecha
        "\u201c": '"',   # comilla doble izquierda
        "\u201d": '"',   # comilla doble derecha
        "\u2026": "...", # puntos suspensivos
        "–": "-",        # guion largo visible
        "—": "-",        # em dash
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'"
    }
    for caracter, reemplazo in reemplazos.items():
        texto = texto.replace(caracter, reemplazo)
    return texto

def agregar_tabla_planificacion(pdf, tabla_data):
    """Agrega una tabla formateada como texto plano"""
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, "Planificación de Controles", ln=True)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 9)
    columnas = ["Brecha", "Control", "Responsable", "Prioridad", "Tiempo", "Acciones", "Indicadores"]
    anchos = [30, 25, 30, 20, 15, 35, 35]

    # Cabecera de la tabla
    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 8, col, border=1)
    pdf.ln()

    # Cuerpo de la tabla
    pdf.set_font('Arial', '', 8)
    for fila in tabla_data:
        for i, campo in enumerate(fila):
            texto = campo.replace("<br>", "\n")
            pdf.multi_cell(anchos[i], 6, texto, border=1, align='L', max_line_height=pdf.font_size)
        pdf.ln()


class PDFProfesional(FPDF):
    def header(self):
        """Encabezado con título centrado"""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "Reporte de Evaluación - Caso ISO 27001", border=False, ln=True, align='C')
        self.ln(5)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        """Pie de página con numeración"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(100)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def agregar_seccion(self, titulo, contenido):
        """Agrega una sección con título en negrita y contenido justificado"""
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0)
        self.cell(0, 10, titulo, ln=True)
        self.ln(1)

        self.set_font('Arial', '', 11)
        self.set_text_color(50)
        self.multi_cell(0, 8, contenido)
        self.ln(5)

def exportar_pdf(caso, planificacion, sugerencias, respuesta, evaluacion):
    # Crear instancia del PDF personalizado
    pdf = PDFProfesional()
    pdf.add_page()

    # Secciones del contenido (limpiadas)
    pdf.agregar_seccion("1. Caso de Estudio", limpiar_unicode(caso))
    pdf.agregar_seccion("2. Planificación", limpiar_unicode(planificacion))
    pdf.agregar_seccion("3. Sugerencias", limpiar_unicode(sugerencias))
    pdf.agregar_seccion("4. Respuesta del Usuario", limpiar_unicode(respuesta))

    # Evaluación con subtítulos
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "5. Evaluación", ln=True)
    pdf.ln(1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, f"Puntaje: {evaluacion[0]}%")
    pdf.multi_cell(0, 8, f"Justificación: {limpiar_unicode(evaluacion[1])}")

    # Guardar PDF en archivo temporal
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_pdf.name)

    return temp_pdf.name
