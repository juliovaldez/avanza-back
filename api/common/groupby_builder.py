from django.db.models import Count,F,Value,CharField,Sum,IntegerField
import json
from api.common.pagination import Pagination
from django.db.models.functions import Coalesce

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
        
        main_selector = None
        main_desc = None
        is_expanded = None
        selectors = []
        
        for index,group in enumerate(self.group):
            selector = group.get("selector", None)
            desc = group.get("desc", False)
            is_expanded = group.get("isExpanded", is_expanded)
            
            if not self.field_is_permitted(selector):
                raise Exception(f'No se permite agrupar por el campo {selector}')
            
            if index==0:
                main_selector = selector
                main_desc = desc
                is_expanded = is_expanded
            else:
                selectors.append(selector)

        
        if not main_selector or not self.field_is_permitted(main_selector):
            raise Exception(f'No se permite agrupar por el campo {main_selector}')
            return self.queryset,None
        
        total_count = self.queryset.count()
        annotations={
            "count":Count(main_selector),
            "items":Value(None,output_field=CharField()), #No tiene valor aun, pensado para futuro
        }
        for summary in self.groupSummary:
            sumary_selector = summary["selector"]
            summary_type = summary["summaryType"]
            if summary_type=='sum':
                annotations[f"{sumary_selector}_{summary_type}"] = Coalesce(Sum(sumary_selector), 0, output_field=IntegerField())
        
        query_set=  self.queryset.values(key=F(main_selector),*selectors).annotate(**annotations).order_by(f"-{main_selector}" if desc else main_selector)
        return query_set,total_count