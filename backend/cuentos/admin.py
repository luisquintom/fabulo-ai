from django.contrib import admin

# Register your models here.
from .models import PerfilNino, ModeloVoz, Cuento

admin.site.register(PerfilNino)
admin.site.register(ModeloVoz)
admin.site.register(Cuento)