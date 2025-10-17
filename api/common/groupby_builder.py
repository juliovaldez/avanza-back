from django.db.models import Count,F,Value,CharField,Sum,IntegerField
import json
from api.common.pagination import Pagination
from django.db.models.functions import Coalesce
from django.db.models import Func, F, CharField
from django.db.models.expressions import RawSQL
from django.db.models import Aggregate, CharField


class Concat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra
        )
        
        
class GroupByBuilder:
    def __init__(self, queryset, model, group=None,groupSummary=None):
        self.queryset = queryset
        self.model = model
        self.group = json.loads(group if group else '[]')
        self.groupSummary = json.loads(groupSummary if groupSummary else '[]')

        
    def field_is_permitted(self,field):
        return field in getattr(self.model, 'FILTER_SORT_ORDER_FIELDS', []) 
       
    def apply_all(self):
        if not len(self.group):
            return self.queryset,None

        group_fields = []
        orderings = []
        main_selector=None
        for index,g in enumerate(self.group):
            selector = g.get("selector", None)
            desc = g.get("desc", False)

            if not selector or not self.field_is_permitted(selector):
                raise Exception(f'No se permite agrupar por el campo {selector}')
            if index==0:
                main_selector=selector
            
            group_fields.append(selector)
            orderings.append(f"-{selector}" if desc else selector)
            
        total_count = self.queryset.count()
        annotations={
            "count":Count('id'),
            "items":Value(None,output_field=CharField()), #No tiene valor aun, pensado para futuro
        }
        for summary in self.groupSummary:
            sumary_selector = summary["selector"]
            summary_type = summary["summaryType"]
            if summary_type=='sum':
                annotations[f"{sumary_selector}_{summary_type}"] = Coalesce(Sum(sumary_selector), 0, output_field=IntegerField())
            if summary_type == "concat":
                annotations[f"{sumary_selector}_concat"] = Concat(f"{sumary_selector}")
        query_set=  self.queryset.values(key=F(main_selector),*group_fields).annotate(**annotations).order_by(*orderings)
        
        return query_set,total_count    