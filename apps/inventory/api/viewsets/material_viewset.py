from apps.inventory.models import Material
from apps.inventory.api.serializers.material_serializer import MaterialSerializer
from rest_framework.filters import OrderingFilter
from api.common.base_models import BaseModelViewSet

class MaterialViewset(BaseModelViewSet):
    queryset=Material.objects.all()
    serializer_class=MaterialSerializer
    ordering_fields = Material.FILTER_SORT_ORDER_FIELDS