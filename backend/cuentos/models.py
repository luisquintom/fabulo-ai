from django.db import models
from django.contrib.auth.models import User

# 1. Entidad: Perfil_Niño
class PerfilNino(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ninos')
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    intereses = models.TextField(help_text="Ej: Dinosaurios, el espacio, princesas")
    valores = models.TextField(help_text="Ej: Amistad, valentía, compartir")

    class Meta:
        verbose_name = "Perfil de Niño"
        verbose_name_plural = "Perfiles de Niños"

    def __str__(self):
        return f"{self.nombre} (Hijo/a de {self.usuario.username})"

# 2. Entidad: Modelo_Voz
class ModeloVoz(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voces')
    nombre_voz = models.CharField(max_length=100, help_text="Ej: Voz de Mamá, Voz del Abuelo")
    elevenlabs_voice_id = models.CharField(max_length=255, blank=True, null=True)
    ruta_audio_muestra = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Modelo de Voz"
        verbose_name_plural = "Modelos de Voz"

    def __str__(self):
        return f"{self.nombre_voz} ({self.usuario.username})"

# 3. Entidad: Cuento
class Cuento(models.Model):
    nino = models.ForeignKey(PerfilNino, on_delete=models.CASCADE, related_name='cuentos')
    voz = models.ForeignKey(ModeloVoz, on_delete=models.SET_NULL, null=True, blank=True)
    
    titulo = models.CharField(max_length=200, blank=True)
    historia_texto = models.TextField(blank=True)
    ruta_audio_final = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cuento"
        verbose_name_plural = "Cuentos"

    def __str__(self):
        return f"{self.titulo} - Para: {self.nino.nombre}"