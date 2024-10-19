from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lend_app.models import BorrowRequest, Borrower
from lend_app.serializers import BorrowRequestSerializer, BorrowQueueSerializer
from lend_app.permissions import IsApproverInOrganization, IsOwner
from rest_framework import serializers
from django.utils import timezone
from ..models import EquipmentStock


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
    permission_classes = [IsAuthenticated, IsApproverInOrganization]
    serializer_class = BorrowRequestSerializer

    def get_queryset(self):
        # ตรวจสอบว่า user ที่ทำการร้องขอเป็น approver
        approver = self.request.user.approver
        # ดึงประวัติการยืมที่สถานะเป็น 'RETURNED' และกรองเฉพาะผู้อนุมัติที่เป็น approver คนปัจจุบัน
        return BorrowRequest.objects.filter(
            approver=approver,
            status__in=[ 'RETURNED']
        ).order_by('-borrow_date')  # เรียงลำดับจากล่าสุดไปหาเก่าสุด

    

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
class ApproveBorrowRequestView(APIView):
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_object(self, pk):
        try:
            return BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            raise serializers.ValidationError("BorrowRequest not found.")
    
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = BorrowRequestSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            # ตรวจสอบสถานะของคำขอยืมว่าเป็น PENDING หรือไม่
            if instance.status != 'PENDING':
                return Response({'error': 'Cannot approve a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

            # ตรวจสอบว่าอุปกรณ์มีจำนวนเพียงพอต่อการอนุมัติคำขอหรือไม่
            equipment_stock = instance.equipment_stock
            if equipment_stock.available < instance.quantity:
                return Response({'error': 'Not enough items available.'}, status=status.HTTP_400_BAD_REQUEST)

            # อัปเดตสถานะเป็น APPROVED และลดจำนวนของใน EquipmentStock
            instance.status = 'APPROVED'
            instance.approver = request.user.approver  # ตั้งค่า Approver เป็นผู้ใช้ที่อนุมัติ
            
            # ลดจำนวน available ของ EquipmentStock ตามจำนวนที่ยืม
            equipment_stock.available -= instance.quantity
            equipment_stock.save()  # บันทึกการเปลี่ยนแปลง

            instance.save()  # บันทึกคำขอยืม
            return Response({'success': 'Borrow request approved successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ปฏิเสธคำขอยืม
class RejectBorrowRequestView(APIView):
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_object(self, pk):
        try:
            return BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            raise serializers.ValidationError("BorrowRequest not found.")
    
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializers = BorrowRequestSerializer(instance, data=request.data, partial=True)
        if serializers.is_valid():
            if instance.status != 'PENDING':
                return Response({'error': 'Cannot reject a request that is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
            serializers.save(status='REJECTED')
            return Response({'success': 'Borrow request rejected successfully.'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# ยืนยันการคืนอุปกรณ์

class ConfirmReturnView(APIView):
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_object(self, pk):
        try:
            return BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            raise serializers.ValidationError("BorrowRequest not found.")
    
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = BorrowRequestSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            # ตรวจสอบสถานะของคำขอยืมว่าเป็น APPROVED ก่อนถึงจะคืนได้
            if instance.status != 'APPROVED':
                return Response({'error': 'Cannot return a request that is not approved.'}, status=status.HTTP_400_BAD_REQUEST)

            # อัปเดตสถานะเป็น RETURNED
            instance.status = 'RETURNED'
            
            # เพิ่มจำนวน available ของ EquipmentStock ตามจำนวนที่คืน
            equipment_stock = instance.equipment_stock
            equipment_stock.available += instance.quantity
            equipment_stock.save()  # บันทึกการเปลี่ยนแปลงในคลัง

            instance.return_date = timezone.now()  # กำหนดวันที่คืนเป็นวันที่ปัจจุบัน
            instance.save()  # บันทึกคำขอยืมที่ถูกคืน

            return Response({'success': 'Borrow request returned successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# แสดงรายการที่รอการอนุมัติ
class WaitingForApproveRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        return get_queryset_for_organization(self.request.user).filter(status='PENDING')

class WaitingForApproveRequestListViewForBorrower(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'borrower'):
            return BorrowRequest.objects.filter(status='PENDING', borrower=user.borrower)
        else:
            raise serializers.ValidationError(
                "User does not have an associated borrower.")

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


class HistoryApproveForOrganization(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    
    permission_classes = [IsAuthenticated, IsApproverInOrganization]

    def get_queryset(self):
        user = self.request.user
        return BorrowRequest.objects.filter(equipment_stock__organization=user.approver.organization, status__in=["RETURNED"]).order_by('-borrow_date')