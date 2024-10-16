from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CategoriesView,BorrowerIDView, ApproverIDView,
    BorrowerListCreateView, ApproverListCreateView,UserDetailView,
    ItemsListCreateView, ItemDetailView, SearchEquipmentStockListView,
    BorrowRequestListView, BorrowRequestDetailView,
    HistoryBorrowRequestForBorrower, HistoryBorrowRequestForApprover,
    WaitingForApproveRequestListView, WaitingForReturnRequestListView,
    ReturnedRequestListView, RejectedRequestListView,
    ListEquipmentStockView, CreateEquipmentStockView, EquipmentStockDetailView,
    AssignItemToStockView, CheckOrganizationStockView, ApproveBorrowRequestView,
    RejectBorrowRequestView, ConfirmReturnView, BorrowQueueCreateView
)


urlpatterns = [
    # URLs สำหรับ Borrower และ Approver ดู User ได้ทั้งหมด, สร้าง User ได้ทั้งหมด
    path('borrowers/', BorrowerListCreateView.as_view(), name='borrower-list-create'),
    path('approvers/', ApproverListCreateView.as_view(), name='approver-list-create'),
    path('user/', UserDetailView.as_view(), name='user-detail'),


    # URLs สำหรับ User request เพื่อดู Borrower และ Approver ID ของตัวเอง และ Organization ID ของตัวเอง
     path('borrowers-id/', BorrowerIDView.as_view(), name='borrower-id'),
     path('approvers-id/', ApproverIDView.as_view(), name='approver-id'),

    # URLs สำหรับ Equipment Item
    path('items/', ItemsListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/search/', SearchEquipmentStockListView.as_view(),
         name='search-item-list'),
     
     #URL Category
     path('categories/', CategoriesView.as_view(), name='category-list'),
    # URL สำหรับการจัดการคำขอยืม
    path('borrow-requests/', BorrowRequestListView.as_view(),
         name='borrow-request-list'),
    path('borrow-requests/<int:pk>/', BorrowRequestDetailView.as_view(),
         name='borrow-request-detail'),

    # URLs สำหรับประวัติการยืม
    path('borrow-requests/history/borrower/', HistoryBorrowRequestForBorrower.as_view(),
         name='history-borrow-request-for-borrower'),
    path('borrow-requests/history/approver/', HistoryBorrowRequestForApprover.as_view(),
         name='history-borrow-request-for-approver'),

    # URLs สำหรับรายการที่รอการอนุมัติ
    path('borrow-requests/waiting-for-approve/',
         WaitingForApproveRequestListView.as_view(), name='waiting-for-approve-request-list'),

    # URLs สำหรับการอนุมัติคำขอยืม
    path('approve-borrow-request/<int:pk>/',
         ApproveBorrowRequestView.as_view(), name='approve-borrow-request'),
    path('reject-borrow-request/<int:pk>/',
         RejectBorrowRequestView.as_view(), name='reject-borrow-request'),
    path('confirm-return/<int:pk>/',
         ConfirmReturnView.as_view(), name='confirm-return'),

    # URLs สำหรับรายการที่รอการคืน
    path('borrow-requests/waiting-for-return/',
         WaitingForReturnRequestListView.as_view(), name='waiting-for-return-request-list'),

    # URLs สำหรับรายการที่คืนแล้ว
    path('borrow-requests/returned/', ReturnedRequestListView.as_view(),
         name='returned-request-list'),

    # URLs สำหรับรายการที่ถูกปฏิเสธ
    path('borrow-requests/rejected/', RejectedRequestListView.as_view(),
         name='rejected-request-list'),


    path('borrow-queue/', BorrowQueueCreateView.as_view(),
         name='borrow-queue-create'),
    # URLs สำหรับ Equipment Stock
    path('equipment-stocks/', ListEquipmentStockView.as_view(),
         name='equipment-stock-list'),
    path('equipment-stocks/create/', CreateEquipmentStockView.as_view(),
         name='equipment-stock-create'),
    path('equipment-stocks/<int:pk>/', EquipmentStockDetailView.as_view(),
         name='equipment-stock-detail'),
    path('organization-stocks/', CheckOrganizationStockView.as_view(),
         name='organization-stock-list'),

    # URL สำหรับ AssignItemToStockView
    path('equipment-stocks/assign/', AssignItemToStockView.as_view(),
         name='assign-item-to-stock'),

    # URLs สำหรับ JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
