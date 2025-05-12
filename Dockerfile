# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto que usa Streamlit
EXPOSE 8501

# Variable de entorno para producción (opcional)
ENV STREAMLIT_SERVER_HEADLESS=true

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]
