
from django.db.models import Q
import json

class FilterBuilder():
    def __init__(self,queryset,model,filters=None) -> None:
        self.queryset = queryset
        self.model=model
        self.filters = filters

    def field_is_permitted(self,field):
        return field in getattr(self.model, 'FILTER_SORT_ORDER_FIELDS', [])

    def build_filter(self,current_item,is_and=True):
        if(isinstance(current_item,list) and len(current_item)==3 and isinstance(current_item[0],str)):
            field,operator,value=current_item
            return self.build_condition(field,operator,value)
        operations=Q()
        for item in current_item:
            if item=="and":
                is_and=True
                continue
            if item=="or":
                is_and=False
                continue
            dynamic_filters=self.build_filter(item,is_and)
            if is_and:
                operations &=dynamic_filters
            else:
                operations |=dynamic_filters
        return (operations)
    
    def build_condition(self,field,operator,value):
        operation=Q()
        if not self.field_is_permitted(field):
            return operation
        if operator == "=":
            operation = Q(**{f"{field}": value})
        elif operator == "contains":
            operation = Q(**{f"{field}__icontains": value})
        elif operator == "notcontains":
            operation = ~Q(**{f"{field}__icontains": value})
        elif operator == "in":
            operation = Q(**{f"{field}__in": value})
        elif operator == ">":
            operation = Q(**{f"{field}__gt": value})
        elif operator == "<":
            operation = Q(**{f"{field}__lt": value})
        elif operator == ">=":
            operation = Q(**{f"{field}__gte": value})
        elif operator == "<=":
            operation = Q(**{f"{field}__lte": value})
        return operation          
                
    
    def apply_filters(self):
        if(self.filters):
            dynamic_filters=self.build_filter(current_item=json.loads(self.filters))
            self.queryset=self.queryset.filter(dynamic_filters)
        return

    def apply_all(self):
        self.apply_filters()
        return self.queryset