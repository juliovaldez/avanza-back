
from rest_framework import serializers
from apps.inventory.models import Transaction
from api.common.base_models import BaseModelSerializer
from apps.inventory.api.serializers.material_serializer import MaterialSerializer
from rest_framework import serializers

class TransactionSerializer(BaseModelSerializer):
    #material = MaterialSerializer()
    class Meta(BaseModelSerializer.Meta):
        model=Transaction
        fields='__all__'
        
        
class TxnMaterialSummarySerializer(serializers.Serializer):
    material = serializers.IntegerField()
    material_name = serializers.CharField(source='material__name')
    serial_number = serializers.CharField()
    base_unit = serializers.IntegerField()
    total_base_quantity=serializers.FloatField() 
    total_available_quantity = serializers.FloatField() 