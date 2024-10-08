import django_filters
from .models import EquipmentStock, Item

class EquipmentStockFilter(django_filters.FilterSet):
    item_name = django_filters.CharFilter(field_name='item__name', lookup_expr='icontains', required=False)
    organization_name = django_filters.CharFilter(field_name='organization__name', lookup_expr='icontains', required=False)
    category_name = django_filters.CharFilter(field_name='item__category__name', lookup_expr='icontains', required=False)
    quantity = django_filters.NumberFilter(field_name='quantity', required=False)

    class Meta:
        model = EquipmentStock
        fields = ['item_name', 'organization_name', 'category_name', 'quantity']