from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from api.common.base_models import BaseModelViewSet
from api.utils.utils import json_response
from apps.testimonials.models import Testimonio
from apps.testimonials.api.serializers import TestimonioSerializer


class TestimonioViewSet(BaseModelViewSet):
    queryset = Testimonio.objects.all()
    ordering_fields = Testimonio.FILTER_SORT_FIELDS
    serializer_class = TestimonioSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(data=serializer.data, message="Testimonio creado")

    def update(self, request, pk=None):
        obj = get_object_or_404(Testimonio, id=pk)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(data=serializer.data, message="Testimonio actualizado")

    def destroy(self, request, pk=None):
        obj = get_object_or_404(Testimonio, id=pk)
        obj.delete()
        return json_response(message="Testimonio eliminado")

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        authentication_classes=[],
        url_path="public",
    )
    def public(self, request):
        testimonios = Testimonio.objects.order_by("-created_at")[:3]
        serializer = TestimonioSerializer(
            testimonios, many=True, context={"request": request}
        )
        return json_response(data=serializer.data)
