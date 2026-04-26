"""Datos iniciales para los catálogos de Documentación."""
from django.db import migrations


def insertar_datos(apps, schema_editor):
    DocumentoPropiedad  = apps.get_model("catalogs", "DocumentoPropiedad")
    Predial             = apps.get_model("catalogs", "Predial")
    ServiciosCorriente  = apps.get_model("catalogs", "ServiciosCorriente")
    Gravamen            = apps.get_model("catalogs", "Gravamen")
    SituacionLegal      = apps.get_model("catalogs", "SituacionLegal")

    DocumentoPropiedad.objects.bulk_create([
        DocumentoPropiedad(nombre="Escrituras",              orden=1, activo=True),
        DocumentoPropiedad(nombre="Contrato de compraventa", orden=2, activo=True),
    ])

    Predial.objects.bulk_create([
        Predial(nombre="No adeudo", orden=1, activo=True),
        Predial(nombre="Adeudo",    orden=2, activo=True),
    ])

    ServiciosCorriente.objects.bulk_create([
        ServiciosCorriente(nombre="Agua", orden=1, activo=True),
        ServiciosCorriente(nombre="Luz",  orden=2, activo=True),
        ServiciosCorriente(nombre="Gas",  orden=3, activo=True),
    ])

    Gravamen.objects.bulk_create([
        Gravamen(nombre="Libre de gravamen", orden=1, activo=True),
        Gravamen(nombre="Infonavit",         orden=2, activo=True),
        Gravamen(nombre="Préstamos",         orden=3, activo=True),
        Gravamen(nombre="Bancario",          orden=4, activo=True),
    ])

    SituacionLegal.objects.bulk_create([
        SituacionLegal(nombre="Invadida", orden=1, activo=True),
        SituacionLegal(nombre="Juicio",   orden=2, activo=True),
    ])


def revertir_datos(apps, schema_editor):
    for model_name in [
        "DocumentoPropiedad", "Predial", "ServiciosCorriente",
        "Gravamen", "SituacionLegal",
    ]:
        apps.get_model("catalogs", model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalogs", "0005_documentacion_models"),
    ]

    operations = [
        migrations.RunPython(insertar_datos, revertir_datos),
    ]
