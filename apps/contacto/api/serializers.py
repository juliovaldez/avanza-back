from api.common.base_models import BaseModelSerializer
from apps.contacto.models import ContactoConfig


class ContactoConfigSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = ContactoConfig
        fields = [
            "id",
            "correo",
            "whatsapp",
            "facebook",
            "instagram",
            "tiktok",
            "created_at",
            "updated_at",
        ]
