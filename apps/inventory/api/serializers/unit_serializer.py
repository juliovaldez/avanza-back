
from rest_framework import serializers
from apps.inventory.models import Unit
from api.common.base_models import BaseModelSerializer

class UnitSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=Unit
        fields= "__all__"
