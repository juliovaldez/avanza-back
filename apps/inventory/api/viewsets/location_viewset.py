
from apps.inventory.models import Location
from apps.inventory.api.serializers.location_serializer import LocationSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class LocationViewSet(BaseModelViewSet):
    queryset = Location.objects.all()
    serializer_class =LocationSerializer
    ordering_fields = Location.FILTER_SORT_ORDER_FIELDS