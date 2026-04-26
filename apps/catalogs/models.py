from django.db import models
from api.common.base_models import BaseModel


class CatalogoBase(BaseModel):
    """
    Base abstracta para todos los catálogos de propiedad.
    Hereda: id, created_at, updated_at, deleted_at, notes.
    Agrega: nombre, orden, activo.
    """
    nombre = models.CharField(max_length=150)
    orden  = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class TipoPropiedad(CatalogoBase):
    class Meta:
        verbose_name        = "Tipo de Propiedad"
        verbose_name_plural = "Tipos de Propiedad"
        ordering            = ["orden", "nombre"]


# ── Catálogos de Calidad ─────────────────────────────────────────────────────

class CalidadConstruccion(CatalogoBase):
    class Meta:
        verbose_name        = "Calidad de Construcción"
        verbose_name_plural = "Calidad de Construcción"
        ordering            = ["orden", "nombre"]


class EstadoConservacion(CatalogoBase):
    class Meta:
        verbose_name        = "Estado de Conservación"
        verbose_name_plural = "Estado de Conservación"
        ordering            = ["orden", "nombre"]


class TipoAcabado(CatalogoBase):
    class Meta:
        verbose_name        = "Tipo de Acabado"
        verbose_name_plural = "Tipos de Acabado"
        ordering            = ["orden", "nombre"]


class Mantenimiento(CatalogoBase):
    class Meta:
        verbose_name        = "Mantenimiento"
        verbose_name_plural = "Mantenimiento"
        ordering            = ["orden", "nombre"]


class Equipamiento(CatalogoBase):
    class Meta:
        verbose_name        = "Equipamiento"
        verbose_name_plural = "Equipamiento"
        ordering            = ["orden", "nombre"]


# ── Catálogos de Documentación ───────────────────────────────────────────────

class DocumentoPropiedad(CatalogoBase):
    class Meta:
        verbose_name        = "Documento de la Propiedad"
        verbose_name_plural = "Documentos de la Propiedad"
        ordering            = ["orden", "nombre"]


class Predial(CatalogoBase):
    class Meta:
        verbose_name        = "Predial"
        verbose_name_plural = "Predial"
        ordering            = ["orden", "nombre"]


class ServiciosCorriente(CatalogoBase):
    class Meta:
        verbose_name        = "Servicios al Corriente"
        verbose_name_plural = "Servicios al Corriente"
        ordering            = ["orden", "nombre"]


class Gravamen(CatalogoBase):
    class Meta:
        verbose_name        = "Gravamen"
        verbose_name_plural = "Gravamen"
        ordering            = ["orden", "nombre"]


class SituacionLegal(CatalogoBase):
    class Meta:
        verbose_name        = "Situación Legal"
        verbose_name_plural = "Situación Legal"
        ordering            = ["orden", "nombre"]
