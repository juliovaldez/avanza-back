from django.contrib import admin
from apps.casos_exito.models import CasoExito


@admin.register(CasoExito)
class CasoExitoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "created_at")
    search_fields = ("titulo",)
