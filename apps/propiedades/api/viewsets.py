from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet
from apps.propiedades.models import Propiedad
from apps.propiedades.api.serializers import PropiedadSerializer


class PropiedadViewSet(BaseModelViewSet):
    queryset         = Propiedad.objects.all()
    serializer_class = PropiedadSerializer
    filter_backends  = [OrderingFilter]
    ordering_fields  = ["precio", "created_at", "habitaciones", "metros_construccion"]
    ordering         = ["-created_at"]

    def get_queryset(self):
        """Agrega select_related y prefetch_related al queryset filtrado."""
        return super().get_queryset().select_related(
            "tipo_propiedad",
            "calidad_construccion",
            "estado_conservacion",
            "tipo_acabado",
            "documento_propiedad",
            "predial",
            "servicios_corriente",
            "gravamen",
            "situacion_legal",
        ).prefetch_related("equipamiento").select_related(
            "asentamiento__municipio__estado",
        )
