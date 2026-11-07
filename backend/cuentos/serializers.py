from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PerfilNino, ModeloVoz, Cuento

class PerfilNinoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=50, required=True, allow_blank=False)
    intereses = serializers.CharField(max_length=200, required=True, allow_blank=False)
    valores = serializers.CharField(max_length=200, required=True, allow_blank=False)

    class Meta:
        model = PerfilNino
        fields = '__all__'
        read_only_fields = ['usuario'] 
        
    def validate_edad(self, value):
        if value is None or value < 1 or value > 15:
            raise serializers.ValidationError("La edad permitida es estrictamente entre 1 y 15 años.")
        return value

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
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Por seguridad, la contraseña debe tener al menos 6 caracteres.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user       