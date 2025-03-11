
from apps.inventory.models import TransactionType
from apps.inventory.api.serializers.transaction_type_serializer import TransactionTypeSerializer
from api.common.base_models import BaseModelViewSet
from rest_framework.filters import OrderingFilter
from django.db.models import Sum

class TransactionTypeViewSet(BaseModelViewSet):
    queryset=TransactionType.objects.all()
    serializer_class=TransactionTypeSerializer
    ordering_fields = TransactionType.FILTER_SORT_ORDER_FIELDS

