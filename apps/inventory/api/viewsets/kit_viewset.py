
from apps.inventory.models import Kit
from apps.inventory.api.serializers.kit_serializer import KitSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class KitViewSet(BaseModelViewSet):
    queryset=Kit.objects.all()
    serializer_class=KitSerializer
    ordering_fields = Kit.FILTER_SORT_ORDER_FIELDS