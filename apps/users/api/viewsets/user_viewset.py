from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from api.common.base_models import BaseModelViewSet
from apps.users.api.serializers.user_serializer import (
    UserSerializer,
    UserProfileSerializer,
)
from apps.users.models import User
from api.utils.utils import json_response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from apps.users.tasks import send_reset_email,send_activate_account

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    ordering_fields = User.FILTER_SORT_ORDER_FIELDS
    serializer_class =UserSerializer

    def create(self, request: Request) -> Response:
        user_serializar = self.get_serializer(data=request.data)
        user_serializar.is_valid(raise_exception=True)
        user_serializar.save()
        #send_activate_account.delay(user_id=user_serializar.instance.id)
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
        user_serializer =UserProfileSerializer(user_instance)
        return json_response(data=user_serializer.data)
    
        to_user=get_object_or_404(User,id=pk)
        location_id=request.query_params.get('location',None)
        to_user_location= get_object_or_404(Location,id=location_id)if location_id else to_user.inventory_profile.location
        transactions = Transaction.objects.select_related('txn_document','material').filter(
            available_quantity__gt=0,
            txn_document__to_user=to_user,
            txn_document__to_user_location=to_user_location
        ).values('material', 'material__name','serial_number','base_unit').annotate(
        total_base_quantity=Sum("base_quantity"),
        total_available_quantity=Sum("available_quantity"),
        )
        transactions_serializer=TxnMaterialSummarySerializer(transactions,many=True)
        return json_response(data=transactions_serializer.data)