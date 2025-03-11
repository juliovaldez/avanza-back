
from apps.inventory.models import UnitConversion
from apps.inventory.api.serializers.unit_conversion_serializer import UnitConversionSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class UnitConversionViewSet(BaseModelViewSet):
    queryset=UnitConversion.objects.all()
    serializer_class=UnitConversionSerializer
    ordering_fields = UnitConversion.FILTER_SORT_ORDER_FIELDS