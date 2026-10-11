from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerfilNinoViewSet, ModeloVozViewSet, CuentoViewSet


router = DefaultRouter()
router.register(r'ninos', PerfilNinoViewSet)
router.register(r'voces', ModeloVozViewSet)
router.register(r'cuentos', CuentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]