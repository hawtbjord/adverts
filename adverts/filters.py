import django_filters
from django_filters import NumberFilter, CharFilter
from django.db.models import Q

from .models import *


class AdvertFilter(django_filters.FilterSet):
    price_from = NumberFilter(field_name='price', lookup_expr='gte')
    price_to = NumberFilter(field_name='price', lookup_expr='lte')
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Advert
        fields = ['region', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['city'].queryset = City.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.filters['city'].queryset = City.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass

    def custom_filter(self, queryset, name, value):
        return Advert.objects.filter(
            Q(title__icontains=value) | Q(text__icontains=value)
        )
