from django.contrib import admin
from apps.sepomex.models import Estado, Municipio, Asentamiento, CargaSepomex


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ("clave", "nombre")
    search_fields = ("nombre",)


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ("clave", "nombre", "estado")
    list_filter = ("estado",)
    search_fields = ("nombre",)


@admin.register(Asentamiento)
class AsentamientoAdmin(admin.ModelAdmin):
    list_display = ("codigo_postal", "nombre", "tipo", "municipio")
    list_filter = ("tipo", "zona")
    search_fields = ("codigo_postal", "nombre")


@admin.register(CargaSepomex)
class CargaSepomexAdmin(admin.ModelAdmin):
    list_display = ("nombre_archivo", "fecha_carga", "estado_proceso", "total_registros")
    readonly_fields = ("fecha_carga",)
