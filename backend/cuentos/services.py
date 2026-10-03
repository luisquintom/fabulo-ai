import os
import asyncio
import edge_tts
import google.generativeai as genai
import time

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Función asíncrona exclusiva para generar y guardar el audio de Microsoft
async def crear_audio_edge(texto, ruta_salida):
    # Usamos una voz neuronal en español (puedes cambiarla luego si prefieres tono latino)
    voz = "es-ES-AlvaroNeural" 
    comunicar = edge_tts.Communicate(texto, voz)
    await comunicar.save(ruta_salida)

def generar_cuento_ai(nombre, edad, intereses, valores):
    prompt = (
        f"Escribe un cuento infantil corto, mágico y muy creativo para un niño/a "
        f"llamado {nombre} de {edad} años. "
        f"El cuento debe estar centrado en estos intereses: {intereses}. "
        f"Además, la moraleja de la historia debe enseñar estos valores: {valores}. "
        f"El lenguaje debe ser tierno, fácil de entender y estructurado en párrafos cortos."
    )
    
    try:
        # 1. Generamos el texto con Google Gemini
        modelo = genai.GenerativeModel('gemini-3.8-flash')
        respuesta_ia = modelo.generate_content(prompt)
        texto_cuento = respuesta_ia.text
        
        # 2. Preparamos el almacenamiento del audio
        # Creamos una carpeta 'media' en el backend si no existe
        os.makedirs("media", exist_ok=True) 
        nombre_archivo = f"cuento_{nombre.lower()}_{int(time.time())}.mp3"
        ruta_absoluta = os.path.join("media", nombre_archivo)
        
        # 3. Generamos el audio MP3 ejecutando la función asíncrona
        asyncio.run(crear_audio_edge(texto_cuento, ruta_absoluta))
        
        # Devolvemos un diccionario con ambas cosas listas
        return {
            "texto": texto_cuento,
            "audio_url": f"http://localhost:8000/media/{nombre_archivo}", # URL provisional para Angular
            "error": None
        }
        
    except Exception as e:
        return {"texto": None, "audio_url": None, "error": f"Error en la IA: {str(e)}"}