from django.urls import path
from .views import BorrowerView
urlpatterns = [
    path('borrowers/', BorrowerView.as_view(), name='borrower-list'),
]