from api.common.base_models import BaseModelSerializer
from apps.casos_exito.models import CasoExito


class CasoExitoSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CasoExito
        fields = [
            "id",
            "titulo",
            "descripcion",
            "fotografia",
            "created_at",
            "updated_at",
        ]
