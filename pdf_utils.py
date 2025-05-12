from fpdf import FPDF
import tempfile

def exportar_pdf(caso, planificacion, sugerencias, respuesta, evaluacion):
    pdf = FPDF()
    pdf.add_page()

    # Usar fuente estándar Arial en lugar de fuentes personalizadas
    pdf.set_font('Arial', 'B', 16)  # Fuente negrita
    pdf.cell(200, 10, "Caso de Estudio - ISO 27001", ln=True, align="C")

    pdf.set_font('Arial', '', 12)  # Fuente normal
    pdf.ln(10)

    pdf.multi_cell(0, 10, "Caso de Estudio - ISO 27001:")
    pdf.multi_cell(0, 10, caso)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "Planificación:")
    pdf.multi_cell(0, 10, planificacion)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "Sugerencias:")
    pdf.multi_cell(0, 10, sugerencias)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "RESPUESTA DEL USUARIO:")
    pdf.multi_cell(0, 10, respuesta)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "EVALUACIÓN:")
    pdf.multi_cell(0, 10, f"Puntaje: {evaluacion[0]}%")
    pdf.multi_cell(0, 10, f"Justificación: {evaluacion[1]}")

    # Guardar el PDF en un archivo temporal
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_pdf.name)

    # Retornar la ruta temporal del archivo para su descarga
    return temp_pdf.name
