from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from django.forms import DateInput
from .models import Category


class NewFilter(FilterSet):
    slug = ModelChoiceFilter(field_name= 'category__title',
                             queryset = Category.objects.all(),
                             label = 'Категория',
                             empty_label = 'Любой'
                             )

    title = CharFilter(lookup_expr='contains',)

    date = DateFilter(field_name='data', lookup_expr='gt', label='Дата', widget=DateInput(attrs={'type': 'date'},))