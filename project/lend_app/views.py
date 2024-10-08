from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BorrowRequest, Borrower, Approver, Item, EquipmentStock
from .serializers import BorrowRequestSerializer, BorrowerSerializer, BorrowerListSerializer, ApproverListSerializer, ApproverSerializer, ItemSerializer, EquipmentStockSerializer, EquipmentStockDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .filters import EquipmentStockFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# Create your views here.

# Borrower
# CRUD with Borrower


class BorrowerListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        borrowers = Borrower.objects.all()
        serializer = BorrowerListSerializer(borrowers, many=True)
        return Response(serializer.data)


class BorrowerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BorrowerSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Return the error details as they are
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApproverRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ApproverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproverListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        approvers = Approver.objects.all()
        serializer = ApproverListSerializer(approvers, many=True)
        return Response(serializer.data)


# ทำเรื่องยืม


class BorrowRequestList(APIView):
    def get(self, request):
        borrow_requests = BorrowRequest.objects.all()
        serializer = BorrowRequestSerializer(borrow_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
