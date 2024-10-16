from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from lend_app.models import Borrower, Approver
from lend_app.serializers import BorrowerListSerializer, BorrowerSerializer, ApproverSerializer, ApproverListSerializer

# Borrower Create List View
class BorrowerListCreateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        borrowers = Borrower.objects.all()
        serializer = BorrowerListSerializer(borrowers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BorrowerSerializer(data=request.data)
        if serializer.is_valid():
            borrower = serializer.save()
            return Response({
                'message': 'Borrower created successfully',
                'borrower': BorrowerListSerializer(borrower).data
            })
        return Response(serializer.errors)



# Approver Registration List View
class ApproverListCreateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        approvers = Approver.objects.all()
        serializer = ApproverListSerializer(approvers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ApproverSerializer(data=request.data)
        if serializer.is_valid():
            approver = serializer.save()
            return Response({
                'message': 'Approver created successfully',
                'approver': ApproverListSerializer(approver).data
            })
        return Response(serializer.errors)

#UserDeatialView
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # บังคับให้ต้องล็อกอิน

    def get(self, request):
        user = request.user  # ดึงข้อมูลผู้ใช้ที่ทำการล็อกอิน
        return Response({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
    
class BorrowerIDView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        borrower = Borrower.objects.get(user_id=request.user.id)
        return Response({
            'id': borrower.id,
        })

class ApproverIDView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        approver = Approver.objects.get(user_id=request.user.id)
        return Response({
            'id': approver.id,
        })