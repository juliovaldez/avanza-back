from rest_framework import serializers
from apps.inventory.models import TxnDocument
from api.common.base_models import BaseModelSerializer

class TxnDocumentSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model=TxnDocument
        fields='__all__'
        read_only_fields =getattr(BaseModelSerializer.Meta, 'read_only_fields', ()) + ('folio_number','from_user_location','to_user_location')