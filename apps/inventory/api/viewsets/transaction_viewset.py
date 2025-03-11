
from apps.inventory.models import Transaction
from apps.inventory.api.serializers.transaction_serializer import TransactionSerializer
from api.common.base_models import BaseModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework import serializers
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from api.utils.utils import json_response
from apps.inventory.api.helpers.transaction_helper import validate_save_transaction

class TransactionViewSet(BaseModelViewSet):
    queryset=Transaction.objects.select_related('material').all()
    serializer_class=TransactionSerializer
    ordering_fields = Transaction.FILTER_SORT_ORDER_FIELDS


    def create(self, request, *args, **kwargs):
        with db_transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            transaction_instance=Transaction(**serializer.validated_data)
            transaction_instance.validate_and_save_transaction()
            serializer = self.get_serializer(transaction_instance)
            return json_response(data=serializer.data,message="Recurso creado exitosamente")
    
    
    def update(self, request,pk=None):
        raise serializers.ValidationError("operation not supported")