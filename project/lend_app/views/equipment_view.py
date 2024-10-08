from .models import Item, EquipmentStock
from .serializers import ItemSerializer, EquipmentStockSerializer, EquipmentStockDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
class ListItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class CreateItemView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class ItemListFilter(generics.ListAPIView):
    queryset = Item.objects.all()


class EquipmentStockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SearchItemListView(generics.ListAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockDetailSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = EquipmentStockFilter
    search_fields = ['item__name', 'organization__name']