from django.urls import path, include

from investment.views import (
    InvestmentView,
    InvestmentDetailView,
)

# /investments
urlpatterns = [
    path('', InvestmentView.as_view()),
    path('/<int:id>', InvestmentDetailView.as_view())
]
