from django.contrib import admin
from apps.propiedades.models import Propiedad


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = [
        "id", "tipo_propiedad", "precio",
        "habitaciones", "banos", "metros_construccion",
        "calidad_construccion", "estado_conservacion",
    ]
    list_filter  = ["tipo_propiedad", "calidad_construccion", "estado_conservacion"]
    search_fields = ["tipo_propiedad__nombre"]
    filter_horizontal = ["equipamiento"]
    readonly_fields = ["created_at", "updated_at"]
