from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from .models import PerfilNino, ModeloVoz, Cuento
from .serializers import PerfilNinoSerializer, ModeloVozSerializer, CuentoSerializer, UserSerializer
from .services import generar_cuento_ai

#  ENDPOINTS DE LA APLICACIÓN 

class PerfilNinoViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilNinoSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return PerfilNino.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def generar_cuento(self, request, pk=None):
        nino = self.get_object()
        
        resultado_ia = generar_cuento_ai(nino.nombre, nino.edad, nino.intereses, nino.valores)

        if resultado_ia["error"]:
            return Response({"error": resultado_ia["error"]}, status=status.HTTP_400_BAD_REQUEST)

        nuevo_cuento = Cuento.objects.create(
            nino=nino,
            titulo=f"La aventura mágica de {nino.nombre}",
            historia_texto=resultado_ia["texto"],
            ruta_audio_final=resultado_ia["audio_url"]
        )

        datos_respuesta = CuentoSerializer(nuevo_cuento).data
        datos_respuesta['audio_url'] = resultado_ia["audio_url"]

        return Response(datos_respuesta, status=status.HTTP_201_CREATED)

class ModeloVozViewSet(viewsets.ModelViewSet):
    serializer_class = ModeloVozSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ModeloVoz.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class CuentoViewSet(viewsets.ModelViewSet):
    serializer_class = CuentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cuento.objects.filter(nino__usuario=self.request.user)

# --- ENDPOINTS DE AUTENTICACIÓN ---

class RegistroView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username})
        return Response({"error": "Usuario o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)