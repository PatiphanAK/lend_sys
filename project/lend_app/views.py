from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BorrowRequest, Borrower, Approver
from .serializers import BorrowRequestSerializer, BorrowerSerializer, BorrowerListSerializer, ApproverListSerializer, ApproverSerializer
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
    
class ApproverListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # ดึงกลุ่มที่ชื่อ 'Approver'
        approver_group = Group.objects.filter(name='Approver').first()

        # ตรวจสอบว่ากลุ่มมีอยู่หรือไหม
        if approver_group:
            # กรอง Approver ที่อยู่ในกลุ่ม 'Approver'
            borrowers = Approver.objects.filter(user__groups=approver_group)
        else:
            borrowers = Approver.objects.none()  # หากไม่มีกลุ่มให้คืนค่าเป็นว่าง

        serializer = ApproverListSerializer(borrowers, many=True)
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
