from apps.inventory.models import TxnDocument
from apps.inventory.api.serializers.txn_document_serializer import TxnDocumentSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet


class TxnDocumentViewSet(BaseModelViewSet):
    queryset=TxnDocument.objects.all()
    serializer_class=TxnDocumentSerializer
    ordering_fields = TxnDocument.FILTER_SORT_ORDER_FIELDS