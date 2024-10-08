from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from lend_app.models import Item, EquipmentStock
from lend_app.serializers import ItemSerializer, EquipmentStockSerializer
from lend_app.permissions import IsApprover, IsApproverInOrganization

# List Item View
class ListItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

# Item Detail View
class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

# Create Item View
class CreateItemView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsApprover]

# Search Item List View
class SearchItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]  # ให้ทุกคนเข้าถึงได้

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return Item.objects.filter(name__icontains=query)
        return Item.objects.all()

# List Equipment Stock View
class ListEquipmentStockView(generics.ListAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [IsAuthenticated]

# Equipment Stock Detail View
class EquipmentStockDetailView(generics.RetrieveAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [IsAuthenticated]

# Create Equipment Stock View
class CreateEquipmentStockView(generics.CreateAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [IsAuthenticated, IsApprover]
