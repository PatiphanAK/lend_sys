from django.urls import path
from .views import BorrowerListView, BorrowerRegisterView, ApproverListView, ApproverRegisterView, ListItemView, ItemDetailView, CreateItemView, SearchItemListView
urlpatterns = [
    path('borrowers/', BorrowerListView.as_view(), name='borrower-list'),
    path('approvers/', ApproverListView.as_view(), name='approver-list'),
    path('borrowers/register/', BorrowerRegisterView.as_view(), name='borrower-register'),
    path('approvers/register/', ApproverRegisterView.as_view(), name='borrower-register'),
    path('items/', ListItemView.as_view(), name='item-list'),
    path('items/create/', CreateItemView.as_view(), name='item-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('equipment-stocks/search/', SearchItemListView.as_view(), name='equipment-stock-search'),
]