from rest_framework import serializers
from .models import PerfilNino, ModeloVoz, Cuento

class PerfilNinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilNino
        fields = '__all__' # Queremos que traduzca todos los campos del modelo

class ModeloVozSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloVoz
        fields = '__all__'

class CuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuento
        fields = '__all__'