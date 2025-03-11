from apps.inventory.models import Status
from apps.inventory.api.serializers.status_serializer import StatusSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class StatusViewset(BaseModelViewSet):
    queryset=Status.objects.all()
    serializer_class=StatusSerializer
    ordering_fields = Status.FILTER_SORT_ORDER_FIELDS
