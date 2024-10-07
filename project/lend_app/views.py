from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BorrowRequest, Borrower
from .serializers import BorrowRequestSerializer, BorrowerSerializer, BorrowerListSerializer
from rest_framework.permissions import AllowAny
# Create your views here.

# Borrower
# CRUD with Borrower


class BorrowerListView(APIView):
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
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
