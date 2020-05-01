from django_filters.filterset import BaseFilterSet,  FilterSetMetaclass, FilterSetOptions
from django_filters.utils import get_model_field
from .models import Contact
from collections import OrderedDict

class ContactFilterMeta(FilterSetMetaclass):
    def __new__(cls, name, bases, attrs):
        attrs['declared_filters'] = cls.get_declared_filters(bases, attrs)

        new_class = super().__new__(cls, name, bases, attrs)
        new_class._meta = FilterSetOptions(getattr(new_class, 'Meta', None))
        new_class.base_filters = new_class.get_filters()

        return new_class

class ContactFilter(BaseFilterSet, metaclass=ContactFilterMeta):
    def __init__(self, model, filters, *args, **kwargs):
        self.model = model
        self.filterszz = filters
        # self._meta = FilterSetOptions(options=FakeMeta)
        self.base_filters = self.get_dynamic_filters(OrderedDict(filters))
        super().__init__(*args, **kwargs)

    # def get_form_class(self):
    #     fields = OrderedDict([(f, lookups) for f, lookups in self.filters.items()])
    #     w.tf
    #     return type(
    #         str('%sForm' % self.__class__.__name__),
    #         (self._meta.form,), fields
    #     )

    def get_dynamic_filters(self, filters):
        # Determine the filters that should be included on the filterset.
        filters = OrderedDict(self.filterszz)
        fields = filters

        for field_name, lookups in fields.items():
            field = get_model_field(self.model, field_name)

            for lookup_expr in lookups:
                filter_name = BaseFilterSet.get_filter_name(field_name, lookup_expr)

                # # If the filter is explicitly declared on the class, skip generation
                # if filter_name in cls.declared_filters:
                #     filters[filter_name] = cls.declared_filters[filter_name]
                #     continue

                if field is not None:
                    filters[filter_name] = BaseFilterSet.filter_for_field(field, field_name, lookup_expr)
        # Add in declared filters. This is necessary since we don't enforce adding
        # declared filters to the 'Meta.fields' option
        # filters.update(cls.declared_filters)
        return filters