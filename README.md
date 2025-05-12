# ChatBot ISO 27001 🛡️

## Descripción ✨

¡Bienvenidos a la aplicación ChatBot ISO 27001! 🚀 Esta herramienta está diseñada para ayudar a los usuarios a simular y gestionar casos de estudio relacionados con la norma ISO 27001. Proporciona una interfaz amigable para generar, evaluar y planificar acciones, ¡y hasta puedes generar informes en PDF! 📑

## Características 🌟

- **Simulación de Casos de Estudio**: Genera casos de estudio sobre ISO 27001 con detalles personalizados para cada escenario. 🧑‍💻
- **Generación de PDF**: Exporta los detalles del caso, planificación, respuestas y evaluaciones a un archivo PDF con un solo clic. 📃
- **Historial de Casos**: Guarda y visualiza tus casos anteriores, ¡nunca pierdas un detalle importante! 📚

## Tecnologías ⚙️

- **Streamlit**: Para la interfaz de usuario interactiva y fácil de usar. 🖥️
- **FPDF**: Para generar PDFs con soporte para Unicode, utilizando fuentes como Arial y DejaVu. 🅰️
- **Python 3.x**: Lenguaje de programación principal de la aplicación. 🐍
- **API de IA (Gemini o similar)**: Usada para generar respuestas y evaluar casos. ¡No olvides tu **token de API**! 🔑

## Requisitos 📦

1. **Python 3.x** 🐍
2. **Dependencias de Python**: Instaladas desde el archivo `requirements.txt` 📄
3. **Token de API de IA**: Necesario para interactuar con el modelo de IA (Gemini o similar). Obtén tu propio token y configúralo en las variables de entorno 🔑

## Instalación 🛠️

1. Clona el repositorio:

   ```bash
   git clone https://github.com/millanda29/bot27001.git
   cd bot27001


2. Crea un entorno virtual y actívalo:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura el **token de la API de IA** en las variables de entorno. Crea un archivo `.env` en la raíz del proyecto y agrega tu token de API:

   ```
   GOOGLE_API_KEY=<tu_token_de_api_aqui>
   ```

5. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

## Uso 🚀

1. **Generación de Casos de Estudio**: Ingrese detalles sobre el caso de estudio relacionado con la ISO 27001. 📝
2. **Planificación y Evaluación**: Defina la planificación de seguridad y proporcione una evaluación para cada caso. ⚖️
3. **Generación de PDF**: Exporte el caso, la planificación y la evaluación en un PDF de alta calidad. 📑
4. **Visualización del Historial**: Vea un historial de los casos generados anteriormente. 📚

## Ejemplo de Flujo de Trabajo 📈

1. **Ingreso del Caso de Estudio**: Los usuarios proporcionan información sobre el caso de estudio relacionado con la ISO 27001. 💡
2. **Planificación y Evaluación**: El usuario define la planificación de seguridad y evalúa el caso según la normativa. 🧑‍💼
3. **Generación de PDF**: La aplicación permite exportar un archivo PDF con todos los detalles. 📄
4. **Visualización del Historial**: Accede a los casos anteriores generados para seguir el progreso. 📖

## Contribuciones 💻

¡Nos encantaría recibir tus contribuciones! Para ello, sigue estos pasos:

1. Haz un fork del repositorio. 🍴
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios necesarios y haz commit de ellos (`git commit -am 'Añadir nueva característica'`).
4. Haz push a tu rama (`git push origin feature/nueva-caracteristica`).
5. Abre un pull request. 🔄

## Licencia 📜

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles. ⚖️

