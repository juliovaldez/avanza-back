from django.db import models
from api.common.base_models import (
    BaseModel
)
from apps.users.models import User
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction as db_transaction


class Unit(BaseModel):
    name= models.CharField(max_length=255,unique=True)
    symbol= models.CharField(max_length=255,unique=True)
    value= models.FloatField(default=1.0)
    FILTER_SORT_ORDER_FIELDS=["id","name","symbol","value","comments"]
    

class Status(BaseModel):
    status_name=models.CharField(max_length=255)
    module_name=models.CharField(max_length=255)
    FILTER_SORT_ORDER_FIELDS=["id","status_name","module_name","comments"]

class Location(BaseModel):
    name=models.CharField(max_length=255,unique=True)
    code=models.CharField(max_length=255,unique=True)
    users = models.ManyToManyField(User, related_name='locations')
    FILTER_SORT_ORDER_FIELDS=["id","name","users","comments","code"]


class inventoryProfile(BaseModel):
    user=models.OneToOneField(User,related_name='inventory_profile',on_delete=models.CASCADE)
    location=models.ForeignKey(Location,related_name='inventory_prfile_by_location',on_delete=models.CASCADE)
    FILTER_SORT_ORDER_FIELDS=["id","user","location","comments"]


class Material(BaseModel):
    code=models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    unit_base=models.ForeignKey(Unit, related_name="materials_by_unit_base", on_delete=models.CASCADE)
    unit_weight=models.FloatField()
    description=models.CharField(max_length=255,null=True)
    FILTER_SORT_ORDER_FIELDS=["id","code","name","unit_base","unit_weight","description","status","comments"]


class UnitConversion(BaseModel):
    material=models.ForeignKey(Material, related_name='conversions_by_material',on_delete=models.CASCADE)
    from_unit=models.ForeignKey(Unit,related_name='conversions_from',on_delete=models.CASCADE)
    to_unit= models.ForeignKey(Unit,related_name='conversions_to',on_delete=models.CASCADE)
    conversion_factor=models.FloatField(default=1.0)
    FILTER_SORT_ORDER_FIELDS=["id","material","from_unit","to_unit","conversion_factor","comments"]


class Kit(BaseModel):
    material=models.ForeignKey(Material, related_name='barcodes_by_material',on_delete=models.CASCADE)
    barcode=models.CharField(max_length=255,unique=True)
    qty_per_code=models.FloatField()
    unit=models.ForeignKey(Unit, related_name="barcodes_by_unit", on_delete=models.CASCADE)
    FILTER_SORT_ORDER_FIELDS=["id","material","barcode","qty_per_code","unit","status","comments"]


class TransactionType(BaseModel):
    name=models.CharField(max_length=255,unique=True)
    FILTER_SORT_ORDER_FIELDS=["id","name","comments"]
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"
    DEL="DEL"
    

class TxnDocument(BaseModel):
    transaction_type=models.ForeignKey(TransactionType,related_name='txn_documents_by_type',on_delete=models.CASCADE)
    folio_number=models.CharField(max_length=255,unique=True)
    reference_number=models.CharField(max_length=255,null=True)
    txn_start_date=models.DateTimeField()
    txn_end_date=models.DateTimeField()
    from_user=models.ForeignKey(User,related_name='txn_documents_from_user',on_delete=models.CASCADE)
    from_user_location=models.ForeignKey(Location,related_name='txn_documents_from_user_location',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='txn_documents_to_user',on_delete=models.CASCADE)
    to_user_location=models.ForeignKey(Location,related_name='txn_documents_to_user_location',on_delete=models.CASCADE)
    FILTER_SORT_ORDER_FIELDS=["id","transaction_type","transaction_type__name","folio_number","reference_number","txn_start_date","txn_end_date","from_user","from_user_location","to_user","to_user_location","comments"]

    def save(self,*args, **kwargs):
        if self.from_user.inventory_profile:
            self.from_user_location=self.from_user.inventory_profile.location
        else:
            raise serializers.ValidationError("El usuario origen no tiene un perfil de inventario asignado") 
        if self.to_user.inventory_profile:
            self.to_user_location=self.to_user.inventory_profile.location
        else:
            raise serializers.ValidationError("El usuario destino no tiene un perfil de inventario asignado")   
        if not self.folio_number:
            total_existentes=TxnDocument.objects.filter(transaction_type=self.transaction_type).count()
            self.folio_number=f'{self.from_user_location.code}-{self.transaction_type.id:02d}-{total_existentes+1:06d}'
        super().save(*args, **kwargs)

class Transaction(BaseModel):
    status=models.ForeignKey(Status,related_name='transactions_by_status',on_delete=models.CASCADE)
    txn_document=models.ForeignKey(TxnDocument,related_name='transactions_by_txn_document',on_delete=models.CASCADE)
    material=models.ForeignKey(Material,related_name='transactions_by_material',on_delete=models.CASCADE)
    serial_number=models.CharField(max_length=255,null=True)
    transaction_quantity=models.FloatField(default=0)
    transaction_unit=models.ForeignKey(Unit,related_name='transactions_by_unit',on_delete=models.CASCADE)
    conversion_factor=models.FloatField(default=1.0)
    base_quantity=models.FloatField(default=0)
    base_unit=models.ForeignKey(Unit, related_name="transactions_by_base_unit", on_delete=models.CASCADE)
    available_quantity=models.FloatField()
    FILTER_SORT_ORDER_FIELDS=["id","parent","status","txn_document","material","serial_number","transaction_quantity","transaction_unit","conversion_factor","base_quantity","base_unit","available_quantity","comments","txn_document__to_user","material__name"]
    

    def delete(self, using=None, keep_parents=False):
        from apps.inventory.api.helpers.transaction_helper import validate_delete_transaction
        with db_transaction.atomic():
            validate_delete_transaction(model=self)
            super().delete(using=using, keep_parents=keep_parents)
    
    def validate_and_save_transaction(self):
        from apps.inventory.api.helpers.transaction_helper import validate_save_transaction
        with db_transaction.atomic():
            self.save()
            validate_save_transaction(model=self)

    
class TransactionRegistry(BaseModel):
    src_transaction=models.ForeignKey(Transaction,related_name='registries_as_source',on_delete=models.CASCADE)
    transaction=models.ForeignKey(Transaction,related_name='registries_as_destination',on_delete=models.CASCADE)
    quantity=models.FloatField()
    FILTER_SORT_ORDER_FIELDS=["id","transaction","parent","quantity","comments"]