from django.urls import path

from deposit.views import DepositView


urlpatterns = [
    # /deposit
    path('', DepositView.as_view()),
]

