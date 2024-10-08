from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from lend_app.models import BorrowRequest, Approver, Borrower
from lend_app.serializers.other_serializers import BorrowRequestSerializer
from lend_app.permissions import IsApproverInOrganization, IsOwner


# แสดงรายการคำขอยืมทั้งหมดและสร้างคำขอยืมใหม่
class BorrowRequestListView(generics.ListCreateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return BorrowRequest.objects.filter(borrower__user=user)

    def perform_create(self, serializer):
        request = self.request
        borrower = Borrower.objects.get(user=request.user)
        serializer.save(borrower=borrower)


# แสดงรายละเอียดคำขอยืม, อัพเดท, และลบคำขอยืม
class BorrowRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsOwner]


# แสดงประวัติการยืมของผู้ยืม
class HistoryBorrowRequestForBorrower(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return BorrowRequest.objects.filter(borrower__user=user, status__in=['REJECTED', 'RETURNED'])


# แสดงประวัติการยืมของผู้อนุมัติ
class HistoryBorrowRequestForApprover(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'approver'):
            return BorrowRequest.objects.filter(approver__user=user)
        return BorrowRequest.objects.none()


# แสดงรายการที่รอการอนุมัติในองค์กรเดียวกัน
class WaitingForApproveListViewForOrganization(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'approver'):
            organization = user.approver.organization
            return BorrowRequest.objects.filter(
                status='PENDING',
                item__equipmentstock__organization=organization
            )
        else:
            raise serializers.ValidationError("User does not have an associated approver.")


# แสดงรายการที่รอการอนุมัติสำหรับคนยืม
class WaitingForApproveListViewForBorrower(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'borrower'):
            return BorrowRequest.objects.filter(status='PENDING', borrower=user.borrower)
        else:
            raise serializers.ValidationError("User does not have an associated borrower.")


# อนุมัติคำขอยืม
class ApproveBorrowRequestView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'PENDING':
            return Response({'error': 'Cannot approve a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.approver = request.user
        instance.status = 'APPROVED'
        instance.save()
        return super().update(request, *args, **kwargs)


# ปฏิเสธคำขอยืม
class RejectBorrowRequestView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'PENDING':
            return Response({'error': 'Cannot reject a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = 'REJECTED'
        instance.save()
        return super().update(request, *args, **kwargs)


# คืนคำขอยืม
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
        return super().update(request, *args, **kwargs)


# แสดงรายการที่รอการอนุมัติ
class WaitingForApproveRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return BorrowRequest.objects.filter(status='PENDING')


# แสดงรายการที่รอการคืน
class WaitingForReturnRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return BorrowRequest.objects.filter(status='APPROVED')


# แสดงรายการที่คืนแล้ว
class ReturnedRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return BorrowRequest.objects.filter(status='RETURNED')


# แสดงรายการที่ถูกปฏิเสธ
class RejectedRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return BorrowRequest.objects.filter(status='REJECTED')
