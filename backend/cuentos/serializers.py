from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PerfilNino, ModeloVoz, Cuento

class PerfilNinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilNino
        fields = '__all__'
        read_only_fields = ['usuario'] 

class ModeloVozSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloVoz
        fields = '__all__'
        read_only_fields = ['usuario']

class CuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuento
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user        