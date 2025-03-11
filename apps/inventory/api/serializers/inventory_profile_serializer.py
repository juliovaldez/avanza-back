from rest_framework import serializers
from apps.inventory.models import inventoryProfile
from api.common.base_models import BaseModelSerializer

class InventoryProfileSerializer(BaseModelSerializer):
    location_name = serializers.SerializerMethodField()
    class Meta(BaseModelSerializer.Meta):
        model=inventoryProfile
        fields='__all__'
        
    def validate(self, data):
        user = data.get('user')
        location = data.get('location')
        if not location.users.filter(id=user.id).exists():
            raise serializers.ValidationError(
                {"location": "The user does not belong to the specified location."}
            )
        return data
    
    def get_location_name(self, obj):
        return obj.location.name