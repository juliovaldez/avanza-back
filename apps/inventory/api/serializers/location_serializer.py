
from rest_framework import serializers
from apps.inventory.models import Location
from api.common.base_models import BaseModelSerializer

class LocationSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=Location
        fields= "__all__"
