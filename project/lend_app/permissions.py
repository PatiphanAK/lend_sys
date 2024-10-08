from rest_framework.permissions import BasePermission

class IsApprover(BasePermission):
    def has_permission(self, request, view):
        # ตรวจสอบว่าผู้ใช้เป็น Approver
        return hasattr(request.user, 'approver')

class IsApproverInOrganization(BasePermission):
    def has_object_permission(self, request, view, obj):
        # ตรวจสอบว่าผู้ใช้เป็น Approver และอยู่ในองค์กรเดียวกัน
        return hasattr(request.user, 'approver') and obj.organization == request.user.organization

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # ตรวจสอบว่า user ที่ทำ request เป็นเจ้าของของ borrow request นั้นๆ
        return obj.borrower.user == request.user