from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from api.utils.utils import json_response
from apps.contacto.models import ContactoConfig
from apps.contacto.api.serializers import ContactoConfigSerializer
from api.common.base_models import BaseModelViewSet


class ContactoConfigViewSet(BaseModelViewSet):
    queryset = ContactoConfig.objects.all()
    serializer_class = ContactoConfigSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(data=serializer.data, message="Contacto creado")

    def update(self, request, pk=None):
        obj = ContactoConfig.objects.filter(id=pk).first()
        if not obj:
            return json_response(message="No encontrado", status=404)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(data=serializer.data, message="Contacto actualizado")

    def destroy(self, request, pk=None):
        obj = ContactoConfig.objects.filter(id=pk).first()
        if obj:
            obj.delete()
        return json_response(message="Contacto eliminado")

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        authentication_classes=[],
        url_path="public",
    )
    def public(self, request):
        obj = ContactoConfig.objects.order_by("-created_at").first()
        if not obj:
            return json_response(data=None)
        serializer = ContactoConfigSerializer(obj, context={"request": request})
        return json_response(data=serializer.data)
