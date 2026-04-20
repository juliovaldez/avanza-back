from django.contrib import admin
from apps.contacto.models import ContactoConfig


@admin.register(ContactoConfig)
class ContactoConfigAdmin(admin.ModelAdmin):
    list_display = ("correo", "whatsapp", "updated_at")
