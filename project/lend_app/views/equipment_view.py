from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from lend_app.models import Item, EquipmentStock
from lend_app.serializers.other_serializers import ItemSerializer, EquipmentStockSerializer, AssignItemToStockSerializer, OrganizationStockSerializer
from lend_app.permissions import IsApprover, IsApproverInOrganization

# List Item View
class ListItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]  # ให้ทุกคนเข้าถึงได้

# Item Detail View
class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]  # ให้ทุกคนเข้าถึงได้

# Create Item View
class CreateItemView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]  # ต้องการการยืนยันตัวตนและเป็น Approver ในองค์กร

# Search Equipment Stock List View
class SearchEquipmentStockListView(generics.ListAPIView):
    serializer_class = EquipmentStockSerializer
    permission_classes = [AllowAny]  # ให้ทุกคนเข้าถึงได้

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        organization = self.request.query_params.get('organization', None)
        
        if query and organization:
            return EquipmentStock.objects.filter(
                Q(item__name__icontains=query) & Q(organization__name__icontains=organization)
            )
        elif query:
            return EquipmentStock.objects.filter(item__name__icontains=query)
        elif organization:
            return EquipmentStock.objects.filter(organization__name__icontains=organization)
        return EquipmentStock.objects.all()

# List Equipment Stock View
class ListEquipmentStockView(generics.ListAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [AllowAny]  # ให้ทุกคนเข้าถึงได้

# Equipment Stock Detail View
class EquipmentStockDetailView(generics.RetrieveAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [AllowAny]  # ให้ทุกคนเข้าถึงได้

# Create Equipment Stock View
class CreateEquipmentStockView(generics.CreateAPIView):
    queryset = EquipmentStock.objects.all()
    serializer_class = EquipmentStockSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]  # ต้องการการยืนยันตัวตนและเป็น Approver ในองค์กร

# Assign Item to Stock View
class AssignItemToStockView(APIView):
    permission_classes = [IsAuthenticated, IsApproverInOrganization]  # ต้องการการยืนยันตัวตนและเป็น Approver ในองค์กร

    def post(self, request, *args, **kwargs):
        serializer = AssignItemToStockSerializer(data=request.data)
        if serializer.is_valid():
            equipment_stock = serializer.save()
            return Response({
                'message': 'Item assigned to stock successfully',
                'equipment_stock': EquipmentStockSerializer(equipment_stock).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckOrganizationStockView(generics.ListAPIView):
    serializer_class = OrganizationStockSerializer
    permission_classes = [IsAuthenticated]  # ต้องการการยืนยันตัวตน

    def get_queryset(self):
        approver = self.request.user.approver
        organization_id = approver.organization.id
        return EquipmentStock.objects.filter(organization_id=organization_id)