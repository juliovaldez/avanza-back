from django.db import models
from api.common.base_models import BaseModel


class ContactoConfig(BaseModel):
    """Singleton — solo debe existir un registro activo."""
    correo    = models.EmailField(max_length=254)
    whatsapp  = models.CharField(max_length=20, help_text="Número con código de país, ej: 524778938183")
    facebook  = models.URLField(max_length=500, blank=True, default="")
    instagram = models.URLField(max_length=500, blank=True, default="")
    tiktok    = models.URLField(max_length=500, blank=True, default="")

    class Meta(BaseModel.Meta):
        verbose_name = "Configuración de Contacto"
        verbose_name_plural = "Configuración de Contacto"

    def __str__(self):
        return f"Contacto — {self.correo}"
