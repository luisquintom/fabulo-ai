import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generar_cuento_ai(nombre, edad, intereses, valores):
    prompt = (
        f"Escribe un cuento infantil corto, mágico y muy creativo para un niño/a "
        f"llamado {nombre} de {edad} años. "
        f"El cuento debe estar centrado en estos intereses: {intereses}. "
        f"Además, la moraleja de la historia debe enseñar estos valores: {valores}. "
        f"El lenguaje debe ser tierno, fácil de entender y estructurado en párrafos cortos."
    )
    
    try:
        modelo = genai.GenerativeModel('gemini-3.5-flash-lite')
        respuesta_ia = modelo.generate_content(prompt)
        texto_cuento = respuesta_ia.text
        
        return {
            "texto": texto_cuento,
            "audio_url": None, 
            "error": None
        }
        
    except Exception as e:
        return {"texto": None, "audio_url": None, "error": f"Error en la IA: {str(e)}"}