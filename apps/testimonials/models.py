from django.db import models
from api.common.base_models import BaseModel


class Testimonio(BaseModel):
    nombre_completo = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to="testimonios/", blank=True, null=True)

    FILTER_SORT_FIELDS = ["nombre_completo", "ciudad", "estado", "created_at"]

    class Meta(BaseModel.Meta):
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"

    def __str__(self):
        return f"{self.nombre_completo} — {self.ciudad}, {self.estado}"
