
from apps.inventory.models import Unit
from apps.inventory.api.serializers.unit_serializer import UnitSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class UnitViewSet(BaseModelViewSet):
    queryset = Unit.objects.all()
    serializer_class =UnitSerializer
    ordering_fields = Unit.FILTER_SORT_ORDER_FIELDS