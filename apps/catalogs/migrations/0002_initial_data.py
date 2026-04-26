"""
Datos iniciales para los catálogos de propiedad.
Ejecutar solo una vez, en el primer deploy.
"""
from django.db import migrations


def insertar_datos(apps, schema_editor):
    TipoPropiedad   = apps.get_model("catalogs", "TipoPropiedad")
    Habitaciones    = apps.get_model("catalogs", "Habitaciones")
    Banos           = apps.get_model("catalogs", "Banos")
    Niveles         = apps.get_model("catalogs", "Niveles")
    Estacionamiento = apps.get_model("catalogs", "Estacionamiento")
    Antiguedad      = apps.get_model("catalogs", "Antiguedad")

    TipoPropiedad.objects.bulk_create([
        TipoPropiedad(nombre="Casa",          orden=1, activo=True),
        TipoPropiedad(nombre="Departamento",  orden=2, activo=True),
    ])

    Habitaciones.objects.bulk_create([
        Habitaciones(nombre="1", orden=1, activo=True),
        Habitaciones(nombre="2", orden=2, activo=True),
        Habitaciones(nombre="3", orden=3, activo=True),
        Habitaciones(nombre="4", orden=4, activo=True),
    ])

    Banos.objects.bulk_create([
        Banos(nombre="1/2 baño",    orden=1, activo=True),
        Banos(nombre="1 baño",      orden=2, activo=True),
        Banos(nombre="1½ baños",    orden=3, activo=True),
        Banos(nombre="2 baños",     orden=4, activo=True),
        Banos(nombre="2½ baños",    orden=5, activo=True),
        Banos(nombre="3 baños",     orden=6, activo=True),
        Banos(nombre="3½ baños",    orden=7, activo=True),
        Banos(nombre="4 baños",     orden=8, activo=True),
    ])

    Niveles.objects.bulk_create([
        Niveles(nombre="1", orden=1, activo=True),
        Niveles(nombre="2", orden=2, activo=True),
        Niveles(nombre="3", orden=3, activo=True),
        Niveles(nombre="4", orden=4, activo=True),
    ])

    Estacionamiento.objects.bulk_create([
        Estacionamiento(nombre="1", orden=1, activo=True),
        Estacionamiento(nombre="2", orden=2, activo=True),
        Estacionamiento(nombre="3", orden=3, activo=True),
        Estacionamiento(nombre="4", orden=4, activo=True),
    ])

    Antiguedad.objects.bulk_create([
        Antiguedad(nombre="1 año",   orden=1, activo=True),
        Antiguedad(nombre="2 años",  orden=2, activo=True),
        Antiguedad(nombre="3 años",  orden=3, activo=True),
        Antiguedad(nombre="4 años",  orden=4, activo=True),
        Antiguedad(nombre="5 años",  orden=5, activo=True),
    ])


def revertir_datos(apps, schema_editor):
    for model_name in [
        "TipoPropiedad", "Habitaciones", "Banos",
        "Niveles", "Estacionamiento", "Antiguedad",
    ]:
        apps.get_model("catalogs", model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalogs", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insertar_datos, revertir_datos),
    ]
