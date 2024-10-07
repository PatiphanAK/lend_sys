from django.urls import path
from .views import BorrowerListView, BorrowerRegisterView
urlpatterns = [
    path('borrowers/', BorrowerListView.as_view(), name='borrower-list'),
    path('borrowers/register/', BorrowerRegisterView.as_view(), name='borrower-register'),
    path('approvers/'),
]