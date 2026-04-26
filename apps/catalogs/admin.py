from django.contrib import admin
from apps.catalogs.models import TipoPropiedad


@admin.register(TipoPropiedad)
class TipoPropiedadAdmin(admin.ModelAdmin):
    list_display = ["nombre", "orden", "activo"]
    list_editable = ["orden", "activo"]
    ordering = ["orden", "nombre"]
