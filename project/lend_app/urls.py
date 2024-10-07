from django.urls import path
from .views import BorrowerView, BorrowerRegisterView #Borrower
urlpatterns = [
    path('borrowers/', BorrowerView.as_view(), name='borrower-list'),
    path('borrowers/register/', BorrowerRegisterView.as_view(), name='borrower-register'),
]