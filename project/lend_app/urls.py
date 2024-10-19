from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CategoriesView, BorrowerDetailView, ApproverDetailView,
    BorrowerListCreateView, ApproverListCreateView,UserProfileView,
    ItemsListCreateView, ItemDetailView, SearchEquipmentStockListView,
    BorrowRequestListView, BorrowRequestDetailView,
    HistoryBorrowRequestForBorrower, HistoryBorrowRequestForApprover,
    WaitingForApproveRequestListView, WaitingForReturnRequestListView,
    ReturnedRequestListView, RejectedRequestListView,
    ListEquipmentStockView, EquipmentStockDetailView,
    AssignItemToStockView, CheckOrganizationStockView, ApproveBorrowRequestView,
    RejectBorrowRequestView, ConfirmReturnView, BorrowQueueCreateView,OrganizationListForRegister,WaitingForApproveRequestListViewForBorrower,HistoryApproveForOrganization
)


urlpatterns = [
    # URLs สำหรับ Borrower และ Approver ดู User ได้ทั้งหมด, สร้าง User ได้ทั้งหมด
    path('borrowers/', BorrowerListCreateView.as_view(), name='borrower-list-create'),
    path('approvers/', ApproverListCreateView.as_view(), name='approver-list-create'),
    path('me/', UserProfileView.as_view(), name='user-detail'),
    
    #URLs สำหรับ Borrower และ Approver ดู User ของตัวเอง, แก้ไข User ของตัวเอง
    path('borrowers/<int:pk>/', BorrowerDetailView.as_view(), name='borrower-detail'),
    path('approvers/<int:pk>/', ApproverDetailView.as_view(), name='approver-detail'),

    # URLs สำหรับ Equipment Item
    path('items/', ItemsListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/search/', SearchEquipmentStockListView.as_view(),name='search-item-list'),
     
     #URL Category
     path('categories/', CategoriesView.as_view(), name='category-list'),

    # URL สำหรับการจัดการคำขอยืม
    path('borrow-requests/', BorrowRequestListView.as_view(),name='borrow-request-list'),
    path('borrow-requests/<int:pk>/', BorrowRequestDetailView.as_view(),name='borrow-request-detail'),

    # URLs สำหรับประวัติการยืม
    path('borrow-requests/history/borrower/', HistoryBorrowRequestForBorrower.as_view(),name='history-borrow-request-for-borrower'),
    path('approval-history/', HistoryBorrowRequestForApprover.as_view(), name='approval-history'),
    path('org-approve-history/', HistoryApproveForOrganization.as_view(), name='org-approve-history'),

    # URLs สำหรับรายการที่รอการอนุมัติ
    path('borrow-requests/waiting-for-approvel/',WaitingForApproveRequestListView.as_view(), name='waiting-for-approve-request-list'),
    path('pending-request/', WaitingForApproveRequestListViewForBorrower.as_view(), name='pending-request-list'),

    # URLs สำหรับการอนุมัติคำขอยืม
    path('approval/<int:pk>/',ApproveBorrowRequestView.as_view(), name='approve-borrow-request'),
    path('rejection/<int:pk>/',RejectBorrowRequestView.as_view(), name='reject-borrow-request'),
    path('confirm-return/<int:pk>/',ConfirmReturnView.as_view(), name='confirm-return'),

    # URLs สำหรับรายการที่รอการคืน
    path('borrow-requests/waiting-for-return/',WaitingForReturnRequestListView.as_view(), name='waiting-for-return-request-list'),

    # URLs สำหรับรายการที่คืนแล้ว
    path('borrow-requests/returned/', ReturnedRequestListView.as_view(),name='returned-request-list'),

    #URLs สำหรับดึง Organization ตอน Register
    path('registed-organizations/', OrganizationListForRegister.as_view(),name='organization-list-for-register'),
    # URLs สำหรับรายการที่ถูกปฏิเสธ
    path('borrow-requests/rejected/', RejectedRequestListView.as_view(),name='rejected-request-list'),


    path('borrow-queue/', BorrowQueueCreateView.as_view(),name='borrow-queue-create'),

    # URLs สำหรับ Equipment Stock
    path('equipment-stocks/', ListEquipmentStockView.as_view(),name='equipment-stock-list'),
    path('equipment-stocks/<int:pk>/', EquipmentStockDetailView.as_view(),name='equipment-stock-detail'),
    path('organization-stocks/', CheckOrganizationStockView.as_view(),name='organization-stock-list'),

    # URL สำหรับ AssignItemToStockView
    path('equipment-stocks/assign/', AssignItemToStockView.as_view(),name='assign-item-to-stock'),

    # URLs สำหรับ JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
