from django.db import models

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.common.permissions import DjangoModelPermissions
from api.common.filter_builder import FilterBuilder
from api.common.groupby_builder import GroupByBuilder
from api.common.serializers import GroupBySerializer
from api.common.base_mixin import BaseMixin
from rest_framework import serializers
from rest_framework.filters import OrderingFilter

import uuid
import inspect
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted_at = models.DateField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()
        return self.hard_delete()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        abstract = True


class NotDeletedQuerySet(models.QuerySet):
    def default(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)          




class BaseManager(models.Manager):
    def get_queryset(self):
        return NotDeletedQuerySet(self.model, using=self._db).default()
    
    

class BaseModel(TimeStampedModel,SoftDeleteModel):
    comments=models.TextField(blank=True, null=True)

    objects= BaseManager()
    
    class Meta:
        abstract=True
        ordering=['-id']



class BaseModelViewSet(BaseMixin):
    permission_classes=[IsAuthenticated,DjangoModelPermissions]
    filter_backends=[OrderingFilter]
    
    def get_queryset(self):
        filters = self.request.query_params.get("filter", None)
        group = self.request.query_params.get("group", None)
        groupSummary = self.request.query_params.get("groupSummary", None)
        query_set = FilterBuilder(self.queryset, model=self.queryset.model, filters=filters).apply_all()
        query_set, self.total_count = GroupByBuilder(query_set, model=self.queryset.model,group=group,groupSummary=groupSummary).apply_all()
        if not group and hasattr(self,'add_aggregations'):
            query_set=self.add_aggregations(query_set)
        return query_set

    def get_serializer_class(self):
        if self.request.query_params.get('group', None) and  self.total_count:
            return GroupBySerializer
        return self.serializer_class
    
class BaseModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        read_only_fields = ('id','created_at','updated_at','deleted_at')