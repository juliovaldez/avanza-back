from rest_framework import serializers
from apps.inventory.models import Status
from api.common.base_models import BaseModelSerializer

class StatusSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=Status
        fields='__all__'
    