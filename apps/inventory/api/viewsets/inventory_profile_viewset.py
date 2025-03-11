
from apps.inventory.models import inventoryProfile
from apps.inventory.api.serializers.inventory_profile_serializer import InventoryProfileSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class InventoryProfileViewSet(BaseModelViewSet):
    queryset=inventoryProfile.objects.all()
    serializer_class=InventoryProfileSerializer
    ordering_fields = inventoryProfile.FILTER_SORT_ORDER_FIELDS