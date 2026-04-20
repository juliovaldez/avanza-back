from api.common.base_models import BaseModelSerializer
from apps.testimonials.models import Testimonio


class TestimonioSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Testimonio
        fields = [
            "id",
            "nombre_completo",
            "ciudad",
            "estado",
            "descripcion",
            "fotografia",
            "created_at",
            "updated_at",
        ]
