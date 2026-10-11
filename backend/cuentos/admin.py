from django.contrib import admin
from .models import PerfilNino, ModeloVoz, Cuento

@admin.register(PerfilNino)
class PerfilNinoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'intereses', 'valores')
    search_fields = ('nombre', 'intereses')
    list_filter = ('edad',)

@admin.register(Cuento)
class CuentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nino')
    search_fields = ('titulo', 'nino__nombre')


admin.site.register(ModeloVoz)