from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    BorrowerListView, BorrowerRegisterView, ApproverListView, ApproverRegisterView,
    ListItemView, ItemDetailView, CreateItemView, SearchEquipmentStockListView,
    BorrowRequestListView, BorrowRequestDetailView, 
    HistoryBorrowRequestForBorrower, HistoryBorrowRequestForApprover,
    WaitingForApproveRequestListView, WaitingForReturnRequestListView,
    ReturnedRequestListView, RejectedRequestListView,
    ListEquipmentStockView, CreateEquipmentStockView, EquipmentStockDetailView,
    AssignItemToStockView
)


urlpatterns = [
    path('borrowers/', BorrowerListView.as_view(), name='borrower-list'),
    path('approvers/', ApproverListView.as_view(), name='approver-list'),
    path('borrowers/register/', BorrowerRegisterView.as_view(),
         name='borrower-register'),
    path('approvers/register/', ApproverRegisterView.as_view(),
         name='borrower-register'),
    path('items/', ListItemView.as_view(), name='item-list'),
    path('items/create/', CreateItemView.as_view(), name='item-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/search/', SearchEquipmentStockListView.as_view(),
         name='search-item-list'),

    # URL สำหรับการจัดการคำขอยืม
    path('borrow-requests/', BorrowRequestListView.as_view(), name='borrow-request-list'),
    path('borrow-requests/<int:pk>/', BorrowRequestDetailView.as_view(), name='borrow-request-detail'),

    # URLs สำหรับประวัติการยืม
    path('borrow-requests/history/borrower/', HistoryBorrowRequestForBorrower.as_view(), name='history-borrow-request-for-borrower'),
    path('borrow-requests/history/approver/', HistoryBorrowRequestForApprover.as_view(), name='history-borrow-request-for-approver'),

    # URLs สำหรับรายการที่รอการอนุมัติ
    path('borrow-requests/waiting-for-approve/', WaitingForApproveRequestListView.as_view(), name='waiting-for-approve-request-list'),

    # URLs สำหรับรายการที่รอการคืน
    path('borrow-requests/waiting-for-return/', WaitingForReturnRequestListView.as_view(), name='waiting-for-return-request-list'),

    # URLs สำหรับรายการที่คืนแล้ว
    path('borrow-requests/returned/', ReturnedRequestListView.as_view(), name='returned-request-list'),

    # URLs สำหรับรายการที่ถูกปฏิเสธ
    path('borrow-requests/rejected/', RejectedRequestListView.as_view(), name='rejected-request-list'),

    # URLs สำหรับ Equipment Stock
    path('equipment-stocks/', ListEquipmentStockView.as_view(),
         name='equipment-stock-list'),
    path('equipment-stocks/create/', CreateEquipmentStockView.as_view(),
         name='equipment-stock-create'),
    path('equipment-stocks/<int:pk>/', EquipmentStockDetailView.as_view(),
         name='equipment-stock-detail'),

    # URL สำหรับ AssignItemToStockView
    path('equipment-stocks/assign/', AssignItemToStockView.as_view(),
         name='assign-item-to-stock'),

    # URLs สำหรับ JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
