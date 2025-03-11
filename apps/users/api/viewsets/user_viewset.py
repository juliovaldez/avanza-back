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
from apps.users.signals import send_activate_account_signal
from django.shortcuts import get_object_or_404
from apps.inventory.api.serializers.location_serializer import LocationSerializer
from apps.inventory.api.serializers.inventory_profile_serializer import InventoryProfileSerializer
from apps.inventory.api.serializers.transaction_serializer import TxnMaterialSummarySerializer
from apps.inventory.models import Location,Transaction
from django.db.models import Sum


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.select_related('inventory_profile').all()
    ordering_fields = User.FILTER_SORT_ORDER_FIELDS
    serializer_class =UserSerializer

    def create(self, request: Request) -> Response:
        user_serializar = self.get_serializer(data=request.data)
        user_serializar.is_valid(raise_exception=True)
        user_serializar.save()
        # send_activate_account_signal.send(
            # sender=self.__class__, user_id=user_instance.id
        # )
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
        json_response(data=None,message="Recurso Eliminado")

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        user_serializer = self.get_serializer(user)
        return json_response(data=user_serializer.data)

    @action(detail=False, methods=["GET"])
    def authenticated(self, request: Request):
        user_instance: User = request.user
        user_serializer =UserProfileSerializer(user_instance)
        return json_response(data=user_serializer.data)
    
    @action(detail=True, methods=["GET"],url_path='locations')
    def locations(self,request,pk=None):
        user = get_object_or_404(User, id=pk)
        location_serializer=LocationSerializer(user.locations.all(), many=True)
        return json_response(data=location_serializer.data)
    
    @action(detail=True, methods=["POST","GET","PUT"],url_path='inventory-profile')
    def inventory_profile(self,request,pk=None):
        if request.method == "GET":
            user = get_object_or_404(User, id=pk)
            inventory_profile = getattr(user, "inventory_profile", None)
            if not inventory_profile:
                return json_response(data={})
                raise NotFound(detail="Inventory profile does not exist for this user.")
            serializer=InventoryProfileSerializer(user.inventory_profile)
            return json_response(data=serializer.data)
        elif request.method=="POST":
            data=request.data
            data['user'] = pk
            serializer=InventoryProfileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return json_response(data=serializer.data)
        elif request.method=="PUT":
            user = get_object_or_404(User, id=pk)
            inventory_profile = getattr(user, "inventory_profile", None)
            if not inventory_profile:
                raise NotFound(detail="Inventory profile does not exist for this user.")
            serializer=InventoryProfileSerializer(user.inventory_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return json_response(data=serializer.data)
    
    @action(detail=True,methods=['GET'],url_path='materials-by-location')
    def materials_by_location(self,request,pk=None):
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