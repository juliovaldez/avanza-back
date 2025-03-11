from rest_framework import serializers
from apps.inventory.models import Material
from api.common.base_models import BaseModelSerializer
class MaterialSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=Material
        fields='__all__'
        