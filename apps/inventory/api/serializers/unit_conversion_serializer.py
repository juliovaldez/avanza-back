
from rest_framework import serializers
from apps.inventory.models import UnitConversion
from api.common.base_models import BaseModelSerializer

class UnitConversionSerializer(BaseModelSerializer):
    from_unit_name=serializers.SerializerMethodField()
    to_unit_name=serializers.SerializerMethodField()
    class Meta(BaseModelSerializer.Meta):
        model=UnitConversion
        fields='__all__'
        
        
    def get_from_unit_name(self, obj):
        return obj.from_unit.name

    def get_to_unit_name(self, obj):
        return obj.to_unit.name