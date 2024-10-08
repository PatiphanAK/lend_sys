from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from lend_app.models import Borrower, Approver
from lend_app.serializers import BorrowerListSerializer, BorrowerSerializer, ApproverSerializer, ApproverListSerializer

# Borrower List View
class BorrowerListView(generics.ListAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerListSerializer
    permission_classes = [AllowAny]


# Borrower Registration View
class BorrowerRegisterView(generics.CreateAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    permission_classes = [AllowAny]


# Approver Registration View
class ApproverRegisterView(generics.CreateAPIView):
    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer
    permission_classes = [AllowAny]


# Approver List View
class ApproverListView(generics.ListAPIView):
    queryset = Approver.objects.all()
    serializer_class = ApproverListSerializer
    permission_classes = [AllowAny]
