from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    BorrowerListView, BorrowerRegisterView, ApproverListView, ApproverRegisterView, 
    ListItemView, ItemDetailView, CreateItemView, SearchItemListView,
    BorrowRequestListView, BorrowRequestDetailView, HistoryBorrowRequestListView, 
    HistoryApproveRequestListView, ApproveBorrowRequestView, RejectBorrowRequestView, 
    ReturnBorrowRequestView, HistoryBorrowRequestListofOrganizationView
)
urlpatterns = [
    path('borrowers/', BorrowerListView.as_view(), name='borrower-list'),
    path('approvers/', ApproverListView.as_view(), name='approver-list'),
    path('borrowers/register/', BorrowerRegisterView.as_view(), name='borrower-register'),
    path('approvers/register/', ApproverRegisterView.as_view(), name='borrower-register'),
    path('items/', ListItemView.as_view(), name='item-list'),
    path('items/create/', CreateItemView.as_view(), name='item-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('equipment-stocks/search/', SearchItemListView.as_view(), name='equipment-stock-search'),


        # URLs สำหรับการยืมและคืน
    path('borrow-requests/', BorrowRequestListView.as_view(), name='borrow-request-list'),
    path('borrow-requests/<int:pk>/', BorrowRequestDetailView.as_view(), name='borrow-request-detail'),
    path('borrow-requests/history/', HistoryBorrowRequestListView.as_view(), name='borrow-request-history'),
    path('approve-requests/history/', HistoryApproveRequestListView.as_view(), name='approve-request-history'),
    path('borrow-requests/<int:pk>/approve/', ApproveBorrowRequestView.as_view(), name='borrow-request-approve'),
    path('borrow-requests/<int:pk>/reject/', RejectBorrowRequestView.as_view(), name='borrow-request-reject'),
    path('borrow-requests/<int:pk>/return/', ReturnBorrowRequestView.as_view(), name='borrow-request-return'),
    path('organization/borrow-requests/history/', HistoryBorrowRequestListofOrganizationView.as_view(), name='organization-borrow-request-history'),

        # URLs สำหรับ JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]