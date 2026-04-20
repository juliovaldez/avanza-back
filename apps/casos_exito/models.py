from django.db import models
from api.common.base_models import BaseModel


class CasoExito(BaseModel):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to="casos_exito/", blank=True, null=True)

    FILTER_SORT_FIELDS = ["titulo", "created_at"]

    class Meta(BaseModel.Meta):
        verbose_name = "Caso de Éxito"
        verbose_name_plural = "Casos de Éxito"

    def __str__(self):
        return self.titulo
