
import json
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel, OneToOneRel


class Expand():
    def __init__(self,queryset,model,expand=None)->None:
        self.queryset=queryset
        self.model=model
        self.expand=expand if isinstance(expand,list) else json.loads(expand)
        pass
    
    
    def classify_expand_field(self, field_path):
        root_field = field_path.split('.')[0].split('__')[0]
        try:
            field = self.model._meta.get_field(root_field)
            if isinstance(field, (ForeignKey, OneToOneField)):
                return 'select'
            elif isinstance(field, ManyToManyField):
                return 'prefetch'
            elif isinstance(field, (ManyToOneRel, OneToOneRel, ManyToManyRel)):
                return 'prefetch'
            return None
        except Exception:
            for rel in self.model._meta.related_objects:
                if rel.get_accessor_name() == root_field:
                    if isinstance(rel, (ManyToOneRel, ManyToManyRel, OneToOneRel)):
                        return 'prefetch'
        return None


    def add_expand_fields(self,related_fields):
        select = []
        prefetch = []
        for field in related_fields:
            root = field.split('__')[0]
            strategy = self.classify_expand_field(field_path=root)
            if strategy == 'select':
                select.append(field)
            elif strategy == 'prefetch':
                prefetch.append(field)

        if select:
            self.queryset = self.queryset.select_related(*select)
        if prefetch:
            self.queryset = self.queryset.prefetch_related(*prefetch)


    def apply_expand_fields(self):
        if(self.expand):
            self.add_expand_fields(related_fields=self.expand)
        return
    
    def apply_all(self):
        self.apply_expand_fields()
        return self.queryset