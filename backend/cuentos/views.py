from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PerfilNino, ModeloVoz, Cuento
from .serializers import PerfilNinoSerializer, ModeloVozSerializer, CuentoSerializer
from .services import generar_cuento_ai # <--- Importamos nuestra función de IA

class PerfilNinoViewSet(viewsets.ModelViewSet):
    queryset = PerfilNino.objects.all()
    serializer_class = PerfilNinoSerializer

    # Creamos una ruta personalizada: POST /api/ninos/{id}/generar_cuento/
    @action(detail=True, methods=['post'])
    def generar_cuento(self, request, pk=None):
        nino = self.get_object() # Extraemos el perfil (ej: Luis) de PostgreSQL
        
        # Ejecutamos el servicio que ahora hace Texto + Voz
        resultado_ia = generar_cuento_ai(nino.nombre, nino.edad, nino.intereses, nino.valores)

        if resultado_ia["error"]:
            return Response({"error": resultado_ia["error"]}, status=status.HTTP_400_BAD_REQUEST)

        # Guardamos la historia en PostgreSQL (el modelo actual que ya tenías)
        nuevo_cuento = Cuento.objects.create(
            nino=nino,
            titulo=f"La aventura mágica de {nino.nombre}",
            historia_texto=resultado_ia["texto"]
        )

        # Empaquetamos la respuesta para Angular.
        # Le añadimos el audio_url manualmente para que el frontend pueda reproducirlo
        datos_respuesta = CuentoSerializer(nuevo_cuento).data
        datos_respuesta['audio_url'] = resultado_ia["audio_url"]

        return Response(datos_respuesta, status=status.HTTP_201_CREATED)

class ModeloVozViewSet(viewsets.ModelViewSet):
    queryset = ModeloVoz.objects.all()
    serializer_class = ModeloVozSerializer

class CuentoViewSet(viewsets.ModelViewSet):
    queryset = Cuento.objects.all()
    serializer_class = CuentoSerializer