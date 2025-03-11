from django.db import transaction as db_transaction
from apps.inventory.models import Transaction, TransactionRegistry, TransactionType
from rest_framework import serializers

def validate_save_transaction(model:Transaction): 
    transaction_type_name=model.txn_document.transaction_type.name
    if transaction_type_name in [TransactionType.IN]:
        if model.serial_number:
            transactions = Transaction.objects.select_related('txn_document', 'material').filter(
                serial_number=model.serial_number,
                txn_document__transaction_type__name=TransactionType.IN
                ).exclude(id=model.id).order_by('id')
            if transactions.exists():
                raise serializers.ValidationError("El número de serie ya existe")
        pass
    elif transaction_type_name in [TransactionType.OUT, TransactionType.TRANSFER]:
        filter_conditions = {
        'txn_document__to_user': model.txn_document.from_user,
        'txn_document__to_user_location': model.txn_document.from_user_location,
        'available_quantity__gt': 0,
        'material': model.material,
        'base_unit': model.base_unit,
        }
        if model.serial_number:
            filter_conditions['serial_number'] = model.serial_number
        transactions = Transaction.objects.select_related('txn_document', 'material').filter(**filter_conditions).order_by('id')
        
        if not transactions.exists():
            raise serializers.ValidationError("No hay existencias disponibles para este material")
    
        temp_base_quantity=model.base_quantity
        for transaction in transactions:
            transaction_registry=TransactionRegistry(transaction=model,src_transaction=transaction,quantity=0)
            if temp_base_quantity==0:
                break
            if temp_base_quantity>=transaction.available_quantity:
                temp_base_quantity-=transaction.available_quantity
                transaction_registry.quantity=transaction.available_quantity
                transaction.available_quantity=0
            else:
                transaction.available_quantity-=temp_base_quantity
                transaction_registry.quantity=temp_base_quantity
                temp_base_quantity=0
            transaction_registry.save()
            transaction.save()
        if temp_base_quantity>0:
            raise serializers.ValidationError("No hay suficientes existencias disponibles para este material")
        pass
    else:
        raise serializers.ValidationError("operation not supported")
    
def validate_delete_transaction(model:Transaction):
    transaction_type_name=model.txn_document.transaction_type.name
    if transaction_type_name in [TransactionType.IN]:
        pass
    elif transaction_type_name in [TransactionType.OUT, TransactionType.TRANSFER]:
        delete_registries(model)
        pass
    else:
        raise serializers.ValidationError("operation not supported")

def delete_registries(model:Transaction):
    for transaction_registry in model.registries_as_destination.all():
        transaction_registry.src_transaction.available_quantity+=transaction_registry.quantity
        transaction_registry.src_transaction.save()
        transaction_registry.delete()
    pass