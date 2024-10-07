from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BorrowRequest, Borrower
from .serializers import BorrowRequestSerializer, BorrowerSerializer

# Create your views here.

# Borrower


class BorrowerView(APIView):
    def get(self, request):
        borrowers = Borrower.objects.all()
        serializer = BorrowerSerializer(borrowers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BorrowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            borrower = Borrower.objects.get(pk=pk)
        except Borrower.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BorrowerSerializer(borrower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            borrower = Borrower.objects.get(pk=pk)
        except Borrower.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        borrower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
