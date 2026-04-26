from django.db import models
from api.common.base_models import BaseModel


class Propiedad(BaseModel):
    """
    Ficha técnica de una propiedad inmobiliaria.
    Todas las FKs apuntan a los catálogos de apps.catalogs.
    El campo equipamiento es M2M (puede tener varios).
    """

    # ── Información general ───────────────────────────────────────────────
    tipo_propiedad = models.ForeignKey(
        "catalogs.TipoPropiedad",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    metros_terreno = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name="Metros de terreno",
    )
    metros_construccion = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name="Metros de construcción",
    )
    precio = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
    )

    # ── Características ───────────────────────────────────────────────────
    habitaciones = models.PositiveSmallIntegerField(null=True, blank=True)
    banos        = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Baños")
    medio_bano   = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name="Medio baño")
    niveles      = models.PositiveSmallIntegerField(null=True, blank=True)
    cochera      = models.PositiveSmallIntegerField(null=True, blank=True)
    antiguedad   = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Antigüedad (años)")

    # ── Calidad y acabados ────────────────────────────────────────────────
    calidad_construccion = models.ForeignKey(
        "catalogs.CalidadConstruccion",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    estado_conservacion = models.ForeignKey(
        "catalogs.EstadoConservacion",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    tipo_acabado = models.ForeignKey(
        "catalogs.TipoAcabado",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    mantenimiento = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name="Mantenimiento (mensual $)",
    )
    equipamiento = models.ManyToManyField(
        "catalogs.Equipamiento",
        blank=True,
        related_name="propiedades",
    )

    # ── Documentación legal ───────────────────────────────────────────────
    documento_propiedad = models.ForeignKey(
        "catalogs.DocumentoPropiedad",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    predial = models.ForeignKey(
        "catalogs.Predial",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    servicios_corriente = models.ForeignKey(
        "catalogs.ServiciosCorriente",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    gravamen = models.ForeignKey(
        "catalogs.Gravamen",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )
    situacion_legal = models.ForeignKey(
        "catalogs.SituacionLegal",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="propiedades",
    )

    # ── Ubicación ─────────────────────────────────────────────────────────────
    asentamiento = models.ForeignKey(
        "sepomex.Asentamiento",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="propiedades",
        verbose_name="Colonia / Asentamiento",
    )

    class Meta:
        verbose_name        = "Propiedad"
        verbose_name_plural = "Propiedades"
        ordering            = ["-created_at"]

    def __str__(self):
        tipo = self.tipo_propiedad.nombre if self.tipo_propiedad else "Propiedad"
        precio = f"${self.precio:,.0f}" if self.precio else "sin precio"
        return f"{tipo} — {precio}"
