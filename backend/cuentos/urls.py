from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerfilNinoViewSet, ModeloVozViewSet, CuentoViewSet, RegistroView, LoginView

router = DefaultRouter()
router.register(r'ninos', PerfilNinoViewSet, basename='nino')
router.register(r'voces', ModeloVozViewSet, basename='voz')
router.register(r'cuentos', CuentoViewSet, basename='cuento')

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
]