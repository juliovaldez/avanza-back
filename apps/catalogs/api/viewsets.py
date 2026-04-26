from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet
from apps.catalogs.models import (
    TipoPropiedad,
    CalidadConstruccion, EstadoConservacion,
    TipoAcabado, Mantenimiento, Equipamiento,
    DocumentoPropiedad, Predial, ServiciosCorriente,
    Gravamen, SituacionLegal,
)
from apps.catalogs.api.serializers import (
    TipoPropiedadSerializer,
    CalidadConstruccionSerializer, EstadoConservacionSerializer,
    TipoAcabadoSerializer, MantenimientoSerializer, EquipamientoSerializer,
    DocumentoPropiedadSerializer, PredialSerializer, ServiciosCorrienteSerializer,
    GravamenSerializer, SituacionLegalSerializer,
)


class CatalogoBaseViewSet(BaseModelViewSet):
    """ViewSet común para todos los catálogos de propiedad."""
    filter_backends  = [OrderingFilter]
    ordering_fields  = ["nombre", "orden"]
    ordering         = ["orden", "nombre"]


class TipoPropiedadViewSet(CatalogoBaseViewSet):
    queryset         = TipoPropiedad.objects.all()
    serializer_class = TipoPropiedadSerializer


class CalidadConstruccionViewSet(CatalogoBaseViewSet):
    queryset         = CalidadConstruccion.objects.all()
    serializer_class = CalidadConstruccionSerializer


class EstadoConservacionViewSet(CatalogoBaseViewSet):
    queryset         = EstadoConservacion.objects.all()
    serializer_class = EstadoConservacionSerializer


class TipoAcabadoViewSet(CatalogoBaseViewSet):
    queryset         = TipoAcabado.objects.all()
    serializer_class = TipoAcabadoSerializer


class MantenimientoViewSet(CatalogoBaseViewSet):
    queryset         = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer


class EquipamientoViewSet(CatalogoBaseViewSet):
    queryset         = Equipamiento.objects.all()
    serializer_class = EquipamientoSerializer


class DocumentoPropiedadViewSet(CatalogoBaseViewSet):
    queryset         = DocumentoPropiedad.objects.all()
    serializer_class = DocumentoPropiedadSerializer


class PredialViewSet(CatalogoBaseViewSet):
    queryset         = Predial.objects.all()
    serializer_class = PredialSerializer


class ServiciosCorrienteViewSet(CatalogoBaseViewSet):
    queryset         = ServiciosCorriente.objects.all()
    serializer_class = ServiciosCorrienteSerializer


class GravamenViewSet(CatalogoBaseViewSet):
    queryset         = Gravamen.objects.all()
    serializer_class = GravamenSerializer


class SituacionLegalViewSet(CatalogoBaseViewSet):
    queryset         = SituacionLegal.objects.all()
    serializer_class = SituacionLegalSerializer
