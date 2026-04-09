from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from api.common.base_models import BaseModelViewSet
from apps.users.api.serializers.user_serializer import (
    UserSerializer,
    ProfileSerializer,
)
from apps.users.models import User
from api.utils.utils import json_response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from apps.users.tasks import send_reset_email,send_activate_account

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    ordering_fields = User.FILTER_SORT_FIELDS
    serializer_class =UserSerializer

    def create(self, request: Request) -> Response:
        user_serializar = self.get_serializer(data=request.data)
        user_serializar.is_valid(raise_exception=True)
        user_serializar.save()
        return json_response(data=user_serializar.data,message="Recurso Creado")

    def update(self, request: Request, pk=None):
        user = get_object_or_404(User, id=pk)
        user_serializer = self.get_serializer(user, data=request.data, partial=False)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return json_response(data=user_serializer.data,message="Recurso Actualizado",)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        user.delete()
        return json_response(message="Recurso Eliminado")

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        user_serializer = self.get_serializer(user)
        return json_response(data=user_serializer.data)

    @action(detail=False, methods=["GET"])
    def authenticated(self, request: Request):
        user_instance: User = request.user
        user_serializer =ProfileSerializer(user_instance)
        return json_response(data=user_serializer.data)