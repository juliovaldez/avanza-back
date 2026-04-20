from django.contrib import admin
from apps.testimonials.models import Testimonio


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "ciudad", "estado", "created_at")
    search_fields = ("nombre_completo", "ciudad", "estado")
    list_filter = ("estado",)
