from rest_framework import serializers
from apps.inventory.models import Kit
from api.common.base_models import BaseModelSerializer

class KitSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=Kit
        fields='__all__'
        