from rest_framework import serializers
from api.common.base_models import BaseModelSerializer
from apps.catalogs.models import (
    TipoPropiedad,
    CalidadConstruccion, EstadoConservacion,
    TipoAcabado, Mantenimiento, Equipamiento,
    DocumentoPropiedad, Predial, ServiciosCorriente,
    Gravamen, SituacionLegal,
)

CATALOGO_FIELDS = ["id", "nombre", "orden", "activo"]


def make_serializer(model_class):
    """Factory que genera un serializer estándar para cualquier catálogo."""
    class _Serializer(BaseModelSerializer):
        class Meta(BaseModelSerializer.Meta):
            model  = model_class
            fields = CATALOGO_FIELDS
    _Serializer.__name__ = f"{model_class.__name__}Serializer"
    return _Serializer


TipoPropiedadSerializer = make_serializer(TipoPropiedad)

CalidadConstruccionSerializer = make_serializer(CalidadConstruccion)
EstadoConservacionSerializer  = make_serializer(EstadoConservacion)
TipoAcabadoSerializer         = make_serializer(TipoAcabado)
MantenimientoSerializer       = make_serializer(Mantenimiento)
EquipamientoSerializer        = make_serializer(Equipamiento)

DocumentoPropiedadSerializer  = make_serializer(DocumentoPropiedad)
PredialSerializer             = make_serializer(Predial)
ServiciosCorrienteSerializer  = make_serializer(ServiciosCorriente)
GravamenSerializer            = make_serializer(Gravamen)
SituacionLegalSerializer      = make_serializer(SituacionLegal)
