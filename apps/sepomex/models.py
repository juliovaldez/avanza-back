from django.db import models
from django.utils import timezone


class Estado(models.Model):
    clave = models.CharField(max_length=2, unique=True)
    nombre = models.CharField(max_length=35)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    clave = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="municipios")

    class Meta:
        unique_together = ("clave", "estado")
        ordering = ["nombre"]
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return f"{self.nombre}, {self.estado.nombre}"


class Asentamiento(models.Model):
    codigo_postal = models.CharField(max_length=5, db_index=True)
    nombre = models.CharField(max_length=60)
    tipo = models.CharField(max_length=40)
    zona = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="asentamientos")

    class Meta:
        indexes = [
            models.Index(fields=["codigo_postal"]),
            models.Index(fields=["nombre"]),
        ]
        verbose_name = "Asentamiento"
        verbose_name_plural = "Asentamientos"

    def __str__(self):
        return f"{self.nombre} ({self.codigo_postal})"


class CargaSepomex(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE  = "pendiente",  "Pendiente"
        PROCESANDO = "procesando", "Procesando"
        COMPLETADO = "completado", "Completado"
        ERROR      = "error",      "Error"

    nombre_archivo   = models.CharField(max_length=255)
    fecha_carga      = models.DateTimeField(default=timezone.now)
    estado_proceso   = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    total_registros  = models.IntegerField(default=0)
    registros_procesados = models.IntegerField(default=0)
    mensaje          = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_carga"]
        verbose_name = "Carga SEPOMEX"

    def __str__(self):
        return f"{self.nombre_archivo} — {self.estado_proceso}"
