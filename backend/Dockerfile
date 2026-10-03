FROM python:3.11-slim

# Evita que Python guarde caché innecesaria y asegura que los logs se vean en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia e instala primero las dependencias (para optimizar la velocidad de Docker)
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código del backend
COPY . /app/