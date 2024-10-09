from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lend_app.models import BorrowRequest, Borrower
from lend_app.serializers import BorrowRequestSerializer, BorrowQueueSerializer
from lend_app.permissions import IsApproverInOrganization, IsOwner
from rest_framework import serializers
from django.utils import timezone


def get_queryset_for_organization(user):
    if hasattr(user, 'approver'):
        organization = user.approver.organization
        # print(f"Organization ID: {organization.id}")  # เพิ่มการพิมพ์เพื่อตรวจสอบ
        queryset = BorrowRequest.objects.filter(equipment_stock__organization=organization)
        # print(f"Queryset: {queryset}")  # เพิ่มการพิมพ์เพื่อตรวจสอบ
        return queryset
    return BorrowRequest.objects.none()

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

# แสดงรายการที่รอการอนุมัติในองค์กรเดียวกัน
class WaitingForApproveListViewForOrganization(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user).filter(status='PENDING')


# แสดงรายการที่รอการอนุมัติสำหรับคนยืม
class WaitingForApproveListViewForBorrower(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'borrower'):
            return BorrowRequest.objects.filter(status='PENDING', borrower=user.borrower)
        else:
            raise serializers.ValidationError(
                "User does not have an associated borrower.")


# อนุมัติคำขอยืม
class ApproveBorrowRequestView(generics.UpdateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # ตรวจสอบว่าสถานะของคำขอยืมคือ PENDING หรือไม่
        if instance.status != 'PENDING':
            return Response({'error': 'Cannot approve a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

        # ตรวจสอบว่าอุปกรณ์มีอยู่เพียงพอในการยืมตามคำขอหรือไม่
        if instance.equipment_stock.available < instance.quantity:
            return Response({'error': 'Not enough items available.'}, status=status.HTTP_400_BAD_REQUEST)

        # อัปเดตสถานะของคำขอยืมเป็น APPROVED
        instance.status = 'APPROVED'

        # อัปเดต approver_id ด้วย ID ของผู้ใช้ที่ทำการอนุมัติ
        # หรือใช้ request.data.get('approver_id') ถ้าต้องการให้ส่งจาก request
        instance.approver = request.user.approver

        # ลดจำนวนของใน EquipmentStock
        instance.equipment_stock.available -= instance.quantity

        # บันทึกการเปลี่ยนแปลงใน EquipmentStock และ BorrowRequest
        instance.equipment_stock.save()
        instance.save()

        return Response({'success': 'Borrow request approved successfully.'}, status=status.HTTP_200_OK)


# ปฏิเสธคำขอยืม
class RejectBorrowRequestView(generics.UpdateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except BorrowRequest.DoesNotExist:
            return Response({'error': 'BorrowRequest not found.'}, status=status.HTTP_404_NOT_FOUND)

        if instance.status != 'PENDING':
            return Response({'error': 'Cannot reject a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = 'REJECTED'
        instance.save()
        return Response({'success': 'Borrow request rejected successfully.'}, status=status.HTTP_200_OK)

# ยืนยันการคืนอุปกรณ์


class ConfirmReturnView(generics.UpdateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # ตรวจสอบว่าสถานะของคำขอยืมคือ APPROVED หรือไม่
        if instance.status != 'APPROVED':
            return Response({'error': 'Cannot confirm return for a request that is not approved.'}, status=status.HTTP_400_BAD_REQUEST)

        # อัปเดตสถานะของคำขอยืมเป็น RETURNED
        instance.status = 'RETURNED'

        # เพิ่มจำนวนของใน EquipmentStock
        instance.equipment_stock.available += instance.quantity

        # บันทึกวันที่คืน
        instance.return_date = timezone.now()  # บันทึกวันที่คืนเป็นวันที่ปัจจุบัน

        # บันทึกการเปลี่ยนแปลงใน EquipmentStock และ BorrowRequest
        instance.equipment_stock.save()
        instance.save()

        return Response({'success': 'Return confirmed successfully.'}, status=status.HTTP_200_OK)


# แสดงรายการที่รอการอนุมัติ
class WaitingForApproveRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user).filter(status='PENDING')


# แสดงรายการที่รอการคืน
class WaitingForReturnRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user).filter(status='APPROVED')


# แสดงรายการที่คืนแล้ว
class ReturnedRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user).filter(status='RETURNED')


# แสดงรายการที่ถูกปฏิเสธ
class RejectedRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user).filter(status='REJECTED')

class BorrowQueueCreateView(generics.CreateAPIView):
    serializer_class = BorrowQueueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user.borrower)