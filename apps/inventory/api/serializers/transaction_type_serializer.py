
from rest_framework import serializers
from apps.inventory.models import TransactionType
from api.common.base_models import BaseModelSerializer

class TransactionTypeSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=TransactionType
        fields='__all__'