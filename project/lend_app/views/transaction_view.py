from lend_app.models import BorrowRequest
from lend_app.serializers import BorrowRequestSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class BorrowRequestListView(generics.ListCreateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

class BorrowRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

class HistoryBorrowRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRequest.objects.filter(borrower=self.request.user) # แสดงรายการที่ยืมโดยผู้ยืม

class HistoryApproveRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRequest.objects.filter(approver=self.request.user) # แสดงรายการที่อนุมัติโดยผู้อนุมัติ

class ApproveBorrowRequestView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'PENDING':
            return Response({'error': 'Cannot approve a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.approver = request.user
        instance.status = 'APPROVED'
        instance.save()
        return super().update(request, *args, **kwargs) # อัพเดทสถานะการอนุมัติ

class RejectBorrowRequestView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'PENDING':
            return Response({'error': 'Cannot reject a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = 'REJECTED'
        instance.save()
        return super().update(request, *args, **kwargs) # อัพเดทสถานะการปฏิเสธ

class ReturnBorrowRequestView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'APPROVED':
            return Response({'error': 'Cannot return a request that is not approved.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = 'RETURNED'
        instance.save()
        return super().update(request, *args, **kwargs) # อัพเดทสถานะการคืนของ

class HistoryBorrowRequestListofOrganizationView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRequest.objects.filter(item__organization=self.request.user.organization) # แสดงรายการที่อยู่ในองค์กรเดียวกัน

class HistoryBorrowRequestListofOrganizationView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRequest.objects.filter(item__organization=self.request.user.organization, status='RETURNED') # แสดงรายการที่อยู่ในองค์กรเดียวกันและสถานะเป็น RETURNED