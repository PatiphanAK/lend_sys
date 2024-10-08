from django.urls import path
from .views import BorrowerListView, BorrowerRegisterView, ApproverListView, ApproverRegisterView, ItemListView, ItemDetailView
urlpatterns = [
    path('borrowers/', BorrowerListView.as_view(), name='borrower-list'),
    path('approvers/', ApproverListView.as_view(), name='borrower-list'),
    path('borrowers/register/', BorrowerRegisterView.as_view(), name='borrower-register'),
    path('approvers/register/', ApproverRegisterView.as_view(), name='borrower-register'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]