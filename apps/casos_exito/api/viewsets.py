from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from api.common.base_models import BaseModelViewSet
from api.utils.utils import json_response
from apps.casos_exito.models import CasoExito
from apps.casos_exito.api.serializers import CasoExitoSerializer


class CasoExitoViewSet(BaseModelViewSet):
    queryset = CasoExito.objects.all()
    ordering_fields = CasoExito.FILTER_SORT_FIELDS
    serializer_class = CasoExitoSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(data=serializer.data, message="Caso de éxito creado")

    def update(self, request, pk=None):
        obj = get_object_or_404(CasoExito, id=pk)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(data=serializer.data, message="Caso de éxito actualizado")

    def destroy(self, request, pk=None):
        obj = get_object_or_404(CasoExito, id=pk)
        obj.delete()
        return json_response(message="Caso de éxito eliminado")

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        authentication_classes=[],
        url_path="public",
    )
    def public(self, request):
        casos = CasoExito.objects.order_by("-created_at")[:3]
        serializer = CasoExitoSerializer(
            casos, many=True, context={"request": request}
        )
        return json_response(data=serializer.data)
