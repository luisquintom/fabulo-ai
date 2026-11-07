from django.test import TestCase
from rest_framework.exceptions import ValidationError
from .serializers import PerfilNinoSerializer
from .services import sanitizar_texto

class SeguridadYValidacionTests(TestCase):
    
    
    # PRUEBAS UNITARIAS
    def test_sanitizar_texto_elimina_saltos_y_comillas(self):
        texto_malicioso = "Me gusta la pizza\ny los 'dinosaurios' con \"magia\"."
        resultado = sanitizar_texto(texto_malicioso)
        
        # Verificamos que no haya saltos de línea ni comillas
        self.assertNotIn('\n', resultado)
        self.assertNotIn('"', resultado)
        self.assertNotIn("'", resultado)
        self.assertEqual(resultado, "Me gusta la pizza y los dinosaurios con magia.")

    def test_sanitizar_texto_limita_longitud(self):
        texto_largo = "A" * 500
        resultado = sanitizar_texto(texto_largo)
        
        # Verificamos que el recorte estricto a 200 caracteres funcione
        self.assertEqual(len(resultado), 200)

    def test_sanitizar_texto_maneja_nulos(self):
        resultado = sanitizar_texto(None)
        self.assertEqual(resultado, "")

  
    # PRUEBAS DE INTEGRACIÓN: SERIALIZADORES
 
    def test_serializer_rechaza_edad_invalida(self):
        datos_invalidos = {
            "nombre": "Leo",
            "edad": 20,  # Edad fuera del rango 
            "intereses": "espacio",
            "valores": "valentía"
        }
        serializer = PerfilNinoSerializer(data=datos_invalidos)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('edad', serializer.errors)

    def test_serializer_acepta_datos_correctos(self):
        datos_validos = {
            "nombre": "Leo",
            "edad": 6,
            "intereses": "espacio",
            "valores": "valentía"
        }
        serializer = PerfilNinoSerializer(data=datos_validos)
        
        self.assertTrue(serializer.is_valid())