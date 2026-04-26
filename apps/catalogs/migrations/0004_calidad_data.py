"""Datos iniciales para los catálogos de Calidad."""
from django.db import migrations


def insertar_datos(apps, schema_editor):
    CalidadConstruccion = apps.get_model("catalogs", "CalidadConstruccion")
    EstadoConservacion  = apps.get_model("catalogs", "EstadoConservacion")
    TipoAcabado         = apps.get_model("catalogs", "TipoAcabado")
    Mantenimiento       = apps.get_model("catalogs", "Mantenimiento")
    Equipamiento        = apps.get_model("catalogs", "Equipamiento")

    CalidadConstruccion.objects.bulk_create([
        CalidadConstruccion(nombre="Alto",  orden=1, activo=True),
        CalidadConstruccion(nombre="Medio", orden=2, activo=True),
        CalidadConstruccion(nombre="Bajo",  orden=3, activo=True),
    ])

    EstadoConservacion.objects.bulk_create([
        EstadoConservacion(nombre="Excelente", orden=1, activo=True),
        EstadoConservacion(nombre="Bueno",     orden=2, activo=True),
        EstadoConservacion(nombre="Regular",   orden=3, activo=True),
    ])

    TipoAcabado.objects.bulk_create([
        TipoAcabado(nombre="Lujo",      orden=1, activo=True),
        TipoAcabado(nombre="Estándar",  orden=2, activo=True),
        TipoAcabado(nombre="Básico",    orden=3, activo=True),
    ])

    Mantenimiento.objects.bulk_create([
        Mantenimiento(nombre="Alto",  orden=1, activo=True),
        Mantenimiento(nombre="Medio", orden=2, activo=True),
        Mantenimiento(nombre="Bajo",  orden=3, activo=True),
    ])

    Equipamiento.objects.bulk_create([
        Equipamiento(nombre="Closets", orden=1, activo=True),
        Equipamiento(nombre="Tinaco",  orden=2, activo=True),
        Equipamiento(nombre="Boiler",  orden=3, activo=True),
    ])


def revertir_datos(apps, schema_editor):
    for model_name in [
        "CalidadConstruccion", "EstadoConservacion",
        "TipoAcabado", "Mantenimiento", "Equipamiento",
    ]:
        apps.get_model("catalogs", model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalogs", "0003_calidad_models"),
    ]

    operations = [
        migrations.RunPython(insertar_datos, revertir_datos),
    ]
