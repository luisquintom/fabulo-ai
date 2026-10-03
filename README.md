# ✨ Fabulo.ai

Plataforma web full-stack orientada a la generación y narración interactiva de cuentos infantiles hiper-personalizados mediante Inteligencia Artificial. 

Este repositorio contiene el código fuente desarrollado para el **Trabajo de Fin de Máster (TFM)** del **Máster Universitario en Desarrollo de Aplicaciones Web** de la **Universidad Europea de Madrid**.

**Autor:** Luis Enrique Quinto Munive  

---

## 🚀 Arquitectura y Tecnologías

El sistema implementa una arquitectura basada en microservicios e integración de APIs cognitivas, orquestada bajo un modelo híbrido (despliegue de infraestructura local mediante contenedores e inferencia de IA en la nube).

### Frontend (Cliente)
* **Framework:** Angular 17+ (TypeScript)
* **Reactividad:** Signals y RxJS
* **Estilos:** HTML5, CSS3, Flexbox/Grid

### Backend (Servidor)
* **Framework:** Python con Django y Django REST Framework (DRF)
* **Base de Datos:** PostgreSQL
* **Almacenamiento:** Sistema de archivos local / MinIO (Media)

### Inteligencia Artificial & Servicios
* **Motor de Texto (LLM):** Google Gemini API (Modelo `gemini-3.8-flash`)
* **Síntesis de Voz (TTS):** Microsoft Edge TTS (Voces Neuronales)

### DevOps & Despliegue
* **Contenedorización:** Docker y Docker Compose
* **Control de Versiones:** Git / GitHub

---

## ⚙️ Requisitos Previos

Para ejecutar este proyecto en un entorno local, es necesario contar con:

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
2. Una API Key gratuita de [Google AI Studio](https://aistudio.google.com/).
3. Git instalado en el sistema.

---

## 🛠️ Instalación y Despliegue Local

**1. Clonar el repositorio**
bash
git clone [https://github.com/luisquintom/fabulo-ai.git]
cd fabulo-ai
**2. Configurar variables de entorno**
Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que docker-compose.yml) y añade las siguientes credenciales:

Fragmento de código
POSTGRES_DB=fabulo_db
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_password
GEMINI_API_KEY=tu_clave_de_google_aqui
**3. Construir y levantar la infraestructura**
Ejecuta el siguiente comando para descargar las imágenes, compilar el backend y levantar la base de datos de forma orquestada:

Bash
docker compose up -d --build
**4. Aplicar migraciones**
Una vez que los contenedores estén activos, inicializa la estructura de la base de datos PostgreSQL:

Bash
docker compose exec backend python manage.py migrate
**5. Acceder a la aplicación**

Panel Web (Angular): http://localhost:4200

API y Panel de Admin (Django): http://localhost:8000/admin

📂 Estructura del Proyecto
Plaintext
fabulo-ai/
├── backend/                  # API REST en Django
│   ├── core/                 # Configuraciones principales de Django
│   ├── cuentos/              # Lógica de negocio, servicios IA (Gemini/Edge TTS)
│   ├── media/                # Almacenamiento de audios generados (.mp3)
│   ├── requirements.txt      # Dependencias de Python
│   └── Dockerfile            # Configuración del contenedor Backend
├── frontend/                 # Interfaz de usuario en Angular
│   ├── src/                  # Componentes, servicios e interfaces
│   ├── package.json          # Dependencias de Node.js
│   └── Dockerfile            # Configuración del contenedor Frontend
├── docker-compose.yml        # Orquestación de servicios (PostgreSQL, Backend, Frontend)
└── README.md                 # Documentación del proyecto

**🔒 Privacidad y Seguridad (GDPR)**
*Este proyecto aplica los principios de Privacidad por Diseño. Todo el procesamiento de los perfiles de los menores se realiza de manera anonimizada mediante el uso de nombres de pila o seudónimos, y los audios generados a través de Edge TTS no requieren el almacenamiento persistente ni la cesión de datos biométricos reales de los usuarios.*